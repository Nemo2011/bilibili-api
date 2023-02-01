"""
bilibili_api.rank

和哔哩哔哩视频排行榜相关的 API
所有数据都会显示在热门页面
（点击主页“热门”按钮进入）
https://www.bilibili.com/v/popular/all
"""

from .utils.network_httpx import request
from .utils.utils import get_api
from .utils.initial_state import get_initial_state
from enum import Enum

API = get_api("rank")


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
    - LIVE: 直播
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
    ALL = None
    BANGUMI = "https://www.bilibili.com/v/popular/rank/bangumi"
    GUOCHUAN_ANIME = "https://www.bilibili.com/v/popular/rank/guochan"
    GUOCHUANG = "https://www.bilibili.com/v/popular/rank/guochuang"
    DOCUMENTARY = "https://www.bilibili.com/v/popular/rank/documentary"
    DOUGA = "https://www.bilibili.com/v/popular/rank/douga"
    MUSIC = "https://www.bilibili.com/v/popular/rank/music"
    DANCE = "https://www.bilibili.com/v/popular/rank/dance"
    GAME = "https://www.bilibili.com/v/popular/rank/game"
    KNOWLEDGE = "https://www.bilibili.com/v/popular/rank/knowledge"
    TECHNOLOGY = "https://www.bilibili.com/v/popular/rank/tech"
    SPORTS = "https://www.bilibili.com/v/popular/rank/sports"
    CAR = "https://www.bilibili.com/v/popular/rank/car"
    LIVE = "https://www.bilibili.com/v/popular/rank/life"
    FOOD = "https://www.bilibili.com/v/popular/rank/food"
    ANIMAL = "https://www.bilibili.com/v/popular/rank/animal"
    KICHIKU = "https://www.bilibili.com/v/popular/rank/kichiku"
    FASHION = "https://www.bilibili.com/v/popular/rank/fashion"
    ENT = "https://www.bilibili.com/v/popular/rank/ent"
    CINEPHILE = "https://www.bilibili.com/v/popular/rank/cinephile"
    MOVIE = "https://www.bilibili.com/v/popular/rank/movie"
    TV = "https://www.bilibili.com/v/popular/rank/tv"
    VARIETY = "https://www.bilibili.com/v/popular/rank/variety"
    ORIGINAL = "https://www.bilibili.com/v/popular/rank/origin"
    ROOKIE = "https://www.bilibili.com/v/popular/rank/rookie"



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


async def get_rank(type_: RankType = RankType.ALL) -> dict:
    """
    获取视频排行榜

    Args:
        type_ (RankType): 排行榜类型. Defaults to RankType.ALL

    Returns:
        dict: 调用 API 返回的结果
    """
    if type_ != RankType.ALL:
        return await get_initial_state(type_.value)
    api = API["info"]["ranking"]
    params = {"type": "all", "rid": 0}
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
