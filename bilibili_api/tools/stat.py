import json
import os
from bilibili_api import utils

count = 0


def get_api_total_count():
    def handle(d: dict):
        for key, value in d.items():
            if type(value) == dict:
                if "url" not in value:
                    handle(value)
                else:
                    global count
                    count += 1
    global count
    api = utils.get_api()
    handle(api)
    print("总共API数量：", count)


def get_total_line():
    line = 0
    file_count = 0
    char_count = 0
    for root, dirs, files in os.walk(utils.get_project_path()):
        if os.path.basename(root) == "__pycache__":
            continue
        for file in files:
            file_count += 1
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf8") as f:
                data = f.read()
                line += len(data.splitlines())
                char_count += len(data)
    print(f"共有文件：{file_count} 个，总行数：{line} 行，总字符数：{char_count} 个")

