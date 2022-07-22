"""
番剧相关

概念：
+ media_id: 番剧本身的 ID，有时候也是每季度的 ID，如 https://www.bilibili.com/bangumi/media/md28231846/
+ season_id: 每季度的 ID，只能通过 get_meta() 获取。
+ episode_id: 每集的 ID，如 https://www.bilibili.com/bangumi/play/ep374717

"""

import datetime
from enum import Enum
import httpx

import requests

from .utils.sync import sync
from .utils.utils import get_api
from .utils.Credential import Credential
from .utils.network_httpx import get_session, request
from .exceptions.ResponseException import ResponseException
from .exceptions.ApiException import ApiException
from .video import Video

import json
import re

API = get_api("bangumi")


class BangumiCommentOrder(Enum):
    """
    短评 / 长评 排序方式

    + DEFAULT: 默认
    + CTIME: 发布时间倒序
    """

    DEFAULT = 0
    CTIME = 1


class Bangumi:
    def __init__(
        self, media_id: int = -1, ssid: int = -1, credential: Credential = Credential()
    ):
        """番剧类"""
        if media_id == -1 and ssid == -1:
            raise ValueError("需要 Media_id 或 Season_id 中的一个 !")
        self.media_id = media_id
        self.credential = credential
        if ssid != -1:
            self.ssid = ssid
        else:
            api = API["info"]["meta"]
            params = {"media_id": self.media_id}
            meta = requests.get(url=api['url'], params=params, cookies=self.credential.get_cookies())
            meta.raise_for_status()
            self.ssid = meta.json()['result']['media']['season_id']
        if self.media_id == -1:
            api = API["info"]["collective_info"]
            params = {"season_id": self.ssid}
            overview = requests.get(url=api['url'], params=params, cookies=self.credential.get_cookies())
            overview.raise_for_status()
            self.media_id = overview.json()['result']['media_id']

    async def get_media_id(self):
        return self.media_id

    async def get_season_id(self):
        return self.ssid

    async def set_media_id(self, media_id: int):
        self.__init__(media_id=media_id, credential=self.credential)

    async def set_ssid(self, ssid: int):
        self.__init__(ssid=ssid, credential=self.credential)

    async def get_meta(self):
        """
        获取番剧元数据信息（评分，封面 URL，标题等）

        Args:
            media_id (int): media_id
            credential (Credential, optional): 凭据. Defaults to None.
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["meta"]
        params = {"media_id": self.media_id}
        return await request("GET", api["url"], params, credential=credential)

    async def get_short_comment_list(
        self, order: BangumiCommentOrder = BangumiCommentOrder.DEFAULT, next: str = None
    ):
        """
        获取短评列表

        Args:
            order      (BangumiCommentOrder, optional): 排序方式。Defaults to BangumiCommentOrder.DEFAULT
            next       (str, optional)                : 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["short_comment"]
        params = {"media_id": self.media_id, "ps": 20, "sort": order.value}
        if next is not None:
            params["cursor"] = next

        return await request("GET", api["url"], params, credential=credential)

    async def get_long_comment_list(
        self, order: BangumiCommentOrder = BangumiCommentOrder.DEFAULT, next: str = None
    ):
        """
        获取长评列表

        Args:
            order      (BangumiCommentOrder, optional): 排序方式。Defaults to BangumiCommentOrder.DEFAULT
            next       (str, optional)                : 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["long_comment"]
        params = {"media_id": self.media_id, "ps": 20, "sort": order.value}
        if next is not None:
            params["cursor"] = next

        return await request("GET", api["url"], params, credential=credential)

    async def get_episode_list(self):
        """
        获取季度分集列表
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["episodes_list"]
        params = {"season_id": self.ssid}
        return await request("GET", api["url"], params, credential=credential)

    async def get_stat(self):
        """
        获取番剧播放量，追番等信息
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["season_status"]
        params = {"season_id": self.ssid}
        return await request("GET", api["url"], params, credential=credential)

    async def get_overview(self):
        """
        获取番剧全面概括信息，包括发布时间、剧集情况、stat 等情况
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["collective_info"]
        params = {"season_id": self.ssid}
        return await request("GET", api["url"], params, credential=credential)


async def set_follow(
    bangumi: Bangumi, status: bool = True, credential: Credential = None
):
    """
    追番状态设置

    Args:
        bangumi  (Bangumi)               : 番剧类
        status     (bool, optional)      : 追番状态，Defaults to True
        credential (Credential, optional): 凭据. Defaults to None
    """
    credential = credential if credential is not None else Credential()
    credential.raise_for_no_sessdata()

    api = API["operate"]["follow_add"] if status else API["operate"]["follow_del"]
    data = {"season_id": bangumi.ssid}
    return await request("POST", api["url"], data=data, credential=credential)


class Episode(Video):
    def __init__(self, epid: int, credential: Credential = None):
        """
        番剧视频类（没错重构了）
        epid: epid
        credential: 凭据
        bangumi: 自动获取：番剧剧集所属的番剧
        """
        self.credential = credential
        self.epid = epid
        credential = self.credential if self.credential else Credential()
        try:
            resp = httpx.get(
                f"https://www.bilibili.com/bangumi/play/ep{self.epid}",
                cookies=credential.get_cookies(),
                headers={"User-Agent": "Mozilla/5.0"},
            )
        except Exception as e:
            raise ResponseException(str(e))
        else:
            content = resp.text

            pattern = re.compile(r"window.__INITIAL_STATE__=(\{.*?\});")
            match = re.search(pattern, content)
            if match is None:
                raise ApiException("未找到番剧信息")
            try:
                content = json.loads(match.group(1))
            except json.JSONDecodeError:
                raise ApiException("信息解析错误")
            else:
                bvid = content["epInfo"]["bvid"]
                self.bangumi = Bangumi(ssid=content["mediaInfo"]["season_id"])
        self.video_class = Video(bvid=bvid, credential=credential)
        super().__init__(bvid=bvid)
        self.set_aid = self.set_aid_e
        self.set_bvid = self.set_bvid_e

    async def get_epid(self):
        """
        获取 epid
        """
        return self.epid

    def set_aid_e(self, aid: str):
        print("Set aid is not allowed in Episode")

    def set_bvid_e(self, bvid: str):
        print("Set bvid is not allowed in Episode")

    async def get_cid(self):
        return await super().get_cid(0)

    def get_bangumi(self):
        """
        获取对应的番剧
        """
        return self.bangumi

    def set_epid(self, epid: int):
        """
        设置 epid
        Args:
            epid: epid
        Returns:
            None
        """
        self.__init__(epid, self.credential)

    async def get_episode_info(self):
        """
        获取番剧单集信息
        Returns:
            HTML 中的数据
        """
        credential = self.credential if self.credential else Credential()
        session = get_session()

        try:
            resp = await session.get(
                f"https://www.bilibili.com/bangumi/play/ep{self.epid}",
                cookies=credential.get_cookies(),
                headers={"User-Agent": "Mozilla/5.0"},
            )
        except Exception as e:
            raise ResponseException(str(e))
        else:
            content = resp.text

            pattern = re.compile(r"window.__INITIAL_STATE__=(\{.*?\});")
            match = re.search(pattern, content)
            if match is None:
                raise ApiException("未找到番剧信息")
            try:
                content = json.loads(match.group(1))
            except json.JSONDecodeError:
                raise ApiException("信息解析错误")

            return content

    async def get_bangumi_from_episode(self):
        """
        获取剧集对应的番剧
        Returns:
            输入的集对应的番剧类
        """
        info = await self.get_episode_info()
        ssid = info["mediaInfo"]["season_id"]
        return Bangumi(ssid=ssid)
    
    async def get_download_url(self):
        """
        获取番剧剧集下载信息。

        Returns:
            dict: 调用 API 返回的结果。
        """
        url = API["info"]["playurl"]["url"]
        if True:
            params = {
                "avid": self.get_aid(),
                "cid": await self.get_cid(),
                "qn": "127",
                "otype": "json",
                "fnval": 4048,
                "fourk": 1,
            }
        return await request("GET", url, params=params, credential=self.credential)

    async def get_danmaku_xml(self):
        """
        获取所有弹幕的 xml 源文件（非装填）

        Returns:
            文件源
        """
        return await self.video_class.get_danmaku_xml(0)

    async def get_danmaku_view(self):
        """
        获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。

        Returns:
            dict: 二进制流解析结果
        """
        return await self.video_class.get_danmaku_view(0)

    async def get_danmakus(self, date: datetime.date = None):
        """
        获取弹幕

        Returns:
            dict[Danmaku]: 弹幕列表
        """
        return await self.video_class.get_danmakus(0, date)

    async def get_history_danmaku_index(self, date: datetime.date = None):
        """
        获取特定月份存在历史弹幕的日期。

        Returns:
            None | List[str]: 调用 API 返回的结果。不存在时为 None。
        """
        return await self.video_class.get_history_danmaku_index(0, date)
