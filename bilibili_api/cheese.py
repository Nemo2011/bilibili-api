"""
bilibili_api.cheese

有关 bilibili 课程的 api。
注意，注意！课程中的视频和其他视频几乎没有任何相通的 API！
获取下载链接需要使用 bilibili_api.cheese.get_download_url，video.get_download_url 不适用。
还有，课程的 season_id 和 ep_id 不与番剧相通，井水不犯河水，请不要错用!
"""

import json
import re
from bilibili_api.exceptions import ApiException, ResponseException
from bilibili_api.utils.Credential import Credential
from bilibili_api.video import Video
from .utils.utils import get_api
from .utils.sync import sync
from .utils.network import get_session, request

API = get_api("cheese")

class CheeseList:
    def __init__(self, season_id=-1, ep_id=-1, credential:Credential=None):
        """
        教程类
        season_id(int): ssid
        ep_id(int): 单集 ep_id
        credential(Credential): 认证类
        """
        if (season_id == -1) and (ep_id == -1):
            raise ValueError("season id 和 ep id 必须选一个")
        self.season_id = season_id
        self.ep_id = ep_id
        self.credential = credential
        if self.season_id == -1:
            self.season_id = str(sync(self.get_meta())['season_id'])

    async def get_meta(self):
        """
        获取教程元数据
        """
        api = API['info']['meta']
        params = {
            "season_id": self.season_id, 
            "ep_id": self.ep_id
        }
        return await request("GET", api['url'], params=params, credential=self.credential)

    async def get_list(self, pn: int=1, ps: int=50):
        """
        获取教程所有视频
        """
        api = API['info']['list']
        params = {
            "season_id": self.season_id,
            "pn": pn, 
            "ps": ps
        }
        return await request("GET", api['url'], params=params, credential=self.credential)


class CheeseVideo:
    def __init__(self, epid, credential: Credential=None):
        """
        教程视频类
        因为不和其他视频相通，所以这里是一个新的类，无继承
        ep_id(int): 单集 ep_id
        credential(Credential): 认证类
        """
        self.epid = epid
        self.cheese = CheeseList(ep_id=self.epid)
        self.credential = credential
        for v in sync(self.cheese.get_meta())['episodes']:
            if v['id'] == epid:
                self.aid = v['aid']
                self.cid = v['cid']

    def set_epid(self, epid: int):
        """
        设置 epid
        """
        self.__init__(epid, self.credential)
    
    async def get_download_url(self):
        """
        获取下载链接
        """
        api = API['info']['playurl']
        params = {
            "avid": self.aid,
            "ep_id": self.epid,
            "cid": self.cid,
            "qn": 127, 
            "fnval": 4048,
            "fourk": 1
        }
        return await request("GET", api['url'], params=params, credential=self.credential)
