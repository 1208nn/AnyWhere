# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name,pointless-string-statement
import pystray
from pystray import MenuItem as item
from PIL import Image
from addon import addon
import CurrOS
from backend import ThreadedMitmProxy, clean_temp

clean_temp()

with ThreadedMitmProxy(addon, listen_port=8080, listen_host="127.0.0.1"):
    try:
        CurrOS.setProxy("127.0.0.1", "8080")
    except AttributeError:
        pass

    def close(icon, item):
        icon.stop()

    pystray.Icon(
        "AnyWhere",
        Image.open("D:\\Profile\\Documents\\Codes\\AnyWhere\\assets\\A.png"),
        "AnyWhere",
        [item("Exit", close)],
    ).run()

    CurrOS.clearProxy()

"""if __name__ == "__main__":
    from mitmproxy.tools.main import mitmdump

    mitmdump(
        args=["-s", "addon.py", "--listen-port", "8080", "--listen-host", "127.0.0.1"]
    )"""

clean_temp()
