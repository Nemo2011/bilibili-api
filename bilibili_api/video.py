"""
bilibili_api.video

视频相关操作
"""

from bilibili_api.exceptions.ResponseException import ResponseException
import aiohttp
import re
import json
import datetime

from .exceptions.NetworkException import NetworkException
from .utils.Credential import Credential
from .exceptions import ArgsException, DanmakuClosedException
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.utils import get_api
from .utils.network import request, get_session
from .utils.Danmaku import Danmaku
from .utils.Color import Color
from .utils.BytesReader import BytesReader

API = get_api("video")


class Video:
    """
    视频类，各种对视频的操作均在里面。
    """

    def __init__(self, bvid: str = None, aid: int = None, credential: Credential = None):
        """
        Args:
            bvid (str, optional):               BV 号. bvid 和 aid 必须提供其中之一。
            aid (int, optional):                AV 号. bvid 和 aid 必须提供其中之一。
            credential (Credential, optional):  Credential 类. Defaults to None.
        """
        # ID 检查
        if bvid is not None:
            self.set_bvid(bvid)
        elif aid is not None:
            self.set_aid(aid)
        else:
            # 未提供任一 ID
            raise ArgsException("请至少提供 bvid 和 aid 中的其中一个参数。")

        # 未提供 credential 时初始化该类
        if credential is None:
            self.credential = Credential()
        else:
            self.credential = credential

        # 用于存储视频信息，避免接口依赖视频信息时重复调用
        self.__info = None

    def set_bvid(self, bvid: str):
        """
        设置 bvid。

        Args:
            bvid (str):   要设置的 bvid。
        """
        # 检查 bvid 是否有效
        if not re.search("^BV[a-zA-Z0-9]{10}$", bvid):
            raise ArgsException(
                "bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。")
        self.__bvid = bvid
        self.__aid = bvid2aid(bvid)

    def get_bvid(self):
        """
        获取 BVID。

        Returns:
            BVID。
        """
        return self.__bvid

    def set_aid(self, aid: int):
        """
        设置 aid。

        Args:
            aid (int):   AV 号。
        """
        if aid <= 0:
            raise ArgsException("aid 不能小于或等于 0。")

        self.__aid = aid
        self.__bvid = aid2bvid(aid)

    def get_aid(self):
        """
        获取 AID。

        Returns:
            aid。
        """
        return self.__aid

    async def get_info(self):
        """
        获取视频信息。

        Returns:
            dict, 调用 API 返回的结果。
        """
        url = API["info"]["detail"]["url"]
        params = {
            "bvid": self.get_bvid(),
            "aid": self.get_aid()
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        # 存入 self.__info 中以备后续调用
        self.__info = resp
        return resp

    async def __get_info_cached(self):
        """
        获取视频信息，如果已获取过则使用之前获取的信息，没有则重新获取。

        Returns:
            dict, 调用 API 返回的结果。
        """
        if self.__info is None:
            return await self.get_info()
        return self.__info

    async def get_stat(self):
        """
        获取视频统计数据（播放量，点赞数等）。

        Returns:
            dict, 调用 API 返回的结果。
        """
        url = API["info"]["stat"]["url"]
        params = {
            "bvid": self.get_bvid(),
            "aid": self.get_aid()
        }
        return await request("GET", url, params=params, credential=self.credential)

    async def get_tags(self):
        """
        获取视频标签。

        Returns:
            dict, 调用 API 返回的结果。
        """
        url = API["info"]["tags"]["url"]
        params = {
            "bvid": self.get_bvid(),
            "aid": self.get_aid()
        }
        return await request("GET", url, params=params, credential=self.credential)

    async def get_chargers(self):
        """
        获取视频充电用户。

        Returns:
            dict, 调用 API 返回的结果。
        """
        info = await self.__get_info_cached()
        mid = info["owner"]["mid"]
        url = API["info"]["chargers"]["url"]
        params = {
            "aid": self.get_aid(),
            "bvid": self.get_bvid(),
            "mid": mid
        }
        return await request("GET", url, params=params, credential=self.credential)

    async def get_pages(self):
        """
        获取分 P 信息。

        Returns:
            dict, 调用 API 返回的结果。
        """
        url = API["info"]["pages"]["url"]
        params = {
            "aid": self.get_aid(),
            "bvid": self.get_bvid()
        }
        return await request("GET", url, params=params, credential=self.credential)

    async def __get_page_id_by_index(self, page_index: int):
        """
        根据分 p 号获取 page_id。

        Args:
            page_index (int):   分 P 号，从 0 开始。

        Returns:
            int, 分 P 的唯一 ID。
        """
        if page_index < 0:
            raise ArgsException("分 p 号必须大于或等于 0。")

        info = await self.__get_info_cached()
        pages = info["pages"]

        if len(pages) > (page_index + 1):
            raise ArgsException("不存在该分 p。")

        page = pages[page_index]
        cid = page["cid"]
        return cid

    async def get_download_url(self, page_index: int):
        """
        获取视频下载信息。

        Args:
            page_index (int):  分 P 号，从 0 开始。

        Returns:
            dict, 调用 API 返回的结果。
        """
        cid = await self.__get_page_id_by_index(page_index)

        url = API["info"]["playurl"]["url"]
        params = {
            "avid": self.get_aid(),
            "cid": cid,
            "qn": "120",
            "otype": "json",
            "fnval": 16
        }
        return await request("GET", url, params=params, credential=self.credential)

    async def get_related(self):
        """
        获取相关视频信息。

        Returns:
            dict, 调用 API 返回的结果。
        """
        url = API["info"]["related"]["url"]
        params = {
            "aid": self.get_aid(),
            "bvid": self.get_bvid()
        }
        return await request("GET", url, params=params, credential=self.credential)

    async def has_liked(self):
        """
        视频是否点赞过。

        Returns:
            bool, 视频是否点赞过。
        """
        self.credential.raise_for_no_sessdata()

        url = API["info"]["has_liked"]["url"]
        params = {
            "bvid": self.get_bvid(),
            "aid": self.get_aid()
        }
        return await request("GET", url, params=params, credential=self.credential) == 1

    async def get_pay_coins(self):
        """
        获取视频已投币数量。

        Returns:
            int, 视频已投币数量。
        """
        self.credential.raise_for_no_sessdata()

        url = API["info"]["get_pay_coins"]["url"]
        params = {
            "bvid": self.get_bvid(),
            "aid": self.get_aid()
        }
        return (await request("GET", url, params=params, credential=self.credential))["multiply"]

    async def has_favoured(self):
        """
        是否已收藏。

        Returns:
            bool, 视频是否已收藏。
        """
        self.credential.raise_for_no_sessdata()

        url = API["info"]["has_favoured"]["url"]
        params = {
            "bvid": self.get_bvid(),
            "aid": self.get_aid()
        }
        return (await request("GET", url, params=params, credential=self.credential))["favoured"]

    async def get_media_list(self):
        """
        获取收藏夹列表信息，用于收藏操作，含各收藏夹对该视频的收藏状态。

        Returns:
            dict, 调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()

        info = await self.__get_info_cached()

        url = API["info"]["media_list"]["url"]
        params = {
            "type": 2,
            "rid": self.get_aid(),
            "up_mid": info["owner"]["mid"]
        }
        return await request("GET", url, params=params, credential=self.credential)

    async def get_danmaku_view(self, page_index: int):
        """
        获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。

        Args:
            page_index (int): 分 p 号，从 0 开始。

        Returns:
            dict, 调用 API 返回的结果。
        """

        session = get_session()
        api = API["danmaku"]["view"]['url']
        oid = await self.__get_page_id_by_index(page_index)
        resp = await session.get(api, params={
            "type": 1,
            "oid": oid,
            "pid": self.get_aid()
        }, cookies=self.credential.get_cookies(), headers={
            "Referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0"
        })

        try:
            resp.raise_for_status()
        except aiohttp.ClientResponseError as e:
            raise NetworkException(e.status, e.message)

        resp_data = await resp.read()
        json_data = {}
        reader = BytesReader(resp_data)
        # 解析二进制数据流

        def read_dm_seg(stream: bytes):
            reader_ = BytesReader(stream)
            data = {}
            while not reader_.has_end():
                t = reader_.byte() >> 3
                if t == 1:
                    data['page_size'] = reader_.varint()
                elif t == 2:
                    data['total'] = reader_.varint()
                else:
                    continue
            return data

        def read_flag(stream: bytes):
            reader_ = BytesReader(stream)
            data = {}
            while not reader_.has_end():
                t = reader_.byte() >> 3
                if t == 1:
                    data['rec_flag'] = reader_.varint()
                elif t == 2:
                    data['rec_text'] = reader_.string()
                elif t == 3:
                    data['rec_switch'] = reader_.varint()
                else:
                    continue
            return data

        def read_command_danmakus(stream: bytes):
            reader_ = BytesReader(stream)
            data = {}
            while not reader_.has_end():
                t = reader_.byte() >> 3
                if t == 1:
                    data['id'] = reader_.varint()
                elif t == 2:
                    data['oid'] = reader_.varint()
                elif t == 3:
                    data['mid'] = reader_.varint()
                elif t == 4:
                    data['commend'] = reader_.string()
                elif t == 5:
                    data['content'] = reader_.string()
                elif t == 6:
                    data['progress'] = reader_.varint()
                elif t == 7:
                    data['ctime'] = reader_.string()
                elif t == 8:
                    data['mtime'] = reader_.string()
                elif t == 9:
                    data['extra'] = json.loads(reader_.string())
                elif t == 10:
                    data['id_str'] = reader_.string()
                else:
                    continue
            return data

        def read_settings(stream: bytes):
            reader_ = BytesReader(stream)
            data = {}
            while not reader_.has_end():
                t = reader_.byte() >> 3

                if t == 1:
                    data['dm_switch'] = reader_.bool()
                elif t == 2:
                    data['ai_switch'] = reader_.bool()
                elif t == 3:
                    data['ai_level'] = reader_.varint()
                elif t == 4:
                    data['enable_top'] = reader_.bool()
                elif t == 5:
                    data['enable_scroll'] = reader_.bool()
                elif t == 6:
                    data['enable_bottom'] = reader_.bool()
                elif t == 7:
                    data['enable_color'] = reader_.bool()
                elif t == 8:
                    data['enable_special'] = reader_.bool()
                elif t == 9:
                    data['prevent_shade'] = reader_.bool()
                elif t == 10:
                    data['dmask'] = reader_.bool()
                elif t == 11:
                    data['opacity'] = reader_.float(True)
                elif t == 12:
                    data['dm_area'] = reader_.varint()
                elif t == 13:
                    data['speed_plus'] = reader_.float(True)
                elif t == 14:
                    data['font_size'] = reader_.float(True)
                elif t == 15:
                    data['screen_sync'] = reader_.bool()
                elif t == 16:
                    data['speed_sync'] = reader_.bool()
                elif t == 17:
                    data['font_family'] = reader_.string()
                elif t == 18:
                    data['bold'] = reader_.bool()
                elif t == 19:
                    data['font_border'] = reader_.varint()
                elif t == 20:
                    data['draw_type'] = reader_.string()
                else:
                    continue
            return data

        while not reader.has_end():
            type_ = reader.byte() >> 3

            if type_ == 1:
                json_data['state'] = reader.varint()
            elif type_ == 2:
                json_data['text'] = reader.string()
            elif type_ == 3:
                json_data['text_side'] = reader.string()
            elif type_ == 4:
                json_data['dm_seg'] = read_dm_seg(reader.bytes_string())
            elif type_ == 5:
                json_data['flag'] = read_flag(reader.bytes_string())
            elif type_ == 6:
                if 'special_dms' not in json_data:
                    json_data['special_dms'] = []
                json_data['special_dms'].append(reader.string())
            elif type_ == 7:
                json_data['check_box'] = reader.bool()
            elif type_ == 8:
                json_data['count'] = reader.varint()
            elif type_ == 9:
                if 'command_dms' not in json_data:
                    json_data['command_dms'] = []
                json_data['command_dms'].append(
                    read_command_danmakus(reader.bytes_string()))
            elif type_ == 10:
                json_data['dm_setting'] = read_settings(reader.bytes_string())
            else:
                continue
        return json_data

    async def get_danmakus(self, page_index: int, date: datetime.date = None):
        """
        获取弹幕。

        Args:
            page_index (int):                分 p 号，从 0 开始。
            data (datetime.Date, optional):  指定日期后为获取历史弹幕，精确到年月日。Defaults to None.

        Returns:
            list[Danmaku], Danmaku 类的列表。
        """

        if date is not None:
            self.credential.raise_for_no_sessdata()

        session = get_session()
        page_id = await self.__get_page_id_by_index(page_index)
        aid = self.get_aid()
        params = {
            "oid": page_id,
            "type": 1,
            "pid": aid
        }
        if date is not None:
            # 获取历史弹幕
            api = API["danmaku"]["get_history_danmaku"]
            params["date"] = date.strftime("%Y-%m-%d")
            params["type"] = 1
            # 仅需要获取一次
            sge_count = 1
        else:
            api = API["danmaku"]["get_danmaku"]
            params["segment_index"] = 1
            # view 信息
            view = await self.get_danmaku_view(page_index)
            sge_count = view['dm_seg']['total']

        # 循环获取所有 segment
        danmakus: list[Danmaku] = []
        for i in range(sge_count):
            if date is None:
                # 仅当获取当前弹幕时需要该参数
                params['segment_index'] = i + 1

            req = await session.get(api["url"], params=params, headers={
                "Referer": "https://www.bilibili.com",
                "User-Agent": "Mozilla/5.0"
            }, cookies=self.credential.get_cookies())
            try:
                req.raise_for_status()
            except aiohttp.ClientResponseError as e:
                raise NetworkException(e.status, e.message)

            content_type = req.headers['content-type']
            if content_type != 'application/octet-stream':
                raise ResponseException("返回数据类型错误：")

            # 解析二进制流数据
            data = await req.read()
            if data == b'\x10\x01':
                # 视频弹幕被关闭
                raise DanmakuClosedException()

            reader = BytesReader(data)
            while not reader.has_end():
                type_ = reader.byte() >> 3
                if type_ != 1:
                    raise ResponseException("解析响应数据错误")

                dm = Danmaku('')
                dm_pack_data = reader.bytes_string()
                dm_reader = BytesReader(dm_pack_data)

                while not dm_reader.has_end():
                    data_type = dm_reader.byte() >> 3

                    if data_type == 1:
                        dm.id = dm_reader.varint()
                    elif data_type == 2:
                        dm.dm_time = datetime.timedelta(
                            seconds=dm_reader.varint() / 1000)
                    elif data_type == 3:
                        dm.mode = dm_reader.varint()
                    elif data_type == 4:
                        dm.font_size = dm_reader.varint()
                    elif data_type == 5:
                        dm.color = Color()
                        dm.color.set_dec_color(dm_reader.varint())
                    elif data_type == 6:
                        dm.crc32_id = dm_reader.string()
                    elif data_type == 7:
                        dm.text = dm_reader.string()
                    elif data_type == 8:
                        dm.send_time = datetime.datetime.fromtimestamp(
                            dm_reader.varint())
                    elif data_type == 9:
                        dm.weight = dm_reader.varint()
                    elif data_type == 10:
                        dm.action = dm_reader.varint()
                    elif data_type == 11:
                        dm.pool = dm_reader.varint()
                    elif data_type == 12:
                        dm.id_str = dm_reader.string()
                    elif data_type == 13:
                        dm.attr = dm_reader.varint()
                    else:
                        break
                danmakus.append(dm)
        return danmakus

    async def get_history_danmaku_index(self, page_index: int, date: datetime.date):
        """
        获取特定月份存在历史弹幕的日期。

        Args:
            page_index (int):       分 P 号，从 0 开始。
            date (datetime.date):   精确到年月。

        Returns:
            None or list[str], 调用 API 返回的结果。不存在时为 None。
        """
        self.credential.raise_for_no_sessdata()

        page_id = self.__get_page_id_by_index(page_index)
        api = API["danmaku"]["get_history_danmaku_index"]
        params = {
            "oid": page_id,
            "month": date.strftime("%Y-%m"),
            "type": 1
        }
        return await request("GET", url=api["url"], params=params, credential=self.credential)

    async def has_liked_danmakus(self, page_index: int, ids: list[int]):
        """
        是否已点赞弹幕。

        Args:
            page_index (int):  分 P 号，从 0 开始。
            ids (list[int])：  要查询的弹幕 ID 列表。

        Returns:
            调用 API 返回的结果。
        """

        self.credential.raise_for_no_sessdata()
        page_id = self.__get_page_id_by_index(page_index)
        api = API["danmaku"]["has_liked_danmaku"]
        params = {
            "oid": page_id,
            "ids": ','.join(ids)
        }
        return await request("GET", url=api["url"], params=params, credential=self.credential)

    async def send_danmaku(self, page_index: int, danmaku: Danmaku):
        """
        发送弹幕。

        Args:
            page_index (int):   分 P 号，从 0 开始。
            danmaku (Danmaku):  Danmaku 类。

        Returns:
            调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["danmaku"]["send_danmaku"]
        oid = await self.__get_page_id_by_index(page_index)
        if danmaku.is_sub:
            pool = 1
        else:
            pool = 0
        data = {
            "type": 1,
            "oid": oid,
            "msg": danmaku.text,
            "aid": self.get_aid(),
            "bvid": self.get_bvid(),
            "progress": int(danmaku.dm_time.seconds * 1000),
            "color": danmaku.color.get_dec_color(),
            "fontsize": danmaku.font_size,
            "pool": pool,
            "mode": danmaku.mode,
            "plat": 1
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)

    async def like_danmaku(self, page_index: int, dmid: int, status: bool = True):
        """
        点赞弹幕。

        Args:
            page_index (int):          分 P 号，从 0 开始。
            dmid (int):                弹幕 ID。
            status (bool, optional):   点赞状态。Defaults to True.

        Returns:
            调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["danmaku"]["like_danmaku"]
        page_id = await self.__get_page_id_by_index(page_index)
        data = {
            "dmid": dmid,
            "oid": page_id,
            "op": 1 if status else 2,
            "platform": "web_player"
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)

    async def like(self, status: bool = True):
        """
        点赞视频。

        Args:
            status (bool, optional): 点赞状态。Defaults to True.

        Returns:
            调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["like"]
        data = {
            "aid": self.get_aid(),
            "like": 1 if status else 2
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)

    async def pay_coin(self, num: int = 1, like: bool = False):
        """
        投币。

        Args:
            num (int, optional):    硬币数量，为 1 ~ 2 个。Defaults to 1.
            like (bool, optional):  是否同时点赞。Defaults to False.

        Returns:
            调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        if num not in (1, 2):
            raise ArgsException("投币数量只能是 1 ~ 2 个。")

        api = API["operate"]["coin"]
        data = {
            "aid": self.get_aid(),
            "bvid": self.get_bvid(),
            "multiply": num,
            "like": 1 if like else 0
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)

    async def add_tag(self, name: str):
        """
        加标签。

        Args:
            name (str): 标签名字。

        Returns:
            调用 API 返回的结果。会返回标签 ID。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["add_tag"]
        data = {
            "aid": self.get_aid(),
            "bvid": self.get_bvid(),
            "tag_name": name
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)

    async def delete_tag(self, tag_id: int):
        """
        删除标签。

        Args:
            tag_id (int): 标签 ID。

        Returns:
            调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["del_tag"]

        data = {
            "tag_id": tag_id,
            "aid": self.get_aid(),
            "bvid": self.get_bvid()
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)

    async def subscribe_tag(self, tag_id: int):
        """
        关注标签。

        Args:
            tag_id (int): 标签 ID。

        Returns:
            调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["subscribe_tag"]

        data = {
            "tag_id": tag_id
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)

    async def unsubscribe_tag(self, tag_id: int):
        """
        取关标签。

        Args:
            tag_id (int): 标签 ID。

        Returns:
            调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["unsubscribe_tag"]

        data = {
            "tag_id": tag_id
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)
