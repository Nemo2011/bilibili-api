"""
bilibili_api.watchroom

放映室相关 API

注意，此类操作务必传入 `Credential` 并且要求传入 `buvid3` 否则可能无法鉴权
"""
import time
from enum import Enum
from typing import List, Union
from .utils.network_httpx import Api
from .utils.utils import get_api
from .credential import Credential

API = get_api("watchroom")


class SeasonType(Enum):
    """
    季度类型

    + ANIME: 番剧
    + MOVIE: 电影
    + DOCUMENTARY: 纪录片
    + GUOCHUANG: 国创
    + TV: 电视剧
    + VARIETY: 综艺
    """

    ANIME = 1
    MOVIE = 2
    DOCUMENTARY = 3
    GUOCHUANG = 4
    TV = 5
    VARIETY = 7
class MessageType(Enum):
    PLAIN = "plain"
    EMOJI = "emoji"


class MessageSegment:
    """
    Example:
        MessageSegment("doge", true) + MessageSegment("2023")
    """
    msg: str
    msg_type: MessageType

    def __init__(self, msg: str, is_emoji: bool = False):
        self.msg, self.msg_type = msg, MessageType.EMOJI if is_emoji else MessageType.PLAIN

    def convert(self) -> str:
        if self.msg_type == MessageType.EMOJI:
            return f"[{self.msg}]"
        return self.msg


class Message:
    msg_list: List[MessageSegment] = []

    def to_msg_segment(self, msg: Union[MessageSegment, str]) -> MessageSegment:
        return MessageSegment(msg) if isinstance(msg, str) else msg

    def __init__(self, *messages: List[Union[MessageSegment, str]]):
        for msg in messages:
            self.msg_list.append(self.to_msg_segment(msg))

    def __add__(self, msg: Union[MessageSegment, "Message"]):
        if isinstance(msg, MessageSegment):
            self.msg_list.append(self.to_msg_segment(msg))
        elif self.__class__ is msg:
            self.msg_list.extend(msg.msg_list)
        return self

    def __str__(self) -> str:
        return "".join([msg.convert() for msg in self.msg_list])

    def __repr__(self) -> str:
        return self.msg_list


class WatchRoom:
    """
    放映室类
    """

    season_id: int
    episode_id: int

    def __init__(self, room_id: int, credential: Credential):
        """
        Agrs:

            credential      (Credential): 凭据类

            room_id (int)       : 放映室 id
        """
        self.room_id: int = room_id
        self.credential: Credential = credential
        self.credential.raise_for_no_buvid3()  # 大部分用户操作都需要与之匹配的 buvid3 值，务必在 credential 传入

    def set_season_id(self, season_id: int):
        self.season_id = season_id

    def set_episode_id(self, episode_id: int):
        self.episode_id = episode_id

    async def get_info(self) -> dict:
        """
        获取放映室信息，播放进度等

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["info"]
        params = {"room_id": self.room_id, "platform": "web"}
        return (
            await Api(credential=self.credential, **api).update_params(**params).result
        )

    async def open(self) -> None:
        """
        开放放映室
        """
        api = API["operate"]["open"]
        data = {
            "room_id": self.room_id,
            "is_open": 1,
            "csrf": self.credential.bili_jct,
            "platform": "web",
        }
        return (
            await Api(credential=self.credential, no_csrf=True, **api)
            .update_data(**data)
            .result
        )

    async def close(self) -> None:
        """
        关闭放映室
        """
        api = API["operate"]["open"]
        data = {
            "room_id": self.room_id,
            "is_open": 0,
            "csrf": self.credential.bili_jct,
            "platform": "web",
        }
        return (
            await Api(credential=self.credential, no_csrf=True, **api)
            .update_data(**data)
            .result
        )

    async def progress(self, progress: int = None, status: int = 1) -> None:
        """
        设置播放状态，包括暂停与进度条

        Args:

            progress (int, None) 进度，单位为秒

            status (bool, None) 播放状态 1 播放中 0 暂停中 2 已结束
        """
        api = API["operate"]["progress"]
        data = {
            "room_id": self.room_id,
            "progress": progress,
            "status": status if status in [1, 2, 0] else 1,
            "csrf": self.credential.bili_jct,
            "platform": "web",
        }
        return (
            await Api(credential=self.credential, no_csrf=True, **api)
            .update_data(**data)
            .result
        )

    async def join(self, token: str = None) -> dict:
        """
        加入放映室

        Args:
            
            token (str, Optional) 邀请 Token

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["operate"]["join"]
        data = {
            "room_id": self.room_id,
            "token": token,
            "csrf": self.credential.bili_jct,
            "platform": "web",
        }
        res = (
            await Api(credential=self.credential, no_csrf=True, **api)
            .update_data(**data)
            .result
        )
        self.set_season_id(res["season_id"])
        self.set_episode_id(res["episode_id"])
        return res

    async def send(self, msg: Message) -> dict:
        """
        发送消息

        Args:

            msg (Message) 消息

        Returns:
            dict: 调用 API 返回的结果
        """
        data = {
            "room_id": self.room_id,
            "content_type": 0,
            "content": '{"text":"msg"}'.replace("msg", str(msg)),
            "req_id": int(time.time()) * 1000,
            "platform": "web",
            "csrf": self.credential.bili_jct,
        }
        api = API["operate"]["send"]
        return (
            await Api(credential=self.credential, no_csrf=True, **api)
            .update_data(**data)
            .result
        )

    async def kickout(self, uid: int) -> dict:
        """
        踢出放映室

        Args:

            uid (int) 用户 uid

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["operate"]["kickout"]
        data = {
            "room_id": self.room_id,
            "mid": uid,
            "csrf": self.credential.bili_jct,
            "platform": "web",
        }
        return (
            await Api(credential=self.credential, no_csrf=True, **api)
            .update_data(**data)
            .result
        )
    
    async def share(self) -> str:
        """
        获取邀请 Token

        Returns:
            str: 邀请 Token
        """
        api = API["info"]["season"]
        params = {
            "room_id": self.room_id,
            "season_id": self.season_id,
            "ep_id": self.episode_id,
            "csrf": self.credential.bili_jct,
            "platform": "web",
        }
        res =  (
            await Api(credential=self.credential, no_csrf=True, **api)
            .update_params(**params)
            .result
        )
        return res["room_info"]["share_url"].split("&token=")[-1]
    
async def create(season_id: int, episode_id: int, is_open: bool = False, credential: Credential = Credential()) -> WatchRoom:
    """
    创建放映室

    Args:

        season_id (int) 每季度的 ID

        ep_id (int) 剧集 ID

        is_open (bool) 是否公开

        credential (Credential) 凭据

    Returns:
        Watchroom
    """
    api = API["operate"]["create"]
    data = {
        "season_id": season_id,
        "episode_id": episode_id,
        "is_open": 1 if is_open else 0,
        "csrf": credential.bili_jct,
        "platform": "web",
    }
    return WatchRoom(
        (await Api(credential=credential, no_csrf=True, **api)
        .update_data(**data)
        .result)["room_id"], credential=credential
    )


async def match(season_id: int, season_type: SeasonType = SeasonType.ANIME, credential: Credential = Credential()) -> WatchRoom:
    """
    匹配放映室

    Args:

        season_id (int) 季度 ID

        season_type (str) 季度类型
    """
    api = API["operate"]["match"]
    data = {
        "season_id": season_id,
        "season_type": season_type.value,
        "csrf": credential.bili_jct,
        "platform": "web",
    }
    return WatchRoom(
        (await Api(credential=credential, no_csrf=True, **api)
        .update_data(**data)
        .result)["room_id"], credential=credential
    )