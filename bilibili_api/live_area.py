"""
bilibili_api.live_area

直播间分区相关操作。
"""

import json
import os
import copy
from typing import Union

def get_channel_info_by_tid(id: int) -> tuple[Union[dict, None], Union[dict, None]]:
    """
    根据 id 获取分区信息。

    Args:
        id (int): 分区的 id。

    Returns:
        `tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/live_area.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if "id" not in main_ch:
            continue
        if id == int(main_ch["id"]):
            return main_ch, None

        # 搜索子分区
        if "list" in main_ch.keys():
            for sub_ch in main_ch["list"]:
                if "id" not in sub_ch:
                    continue
                if id == sub_ch["id"]:
                    return main_ch, sub_ch
    else:
        return None, None


def get_channel_info_by_name(name: str) -> tuple[Union[dict, None], Union[dict, None]]:
    """
    根据频道名称获取频道信息。

    Args:
        name (str): 分区的名称。

    Returns:
        tuple[dict | None, dict | None]: 第一个是主分区，第二个是子分区，没有时返回 None。
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/live_area.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if name in main_ch["name"]:
            return main_ch, None
        if "list" in main_ch.keys():
            for sub_ch in main_ch["list"]:
                if name in sub_ch["name"]:
                    return main_ch, sub_ch
    else:
        return None, None


def get_channel_list() -> list[dict]:
    """
    获取所有分区的数据

    Returns:
        list[dict]: 所有分区的数据
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/live_area.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())
    channel_list = []
    for channel_big in channel:
        channel_big_copy = copy.copy(channel_big)
        channel_list.append(channel_big_copy)
        if "list" in channel_big.keys():
            channel_big_copy.pop("list")
            for channel_sub in channel_big["list"]:
                channel_sub_copy = copy.copy(channel_sub)
                channel_sub_copy["father"] = channel_big_copy
                channel_list.append(channel_sub_copy)
    return channel_list


def get_channel_list_sub() -> dict:
    """
    获取所有分区的数据
    含父子关系（即一层次只有主分区）

    Returns:
        dict: 所有分区的数据
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/live_area.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())
    return channel
