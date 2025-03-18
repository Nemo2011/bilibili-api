"""
bilibili_api.live_area

直播间分区相关操作。
"""

import os
import copy
import json
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from .utils.utils import get_api
from .utils.network import Api, Credential
from .live import get_area_info
from .exceptions import ApiException

API = get_api("live-area")


live_area_data = None


async def fetch_live_area_data() -> None:
    """
    抓取直播分区数据

    因为直播分区容易出现变动，故不像视频分区一样直接使用文件保存，而是每次查询时先抓取一遍。

    一次运行整个程序仅需执行一次此函数即可，无需多次调用。
    """
    global live_area_data
    live_area_data = await get_area_info()


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
        Tuple[dict | None, dict | None]: 第一个是主分区，第二个是子分区，没有时返回 None。
    """
    global live_area_data
    if not live_area_data:
        raise ApiException("请先调用 fetch_live_area_data()")
    channel = live_area_data

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
    global live_area_data
    if not live_area_data:
        raise ApiException("请先调用 fetch_live_area_data()")
    channel = live_area_data

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
    global live_area_data
    if not live_area_data:
        raise ApiException("请先调用 fetch_live_area_data()")
    channel = live_area_data
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
    global live_area_data
    if not live_area_data:
        raise ApiException("请先调用 fetch_live_area_data()")
    channel = live_area_data
    return channel


async def get_list_by_area(
    area_id: int,
    page: int = 1,
    order: LiveRoomOrder = LiveRoomOrder.RECOMMEND,
    credential: Optional[Credential] = None,
) -> dict:
    """
    根据分区获取直播间列表

    Args:
        area_id    (int)                 : 分区 id

        page       (int)                 : 第几页. Defaults to 1.

        order      (LiveRoomOrder)       : 直播间排序方式. Defaults to LiveRoomOrder.RECOMMEND.

        credential (Credential, optional): 凭据类. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    api = API["info"]["list"]
    params = {
        "platform": "web",
        "parent_area_id": get_area_info_by_id(area_id)[0]["id"],
        "area_id": 0 if (get_area_info_by_id(area_id)[1] == None) else area_id,
        "page": page,
        "sort_type": order.value,
    }
    return await Api(**api, credential=credential).update_params(**params).result
