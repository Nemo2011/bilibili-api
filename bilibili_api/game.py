from .utils.network import request
from .utils.Credential import Credential
from .utils.utils import get_api

API = get_api("game")

class Game:
    def __init__(self, game_id: str):
        self.__game_id = game_id
    
    def get_game_id(self):
        return self.__game_id
