# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
# pylint: disable=invalid-name
from re import sub
import os
import CurrOS


class addon:
    def __init__(self):
        self.formatted_scripts = ""
        self.data_path = CurrOS.appdata_path + "\\n0\\AnyWhere\\"
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

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

    def response(self, flow):
        if flow.response.headers.get("content-type", "").startswith("text/html"):
            self._load_scripts()
            flow.response.set_text(
                sub(
                    r"</head>",
                    f"{self.formatted_scripts}</head>",
                    flow.response.get_text(),
                    count=1,
                )
            )


addons = [addon()]
