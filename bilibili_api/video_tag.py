"""
bilibili_api.video_tag

视频标签相关，部分的标签的 id 与同名的频道的 id 一模一样。
"""


from .exceptions import *
from .utils.network import Api, Credential
from .utils.utils import get_api

API = get_api("video_tag")
API_video = get_api("video")


class Tag:
    """
    标签类
    """

    def __init__(
        self,
        tag_name: str | None = None,
        tag_id: int | None = None,
        credential: Credential | None = None,
    ):
        """
        Args:
            tag_name   (str | None): 标签名. Defaults to None.

            tag_id     (int | None): 标签 id. Defaults to None.

            credential (Credential): 凭据类. Defaults to None.

        注意：tag_name 和 tag_id 任选一个传入即可。tag_id 优先。
        """
        self.__tag_id = tag_id
        self.__tag_name = tag_name
        credential = credential if credential else Credential()
        self.credential: Credential = credential

    async def get_tag_id(self) -> int:
        """
        获取标签 id

        Returns:
            int: 标签 id
        """
        if not self.__tag_id:
            await self.get_tag_info()
        return self.__tag_id

    async def get_tag_name(self) -> str:
        """
        获取标签名

        Returns:
            str: 标签名
        """
        if not self.__tag_name:
            await self.get_tag_info()
        return self.__tag_name

    async def get_tag_info(self) -> dict:
        """
        获取标签信息。

        Returns:
            dict: 调用 API 返回的结果
        """
        if not self.__tag_id and not self.__tag_name:
            raise ArgsException("初始化时 tag_id 和 tag_name 至少要提供一个。")
        api = API["info"]["tag_info"]
        if self.__tag_id:
            params = {"tag_id": self.__tag_id}
        else:
            params = {"tag_name": self.__tag_name}
        res = await Api(**api).update_params(**params).result
        if not self.__tag_id:
            self.__tag_id = res["tag_id"]
        if not self.__tag_name:
            self.__tag_name = res["tag_name"]
        return res

    async def get_similar_tags(self) -> dict:
        """
        获取相关的标签

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["get_similar"]
        params = {"tag_id": await self.get_tag_id()}
        return await Api(**api).update_params(**params).result

    # async def get_cards(self) -> dict:
    #     """
    #     获取标签下的视频/动态

    #     Returns:
    #         dict: 调用 API 返回的结果
    #     """
    #     api = API["info"]["get_list"]
    #     params = {"topic_id": await self.get_tag_id()}
    #     return await Api(**api).update_params(**params).result

    # async def get_history_cards(self, offset_dynamic_id: int) -> dict:
    #     """
    #     获取标签下，指定dynamic_id的视频的后一个视频/动态作为起始的视频/动态

    #     Returns:
    #         dict: 调用 API 返回的结果
    #     """
    #     api = API["info"]["get_history_list"]
    #     params = {"topic_id": await self.get_tag_id(), "offset_dynamic_id": offset_dynamic_id}
    #     return await Api(**api).update_params(**params).result

    async def subscribe_tag(self) -> dict:
        """
        关注标签。

        Returns:
            dict: 调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API_video["operate"]["subscribe_tag"]

        data = {"tag_id": await self.get_tag_id()}
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

        data = {"tag_id": await self.get_tag_id()}
        return await Api(**api, credential=self.credential).update_data(**data).result
