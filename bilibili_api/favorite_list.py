"""
bilibili_api.favorite_list

收藏夹操作。
"""

from bilibili_api.utils.network import request
from bilibili_api.exceptions.ArgsException import ArgsException
from bilibili_api.utils.Credential import Credential
from .utils.utils import get_api

API = get_api("favorite-list")


async def get_favorite_list(uid: int, aid: int = None, credential: Credential = None):
    """
    获取收藏夹列表。

    Args:
        uid        (int)                 : 用户 UID。
        aid        (int, optional)       : 视频 AV 号，当提供时将会额外返回各收藏夹对该视频的收藏情况. Defaults to None.
        credential (Credential, optional): Credential. Defaults to None.

    Returns:
        dict: API 调用结果。
    """
    api = API["info"]["list_list"]
    params = {
        "up_mid": uid
    }

    if aid is not None:
        if aid <= 0:
            raise ArgsException("aid 必须大于 0。")
        params["type"] = 2
        params["rid"] = aid

    return await request("GET", url=api["url"], params=params, credential=credential)


async def get_favorite_list_content(media_id: )
