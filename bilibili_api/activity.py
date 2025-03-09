"""
bilibili_api.activity

活动相关
"""

from .utils.initial_state import get_initial_state
from .utils.network import Api
from .utils.utils import get_api


API = get_api("activity")


async def get_activity_list(pn: int = 1, ps: int = 15) -> dict:
    """
    获取活动列表

    Args:
        pn (int, optional): 页数. Defaults to 1.
        ps (int, optional): 每页数量. Defaults to 15.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["list"]
    params = {"plat": "1,3", "mold": "0", "http": "3", "pn": pn, "ps": ps}
    return await Api(**api).update_params(**params).result


async def get_activity_info(url: str) -> dict:
    """
    获取活动详情

    Args:
        url (str): 活动链接

    Returns:
        dict: 活动详情
    """
    return (await get_initial_state(url))[0]


async def get_activity_aid(url: str) -> dict:
    """
    获取部分活动存在的 aid，可用于获取评论

    Args:
        url (str): 活动链接

    Returns:
        int: 活动 aid，若活动无 aid 返回 -1
    """
    return int((await get_activity_info(url))["BaseInfo"].get("aid", "0"))

