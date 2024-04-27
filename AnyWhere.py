import os, CurrOS
from re import sub


file_dir = os.path.dirname(os.path.abspath(__file__))
formatted_scripts = ""


def load_scripts():
    global formatted_scripts
    scripts = [
        filename for filename in os.listdir(file_dir) if filename.endswith(".user.js")
    ]
    formatted_scripts = ""
    for script in scripts:
        with open(script, "r", encoding="utf-8") as f:
            formatted_scripts += f"<script>{f.read()}</script>"
    htmls = [
        filename for filename in os.listdir(file_dir) if filename.endswith(".html")
    ]
    for html in htmls:
        with open(html, "r", encoding="utf-8") as f:
            formatted_scripts += f.read()


def response(flow):
    if flow.response.headers.get("content-type", "").startswith("text/html"):
        load_scripts()
        flow.response.set_text(
            sub(
                r"</head>",
                f"{formatted_scripts}</head>",
                flow.response.get_text(),
                count=1,
            )
        )


def done():
    CurrOS.clearProxy()


addons = [response, done]
CurrOS.setProxy("127.0.0.1", "8080")
