"""
bilibili_api.black_room

小黑屋
"""

from enum import Enum
from typing import Union

from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.Credential import Credential


class BlackReasonType(Enum):
    """
    违规原因类型枚举 (英语翻译错误请忽略/提 issue/发起 PR)

    - ALL: 全部
    - FLOOD_SCREEN: 刷屏
    - SOFA: 抢沙发
    - PRON_VULGAR: 色情低俗内容
    - GAMBLED_SCAMS: 赌博诈骗内容
    - ILLEGAL: 违禁信息
    - ADS: 垃圾广告信息
    - PERSONAL_ATTACK: 人身攻击
    - INVASION_OF_PRIVACY: 侵犯隐私
    - LEAD_WAR: 引战
    - SPOILER: 剧透
    - ADD_MALICIOUS_TAG: 恶意为他人添加标签
    - DEL_OTHERS_TAG: 恶意删除他人标签
    - PRON: 色情
    - VULGAR: 低俗
    - VIOLENT: 暴力血腥内容
    - MALICIOUS_ARCHIVES: 恶意投稿行为
    - ILLEGAL_STATION: 发布非法网站信息
    - SEND_UNREAL_EVENT: 发布不实信息
    - ABETMENT: 发布教唆怂恿信息
    - MALICIOUS_SPAMMING: 恶意刷屏
    - ILLEGAL_ACCOUNT: 账号违规
    - PLAGIARISM: 抄袭
    - PRETEND_ORIGINAL: 冒充官号
    - BAD_FOR_YOUNGS: 青少年不宜
    - BREAK_INTERNET_SECURITY: 破坏网络安全
    - SEND_UNREAL_MISLEADING_EVENT: 发布不实舞蹈信息
    - VIOLATE_SITE_OPERATING_RULES: 违规网站运营规则
    - MALICIOUS_TOPICS: 恶意创建话题
    - CREATE_ILLEGAL_LUCKY_DRAW: 发布违规抽奖
    - PRETEND_OTHER: 冒充他人
    """
    ALL = 0
    FLOOD_SCREEN = 1
    SOFA = 2
    PRON_VULGAR = 3
    GAMBLED_SCAMS = 4
    ILLEGAL = 5
    ADS = 6
    PERSONAL_ATTACK = 7
    INVASION_OF_PRIVACY = 8
    LEAD_WAR = 9
    SPOILER = 10
    ADD_MALICIOUS_TAG = 11
    DEL_OTHERS_TAG = 12
    PRON = 13
    VULGAR = 14
    VIOLENT = 15
    MALICIOUS_ARCHIVES = 16
    ILLEGAL_STATION = 17
    SEND_UNREAL_EVENT = 18
    ABETMENT = 19
    MALICIOUS_SPAMMING = 20
    ILLEGAL_ACCOUNT = 21
    PLAGIARISM = 22
    PRETEND_ORIGINAL = 23
    BAD_FOR_YOUNGS = 24
    BREAK_INTERNET_SECURITY = 25
    SEND_UNREAL_MISLEADING_EVENT = 26
    PRETEND_ORIGINAL_ACCOUNT = 27
    SEND_BAD_EVENT = 28
    VIOLATE_SITE_OPERATING_RULES = 29
    MALICIOUS_TOPICS = 30
    CREATE_ILLEGAL_LUCKY_DRAW = 31
    PRETEND_OTHER = 32


class BlackType(Enum):
    """
    违规类型枚举

    - ALL: 全部
    - COMMENT: 评论
    - DANMAKU: 弹幕
    - PRIVATE_MESSAGE: 私信
    - TAG: 标签
    - PERSONAL_INFORMATION: 个人信息
    - VIDEO: 视频
    - ARTICLE: 专栏
    - DYNAMIC: 动态
    - ALBUM: 相簿
    """
    ALL = 0
    COMMENT = 1
    DANMAKU = 2
    PRIVATE_MESSAGE = 3
    TAG = 4
    PERSONAL_INFORMATION = 5
    VIDEO = 6
    ARTICLE = 8
    DYNAMIC = 10
    ALBUM = 11


class BlackFrom(Enum):
    """
    违规来源

    - SYSTEM: 系统封禁
    - ADMIN: 风纪仲裁
    - ALL: 全部
    """

    SYSTEM = 0
    ADMIN = 1
    ALL = None


API = get_api("black-room")


async def get_blocked_list(
    from_: BlackFrom = BlackFrom.ALL,
    type_: BlackType = BlackType.ALL,
    pn: int = 1,
    credential: Union[Credential, None] = None,
) -> dict:
    """
    获取小黑屋中的违规列表

    Args:
        from_      (BlackFrom)        : 违规来源. Defaults to BlackFrom.ALL.
        type_      (int)              : 违规类型. Defaults to BlackType.ALL. 
        pn         (int)              : 页数. Defaults to 1.
        credential (Credential | None): 凭据. Defaults to None.
    """
    credential = credential if credential else Credential()
    api = API["info"]
    params = {"pn": pn, "otype": type_.value}
    if from_.value != None:
        params["btype"] = from_.value
    return await request("GET", api["url"], params=params, credential=credential)


class BlackRoom:
    """
    小黑屋

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(self, black_room_id: int, credential: Union[Credential, None] = None):
        """
        Args:
            black_room_id (int)                        : 小黑屋 id
            credential    (Credential | None, optional): 凭据类. Defaults to None.
        """
        self.__id = black_room_id
        self.credential = credential if credential else Credential()

    async def get_details(self) -> dict:
        """
        获取小黑屋详细信息

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["detail"]
        params = {"id": self.__id}
        return await request(
            "GET", api["url"], params=params, credential=self.credential
        )

    async def get_reason(self) -> BlackReasonType:
        """
        获取小黑屋的封禁原因

        Returns:
            BlackReasonType: 封禁原因枚举类
        """
        return BlackReasonType((await self.get_details())["reasonType"])

    async def get_id(self) -> int:
        return self.__id

    async def set_id(self, id_) -> None:
        self.__init__(id_, self.credential)
