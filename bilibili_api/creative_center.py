"""
bilibili_api.creative_center

创作中心相关。

务必携带 Credential 信息，否则无法获取到数据。
"""

from enum import Enum
from typing import Union, List

from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.Credential import Credential

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


async def get_video_compare(credential: Credential) -> dict:
    """
    获取视频对比数据。

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 视频对比数据。
    """
    api = API["overview"]["compare"]
    return await request("GET", api["url"], credential=credential)


async def get_graph(credential: Credential, period: GraphPeriod = GraphPeriod.WEEK, graph_type: GraphType = GraphType.PLAY) -> dict:
    """
    获取统计图表数据。

    Args:
        credentials (Credential): Credential 凭据。
        period      (GraphPeriod): 时间段。
        graph_type  (GraphType):   图表类型。

    Returns:
        dict: 视频统计数据。
    """
    api = API["overview"]["graph"]
    params = {
        "period": period.value,
        "s_locale": "zh_CN",
        "type": graph_type.value,
    }
    return await request("GET", api["url"], params=params, credential=credential)


async def get_video_overview(credential: Credential, period: GraphPeriod = GraphPeriod.WEEK) -> dict:
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
        dict: 视频问卷数据。
    """
    api = API["survey"]
    params = {"type": 1}
    return await request("GET", api["url"], params=params, credential=credential)
