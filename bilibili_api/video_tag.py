"""
bilibili_api.video_tag

视频标签相关，部分的标签的 id 与同名的频道的 id 一模一样。
"""

from typing import Optional

import httpx

from .errors import *
from .utils.utils import get_api
from .utils.credential import Credential
from .utils.network import Api

API = get_api("video_tag")
API_video = get_api("video")


class Tag:
    """
    标签类
    """

    def __init__(
        self,
        tag_name: Optional[str] = None,
        tag_id: Optional[int] = None,
        credential: Optional[Credential] = None,
    ):
        """
        Args:
            tag_name   (str | None): 标签名. Defaults to None.

            tag_id     (int | None): 标签 id. Defaults to None.

            credential (Credential): 凭据类. Defaults to None.

        注意：tag_name 和 tag_id 任选一个传入即可。tag_id 优先使用。
        """
        if tag_id == None:
            if tag_name == None:
                raise ArgsException("tag_name 和 tag_id 需要提供一个。")
            self.__tag_id = self.__get_tag_info_sync(tag_name)["tag_id"]
        else:
            self.__tag_id = tag_id
        credential = credential if credential else Credential()
        self.credential = credential

    def get_tag_id(self) -> int:
        return self.__tag_id

    def __get_tag_info_sync(self, tag_name: str) -> dict:
        api = API["info"]["tag_info"]
        params = {"tag_name": tag_name}
        return Api(**api).update_params(**params).result_sync

    async def get_tag_info(self) -> dict:
        """
        获取标签信息。

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["tag_info"]
        params = {"tag_id": self.get_tag_id()}
        return await Api(**api).update_params(**params).result

    async def get_similar_tags(self) -> dict:
        """
        获取相关的标签

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["get_similar"]
        params = {"tag_id": self.get_tag_id()}
        return await Api(**api).update_params(**params).result

    # async def get_cards(self) -> dict:
    #     """
    #     获取标签下的视频/动态

    #     Returns:
    #         dict: 调用 API 返回的结果
    #     """
    #     api = API["info"]["get_list"]
    #     params = {"topic_id": self.get_tag_id()}
    #     return await Api(**api).update_params(**params).result

    async def get_history_cards(self, offset_dynamic_id: int) -> dict:
        """
        获取标签下，指定dynamic_id的视频的后一个视频/动态作为起始的视频/动态

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["get_history_list"]
        params = {"topic_id": self.get_tag_id(), "offset_dynamic_id": offset_dynamic_id}
        return await Api(**api).update_params(**params).result

    async def subscribe_tag(self) -> dict:
        """
        关注标签。

        Returns:
            dict: 调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API_video["operate"]["subscribe_tag"]

        data = {"tag_id": self.__tag_id}
        return await Api(**api, credential=self.credential).update_data(**data).result

    async def unsubscribe_tag(self) -> dict:
        """
        取关标签。

        Returns:
            dict: 调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API_video["operate"]["unsubscribe_tag"]

        data = {"tag_id": self.__tag_id}
        return await Api(**api, credential=self.credential).update_data(**data).result
