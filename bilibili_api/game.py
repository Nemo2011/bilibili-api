from .utils.network import request
from .utils.Credential import Credential
from .utils.utils import get_api

API = get_api("game")

class Game:
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
