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
from enum import Enum

from .exceptions import ArgsException, CredentialNoSessdataException, CredentialNoBiliJctException
from .utils.Credential import Credential
from .utils.network import request
from .utils.utils import get_api

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
        # 用于存储uid，避免接口依时重复调用
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

    async def get_room_play_info(self, stream_config: dict = None):
        """
        获取房间信息（真实房间号，封禁情况等）
        :param stream_config: 获取流信息，如不需要可以不传。内容比较多，参见文档 https://github.com/Passkou/bilibili-api/blob/main/docs/模块/live.md#get_room_play_info
        :return: resp
        """
        if stream_config is None:
            stream_config = {
                "protocol": 0,
                "format": 0,
                "codec": 1,
                "qn": 10000
            }
        api = API["info"]["room_play_info"]
        params = {
            "room_id": self.room_display_id,
            "platform": "web",
            "ptype": "16",
        }
        if stream_config:
            params.update(stream_config)
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

    async def get_dahanghai_raw(self, page: int = 1, page_size: int = 30):
        """
        低层级API，获取大航海列表
        :param page: 页码
        :param page_size: 保持默认29，每页数量
        :return:
        """
        if not self.__uid:
            await self.get_room_play_info()
        api = API["info"]["dahanghai"]
        params = {
            "roomid": self.room_display_id,
            "ruid": self.__uid,
            "page_size": page_size,
            "page": page
        }
        resp = await request(api['method'], api["url"], params, credential=self.credential)
        return resp

    async def get_dahanghai(self, limit: int = 114514, callback=None):
        """
        获取大航海列表
        :param callback: 回调
        :param limit: 限制数量
        :return:
        """
        if not self.__uid:
            await self.get_room_play_info()
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

    async def get_room_play_url(self, live_clarity: LiveClarity = LiveClarity.Original):
        """
        获取获取房间直播流地址
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


"""
なにせ高性能ですから！（このAPIを指す）
ーー「ATRI」
"""
