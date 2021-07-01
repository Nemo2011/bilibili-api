"""
bilibili_api.interactive_video

互动视频相关操作
"""

import re
from .exceptions import ArgsException
from .utils.Credential import Credential
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.utils import get_api
from .utils.network import request, get_session
from .utils.Danmaku import Danmaku
from .video import Video
from typing import List
from urllib import parse
import datetime


API = get_api("interactive_video")

class IVideo(Video):
    """
    互动视频类，各种对互动视频的操作将均在里面。TODO：持续更新。
    """

    def __init__(self, bvid: str = None, aid: int = None, credential: Credential = None):
        """
        Args:
            bvid       (str, optional)       : BV 号. bvid 和 aid 必须提供其中之一。
            aid        (int, optional)       : AV 号. bvid 和 aid 必须提供其中之一。
            credential (Credential, optional): Credential 类. Defaults to None.
        """
        super().__init__(bvid=bvid, aid=aid, credential=credential)
        self.__pages = None

    async def get_pages(self):
        """
        获取交互视频的分P信息。

        Returns:
        dict: 调用 API 返回结果
        """
        url = API["info"]["videolist"]["url"]
        params = {"bvid": self.get_bvid()}
        return await request("GET", url=url, params=params, credential=self.credential)

    async def __get_pages_cached(self):
        """
        获取视频信息，如果已获取过则使用之前获取的信息，没有则重新获取。

        Returns:
            dict: 调用 API 返回的结果。
        """
        if self.__pages is None:
            return await self.get_pages()
        return self.__pages


    async def __get_page_id_by_index(self, page_index: int):
        """
        根据分 p 号获取 page_id。

        Args:
            page_index (int):   分 P 号，从 0 开始。

        Returns:
            int: 分 P 的唯一 ID。
        """
        if page_index < 0:
            raise ArgsException("分 p 号必须大于或等于 0。")

        info = await self.__get_pages_cached()
        pages = info["videos"]

        if len(pages) <= page_index:
            raise ArgsException("不存在该分 p。")

        page = pages[page_index]
        cid = page["cid"]
        return cid

    async def get_download_url(self, page_index: int):
        """
        获取视频下载信息。

        Args:
            page_index (int):  分 P 号，从 0 开始。

        Returns:
            dict: 调用 API 返回的结果。
        """
        cid = await self.__get_page_id_by_index(page_index)

        url = API["info"]["playurl"]["url"]
        params = {
            "avid": self.get_aid(),
            "cid": cid,
            "qn": "120",
            "otype": "json",
            "fnval": 16
        }
        return await request("GET", url, params=params, credential=self.credential)

    async def submit_story_tree(self, story_tree: str):
        """
        上传交互视频的情节树。

        Args:
        story_tree: 情节树的描述，参考 bilibili_storytree.StoryGraph, 需要 Serialize 这个结构

        Returns:
        dict: 调用 API 返回结果
        """
        url = API["operate"]["savestory"]["url"]
        form_data = {"preview": "0", "data": story_tree, "csrf": self.credential.bili_jct}
        headers = {
          "User-Agent": "Mozilla/5.0",
          "Referer": "https://member.bilibili.com",
          "Content-Encoding" : "gzip, deflate, br",
          "Content-Type": "application/x-www-form-urlencoded",
          "Accept": "application/json, text/plain, */*"
        }
        data = parse.urlencode(form_data)
        return await request("POST", url=url, data=data,
                           headers=headers,
                           no_csrf=True,
                           credential=self.credential)

