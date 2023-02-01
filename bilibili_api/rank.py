"""
bilibili_api.rank

和哔哩哔哩视频排行榜相关的 API
所有数据都会显示在热门页面
（点击主页“热门”按钮进入）
https://www.bilibili.com/v/popular/all
"""

from .utils.network_httpx import request
from .utils.utils import get_api
from enum import Enum

API = get_api("rank")


class RankAPIType(Enum):
    """
    排行榜 API 接口类型判断

    - PGC: https://api.bilibili.com/pgc/web/rank/list
    - V2: https://api.bilibili.com/x/web-interface/ranking/v2
    """
    PGC = "pgc"
    V2 = "x"


class RankDayType(Enum):
    """
    RankAPIType.PGC 排行榜时间类型
    """
    THREE_DAY = 3
    WEEK = 7


class RankType(Enum):
    """
    排行榜类型

    - ALL: 全部
    - BANGUMI: 番剧
    - GUOCHUAN_ANIME: 国产动画
    - GUOCHUANG: 国创番剧
    - DOCUMENTARY: 纪录片
    - DOUGA: 动画
    - MUSIC: 音乐
    - DANCE: 舞蹈
    - GAME: 游戏
    - KNOWLEDGE: 知识
    - TECHNOLOGY: 科技
    - SPORTS: 运动
    - CAR: 汽车
    - FOOD: 美食
    - ANIMAL: 动物圈
    - KICHIKU: 鬼畜
    - FASHION: 时尚
    - ENT: 娱乐
    - CINEPHILE: 影视
    - MOVIE: 电影
    - TV: 电视剧
    - VARIETY: 综艺
    - ORIGINAL: 原创
    - ROOKIE: 新人
    """
    ALL = {"api_type": RankAPIType.V2, "rid": 0, "type": "all"}
    BANGUMI = {"api_type": RankAPIType.PGC, "season_type": 1}
    GUOCHUAN_ANIME = {"api_type": RankAPIType.PGC, "season_type": 4}
    GUOCHUANG = {"api_type": RankAPIType.V2, "rid": 168}
    DOCUMENTARY = {"api_type": RankAPIType.V2, "rid": 177}
    DOUGA = {"api_type": RankAPIType.V2, "rid": 1}
    MUSIC = {"api_type": RankAPIType.V2, "rid": 3}
    DANCE = {"api_type": RankAPIType.V2, "rid": 129}
    GAME = {"api_type": RankAPIType.V2, "rid": 4}
    KNOWLEDGE = {"api_type": RankAPIType.V2, "rid": 36}
    TECHNOLOGY = {"api_type": RankAPIType.V2, "rid": 188}
    SPORTS = {"api_type": RankAPIType.V2, "rid": 234}
    CAR = {"api_type": RankAPIType.V2, "rid": 223}
    FOOD = {"api_type": RankAPIType.V2, "rid": 211}
    ANIMAL = {"api_type": RankAPIType.V2, "rid": 217}
    KICHIKU = {"api_type": RankAPIType.V2, "rid": 119}
    FASHION = {"api_type": RankAPIType.V2, "rid": 155}
    ENT = {"api_type": RankAPIType.V2, "rid": 5}
    CINEPHILE = {"api_type": RankAPIType.V2, "rid": 181}
    MOVIE = {"api_type": RankAPIType.PGC, "season_type": 2}
    TV = {"api_type": RankAPIType.PGC, "season_type": 3}
    VARIETY = {"api_type": RankAPIType.PGC, "season_type": 7}
    ORIGINAL = {"api_type": RankAPIType.V2, "rid": 0, "type": "origin"}
    ROOKIE = {"api_type": RankAPIType.V2, "rid": 0, "type": "rookie"}


async def get_hot_videos(pn: int = 1, ps: int = 20) -> dict:
    """
    获取热门视频

    Args:
        pn (int): 第几页. Default to 1.
        ps (int): 每页视频数. Default to 20.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["hot"]
    params = {"ps": ps, "pn": pn}
    return await request("GET", url=api["url"], params=params)


async def get_weakly_hot_videos_list() -> dict:
    """
    获取每周必看列表(仅概述)

    Returns:
        调用 API 返回的结果
    """
    api = API["info"]["weakly_series"]
    return await request("GET", url=api["url"])


async def get_weakly_hot_videos(week: int = 1) -> dict:
    """
    获取一周的每周必看视频列表

    Args:
        week(int): 第几周. Default to 1.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["weakly_details"]
    params = {"number": week}
    return await request("GET", url=api["url"], params=params)


async def get_history_popular_videos() -> dict:
    """
    获取入站必刷 85 个视频

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["history_popular"]
    params = {"page_size": 85, "page": 1}
    return await request("GET", url=api["url"], params=params)


async def get_rank(type_: RankType = RankType.ALL, day: RankDayType = RankDayType.THREE_DAY) -> dict:
    """
    获取视频排行榜

    Args:
        type_ (RankType): 排行榜类型. Defaults to RankType.ALL
        day (RankDayType): 排行榜时间. Defaults to RankDayType.THREE_DAY 
                           仅对 api_type 为 RankAPIType.PGC 有效

    Returns:
        dict: 调用 API 返回的结果
    """
    params = type_.value

    # 确定 API 接口类型

    if type_.value["api_type"] == RankAPIType.V2:
        api = API["info"]["v2-ranking"]
    elif type_.value["api_type"] == RankAPIType.PGC:
        api = API["info"]["pgc-ranking"]
        params["day"] = day.value
    del params["api_type"]

    return await request("GET", api["url"], params=params)


async def get_music_rank_list() -> dict:
    """
    获取全站音乐榜每周信息(不包括具体的音频列表)

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["music_weakly_series"]
    params = {"list_type": 1}
    return await request("GET", api["url"], params=params)


async def get_music_rank_weakly_detail(week: int = 1) -> dict:
    """
    获取全站音乐榜一周的详细信息(不包括具体的音频列表)

    Args:
        week(int): 第几周. Defaults to 1.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["music_weakly_details"]
    params = {"list_id": week}
    return await request("GET", api["url"], params=params)


async def get_music_rank_weakly_musics(week: int = 1) -> dict:
    """
    获取全站音乐榜一周的音频列表

    Args:
        week(int): 第几周. Defaults to 1.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["music_weakly_content"]
    params = {"list_id": week}
    return await request("GET", api["url"], params=params)
