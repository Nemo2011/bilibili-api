r"""
bilibili_api.live

直播相关
"""
import time
from enum import Enum
import logging
import json
import struct
import base64
import asyncio
import aiohttp
import zlib

from aiohttp.client_ws import ClientWebSocketResponse
from aiohttp.http_websocket import WSMsgType

from .utils.Credential import Credential
from .utils.network import get_session, request
from .utils.utils import get_api
from .utils.Danmaku import Danmaku
from .utils.AsyncEvent import AsyncEvent
from .exceptions.LiveException import LiveException

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


class LiveRoom:
    """
    直播类，获取各种直播间的操作均在里边。
    """

    def __init__(self, room_display_id: int, credential: Credential = None):
        """
        Args:
            room_display_id (int)                 : 房间展示 ID（即 URL 中的 ID）
            credential      (Credential, optional): 凭据. Defaults to None.
        """
        self.room_display_id = room_display_id

        if credential is None:
            self.credential = Credential()
        else:
            self.credential = credential

        self.__ruid = None

    async def get_room_play_info(self):
        """
        获取房间信息（真实房间号，封禁情况等）

        Returns:
            API 调用返回结果
        """
        api = API["info"]["room_play_info"]
        params = {
            "room_id": self.room_display_id,
        }
        resp = await request(api['method'], api['url'], params=params, credential=self.credential)

        # 缓存真实房间 ID
        self.__ruid = resp['uid']
        return resp

    async def __get_ruid(self):
        """
        获取真实房间 ID，若有缓存则使用缓存
        """
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

        Args:
            live_protocol (LiveProtocol, optional)    : 直播源流协议. Defaults to LiveProtocol.DEFAULT.
            live_format   (LiveFormat, optional)      : 直播源容器格式. Defaults to LiveFormat.DEFAULT.
            live_codec    (LiveCodec, optional)       : 直播源视频编码. Defaults to LiveCodec.DEFAULT.
            live_qn       (ScreenResolution, optional): 直播源清晰度. Defaults to ScreenResolution.ORIGINAL.
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
            hour (int, optional): 封禁时长（小时）. Defaults to 1
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
            block_id (int): 封禁用户时会返回该封禁事件的 ID，使用该值
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


class LiveDanmaku(AsyncEvent):
    """
    Websocket 实时获取直播弹幕

    Events：
    + DANMU_MSG: 用户发送弹幕
    + SEND_GIFT: 礼物
    + COMBO_SEND：礼物连击
    + GUARD_BUY：续费大航海
    + SUPER_CHAT_MESSAGE：醒目留言（SC）
    + SUPER_CHAT_MESSAGE_JPN：醒目留言（带日语翻译？）
    + WELCOME: 老爷进入房间
    + WELCOME_GUARD: 房管进入房间
    + NOTICE_MSG: 系统通知（全频道广播之类的）
    + PREPARING: 直播准备中
    + LIVE: 直播开始
    + ROOM_REAL_TIME_MESSAGE_UPDATE: 粉丝数等更新
    + ENTRY_EFFECT: 进场特效
    + ROOM_RANK: 房间排名更新
    + INTERACT_WORD: 用户进入直播间
    + ACTIVITY_BANNER_UPDATE_V2: 好像是房间名旁边那个xx小时榜
    + 本模块自定义事件：
    + VIEW: 直播间人气更新
    + ALL: 所有事件
    + DISCONNECT: 断开连接（传入连接状态码参数）
    """
    PROTOCOL_VERSION_RAW_JSON = 0
    PROTOCOL_VERSION_HEARTBEAT = 1
    PROTOCOL_VERSION_ZLIB_JSON = 2

    DATAPACK_TYPE_HEARTBEAT = 2
    DATAPACK_TYPE_HEARTBEAT_RESPONSE = 3
    DATAPACK_TYPE_NOTICE = 5
    DATAPACK_TYPE_VERIFY = 7
    DATAPACK_TYPE_VERIFY_SUCCESS_RESPONSE = 8

    STATUS_INIT = 0
    STATUS_CONNECTING = 1
    STATUS_ESTABLISHED = 2
    STATUS_CLOSING = 3
    STATUS_CLOSED = 4
    STATUS_ERROR = 5

    def __init__(self, room_display_id: int, debug: bool = False,
                    credential: Credential = None):
        """
        Args:
            room_display_id (int)                 : 房间展示 ID
            debug           (bool, optional)      : 调试模式，将输出更多信息。. Defaults to False.
            credential      (Credential, optional): 凭据. Defaults to None.
        """
        super().__init__()

        self.credential = credential if credential is not None else Credential()
        self.room_display_id = room_display_id
        self.__room_real_id = None
        self.__status = 0
        self.__ws = None
        self.__tasks = []
        self.__debug = debug

        # logging
        self.logger = logging.getLogger(f"LiveDanmaku_{self.room_display_id}")
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[" + str(room_display_id) + "][%(asctime)s][%(levelname)s] %(message)s"))
        self.logger.addHandler(handler)

    def get_status(self):
        """
        获取连接状态

        Returns:
            int: 0 初始化，1 连接建立中，2 已连接，3 断开连接中，4 已断开，5 错误
        """
        return self.__status

    async def connect(self):
        """
        连接直播间
        """
        if self.get_status() == self.STATUS_CONNECTING:
            raise LiveException('正在建立连接中')

        if self.get_status() == self.STATUS_ESTABLISHED:
            raise LiveException('连接已建立，不可重复调用')

        if self.get_status() == self.STATUS_CLOSING:
            raise LiveException('正在关闭连接，不可调用')

        await self.__main()


    async def disconnect(self):
        """
        断开连接
        """
        if self.get_status() != self.STATUS_ESTABLISHED:
            raise LiveException('尚未连接服务器')

        self.__status = self.STATUS_CLOSING
        self.logger.info('连接正在关闭')

        # 取消所有任务
        while len(self.__tasks) > 0:
            self.__tasks.pop().cancel()

        await self.__ws.close()
        self.__status = self.STATUS_CLOSED

        self.logger.info('连接已关闭')


    async def __main(self):
        """
        入口
        """
        self.__status == self.STATUS_CONNECTING

        room = LiveRoom(self.room_display_id, self.credential)
        # 获取真实房间号
        self.logger.debug("正在获取真实房间号")
        self.__room_real_id = (await room.get_room_play_info())["room_id"]
        self.logger.debug(f"获取成功，真实房间号：{self.__room_real_id}")

        # 获取直播服务器配置
        self.logger.debug("正在获取聊天服务器配置")
        conf = await room.get_chat_conf()
        self.logger.debug("聊天服务器配置获取成功")

        # 连接直播间
        self.logger.debug("准备连接直播间")
        session = get_session()

        for host in conf["host_server_list"]:
            port = host['wss_port']
            protocol = "wss"
            uri = f"{protocol}://{host['host']}:{port}/sub"
            self.logger.debug(f"正在尝试连接主机： {uri}")

            try:
                async with session.ws_connect(uri) as ws:
                    self.__ws = ws
                    self.logger.debug(f"连接主机成功, 准备发送认证信息")
                    await self.__send_verify_data(ws, conf['token'])

                    # 新建心跳任务
                    self.__tasks.append(asyncio.create_task(self.__heartbeat(ws)))

                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.BINARY:
                            await self.__handle_data(msg.data)

                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            self.__status = self.STATUS_ERROR
                            self.logger.error('出现错误')

                        elif msg.type == aiohttp.WSMsgType.CLOSING:
                            self.logger.debug('连接正在关闭')
                            self.__status = self.STATUS_CLOSING

                        elif msg.type == aiohttp.WSMsgType.CLOSED:
                            self.logger.info('连接已关闭')
                            self.__status = self.STATUS_CLOSED
                break

            except Exception as e:
                self.logger.error('出现错误：' + str(e))
                if self.__debug:
                    raise e

    async def __handle_data(self, data):
        """
        处理数据
        """
        data = self.__unpack(data)
        self.logger.debug(f"收到信息：{data}")

        for info in data:
            callback_info = {
                'room_display_id': self.room_display_id,
                'room_real_id': self.__room_real_id
            }
            # 依次处理并调用用户指定函数
            if info["datapack_type"] == LiveDanmaku.DATAPACK_TYPE_VERIFY_SUCCESS_RESPONSE:
                # 认证反馈
                if info["data"]["code"] == 0:
                    # 认证成功反馈
                    self.logger.info("连接服务器并认证成功")
                    self.__status = self.STATUS_ESTABLISHED

            elif info["datapack_type"] == LiveDanmaku.DATAPACK_TYPE_HEARTBEAT_RESPONSE:
                # 心跳包反馈，返回直播间人气
                self.logger.debug("收到心跳包反馈")
                callback_info["type"] = 'VIEW'
                callback_info["data"] = info["data"]["view"]
                self.dispatch('VIEW', callback_info)
                self.dispatch('ALL', callback_info)

            elif info["datapack_type"] == LiveDanmaku.DATAPACK_TYPE_NOTICE:
                # 直播间弹幕、礼物等信息
                callback_info["type"] = info["data"]["cmd"]

                # DANMU_MSG 事件名特殊：DANMU_MSG:4:0:2:2:2:0，需取出事件名，暂不知格式
                if callback_info["type"].find('DANMU_MSG') > -1:
                     callback_info["type"] = 'DANMU_MSG'
                     info["data"]["cmd"] = 'DANMU_MSG'

                callback_info["data"] = info["data"]
                self.dispatch(callback_info["type"], callback_info)
                self.dispatch('ALL', callback_info)

            else:
                self.logger.warning("检测到未知的数据包类型，无法处理")

    async def __send_verify_data(self, ws: ClientWebSocketResponse, token: str):
        verifyData = {"uid": 0, "roomid": self.__room_real_id,
                        "protover": 2, "platform": "web", "type": 2, "key": token}
        data = json.dumps(verifyData).encode()
        await self.__send(data, self.PROTOCOL_VERSION_HEARTBEAT, self.DATAPACK_TYPE_VERIFY, ws)


    async def __heartbeat(self, ws: ClientWebSocketResponse):
        """
        定时发送心跳包
        """
        HEARTBEAT = base64.b64decode("AAAAHwAQAAEAAAACAAAAAVtvYmplY3QgT2JqZWN0XQ==")
        while True:
            self.logger.debug("发送心跳包")
            await ws.send_bytes(HEARTBEAT)
            await asyncio.sleep(30.0)

    async def __send(self, data: bytes, protocol_version: int, datapack_type: int, ws: ClientWebSocketResponse):
        """
        自动打包并发送数据
        """
        data = self.__pack(data, protocol_version, datapack_type)
        await ws.send_bytes(data)

    @staticmethod
    def __pack(data: bytes, protocol_version: int, datapack_type: int):
        """
        打包数据
        """
        sendData = bytearray()
        sendData += struct.pack(">H", 16)
        assert 0 <= protocol_version <= 2, LiveException("数据包协议版本错误，范围0~2")
        sendData += struct.pack(">H", protocol_version)
        assert datapack_type in [2, 7], LiveException("数据包类型错误，可用类型：2, 7")
        sendData += struct.pack(">I", datapack_type)
        sendData += struct.pack(">I", 1)
        sendData += data
        sendData = struct.pack(">I", len(sendData) + 4) + sendData
        return bytes(sendData)

    @staticmethod
    def __unpack(data: bytes):
        """
        解包数据
        """
        ret = []
        offset = 0
        header = struct.unpack(">IHHII", data[:16])
        if header[2] == 2:
            realData = zlib.decompress(data[16:])
        else:
            realData = data

        while offset < len(realData):
            header = struct.unpack(">IHHII", realData[offset:offset + 16])
            length = header[0]
            recvData = {
                "protocol_version": header[2],
                "datapack_type": header[3],
                "data": None
            }
            chunkData = realData[(offset + 16):(offset + length)]
            if header[2] == 0:
                recvData["data"] = json.loads(chunkData.decode())
            elif header[2] == 2:
                recvData["data"] = json.loads(chunkData.decode())
            elif header[2] == 1:
                if header[3] == LiveDanmaku.DATAPACK_TYPE_HEARTBEAT_RESPONSE:
                    recvData["data"] = {"view": struct.unpack(">I", chunkData)[0]}
                elif header[3] == LiveDanmaku.DATAPACK_TYPE_VERIFY_SUCCESS_RESPONSE:
                    recvData["data"] = json.loads(chunkData.decode())
            ret.append(recvData)
            offset += length
        return ret


async def get_self_info(credential: Credential):
    """
    获取自己直播等级、排行等信息
    """
    credential.raise_for_no_sessdata()

    api = API["info"]["user_info"]
    return await request(api['method'], api["url"], credential=credential)
