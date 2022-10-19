from .utils.network import request
from .utils.Credential import Credential
from .utils.utils import get_api

API = get_api("game")

class Game:
    """
    游戏类
    """
    def __init__(self, game_id: int, credential: Credential = None):
        """
        Args:
            game_id(int)          : 游戏 id
            credential(Credential): 凭据类
        """
        self.__game_id = game_id
        self.credential = credential if credential else Credential()
    
    def get_game_id(self):
        """
        获取游戏 id

        Returns:
            游戏 id
        """
        return self.__game_id

    async def get_info(self):
        """
        获取游戏简介

        Returns:
            dict: 调用 API 返回的结构
        """
        api = API["info"]["info"]
        params = {
            "game_base_id": self.__game_id
        }
        return await request("GET", api["url"], params = params, credential = self.credential)

    async def get_up_info(self):
        """
        获取游戏官方账号

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["UP"]
        params = {
            "game_base_id": self.__game_id
        }
        return await request("GET", api["url"], params = params, credential = self.credential)

    async def get_detail(self):
        """
        获取游戏详情

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["detail"]
        params = {
            "game_base_id": self.__game_id
        }
        return await request("GET", api["url"], params = params, credential = self.credential)

    async def get_wiki(self):
        """
        获取游戏教程(wiki)

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["wiki"]
        params = {
            "game_base_id": self.__game_id
        }
        return await request("GET", api["url"], params = params, credential = self.credential)

    async def get_videos(self):
        """
        获取游戏介绍视频

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["videos"]
        params = {
            "game_base_id": self.__game_id
        }
        return await request("GET", api["url"], params = params, credential = self.credential)
