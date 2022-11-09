"""
bilibili_api.channel

频道相关操作。
"""

import json
import os
import copy

from .exceptions import ArgsException
from .utils.utils import get_api
from .utils.network_httpx import request
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
    with open(
        os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if "tid" not in main_ch:
            continue
        if tid == int(main_ch["tid"]):
            return main_ch, None

        # 搜索子分区
        if "sub" in main_ch.keys():
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
    with open(
        os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if name in main_ch["name"]:
            return main_ch, None
        if "sub" in main_ch.keys():
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
    params = {"rid": tid, "day": day}
    return await request("GET", url, params=params, credential=credential)


def get_channel_list():
    """
    获取所有分区的数据

    Returns:
        dict: 所有分区的数据
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())
    channel_list = []
    for channel_big in channel:
        channel_big_copy = copy.copy(channel_big)
        channel_list.append(channel_big_copy)
        if "sub" in channel_big.keys():
            channel_big_copy.pop("sub")
            for channel_sub in channel_big["sub"]:
                channel_sub_copy = copy.copy(channel_sub)
                channel_sub_copy["father"] = channel_big_copy
                channel_list.append(channel_sub_copy)
    return channel_list


def get_channel_list_sub():
    """
    获取所有分区的数据
    含父子关系（即一层次只有主分区）

    Returns:
        dict: 所有分区的数据
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())
    return channel


async def get_channel_videos_count_today(credential: Credential = None):
    """
    获取每个分区当日最新投稿数量

    Args:
        credential(Credential): 凭据类
    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    api = API["count"]
    return (await request("GET", api["url"], credential=credential))["region_count"]


async def get_channel_new_videos(tid: int, credential: Credential = None):
    """
    获取分区最新投稿

    Args:
        tid(int)              : 分区 id
        credential(Credential): 凭据类
    """
    credential = credential if credential else Credential()
    api = API["new"]
    params = {"rid": tid}
    return await request("GET", api["url"], params=params, credential=credential)
