"""
bilibili_api.video

视频相关操作
"""

from v5.exceptions.ApiCodeException import ApiCodeException
import aiohttp
from v5.exceptions.NetworkException import NetworkException
from .utils.Credential import Credential
from .exceptions import ArgsException, DanmakuClosedException
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.utils import get_api
from .utils.network import request, get_session
from .utils.Danmaku import Danmaku
from .utils.varint import read_varint
from .utils.Color import Color
import re
import json
import struct
import datetime

API = get_api("video")


class Video:
    """
    视频类，各种对视频的操作均在里面
    """
    def __init__(self, bvid: str = None, aid: int = None, credential: Credential = None):
        """
        :param bvid: BV号，以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）
        :param aid: AV号，大于 0 的整数（若已提供 bvid 则该参数无效）
        :param credential: Credential 类，用于一些操作的凭据认证
        """
        # ID 检查
        if bvid is not None:
            self.set_bvid(bvid)
        elif aid is not None:
            self.set_aid(aid)
        else:
            # 未提供任一 ID
            raise ArgsException("请至少提供 bvid 和 aid 中的其中一个参数")

        # 未提供 credential 时初始化该类
        if credential is None:
            self.credential = Credential()

        # 用于存储视频信息，避免接口依赖视频信息时重复调用
        self.__info = None

    def set_bvid(self, bvid: str):
        """
        设置 BVID

        :param bvid: 以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）
        :type bvid: str
        :raises ArgsException: BVID 不正确
        """
        # 检查 bvid 是否有效
        if not re.search("^BV[a-zA-Z0-9]{10}$", bvid):
            raise ArgsException("bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）")
        self.__bvid = bvid
        self.__aid = bvid2aid(self.bvid)

    def get_bvid(self):
        """
        获取 BVID

        :return: BVID
        :rtype: str
        """
        return self.__bvid

    def set_aid(self, aid: int):
        """
        设置 AID

        :param aid: 大于 0 的整数
        :type aid: int
        :raises ArgsException: aid 错误
        """
        if aid <= 0:
            raise ArgsException("aid 不能小于或等于 0")
        self.__aid = aid
        self.__bvid = aid2bvid(aid)

    def get_aid(self):
        """
        获取 AID

        :return: aid
        :rtype: int
        """
        return self.__aid

    async def get_info(self):
        """
        获取视频信息
        """
        url = API["info"]["detail"]["url"]
        params = {
            "bvid": self.__bvid,
            "aid": self.__aid
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        # 存入 self.__info 中以备后续调用
        self.__info = resp
        return resp

    async def __get_info_cached(self):
        """
        获取视频信息，如果已获取过则使用之前获取的信息，没有则重新获取
        """
        if self.__info is None:
            return await self.get_info()
        else:
            return self.__info

    async def get_stat(self):
        """
        获取视频统计数据（播放量，点赞数等）
        """
        url = API["info"]["stat"]["url"]
        params = {
            "bvid": self.__bvid,
            "aid": self.__aid
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        return resp

    async def get_tags(self):
        """
        获取视频标签
        """
        url = API["info"]["tags"]["url"]
        params = {
            "bvid": self.__bvid,
            "aid": self.__aid
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        return resp

    async def get_chargers(self):
        """
        获取视频充电用户
        """
        info = await self.__get_info_cached()
        mid = info["owner"]["mid"]
        url = API["info"]["chargers"]["url"]
        params = {
            "aid": self.__aid,
            "bvid": self.__bvid,
            "mid": mid
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        return resp

    async def get_pages(self):
        """
        获取分 P 信息
        """
        url = API["info"]["pages"]["url"]
        params = {
            "aid": self.__aid,
            "bvid": self.__bvid
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        return resp

    async def __get_pages_id_by_index(self, page_index: int):
        """
        根据分 p 号获取 page_id

        :param page_index: 分 p 号
        :type page_index: int
        :return: 分 p 号
        :rtype: int
        """
        if page_index < 0:
            raise ArgsException("分 p 号必须大于或等于 0")

        info = await self.__get_info_cached()
        pages = info["pages"]

        if len(pages) >= page_index:
            raise ArgsException("不存在该分 p")
        cid = pages[page_index]["cid"]
        return cid

    async def get_download_url(self, page_index: int):
        """
        获取视频下载信息

        :param page_index: 分 P 号，下标从 0 开始
        """
        cid = await self.__get_pages_id_by_index(page_index)

        url = API["info"]["playurl"]["url"]
        params = {
            "avid": self.__aid,
            "cid": cid,
            "qn": "120",
            "otype": "json",
            "fnval": 16
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        return resp

    async def get_related(self):
        """
        获取相关视频信息
        """
        url = API["info"]["related"]["url"]
        params = {
            "aid": self.__aid,
            "bvid": self.__bvid
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        return resp

    async def has_liked(self):
        """
        视频是否点赞过

        :return: bool
        """
        self.credential.raise_for_no_sessdata()

        url = API["info"]["has_liked"]["url"]
        params = {
            "bvid": self.__bvid,
            "aid": self.__aid
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        return resp == 1
        
    async def get_pay_coins(self):
        """
        获取视频已投币数量

        :return: int
        """
        self.credential.raise_for_no_sessdata()

        url = API["info"]["get_pay_coins"]["url"]
        params = {
            "bvid": self.__bvid,
            "aid": self.__aid
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        return resp["multiply"]

    async def has_favoured(self):
        """
        是否已收藏

        :return: bool
        """
        self.credential.raise_for_no_sessdata()

        url = API["info"]["has_favoured"]["url"]
        params = {
            "bvid": self.__bvid,
            "aid": self.__aid
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        return resp["favoured"]

    async def get_media_list(self):
        """
        获取收藏夹列表信息，用于收藏操作，含各收藏夹对该视频的收藏状态
        """
        self.credential.raise_for_no_sessdata()

        info = self.__get_info_cached()

        url = API["info"]["media_list"]["url"]
        params = {
            "type": 2,
            "rid": self.__aid,
            "up_mid": info["owner"]["mid"]
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        return resp["favoured"]

    async def get_danmaku_view(self, page_index: int):
        """
        获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息
        :param page_id: 分 p 号
        :return:
        """

        session = get_session()
        api = API["video"]["danmaku"]["view"]['url']
        oid = await self.__get_pages_id_by_index(page_index)
        resp = await session.get(api, params={
            "type": 1,
            "oid": oid,
            "pid": self.__aid
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
        pos = 0
        length = len(resp_data)
        # 解析二进制数据流

        def read_dmSge(stream: bytes):
            length_ = len(stream)
            pos = 0
            data = {}
            while pos < length_:
                t = stream[pos] >> 3
                pos += 1
                if t == 1:
                    d, l = read_varint(stream[pos:])
                    data['pageSize'] = int(d)
                    pos += l
                elif t == 2:
                    d, l = read_varint(stream[pos:])
                    data['total'] = int(d)
                    pos += l
                else:
                    continue
            return data

        def read_flag(stream: bytes):
            length_ = len(stream)
            pos = 0
            data = {}
            while pos < length_:
                t = stream[pos] >> 3
                pos += 1
                if t == 1:
                    d, l = read_varint(stream[pos:])
                    data['recFlag'] = int(d)
                    pos += l
                elif t == 2:
                    str_len, l = read_varint(stream[pos:])
                    pos += l
                    data['recText'] = stream[pos: pos + str_len].decode()
                    pos += str_len
                elif t == 3:
                    d, l = read_varint(stream[pos:])
                    data['recSwitch'] = int(d)
                    pos += l
                else:
                    continue
            return data

        def read_commandDms(stream: bytes):
            length_ = len(stream)
            pos = 0
            data = {}
            while pos < length_:
                t = stream[pos] >> 3
                pos += 1
                if t == 1:
                    d, l = read_varint(stream[pos:])
                    data['id'] = int(d)
                    pos += l
                elif t == 2:
                    d, l = read_varint(stream[pos:])
                    data['oid'] = int(d)
                    pos += l
                elif t == 3:
                    d, l = read_varint(stream[pos:])
                    data['mid'] = int(d)
                    pos += l
                elif t == 4:
                    str_len, l = read_varint(stream[pos:])
                    pos += l
                    data['commend'] = stream[pos: pos + str_len].decode()
                    pos += str_len
                elif t == 5:
                    str_len, l = read_varint(stream[pos:])
                    pos += l
                    data['content'] = stream[pos: pos + str_len].decode()
                    pos += str_len
                elif t == 6:
                    d, l = read_varint(stream[pos:])
                    data['progress'] = int(d)
                    pos += l
                elif t == 7:
                    str_len, l = read_varint(stream[pos:])
                    pos += l
                    data['ctime'] = stream[pos: pos + str_len].decode()
                    pos += str_len
                elif t == 8:
                    str_len, l = read_varint(stream[pos:])
                    pos += l
                    data['mtime'] = stream[pos: pos + str_len].decode()
                    pos += str_len
                elif t == 9:
                    str_len, l = read_varint(stream[pos:])
                    pos += l
                    data['extra'] = json.loads(stream[pos: pos + str_len].decode())
                    pos += str_len
                elif t == 10:
                    str_len, l = read_varint(stream[pos:])
                    pos += l
                    data['idStr'] = stream[pos: pos + str_len].decode()
                    pos += str_len
                else:
                    continue
            return data

        def read_dmSetting(stream: bytes):
            length_ = len(stream)
            pos = 0
            data = {}
            while pos < length_:
                t = stream[pos] >> 3
                pos += 1
                if t == 1:
                    data['dmSwitch'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 2:
                    data['aiSwitch'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 3:
                    d, l = read_varint(stream[pos:])
                    data['aiLevel'] = int(d)
                    pos += l
                elif t == 4:
                    data['blocktop'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 5:
                    data['blockscroll'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 6:
                    data['blockbottom'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 7:
                    data['blockcolor'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 8:
                    data['blockspecial'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 9:
                    data['preventshade'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 10:
                    data['dmask'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 11:
                    d = struct.unpack('>f', stream[pos: pos+4])[0]
                    pos += 4
                    data['opacity'] = d
                elif t == 12:
                    d, l = read_varint(stream[pos:])
                    data['dmarea'] = int(d)
                    pos += l
                elif t == 13:
                    d = struct.unpack('>f', stream[pos: pos + 4])[0]
                    pos += 4
                    data['speedplus'] = d
                elif t == 14:
                    d = struct.unpack('>f', stream[pos: pos + 4])[0]
                    pos += 4
                    data['fontsize'] = d
                elif t == 15:
                    data['screensync'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 16:
                    data['speedsync'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 17:
                    str_len, l = read_varint(stream[pos:])
                    pos += l
                    data['fontfamily'] = stream[pos: pos + str_len].decode()
                    pos += str_len
                elif t == 18:
                    data['bold'] = True if stream[pos] == b'\x01' else False
                    pos += 1
                elif t == 19:
                    d, l = read_varint(stream[pos:])
                    data['fontborder'] = int(d)
                    pos += l
                elif t == 20:
                    str_len, l = read_varint(stream[pos:])
                    pos += l
                    data['drawType'] = stream[pos: pos + str_len].decode()
                    pos += str_len
                else:
                    continue
            return data

        while pos < length:
            type_ = resp_data[pos] >> 3
            pos += 1
            if type_ == 1:
                d, l = read_varint(resp_data[pos:])
                json_data['state'] = int(d)
                pos += l
            elif type_ == 2:
                str_len, l = read_varint(resp_data[pos:])
                pos += l
                json_data['text'] = resp_data[pos:pos + str_len].decode()
                pos += str_len
            elif type_ == 3:
                str_len, l = read_varint(resp_data[pos:])
                pos += l
                json_data['textSide'] = resp_data[pos:pos + str_len].decode()
                pos += str_len
            elif type_ == 4:
                data_len, l = read_varint(resp_data[pos:])
                pos += l
                json_data['dmSge'] = read_dmSge(resp_data[pos:pos+data_len])
                pos += data_len
            elif type_ == 5:
                data_len, l = read_varint(resp_data[pos:])
                pos += l
                json_data['flag'] = read_flag(resp_data[pos:pos + data_len])
                pos += data_len
            elif type_ == 6:
                if 'specialDms' not in json_data:
                    json_data['specialDms'] = []
                data_len, l = read_varint(resp_data[pos:])
                pos += l
                json_data['specialDms'].append(resp_data[pos: pos+data_len].decode())
                pos += data_len
            elif type_ == 7:
                json_data['checkBox'] = True if resp_data[pos] == b'\x01' else False
                pos += 1
            elif type_ == 8:
                d, l = read_varint(resp_data[pos:])
                pos += l
                json_data['count'] = int(d)
            elif type_ == 9:
                data_len, l = read_varint(resp_data[pos:])
                pos += l
                if 'commandDms' not in json_data:
                    json_data['commandDms'] = []
                json_data['commandDms'].append(read_commandDms(resp_data[pos: pos+data_len]))
                pos += data_len
            elif type_ == 10:
                data_len, l = read_varint(resp_data[pos:])
                pos += l
                json_data['dmSetting'] = read_dmSetting(resp_data[pos: pos+data_len])
                pos += data_len
            else:
                continue
        return json_data

    async def get_danmaku(self, page_index: int, date: datetime.date = None):
        """
        获取弹幕

        :param page_index: 分 p 号
        :param date: 为None时获取最新弹幕，为datetime.date时获取历史弹幕
        """

        if date is not None:
            self.credential.raise_for_no_sessdata()

        session = get_session()
        page_id = self.__get_pages_id_by_index(page_index)
        aid = self.__aid
        api = API["video"]["danmaku"]["get_danmaku"]
        params = {
            "oid": page_id,
            "type": 1,
            "segment_index": 1,
            "pid": aid
        }
        if date is not None:
            params["date"] = date.strftime("%Y-%m-%d")
            params["type"] = 1
        # 先获取 view 信息
        view = self.get_danmaku_view(page_id, aid=aid)
        sge_count = view['dmSge']['total']

        # 循环获取所有 segment
        danmakus = []
        for i in range(sge_count):
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
            if content_type == 'application/json':
                con = await req.json()
                if con['code'] != 0:
                    raise ApiCodeException(con['code'], con['message'])
                else:
                    return con
            elif content_type == 'application/octet-stream':
                # 解析二进制流数据
                data = await req.read()

                offset = 0
                if data == b'\x10\x01':
                    # 视频弹幕呗关闭
                    raise DanmakuClosedException()
                while offset < len(data):
                    if data[offset] == 0x0a:
                        dm = Danmaku('')
                        offset += 1
                        dm_data_length, l = read_varint(data[offset:])
                        offset += l
                        real_data = data[offset:offset+dm_data_length]
                        dm_data_offset = 0

                        while dm_data_offset < dm_data_length:
                            data_type = real_data[dm_data_offset] >> 3
                            dm_data_offset += 1
                            if data_type == 1:
                                d, l = read_varint(real_data[dm_data_offset:])
                                dm_data_offset += l
                                dm.id = d
                            elif data_type == 2:
                                d, l = read_varint(real_data[dm_data_offset:])
                                dm_data_offset += l
                                dm.dm_time = datetime.timedelta(seconds=d / 1000)
                            elif data_type == 3:
                                d, l = read_varint(real_data[dm_data_offset:])
                                dm_data_offset += l
                                dm.mode = d
                            elif data_type == 4:
                                d, l = read_varint(real_data[dm_data_offset:])
                                dm_data_offset += l
                                dm.font_size = d
                            elif data_type == 5:
                                d, l = read_varint(real_data[dm_data_offset:])
                                dm_data_offset += l
                                dm.color = Color()
                                dm.color.set_dec_color(d)
                            elif data_type == 6:
                                str_len = real_data[dm_data_offset]
                                dm_data_offset += 1
                                d = real_data[dm_data_offset:dm_data_offset + str_len]
                                dm_data_offset += str_len
                                dm.crc32_id = d.decode()
                            elif data_type == 7:
                                str_len = real_data[dm_data_offset]
                                dm_data_offset += 1
                                d = real_data[dm_data_offset:dm_data_offset + str_len]
                                dm_data_offset += str_len
                                dm.text = d.decode(errors='ignore')
                            elif data_type == 8:
                                d, l = read_varint(real_data[dm_data_offset:])
                                dm_data_offset += l
                                dm.send_time = datetime.datetime.fromtimestamp(d)
                            elif data_type == 9:
                                d, l = read_varint(real_data[dm_data_offset:])
                                dm_data_offset += l
                                dm.weight = d
                            elif data_type == 10:
                                d, l = read_varint(real_data[dm_data_offset:])
                                dm_data_offset += l
                                dm.action = d
                            elif data_type == 11:
                                d, l = read_varint(real_data[dm_data_offset:])
                                dm_data_offset += l
                                dm.pool = d
                            elif data_type == 12:
                                str_len = real_data[dm_data_offset]
                                dm_data_offset += 1
                                d = real_data[dm_data_offset:dm_data_offset + str_len]
                                dm_data_offset += str_len
                                dm.id_str = d.decode()
                            elif data_type == 13:
                                d, l = read_varint(real_data[dm_data_offset:])
                                dm_data_offset += l
                                dm.attr = d
                            else:
                                break
                        offset += dm_data_length
                        danmakus.append(dm)
        return danmakus