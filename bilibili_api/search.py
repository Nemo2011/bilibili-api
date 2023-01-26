"""
bilibili_api.search

搜索
"""
from enum import Enum
from typing import Callable, Union, List
import json
from .utils.utils import get_api
from .utils.network_httpx import request, get_session
from .video_zone import VideoZoneTypes

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


class OrderCheese(Enum):
    """
    课程搜索排序类型

    + RECOMMEND: 综合
    + SELL     : 销量最高
    + NEW      : 最新上架
    + CHEEP    : 售价最低
    """
    RECOMMEND = -1
    SELL = 1
    NEW = 2
    CHEEP = 3


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
    + Anime 动画
    + Game 游戏
    + TV 电视
    + Life 生活
    + Hobby 兴趣
    + LightNovel 轻小说
    + Technology 科技
    """

    All = 0
    Anime = 2
    Game = 1
    TV = 28
    Life = 3
    Hobby = 29
    LightNovel = 16
    Technology = 17


async def search(keyword: str, page: int = 1) -> dict:
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
    search_type: Union[SearchObjectType, None] = None,
    order_type: Union[OrderUser, OrderLiveRoom, OrderArticle, OrderVideo, None] = None,
    time_range: int = -1,
    video_zone_type: Union[int, VideoZoneTypes, None] = None,
    order_sort: Union[int, None] = None,
    category_id: Union[CategoryTypeArticle, CategoryTypePhoto, int, None] = None,
    page: int = 1,
    debug_param_func: Union[Callable, None]=None,
) -> dict:
    """
    指定分区，类型，视频长度等参数进行搜索，返回未经处理的字典
    类型：视频(video)、番剧(media_bangumi)、影视(media_ft)、直播(live)、直播用户(liveuser)、专栏(article)、话题(topic)、用户(bili_user)

    Args:
        debug_param_func (Callable | None, optional)                                             : 参数回调器，用来存储或者什么的
        order_sort       (int | None, optional)                                                  : 用户粉丝数及等级排序顺序 默认为0 由高到低：0 由低到高：1
        category_id      (CategoryTypeArticle | CategoryTypePhoto | int | None, optional)        : 专栏/相簿分区筛选，指定分类，只在相册和专栏类型下生效
        time_range       (int, optional)                                                         : 指定时间，自动转换到指定区间，只在视频类型下生效 有四种：10分钟以下，10-30分钟，30-60分钟，60分钟以上
        video_zone_type        (int | ZoneTypes | None, optional)                                : 话题类型，指定 tid (可使用 channel 模块查询)
        order_type       (OrderUser | OrderLiveRoom | OrderArticle | OrderVideo | None, optional): 排序分类类型
        keyword          (str)                                                                   : 搜索关键词
        search_type      (SearchObjectType | None, optional)                                     : 搜索类型
        page             (int, optional)                                                         : 页码

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
            time_code = 1
        else:
            time_code = 0
        params["duration"] = time_code
    # zone_type
    if zone_type:
        if isinstance(zone_type, int):
            params["tids"] = zone_type
        elif isinstance(zone_type, VideoZoneTypes):
            params["tids"] = zone_type.value
        else:
            params["tids"] = zone_type.value
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


async def get_default_search_keyword() -> dict:
    """
    获取默认的搜索内容

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["search"]["default_search_keyword"]
    return await request("GET", api["url"])


async def get_hot_search_keywords() -> dict:
    """
    获取热搜

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["search"]["hot_search_keywords"]
    sess = get_session()
    return json.loads((await sess.request("GET", api["url"])).text)["cost"]


async def get_suggest_keywords(keyword: str) -> List[str]:
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


async def search_games(keyword: str) -> dict:
    """
    搜索游戏特用函数

    Args:
        keyword (str): 搜索关键词

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["search"]["game"]
    params = {"keyword": keyword}
    return await request("GET", api["url"], params=params)


async def search_manga(keyword: str, page_num: int = 1, page_size: int = 9):
    """
    搜索漫画特用函数

    Args:
        keyword   (str): 搜索关键词
        page_num  (int): 页码. Defaults to 1.
        page_size (int): 每一页的数据大小. Defaults to 9.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["search"]["manga"]
    data = {
        "key_word": keyword,
        "page_num": page_num,
        "page_size": page_size
    }
    return await request(
        "POST", api["url"], data=data, no_csrf=True
    )


async def search_cheese(keyword: str, page_num: int = 1, page_size: int = 30, order: OrderCheese = OrderCheese.RECOMMEND):
    """
    搜索课程特用函数

    Args:
        keyword   (str)        : 搜索关键词
        page_num  (int)        : 页码. Defaults to 1.
        page_size (int)        : 每一页的数据大小. Defaults to 30.
        order     (OrderCheese): 排序方式. Defaults to OrderCheese.RECOMMEND

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["search"]["cheese"]
    params = {
        "word": keyword,
        "page": page_num,
        "page_size": page_size,
        "sort_type": order.value
    }
    return await request(
        "GET",
        api["url"],
        params=params
    )
