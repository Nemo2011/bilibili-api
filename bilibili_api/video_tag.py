"""
bilibili_api.video_tag

视频标签相关，部分的标签的 id 与同名的频道的 id 一模一样。
"""

from .utils.network_httpx import request
from .utils.utils import get_api
from .errors import *
import httpx
from typing import Optional

API = get_api("video_tag")

class Tag:
    """
    标签类
    """
    def __init__(
        self,
        tag_name: Optional[str] = None,
        tag_id: Optional[int] = None
    ):
        """
        Args:
            tag_name (str | None): 标签名. Defaults to None.
            tag_id   (int | None): 标签 id. Defaults to None.

        注意：tag_name 和 tag_id 任选一个传入即可。tag_id 优先使用。
        """
        if tag_id == None:
            if tag_name == None:
                raise ArgsException("tag_name 和 tag_id 需要提供一个。")
            resp = httpx.get(f"https://api.bilibili.com/x/tag/info?tag_name={tag_name}").json()
            self.__tag_id = resp["data"]["tag_id"]
        else:
            self.__tag_id = tag_id
        self.credential = None # 不做 Credential 接入

    def get_tag_id(self) -> int:
        return self.__tag_id

    async def get_tag_info(self) -> dict:
        """
        获取标签信息。

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["tag_info"]
        params = {
            "tag_id": self.get_tag_id()
        }
        return await request(
            "GET",
            api["url"],
            params=params
        )

    async def get_simular_tags(self) -> dict:
        """
        获取相关的标签

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["get_simular"]
        params = {
            "tag_id": self.get_tag_id()
        }
        return await request(
            "GET",
            api["url"],
            params=params
        )

    async def get_cards(self) -> dict:
        """
        获取标签下的视频/动态

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["get_list"]
        params = {
            "topic_id": self.get_tag_id()
        }
        return await request(
            "GET",
            api["url"],
            params=params
        )
