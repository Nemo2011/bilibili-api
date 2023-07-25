"""
bilibili_api.channel

频道相关，与视频分区不互通。
"""
import re
import json
from enum import Enum
from typing import List, Union, Optional

from bilibili_api.utils.utils import get_api
from bilibili_api.utils.credential import Credential
from bilibili_api.utils.initial_state import get_initial_state
from bilibili_api.errors import ApiException, ResponseException
from bilibili_api.utils.network_httpx import request, Api

API = get_api("channel")


async def get_channel_categories() -> dict:
    """
    获取所有的频道分类（如游戏、鬼畜等）。

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["categories"]["list"]
    return await Api(**api).result


async def get_channel_category_detail(
    category_id: int, offset: str = "0", credential: Optional[Credential] = None
) -> dict:
    """
    获取频道分类的频道列表及其详细信息

    Args:
        category_id (int): 频道分类的 id。

        offset      (str): 偏移值（下面的数据的第一个频道 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to "0"
    """
    credential = credential if credential else Credential()
    api = API["categories"]["sub_channels"]
    params = {"id": category_id, "offset": offset}
    return await Api(**api, credential=credential).update_params(**params).result


class ChannelVideosOrder(Enum):
    """
    频道视频排序方式。

    - NEW: 最新
    - HOT: 最火
    - VIEW: 播放量最高
    """

    NEW = "new"
    HOT = "hot"
    VIEW = "view"


class ChannelVideosFilter(Enum):
    """
    频道视频筛选条件

    - ALL     : 全部
    - YEAR_年份: 指定年份筛选
    """

    ALL = 0
    YEAR_2023 = 2023
    YEAR_2022 = 2022
    YEAR_2021 = 2021
    YEAR_2020 = 2020
    YEAR_2019 = 2019
    YEAR_2018 = 2018
    YEAR_2017 = 2017
    YEAR_2016 = 2016
    YEAR_2015 = 2015
    YEAR_2014 = 2014
    YEAR_2013 = 2013
    YEAR_2012 = 2012
    YEAR_2011 = 2011


class Channel:
    """
    频道类。
    """

    def __init__(self, channel_id: int):
        """
        Args:
            channel_id (int): 频道 id.
        """
        self.__channel_id = channel_id

    def get_channel_id(self) -> int:
        return self.__channel_id

    async def get_info(self) -> dict:
        """
        获取频道详细信息

        Returns:
            dict: HTML 中 window.__INITIAL_STATE__ 中的信息
        """
        return await get_initial_state(
            f"https://www.bilibili.com/v/channel/{self.get_channel_id()}"
        )

    async def get_related_channels(self) -> List[dict]:
        """
        获取相关频道

        Returns:
            dict: HTML 中 window.__INITIAL_STATE__ 中的信息
        """
        return (await self.get_info())["channelDetailBanner"]["data"]["tag_channels"]

    def only_achieve(self, info: list) -> List[dict]:
        """
        只返回 card_type=achieve 的数据

        Args:
            info (list): 待筛选的数据

        Returns:
            list: card_type=achieve 的数据
        """
        results = []
        for obj in info:
            if obj.get("card_type") == "archive":
                results.append(obj)
        return results

    async def get_featured_list(
        self,
        filter: ChannelVideosFilter = ChannelVideosFilter.ALL,
        offset: Optional[str] = None,
        page_size: int = 30,
    ) -> dict:
        """
        获取频道精选视频

        Args:
            filter          (ChannelVideosFilter)       : 获取视频的相关选项. Defaults to ALL

            offset          (str)                       : 偏移值（下面的第一个视频的 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to None

            page_size       (int)                       : 每页的数据大小. Defaults to 30

        Returns:
            dict: 调用 API 返回的结果
        """
        # page_size 默认设置为网页端的 30
        api = API["channel"]["list_featured"]
        params = {"channel_id": self.get_channel_id()}
        if isinstance(filter, ChannelVideosFilter):
            params["filter_type"] = filter.value
        if offset is not None:
            params["offset"] = offset
        params["page_size"] = page_size
        info = await Api(**api).update_params(**params).result

        # 如果频道与番剧有关，会有番剧信息，需要排除掉 card_type=season 的数据
        info["list"] = self.only_achieve(info["list"])
        return info

    async def get_raw_list(
        self,
        order: ChannelVideosOrder = ChannelVideosOrder.HOT,
        offset: Optional[str] = None,
        page_size: int = 30,
    ) -> dict:
        """
        获取频道视频列表原数据

        Args:
            order          (ChannelVideosOrder)         : 排序方式. Defaults to HOT

            offset         (str)                        : 偏移值（下面的第一个视频的 ID，为该请求结果中的 offset 键对应的值），类似单向链表

            page_size      (int)                        : 每页的数据大小

        Returns:
            dict: 调用 API 返回的结果
        """
        # page_size 默认设置为网页端的 30
        api = API["channel"]["list_multiple"]
        params = {
            "channel_id": self.get_channel_id(),
            "offset": offset,
            "page_size": page_size,
        }
        if isinstance(order, ChannelVideosOrder):
            params["sort_type"] = order.value
        if offset is not None:
            params["offset"] = offset
        params["page_size"] = page_size

        return await Api(**api).update_params(**params).result

    async def get_list(
        self,
        order: ChannelVideosOrder = ChannelVideosOrder.HOT,
        offset: Optional[str] = None,
        page_size: int = 30,
    ) -> dict:
        """
        获取频道视频列表

        Args:
            order          (ChannelVideosOrder)         : 排序方式. Defaults to HOT

            offset         (str)                        : 偏移值（下面的第一个视频的 ID，为该请求结果中的 offset 键对应的值），类似单向链表

            page_size      (int)                        : 每页的数据大小

        Returns:
            dict: 调用 API 返回的结果
        """

        info = await self.get_raw_list(order, offset, page_size)

        # 如果频道与番剧有关，会有番剧信息，需要排除掉 card_type=rank 的数据
        info["list"] = self.only_achieve(info["list"])
        return info

    async def get_channel_video_rank(self) -> List[dict]:
        """
        获取频道热门视频排行榜

        Returns:
            List[dict]: 热门视频排行榜
        """

        info = await self.get_raw_list(order=ChannelVideosOrder.HOT)
        rank = info["list"][0]
        if rank["card_type"] == "rank":
            return rank["items"]


async def get_channels_in_category(category_id: int) -> List["Channel"]:
    """
    获取频道分类中的所有频道。

    Args:
        category_id (int): 频道 id

    Returns:
        List[Channel]: 频道分类中的所有频道。
    """
    channel_list = []
    offset = "0"
    while True:
        raw_data = await get_channel_category_detail(
            category_id=category_id, offset=offset
        )
        channel_list += raw_data["archive_channels"]
        if not raw_data["has_more"]:
            break
        else:
            offset = raw_data["offset"]
    channel_objects = []
    for channel in channel_list:
        channel_objects.append(Channel(channel["id"]))
    return channel_objects


async def get_self_subscribe_channels(credential: Credential) -> dict:
    """
    获取自己订阅的频道

    Args:
        credential (Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["self_subscribes"]["list"]
    return await Api(**api, credential=credential).result


async def subscribe_channel(channel: Channel, credential: Credential) -> dict:
    """
    订阅频道

    Args:
        channel    (Channel)   : 要订阅的频道

        credential (Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["channel"]["subscribe"]
    data = {"id": channel.get_channel_id()}
    return await Api(**api, credential=credential).update_data(**data).result


async def unsubscribe_channel(channel: Channel, credential: Credential) -> dict:
    """
    取关频道

    Args:
        channel    (Channel)   : 要订阅的频道

        credential (Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["channel"]["unsubscribe"]
    data = {"id": channel.get_channel_id()}
    return await Api(**api, credential=credential).update_data(**data).result
