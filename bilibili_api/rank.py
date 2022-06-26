"""
bilibili_api.bank

和哔哩哔哩视频排行榜相关的 API
所有数据都会显示在热门页面
（点击主页“热门”按钮进入）
https://www.bilibili.com/v/popular/all
"""

from .utils.network import request
from .utils.utils import get_api

API = get_api("rank")

async def get_hot_videos():
    """
    获取热门视频

    Returns:
        调用 API 返回的结果
    """
    api = API['info']['hot']
    return await request("GET", url=api['url'])

async def get_weakly_hot_videos_list():
    """
    获取每周必看列表(仅概述)

    Returns:
        调用 API 返回的结果
    """
    api = API['info']['weakly_series']
    return await request("GET", url=api['url'])

async def get_weakly_hot_videos(week: int=1):
    """
    获取一周的每周必看视频列表

    Args:
        week(int): 第几周, default to 1

    Returns:
        调用 API 返回的结果
    """
    api = API['info']['weakly_details']
    params = {
        "number": week
    }
    return await request("GET", url=api['url'], params=params)

async def get_history_popular_videos():
    """
    获取入站必刷 85 个视频

    Returns:
        调用 API 返回的结果
    """
    api = API['info']['history_popular']
    params = {
        "page_size": 85, 
        "page": 1
    }
    return await request("GET", url=api['url'], params=params)

async def get_rank():
    """
    获取视频排行榜

    Returns:
        调用 API 返回的结果
    """
    api = API['info']['ranking']
    params = {
        "type": "all", 
        "rid": 0
    }
    return await request("GET", api['url'], params=params)
