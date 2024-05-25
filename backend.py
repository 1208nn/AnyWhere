# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name
import asyncio
import threading
from typing import Any, Callable, Self
import shutil
import os

from mitmproxy.addons import default_addons, script
from mitmproxy.master import Master
from mitmproxy.options import Options


class ThreadedMitmProxy(threading.Thread):
    def __init__(self, user_addon: Callable, **options: Any) -> None:
        self.loop = asyncio.new_event_loop()
        self.master = Master(Options(), event_loop=self.loop)
        # replace the ScriptLoader with the user addon
        self.master.addons.add(
            *(
                user_addon() if isinstance(addon, script.ScriptLoader) else addon
                for addon in default_addons()
            )
        )
        # set the options after the addons since some options depend on addons
        self.master.options.update(**options)
        super().__init__()

    def run(self) -> None:
        self.loop.run_until_complete(self.master.run())

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, *_) -> None:
        self.master.shutdown()
        self.join()


def clean_temp():
    try:
        shutil.rmtree(os.path.join(os.environ['TEMP'], "AnyWhere"))
    except FileNotFoundError:
        pass
