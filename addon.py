# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name,consider-using-f-string,line-too-long
from re import sub, finditer
import os
from urllib.parse import unquote
import threading
import subprocess
import CurrOS


class addon:
    def __init__(self):
        self.formatted_scripts = ""
        self.data_path = os.path.join(CurrOS.appdata_path, "n0", "AnyWhere")
        self.iframe_src = []
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    # MARK: Scripts Loading
    def _load_scripts(self):
        scripts = [
            filename
            for filename in os.listdir(self.data_path)
            if filename.endswith(".user.js")
        ]
        self.formatted_scripts = ""
        for script in scripts:
            with open(script, "r", encoding="utf-8") as f:
                self.formatted_scripts += f"<script>{f.read()}</script>"
        htmls = [
            filename
            for filename in os.listdir(self.data_path)
            if filename.endswith(".html")
        ]
        for html in htmls:
            with open(html, "r", encoding="utf-8") as f:
                self.formatted_scripts += f.read()

    # MARK: Response
    def response(self, flow):
        if flow.response.headers.get("content-type", "").startswith("text/html"):
            # MARK: Iframe dealing
            if flow.request.url in self.iframe_src:
                self.iframe_src.remove(flow.request.url)
            else:
                iframe_src = [
                    match.group(1)
                    for match in finditer(
                        r'<iframe\s+src="([^"]+)"(?!(?:[^<]+)?>(?:[^<]*<(?:(?!</iframe>)<)[^<]*)*</iframe>)',
                        flow.response.get_text(),
                    )
                ]
                self.iframe_src += iframe_src
                for i in iframe_src:
                    threading.Timer(60, lambda j=i: self.iframe_src.remove(j)).start()
                self._load_scripts()
                # MARK: Scripts injecting
                flow.response.set_text(
                    sub(
                        r"</head>",
                        f"{self.formatted_scripts}</head>",
                        flow.response.get_text(),
                        count=1,
                    )
                )
        # MARK: Script Installing
        elif flow.request.url.endswith(".user.js"):
            script_name = (
                flow.response.get_text().split("// @name")[1].split("\n")[0].strip()
            )
            script_file_name = unquote(flow.request.url.split("/")[-1].split("?")[0])
            if not all(ord(c) < 128 for c in script_name):
                script_name = script_file_name
            if not all(ord(c) < 128 for c in script_file_name):
                script_file_name = str(hash(script_name)) + ".user.js"
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
                        r".\bin\win\toast64.exe",
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
                    ]
                )
            else:
                pass


addons = [addon()]
