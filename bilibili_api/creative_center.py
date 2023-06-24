"""
bilibili_api.creative_center

创作中心相关。

务必携带 Credential 信息，否则无法获取到数据。
"""

from enum import Enum
from typing import Union, List

from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.credential import Credential

API = get_api("creative_center")


class GraphPeriod(Enum):
    """
    统计图表的时间段。

    + YESTERDAY: 昨天
    + WEEK: 近一周
    + MONTH: 近一月
    + THREE_MONTH: 近三月
    + TOTAL: 历史累计
    """

    YESTERDAY = -1
    WEEK = 0
    MONTH = 1
    THREE_MONTH = 2
    TOTAL = 3


class FanGraphPeriod(Enum):
    """
    粉丝统计图表的时间段。

    + YESTERDAY: 昨天
    + WEEK: 近一周
    + MONTH: 近一月
    + THREE_MONTH: 近三月
    """

    YESTERDAY = -1
    WEEK = 0
    MONTH = 1
    THREE_MONTH = 2


class GraphType(Enum):
    """
    统计图表的类型。

    + PLAY: 播放量
    + VISITOR: 访问量
    + FAN: 粉丝数
    + LIKE: 点赞数
    + FAV: 收藏数
    + SHARE: 分享数
    + COMMENT: 评论数
    + DAMKU: 弹幕数
    + COIN: 投币数
    + ELEC: 充电数
    """

    PLAY = "play"
    VISITOR = "visitor"
    FAN = "fan"
    LIKE = "like"
    FAV = "fav"
    SHARE = "share"
    COMMENT = "comment"
    DAMKU = "dm"
    COIN = "coin"
    ELEC = "elec"


class FanGraphType(Enum):
    """
    粉丝统计图表的类型。

    + ALL_FANS: 粉丝总量
    + FAN: 新增粉丝
    + FOLLOW: 新增关注
    + UNFOLLOW: 取消关注
    """

    ALL_FANS = "all_fans"
    NEW_FANS = "fan"
    FOLLOW = "follow"
    UNFOLLOW = "unfollow"


class ArticleInfoType(Enum):
    """
    文章统计信息的类型。

    + READ: 阅读
    + COMMENT: 评论
    + SHARE: 分享
    + COIN: 投币
    + FAV: 收藏
    + LIKE: 点赞
    """

    READ = 1
    COMMENT = 2
    SHARE = 3
    COIN = 4
    FAV = 5
    LIKE = 6


class Copyright(Enum):
    """
    稿件播放完成率对比的版权类型。

    + ALL: 全部
    + ORIGINAL: 原创
    + REPRINT: 转载
    """

    ALL = 0
    ORIGINAL = 1
    REPRINT = 2


async def get_compare(credential: Credential) -> dict:
    """
    获取对比数据。

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 视频对比数据。
    """
    api = API["overview"]["compare"]
    return await request("GET", api["url"], credential=credential)


async def get_graph(
    credential: Credential,
    period: GraphPeriod = GraphPeriod.WEEK,
    graph_type: GraphType = GraphType.PLAY,
) -> dict:
    """
    获取统计图表数据。

    Args:
        credentials (Credential): Credential 凭据。

        period      (GraphPeriod): 时间段。

        graph_type  (GraphType):   图表类型。

    Returns:
        dict: 视频统计图表数据。
    """
    api = API["overview"]["graph"]
    params = {
        "period": period.value,
        "s_locale": "zh_CN",
        "type": graph_type.value,
    }
    return await request("GET", api["url"], params=params, credential=credential)


async def get_overview(
    credential: Credential, period: GraphPeriod = GraphPeriod.WEEK
) -> dict:
    """
    获取概览数据。

    Args:
        credentials (Credential): Credential 凭据。

        period      (GraphPeriod): 时间段。

    Returns:
        dict: 视频概览数据。
    """
    api = API["overview"]["num"]
    # 不知道 tab 的作用是什么，但是不传会报错
    params = {"period": period.value, "s_locale": "zh_CN", "tab": 0}
    return await request("GET", api["url"], params=params, credential=credential)


async def get_video_survey(credential: Credential) -> dict:
    """
    获取视频各分区中占比排行。

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 视频分区排行数据。
    """
    api = API["video"]["survey"]
    params = {"type": 1}
    return await request("GET", api["url"], params=params, credential=credential)


async def get_video_playanalysis(
    credential: Credential, copyright: Copyright = Copyright.ALL
) -> dict:
    """
    获取稿件播放完成率对比。

    Args:
        credentials (Credential): Credential 凭据。

        copyright   (Copyright):   版权类型。

    Returns:
        dict: 稿件播放完成率对比数据。
    """
    api = API["video"]["playanalysis"]
    params = {"copyright": copyright.value}
    return await request("GET", api["url"], params=params, credential=credential)


async def get_video_source(credential: Credential) -> dict:
    """
    获取稿件播放来源分布。

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 视频来源分布数据。
    """
    api = API["video"]["source"]
    params = {"s_locale": "zh_CN"}
    return await request("GET", api["url"], params=params, credential=credential)


async def get_fan_overview(
    credential: Credential, period: FanGraphPeriod = FanGraphPeriod.WEEK
) -> dict:
    """
    获取粉丝概览数据。

    Args:
        credentials (Credential): Credential 凭据。

        period      (FanGraphPeriod): 时间段。

    Returns:
        dict: 粉丝概览数据。
    """
    api = API["fan"]["overview"]
    params = {"period": period.value}
    return await request("GET", api["url"], params=params, credential=credential)


async def get_fan_graph(
    credential: Credential,
    period: FanGraphPeriod = FanGraphPeriod.WEEK,
    graph_type: FanGraphType = FanGraphType.ALL_FANS,
) -> dict:
    """
    获取粉丝图表数据。

    Args:
        credentials (Credential): Credential 凭据。

        period      (FanGraphPeriod): 时间段。

        graph_type  (FanGraphType):   图表类型。

    Returns:
        dict: 粉丝图表数据。
    """
    api = API["fan"]["graph"]
    params = {"period": period.value, "type": graph_type.value}
    return await request("GET", api["url"], params=params, credential=credential)


async def get_article_overview(credential: Credential) -> dict:
    """
    获取文章概览数据。

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 文章概览数据。
    """
    api = API["article"]["overview"]
    return await request("GET", api["url"], credential=credential)


async def get_article_graph(
    credential: Credential, graph_type: ArticleInfoType = ArticleInfoType.READ
) -> dict:
    """
    获取文章图表数据。

    Args:
        credentials (Credential): Credential 凭据。

        graph_type  (ArticleInfoType):   图表类型。

    Returns:
        dict: 文章图表数据。
    """

    api = API["article"]["graph"]
    params = {"type": graph_type.value}
    return await request("GET", api["url"], params=params, credential=credential)


async def get_article_rank(
    credential: Credential, rank_type: ArticleInfoType = ArticleInfoType.READ
) -> dict:
    """
    获取文章排行数据。

    Args:
        credentials (Credential): Credential 凭据。

        rank_type  (ArticleInfoType):   排行依据。

    Returns:
        dict: 文章排行数据。
    """

    api = API["article"]["rank"]
    params = {"type": rank_type.value}
    return await request("GET", api["url"], params=params, credential=credential)


async def get_article_source(credential: Credential) -> dict:
    """
    获取文章阅读终端数据

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 文章阅读终端数据。
    """

    api = API["article"]["source"]
    return await request("GET", api["url"], credential=credential)
