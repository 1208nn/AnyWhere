# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name
from addon import addon
import CurrOS
from backend import ThreadedMitmProxy

try:
    CurrOS.setProxy("127.0.0.1", "8080")
except AttributeError:
    pass

if __name__ == "__main__":
    from mitmproxy.tools.main import mitmdump

    mitmdump(args=["-s", "addon.py"])

with ThreadedMitmProxy(addon, listen_port=8080, listen_host="127.0.0.1"):
    input()

CurrOS.clearProxy()
