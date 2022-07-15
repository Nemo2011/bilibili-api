"""
bilibili_api.search

搜索
"""
from enum import Enum
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

    """

    VIDEO = "video"
    BANGUMI = "media_bangumi"
    FT = "media_ft"
    LIVE = "live"
    ARTICLE = "article"
    TOPIC = "topic"
    USER = "bili_user"


async def web_search(keyword: str, page: int = 1):
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


async def web_search_by_type(
    keyword: str, search_type: SearchObjectType, page: int = 1
):
    """
    指定关键字和类型进行搜索，返回未经处理的字典
    类型：视频(video)、番剧(media_bangumi)、影视(media_ft)、直播(live)、专栏(article)、话题(topic)、用户(bili_user)

    Args:
        keyword     (str): 搜索关键词
        search_type (str): 搜索类型
        page        (int): 页码
    Returns:
        调用 api 返回的结果
    """
    api = API["search"]["web_search_by_type"]
    params = {"keyword": keyword, "search_type": search_type.value, "page": page}
    return await request("GET", url=api["url"], params=params)

async def get_default_search_keyword():
    """
    获取默认的搜索内容

    Returns:
        调用 api 返回的结果
    """
    api = API['search']['default_search_keyword']
    return await request("GET", api['url'])

async def get_hot_search_keywords():
    """
    获取热搜

    Returns:
        调用 api 返回的结果
    """
    api = API['search']['hot_search_keywords']
    sess = get_session()
    return json.loads((await sess.request("GET", api['url'])).text)['cost']
    