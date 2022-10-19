"""
bilibili_api.black_room

小黑屋
"""

from enum import Enum

from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.Credential import Credential

# 违规类型代码
BLACK_TYPE = {
    0: "全部",
    1: "刷屏",
    2: "抢楼",
    3: "发布色情低俗信息",
    4: "发布赌博诈骗信息",
    5: "发布违禁相关信息",
    6: "发布垃圾广告信息",
    7: "发布人身攻击言论",
    8: "发布侵犯他人隐私信息",
    9: "发布引战言论",
    10: "发布剧透信息",
    11: "恶意添加无关标签",
    12: "恶意删除他人标签",
    13: "发布色情信息",
    14: "发布低俗信息",
    15: "发布暴力血腥信息",
    16: "涉及恶意投稿行为",
    17: "发布非法网站信息",
    18: "发布传播不实信息",
    19: "发布怂恿教唆信息",
    20: "恶意刷屏",
    21: "账号违规",
    22: "恶意抄袭",
    23: "冒充自制原创",
    24: "发布青少年不良内容",
    25: "破坏网络安全",
    26: "发布虚假误导信息",
    27: "仿冒官方认证账号",
    28: "发布不适宜内容",
    29: "违反运营规则",
    30: "恶意创建话题",
    31: "发布违规抽奖",
    32: "恶意冒充他人",
}


class BlackFrom(Enum):
    """
    违规来源

    SYSTEM: 系统封禁
    ADMIN: 风纪仲裁
    ALL: 全部
    """

    SYSTEM = 0
    ADMIN = 1
    ALL = None


API = get_api("black-room")


async def get_blocked_list(
    from_: BlackFrom = BlackFrom.ALL,
    type_: int = 0,
    pn: int = 1,
    credential: Credential = None,
):
    """
    获取小黑屋中的违规列表

    Args:
        from_(BlackFrom)      : 违规来源. Defaults to BlackFrom.ALL
        type_(int)            : 违规类型. 查看 black_room.BLACK_TYPE。Defaults to 0 (ALL)
        pn(int)               : 页数. Defaults to 1
        credential(Credential): 凭据, Defaults to None
    """
    credential = credential if credential else Credential()
    api = API["info"]
    params = {"pn": pn, "otype": type_}
    if from_.value != None:
        params["btype"] = from_.value
    return await request("GET", api["url"], params=params, credential=credential)


class BlackRoom:
    """
    小黑屋
    """
    def __init__(self, black_room_id: int, credential: Credential = None):
        """
        Args:
            black_room_id(int)    : 小黑屋 id
            credential(Credential): 凭据类
        """
        self.__id = black_room_id
        self.credential = credential if credential else Credential()

    async def get_details(self):
        """
        获取小黑屋详细信息
        """
        api = API["detail"]
        params = {"id": self.__id}
        return await request(
            "GET", api["url"], params=params, credential=self.credential
        )

    async def get_id(self):
        """
        获取小黑屋 id
        """
        return self.__id
