"""
bilibili_api.channel

频道相关操作
"""

import json
import os
from .exceptions import ArgsException
from .utils.utils import get_api
from .utils.network import request
from .utils.Credential import Credential

API = get_api("channel")


async def get_channel_info_by_tid(tid: int):
    """
    根据tid获取频道信息。
    Args:
        tid (int):               频道的tid。
    Returns:
        dict, 第一个是主分区，第二个是子分区，没有时返回None
    """
    with open(os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8") as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if "tid" not in main_ch:
            continue
        if tid == int(main_ch["tid"]):
            return main_ch, None
        for sub_ch in main_ch["sub"]:
            if "tid" not in sub_ch:
                continue
            if tid == sub_ch["tid"]:
                return main_ch, sub_ch
    else:
        return None, None


async def get_channel_info_by_name(name: str):
    """
    根据频道名称获取频道信息。
    Args:
        name (str):               频道的名称。
    Returns:
        dict, 第一个是主分区，第二个是子分区，没有时返回None
    """
    with open(os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8") as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if name in main_ch["name"]:
            return main_ch, None
        for sub_ch in main_ch["sub"]:
            if name in sub_ch["name"]:
                return main_ch, sub_ch
    else:
        return None, None


async def get_top10(tid: int, day: int = 7, credential: Credential = None):
    """
    获取分区前十排行榜
    Args:
        tid (int):               频道的tid。
        day (int):               可选3或者7. Defaults to 7.
        credential (Credential, optional):  Credential 类. Defaults to None.
    Returns:
        list, 前10的视频信息
    """
    if credential is None:
        credential = Credential()
    if day not in (3, 7):
        raise ArgsException("day只能是3，7")

    url = API["ranking"]["get_top10"]["url"]
    params = {
        "rid": tid,
        "day": day
    }
    resp = await request("GET", url, params=params, credential=credential)
    return resp
