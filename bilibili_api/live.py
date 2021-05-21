r"""
bilibili_api.live

直播相关
"""
import time
from enum import Enum

from .utils.Credential import Credential
from .utils.network import request
from .utils.utils import get_api
from .utils.Danmaku import Danmaku

API = get_api("live")


class ScreenResolution(Enum):
    """
    直播源清晰度。

    清晰度编号，4K 20000，原画 10000，蓝光（杜比）401，蓝光 400，超清 250，高清 150，流畅 80
    + FOUR_K        : 4K。
    + ORIGINAL      : 原画。
    + BLU_RAY_DOLBY : 蓝光（杜比）。
    + BLU_RAY       : 蓝光。
    + ULTRA_HD      : 超清。
    + HD            : 高清。
    + FLUENCY       : 流畅。
    """
    FOUR_K = 20000
    ORIGINAL = 10000
    BLU_RAY_DOLBY = 401
    BLU_RAY = 400
    ULTRA_HD = 250
    HD = 150
    FLUENCY = 80


class LiveProtocol(Enum):
    """
    直播源流协议。

    流协议，0 为 FLV 流，1 为 HLS 流。默认：0,1
    + FLV     : 0。
    + HLS     : 1。
    + DEFAULT : 0,1
    """
    FLV = 0
    HLS = 1
    DEFAULT = '0,1'


class LiveFormat(Enum):
    """
    直播源容器格式

    容器格式，0 为 flv 格式；1 为 ts 格式（仅限 hls 流）；2 为 fmp4 格式（仅限 hls 流）。默认：0,2
    + FLV       : 0。
    + TS        : 1。
    + FMP4      : 2。
    + DEFAULT   : 2。
    """
    FLV = 0
    TS = 1
    FMP4 = 2
    DEFAULT = '0,1,2'


class LiveCodec(Enum):
    """
    直播源视频编码

    视频编码，0 为 avc 编码，1 为 hevc 编码。默认：0,1
    + AVC       : 0。
    + HEVC      : 1。
    + DEFAULT   : 0,1。
    """
    AVC = 0
    HEVC = 1
    DEFAULT = '0,1'


def check_uid(func):
    """
    检查 uid 参数
    """

    async def wrapper(self, *args, **kwargs):
        if not self._Live__uid:
            await self.get_room_play_info()
        return await func(self, *args, **kwargs)

    return wrapper


class LiveRoom:
    """
    直播类，获取各种直播间的操作均在里边。
    """

    def __init__(self, room_display_id: int = None, credential: Credential = None):
        self.room_display_id = room_display_id

        if credential is None:
            self.credential = Credential()
        else:
            self.credential = credential

        self.__ruid = None

    async def get_room_play_info(self):
        """
        获取房间信息（真实房间号，封禁情况等）

        :return: resp
        """
        api = API["info"]["room_play_info"]
        params = {
            "room_id": self.room_display_id,
        }
        resp = await request(api['method'], api['url'], params=params, credential=self.credential)
        self.__ruid = resp['uid']
        return resp

    async def __get_ruid(self):
        if self.__ruid is None:
            await self.get_room_play_info()

        return self.__ruid

    async def get_chat_conf(self):
        """
        获取聊天弹幕服务器配置信息(websocket)
        """
        api = API["info"]["chat_conf"]
        params = {
            "room_id": self.room_display_id
        }
        return await request(api['method'], api["url"], params, credential=self.credential)

    async def get_room_info(self):
        """
        获取直播间信息（标题，简介等）
        """
        api = API["info"]["room_info"]
        params = {
            "room_id": self.room_display_id
        }
        return await request(api['method'], api["url"], params, credential=self.credential)


    async def get_user_info_in_room(self):
        """
        获取自己在直播间的信息（粉丝勋章等级，直播用户等级等）
        """
        self.credential.raise_for_no_sessdata()

        api = API["info"]["user_info_in_room"]
        params = {
            "room_id": self.room_display_id
        }
        return await request(api['method'], api["url"], params, credential=self.credential)

    async def get_self_info(self):
        """
        获取自己直播等级、排行等信息
        """
        self.credential.raise_for_no_sessdata()

        api = API["info"]["user_info"]
        return await request(api['method'], api["url"], credential=self.credential)

    async def get_dahanghai(self, page: int = 1):
        """
        获取大航海列表

        Args:
            page (int, optional): 页码. Defaults to 1
        """
        api = API["info"]["dahanghai"]
        params = {
            "roomid": self.room_display_id,
            "ruid": await self.__get_ruid(),
            "page_size": 30,
            "page": page
        }
        return await request(api['method'], api["url"], params, credential=self.credential)


    async def get_seven_rank(self):
        """
        获取七日榜
        """
        api = API["info"]["seven_rank"]
        params = {
            "roomid": self.room_display_id,
            "ruid": await self.__get_ruid(),
        }
        return await request(api['method'], api["url"], params, credential=self.credential)

    async def get_fans_medal_rank(self):
        """
        获取粉丝勋章排行
        """
        api = API["info"]["fans_medal_rank"]
        params = {
            "roomid": self.room_display_id,
            "ruid": await self.__get_ruid()
        }
        return await request(api['method'], api["url"], params, credential=self.credential)

    async def get_black_list(self, page: int = 1):
        """
        获取黑名单列表

        Args:
            page (int, optional): 页码. Defaults to 1
        """
        api = API["info"]["black_list"]
        params = {
            "roomid": self.room_display_id,
            "page": page
        }

        return await request(api['method'], api["url"], params, credential=self.credential)

    async def get_room_play_url(self, screen_resolution: ScreenResolution = ScreenResolution.ORIGINAL):
        """
        获取房间直播流列表

        Args:
            screen_resolution (ScreenResolution, optional): 清晰度. Defaults to ScreenResolution.ORIGINAL
        """
        api = API["info"]["room_play_url"]
        params = {
            "cid": self.room_display_id,
            "platform": "web",
            "qn": screen_resolution.value,
            "https_url_req": "1",
            "ptype": "16"
        }
        return await request(api['method'], api["url"], params, credential=self.credential)

    async def get_room_play_info_v2(self, live_protocol: LiveProtocol = LiveProtocol.DEFAULT,
                                    live_format: LiveFormat = LiveFormat.DEFAULT,
                                    live_codec: LiveCodec = LiveCodec.DEFAULT,
                                    live_qn: ScreenResolution = ScreenResolution.ORIGINAL):
        """
        获取房间信息及可用清晰度列表
        """
        api = API["info"]["room_play_info_v2"]
        params = {
            "room_id": self.room_display_id,
            "platform": "web",
            "ptype": "16",
            "protocol": live_protocol.value,
            "format": live_format.value,
            "codec": live_codec.value,
            "qn": live_qn.value
        }
        return await request(api['method'], api['url'], params=params, credential=self.credential)


    async def ban_user(self, uid: int, hour: int = 1):
        """
        封禁用户

        Args:
            uid (int): 用户 UID
            hour (int): 封禁时长. Defaults to 1
        """
        self.credential.raise_for_no_sessdata()

        api = API["operate"]["add_block"]
        data = {
            "roomid": self.room_display_id,
            "block_uid": uid,
            "hour": hour,
            "visit_id": ""
        }
        return await request(api['method'], api["url"], data=data, credential=self.credential)


    async def unban_user(self, block_id: int):
        """
        解封用户

        Args:
            block_id (int): 封禁用户时会返回该封禁的 ID，使用该值
        """
        self.credential.raise_for_no_sessdata()
        api = API["operate"]["del_block"]
        data = {
            "roomid": self.room_display_id,
            "id": block_id,
            "visit_id": "",
        }
        return await request(api['method'], api["url"], data=data, credential=self.credential)

    async def send_danmaku(self, danmaku: Danmaku):
        """
        直播间发送弹幕

        Args:
            danmaku (Danmaku): 弹幕类
        """
        self.credential.raise_for_no_sessdata()

        api = API["operate"]["send_danmaku"]
        data = {
            "mode": danmaku.mode.value,
            "msg": danmaku.text,
            "roomid": self.room_display_id,
            "bubble": 0,
            "rnd": int(time.time()),
            "color": danmaku.color.get_dec_color(),
            "fontsize": danmaku.font_size.value
        }
        return await request(api['method'], api["url"], data=data, credential=self.credential)

