"""
bilibili_api.cheese

有关 bilibili 课程的 api。
注意，注意！课程中的视频和其他视频几乎没有任何相通的 API！
不能将 CheeseVideo 转成 Video 类，后果自负（因为改动太多，所以我都不敢继承）
课程的视频好像都没有 bvid，有也没用。而且这种连官方的 html5 播放器都不能看课程！
呵呵，官方是只打算保留 aid 和 cid 啊，我太难了！
获取下载链接需要使用 bilibili_api.cheese.get_download_url，video.get_download_url 不适用。
还有，课程的 season_id 和 ep_id 不与番剧相通，井水不犯河水，请不要错用!
"""

from .utils.Credential import Credential
from .utils.utils import get_api
from .utils.sync import sync
from .utils.network_httpx import request

API = get_api("cheese")

class CheeseList:
    def __init__(self, season_id: int=-1, ep_id: int=-1, credential:Credential=None):
        """
        教程类
        season_id(int): ssid
        ep_id(int): 单集 ep_id
        credential(Credential): 凭据类
        注意：season_id 和 ep_id 任选一个即可，两个都选的话
        以 season_id 为主
        """
        if (season_id == -1) and (ep_id == -1):
            raise ValueError("season id 和 ep id 必须选一个")
        self.season_id = season_id
        self.ep_id = ep_id
        self.credential = credential
        if self.season_id == -1:
            self.season_id = str(sync(self.get_meta())['season_id'])

    def set_season_id(self, season_id: int):
        self.__init__(season_id=season_id)

    def set_ep_id(self, ep_id: int):
        self.__init__(ep_id=ep_id)

    def get_season_id(self):
        return self.season_id

    async def get_meta(self):
        """
        获取教程元数据
        Returns:
            调用 API 所得的结果。
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
        Returns:
            调用 API 所得的结果。
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
        credential(Credential): 凭据类
        """
        self.epid = epid
        self.cheese = CheeseList(ep_id=self.epid)
        self.credential = credential
        for v in sync(self.cheese.get_meta())['episodes']:
            if v['id'] == epid:
                self.aid = v['aid']
                self.cid = v['cid']

    def get_cheese(self):
        """
        获取所属课程
        """
        return self.cheese

    def set_epid(self, epid: int):
        """
        设置 epid

        Returns:
            None
        """
        self.__init__(epid, self.credential)
    
    async def get_download_url(self):
        """
        获取下载链接

        Returns:
            调用 API 所得的结果。
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
