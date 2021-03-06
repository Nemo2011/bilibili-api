r"""
模块：channel
功能：频道相关
项目GitHub地址：https://github.com/Passkou/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/4
"""
import os
import json
from . import utils, exceptions

API = utils.get_api()


def get_channel_info_by_tid(tid: int):
    """
    根据tid获取频道信息
    :param tid:
    :return: 第一个是主分区，第二个是子分区，没有时返回None
    """
    with open(os.path.join(utils.get_project_path(), "data/channel.json"), encoding="utf8") as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if "tid" not in main_ch:
            continue
        if tid == int(main_ch["tid"]):
            return main_ch, None
        for sub_ch in main_ch["sub"]:
            if tid == sub_ch["tid"]:
                return main_ch, sub_ch
    else:
        return None, None


def get_channel_info_by_name(name: str):
    """
    根据名字获取频道信息
    :param name:
    :return: 第一个是主分区，第二个是子分区，没有时返回None
    """
    with open(os.path.join(utils.get_project_path(), "data/channel.json"), encoding="utf8") as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if name in main_ch["name"]:
            return main_ch, None
        for sub_ch in main_ch["sub"]:
            if name in sub_ch["name"]:
                return main_ch, sub_ch
    else:
        return None, None


def get_top10(tid: int, day: int = 7, verify: utils.Verify = None):
    """
    获取分区前十排行榜
    :param tid: 0为主页
    :param day:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if day not in (3, 7):
        raise exceptions.BilibiliApiException("day只能是3，7")

    api = API["channel"]["ranking"]["get_top10"]
    params = {
        "rid": tid,
        "day": day
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp