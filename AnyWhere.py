# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name,pointless-string-statement
import sys
import os
import shutil
import pystray
from pystray import MenuItem
from PIL import Image
from addon import addon
import CurrOS
from backend import ThreadedMitmProxy, clean_temp


if len(sys.argv) > 1:
    operation_type, arg = sys.argv[1].split(":")[1].split("/", maxsplit=1)
    if operation_type == "install":
        shutil.move(
            os.path.join(os.environ["TEMP"], "AnyWhere", arg),
            os.path.join(CurrOS.appdata_path, "n0", "AnyWhere", arg),
        )
    elif operation_type == "check":
        pass  # TODO:Not Developed Yet
    elif operation_type == "dismiss":
        os.remove(os.path.join(os.environ["TEMP"], "anywhere", arg))
    elif operation_type == "mute":
        pass  # TODO:mute

else:
    clean_temp()
    # MARK: Start App
    # For packed
    # Only support proxy auto set on Windows now
    # It's better to be packed without console
    if getattr(sys, "frozen", False):
        os.chdir(os.path.dirname(sys.executable))
        with ThreadedMitmProxy(addon, listen_port=8080, listen_host="127.0.0.1"):
            try:
                CurrOS.setProxy("127.0.0.1", "8080")
            except AttributeError:
                pass

            def close(icon, _):
                icon.stop()

            pystray.Icon(
                "AnyWhere",
                Image.open("D:\\Profile\\Documents\\Codes\\AnyWhere\\assets\\A.png"),
                "AnyWhere",
                [MenuItem("Exit", close)],
            ).run()

            CurrOS.clearProxy()
    # MARK: Debug Mode
    # When not packed, no proxy auto set support
    else:
        os.chdir(os.path.dirname(__file__))
        from mitmproxy.tools.main import mitmdump

        mitmdump(
            args=[
                "-s",
                "addon.py",
                "--listen-port",
                "8080",
                "--listen-host",
                "127.0.0.1",
            ]
        )

    clean_temp()
