"""
杂项
"""
from enum import Enum
from .utils.utils import get_api
from .utils.network import request

API = get_api('misc')

class SearchObjectType(Enum):
    VIDEO = "video"
    BANGUMI = "media_bangumi"
    FT = "media_ft"
    LIVE = "live"
    ARTICLE = "article"
    TOPIC = "topic"
    USER = "bili_user"

async def web_search(keyword: str):
    """
    只指定关键字在 web 进行搜索，返回未经处理的字典

    Args:
        keyword (str): 搜索关键词
    """
    api = API["search"]["web_search"]
    params = {
        "keyword": keyword
    }
    return await request('GET', url=api["url"], params=params)

async def web_search_by_type(keyword: str, search_type: SearchObjectType):
    """
    指定关键字和类型进行搜索，返回未经处理的字典
    类型：视频(video)、番剧(media_bangumi)、影视(media_ft)、直播(live)、专栏(article)、话题(topic)、用户(bili_user)

    Args:
        keyword     (str): 搜索关键词
        search_type (str): 搜索类型
    """
    api = API["search"]["web_search_by_type"]
    params = {
        "keyword": keyword,
        "search_type": search_type.value
    }
    return await request('GET', url=api["url"], params=params)
