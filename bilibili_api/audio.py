"""
音频相关
"""

from .utils.utils import get_api
from .utils.Credential import Credential
from .utils.network import request

API = get_api("audio")


class Audio:
    def __init__(self, auid: int, credential: Credential = None):
        """
        Args:
            auid       (int)                 : 音频 AU 号
            credential (Credential, optional): 凭据. Defaults to None
        """
        self.credential = credential if credential is not None else Credential()
        self.auid = auid

    async def get_auid(self):
        return self.auid

    async def get_info(self):
        """
        获取音频信息
        """

        api = API["audio_info"]["info"]
        params = {"sid": self.auid}
        return await request("GET", api["url"], params, credential=self.credential)

    async def get_tags(self):
        """
        获取音频 tags
        """
        api = API["audio_info"]["tag"]
        params = {"sid": self.auid}
        return await request("GET", api["url"], params, credential=self.credential)

    async def get_download_url(self):
        """
        获取音频下载链接
        """
        api = API["audio_info"]["download_url"]
        params = {"sid": self.auid, "privilege": 2, "quality": 2}
        return await request("GET", api["url"], params, credential=self.credential)

    async def add_coins(self, num: int = 2):
        """
        投币

        Args:
            num (int, optional): 投币数量。Defaults to 2.
        """
        self.credential.raise_for_no_sessdata()

        api = API["audio_operate"]["coin"]
        data = {"sid": self.auid, "multiply": num}

        return await request("POST", api["url"], data=data, credential=self.credential)


class AudioList:
    """
    歌单
    """

    def __init__(self, amid: int, credential: Credential = None):
        """

        Args:
            amid       (int)                 : 歌单 ID
            credential (Credential, optional): 凭据. Defaults to None.
        """
        self.amid = amid
        self.credential = credential if credential is not None else Credential()

    async def get_info(self):
        """
        获取歌单信息
        """

        api = API["list_info"]["info"]
        params = {"sid": self.amid}
        return await request("GET", api["url"], params, credential=self.credential)

    async def get_tags(self):
        """
        获取歌单 tags
        """

        api = API["list_info"]["tag"]
        params = {"sid": self.amid}
        return await request("GET", api["url"], params, credential=self.credential)

    async def get_song_list(self, pn: int = 1):
        """
        获取歌单歌曲列表

        Args:
            pn (int, optional): 页码. Defaults to 1
        """
        api = API["list_info"]["song_list"]
        params = {"sid": self.amid, "pn": pn, "ps": 100}

        return await request("GET", api["url"], params, credential=self.credential)


async def get_user_stat(uid: int, credential: Credential = None):
    """
    获取用户数据（收听数，粉丝数等）

    Args:
        uid        (int)                 : 用户 UID
        credential (Credential, optional): 凭据. Defaults to None
    """
    credential = credential if credential is not None else Credential()
    api = API["audio_info"]["user"]
    params = {"uid": uid}
    return await request("GET", api["url"], params, credential=credential)
