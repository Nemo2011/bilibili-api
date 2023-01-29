"""
bilibili_api.audio

音频相关
"""

from .utils.utils import get_api
from .utils.Credential import Credential
from .utils.network_httpx import request
from typing import Union, Optional
from enum import Enum

API = get_api("audio")


class OrderAudio(Enum):
    """
    音频搜索排序类型

    + NEW: 最新
    + HOT: 最热
    """
    NEW = 1
    HOT = 2


class TagsAudio:
    """
    音频搜索可以用的标签，有语言和类型两种标签，每种标签选一个

    - Lang: 语言标签枚举类
    - Genre: 类型标签枚举类
    """
    class Lang(Enum):
        """
        音频搜索语言标签枚举

        - ALL: 全部
        - CHINESE: 华语
        - EUROPE_AMERICA: 欧美
        - JAPAN: 日语
        - KOREA: 韩语
        - OTHER: 其他
        """
        ALL = ""
        CHINESE = 3
        EUROPE_AMERICA = 6
        JAPAN = 7
        KOREA = 61
        OTHER = 1

    class Genre(Enum):
        """
        音频搜索类型标签枚举

        - ALL: 全部
        - POPULAR: 流行
        - ROCK: 摇滚
        - ELECTRONIC: 电子音乐
        - COUNTRYSIDE: 乡村
        - FOLK: 民谣
        - LIVE: 轻音乐
        - CLASSICAL: 古典
        - NEW_CENTURY: 新世纪
        - REGGAE: 雷鬼
        - BLUES: 布鲁斯
        - RHYTHM_BLUES: 节奏与布鲁斯
        - ORIGINAL: 原声
        - WORLD: 世界音乐
        - CHILDREN: 儿童音乐
        - LATIN: 拉丁
        - PUNK: 朋克
        - MEDAL: 金属
        - JAZZ: 爵士乐
        - HIP_HOP: 嘻哈
        - SINGER_SONGWRITER: 唱作人
        - AMUSEMENT: 娱乐/舞台
        - OTHER: 其他
        """
        ALL = ""
        POPULAR = 1
        ROCK = 2
        ELECTRONIC = 3
        COUNTRYSIDE = 4
        FOLK = 5
        LIVE = 6
        CLASSICAL = 7
        NEW_CENTURY = 8
        REGGAE = 9
        BLUES = 10
        RHYTHM_BLUES = 12
        ORIGINAL = 13
        WORLD = 14
        CHILDREN = 15
        LATIN = 16
        PUNK = 17
        MEDAL = 18
        JAZZ = 19
        HIP_HOP = 20
        SINGER_SONGWRITER = 21
        AMUSEMENT = 22
        OTHER = 23


async def get_homepage_recommend(credential: Optional[Credential] = None):
    """
    获取音频首页推荐

    Args:
        credential (Credential | None): 凭据类. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    api = API["audio_info"]["homepage_recommend"]
    return await request("GET", api["url"], credential = credential)


class Audio:
    """
    音频

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(self, auid: int, credential: Union[Credential, None] = None):
        """
        Args:
            auid       (int)                        : 音频 AU 号
            credential (Credential | None, optional): 凭据. Defaults to None
        """
        self.credential = credential if credential is not None else Credential()
        self.__auid = auid

    def get_auid(self) -> int:
        return self.__auid

    async def get_info(self) -> dict:
        """
        获取音频信息

        Returns:
            dict: 调用 API 返回的结果
        """

        api = API["audio_info"]["info"]
        params = {"sid": self.__auid}
        return await request("GET", api["url"], params, credential=self.credential)

    async def get_tags(self) -> dict:
        """
        获取音频 tags

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["audio_info"]["tag"]
        params = {"sid": self.__auid}
        return await request("GET", api["url"], params, credential=self.credential)

    async def get_download_url(self) -> dict:
        """
        获取音频下载链接

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["audio_info"]["download_url"]
        params = {"sid": self.__auid, "privilege": 2, "quality": 2}
        return await request("GET", api["url"], params, credential=self.credential)

    async def add_coins(self, num: int = 2) -> dict:
        """
        投币

        Args:
            num (int, optional): 投币数量。Defaults to 2.

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()

        api = API["audio_operate"]["coin"]
        data = {"sid": self.__auid, "multiply": num}

        return await request("POST", api["url"], data=data, credential=self.credential)

    # TODO: 音频编辑


class AudioList:
    """
    歌单

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(self, amid: int, credential: Union[Credential, None] = None):
        """
        Args:
            amid       (int)                        : 歌单 ID
            credential (Credential | None, optional): 凭据. Defaults to None.
        """
        self.__amid = amid
        self.credential = credential if credential is not None else Credential()

    def get_amid(self) -> int:
        return self.__amid

    async def get_info(self) -> dict:
        """
        获取歌单信息

        Returns:
            dict: 调用 API 返回的结果
        """

        api = API["list_info"]["info"]
        params = {"sid": self.__amid}
        return await request("GET", api["url"], params, credential=self.credential)

    async def get_tags(self) -> dict:
        """
        获取歌单 tags

        Returns:
            dict: 调用 API 返回的结果
        """

        api = API["list_info"]["tag"]
        params = {"sid": self.__amid}
        return await request("GET", api["url"], params, credential=self.credential)

    async def get_song_list(self, pn: int = 1) -> dict:
        """
        获取歌单歌曲列表

        Args:
            pn (int, optional): 页码. Defaults to 1

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["list_info"]["song_list"]
        params = {"sid": self.__amid, "pn": pn, "ps": 100}

        return await request("GET", api["url"], params, credential=self.credential)

    # TODO: 歌单编辑


async def get_user_stat(uid: int, credential: Union[Credential, None] = None) -> dict:
    """
    获取用户数据（收听数，粉丝数等）

    Args:
        uid        (int)                        : 用户 UID
        credential (Credential | None, optional): 凭据. Defaults to None

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential is not None else Credential()
    api = API["audio_info"]["user"]
    params = {"uid": uid}
    return await request("GET", api["url"], params, credential=credential)


async def get_hot_song_list(pn: int = 1, credential: Union[Credential, None] = None) -> dict:
    """
    获取热门歌单

    Args:
        pn(int, optional)                       : 页数. Defaults to 1
        credential (Credential | None, optional): 凭据. Defaults to None

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential is not None else Credential()
    api = API["list_info"]["hot"]
    params = {"pn": pn, "ps": 100}
    return await request("GET", api["url"], params, credential=credential)


async def get_homepage_music_video_list(
    keyword: str = "",
    lang: TagsAudio.Lang = TagsAudio.Lang.ALL,
    genre: TagsAudio.Genre = TagsAudio.Genre.ALL,
    order: OrderAudio = OrderAudio.NEW,
    page_num: int = 1,
    page_size: int = 10
) -> dict:
    """
    获取首页的音乐视频列表

    Args:
        keyword   (str)            : 关键词. Defaults to None.
        lang      (TagsAudio.Lang) : 音频语言. Defaults to TagsAudio.Lang.ALL
        genre     (TagsAudio.Genre): 音频类型. Defaults to TagsAudio.Genre.ALL
        order     (OrderAudio)     : 音频排序方式. Defaults to OrderAudio.NEW
        page_num  (int)            : 页码. Defaults to 1.
        page_size (int)            : 每页的数据大小. Defaults to 10.
    """
    api = API["audio_info"]["audio_list"]
    params = {
        "type": order.value,
        "lang": lang.value,
        "genre": genre.value,
        "keyword": keyword,
        "pn": page_num,
        "ps": page_size
    }
    return await request(
        "GET",
        api["url"],
        params = params
    )
