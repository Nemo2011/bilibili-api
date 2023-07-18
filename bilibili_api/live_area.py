"""
bilibili_api.live_area

直播间分区相关操作。
"""

import os
import copy
import json
from enum import Enum
from typing import Dict, List, Tuple, Union

from .utils.utils import get_api
from .utils.network_httpx import request

API = get_api("live-area")


class LiveRoomOrder(Enum):
    """
    直播间排序方式

    - RECOMMEND: 综合
    - NEW: 最新
    """

    RECOMMEND = ""
    NEW = "live_time"


def get_area_info_by_id(id: int) -> Tuple[Union[dict, None], Union[dict, None]]:
    """
    根据 id 获取分区信息。

    Args:
        id (int): 分区的 id。

    Returns:
        `Tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。
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
                if str(id) == sub_ch["id"]:
                    return main_ch, sub_ch
    else:
        return None, None


def get_area_info_by_name(name: str) -> Tuple[Union[dict, None], Union[dict, None]]:
    """
    根据频道名称获取频道信息。

    Args:
        name (str): 分区的名称。

    Returns:
        Tuple[dict | None, dict | None]: 第一个是主分区，第二个是子分区，没有时返回 None。
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


def get_area_list() -> List[Dict]:
    """
    获取所有分区的数据

    Returns:
        List[dict]: 所有分区的数据
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


def get_area_list_sub() -> dict:
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


async def get_list_by_area(
    area_id: int, page: int = 1, order: LiveRoomOrder = LiveRoomOrder.RECOMMEND
) -> dict:
    """
    根据分区获取直播间列表

    Args:
        area_id (int)          : 分区 id

        page    (int)          : 第几页. Defaults to 1.

        order   (LiveRoomOrder): 直播间排序方式. Defaults to LiveRoomOrder.RECOMMEND.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["list"]
    params = {
        "platform": "web",
        "parent_area_id": get_area_info_by_id(area_id)[0]["id"],
        "area_id": 0 if (get_area_info_by_id(area_id)[1] == None) else area_id,
        "page": page,
        "sort_type": order.value,
    }
    return await request("GET", api["url"], params=params)
