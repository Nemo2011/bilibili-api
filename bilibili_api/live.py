r"""
模块：live
功能：直播间各种信息和操作
项目GitHub地址：https://github.com/Passkou/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""
import time
from enum import Enum

from .exceptions import ArgsException, CredentialNoSessdataException, CredentialNoBiliJctException
from .utils.Credential import Credential
from .utils.network import request
from .utils.utils import get_api
from .utils.Danmaku import Danmaku

API = get_api("live")


class LiveClarity(Enum):
    """
    直播源清晰度。
    清晰度编号，4K20000，原画10000，蓝光（杜比）401，蓝光400，超清250，高清150，流畅80
    + four_K        : 4K。
    + Original      : 原画。
    + Blu_ray_Dolby : 蓝光（杜比）。
    + Blu_ray       : 蓝光。
    + Ultra_HD      : 超清。
    + HD            : 高清。
    + Fluency       : 流畅。
    """
    four_K = 20000
    Original = 10000
    Blu_ray_Dolby = 401
    Blu_ray = 400
    Ultra_HD = 250
    HD = 150
    Fluency = 80


class LiveProtocol(Enum):
    """
    直播源流协议。
    流协议，0为FLV流，1为HLS流。默认：0,1
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
    容器格式，0为flv格式；1为ts格式（仅限hls流）；2为fmp4格式（仅限hls流）。默认：0,2
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
    视频编码，0为avc编码，1为hevc编码。默认：0,1
    + AVC       : 0。
    + HEVC      : 1。
    + DEFAULT   : 0,1。
    """
    AVC = 0
    HEVC = 1
    DEFAULT = '0,1'


def check_user(proof_listing: list):
    """
    检查 cookie 参数
    """

    def middle(func):
        def wrapper(self, *args, **kwargs):
            for proof in proof_listing:
                if not eval(f"self.credential.{proof}"):
                    raise {'sessdata': CredentialNoSessdataException, 'bili_jct': CredentialNoBiliJctException}.get(
                        proof)()
            else:
                return func(self, *args, **kwargs)

        return wrapper

    return middle


def check_uid(func):
    """
    检查 uid 参数
    """

    async def wrapper(self, *args, **kwargs):
        if not self._Live__uid:
            await self.get_room_play_info()
        return await func(self, *args, **kwargs)

    return wrapper


class Live(object):
    """
    直播类，获取各种直播间的操作均在里边。
    """

    def __init__(self, room_display_id: int = None, credential: Credential = None):
        self.room_display_id = room_display_id
        if credential is None:
            self.credential = Credential()
        else:
            self.credential = credential
        # 用于存储uid，避免接口依赖时重复调用
        self.__uid = None

    @property
    def room_display_id(self):
        """
        获取 room_display_id。

        Returns:
            int: room_display_id。
        """
        return self.__room_display_id

    @room_display_id.setter
    def room_display_id(self, room_display_id: int):
        """
        设置 room_display_id。

        Args:
            room_display_id (int):   要设置的 room_display_id。
        """
        if not room_display_id or not isinstance(room_display_id, int):
            raise ArgsException(
                "room_display_id 提供错误，必须要提供 int 类型的 room_display_id")
        self.__room_display_id = room_display_id

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
        self.__uid = int(resp.get('uid', ''))
        return resp

    async def get_chat_conf(self):
        """
        获取聊天弹幕服务器配置信息(websocket)
        :return:
        """
        api = API["info"]["chat_conf"]
        params = {
            "room_id": self.room_display_id
        }
        resp = await request(api['method'], api["url"], params, credential=self.credential)
        return resp

    async def get_room_info(self):
        """
        获取直播间信息（标题，简介等）
        :return:
        """
        api = API["info"]["room_info"]
        params = {
            "room_id": self.room_display_id
        }
        resp = await request(api['method'], api["url"], params, credential=self.credential)
        return resp

    @check_user(proof_listing=['sessdata'])
    async def get_user_info_in_room(self):
        """
        获取自己在直播间的信息（粉丝勋章等级，直播用户等级等）
        :return:
        """
        api = API["info"]["user_info_in_room"]
        params = {
            "room_id": self.room_display_id
        }
        resp = await request(api['method'], api["url"], params, credential=self.credential)
        return resp

    @check_user(proof_listing=['sessdata'])
    async def get_self_info(self):
        """
        获取自己的直播信息
        :return:
        """
        api = API["info"]["user_info"]
        resp = await request(api['method'], api["url"], credential=self.credential)
        return resp

    @check_uid
    async def get_dahanghai_raw(self, page: int = 1, page_size: int = 30):
        """
        低层级API，获取大航海列表
        :param page: 页码
        :param page_size: 保持默认29，每页数量
        :return:
        """
        api = API["info"]["dahanghai"]
        params = {
            "roomid": self.room_display_id,
            "ruid": self.__uid,
            "page_size": page_size,
            "page": page
        }
        resp = await request(api['method'], api["url"], params, credential=self.credential)
        return resp

    @check_uid
    async def get_dahanghai(self, limit: int = 114514, callback=None):
        """
        获取大航海列表
        :param callback: 回调
        :param limit: 限制数量
        :return:
        """
        count = 0
        users = []
        page = 1
        while count < limit:
            resp = await self.get_dahanghai_raw(page)
            if page == 1:
                if len(resp['top3']) != 0:
                    count += len(resp["top3"])
                    users += resp["top3"]
            if len(resp["list"]) == 0:
                break
            count += len(resp["list"])
            users += resp["list"]
            if callable(callback):
                callback(resp["list"])
            page += 1
        return users[:limit]

    @check_uid
    async def get_seven_rank(self):
        """
        获取七日榜
        :return:
        """
        api = API["info"]["seven_rank"]
        params = {
            "roomid": self.room_display_id,
            "ruid": self.__uid,
        }
        resp = await request(api['method'], api["url"], params, credential=self.credential)
        return resp

    @check_uid
    async def get_fans_medal_rank(self):
        """
        获取粉丝勋章排行
        :return:
        """
        api = API["info"]["fans_medal_rank"]
        params = {
            "roomid": self.room_display_id,
            "ruid": self.__uid
        }
        resp = await request(api['method'], api["url"], params, credential=self.credential)
        return resp

    @check_user(proof_listing=['sessdata'])
    async def get_black_raw(self, page: int = 1):
        """
        低层级API，获取黑名单列表
        :param page: 页码
        :return:
        """
        api = API["info"]["black_list"]
        params = {
            "roomid": self.room_display_id,
            "page": page
        }
        resp = await request(api['method'], api["url"], params, credential=self.credential)
        return resp

    @check_user(proof_listing=['sessdata'])
    async def get_black_list(self, limit: int = 114514, callback=None):
        """
        获取房间黑名单列表，登录账号需要是该房间房管
        :param callback: 回调
        :param limit: 限制数量
        :return:
        """
        users = []
        count = 0
        page = 1
        while count < limit:
            resp = await self.get_black_raw(page)
            if len(resp) == 0:
                break
            if callable(callback):
                callback(resp)
            users += resp
            page += 1
            count += len(resp)
        return users[:limit]

    async def get_room_play_url(self, live_clarity: LiveClarity = LiveClarity.Original):
        """
        获取房间直播流列表
        :param live_clarity: 清晰度
        :return:
        """
        api = API["info"]["room_play_url"]
        params = {
            "cid": self.room_display_id,
            "platform": "web",
            "qn": live_clarity.value,
            "https_url_req": "1",
            "ptype": "16"
        }
        resp = await request(api['method'], api["url"], params, credential=self.credential)
        return resp

    async def get_room_play_info_v2(self, live_protocol: LiveProtocol = LiveProtocol.DEFAULT,
                                    live_format: LiveFormat = LiveFormat.DEFAULT,
                                    live_codec: LiveCodec = LiveCodec.DEFAULT,
                                    live_qn: LiveClarity = LiveClarity.Original):
        """
        获取房间信息及可用清晰度列表
        内容比较多，参见文档 https://github.com/Passkou/bilibili-api/blob/main/docs/模块/live.md#get_room_play_info
        :param live_protocol: 流协议
        :param live_format: 容器格式
        :param live_codec: 视频编码
        :param live_qn: 清晰度编号
        :return: resp
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
        resp = await request(api['method'], api['url'], params=params, credential=self.credential)
        return resp

    @check_user(proof_listing=['sessdata', 'bili_jct'])
    async def ban_user(self, uid: int, hour: int = 1):
        """
        封禁用户
        :param hour: 封禁时长，小时
        :param uid: 用户UID
        :return:
        """
        api = API["operate"]["add_block"]
        data = {
            "roomid": self.room_display_id,
            "block_uid": uid,
            "hour": hour,
            "visit_id": ""
        }
        resp = await request(api['method'], api["url"], data=data, credential=self.credential)
        return resp

    @check_user(proof_listing=['sessdata', 'bili_jct'])
    async def unban_user(self, block_id: int):
        """
        解封
        :param block_id: 封禁ID，从live.info.black_list中获取或者live.operate.add_black的返回值获取
        :return:
        """
        api = API["operate"]["del_block"]
        data = {
            "roomid": self.room_display_id,
            "id": block_id,
            "visit_id": "",
        }
        resp = await request(api['method'], api["url"], data=data, credential=self.credential)
        return resp

    @check_user(proof_listing=['sessdata', 'bili_jct'])
    async def send_danmaku(self, danmaku: Danmaku):
        """
        直播间发送弹幕
        :param room_real_id: 真实房间ID
        :param danmaku: utils.Danmaku
        :param verify:
        :return:
        """
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
        resp = await request(api['method'], api["url"], data=data, credential=self.credential)
        return resp

