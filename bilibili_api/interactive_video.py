"""
bilibili_api.interactive_video

互动视频相关操作
"""

from .utils.Credential import Credential
from .utils.utils import get_api
from .utils.network import request, get_session
from .video import Video
from urllib import parse
from .exceptions import ArgsException

API = get_api("interactive_video")

 
async def get_ivideo_pages(bvid: str, credential: Credential):
    """
    获取交互视频的分P信息。up 主需要拥有视频所有权。
    Args:
        bvid       (str)       : BV 号.
        credential (Credential): Credential 类.

    Returns:
      dict: 调用 API 返回结果
    """
    url = API["info"]["videolist"]["url"]
    params = {"bvid": bvid}
    return await request("GET", url=url, params=params, credential=credential)

async def submit_story_tree(story_tree: str, credential: Credential):
    """
    上传交互视频的情节树。up 主需要拥有视频所有权。

    Args:
      story_tree  (str): 情节树的描述，参考 bilibili_storytree.StoryGraph, 需要 Serialize 这个结构

    Returns:
      dict: 调用 API 返回结果
    """
    url = API["operate"]["savestory"]["url"]
    form_data = {"preview": "0", "data": story_tree, "csrf": credential.bili_jct}
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
                       credential=credential)

