"""
bilibili_api.video

视频相关操作
"""

from copy import copy
from enum import Enum
from typing import Coroutine
import aiohttp
import re
import json
import datetime
import asyncio
import aiohttp
import logging
import json
import struct
import io
import base64
from typing import List

from .exceptions import VideoUploadException
from .exceptions import ResponseException
from .exceptions import NetworkException
from .exceptions import ArgsException, DanmakuClosedException

from .utils.Credential import Credential
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.utils import get_api
from .utils.network import request, get_session
from .utils.Danmaku import Danmaku
from .utils.Color import Color
from .utils.BytesReader import BytesReader
from .utils.AsyncEvent import AsyncEvent

API = get_api("video")


class Video:
    """
    视频类，各种对视频的操作均在里面。
    """

    def __init__(self, bvid: str = None, aid: int = None, credential: Credential = None):
        """
        Args:
            bvid       (str, optional)       : BV 号. bvid 和 aid 必须提供其中之一。
            aid        (int, optional)       : AV 号. bvid 和 aid 必须提供其中之一。
            credential (Credential, optional): Credential 类. Defaults to None.
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
            str: BVID。
        """
        return self.__bvid

    def set_aid(self, aid: int):
        """
        设置 aid。

        Args:
            aid (int): AV 号。
        """
        if aid <= 0:
            raise ArgsException("aid 不能小于或等于 0。")

        self.__aid = aid
        self.__bvid = aid2bvid(aid)

    def get_aid(self):
        """
        获取 AID。

        Returns:
            int: aid。
        """
        return self.__aid

    async def get_info(self):
        """
        获取视频信息。

        Returns:
            dict: 调用 API 返回的结果。
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
            dict: 调用 API 返回的结果。
        """
        if self.__info is None:
            return await self.get_info()
        return self.__info

    async def get_stat(self):
        """
        获取视频统计数据（播放量，点赞数等）。

        Returns:
            dict: 调用 API 返回的结果。
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
            dict: 调用 API 返回的结果。
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
            dict: 调用 API 返回的结果。
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
            dict: 调用 API 返回的结果。
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
            int: 分 P 的唯一 ID。
        """
        if page_index < 0:
            raise ArgsException("分 p 号必须大于或等于 0。")

        info = await self.__get_info_cached()
        pages = info["pages"]

        if len(pages) <= page_index:
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
            dict: 调用 API 返回的结果。
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
            dict: 调用 API 返回的结果。
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
            bool: 视频是否点赞过。
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
            int: 视频已投币数量。
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
            bool: 视频是否已收藏。
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
            dict: 调用 API 返回的结果。
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
            dict: 调用 API 返回的结果。
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
            page_index (int)                    : 分 p 号，从 0 开始。
            data       (datetime.Date, optional): 指定日期后为获取历史弹幕，精确到年月日。Defaults to None.

        Returns:
            List[Danmaku]: Danmaku 类的列表。
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
        danmakus: List[Danmaku] = []
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
            page_index (int)          : 分 P 号，从 0 开始。
            date       (datetime.date): 精确到年月。

        Returns:
            None | List[str]: 调用 API 返回的结果。不存在时为 None。
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

    async def has_liked_danmakus(self, page_index: int, ids: List[int]):
        """
        是否已点赞弹幕。

        Args:
            page_index (int)      : 分 P 号，从 0 开始。
            ids        (List[int]): 要查询的弹幕 ID 列表。

        Returns:
            dict: 调用 API 返回的结果。
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
            page_index (int)    : 分 P 号，从 0 开始。
            danmaku    (Danmaku): Danmaku 类。

        Returns:
            dict: 调用 API 返回的结果。
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
            "fontsize": danmaku.font_size.value,
            "pool": pool,
            "mode": danmaku.mode.value,
            "plat": 1
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)

    async def like_danmaku(self, page_index: int, dmid: int, status: bool = True):
        """
        点赞弹幕。

        Args:
            page_index (int)           : 分 P 号，从 0 开始。
            dmid       (int)           : 弹幕 ID。
            status     (bool, optional): 点赞状态。Defaults to True.

        Returns:
            dict: 调用 API 返回的结果。
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
            dict: 调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata
        self.credential.raise_for_no_bili_jct()
        self.credential.raise_for_no_buvid3()

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
            num  (int, optional) : 硬币数量，为 1 ~ 2 个。Defaults to 1.
            like (bool, optional): 是否同时点赞。Defaults to False.

        Returns:
            dict: 调用 API 返回的结果。
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
            dict: 调用 API 返回的结果。会返回标签 ID。
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
            dict: 调用 API 返回的结果。
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
            dict: 调用 API 返回的结果。
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
            dict: 调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["unsubscribe_tag"]

        data = {
            "tag_id": tag_id
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)

    async def set_favorite(self, add_media_ids: List[int] = [], del_media_ids: List[int] = []):
        """
        设置视频收藏状况。

        Args:
            add_media_ids (List[int], optional): 要添加到的收藏夹 ID. Defaults to [].
            del_media_ids (List[int], optional): 要移出的收藏夹 ID. Defaults to [].

        Returns:
            dict: 调用 API 返回结果。
        """
        if len(add_media_ids) + len(del_media_ids) == 0:
            raise ArgsException(
                "对收藏夹无修改。请至少提供 add_media_ids 和 del_media_ids 中的其中一个。")

        api = API["operate"]["favorite"]
        data = {
            "rid": self.get_aid(),
            "type": 2,
            "add_media_ids": ",".join(map(lambda x: str(x), add_media_ids)),
            "del_media_ids": ",".join(map(lambda x: str(x), del_media_ids)),
        }
        return await request("POST", url=api["url"], data=data, credential=self.credential)


class VideoOnlineMonitor(AsyncEvent):
    """
    视频在线人数实时监测。

    示例代码：

    ```python
        import asyncio
        from bilibili_api import video

        # 实例化
        r = video.VideoOnlineMonitor("BV1Bf4y1Q7QP")

        # 装饰器方法注册事件监听器
        @r.on("ONLINE")
        async def handler(data):
            print(data)

        # 函数方法注册事件监听器
        async def handler2(data):
            print(data)

        r.add_event_listener("ONLINE", handler2)

        asyncio.get_event_loop().run_until_complete(r.connect())

    ```

    Extends: AsyncEvent

    Events:
        ONLINE：        在线人数更新。  CallbackData: dict。
        DANMAKU：       收到实时弹幕。  CallbackData: Danmaku。
        DISCONNECTED：  正常断开连接。  CallbackData: None。
        ERROR:          发生错误。     CallbackData: aiohttp.ClientWebSocketResponse。
        CONNECTED:      成功连接。     CallbackData: None。
    """

    class Datapack(Enum):
        """
        数据包类型枚举。

        + CLIENT_VERIFY   : 客户端发送验证信息。
        + SERVER_VERIFY   : 服务端响应验证信息。
        + CLIENT_HEARTBEAT: 客户端发送心跳包。
        + SERVER_HEARTBEAT: 服务端响应心跳包。
        + DANMAKU         : 实时弹幕更新。
        """
        CLIENT_VERIFY = 0x7
        SERVER_VERIFY = 0x8
        CLIENT_HEARTBEAT = 0x2
        SERVER_HEARTBEAT = 0x3
        DANMAKU = 0x3e8

    def __init__(self,
                 bvid: str = None,
                 aid: int = None,
                 page_index: int = 0,
                 credential: Credential = None,
                 debug: bool = False):
        """
        Args:
            bvid       (str, optional)       : BVID. Defaults to None.
            aid        (int, optional)       : AID. Defaults to None.
            page_index (int, optional)       : 分 P 序号. Defaults to 0.
            credential (Credential, optional): Credential 类. Defaults to None.
            debug      (bool, optional)      : 调试模式，将输出更详细信息. Defaults to False.
        """
        super().__init__()
        self.credential = credential
        self.__video = Video(bvid, aid, credential=credential)

        # 智能选择在 log 中展示的 ID。
        id_showed = None
        if bvid is not None:
            id_showed = bvid
        else:
            id_showed = aid

        # logger 初始化
        self.logger = logging.getLogger(f'VideoOnlineMonitor-{id_showed}')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "[" + str(id_showed) + "][%(asctime)s][%(levelname)s] %(message)s"))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO if not debug else logging.DEBUG)

        self.__page_index = page_index
        self.__tasks = []

    async def connect(self):
        """
        连接服务器
        """
        await self.__main()

    async def disconnect(self):
        """
        断开服务器
        """
        self.logger.info("主动断开连接。")
        self.dispatch("DISCONNECTED")
        await self.__cancel_all_tasks()
        await self.__ws.close()

    async def __main(self):
        """
        入口。
        """
        # 获取分 P id
        pages = await self.__video.get_pages()
        if self.__page_index >= len(pages):
            raise ArgsException("不存在该分 P。")
        cid = pages[self.__page_index]['cid']

        # 获取服务器信息
        self.logger.debug(f'准备连接：{self.__video.get_bvid()}')
        self.logger.debug(f'获取服务器信息中...')
        resp = await request(
            'GET',
            'https://api.bilibili.com/x/web-interface/broadcast/servers?platform=pc',
            credential=self.credential)

        uri = f"wss://{resp['domain']}:{resp['wssPort']}/sub"
        self.__heartbeat_interval = resp['heartbeat']
        self.logger.debug(f'服务器信息获取成功，URI：{uri}')

        # 连接服务器
        self.logger.debug('准备连接服务器...')
        session = get_session()
        async with session.ws_connect(uri) as ws:
            self.__ws = ws

            # 发送认证信息
            self.logger.debug('服务器连接成功，准备发送认证信息...')
            verify_info = {
                'room_id': f'video://{self.__video.get_aid()}/{cid}',
                'platform': 'web',
                'accepts': [1000, 1015]
            }
            verify_info = json.dumps(verify_info, separators=(',', ':'))
            await ws.send_bytes(self.__pack(VideoOnlineMonitor.Datapack.CLIENT_VERIFY, 1, verify_info.encode()))

            # 循环接收消息
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.BINARY:
                    data = self.__unpack(msg.data)
                    self.logger.debug(f'收到消息：{data}')
                    await self.__handle_data(data)

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    self.logger.warning('连接被异常断开')
                    await self.__cancel_all_tasks()
                    self.dispatch("ERROR", msg)
                    break

    async def __handle_data(self, data: List[dict]):
        """
        处理数据。

        Args:
            data (List[dict]): 收到的数据（已解析好）。
        """
        for d in data:
            if d['type'] == VideoOnlineMonitor.Datapack.SERVER_VERIFY.value:
                # 服务器认证反馈。
                if d['data']['code'] == 0:
                    # 创建心跳 Task
                    heartbeat = asyncio.create_task(
                        self.__heartbeat_task())
                    self.__tasks.append(heartbeat)

                    self.logger.info('连接服务器并验证成功')

            elif d['type'] == VideoOnlineMonitor.Datapack.SERVER_HEARTBEAT.value:
                # 心跳包反馈，同时包含在线人数。
                self.logger.debug(f'收到服务器心跳包反馈，编号：{d["number"]}')
                self.logger.info(
                    f'实时观看人数：{d["data"]["data"]["room"]["online"]}')
                self.dispatch("ONLINE", d["data"])

            elif d['type'] == VideoOnlineMonitor.Datapack.DANMAKU.value:
                # 实时弹幕。
                info = d['data'][0].split(",")
                text = d['data'][1]
                if info[5] == '0':
                    is_sub = False
                else:
                    is_sub = True
                dm = Danmaku(
                    dm_time=float(info[0]),
                    send_time=int(info[4]),
                    crc32_id=info[6],
                    color=Color(info[3]),
                    mode=info[1],
                    font_size=info[2],
                    is_sub=is_sub,
                    text=text
                )
                self.logger.info(f'收到实时弹幕：{dm.text}')
                self.dispatch("DANMAKU", dm)

            else:
                # 未知类型数据包
                self.logger.warning('收到未知的数据包类型，无法解析：' + json.dumps(d))

    async def __heartbeat_task(self):
        """
        心跳 Task。
        """
        index = 2
        while True:
            self.logger.debug(f'发送心跳包，编号：{index}')
            await self.__ws.send_bytes(self.__pack(VideoOnlineMonitor.Datapack.CLIENT_HEARTBEAT, index, b'[object Object]'))
            index += 1
            await asyncio.sleep(self.__heartbeat_interval)

    async def __cancel_all_tasks(self):
        """
        取消所有 Task。
        """
        for task in self.__tasks:
            task.cancel()

    @staticmethod
    def __pack(data_type: Datapack, number: int, data: bytes):
        """
        打包数据。

        # 数据包格式：

        16B 头部:

        | offset(bytes) | length(bytes) | type | description         |
        | ------------- | ------------- | ---- | ------------------- |
        | 0             | 4             | I    | 数据包长度           |
        | 4             | 4             | I    | 固定0x00120001      |
        | 8             | 4             | I    | 数据包类型           |
        | 12            | 4             | I    | 递增数据包编号        |
        | 16            | 2             | H    | 固定0x0000           |

        之后是有效载荷。

        # 数据包类型表：

        + 0x7    客户端发送认证信息
        + 0x8    服务端回应认证结果
        + 0x2    客户端发送心跳包，有效载荷：'[object Object]'
        + 0x3    服务端回应心跳包，会带上在线人数等信息，返回JSON
        + 0x3e8  实时弹幕更新，返回列表，[0]弹幕信息，[1]弹幕文本

        Args:
            data_type (VideoOnlineMonitor.DataType):  数据包类型枚举。

        Returns:
            bytes: 打包好的数据。
        """
        packed_data = bytearray()
        packed_data += struct.pack('>I', 0x00120001)
        packed_data += struct.pack('>I', data_type.value)
        packed_data += struct.pack('>I', number)
        packed_data += struct.pack('>H', 0)
        packed_data += data
        packed_data = struct.pack('>I', len(packed_data) + 4) + packed_data
        return bytes(packed_data)

    @staticmethod
    def __unpack(data: bytes):
        """
        解包数据。

        Args:
            data (bytes):  原始数据。

        Returns:
            tuple(dict): 解包后的数据。
        """
        offset = 0
        real_data = []
        while offset < len(data):
            region_header = struct.unpack('>IIII', data[:16])
            region_data = data[offset:offset+region_header[0]]
            real_data.append({
                'type': region_header[2],
                'number': region_header[3],
                'data': json.loads(region_data[offset+18:offset+18+(region_header[0]-16)])
            })
            offset += region_header[0]
        return tuple(real_data)


class VideoUploaderPageObject:
    """
    分 P 对象。
    """

    def __init__(self, video_stream: io.BufferedIOBase, title: str, description: str = ""):
        """
        Args:
            video_stream (io.BufferedIOBase): 分 P 视频流。可以是 open() 返回的 FileIO 对象。
            title        (str)              : 分 P 标题。
            description  (str, optional)    : 分 P 描述. Defaults to "".
        """
        self.stream = video_stream
        self.title = title
        self.description = description
        self.__total_size = None

    def get_total_size(self):
        """
        获取总大小。

        Returns:
            int: 文件总大小。
        """
        if self.__total_size is None:
            self.__total_size = len(self.stream.read())
        return self.__total_size


class VideoUploader(AsyncEvent):
    """
    视频上传。任何上传中的出错将会直接抛出错误并终止上传。

    Events:
        COVER_SUCCESS   封面上传成功。CallbackData：封面 URL。
        BEGIN           开始上传分 P。CallbackData：VideoUploaderPageObject
        CHUNK_BEGIN     开始上传分 P 分块。
                        CallbackData：
                            VideoUploaderPageObject,
                            {
                                "chunk_index": "int: 分块编号",
                                "total_chunk": "int: 总共有多少个分块",
                                "start": "int: 该 chunk 数据开始位置",
                                "end": "int: 该 chunk 数据结束位置"
                            }
        CHUNK_END       分块上传结束。CallbackData：VideoUploaderPageObject
        END             分 P 上传结束。CallbackData：VideoUploaderPageObject
    """

    def __init__(self,
                 cover: io.BufferedIOBase,
                 cover_type: str,
                 pages: List[VideoUploaderPageObject],
                 config: dict,
                 credential: Credential):
        """
        Args:
            cover      (io.BufferedIOBase)            : 封面 io 类，比如调用 open() 打开文件后的返回值。
            cover_type (str)                          : 封面数据 MIME 类型。常见类型对照 jpg: image/jpeg, png: image/png
            pages      (List[VideoUploaderPageObject]): 分 P 视频列表。
            config     (dict)                         : 设置，格式参照 self.set_config()
            credential (Credential)                   : Credential 类。
        """
        super().__init__()
        self.cover = cover
        self.cover_type = cover_type
        self.pages = pages
        self.__config = {}
        self.__session = get_session()
        self.credential = credential

        credential.raise_for_no_sessdata()
        credential.raise_for_no_bili_jct()

        self.set_config(config)

    def set_config(self, config: dict):
        """
        设置上传配置。

        不可设置的参数：cover, videos。

        参考如下：

        ```json
        {
            "copyright": "int, 投稿类型。1 自制，2 转载。",
            "source": "str, 视频来源。投稿类型为转载时注明来源，为原创时为空。",
            "cover": "str, 封面 URL。。",
            "desc": "str, 视频简介。",
            "desc_format_id": 0,
            "dynamic": "str, 动态信息。",
            "interactive": 0,
            "open_elec": "int, 是否展示充电信息。1 为是，0 为否。",
            "no_reprint": "int, 显示未经作者授权禁止转载，仅当为原创视频时有效。1 为启用，0 为关闭。",
            "subtitles": {
                "lan": "字幕语言，不清楚作用请将该项设置为空",
                "open": 0
            },
            "tag": "str, 视频标签。使用英文半角逗号分隔的标签组。示例：标签1,标签2,标签3",
            "tid": "int, 分区ID。可以使用 channel 模块进行查询。",
            "title": "视频标题",
            "up_close_danmaku": "bool, 是否关闭弹幕。",
            "up_close_reply": "bool, 是否关闭评论。",
            "videos": [
                {
                    "desc": "str, 分 P 描述。",
                    "filename": "str, 视频上传后的文件名。",
                    "title": "str, 分 P 标题"
                }
            ]
        }
        ```

        Args:
            config (dict): 上传配置
        """
        if any(["videos" in config, "cover" in config]):
            raise ArgsException("不可手动设置参数：cover, videos。将会自动设置。")
        self.__config = copy(config)

    def get_config(self):
        """
        获取配置。

        Returns:
            dict: 视频配置。
        """
        return copy(self.__config)

    async def start(self):
        """
        开始上传。

        Returns:
            dict: 包含 bvid 和 aid 的字典。
        """
        # 上传封面
        cover_info = await self.__upload_cover()
        cover_url = cover_info["url"]
        self.dispatch("COVER_SUCCESS", cover_url)

        # 上传视频
        videos = []
        for page in self.pages:
            filename = await self.__upload_video(page)
            videos.append({
                "filename": filename,
                "page": page
            })

        # 提交视频
        result = await self.__submit(cover_url, videos)
        return result

    async def __submit(self, cover: str, videos: list):
        """
        提交视频。

        Args:
            cover  (str) : 封面 URL。
            videos (list): 要提交的视频，格式参照 self.start() 中的代码。

        Returns:
            dict: 包含 bvid 和 aid 的字典。
        """
        config = copy(self.__config)
        config["cover"] = cover
        config["videos"] = []
        for video in videos:
            v = {
                "desc": video["page"].description,
                "title": video["page"].title,
                "filename": video["filename"],
                "cid": 0
            }
            config["videos"].append(v)
        data = config
        params = {
            "csrf": self.credential.bili_jct
        }
        return await request("POST", "https://member.bilibili.com/x/vu/web/add",
                             data=data,
                             params=params,
                             credential=self.credential,
                             no_csrf=True,
                             json_body=True)

    async def __upload_cover(self):
        """
        上传视频封面。

        Returns:
            str: 封面 URL。
        """
        b64 = base64.b64encode(self.cover.read())
        data_url = f"data:{self.cover_type};base64,{b64.decode()}"
        payload = {
            "cover": data_url
        }
        return await request("POST", "https://member.bilibili.com/x/vu/web/cover/up", data=payload, credential=self.credential)

    async def __upload_video(self, page: VideoUploaderPageObject):
        """
        上传视频。

        Args:
            page (VideoUploaderPageObject): VideoUploaderPageObject。

        Returns:
            str: filename，用于最后提交视频。
        """
        self.dispatch("BEGIN", page)
        # 获取上传信息
        upload_info = await self.__get_upload_info(page)
        # 最大并发数
        threads = upload_info["threads"]
        # chunk 大小
        chunk_size = upload_info["chunk_size"]
        # X-Upos-Auth 头内容
        auth = upload_info["auth"]
        # 上传节点
        endpoint = upload_info["endpoint"]
        # 上传 URL
        url = f"https:{endpoint}/{upload_info['upos_uri'][7:]}"
        # 文件名
        filename = upload_info["upos_uri"][7:].split("/")[1]
        # 其他后面会用到的
        biz_id = upload_info["biz_id"]

        # 获取 upload_id
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://member.bilibili.com",
            "X-Upos-Auth": auth,
        }
        async with self.__session.post(
                url=url,
                params={"uploads": "", "output": "json"},
                headers=headers,
                cookies=self.credential.get_cookies()) as resp:

            data = await resp.read()
            data = json.loads(data)
            upload_id = data["upload_id"]

        # 分配任务
        total_size = page.get_total_size()
        # 计算每 chunk 开始位置
        chunk_offsets = list(range(0, total_size, chunk_size))
        # 总 chunk 数量
        total_chunks_count = len(chunk_offsets)
        # 初始化 chunk
        chunks = []
        remain_size = total_size
        for i, offset in enumerate(chunk_offsets):
            length = chunk_size if remain_size > chunk_size else remain_size
            chunks.append(self.__upload_chunk(offset, length, total_size,
                                              total_chunks_count, page.stream,
                                              url, auth, i, upload_id, page))
            remain_size -= length

        # 分配并发线程
        tasks = []
        if len(chunks) <= threads:
            # chunks 长度比最大并发数小或相等
            for chunk in chunks:
                tasks.append(self.__task([chunk]))
        else:
            # chunks 长度比最大并发数大
            chunks_of_every_tasks: List[List[Coroutine]] = []
            for i in range(threads):
                chunks_of_every_tasks.append([])
            i = 0
            for chunk in chunks:
                # 平均打散到每个 Task
                chunks_of_every_tasks[i].append(chunk)
                i += 1
                if i >= threads:
                    i = 0
            for c in chunks_of_every_tasks:
                tasks.append(self.__task(c))

        # 开始上传
        await asyncio.gather(*tasks)

        # 确认是否上传成功
        params = {
            "output": "json",
            "name": page.title,
            "profile": "ugcupos/bup",
            "uploadId": upload_id,
            "biz_id": biz_id
        }
        data = {
            "parts": []
        }
        for i in range(total_chunks_count):
            data["parts"].append({
                "eTag": "etag",
                "partNumber": i + 1
            })
        headers.update({
            "Content-Type": "application/json"
        })
        async with self.__session.post(
                url=url,
                params=params,
                data=json.dumps(data),
                headers=headers,
                cookies=self.credential.get_cookies()) as resp:

            data = await resp.read()
            data = json.loads(data)
            if data["OK"] != 1:
                raise VideoUploadException("上传失败")
        self.dispatch("END", page)
        return filename

    async def __task(self, chunks: List[Coroutine]):
        """
        按顺序执行 chunk coroutine.

        Args:
            chunks (List[Coroutine]): Coroutine
        """
        for chunk in chunks:
            await chunk

    async def __upload_chunk(self,
                             start: int,
                             length: int,
                             total_size: int,
                             total_chunks_count: int,
                             stream: io.BufferedIOBase,
                             url: str,
                             auth: str,
                             index: int,
                             upload_id: str,
                             page: VideoUploaderPageObject
                             ):
        """
        上传分块。

        Args:
            start              (int)                    : 起始位置。
            length             (int)                    : 长度。
            total_size         (int)                    : 视频总大小。
            total_chunks_count (int)                    : 总共分块数量。
            stream             (io.BufferedIOBase)      : IO 流。
            url                (str)                    : 上传 URL。
            auth               (str)                    : X-Upos-Auth 头内容。
            index              (int)                    : 分块序号。
            upload_id          (str)                    : upload_id。
            page               (VideoUploaderPageObject): VideoUploaderPageObject
        """
        callback_data = {
            "chunk_index": index + 1,
            "total_chunk": total_chunks_count,
            "start": start,
            "end": start + length
        }
        self.dispatch("CHUNK_BEGIN", page, callback_data)
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://member.bilibili.com",
            "X-Upos-Auth": auth,
        }

        params = {
            "partNumber": index + 1,
            "uploadId": upload_id,
            "chunk": index,
            "chunks": total_chunks_count,
            "size": length,
            "start": start,
            "end": start + length,
            "total": total_size
        }
        stream.seek(start)
        async with self.__session.put(
                url=url,
                headers=headers,
                params=params,
                data=stream.read(length),
                cookies=self.credential.get_cookies()) as resp:

            await resp.wait_for_close()
        self.dispatch("CHUNK_END", page, callback_data)

    async def __get_upload_info(self, page_object: VideoUploaderPageObject):
        """
        获取上传信息。

        Args:
            page_object (VideoUploaderPageObject): VideoUploaderPageObject。
        """
        params = {
            "name": page_object.title,
            "size": page_object.get_total_size(),
            "r": "upos",
            "profile": "ugcupos/bup",
            "ssl": 0,
            "version": "2.8.12",
            "build": 2081200,
            "upcdn": "bda2",
            "probe_version": 20200810
        }
        page_object.stream.seek(0)
        async with self.__session.get(
            "https://member.bilibili.com/preupload",
            params=params,
            cookies=self.credential.get_cookies(),
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://www.bilibili.com"
            }
        ) as resp:
            data = await resp.json()
            if data["OK"] != 1:
                raise VideoUploadException("获取上传信息失败：" + str(data))
            return data
