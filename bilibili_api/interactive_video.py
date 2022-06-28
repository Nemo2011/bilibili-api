"""
bilibili_api.interactive_video

互动视频相关操作
"""

from .utils.Credential import Credential
from .utils.utils import get_api
from .utils.network_httpx import request, get_session
from .video import Video
from urllib import parse
from .exceptions import ArgsException
from bilibili_api import video

API = get_api("interactive_video")


async def up_get_ivideo_pages(bvid: str, credential: Credential):
    """
    获取交互视频的分 P 信息。up 主需要拥有视频所有权。
    Args:
        bvid       (str)       : BV 号.
        credential (Credential): Credential 类.

    Returns:
      dict: 调用 API 返回结果
    """
    url = API["info"]["videolist"]["url"]
    params = {"bvid": bvid}
    return await request("GET", url=url, params=params, credential=credential)


async def up_submit_story_tree(story_tree: str, credential: Credential):
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
        "Content-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/plain, */*",
    }
    data = parse.urlencode(form_data)
    return await request(
        "POST", url=url, data=data, headers=headers, no_csrf=True, credential=credential
    )


async def get_graph_version(bvid: str, credential: Credential = None):
    """
    获取剧情图版本号，仅供 `get_edge_info()` 使用。

    Args:
        bvid (str): bvid
        credential (Credential, optional): [description]. Defaults to None.

    Returns:
        int: 剧情图版本号
    """
    # 取得初始顶点 cid
    v = video.Video(bvid=bvid, credential=credential)
    page_list = await v.get_pages()
    cid = page_list[0]["cid"]

    # 获取剧情图版本号
    api = "https://api.bilibili.com/x/player/v2"
    params = {"bvid": bvid, "cid": cid}

    resp = await request("GET", api, params, credential=credential)
    return resp["interaction"]["graph_version"]


async def get_edge_info(
    bvid: str, graph_version: int, edge_id: int = None, credential: Credential = None
):
    """
    获取剧情图节点信息

    Args:
        bvid          (str)                 : BV 号
        graph_version (int)                 : 剧情图版本号，可使用 get_graph_version() 获取
        edge_id       (int, optional)       : 节点 ID，为 None 时获取根节点信息. Defaults to None.
        credential    (Credential, optional): 凭据. Defaults to None.
    """
    credential = credential if credential is not None else Credential()

    url = API["info"]["edge_info"]["url"]
    params = {"bvid": bvid, "graph_version": graph_version}

    if edge_id is not None:
        params["edge_id"] = edge_id

    return await request("GET", url, params, credential=credential)
