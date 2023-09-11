"""
bilibili_api.game

游戏相关
"""

import json
import re
from enum import Enum
from typing import Union
from .errors import ApiException

from httpx import AsyncClient

from .utils.credential import Credential
from .utils.network import HEADERS, Api, get_session
from .utils.utils import get_api

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


class GameRankType(Enum):
    """
    游戏排行榜类型枚举

    - HOT: 热度榜
    - SUBSCRIBE: 预约榜
    - NEW: 新游榜
    - REPUTATION: 口碑榜
    - BILIBILI: B指榜
    - CLIENT: 端游榜
    """

    HOT = 1
    SUBSCRIBE = 5
    NEW = 6
    REPUTATION = 2
    BILIBILI = 7
    CLIENT = 11


async def get_game_rank(
    rank_type: GameRankType, page_num: int = 1, page_size: int = 20
) -> dict:
    """
    获取游戏排行榜

    Args:
        rank_type (GameRankType): 游戏排行榜类型
        page_num (int, optional): 页码. Defaults to 1.
        page_size (int, optional): 每页游戏数量. Defaults to 20.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["rank"]
    params = {
        "ranking_type": rank_type.value,
        "page_num": page_num,
        "page_size": page_size,
    }
    return await Api(**api).update_params(**params).result


async def get_start_test_list(page_num: int = 1, page_size: int = 20) -> dict:
    """
    获取游戏公测时间线

    Args:
        page_num (int, optional): 页码. Defaults to 1.
        page_size (int, optional): 每页游戏数量. Defaults to 20.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["start_test"]
    params = {"x-fix-page-num": 1, "page_num": page_num, "page_size": page_size}
    return await Api(**api).update_params(**params).result


def get_wiki_api_root(game_id: str) -> str:
    """
    获取游戏 WIKI 对应的 api 链接，以便传入第三方库进行其他解析操作。

    Args:
        game_id (str): 游戏编码

    Returns:
        str: 游戏 WIKI 对应的 api 链接
    """
    return f"https://wiki.biligame.com/{game_id}/api.php"


async def game_name2id(game_name: str) -> str:
    """
    将游戏名转换为游戏的编码

    Args:
        game_name (str): 游戏名

    Returns:
        str: 游戏编码
    """
    sess: AsyncClient = get_session()
    try:
        wiki_page_title = json.loads(
            (
                await sess.get(
                    f"https://wiki.biligame.com/wiki/api.php?action=opensearch&format=json&formatversion=2&search={game_name}&namespace=0&limit=10"
                )
            ).text
        )[3][0].lstrip("https://wiki.biligame.com/wiki/")
    except IndexError as e:
        raise ApiException("未找到游戏")
    wiki_page_content = (
        await sess.get(
            f"https://wiki.biligame.com/wiki/api.php?action=query&prop=revisions&titles={wiki_page_title}&rvprop=content&format=json",
        )
    ).text
    wiki_page_template_re = re.compile(r"\{\{(.*?)\}\}")
    match = re.search(wiki_page_template_re, wiki_page_content)
    if match is None:
        raise ApiException("获取游戏编码失败")
    wiki_page_template_content = match.group(1)
    wiki_page_template_content = wiki_page_template_content.encode("ascii").decode("unicode-escape")
    for prop in wiki_page_template_content.split("|"):
        if prop.startswith("WIKI域名="):
            return prop.lstrip("WIKI域名=").rstrip()
