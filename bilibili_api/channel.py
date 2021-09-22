"""
bilibili_api.channel

频道相关操作。
"""

import json
import os

from .exceptions import ArgsException
from .utils.utils import get_api
from .utils.network import request
from .utils.Credential import Credential

API = get_api("channel")


def get_channel_info_by_tid(tid: int):
    """
    根据 tid 获取频道信息。

    Args:
        tid (int):               频道的 tid。

    Returns:
        `tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。
    """
    with open(os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8") as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if "tid" not in main_ch:
            continue
        if tid == int(main_ch["tid"]):
            return main_ch, None

        # 搜索子分区
        for sub_ch in main_ch["sub"]:
            if "tid" not in sub_ch:
                continue
            if tid == sub_ch["tid"]:
                return main_ch, sub_ch
    else:
        return None, None


def get_channel_info_by_name(name: str):
    """
    根据频道名称获取频道信息。

    Args:
        name (str):               频道的名称。

    Returns:
        tuple[dict | None, dict | None]: 第一个是主分区，第二个是子分区，没有时返回 None。
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
    获取分区前十排行榜。

    Args:
        tid (int):                          频道的 tid。
        day (int, optional):                          3 天排行还是 7 天排行。 Defaults to 7.
        credential (Credential, optional):  Credential 类。Defaults to None.

    Returns:
        list: 前 10 的视频信息。
    """
    if credential is None:
        credential = Credential()
    if day not in (3, 7):
        raise ArgsException("参数 day 只能是 3，7。")

    url = API["ranking"]["get_top10"]["url"]
    params = {
        "rid": tid,
        "day": day
    }
    return await request("GET", url, params=params, credential=credential)
