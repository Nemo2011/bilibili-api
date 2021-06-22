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

IVIDEO_API = get_api("interactive_video")

class IVideo:
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
        # ID 检查
        if bvid is not None:
            self.set_bvid(bvid)
        elif aid is not None:
            self.set_aid(aid)
        else:
            # 未提供任一 ID
            raise ArgsException("请至少提供 bvid 和 aid 中的其中一个参数。")

        # 未提供 credential 时初始化该类
        if credential is None:
            self.credential = Credential()
        else:
            self.credential = credential

        # 用于存储视频信息，避免接口依赖视频信息时重复调用
        self.__info = None

    def set_bvid(self, bvid: str):
        """
        设置 bvid。

        Args:
            bvid (str):   要设置的 bvid。
        """
        # 检查 bvid 是否有效
        if not re.search("^BV[a-zA-Z0-9]{10}$", bvid):
            raise ArgsException(
                "bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。")
        self.__bvid = bvid
        self.__aid = bvid2aid(bvid)

    def get_bvid(self):
        """
        获取 BVID。

        Returns:
            str: BVID。
        """
        return self.__bvid

    def set_aid(self, aid: int):
        """
        设置 aid。

        Args:
            aid (int): AV 号。
        """
        if aid <= 0:
            raise ArgsException("aid 不能小于或等于 0。")

        self.__aid = aid
        self.__bvid = aid2bvid(aid)

    def get_aid(self):
        """
        获取 AID。

        Returns:
            int: aid。
        """
        return self.__aid


    async def get_video_pages(self):
      """
      获取交互视频的分P信息。
      
      Returns:
        dict: 调用 API 返回结果
      """
      api = IVIDEO_API["videolist"]
      params = {"bvid": self.get_bvid()}
      return await request("GET", url=api["url"], params=params, credential=self.credential)

    async def submit_story_tree(self, story_tree: str):
      """
      上传交互视频的情节树。

      Args:
        story_tree: 情节树的描述，参考 bilibili_storytree.StoryGraph, 需要 Serialize 这个结构

      Returns:
        dict: 调用 API 返回结果
      """
      api = IVIDEO_API["savestory"]
      form_data = {"preview": "0", "data": story_tree, "csrf": self.credential.bili_jct}
      headers = {
          "User-Agent": "Mozilla/5.0",
          "Referer": "https://member.bilibili.com",
          "Content-Encoding" : "gzip, deflate, br",
          "Content-Type": "application/x-www-form-urlencoded",
          "Accept": "application/json, text/plain, */*"
      }
      from urllib import parse
      data = parse.urlencode(form_data)
      return await request("POST", url=api["url"], data=data,
                           headers=headers,
                           no_csrf=True,
                           credential=self.credential)


