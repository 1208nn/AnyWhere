# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name,consider-using-f-string,line-too-long
import re
import os
from urllib.parse import unquote
import threading
import subprocess
from mitmproxy import http
import CurrOS


class addon:
    def __init__(self):
        self.data_path = os.path.join(CurrOS.appdata_path, "n0", "AnyWhere")
        self.iframe_src = []
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    # MARK: Scripts Loading
    # TODO: Change Loading whole js to many single ones
    def _load_scripts(self, url):
        scripts = [
            filename
            for filename in os.listdir(self.data_path)
            if filename.endswith(".user.js")
        ]
        formatted_scripts = ""
        for script in scripts:
            with open(script, "r", encoding="utf-8") as f:
                if "@match" not in f.read():
                    formatted_scripts += f.read()
                else:
                    for i in f.readline():
                        if i == "// ==/UserScript==":
                            break
                        if "@match" in i:
                            if re.match(
                                re.compile(
                                    re.escape(i.split("@match").strip()).replace(
                                        "\\*", ".*"
                                    )
                                ),
                                url,
                            ):
                                formatted_scripts += f.read()
                                break
        return formatted_scripts

    # MARK: Script Generating
    def request(self, flow: http.HTTPFlow):
        if flow.request.host == "any.where":
            if flow.request.path == "/getuserscript":
                flow.response = http.Response.make(
                    200,
                    bytes(self._load_scripts(flow.request.query), encoding="utf-8"),
                    {"Content-Type": "text/javascript"},
                )
        elif flow.request.url.endswith(".user.js"):
            flow.request.headers["Cache-Control"] = "no-cache"
            flow.request.headers["Pragma"] = "no-cache"
            flow.request.headers["If-Modified-Since"] = "0"

    # MARK: Response
    def response(self, flow: http.HTTPFlow):
        if flow.response.headers.get("content-type", "").startswith("text/html"):
            # MARK: Iframe dealing
            iframe_src = re.findall(
                r'<iframe[^>]*src="([^"]+)"[^>]*>',
                flow.response.get_text(),
            )
            if flow.request.url in self.iframe_src:
                self.iframe_src.remove(flow.request.url)
            else:
                flow.response.set_text(
                    f'<script src="http://any.where/getuserscript?{flow.request.url}"></script>'
                    + flow.response.get_text()
                )
            self.iframe_src += iframe_src
            for i in iframe_src:
                threading.Timer(
                    60,
                    lambda j=i: (
                        self.iframe_src.remove(j) if j in self.iframe_src else None
                    ),
                ).start()
        # MARK: Script Installing
        elif flow.request.url.endswith(".user.js"):
            script_file_name = unquote(flow.request.url.split("/")[-1])
            script_name = (
                flow.response.get_text().split("@name")[1].split("\n")[0].strip()
                if "@name" in flow.response.get_text()
                else script_file_name
            )
            os.makedirs(os.path.join(os.environ["TEMP"], "anywhere"), exist_ok=True)
            with open(
                os.path.join(os.environ["TEMP"], "anywhere", script_file_name),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(flow.response.get_text())
            if os.name == "nt":  # A really good experience for Windows
                subprocess.Popen(
                    [
                        "powershell",
                        "-ep",
                        "Bypass",
                        "-File",
                        "win/toast.ps1",
                        r'''# TODO: change method for push toast,not finished this is old one
                        "--app-id",
                        "Anywhere",
                        "--title",
                        "New Userscript Detected",
                        "--message",
                        "Click to check{script}. You can also install it directly, or ignore it.".format(
                            script=(
                                (" " + script_name)
                                if all(ord(c) < 128 for c in script_name)
                                else ""
                            )
                        ),
                        "--icon",
                        os.path.join(os.getcwd(), "A.png"),
                        "--audio",
                        "default",
                        "--loop",
                        "--duration",
                        "long",
                        "--activation-arg",
                        "anywhere:check/{script}".format(script=script_file_name),
                        "--action",
                        "Install",
                        "--action-arg",
                        "anywhere:install/{script}".format(script=script_file_name),
                        "--action",
                        "Ignore",
                        "--action-arg",
                        "anywhere:decline/{script}".format(script=script_file_name),
                        '''
                    ]
                )
            else:
                pass


addons = [addon()]
