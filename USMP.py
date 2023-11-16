import os, CurrOS
from mitmproxy import http, ctx, options, master
from re import sub
import mitmproxy
from mitmproxy.tools.main import mitmdump
import sys

last_modified_time = None
file_dir = os.path.dirname(os.path.abspath(__file__))


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


def check_directory_changes():
    global last_modified_time
    # 获取目录元数据
    stat_info = os.stat(file_dir)
    # 获取目录的最后修改时间
    current_modified_time = stat_info.st_mtime
    # 比较目录的最后修改时间和上一次记录的时间戳
    if last_modified_time is None or current_modified_time > last_modified_time:
        # 目录有更改，重新加载
        load_scripts()
    # 更新上一次记录的时间戳
    last_modified_time = current_modified_time


def response(flow):
    check_directory_changes()
    # 检查响应的Content-Type是否为text/html
    if flow.response.headers.get("content-type", "").startswith("text/html"):
        flow.response.set_text(
            sub(
                r"</head>",
                f"{formatted_scripts}</head>",
                flow.response.get_text(),
                count=1,
            )
        )


check_directory_changes()
CurrOS.setProxy("127.0.0.1", "8080")


def done():
    CurrOS.clearProxy()


addons = [response, done]
