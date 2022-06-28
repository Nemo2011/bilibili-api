"""
bilibili_api.comment

评论相关。

关于资源 ID（oid）的一些示例（{}部分为应该传入的参数）。

+ 视频：AV 号：av{170001}。
+ 专栏：cv{9762979}。
+ 动态（画册类型）：{116859542}。
+ 动态（纯文本）：{497080393649439253}。
"""
from enum import Enum

from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.Credential import Credential
from .exceptions.ArgsException import ArgsException


API = get_api("common")


class ResourceType(Enum):
    """
    资源类型枚举。

    + VIDEO: 视频。
    + ARTICLE: 专栏。
    + DYNAMIC_DRAW: 画册。
    + DYNAMIC: 动态（画册也属于动态的一种，只不过画册还有一个专门的 ID）。
    + AUDIO：音频。
    + AUDIO_LIST：歌单。
    """

    VIDEO = 1
    ARTICLE = 12
    DYNAMIC_DRAW = 11
    DYNAMIC = 17
    AUDIO = 14
    AUDIO_LIST = 19


class OrderType(Enum):
    """
    评论排序方式枚举。

    + LIKE：按点赞数倒序。
    + TIME：按发布时间倒序。
    """

    LIKE = 2
    TIME = 0


class Comment:
    """
    对单条评论的相关操作。
    """

    def __init__(
        self, oid: int, type_: ResourceType, rpid: int, credential: Credential
    ):
        """
        Args:
            oid        (int)         : 评论所在资源 ID。
            type_      (ResourceType): 评论所在资源类型枚举。
            rpid       (int)         : 评论 ID。
            credential (Credential)  : Credential 类。
        """
        self.oid = oid
        self.rpid = rpid
        self.type_ = type_
        self.credential = credential

    def __get_data(self, status: bool):
        """
        获取通用请求载荷。

        Args:
            status (bool):  状态。

        Returns:
            dict: 请求载荷数据。
        """
        return {
            "oid": self.oid,
            "type": self.type_.value,
            "rpid": self.rpid,
            "action": 1 if status else 0,
        }

    async def like(self, status: bool = True):
        """
        点赞评论。

        Args:
            status (bool, optional):  状态, Defaults to True.

        Returns:
            dict: 调用接口返回的内容。
        """

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["comment"]["like"]
        return await request(
            "POST", api["url"], data=self.__get_data(status), credential=self.credential
        )

    async def hate(self, status: bool = True):
        """
        点踩评论。

        Args:
            status (bool, optional):  状态, Defaults to True.

        Returns:
            dict: 调用接口返回的内容。
        """

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["comment"]["hate"]
        return await request(
            "POST", api["url"], data=self.__get_data(status), credential=self.credential
        )

    async def pin(self, status: bool = True):
        """
        置顶评论。

        Args:
            status (bool, optional):  状态, Defaults to True.

        Returns:
            dict: 调用接口返回的内容。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["comment"]["pin"]
        return await request(
            "POST", api["url"], data=self.__get_data(status), credential=self.credential
        )

    async def delete(self):
        """
        删除评论。

        Returns:
            dict: 调用接口返回的内容。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["comment"]["del"]
        data = self.__get_data(True)
        del data["action"]
        return await request("POST", api["url"], data=data, credential=self.credential)

    async def get_sub_comments(self, page_index: int = 1):
        """
        获取子评论。即评论下的评论。

        Args:
            page_index (int, optional):  页码索引，从 1 开始。Defaults to 1.

        Returns:
            dict: 调用接口返回的内容。
        """
        if page_index <= 0:
            raise ArgsException("page_index 必须大于或等于 1")

        api = API["comment"]["sub_reply"]
        params = {
            "pn": page_index,
            "ps": 10,
            "type": self.type_.value,
            "oid": self.oid,
            "root": self.rpid,
        }

        return await request(
            "GET", api["url"], params=params, credential=self.credential
        )


async def send_comment(
    text: str,
    oid: int,
    type_: ResourceType,
    root: int = None,
    parent: int = None,
    credential: Credential = None,
):
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
        type_      (ResourceType) : 资源类型枚举。
        root       (int, optional): 根评论 ID, Defaults to None.
        parent     (int, optional): 父评论 ID, Defaults to None.
        credential (Credential)   : 凭据
    Returns:
        dict: 调用接口返回的内容。
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
    return await request("POST", api["url"], data=data, credential=credential)


async def get_comments(
    oid: int,
    type_: ResourceType,
    page_index: int = 1,
    order: OrderType = OrderType.TIME,
    credential: Credential = None,
):
    """
    获取资源评论列表。

    Args:
        oid        (int)                 : 资源 ID。
        type_      (ResourceType)        : 资源类枚举。
        page_index (int, optional)       : 页码. Defaults to 1.
        order      (OrderType, optional) : 排序方式枚举. Defaults to OrderType.TIME.
        credential (Credential, optional): 凭据。Defaults to None.

    Returns:
        dict: 调用接口返回的内容。
    """
    if page_index <= 0:
        raise ArgsException("page_index 必须大于或等于 1")

    api = API["comment"]["get"]
    params = {"pn": page_index, "type": type_.value, "oid": oid, "sort": order.value}
    return await request("GET", api["url"], params=params, credential=credential)
