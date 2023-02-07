"""
bilibili_api.hot

热门相关 API
"""

from .utils.network_httpx import request
from .utils.utils import get_api

API_rank = get_api("rank")
API = get_api("hot")


async def get_hot_videos(pn: int = 1, ps: int = 20) -> dict:
    """
    获取热门视频

    Args:
        pn (int): 第几页. Default to 1.
        ps (int): 每页视频数. Default to 20.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API_rank["info"]["hot"]
    params = {"ps": ps, "pn": pn}
    return await request("GET", url=api["url"], params=params)


async def get_weakly_hot_videos_list() -> dict:
    """
    获取每周必看列表(仅概述)

    Returns:
        调用 API 返回的结果
    """
    api = API_rank["info"]["weakly_series"]
    return await request("GET", url=api["url"])


async def get_weakly_hot_videos(week: int = 1) -> dict:
    """
    获取一周的每周必看视频列表

    Args:
        week(int): 第几周. Default to 1.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API_rank["info"]["weakly_details"]
    params = {"number": week}
    return await request("GET", url=api["url"], params=params)


async def get_history_popular_videos() -> dict:
    """
    获取入站必刷 85 个视频

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API_rank["info"]["history_popular"]
    params = {"page_size": 85, "page": 1}
    return await request("GET", url=api["url"], params=params)


async def get_hot_buzzwords(page_num: int = 1, page_size: int = 20) -> dict:
    """
    获取热词图鉴信息

    Args:
        page_num  (int): 页码. Defaults to 1.
        page_size (int): 每一页的数据大小. Defaults to 20.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["buzzwords"]
    params = {
        "pn": page_num,
        "ps": page_size,
        "type_id": 4
    }
    return await request("GET", api["url"], params = params)
