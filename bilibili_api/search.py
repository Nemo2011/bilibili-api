"""
bilibili_api.search

搜索
"""
from enum import Enum
from typing import Union
import json
from .utils.utils import get_api
from .utils.network_httpx import request, get_session

API = get_api("search")


class SearchObjectType(Enum):
    """
    搜索对象。
    + VIDEO : 视频
    + BANGUMI : 番剧
    + FT : 影视
    + LIVE : 直播
    + ARTICLE : 专栏
    + TOPIC : 话题
    + USER : 用户
    + LIVEUSER : 直播间用户
    """

    VIDEO = "video"
    BANGUMI = "media_bangumi"
    FT = "media_ft"
    LIVE = "live"
    ARTICLE = "article"
    TOPIC = "topic"
    USER = "bili_user"
    LIVEUSER = "live_user"
    PHOTO = "photo"


class OrderVideo(Enum):
    """
    视频搜索类型
    + TOTALRANK : 综合排序
    + CLICK : 最多点击
    + PUBDATE : 最新发布
    + DM : 最多弹幕
    + STOW : 最多收藏
    + SCORES : 最多评论
    Ps: Api 中 的 order_sort 字段决定顺序还是倒序

    """

    TOTALRANK = "totalrank"
    CLICK = "click"
    PUBDATE = "pubdate"
    DM = "dm"
    STOW = "stow"
    SCORES = "scores"


class OrderLiveRoom(Enum):
    """
    直播间搜索类型
    + NEWLIVE 最新开播
    + ONLINE 综合排序
    """

    NEWLIVE = "live_time"
    ONLINE = "online"


class OrderArticle(Enum):
    """
    文章的排序类型
    + TOTALRANK : 综合排序
    + CLICK : 最多点击
    + PUBDATE : 最新发布
    + ATTENTION : 最多喜欢
    + SCORES : 最多评论
    """

    TOTALRANK = "totalrank"
    PUBDATE = "pubdate"
    CLICK = "click"
    ATTENTION = "attention"
    SCORES = "scores"


class OrderUser(Enum):
    """
    搜索用户的排序类型
    + FANS : 按照粉丝数量排序
    + LEVEL : 按照等级排序
    """

    FANS = "fans"
    LEVEL = "level"


class CategoryTypePhoto(Enum):
    """
    相册分类
    + All 全部
    + DrawFriend 画友
    + PhotoFriend 摄影
    """

    All = 0
    DrawFriend = 2
    PhotoFriend = 1


class CategoryTypeArticle(Enum):
    """
    文章分类
    + All 全部
    + Anime
    + Game
    + TV
    + Life
    + Hobby
    + LightNovel
    + Technology
    """

    All = 0
    Anime = 2
    Game = 1
    TV = 28
    Life = 3
    Hobby = 29
    LightNovel = 16
    Technology = 17


async def search(keyword: str, page: int = 1):
    """
    只指定关键字在 web 进行搜索，返回未经处理的字典

    Args:
        keyword (str): 搜索关键词
        page    (int): 页码. Defaults to 1. 

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["search"]["web_search"]
    params = {"keyword": keyword, "page": page}
    return await request("GET", url=api["url"], params=params)


async def search_by_type(
    keyword: str,
    search_type: SearchObjectType = None,
    order_type: Union[OrderUser, OrderLiveRoom, OrderArticle, OrderVideo] = None,
    time_range: int = -1,
    topic_type: int = None,
    order_sort: int = None,
    category_id: Union[CategoryTypeArticle, CategoryTypePhoto, int] = None,
    page: int = 1,
    debug_param_func=None,
):
    """
    指定分区，类型，视频长度等参数进行搜索，返回未经处理的字典
    类型：视频(video)、番剧(media_bangumi)、影视(media_ft)、直播(live)、直播用户(liveuser)、专栏(article)、话题(topic)、用户(bili_user)

    Args:
        debug_param_func (func)                                              : 参数回调器，用来存储或者什么的
        order_sort       (int)                                               : 用户粉丝数及等级排序顺序 默认为0 由高到低：0 由低到高：1
        category_id      (Union[CategoryTypeArticle, CategoryTypePhoto, int]): 专栏/相簿分区筛选，指定分类，只在相册和专栏类型下生效
        time_range       (int)                                               : 指定时间，自动转换到指定区间，只在视频类型下生效 有四种：10分钟以下，10-30分钟，30-60分钟，60分钟以上
        topic_type       (int)                                               : 话题类型，指定 tid (可使用 channel 模块查询)
        order_type       (str)                                               : 排序分类类型
        keyword          (str)                                               : 搜索关键词
        search_type      (str)                                               : 搜索类型
        page             (int)                                               : 页码

    Returns:
        dict: 调用 API 返回的结果
    """
    params = {"keyword": keyword, "page": page}
    if search_type:
        params["search_type"] = search_type.value
    else:
        raise ValueError("Missing arg:search_type")
        # params["search_type"] = SearchObjectType.VIDEO.value
    # category_id
    if (
        search_type.value == SearchObjectType.ARTICLE.value
        or search_type.value == SearchObjectType.PHOTO.value
    ):
        if category_id:
            if isinstance(category_id, int):
                params["category_id"] = category_id
            else:
                params["category_id"] = category_id.value
    # time_code
    if search_type.value == SearchObjectType.VIDEO.value:
        if time_range > 60:
            time_code = 4
        elif 30 < time_range <= 60:
            time_code = 3
        elif 10 < time_range <= 30:
            time_code = 2
        elif 0 < time_range <= 10:
            time_code = 2
        else:
            time_code = 0
        params["duration"] = time_code
    # topic_type
    if topic_type:
        if isinstance(topic_type, int):
            params["tids"] = topic_type
        else:
            params["tids"] = topic_type.value
    # order_type
    if order_type:
        params["order"] = order_type.value
    # order_sort
    if search_type.value == SearchObjectType.USER.value:
        params["order_sort"] = order_sort
    if debug_param_func:
        debug_param_func(params)
    api = API["search"]["web_search_by_type"]
    return await request("GET", url=api["url"], params=params)


async def get_default_search_keyword():
    """
    获取默认的搜索内容

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["search"]["default_search_keyword"]
    return await request("GET", api["url"])


async def get_hot_search_keywords():
    """
    获取热搜

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["search"]["hot_search_keywords"]
    sess = get_session()
    return json.loads((await sess.request("GET", api["url"])).text)["cost"]


async def get_suggest_keywords(keyword: str):
    """
    通过一些文字输入获取搜索建议。类似搜索词的联想。

    Args:
        keyword(str): 搜索关键词

    Returns:
        List[str]: 关键词列表
    """
    keywords = []
    sess = get_session()
    api = API["search"]["suggest"]
    params = {"term": keyword}
    data = json.loads((await sess.request("GET", api["url"], params=params)).text)
    keys = data.keys()
    for key in keys:
        keywords.append(data[key]["value"])
    return keywords


async def search_games(keyword: str):
    """
    搜索游戏特用函数

    Args:
        keyword(str): 搜索关键词

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["search"]["game"]
    params = {"keyword": keyword}
    return await request("GET", api["url"], params=params)
