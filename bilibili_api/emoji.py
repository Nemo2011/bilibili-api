"""
bilibili_api.emoji

表情包相关
"""

from .utils.utils import get_api
from .utils.network_httpx import Api

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
    return await Api(**api).update_params(**params).result
