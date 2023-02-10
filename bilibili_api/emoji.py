"""
bilibili_api.emoji

表情包相关
"""

from .utils.network_httpx import request
from .utils.utils import get_api

API = get_api("emoji")


async def get_emoji_list(business: str = "reply") -> dict:
    """
    获取表情包列表

    Args:
        business (str): 使用场景, reply / dynamic

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["list"]
    params = {"business": business}
    return await request("GET", api["url"], params=params)
