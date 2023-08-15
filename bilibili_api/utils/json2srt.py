# https://blog.csdn.net/mondaiji/article/details/104294430
# author: 皓空Fly
# 此文件采用 CC 4.0 BY-SA 协议开源。

import os
import json
import math


def json2srt(doc: str, out: str):
    """
    Args:
        doc: 文件

    Returns:
        None
    """
    file = ""  # 这个变量用来保存数据
    i = 1
    with open(doc, encoding="utf-8") as f:
        datas = json.load(f)  # 加载文件数据
        f.close()
    for data in datas["body"]:
        start = data["from"]  # 获取开始时间
        stop = data["to"]  # 获取结束时F间
        content = data["content"]  # 获取字幕内容
        file += "{}\n".format(i)  # 加入序号
        hour = math.floor(start) // 3600
        minute = (math.floor(start) - hour * 3600) // 60
        sec = math.floor(start) - hour * 3600 - minute * 60
        minisec = int(math.modf(start)[0] * 100)  # 处理开始时间
        file += (
            str(hour).zfill(2)
            + ":"
            + str(minute).zfill(2)
            + ":"
            + str(sec).zfill(2)
            + ","
            + str(minisec).zfill(2)
        )  # 将数字填充0并按照格式写入
        file += " --> "
        hour = math.floor(stop) // 3600
        minute = (math.floor(stop) - hour * 3600) // 60
        sec = math.floor(stop) - hour * 3600 - minute * 60
        minisec = abs(int(math.modf(stop)[0] * 100 - 1))  # 此处减1是为了防止两个字幕同时出现
        file += (
            str(hour).zfill(2)
            + ":"
            + str(minute).zfill(2)
            + ":"
            + str(sec).zfill(2)
            + ","
            + str(minisec).zfill(2)
        )
        file += "\n" + content + "\n\n"  # 加入字幕文字
        i += 1
    with open(out, "w+", encoding="utf-8") as f:
        f.write(file)  # 将数据写入文件
        f.close()
