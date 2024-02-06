"""
bilibili_api.comment

评论相关。

关于资源 ID（oid）的一些示例（{}部分为应该传入的参数）。

+ 视频：AV 号：av{170001}。
+ 专栏：cv{9762979}。
+ 动态（画册类型）：{116859542}。
+ 动态（纯文本）：{497080393649439253}。
+ 课程：ep{5556}
+ 小黑屋: ban/{2600321}
"""
from enum import Enum
from typing import Union, Optional

from .utils.utils import get_api
from .utils.credential import Credential
from .utils.network import Api
from .exceptions.ArgsException import ArgsException

API = get_api("common")


class CommentResourceType(Enum):
    """
    资源类型枚举。

    + VIDEO: 视频。
    + ARTICLE: 专栏。
    + DYNAMIC_DRAW: 画册。
    + DYNAMIC: 动态（画册也属于动态的一种，只不过画册还有一个专门的 ID）。
    + AUDIO：音频。
    + AUDIO_LIST：歌单。
    + CHEESE: 课程
    + BLACK_ROOM: 小黑屋
    + MANGA: 漫画
    """

    VIDEO = 1
    ARTICLE = 12
    DYNAMIC_DRAW = 11
    DYNAMIC = 17
    AUDIO = 14
    AUDIO_LIST = 19
    CHEESE = 33
    BLACK_ROOM = 6
    MANGA = 22


class OrderType(Enum):
    """
    评论排序方式枚举。

    + LIKE：按点赞数倒序。
    + TIME：按发布时间倒序。
    """

    LIKE = 2
    TIME = 0


class ReportReason(Enum):
    """
    举报类型枚举

    + OTHER: 其他
    + SPAM_AD: 垃圾广告
    + PORNOGRAPHY: 色情
    + FLOOD: 刷屏
    + PROVOCATION: 引战
    + SPOILER: 剧透
    + POLITICS: 政治
    + PERSONAL_ATTACK: 人身攻击
    + IRRELEVANT_CONTENT: 内容不相关
    + ILLEGAL: 违法违规
    + VULGAR: 低俗
    + ILLEGAL_WEBSITE: 非法网站
    + GAMBLING_FRAUD: 赌博诈骗
    + SPREADING_FALSE_INFORMATION: 传播不实信息
    + INCITING_INFORMATION: 怂恿教唆信息
    + PRIVACY_VIOLATION: 侵犯隐私
    + FLOOR_TAKING: 抢楼
    + INAPPROPRIATE_CONTENT_FOR_MINORS: 青少年不良信息
    """

    OTHER = 0
    SPAM_AD = 1
    PORNOGRAPHY = 2
    FLOOD = 3
    PROVOCATION = 4
    SPOILER = 5
    POLITICS = 6
    PERSONAL_ATTACK = 7
    IRRELEVANT_CONTENT = 8
    ILLEGAL = 9
    VULGAR = 10
    ILLEGAL_WEBSITE = 11
    GAMBLING_FRAUD = 12
    SPREADING_FALSE_INFORMATION = 13
    INCITING_INFORMATION = 14
    PRIVACY_VIOLATION = 15
    FLOOR_TAKING = 16
    INAPPROPRIATE_CONTENT_FOR_MINORS = 17


class Comment:
    """
    对单条评论的相关操作。

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(
        self,
        oid: int,
        type_: CommentResourceType,
        rpid: int,
        credential: Union[Credential, None] = None,
    ):
        """
        Args:
            oid        (int)         : 评论所在资源 ID。

            type_      (ResourceType): 评论所在资源类型枚举。

            rpid       (int)         : 评论 ID。

            credential (Credential)  : 凭据类. Defaults to None.
        """
        self.__oid = oid
        self.__rpid = rpid
        self.__type = type_
        self.credential = credential if credential else Credential()

    def __get_data(self, status: bool) -> dict:
        """
        获取通用请求载荷。

        Args:
            status (bool):  状态。

        Returns:
            dict: 请求载荷数据。
        """
        return {
            "oid": self.__oid,
            "type": self.__type.value,
            "rpid": self.__rpid,
            "action": 1 if status else 0,
        }

    def get_rpid(self) -> int:
        return self.__rpid

    def get_type(self) -> CommentResourceType:
        return self.__type

    def get_oid(self) -> int:
        return self.__oid

    async def like(self, status: bool = True) -> dict:
        """
        点赞评论。

        Args:
            status (bool, optional):  状态, Defaults to True.

        Returns:
            dict: 调用 API 返回的结果
        """

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["comment"]["like"]
        return (
            await Api(**api, credential=self.credential)
            .update_data(**self.__get_data(status))
            .result
        )

    async def hate(self, status: bool = True) -> dict:
        """
        点踩评论。

        Args:
            status (bool, optional):  状态, Defaults to True.

        Returns:
            dict: 调用 API 返回的结果
        """

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["comment"]["hate"]
        return (
            await Api(**api, credential=self.credential)
            .update_data(**self.__get_data(status))
            .result
        )

    async def pin(self, status: bool = True) -> dict:
        """
        置顶评论。

        Args:
            status (bool, optional):  状态, Defaults to True.

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["comment"]["pin"]
        return (
            await Api(**api, credential=self.credential)
            .update_data(**self.__get_data(status))
            .result
        )

    async def delete(self) -> dict:
        """
        删除评论。

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["comment"]["del"]
        data = self.__get_data(True)
        del data["action"]
        return await Api(**api, credential=self.credential).update_data(**data).result

    async def get_sub_comments(self, page_index: int = 1) -> dict:
        """
        获取子评论。即评论下的评论。

        Args:
            page_index (int, optional):  页码索引，从 1 开始。Defaults to 1.

        Returns:
            dict: 调用 API 返回的结果
        """
        if page_index <= 0:
            raise ArgsException("page_index 必须大于或等于 1")

        api = API["comment"]["sub_reply"]
        params = {
            "pn": page_index,
            "ps": 10,
            "type": self.__type.value,
            "oid": self.__oid,
            "root": self.__rpid,
        }

        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def report(
        self, report_reason: ReportReason, content: Optional[str] = None
    ) -> dict:
        """
        举报评论

        Args:
            report_reason (ReportReason): 举报类型枚举

            content (str, optional): 其他举报备注内容仅 reason=ReportReason.OTHER 可用且不能为 None.

        Error Code:
            0: 成功
            -101: 账号未登录
            -102: 账号被封停
            -111: csrf校验失败
            -400: 请求错误
            -403: 权限不足
            -404: 无此项
            -500: 服务器错误
            -509: 请求过于频繁
            12002: 评论区已关闭
            12006: 没有该评论
            12008: 已经举报过了
            12009: 评论主体的type不合法
            12019: 举报过于频繁
            12077: 举报理由过长或过短
        """

        self.credential.raise_for_no_sessdata()

        api = API["comment"]["report"]
        if content is not None and report_reason != ReportReason.OTHER:
            raise ArgsException("content 只能在 report_reason=ReportReason.OTHER 时使用")
        elif content is None and report_reason == ReportReason.OTHER:
            raise ArgsException("report_reason=ReportReason.OTHER 时 content 不能为空")
        data = {
            "oid": self.__oid,
            "type": self.__type.value,
            "rpid": self.__rpid,
            "reason": report_reason.value,
            "content": content,
        }
        return await Api(**api, credential=self.credential).update_data(**data).result


async def send_comment(
    text: str,
    oid: int,
    type_: CommentResourceType,
    root: Union[int, None] = None,
    parent: Union[int, None] = None,
    credential: Union[None, Credential] = None,
) -> dict:
    """
    通用发送评论 API。

    说明 `root` 和 `parent`，假设评论的是视频，常见的评论有三种情况：

    1. 只在视频下面发送评论：root=None, parent=None；
    2. 回复视频下面的评论：root=评论 ID, parent=None；
    3. 回复视频下面的评论中的评论：root=在哪条评论下评论的 ID, parent=回复哪条评论的 ID。

    当 root 为空时，parent 必须为空。

    Args:
        text       (str)          : 评论内容。

        oid        (str)          : 资源 ID。

        type_      (CommentsResourceType) : 资源类型枚举。

        root       (int, optional): 根评论 ID, Defaults to None.

        parent     (int, optional): 父评论 ID, Defaults to None.

        credential (Credential)   : 凭据

    Returns:
        dict: 调用 API 返回的结果
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    data = {
        "oid": oid,
        "type": type_.value,
        "message": text,
        "plat": 1,
    }

    if root is None and parent is None:
        # 直接回复资源
        pass
    elif root is not None and parent is None:
        # 回复资源下面的评论
        data["root"] = root
        data["parent"] = root
    elif root is not None and parent is not None:
        # 回复资源下面的评论的评论
        data["root"] = root
        data["parent"] = parent
    else:
        # root=None 时，parent 不得设置
        raise ArgsException("root=None 时，parent 不得设置")

    api = API["comment"]["send"]
    return await Api(**api, credential=credential).update_data(**data).result


async def get_comments(
    oid: int,
    type_: CommentResourceType,
    page_index: int = 1,
    order: OrderType = OrderType.TIME,
    credential: Union[Credential, None] = None,
) -> dict:
    """
    获取资源评论列表。

    第二页以及往后需要提供 `credential` 参数。

    Args:
        oid        (int)                 : 资源 ID。

        type_      (CommentsResourceType)        : 资源类枚举。

        page_index (int, optional)       : 页码. Defaults to 1.

        order      (OrderType, optional) : 排序方式枚举. Defaults to OrderType.TIME.

        credential (Credential, optional): 凭据。Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    if page_index <= 0:
        raise ArgsException("page_index 必须大于或等于 1")

    api = API["comment"]["get"]
    params = {"pn": page_index, "type": type_.value, "oid": oid, "sort": order.value}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_comments_lazy(
    oid: int,
    type_: CommentResourceType,
    # pagination_str: str = "",
    pn: int = 1,
    ps: int = 20,
    order: OrderType = OrderType.TIME,
    credential: Union[Credential, None] = None,
) -> dict:
    """
    新版获取资源评论列表。

    第二次以及往后需要提供 `credential` 参数。

    Args:
        oid        (int)                 : 资源 ID。

        type_      (CommentsResourceType)        : 资源类枚举。

        pagination_str (str, optional)       : 分页依据 Defaults to `{"offset":""}`. 弃用 #658

        pn (int, optional)       : 页码. Defaults to 1.

        ps (int, optional)       : 每页数量. Defaults to 20.

        order      (OrderType, optional) : 排序方式枚举. Defaults to OrderType.TIME.

        credential (Credential, optional): 凭据。Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["comment"]["reply_by_session_id"]
    params = {
        "oid": oid,
        "type": type_.value,
        "mode": order.value,
        "next": pn - 1,
        "ps": ps,
    }
    return await Api(**api, credential=credential).update_params(**params).result
