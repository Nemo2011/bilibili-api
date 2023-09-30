"""
bilibili_api.creative_center

创作中心相关。

务必携带 Credential 信息，否则无法获取到数据。
"""

from enum import Enum
from typing import List, Union, Optional
from datetime import datetime

from .video_zone import VideoZoneTypes
from .utils.utils import get_api
from .utils.credential import Credential
from .utils.network import Api

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


class UploadManagerOrder(Enum):
    """
    内容管理排序字段。

    + CLICK: 点击
    + STOW: 收藏
    + SENDDATE: 上传日期
    + DM_COUNT: 弹幕数量
    + COMMENT_COUNT: 评论数量
    """

    CLICK = "click"
    STOW = "stow"
    SENDDATE = "senddate"
    DM_COUNT = "dm_count"
    COMMENT_COUNT = "scores"  # wtf the scores means


class UploadManagerStatus(Enum):
    """
    内容管理稿件状态字段。

    + ALL: 全部稿件
    + PUBED: 已通过
    + IS_PUBING: 进行中
    + NOT_PUBED: 未通过
    """

    ALL = "is_pubing,pubed,not_pubed"
    PUBED = "pubed"
    IS_PUBING = "is_pubing"
    NOT_PUBED = "not_pubed"


class UploadManagerSort(Enum):
    """
    内容管理文章排序字段。

    + CREATED_TIME: 创建日期
    + LIKE: 点赞
    + COMMENT: 评论
    + FAV: 收藏
    + COIN: 投币
    """

    CREATED_TIME = 1
    LIKE = 2
    COMMENT = 3
    FAV = 5
    COIN = 6


class UploadManagerArticleStatus(Enum):
    """
    内容管理文章状态字段。

    + ALL: 全部稿件
    + PUBED: 已通过
    + IS_PUBING: 进行中
    + NOT_PUBED: 未通过
    """

    ALL = 0
    PUBED = 2
    IS_PUBING = 1
    NOT_PUBED = 3


class ArchiveType(Enum):
    """
    评论管理中的稿件类型。

    + VIDEO: 视频
    + ARTICLE: 文章
    + AUDIO: 音频
    """

    VIDEO = 1  # 视频
    ARTICLE = 12  # 文章
    AUDIO = 14  # 音频


class CommentManagerOrder(Enum):
    """
    评论管理中的排序字段。

    + RECENTLY: 最近
    + LIKE: 点赞
    + REPLY: 回复
    """

    RECENTLY = 1  # 最近
    LIKE = 2  # 点赞
    REPLY = 3  # 回复


class DanmakuMode(Enum):
    """
    弹幕模式。

    + ROLL: 滚动
    + BOTTOM: 底端
    + TOP: 顶端
    + REVERSE: 逆向
    + ADVANCED: 高级
    + CODE: 代码
    + BAS: BAS 补充注释
    """

    ROLL = 1  # 滚动
    BOTTOM = 4  # 底端
    TOP = 5  # 顶端
    REVERSE = 6  # 逆向
    ADVANCED = 7  # 高级
    CODE = 8  # 代码
    BAS = 9  # BAS


class DanmakuPool(Enum):
    """
    子弹幕池类型。

    + NORMAL: 普通
    + SUBTITLE: 字幕
    + SPECIAL: 特殊
    """

    NORMAL = 0  # 普通
    SUBTITLE = 1  # 字幕
    SPECIAL = 2  # 特殊


async def get_compare(credential: Credential) -> dict:
    """
    获取对比数据。

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 视频对比数据。
    """
    api = API["overview"]["compare"]
    return await Api(**api, credential=credential).result


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
    return await Api(**api, credential=credential).update_params(**params).result


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
    return await Api(**api, credential=credential).update_params(**params).result


async def get_video_survey(credential: Credential) -> dict:
    """
    获取视频各分区中占比排行。

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 视频分区排行数据。
    """
    api = API["data-up"]["video"]["survey"]
    params = {"type": 1}
    return await Api(**api, credential=credential).update_params(**params).result


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
    api = API["data-up"]["video"]["playanalysis"]
    params = {"copyright": copyright.value}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_video_source(credential: Credential) -> dict:
    """
    获取稿件播放来源分布。

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 视频来源分布数据。
    """
    api = API["data-up"]["video"]["source"]
    params = {"s_locale": "zh_CN"}
    return await Api(**api, credential=credential).update_params(**params).result


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
    api = API["data-up"]["fan"]["overview"]
    params = {"period": period.value}
    return await Api(**api, credential=credential).update_params(**params).result


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
    api = API["data-up"]["fan"]["graph"]
    params = {"period": period.value, "type": graph_type.value}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_article_overview(credential: Credential) -> dict:
    """
    获取文章概览数据。

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 文章概览数据。
    """
    api = API["data-up"]["article"]["overview"]
    return await Api(**api, credential=credential).result


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

    api = API["data-up"]["article"]["graph"]
    params = {"type": graph_type.value}
    return await Api(**api, credential=credential).update_params(**params).result


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

    api = API["data-up"]["article"]["rank"]
    params = {"type": rank_type.value}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_article_source(credential: Credential) -> dict:
    """
    获取文章阅读终端数据

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 文章阅读终端数据。
    """

    api = API["data-up"]["article"]["source"]
    return await Api(**api, credential=credential).result


"""
upload manager

https://member.bilibili.com/platform/upload-manager
"""


async def get_video_draft_upload_manager_info(credential: Credential) -> dict:
    """
    获取内容管理视频草稿信息

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 内容管理视频草稿信息。
    """

    api = API["upload-manager"]["video_draft"]
    return await Api(**api, credential=credential).result


async def get_video_upload_manager_info(
    credential: Credential,
    is_interative: bool = False,
    pn: int = 1,
    ps: int = 10,
    order: UploadManagerOrder = UploadManagerOrder.CLICK,
    tid: Union[VideoZoneTypes, None, int] = None,
    status: UploadManagerStatus = UploadManagerStatus.ALL,
) -> dict:
    """
    获取内容管理视频信息

    Args:
        credentials (Credential): Credential 凭据。

        is_interative (bool): 是否为互动视频

        pn (int): 页码

        ps (int): 每页项数

        tid: (VideoZoneTypes, None, int): 分区

        status (UploadManagerStatus): 稿件状态

        order (UploadManagerOrder): 稿件排序

    Returns:
        dict: 内容管理视频信息。
    """
    params = {
        "pn": pn,
        "ps": ps,
        "coop": 1,
        "status": status.value,
        "order": order.value,
        "interactive": 2 if is_interative else 1,
        "tid": tid.value if isinstance(tid, Enum) else tid,
    }
    api = API["upload-manager"]["video"]
    return await Api(**api, credential=credential).update_params(**params).result


async def get_article_upload_manager_info(
    credential: Credential,
    status: UploadManagerArticleStatus = UploadManagerArticleStatus.ALL,
    sort: UploadManagerSort = UploadManagerSort.CREATED_TIME,
    pn: int = 1,
) -> dict:
    """
    获取内容管理文章信息

    Args:
        credentials (Credential): Credential 凭据。

        pn (int): 页码

        status (UploadManagerArticleStatus): 稿件状态

        sort (UploadManagerSort): 稿件排序

    Returns:
        dict: 内容管理文章信息。
    """

    params = {"pn": pn, "group": status.value, "sort": sort.value, "mobi_app": "pc"}
    api = API["upload-manager"]["article"]
    return await Api(**api, credential=credential).update_params(**params).result


async def get_article_list_upload_manager_info(credential: Credential) -> dict:
    """
    获取内容管理文章信息

    Args:
        credentials (Credential): Credential 凭据。

    Returns:
        dict: 内容管理文集信息。
    """

    api = API["upload-manager"]["article_list"]
    return await Api(**api, credential=credential).result


"""
comment manager

https://member.bilibili.com/platform/comment
"""


async def get_comments(
    credential: Credential,
    oid: Optional[int] = None,
    keyword: Optional[str] = None,
    archive_type: ArchiveType = ArchiveType.VIDEO,
    order: CommentManagerOrder = CommentManagerOrder.RECENTLY,
    filter: int = -1,
    pn: int = 1,
    ps: int = 10,
    charge_plus_filter: bool = False,
) -> dict:
    """
    获取评论

    Args:
        credentials (Credential): Credential 凭据。

        oid (Optional, int): 指定稿件

        keyword (Optional, str): 关键词

        archive_type (ArchiveType): 稿件类型

        order (CommentManagerOrder): 排序字段

        filter (int): 筛选器，作用未知

        pn (int): 页码

        ps (int): 每页项数

        charge_plus_filter (bool): charge_plus_filter

    Returns:
        dict: 评论管理评论信息。
    """

    params = {
        "order": order.value,
        "filter": filter,
        "type": archive_type.value,
        "pn": pn,
        "ps": ps,
        "charge_plus_filter": charge_plus_filter,
    }

    if keyword is not None:
        params["keyword"] = keyword
    if oid is not None:
        params["oid"] = oid

    api = API["comment-manager"]["fulllist"]
    return await Api(**api, credential=credential).update_params(**params).result


async def del_comments(
    credential: Credential,
    oid: Union[int, List[int]],
    rpid: Union[int, List[int]],
    archive_type: ArchiveType = ArchiveType.VIDEO,
):
    """
    删除评论

    每个评论对应一个 oid

    Args:
        credentials (Credential): Credential 凭据。

        oid (int, lsit): 指定稿件

        rpid (int, lsit): 指定评论

        archive_type (ArchiveType): 稿件类型
    """
    data = {
        "oid": ",".join(oid) if isinstance(oid, list) else oid,
        "type": archive_type.value,
        "rpid": ",".join(rpid) if isinstance(rpid, list) else rpid,
        "jsonp": "jsonp",
        "csrf": credential.bili_jct,
    }

    api = API["comment-manager"]["del"]
    return await Api(**api, credential=credential).update_data(**data).result


"""
danmaku manager

https://member.bilibili.com/platform/inter-active/danmu
"""


async def get_recently_danmakus(
    credential: Credential, pn: int = 1, ps: int = 50
) -> dict:
    """
    最近弹幕

    Args:
        credential (Credential): Credential 凭据。

        pn (int): 页码。

        ps (int): 每页项数。

    Returns:
        dict: 弹幕管理最近弹幕信息。
    """

    params = {"pn": pn, "ps": ps}

    api = API["danmaku-manager"]["recent"]
    return await Api(**api, credential=credential).update_params(**params).result


class DanmakuOrder(Enum):
    """
    弹幕排序依据

    + CTIME: 发送时间
    + LIKE_COUNT: 点赞数
    """

    CTIME = "ctime"
    LIKE_COUNT = "like_count"


class DanmakuSort(Enum):
    """
    弹幕排序顺序

    + DESC: 降序
    + ASC: 升序
    """

    DESC = "desc"
    ASC = "asc"


class DanmakuType(Enum):
    """
    弹幕筛选类型

    + ALL: 全部
    + PROTECT: 保护弹幕
    """

    ALL = 0
    PROTECT = 2


async def get_dammakus(
    credential: Credential,
    oid: int,
    select_type: DanmakuType = DanmakuType.ALL,
    archive_type: ArchiveType = ArchiveType.VIDEO,
    mids: Optional[Union[int, List[int]]] = None,
    keyword: Optional[str] = None,
    progress_from: Optional[int] = None,
    progress_to: Optional[int] = None,
    ctime_from: Optional[datetime] = None,
    ctime_to: Optional[datetime] = None,
    modes: Optional[Union[DanmakuMode, List[DanmakuMode]]] = None,
    pools: Optional[Union[DanmakuPool, List[DanmakuPool]]] = None,
    attrs=None,  # 未知参数，我在高级筛选里面找不到
    order: DanmakuOrder = DanmakuOrder.CTIME,
    sort: DanmakuSort = DanmakuSort.DESC,
    pn: int = 1,
    ps: int = 50,
    cp_filter: bool = False,
) -> dict:
    """
    弹幕搜索

    Args:
        credential (Credential): Credential 凭据

        oid (int): 稿件oid，用逗号分隔

        select_type (DanmakuType): 弹幕类型

        archive_type (ArchiveType): 稿件类型

        mids (list[int], int): 用户mids，用逗号分隔或者直接 int

        keyword (str): 关键词

        progress_from (int): 进度开始

        progress_to (int): 进度结束

        ctime_from (datetime.datetime): 创建时间起始

        ctime_to (datetime.datetime): 创建时间结束

        modes (DanmakuMode): 弹幕模式。

        pool (DanmakuPool): 弹幕池

        attrs (Unknown): 弹幕属性，未知参数

        order (DanmakuOrder): 排序字段

        sort (DanmakuSort): 排序方式

        pn (int): 页码。

        ps (int): 每页项数。

        cp_filter (bool): 是否过滤CP弹幕。未知参数，默认为 False

    Returns:
        dict: 弹幕搜索结果
    """
    params = {
        "oid": oid,
        "type": archive_type.value,
        "mids": ",".join(mids) if isinstance(mids, list) else mids,
        "select_type": select_type.value,
        "keyword": keyword,
        "progress_from": progress_from,
        "progress_to": progress_to,
        "ctime_from": ctime_from.strftime("%d-%m-%Y %H:%M:%S")
        if ctime_from is not None
        else None,
        "ctime_to": ctime_to.strftime("%d-%m-%Y %H:%M:%S")
        if ctime_to is not None
        else None,
        "modes": (
            ",".join([mode.value for mode in modes])
            if isinstance(modes, list)
            else modes.value
        )
        if modes is not None
        else None,
        "pool": (
            ",".join([pool.value for pool in pools])
            if isinstance(pools, list)
            else pools.value
        )
        if pools is not None
        else None,
        "attrs": attrs,
        "order": order.value,
        "sort": sort.value,
        "pn": pn,
        "ps": ps,
        "cp_filter": cp_filter,
    }

    api = API["danmaku-manager"]["search"]
    return await Api(**api, credential=credential).update_params(**params).result


async def del_danmaku(
    credential: Credential, oid: int, dmids: Union[int, List[int]]
) -> dict:
    """
    删除弹幕

    Args:
        oid (int): 稿件 oid

        dmids (list[int], int): 弹幕 id，可以传入列表和 int
    """

    return await edit_danmaku_state(credential=credential, oid=oid, dmids=dmids, state=1)


async def edit_danmaku_state(
    credential: Credential,
    oid: int,
    dmids: Union[int, List[int]],
    state: Optional[int] = None,
) -> dict:
    """
    操作弹幕状态

    Args:
        oid (int): 稿件 oid

        dmids (list[int], int): 弹幕 id，可以传入列表和 int

        state (int, Optional): 弹幕状态 1 删除 2 保护 3 取消保护

    Returns:
        dict: API 返回信息
    """
    data = {
        "type": 1,
        "oid": oid,
        "dmids": ",".join(dmids) if isinstance(dmids, list) else dmids,
        "state": state,
    }

    api = API["danmaku-manager"]["state"]
    return await Api(**api, credential=credential).update_data(**data).result


async def edit_danmaku_pool(
    credential: Credential,
    oid: int,
    dmids: Union[int, List[int]],
    is_subtitle: bool = True,
) -> dict:
    """
    操作弹幕池

    Args:
        oid (int): 稿件 oid

        dmids (list[int], int): 弹幕 id，可以传入列表和 int

        is_subtitle (bool): 是否为字幕

    Returns:
        dict: API 返回信息
    """
    data = {
        "type": 1,
        "oid": oid,
        "dmids": ",".join(dmids) if isinstance(dmids, list) else dmids,
        "pool": 1 if is_subtitle else 0,
    }

    api = API["danmaku-manager"]["pool"]
    return await Api(**api, credential=credential).update_data(**data).result
