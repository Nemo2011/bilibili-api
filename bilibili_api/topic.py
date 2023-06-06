"""
bilibili_api.topic

话题相关
"""

from typing import Union, Optional
from enum import Enum
from .utils.network_httpx import request
from .utils.utils import get_api
from .utils.credential import Credential
from .user import get_self_info
from . import dynamic

API = get_api("topic")


class TopicCardsSortBy(Enum):
    """
    话题下内容排序方式

    + NEW: 最新
    + HOT: 最热
    + RECOMMEND: 推荐
    """

    NEW = 3
    HOT = 2
    RECOMMEND = 1


async def get_hot_topics(numbers: int = 33) -> dict:
    """
    获取动态页的火热话题

    Args:
        numbers (int): 话题数量. Defaults to 33.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["dynamic_page_topics"]
    params = {"page_size": numbers}
    return await request("GET", api["url"], params=params)


async def search_topic(keyword: str, ps: int = 20, pn: int = 1) -> dict:
    """
    搜索话题

    从动态页发布动态处的话题搜索框搜索话题

    Args:
        keyword (str): 搜索关键词
        ps      (int): 每页数量. Defaults to 20.
        pn      (int): 页数. Defaults to 1.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["search"]
    params = {"keywords": keyword, "page_size": ps, "page_num": pn}
    return await request("GET", api["url"], params=params)


class Topic:
    """
    话题类

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(self, topic_id: int, credential: Union[Credential, None] = None):
        """
        Args:
            topic_id   (int)       : 话题 id
            credential (Credential): 凭据类
        """
        self.__topic_id = topic_id
        self.credential = credential if credential else Credential()

    def get_topic_id(self) -> int:
        """
        获取话题 id

        Returns:
            int: 话题 id
        """
        return self.__topic_id

    async def get_info(self) -> dict:
        """
        获取话题简介

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["info"]
        params = {"topic_id": self.get_topic_id()}
        return await request(
            "GET", api["url"], params=params, credential=self.credential
        )

    async def get_raw_cards(
        self,
        ps: int = 100,
        offset: Optional[str] = None,
        sort_by: TopicCardsSortBy = TopicCardsSortBy.HOT,
    ) -> dict:
        """
        获取话题下的原始内容

        未登录无法使用热门排序字段即 TopicCardsSortBy.RECOMMEND

        Args:
            ps (int): 数据数量. Defaults to 100.
            offset (Optional[str]): 偏移量. 生成格式为 f'{页码}_{页码*数据量]}' 如'2_40' Defaults to None.
            sort_by (TopicCardsSortBy): 排序方式. Defaults to TopicCardsSortBy.HOT.

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["cards"]
        params = {
            "topic_id": self.get_topic_id(),
            "page_size": ps,
            "sort_by": sort_by.value,
            "offset": offset,
        }
        return await request(
            "GET", api["url"], params=params, credential=self.credential
        )

    async def get_cards(
        self,
        ps: int = 100,
        offset: Optional[str] = None,
        sort_by: TopicCardsSortBy = TopicCardsSortBy.HOT,
    ) -> list:
        """
        获取话题下的内容，返回列表

        自动处理并转换成动态类

        未登录无法使用热门排序字段即 TopicCardsSortBy.RECOMMEND

        Args:
            ps (int): 数据数量. Defaults to 100.
            offset (Optional[str]): 偏移量. 生成格式为 f'{页码}_{页码*数据量]}' 如'2_40' Defaults to None.
            sort_by (TopicCardsSortBy): 排序方式. Defaults to TopicCardsSortBy.HOT.

        Returns:
            list: 内容列表
        """
        topic_cards, cards = (
            await self.get_raw_cards(ps=ps, offset=offset, sort_by=sort_by),
            [],
        )
        for card in topic_cards["topic_card_list"]["items"]:
            if card["topic_type"] == "DYNAMIC":  # 我只看到这一个类型...没找到其他的
                cards.append(
                    dynamic.Dynamic(dynamic_id=int(card["dynamic_card_item"]["id_str"]))
                )
            else:
                cards.append(card)
        return cards

    async def like(self, status: bool = True) -> dict:
        """
        设置点赞话题

        Args:
            status (bool): 是否设置点赞. Defaults to True.

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["operate"]["like"]
        data = {
            "topic_id": self.get_topic_id(),
            "action": "like" if status else "cancel_like",
            "business": "topic",
            "up_mid": (await get_self_info(self.credential))["mid"],
        }
        return await request("POST", api["url"], data=data, credential=self.credential)

    async def set_favorite(self, status: bool = True) -> dict:
        """
        设置收藏话题

        Args:
            status (bool): 是否设置收藏. Defaults to True.

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["operate"]["add_favorite" if status else "cancel_favorite"]
        data = {"topic_id": self.get_topic_id()}
        return await request("POST", api["url"], data=data, credential=self.credential)
