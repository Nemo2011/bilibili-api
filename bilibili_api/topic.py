"""
bilibili_api.topic

话题相关
"""

from typing import Union
from .utils.network_httpx import request
from .utils.utils import get_api
from .utils.Credential import Credential
from .user import get_self_info

API = get_api("topic")


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

    async def get_cards(self, size: int = 100) -> dict:
        """
        获取话题下的内容

        Args:
            size (int): 数据数量. Defaults to 100.

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["cards"]
        params = {"topic_id": self.get_topic_id(), "page_size": size}
        return await request(
            "GET", api["url"], params=params, credential=self.credential
        )

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
