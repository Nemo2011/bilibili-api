"""
话题相关
"""

from .utils.network_httpx import request
from .utils.utils import get_api
from .utils.Credential import Credential

API = get_api("topic")

class Topic:
    """
    话题类

    Attributes:
        credential (Credential): 凭据类
    """
    def __init__(self, topic_id: int, credential: Credential = None):
        """
        Args:
            topic_id   (int)       : 话题 id
            credential (Credential): 凭据类
        """
        self.__topic_id = topic_id
        self.credential = credential if credential else Credential()

    def get_topic_id(self):
        """
        获取话题 id

        Returns:
            int: 话题 id
        """
        return self.__topic_id

    async def get_info(self):
        """
        获取话题简介
        
        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["info"]
        params = {
            "topic_id": self.get_topic_id()
        }
        return await request("GET", api["url"], params = params, credential = self.credential)

    async def get_cards(self, size: int = 100):
        """
        获取话题下的内容

        Args:
            size (int): 数据数量. Defaults to 100. 

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["cards"]
        params = {
            "topic_id": self.get_topic_id(), 
            "page_size": size
        }
        return await request("GET", api["url"], params = params, credential = self.credential)
