"""
bilibili_api.black_room

小黑屋
"""

from enum import Enum
from typing import List, Union, Optional

from .utils.utils import get_api
from .utils.credential import Credential
from .utils.network_httpx import Api


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


class JuryVoteOpinion(Enum):
    """
    仲裁投票类型枚举，选择对应案件类型的观点

    单条评论（弹幕）
    - SUITABLE: 合适
    - AVERAGE: 一般
    - UNSUITABLE: 不合适
    - UNKNOW: 无法判断

    评论（弹幕）氛围
    - ENV_GREAT: 评论环境好
    - ENV_AVERAGE: 评论环境一般
    - ENV_BAD: 评论环境差
    - ENV_UNKNOW: 无法判断评论环境
    """

    SUITABLE = 1
    AVERAGE = 2
    UNSUITABLE = 3
    UNKNOW = 4
    ENV_GREAT = 11
    ENV_AVERAGE = 12
    ENV_BAD = 13
    ENV_UNKNOW = 14


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
    api = API["black_room"]["info"]
    params = {"pn": pn, "otype": type_.value}
    if from_.value != None:
        params["btype"] = from_.value
    return await Api(**api, credential=credential).update_params(**params).result


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
        api = API["black_room"]["detail"]
        params = {"id": self.__id}
        return await Api(**api, credential=self.credential).update_params(**params).result

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


class JuryCase:
    def __init__(self, case_id: str, credential: Credential):
        """
        Args:
            case_id (str)                              : 案件 id

            credential (Credential)                    : 凭据类
        """
        self.case_id = case_id
        self.credential = credential

    async def get_details(self) -> dict:
        """
        获取案件详细信息

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["jury"]["detail"]
        params = {"case_id": self.case_id}
        return await Api(**api, credential=self.credential).update_params(**params).result

    async def get_opinions(self, pn: int = 1, ps: int = 20) -> dict:
        """
        获取案件的观点列表

        Args:
            pn (int, optional): 页数. Defaults to 1.

            ps (int, optional): 每页数量. Defaults to 20.

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["jury"]["opinion"]
        params = {"case_id": self.case_id, "pn": pn, "ps": ps}
        return await Api(**api, credential=self.credential).update_params(**params).result

    async def vote(
        self,
        opinion: JuryVoteOpinion,
        is_insider: bool,
        is_anonymous: bool,
        reason: Optional[str] = None,
    ) -> dict:
        """
        进行仲裁投票

        Args:
            opinion (JuryVoteOpinion): 投票选项类型

            is_insider (bool): 是否观看此类视频

            is_anonymous (bool): 是否匿名投票

            reason (str, optional): 投票理由. Defaults to None.

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["jury"]["vote"]
        data = {
            "case_id": self.case_id,
            "vote": opinion.value,
            "insiders": 1 if is_insider else 0,
            "anonymous": 1 if is_anonymous else 0,
            "csrf": self.credential.bili_jct,
        }
        if reason:
            data["content"] = reason
        return await Api(**api, credential=self.credential).update_data(**data).result


async def get_next_jury_case(credential: Credential) -> JuryCase:
    """
    获取下一个待审理的案件

    Args:
        credential (Credential | None, optional): 凭据类. Defaults to None.

    Returns:
        JuryCase: 案件类
    """
    credential.raise_for_no_sessdata()
    api = API["jury"]["next_case"]
    return JuryCase(
        (await Api(**api, credential=credential).result)["case_id"], credential
    )


async def get_jury_case_list(
    credential: Credential, pn: int = 1, ps: int = 20
) -> List[JuryCase]:
    """
    获取仲裁案件列表

    Args:
        credential (Credential): 凭据类

        pn (int, optional): 页数. Defaults to 1.

        ps (int, optional): 每页数量. Defaults to 20.

    Returns:
        List[JuryCase]: 仲裁案件列表
    """
    api = API["jury"]["case_list"]
    params = {"pn": pn, "ps": ps}
    info = await Api(**api, credential=credential).update_params(**params).result
    return [JuryCase(case["case_id"], credential) for case in info["list"]]
