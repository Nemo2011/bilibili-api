"""
bilibili_api.game

游戏相关
"""

from typing import Union

from .utils.utils import get_api
from .utils.credential import Credential
from .utils.network_httpx import Api

API = get_api("game")


class Game:
    """
    游戏类

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(self, game_id: int, credential: Union[None, Credential] = None):
        """
        Args:
            game_id    (int)       : 游戏 id

            credential (Credential): 凭据类. Defaults to None.
        """
        self.__game_id = game_id
        self.credential = credential if credential else Credential()

    def get_game_id(self) -> int:
        return self.__game_id

    async def get_info(self) -> dict:
        """
        获取游戏简介

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["info"]
        params = {"game_base_id": self.__game_id}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_up_info(self) -> dict:
        """
        获取游戏官方账号

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["UP"]
        params = {"game_base_id": self.__game_id}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_detail(self) -> dict:
        """
        获取游戏详情

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["detail"]
        params = {"game_base_id": self.__game_id}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_wiki(self) -> dict:
        """
        获取游戏教程(wiki)

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["wiki"]
        params = {"game_base_id": self.__game_id}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_videos(self) -> dict:
        """
        获取游戏介绍视频

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["videos"]
        params = {"game_base_id": self.__game_id}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    # async def get_score(self) -> dict:
    #     """
    #     获取游戏评分

    #     该接口需要鉴权，暂时停用

    #     Returns:
    #         dict: 调用 API 返回的结果
    #     """
    #     api = API["info"]["score"]
    #     params = {"game_base_id": self.__game_id}
    #     return await request(
    #         "GET", api["url"], params=params, credential=self.credential
    #     )

    # async def get_comments(self) -> dict:
    #     """
    #     获取游戏的评论

    #     Returns:
    #         dict: 调用 API 返回的结果
    #     """
    #     api = API["info"]["comment"]
    #     params = {"game_base_id": self.__game_id}
    #     return await request(
    #         "GET", api["url"], params=params, credential=self.credential
    #     )
