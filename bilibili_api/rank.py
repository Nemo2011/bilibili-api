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


class RankType:
    """
    排行榜类型

    - All: 全部
    - Bangumi: 番剧
    - GuochuanAnime: 国产动画
    - Guochuang: 国创相关
    - Documentary: 纪录片
    - Douga: 动画
    - Music: 音乐
    - Dance: 舞蹈
    - Game: 游戏
    - Knowledge: 知识
    - Technology: 科技
    - Sports: 运动
    - Car: 汽车
    - Life: 生活
    - Food: 美食
    - Animal: 动物圈
    - Kitchen: 鬼畜
    - Fashion: 时尚
    - Ent: 娱乐
    - Cinephile: 影视
    - Movie: 电影
    - TV: 电视剧
    - Variety: 综艺
    - Original: 原创
    - Rookie: 新人
    """
    class All:
        """
        全部
        """
        api_type = RankAPIType.V2
        rid = 0
        type = "all"

    class Bangumi:
        """
        番剧
        """
        api_type = RankAPIType.PGC
        season_type = 1

    class GuochuanAnime:
        """
        国产动画
        """
        api_type = RankAPIType.PGC
        season_type = 4

    class Guochuang:
        """
        国创相关
        """
        api_type = RankAPIType.V2
        rid = 168

    class Documentary:
        """
        纪录片
        """
        api_type = RankAPIType.PGC
        season_type = 3

    class Douga:
        """
        动画
        """
        api_type = RankAPIType.V2
        rid = 1

    class Music:
        """
        音乐
        """
        api_type = RankAPIType.V2
        rid = 3

    class Dance:
        """
        舞蹈
        """
        api_type = RankAPIType.V2
        rid = 129

    class Game:
        """
        游戏
        """
        api_type = RankAPIType.V2
        rid = 4

    class Knowledge:
        """
        知识
        """
        api_type = RankAPIType.V2
        rid = 36

    class Technology:
        """
        科技
        """
        api_type = RankAPIType.V2
        rid = 188

    class Sports:
        """
        运动
        """
        api_type = RankAPIType.V2
        rid = 234

    class Car:
        """
        汽车
        """
        api_type = RankAPIType.V2
        rid = 223
    
    class Life:
        """
        生活
        """
        api_type = RankAPIType.V2
        rid = 160

    class Food:
        """
        美食
        """
        api_type = RankAPIType.V2
        rid = 211

    class Animal:
        """
        动物圈
        """
        api_type = RankAPIType.V2
        rid = 217

    class Kitchen:
        """
        鬼畜
        """
        api_type = RankAPIType.V2
        rid = 119

    class Fashion:
        """
        时尚
        """
        api_type = RankAPIType.V2
        rid = 155

    class Ent:
        """
        娱乐
        """
        api_type = RankAPIType.V2
        rid = 5

    class Cinephile:
        """
        影视
        """
        api_type = RankAPIType.V2
        rid = 181
    
    class Movie:
        """
        电影
        """
        api_type = RankAPIType.PGC
        season_type = 2

    class TV:
        """
        电视剧
        """
        api_type = RankAPIType.PGC
        season_type = 5

    class Variety:
        """
        综艺
        """
        api_type = RankAPIType.PGC
        season_type = 7

    class Original:
        """
        原创
        """
        api_type = RankAPIType.V2
        rid = 0
        type = "origin"
    
    class Rookie:
        """
        新人
        """
        api_type = RankAPIType.V2
        rid = 0
        type = "rookie"

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


async def get_rank(type_: RankType = RankType.All, day: RankDayType = RankDayType.THREE_DAY) -> dict:
    """
    获取视频排行榜

    Args:
        type_ (RankType): 排行榜类型. Defaults to RankType.ALL
        day (RankDayType): 排行榜时间. Defaults to RankDayType.THREE_DAY 
                           仅对 api_type 为 RankAPIType.PGC 有效

    Returns:
        dict: 调用 API 返回的结果
    """
    params = {}

    # 确定 API 接口类型
    if type_.api_type == RankAPIType.V2:
        api = API["info"]["v2-ranking"]
        params["rid"] = type_.rid
    elif type_.api_type == RankAPIType.PGC:
        api = API["info"]["pgc-ranking"]
        params["season_type"] = type_.season_type
        params["day"] = day.value

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
