# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name,consider-using-f-string,line-too-long
import re
import os
import threading
import subprocess
from urllib import parse
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
            with open(os.path.join(self.data_path,script), "r", encoding="utf-8") as f:
                fcontent=f.read()
                if "@match" not in fcontent:
                    formatted_scripts += "<script>" + fcontent + "</script>"
                else:
                    for i in fcontent.splitlines():
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
                                formatted_scripts += "<script>" + fcontent + "</script>"
                                break
        return formatted_scripts

    # MARK: Script Generating
    def request(self, flow: http.HTTPFlow):
        if flow.request.host == "any.where":
            if flow.request.path_components[-1] == "userscript":
                flow.response = http.Response.make(
                    200,
                    bytes(
                        self._load_scripts(parse.unquote(flow.request.query)),
                        encoding="utf-8",
                    ),
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
                    re.sub(
                        r"</head>",
                        f"{self._load_scripts(flow.request.url)}</head>",
                        flow.response.get_text(),
                        count=1,
                    )
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
            script_file_name = flow.request.path_components[-1]
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
            if os.name == "nt":
                # TODO: script logo
                subprocess.Popen(
                    [
                        "powershell",
                        "-ep",
                        "Bypass",
                        "-File",
                        "win/toast.ps1",
                        os.getcwd(),
                        script_name,
                        script_file_name,
                    ]
                )
            else:
                pass


addons = [addon()]
