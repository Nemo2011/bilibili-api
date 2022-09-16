"""
bilibili_api.search

搜索
"""
from enum import Enum
import json
from .utils.utils import get_api, DictForm
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


class VideoOrder(Enum):
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


class LiveRoomOrder(Enum):
    """
    直播间搜索类型
    + NEWLIVE 最新开播
    + ONLINE 综合排序
    """
    NEWLIVE = "live_time"
    ONLINE = "online"


class ArticleOrder(Enum):
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


class UserOrder(Enum):
    """
    用户的排序类型
    + FANS : 按照粉丝数量排序
    + LEVEL : 按照等级排序
    """
    FANS = "fans"
    LEVEL = "level"


async def search(keyword: str, page: int = 1):
    """
    只指定关键字在 web 进行搜索，返回未经处理的字典

    Args:
        keyword (str): 搜索关键词
        page (int)   : 页码

    Returns:
        调用 api 返回的结果
    """
    api = API["search"]["web_search"]
    params = {"keyword": keyword, "page": page}
    return await request("GET", url=api["url"], params=params)


async def search_by_type(keyword: str, search_type: SearchObjectType,
                         rank_order: UserOrder | VideoOrder | ArticleOrder | LiveRoomOrder = None,
                         page: int = 1):
    """
    指定关键字和类型进行搜索，返回未经处理的字典
    类型：视频(video)、番剧(media_bangumi)、影视(media_ft)、直播(live)、专栏(article)、话题(topic)、用户(bili_user)

    Args:
        rank_order: (str): 排序类型
        keyword     (str): 搜索关键词
        search_type (str): 搜索类型
        page        (int): 页码
    Returns:
        调用 api 返回的结果
    """
    params = {"keyword": keyword, "search_type": search_type.value, "page": page}
    if rank_order:
        params["order"] = rank_order.value
    print(params)
    api = API["search"]["web_search_by_type"]
    return await request("GET", url=api["url"], params=params)


async def get_default_search_keyword():
    """
    获取默认的搜索内容

    Returns:
        调用 api 返回的结果
    """
    api = API["search"]["default_search_keyword"]
    return await request("GET", api["url"])


async def get_hot_search_keywords():
    """
    获取热搜

    Returns:
        调用 api 返回的结果
    """
    api = API["search"]["hot_search_keywords"]
    sess = get_session()
    return json.loads((await sess.request("GET", api["url"])).text)["cost"]


async def get_suggest_keywords(keyword: str):
    """
    通过一些文字输入获取搜索建议。类似搜索词的联想。

    Args:
        keyword(string): 搜索关键词

    Returns:
        List[string]: 关键词列表
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
