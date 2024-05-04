# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name,pointless-string-statement
from addon import addon
import CurrOS
from backend import ThreadedMitmProxy, clean_temp


clean_temp()
try:
    CurrOS.setProxy("127.0.0.1", "8080")
except AttributeError:
    pass

with ThreadedMitmProxy(addon, listen_port=8080, listen_host="127.0.0.1"):
    input()

"""if __name__ == "__main__":
    from mitmproxy.tools.main import mitmdump

    mitmdump(
        args=["-s", "addon.py", "--listen-port", "8080", "--listen-host", "127.0.0.1"]
    )"""

CurrOS.clearProxy()

clean_temp()
