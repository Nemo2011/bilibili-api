r"""
模块：live
功能：直播间各种信息和操作
项目GitHub地址：https://github.com/Passkou/bilibili_api
项目主页：https://passkou.com/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""
import time
import websockets
import struct
import zlib
import asyncio
import logging
import json
import base64
import functools
from . import exceptions, utils, user
import copy


API = utils.get_api()


def get_room_play_info(room_display_id: int, stream_config: dict = None, verify: utils.Verify = None):
    """
    获取房间信息（真实房间号，封禁情况等）  
    :param room_display_id: 房间号（展示在URL的房间号）  
    :param stream_config: 获取流信息，如不需要可以不传。内容比较多，参见文档 模块/live#get_room_play_info
    :param verify:  
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if stream_config is None:
        stream_config = {
            "protocol": 0,
            "format": 0,
            "codec": 1,
            "qn": 10000
        }

    api = API["live"]["info"]["room_play_info_v2"]
    params = {
        "room_id": room_display_id,
        "platform": "web",
        "ptype": "16",
    }
    if stream_config:
        params.update(stream_config)
    resp = utils.get(api["url"], params, cookies=verify.get_cookies())
    return resp


def get_room_play_url(room_real_id: int, verify: utils.Verify = None):
    """
    获取获取房间直播流地址
    :param room_real_id: 房间真实ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["live"]["info"]["room_play_url"]
    params = {
        "cid": room_real_id,
        "platform": "web",
        "qn": 10000,
        "https_url_req": "1",
        "ptype": "16"
    }
    resp = utils.get(api["url"], params, cookies=verify.get_cookies())
    return resp


def get_chat_conf(room_real_id: int, verify: utils.Verify = None):
    """
    获取聊天弹幕服务器配置信息(websocket)
    :param room_real_id: 真实房间号
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["live"]["info"]["chat_conf"]
    resp = utils.get(api["url"], {"room_id": room_real_id}, cookies=verify.get_cookies())
    return resp


def get_room_info(room_real_id: int, verify: utils.Verify = None):
    """
    获取直播间信息（标题，简介等）
    :param room_real_id: 真实房间ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["live"]["info"]["room_info"]
    resp = utils.get(api["url"], {"room_id": room_real_id}, cookies=verify.get_cookies())
    return resp


def get_user_info_in_room(room_real_id: int, verify: utils.Verify = None):
    """
    获取自己在直播间的信息（粉丝勋章等级，直播用户等级等）
    :param room_real_id: 真实房间ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["live"]["info"]["user_info_in_room"]
    resp = utils.get(api["url"], {"room_id": room_real_id}, cookies=verify.get_cookies())
    return resp


def get_self_info(verify: utils.Verify = None):
    """
    获取直播用户等级等信息
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["live"]["info"]["user_info"]
    resp = utils.get(api["url"], cookies=verify.get_cookies())
    return resp


def get_black_list(room_real_id: int, limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    获取房间黑名单列表，登录账号需要是该房间房管
    :param callback: 回调
    :param limit: 限制数量
    :param room_real_id: 房间真实ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["live"]["info"]["black_list"]
    users = []
    count = 0
    page = 1
    while count < limit:
        resp = utils.get(api["url"], {"roomid": room_real_id, "page": page}, cookies=verify.get_cookies())
        if len(resp) == 0:
            break
        if callable(callback):
            callback(resp)
        users += resp
        page += 1
        count += len(resp)
    return users[:limit]


def get_dahanghai_raw(room_real_id: int, ruid: int, page: int = 1, page_size: int = 29, verify: utils.Verify = None):
    """
    低层级API，获取大航海列表
    :param room_real_id: 房间真实ID
    :param ruid: room_uid
    :param page: 页码
    :param page_size: 保持默认29，每页数量
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["live"]["info"]["dahanghai"]
    params = {
        "roomid": room_real_id,
        "ruid": ruid,
        "page_size": page_size,
        "page": page
    }
    resp = utils.get(api["url"], params, cookies=verify.get_cookies())
    return resp


def get_dahanghai(room_real_id: int, limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    获取大航海列表
    :param callback: 回调
    :param limit: 限制数量
    :param room_real_id: 真实房间ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    ruid = get_room_play_info(room_real_id)["uid"]
    count = 0
    users = []
    page = 1
    while count < limit:
        resp = get_dahanghai_raw(room_real_id=room_real_id, ruid=ruid, page=page, verify=verify)
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


def get_seven_rank(room_real_id: int, verify: utils.Verify = None):
    """
    获取七日榜
    :param room_real_id: 真实房间ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["live"]["info"]["seven_rank"]
    ruid = get_room_play_info(room_real_id)["uid"]
    resp = utils.get(api["url"], {"roomid": room_real_id, "ruid": ruid}, cookies=verify.get_cookies())
    return resp


def get_fans_medal_rank(room_real_id: int, verify: utils.Verify = None):
    """
    获取粉丝勋章排行
    :param room_real_id: 真实房间ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["live"]["info"]["fans_medal_rank"]
    ruid = get_room_play_info(room_real_id)["uid"]
    resp = utils.get(api["url"], {"roomid": room_real_id, "ruid": ruid}, cookies=verify.get_cookies())
    return resp


def send_danmaku(room_real_id: int, danmaku: utils.Danmaku, verify: utils.Verify = None):
    """
    直播间发送弹幕
    :param room_real_id: 真实房间ID
    :param danmaku: utils.Danmaku
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["live"]["operate"]["send_danmaku"]
    data = {
        "mode": danmaku.mode,
        "msg": danmaku.text,
        "roomid": room_real_id,
        "bubble": 0,
        "csrf": verify.csrf,
        "csrf_token": verify.csrf,
        "rnd": int(time.time()),
        "color": danmaku.color.get_dec_color(),
        "fontsize": danmaku.font_size
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def ban_user(room_real_id: int, uid: int, hour: int = 1, verify: utils.Verify = None):
    """
    封禁用户
    :param hour: 封禁时长，小时
    :param uid: 用户UID
    :param room_real_id: 真实房间ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["live"]["operate"]["add_block"]
    data = {
        "roomid": room_real_id,
        "block_uid": uid,
        "hour": hour,
        "csrf": verify.csrf,
        "csrf_token": verify.csrf,
        "visit_id": ""
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def unban_user(room_real_id: int, block_id: int, verify: utils.Verify = None):
    """
    解封
    :param block_id: 封禁ID，从live.info.black_list中获取或者live.operate.add_black的返回值获取
    :param room_real_id: 真实房间ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["live"]["operate"]["del_block"]
    data = {
        "roomid": room_real_id,
        "id": block_id,
        "visit_id": "",
        "csrf": verify.csrf,
        "csrf_token": verify.csrf
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def connect_all_LiveDanmaku(*livedanmaku_classes):
    """
    简单同时连接多个直播间，一般建议自行处理事件循环来进行更精准的控制
    使用 `room.connect(True)` 可以返回一个 Coroutine，将这个安排进事件循环即可连接到房间
    :param livedanmaku_classes: LiveDanmaku类动态参数
    :return:
    """

    async def run():
        tasks = []
        for room in livedanmaku_classes:
            task = asyncio.create_task(room.connect(True))
            tasks.append(task)
        await asyncio.gather(*tasks)

    asyncio.run(run())


class LiveDanmaku(object):
    """
    Websocket实时获取直播弹幕
    """
    PROTOCOL_VERSION_RAW_JSON = 0
    PROTOCOL_VERSION_HEARTBEAT = 1
    PROTOCOL_VERSION_ZLIB_JSON = 2

    DATAPACK_TYPE_HEARTBEAT = 2
    DATAPACK_TYPE_HEARTBEAT_RESPONSE = 3
    DATAPACK_TYPE_NOTICE = 5
    DATAPACK_TYPE_VERIFY = 7
    DATAPACK_TYPE_VERIFY_SUCCESS_RESPONSE = 8

    def __init__(self, room_display_id: int, debug: bool = False, use_wss: bool = True, should_reconnect: bool = True
                 , verify: utils.Verify = None):
        self.verify = verify
        self.room_real_id = room_display_id
        self.room_display_id = room_display_id
        self.__use_wss = use_wss
        self.__event_loop = asyncio.get_event_loop()
        # logging
        self.logger = logging.getLogger(f"LiveDanmaku_{self.room_display_id}")
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[" + str(room_display_id) + "][%(asctime)s][%(levelname)s] %(message)s"))
        self.logger.addHandler(handler)

        self.__event_handlers = {}
        self.__websocket = None
        # 连接状态，0未连接，1已连接，3已正常断开，-1异常断开
        self.__connected_status = 0
        self.__conf = None

        # 重连设置
        self.should_reconnect = should_reconnect

        self.__heartbeat_task = None
        self.__is_single_room = False

    def connect(self, return_coroutine: bool = False):
        """
        连接直播间
        :param return_coroutine: 是否返回房间入口的 Coroutine 而不是直接连接单个房间。用以自行进行更精准的异步控制。
        :return:
        """
        if self.__connected_status == 1:
            raise exceptions.LiveException("已连接直播间，不可重复连接")
        if return_coroutine:
            self.__is_single_room = False
            return self.__main()
        else:
            self.__is_single_room = True
            asyncio.get_event_loop().run_until_complete(self.__main())

    def disconnect(self):
        """
        断开连接
        :return:
        """
        self.__connected_status = 2
        asyncio.gather(self.__ws.close())

    def get_connect_status(self):
        return self.__connected_status

    async def __main(self):
        """
        入口
        :return:
        """
        # 获取真实房间号
        self.logger.debug("正在获取真实房间号")
        self.room_real_id = get_room_play_info(room_display_id=self.room_real_id, verify=self.verify)["room_id"]
        self.logger.debug(f"获取成功，真实房间号：{self.room_real_id}")
        # 获取直播服务器配置
        self.logger.debug("正在获取聊天服务器配置")
        self.__conf = get_chat_conf(room_real_id=self.room_real_id, verify=self.verify)
        self.logger.debug("聊天服务器配置获取成功")
        # 连接直播间
        self.logger.debug("准备连接直播间")
        for host in self.__conf["host_server_list"]:
            port = host['wss_port'] if self.__use_wss else host['ws_port']
            protocol = "wss" if self.__use_wss else "ws"
            uri = f"{protocol}://{host['host']}:{port}/sub"
            self.logger.debug(f"正在尝试连接主机： {uri}")
            try:
                while True:
                    async with websockets.connect(uri) as ws:
                        self.__ws = ws
                        self.logger.debug(f"连接主机成功, 准备发送认证信息")
                        uid = None
                        if self.verify is not None:
                            if self.verify.has_sess():
                                self.logger.debug("检测到传入Verify，正在获取用户UID")
                                self_info = user.get_self_info(self.verify)
                                uid = self_info["mid"]
                                self.logger.debug(f"用户UID为{uid}")
                        verifyData = {"uid": 0 if uid is None else uid, "roomid": self.room_real_id,
                                      "protover": 2, "platform": "web",
                                      "clientver": "1.17.0", "type": 2, "key": self.__conf["token"]}
                        data = json.dumps(verifyData).encode()
                        await self.__send(data, LiveDanmaku.PROTOCOL_VERSION_HEARTBEAT, LiveDanmaku.DATAPACK_TYPE_VERIFY)
                        self.__connected_status = 1
                        await self.__loop()
                        if self.__connected_status >= 0:
                            return
                        if not self.should_reconnect:
                            return
            except websockets.ConnectionClosedError:
                self.logger.warning(f"连接失败，准备尝试下一个地址")
        else:
            self.__connected_status = -1
            self.logger.error(f"所有主机连接失败，程序终止")

    async def __loop(self):
        """
        循环收取数据
        :return:
        """
        heartbeat_task = asyncio.create_task(self.__heartbeat())
        self.__heartbeat_task = heartbeat_task
        while True:
            try:
                data = await self.__recv()
            except websockets.ConnectionClosed:
                callback_info = {
                    'room_display_id': self.room_display_id,
                    'room_real_id': self.room_real_id,
                    "type": "DISCONNECT",
                    "data": self.__connected_status
                }
                handlers = self.__event_handlers.get("DISCONNECT", []) + self.__event_handlers.get("ALL", [])
                for handler in handlers:
                    asyncio.create_task(self.__run_as_asynchronous_func(handler, callback_info))
                if self.__connected_status == 2:
                    self.logger.info("连接正常断开")
                    return
                else:
                    self.__connected_status = -1
                    self.logger.warning("连接被异常断开")
                if self.__heartbeat_task is not None:
                    self.__heartbeat_task.cancel()
                break
            self.logger.debug(f"收到信息：{data}")
            for info in data:
                callback_info = {
                    'room_display_id': self.room_display_id,
                    'room_real_id': self.room_real_id
                }
                # 依次处理并调用用户指定函数
                if info["datapack_type"] == LiveDanmaku.DATAPACK_TYPE_VERIFY_SUCCESS_RESPONSE:
                    # 认证反馈
                    if info["data"]["code"] == 0:
                        # 认证成功反馈
                        self.logger.info("连接服务器并认证成功")
                    else:
                        # 认证失败（实际上直接断开了）
                        self.logger.error("连接服务器成功但认证失败")
                elif info["datapack_type"] == LiveDanmaku.DATAPACK_TYPE_HEARTBEAT_RESPONSE:
                    # 心跳包反馈，返回直播间人气
                    self.logger.debug("收到心跳包反馈")
                    callback_info["type"] = 'VIEW'
                    callback_info["data"] = info["data"]["view"]
                    handlers = self.__event_handlers.get("VIEW", []) + self.__event_handlers.get("ALL", [])
                    for handler in handlers:
                        asyncio.create_task(self.__run_as_asynchronous_func(handler, callback_info))
                elif info["datapack_type"] == LiveDanmaku.DATAPACK_TYPE_NOTICE:
                    # 直播间弹幕、礼物等信息
                    callback_info["type"] = info["data"]["cmd"]
                    callback_info["data"] = info["data"]
                    handlers = self.__event_handlers.get(info["data"]["cmd"], []) + self.__event_handlers.get("ALL", [])
                    for handler in handlers:
                        asyncio.create_task(self.__run_as_asynchronous_func(handler, callback_info))
                else:
                    self.logger.warning("检测到未知的数据包类型，无法处理")

    async def __heartbeat(self):
        """
        定时发送心跳包
        :return:
        """
        HEARTBEAT = base64.b64decode("AAAAHwAQAAEAAAACAAAAAVtvYmplY3QgT2JqZWN0XQ==")
        while self.__connected_status == 1:
            self.logger.debug("发送心跳包")
            await self.__ws.send(HEARTBEAT)
            await asyncio.sleep(30.0)

    async def __send(self, data: bytes, protocol_version: int, datapack_type: int):
        """
        自动打包并发送数据
        :param data: 待发送的二进制数据
        :param protocol_version: 数据包协议版本
        :param datapack_type: 数据包类型
        :return:
        """
        data = self.__pack(data, protocol_version, datapack_type)
        await self.__ws.send(data)

    async def __recv(self):
        """
        接收数据并自动解包
        :return:
        """
        raw_data = await self.__ws.recv()
        data = self.__unpack(raw_data)
        return data

    @classmethod
    def __pack(cls, data: bytes, protocol_version: int, datapack_type: int):
        """
        打包数据
        :param data: 待发送的二进制数据
        :param protocol_version: 数据包协议版本
        :param datapack_type: 数据包类型
        :return:
        """
        sendData = bytearray()
        sendData += struct.pack(">H", 16)
        assert 0 <= protocol_version <= 2, exceptions.LiveException("数据包协议版本错误，范围0~2")
        sendData += struct.pack(">H", protocol_version)
        assert datapack_type in [2, 7], exceptions.LiveException("数据包类型错误，可用类型：2, 7")
        sendData += struct.pack(">I", datapack_type)
        sendData += struct.pack(">I", 1)
        sendData += data
        sendData = struct.pack(">I", len(sendData) + 4) + sendData
        return bytes(sendData)

    @classmethod
    def __unpack(cls, data: bytes):
        """
        解包数据
        :param data: 服务器传来的原始数据
        :return:
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
                if header[3] == cls.DATAPACK_TYPE_HEARTBEAT_RESPONSE:
                    recvData["data"] = {"view": struct.unpack(">I", chunkData)[0]}
                elif header[3] == cls.DATAPACK_TYPE_VERIFY_SUCCESS_RESPONSE:
                    recvData["data"] = json.loads(chunkData.decode())
            ret.append(recvData)
            offset += length
        return ret

    @staticmethod
    async def __run_as_asynchronous_func(func, *args):
        """
        区分同步和异步执行函数
        :param func: 回调函数，非异步函数
        :param *args: 传递给函数的参数
        :return:
        """
        if asyncio.iscoroutinefunction(func):
            await func(*args)
        else:
            func(*args)

    def add_event_handler(self, event_name: str, func):
        """
        为当前直播弹幕增加事件回调
        :param event_name: 事件名
        :param func: 回调函数
        :return:
        """
        if not callable(func):
            raise exceptions.LiveException("回调函数请传入方法")
        upper_name = event_name.upper()
        if upper_name not in self.__event_handlers:
            self.__event_handlers[upper_name] = []
        self.__event_handlers[upper_name].append(func)

    def on(self, name: str):
        """
        使用@语法，触发事件时会被调用
        :param name: 事件名
        :return:
        """
        """
        直播区更新速度快，以实际API为准，可以开debug自己看
        常见事件名：
        DANMU_MSG: 用户发送弹幕
        SEND_GIFT: 礼物
        COMBO_SEND：礼物连击
        GUARD_BUY：续费大航海
        SUPER_CHAT_MESSAGE：醒目留言（SC）
        SUPER_CHAT_MESSAGE_JPN：醒目留言（带日语翻译？）
        WELCOME: 老爷进入房间
        WELCOME_GUARD: 房管进入房间
        NOTICE_MSG: 系统通知（全频道广播之类的）
        PREPARING: 直播准备中
        LIVE: 直播开始
        ROOM_REAL_TIME_MESSAGE_UPDATE: 粉丝数等更新
        ENTRY_EFFECT: 进场特效
        ROOM_RANK: 房间排名更新
        INTERACT_WORD: 用户进入直播间
        ACTIVITY_BANNER_UPDATE_V2: 好像是房间名旁边那个xx小时榜
        本模块自定义事件：
        VIEW: 直播间人气更新
        ALL: 所有事件
        DISCONNECT: 断开连接（传入连接状态码参数）
        """
        def decoration(func):
            upper_name = name.upper()
            if upper_name not in self.__event_handlers:
                self.__event_handlers[upper_name] = []
            self.__event_handlers[upper_name].append(func)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
            return wrapper
        return decoration


"""
なにせ高性能ですから！（このAPIを指す）
ーー「ATRI」
"""
