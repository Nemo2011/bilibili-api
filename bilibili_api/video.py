"""
bilibili_api.video

视频相关操作

注意，同时存在 page_index 和 cid 的参数，两者至少提供一个。
"""

from enum import Enum
import re
import datetime
import asyncio
import logging
import json
import struct
import aiohttp
import httpx
from typing import Any, List, Union

from .exceptions import ResponseException
from .exceptions import NetworkException
from .exceptions import ArgsException, DanmakuClosedException

from .utils.Credential import Credential
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.utils import get_api
from .utils.network_httpx import request, get_session
from .utils.network import get_session as get_session_aiohttp
from .utils.Danmaku import Danmaku, SpecialDanmaku
from .utils.BytesReader import BytesReader
from .utils.AsyncEvent import AsyncEvent
from dataclasses import dataclass
from . import settings

API = get_api("video")


class VideoQuality(Enum):
    """
    视频的视频流分辨率枚举

    - _360P: 流畅 360P
    - _480P: 清晰 480P
    - _720P: 高清 720P60
    - _1080P: 高清 1080P
    - _1080P_PLUS: 高清 1080P 高码率
    - _1080P_60: 高清 1080P 60 帧码率
    - _4K: 超清 4K
    - HDR: 真彩 HDR
    - DOLBY: 杜比视界
    - _8K: 超高清 8K
    """
    _360P = 16
    _480P = 32
    _720P = 64
    _1080P = 80
    _1080P_PLUS = 112
    _1080P_60 = 116
    _4K = 120
    HDR = 125
    DOLBY = 126
    _8K = 127



class VideoCodecs(Enum):
    """
    视频的视频流编码枚举

    - HEV: HEVC(H.265)
    - AVC: AVC(H.264)
    - AV1: AV1
    """
    HEV = "hev"
    AVC = "avc"
    AV1 = "av01"


class AudioQuality(Enum):
    """
    视频的音频流清晰度枚举

    - _64K: 64K
    - _132K: 132K
    - _192K: 192K
    - HI_RES: Hi-Res 无损
    - DOLBY: 杜比全景声
    """
    _64K = 30216
    _132K = 30232
    DOLBY = 30250
    HI_RES = 30251
    _192K = 30280


@dataclass
class VideoStreamDownloadURL:
    """
    (@dataclass)

    视频流 URL 类

    Attributes:
        url           (str)         : 视频流 url
        video_quality (VideoQuality): 视频流清晰度
        video_codecs  (VideoCodecs) : 视频流编码
    """
    url: str
    video_quality: VideoQuality
    video_codecs: VideoCodecs


@dataclass
class AudioStreamDownloadURL:
    """
    (@dataclass)

    音频流 URL 类

    Attributes:
        url           (str)         : 音频流 url
        audio_quality (AudioQuality): 音频流清晰度
    """
    url: str
    audio_quality: AudioQuality


@dataclass
class FLVStreamDownloadURL:
    """
    (@dataclass)

    FLV 视频流

    Attributes:
        url           (str): FLV 流 url
    """
    url: str


@dataclass
class HTML5MP4DownloadURL:
    """
    (@dataclass)

    可供 HTML5 播放的 mp4 视频流

    Attributes:
        url           (str): HTML5 mp4 视频流
    """
    url: str



class VideoDownloadURLDataDetecter:
    """
    `Video.get_download_url` 返回结果解析类。

    在调用 `Video.get_download_url` 之后可以将代入 `VideoDownloadURLDataDetecter`，此类将一键解析。

    目前支持:
      - 视频清晰度: 360P, 480P, 720P, 1080P, 1080P 高码率, 1080P 60 帧, 4K, HDR, 杜比视界, 8K
      - 视频编码: HEVC(H.265), AVC(H.264), AV1
      - 音频清晰度: 64K, 132K, Hi-Res 无损音效, 杜比全景声, 192K
      - FLV 视频流
    """
    def __init__(self, data: dict):
        """
        Args:
            data (dict): `Video.get_download_url` 返回的结果
        """
        self.__data = data

    def check_video_and_audio_stream(self) -> bool:
        """
        判断是否为音视频分离流

        Returns:
            bool: 是否为音视频分离流
        """
        if "dash" in self.__data.keys():
            return True
        return False

    def check_flv_stream(self) -> bool:
        """
        判断是否为 FLV 视频流

        Returns:
            bool: 是否为 FLV 视频流
        """
        if "durl" in self.__data.keys():
            if self.__data["format"].startswith("flv"):
                return True
        return False

    def check_html5_mp4_stream(self) -> bool:
        """
        判断是否为 HTML5 可播放的 mp4 视频流

        Returns:
            bool: 是否为 HTML5 可播放的 mp4 视频流
        """
        if "durl" in self.__data.keys():
            if self.__data["format"].startswith("mp4"):
                return True
        return False

    def detect_all(self) -> \
        List[
            Union[
                VideoStreamDownloadURL,
                AudioStreamDownloadURL,
                FLVStreamDownloadURL,
                HTML5MP4DownloadURL
            ]
        ]:
        """
        解析数据

        Returns:
            List[VideoStreamDownloadURL | AudioStreamDownloadURL | FLVStreamDownloadURL | HTML5MP4DownloadURL]: 所有的视频/音频流
        """
        if "durl" in self.__data.keys():
            if self.__data["format"].startswith("flv"):
                # FLV 视频流
                return [FLVStreamDownloadURL(url = self.__data["durl"][0]["url"])]
            else:
                # HTML5 MP4 视频流
                return [HTML5MP4DownloadURL(url = self.__data["durl"][0]["url"])]
        else:
            # 正常情况
            streams = []
            videos_data = self.__data["dash"]["video"]
            audios_data = self.__data["dash"]["audio"]
            flac_data = self.__data["dash"]["flac"]
            dolby_data = self.__data["dash"]["dolby"]
            for video_data in videos_data:
                video_stream_url = video_data["baseUrl"]
                video_stream_quality = VideoQuality(video_data["id"])
                video_stream_codecs = None
                for val in VideoCodecs:
                    if val.value in video_data["codecs"]:
                        video_stream_codecs = val
                video_stream = VideoStreamDownloadURL(
                    url=video_stream_url,
                    video_quality=video_stream_quality,
                    video_codecs=video_stream_codecs # type: ignore
                )
                streams.append(video_stream)
            for audio_data in audios_data:
                audio_stream_url = audio_data["baseUrl"]
                audio_stream_quality = AudioQuality(audio_data["id"])
                audio_stream = AudioStreamDownloadURL(
                    url=audio_stream_url,
                    audio_quality=audio_stream_quality
                )
                streams.append(audio_stream)
            if flac_data:
                if flac_data["audio"]:
                    for flac in flac_data["audio"]:
                        flac_stream_url = flac["baseUrl"]
                        flac_stream_quality = AudioQuality(flac["id"])
                        flac_stream = AudioStreamDownloadURL(
                            url=flac_stream_url,
                            audio_quality=flac_stream_quality
                        )
                        streams.append(flac_stream)
            if dolby_data:
                if dolby_data["audio"]:
                    for dolby in dolby_data["audio"]:
                        dolby_stream_url = dolby["baseUrl"]
                        dolby_stream_quality = AudioQuality(dolby["id"])
                        dolby_stream = AudioStreamDownloadURL(
                            url=dolby_stream_url,
                            audio_quality=dolby_stream_quality
                        )
                        streams.append(dolby_stream)
            return streams

    def detect_best_streams(self) -> \
        Union[
            List[FLVStreamDownloadURL],
            List[HTML5MP4DownloadURL],
            List[Union[VideoStreamDownloadURL, AudioStreamDownloadURL]]
        ]:
        """
        提取出分辨率、音质等信息最好的音视频流

        Returns:
            List[VideoStreamDownloadURL | AudioStreamDownloadURL | FLVStreamDownloadURL | HTML5MP4DownloadURL]: 所有的视频/音频流
        """
        if self.check_flv_stream():
            return self.detect_all() # type: ignore
        elif self.check_html5_mp4_stream():
            return self.detect_all() # type: ignore
        else:
            data = self.detect_all()
            video_streams = []
            audio_streams = []
            for stream in data:
                if isinstance(stream, VideoStreamDownloadURL):
                    video_streams.append(stream)
                if isinstance(stream, AudioStreamDownloadURL):
                    audio_streams.append(stream)
            video_streams.sort(key=lambda s: s.video_quality.value, reverse=True)
            audio_streams.sort(key=lambda s: s.audio_quality.value, reverse=True)
            return [video_streams[0], audio_streams[0]]


class DanmakuOperatorType(Enum):
    DELETE = 1
    PROTECT = 2
    UNPROTECT = 3


class Video:
    """
    视频类，各种对视频的操作均在里面。
    """

    def __init__(
        self,
        bvid: Union[None, str] = None,
        aid: Union[None, int] = None,
        credential: Union[None, Credential] = None
    ):
        """
        Args:
            bvid       (str | None, optional)       : BV 号. bvid 和 aid 必须提供其中之一。
            aid        (int | None, optional)       : AV 号. bvid 和 aid 必须提供其中之一。
            credential (Credential | None, optional): Credential 类. Defaults to None.
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
        self.credential: Credential = Credential() if credential is None else credential

        # 用于存储视频信息，避免接口依赖视频信息时重复调用
        self.__info: Union[dict, None] = None

    def set_bvid(self, bvid: str) -> None:
        """
        设置 bvid。

        Args:
            bvid (str):   要设置的 bvid。
        """
        # 检查 bvid 是否有效
        if not re.search("^BV[a-zA-Z0-9]{10}$", bvid):
            raise ArgsException("bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。")
        self.__bvid = bvid
        self.__aid = bvid2aid(bvid)

    def get_bvid(self) -> str:
        """
        获取 BVID。

        Returns:
            str: BVID。
        """
        return self.__bvid

    def set_aid(self, aid: int) -> None:
        """
        设置 aid。

        Args:
            aid (int): AV 号。
        """
        if aid <= 0:
            raise ArgsException("aid 不能小于或等于 0。")

        self.__aid = aid
        self.__bvid = aid2bvid(aid)

    def get_aid(self) -> int:
        """
        获取 AID。

        Returns:
            int: aid。
        """
        return self.__aid

    async def get_info(self) -> dict:
        """
        获取视频信息。

        Returns:
            dict: 调用 API 返回的结果。
        """
        api = API["info"]["detail"]
        params = {"bvid": self.get_bvid(), "aid": self.get_aid()}
        resp = await request(
            "GET", api["url"], params=params, credential=self.credential
        )
        # 存入 self.__info 中以备后续调用
        self.__info = resp
        return resp

    async def __get_info_cached(self) -> dict:
        """
        获取视频信息，如果已获取过则使用之前获取的信息，没有则重新获取。

        Returns:
            dict: 调用 API 返回的结果。
        """
        if self.__info is None:
            return await self.get_info()
        return self.__info

    async def get_stat(self) -> dict:
        """
        获取视频统计数据（播放量，点赞数等）。

        Returns:
            dict: 调用 API 返回的结果。
        """
        url = API["info"]["stat"]["url"]
        params = {"bvid": self.get_bvid(), "aid": self.get_aid()}
        return await request("GET", url, params=params, credential=self.credential)

    async def get_tags(self, page_index: int = 0, cid: int = None) -> dict:
        """
        获取视频标签。

        Args:
            page_index (int): 分 P 序号. Defaults to 0.
            cid        (int): 分 P 编码. Defaults to None.

        Returns:
            dict: 调用 API 返回的结果。
        """
        if cid == None:
            cid = await self.get_cid(page_index = page_index)
        url = API["info"]["tags"]["url"]
        params = {"bvid": self.get_bvid(), "aid": self.get_aid(), "cid": cid}
        return await request("GET", url, params=params, credential=self.credential)

    async def get_chargers(self) -> dict:
        """
        获取视频充电用户。

        Returns:
            dict: 调用 API 返回的结果。
        """
        info = await self.__get_info_cached()
        mid = info["owner"]["mid"]
        url = API["info"]["chargers"]["url"]
        params = {"aid": self.get_aid(), "bvid": self.get_bvid(), "mid": mid}
        return await request("GET", url, params=params, credential=self.credential)

    async def get_pages(self) -> dict:
        """
        获取分 P 信息。

        Returns:
            dict: 调用 API 返回的结果。
        """
        url = API["info"]["pages"]["url"]
        params = {"aid": self.get_aid(), "bvid": self.get_bvid()}
        return await request("GET", url, params=params, credential=self.credential)

    async def __get_page_id_by_index(self, page_index: int) -> int:
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

    async def get_video_snapshot(
        self,
        cid: Union[int, None] = None,
        json_index: bool = False,
        pvideo: bool = True
    ) -> dict:
        """
        获取视频快照(视频各个时间段的截图拼图)

        Args:
            cid(int): 分 P CID(可选)
            json_index(bool): json 数组截取时间表 True 为需要，False 不需要
            pvideo(bool): 是否只获取预览

        Returns:
            dict: 调用 API 返回的结果,数据中 Url 没有 http 头
        """
        params: dict[str, Any] = {"aid": self.get_aid()}
        if pvideo:
            url = API["info"]["video_snapshot_pvideo"]["url"]
        else:
            params["bvid"] = self.get_bvid()
            if json_index:
                params["index"] = 1
            if cid:
                params["cid"] = cid
            url = API["info"]["video_snapshot"]["url"]
        return await request("GET", url, params=params)

    async def get_cid(self, page_index: int) -> int:
        """
        获取稿件 cid

        Args:
            page_index(int): 分 P

        Returns:
            int: cid
        """
        return await self.__get_page_id_by_index(page_index)

    async def get_download_url(
        self,
        page_index: Union[int, None] = None,
        cid: Union[int, None] = None,
        html5: bool = False
    ) -> dict:
        """
        获取视频下载信息。

        返回结果可以传入 `VideoDownloadURLDataDetecter` 进行解析。

        page_index 和 cid 至少提供其中一个，其中 cid 优先级最高

        Args:
            page_index (int | None, optional) : 分 P 号，从 0 开始。Defaults to None
            cid        (int | None, optional) : 分 P 的 ID。Defaults to None
            html5      (bool, optional): 是否以 html5 平台访问，这样子能直接在网页中播放，但是链接少。

        Returns:
            dict: 调用 API 返回的结果。
        """
        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        url = API["info"]["playurl"]["url"]
        if html5:
            params = {
                "avid": self.get_aid(),
                "cid": cid,
                "qn": "127",
                "otype": "json",
                "fnval": 4048,
                "fourk": 1,
                "platform": "html5",
            }
        else:
            params = {
                "avid": self.get_aid(),
                "cid": cid,
                "qn": "127",
                "otype": "json",
                "fnval": 4048,
                "fourk": 1,
            }
        return await request("GET", url, params=params, credential=self.credential)

    async def get_related(self) -> dict:
        """
        获取相关视频信息。

        Returns:
            dict: 调用 API 返回的结果。
        """
        url = API["info"]["related"]["url"]
        params = {"aid": self.get_aid(), "bvid": self.get_bvid()}
        return await request("GET", url, params=params, credential=self.credential)

    async def has_liked(self) -> bool:
        """
        视频是否点赞过。

        Returns:
            bool: 视频是否点赞过。
        """
        self.credential.raise_for_no_sessdata()

        url = API["info"]["has_liked"]["url"]
        params = {"bvid": self.get_bvid(), "aid": self.get_aid()}
        return await request("GET", url, params=params, credential=self.credential) == 1

    async def get_pay_coins(self) -> int:
        """
        获取视频已投币数量。

        Returns:
            int: 视频已投币数量。
        """
        self.credential.raise_for_no_sessdata()

        url = API["info"]["get_pay_coins"]["url"]
        params = {"bvid": self.get_bvid(), "aid": self.get_aid()}
        return (await request("GET", url, params=params, credential=self.credential))[
            "multiply"
        ]

    async def has_favoured(self) -> bool:
        """
        是否已收藏。

        Returns:
            bool: 视频是否已收藏。
        """
        self.credential.raise_for_no_sessdata()

        url = API["info"]["has_favoured"]["url"]
        params = {"bvid": self.get_bvid(), "aid": self.get_aid()}
        return (await request("GET", url, params=params, credential=self.credential))[
            "favoured"
        ]

    async def is_forbid_note(self) -> bool:
        """
        是否禁止笔记。

        Returns:
            bool: 是否禁止笔记。
        """
        url = API["info"]["is_forbid"]["url"]
        params = {"aid": self.get_aid()}
        return (await request("GET", url, params=params, credential=self.credential))[
            "forbid_note_entrance"
        ]

    async def get_private_notes_list(self) -> list:
        """
        获取稿件私有笔记列表。

        Returns:
            list: note_Ids。
        """
        self.credential.raise_for_no_sessdata()

        url = API["info"]["private_notes"]["url"]
        params = {"oid": self.get_aid(), "oid_type": 0}
        return (await request("GET", url, params=params, credential=self.credential))["noteIds"]

    async def get_public_notes_list(self, pn: int, ps: int) -> dict:
        """
        获取稿件公开笔记列表。

        Args:
            pn (int): 页码
            ps (int): 每页项数

        Returns:
            dict: 调用 API 返回的结果。
        """

        url = API["info"]["public_notes"]["url"]
        params = {"oid": self.get_aid(), "oid_type": 0, "pn": pn, "ps": ps}
        return await request("GET", url, params=params, credential=self.credential)

    async def get_danmaku_view(
        self,
        page_index: Union[int, None] = None,
        cid: Union[int, None] = None
    ) -> dict:
        """
        获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。

        Args:
            page_index (int, optional): 分 P 号，从 0 开始。Defaults to None
            cid        (int, optional): 分 P 的 ID。Defaults to None

        Returns:
            dict: 调用 API 返回的结果。
        """
        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        session = get_session()
        api = API["danmaku"]["view"]

        config = {}
        config["url"] = api["url"]
        config["params"] = {"type": 1, "oid": cid, "pid": self.get_aid()}
        config["cookies"] = self.credential.get_cookies()
        config["headers"] = {
            "Referer": "https://www.bilibili.com",
            "User-Agent": "Mozilla/5.0",
        }

        try:
            resp = await session.get(**config)
        except Exception as e:
            raise NetworkException(-1, str(e))

        resp_data = resp.read()
        json_data = {}
        reader = BytesReader(resp_data)

        # 解析二进制数据流

        def read_dm_seg(stream: bytes):
            reader_ = BytesReader(stream)
            data = {}
            while not reader_.has_end():
                t = reader_.varint() >> 3
                if t == 1:
                    data["page_size"] = reader_.varint()
                elif t == 2:
                    data["total"] = reader_.varint()
                else:
                    continue
            return data

        def read_flag(stream: bytes):
            reader_ = BytesReader(stream)
            data = {}
            while not reader_.has_end():
                t = reader_.varint() >> 3
                if t == 1:
                    data["rec_flag"] = reader_.varint()
                elif t == 2:
                    data["rec_text"] = reader_.string()
                elif t == 3:
                    data["rec_switch"] = reader_.varint()
                else:
                    continue
            return data

        def read_command_danmakus(stream: bytes):
            reader_ = BytesReader(stream)
            data = {}
            while not reader_.has_end():
                t = reader_.varint() >> 3
                if t == 1:
                    data["id"] = reader_.varint()
                elif t == 2:
                    data["oid"] = reader_.varint()
                elif t == 3:
                    data["mid"] = reader_.varint()
                elif t == 4:
                    data["commend"] = reader_.string()
                elif t == 5:
                    data["content"] = reader_.string()
                elif t == 6:
                    data["progress"] = reader_.varint()
                elif t == 7:
                    data["ctime"] = reader_.string()
                elif t == 8:
                    data["mtime"] = reader_.string()
                elif t == 9:
                    data["extra"] = json.loads(reader_.string())

                elif t == 10:
                    data["id_str"] = reader_.string()
                else:
                    continue
            return data

        def read_settings(stream: bytes):
            reader_ = BytesReader(stream)
            data = {}
            while not reader_.has_end():
                t = reader_.varint() >> 3

                if t == 1:
                    data["dm_switch"] = reader_.bool()
                elif t == 2:
                    data["ai_switch"] = reader_.bool()
                elif t == 3:
                    data["ai_level"] = reader_.varint()
                elif t == 4:
                    data["enable_top"] = reader_.bool()
                elif t == 5:
                    data["enable_scroll"] = reader_.bool()
                elif t == 6:
                    data["enable_bottom"] = reader_.bool()
                elif t == 7:
                    data["enable_color"] = reader_.bool()
                elif t == 8:
                    data["enable_special"] = reader_.bool()
                elif t == 9:
                    data["prevent_shade"] = reader_.bool()
                elif t == 10:
                    data["dmask"] = reader_.bool()
                elif t == 11:
                    data["opacity"] = reader_.float(True)
                elif t == 12:
                    data["dm_area"] = reader_.varint()
                elif t == 13:
                    data["speed_plus"] = reader_.float(True)
                elif t == 14:
                    data["font_size"] = reader_.float(True)
                elif t == 15:
                    data["screen_sync"] = reader_.bool()
                elif t == 16:
                    data["speed_sync"] = reader_.bool()
                elif t == 17:
                    data["font_family"] = reader_.string()
                elif t == 18:
                    data["bold"] = reader_.bool()
                elif t == 19:
                    data["font_border"] = reader_.varint()
                elif t == 20:
                    data["draw_type"] = reader_.string()
                else:
                    continue
            return data

        def read_image_danmakus(string: bytes):
            image_list = []
            reader_ = BytesReader(string)
            while not reader_.has_end():
                type_ = reader_.varint() >> 3
                if type_ == 1:
                    details_dict: dict[Any, Any] = {"texts": []}
                    img_details = reader_.bytes_string()
                    reader_details = BytesReader(img_details)
                    while not reader_details.has_end():
                        type_details = reader_details.varint() >> 3
                        if type_details == 1:
                            details_dict["texts"].append(reader_details.string())
                        elif type_details == 2:
                            details_dict["image"] = reader_details.string()
                        elif type_details == 3:
                            id_string = reader_details.bytes_string()
                            id_reader = BytesReader(id_string)
                            while not id_reader.has_end():
                                type_id = id_reader.varint() >> 3
                                if type_id == 2:
                                    details_dict["id"] = id_reader.varint()
                                else:
                                    raise ResponseException("解析响应数据错误")
                    image_list.append(details_dict)
                else:
                    raise ResponseException("解析响应数据错误")
            return image_list

        while not reader.has_end():
            type_ = reader.varint() >> 3

            if type_ == 1:
                json_data["state"] = reader.varint()
            elif type_ == 2:
                json_data["text"] = reader.string()
            elif type_ == 3:
                json_data["text_side"] = reader.string()
            elif type_ == 4:
                json_data["dm_seg"] = read_dm_seg(reader.bytes_string())
            elif type_ == 5:
                json_data["flag"] = read_flag(reader.bytes_string())
            elif type_ == 6:
                if "special_dms" not in json_data:
                    json_data["special_dms"] = []
                json_data["special_dms"].append(reader.string())
            elif type_ == 7:
                json_data["check_box"] = reader.bool()
            elif type_ == 8:
                json_data["count"] = reader.varint()
            elif type_ == 9:
                if "command_dms" not in json_data:
                    json_data["command_dms"] = []
                json_data["command_dms"].append(
                    read_command_danmakus(reader.bytes_string())
                )
            elif type_ == 10:
                json_data["dm_setting"] = read_settings(reader.bytes_string())
            elif type_ == 12:
                json_data["image_dms"] = read_image_danmakus(reader.bytes_string())
            else:
                continue
        return json_data

    async def get_danmakus(
        self,
        page_index: int = 0,
        date: Union[datetime.date, None] = None,
        cid: Union[int, None] = None
    ) -> List[Danmaku]:
        """
        获取弹幕。

        Args:
            page_index (int, optional): 分 P 号，从 0 开始。Defaults to None
            date       (datetime.Date | None, optional): 指定日期后为获取历史弹幕，精确到年月日。Defaults to None.
            cid        (int | None, optional): 分 P 的 ID。Defaults to None

        Returns:
            List[Danmaku]: Danmaku 类的列表。
        """
        if date is not None:
            self.credential.raise_for_no_sessdata()

        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        session = get_session()
        aid = self.get_aid()
        params: dict[str, Any] = {"oid": cid, "type": 1, "pid": aid}
        if date is not None:
            # 获取历史弹幕
            api = API["danmaku"]["get_history_danmaku"]
            params["date"] = date.strftime("%Y-%m-%d")
            params["type"] = 1
            all_seg = 1
        else:
            api = API["danmaku"]["get_danmaku"]
            view = await self.get_danmaku_view(cid=cid)
            all_seg = view["dm_seg"]["total"]

        danmakus = []

        for seg in range(all_seg):
            if date is None:
                # 仅当获取当前弹幕时需要该参数
                params["segment_index"] = seg + 1

            config = {}
            config["url"] = api["url"]
            config["params"] = params
            config["headers"] = {
                "Referer": "https://www.bilibili.com",
                "User-Agent": "Mozilla/5.0",
            }
            config["cookies"] = self.credential.get_cookies()

            try:
                req = await session.get(**config)
            except Exception as e:
                raise NetworkException(-1, str(e))

            if "content-type" not in req.headers.keys():
                break
            else:
                content_type = req.headers["content-type"]
                if content_type != "application/octet-stream":
                    raise ResponseException("返回数据类型错误：")

            # 解析二进制流数据
            data = req.read()
            if data == b"\x10\x01":
                # 视频弹幕被关闭
                raise DanmakuClosedException()

            reader = BytesReader(data)
            while not reader.has_end():
                type_ = reader.varint() >> 3
                if type_ != 1:
                    if type_ == 4:
                        reader.bytes_string()
                        # 什么鬼？我用 protoc 解析出乱码！
                    else:
                        raise ResponseException("解析响应数据错误")

                dm = Danmaku("")
                dm_pack_data = reader.bytes_string()
                dm_reader = BytesReader(dm_pack_data)

                while not dm_reader.has_end():
                    data_type = dm_reader.varint() >> 3

                    if data_type == 1:
                        dm.id_ = dm_reader.varint()
                    elif data_type == 2:
                        dm.dm_time = dm_reader.varint() / 1000
                    elif data_type == 3:
                        dm.mode = dm_reader.varint()
                    elif data_type == 4:
                        dm.font_size = dm_reader.varint()
                    elif data_type == 5:
                        dm.color = hex(dm_reader.varint())[2:]
                    elif data_type == 6:
                        dm.set_crc32_id(dm_reader.string())
                    elif data_type == 7:
                        dm.text = dm_reader.string()
                    elif data_type == 8:
                        dm.send_time = dm_reader.varint()
                    elif data_type == 9:
                        dm.weight = dm_reader.varint()
                    elif data_type == 10:
                        dm.action = str(dm_reader.varint())
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

    async def get_special_dms(
        self,
        page_index: int = 0,
        cid: Union[int, None] = None
    ) -> List[SpecialDanmaku]:
        """
        获取特殊弹幕

        Args:
            page_index (int, optional)       : 分 P 号. Defaults to 0.
            cid        (int | None, optional): 分 P id. Defaults to None.

        Returns:
            List[SpecialDanmaku]: 调用接口解析后的结果
        """
        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        view = await self.get_danmaku_view(cid=cid)
        special_dms = view["special_dms"][0]
        if settings.proxy != "":
            sess = httpx.AsyncClient(proxies={"all://": settings.proxy})
        else:
            sess = httpx.AsyncClient()
        dm_content = await sess.get(special_dms, cookies=self.credential.get_cookies())
        dm_content.raise_for_status()
        reader = BytesReader(dm_content.content)
        dms: List[SpecialDanmaku] = []
        while not reader.has_end():
            spec_dm = SpecialDanmaku("")
            type_ = reader.varint() >> 3
            if type_ == 1:
                reader_ = BytesReader(reader.bytes_string())
                while not reader_.has_end():
                    type__ = reader_.varint() >> 3
                    if type__ == 1:
                        spec_dm.id_ = reader_.varint()
                    elif type__ == 3:
                        spec_dm.mode = reader_.varint()
                    elif type__ == 4:
                        reader_.varint()
                    elif type__ == 5:
                        reader_.varint()
                    elif type__ == 6:
                        reader_.string()
                    elif type__ == 7:
                        spec_dm.content = reader_.string()
                    elif type__ == 8:
                        reader_.varint()
                    elif type__ == 11:
                        spec_dm.pool = reader_.varint()
                    elif type__ == 12:
                        spec_dm.id_str = reader_.string()
                    else:
                        continue
            else:
                continue
            dms.append(spec_dm)
        return dms

    async def get_history_danmaku_index(
        self,
        page_index: Union[int, None] = None,
        date: Union[datetime.date, None] = None,
        cid: Union[int, None] = None
    ) -> Union[None, List[str]]:
        """
        获取特定月份存在历史弹幕的日期。

        Args:
            page_index (int | None, optional): 分 P 号，从 0 开始。Defaults to None
            date       (datetime.date | None): 精确到年月. Defaults to None。
            cid        (int | None, optional): 分 P 的 ID。Defaults to None

        Returns:
            None | List[str]: 调用 API 返回的结果。不存在时为 None。
        """
        if date is None:
            raise ArgsException("请提供 date 参数")

        self.credential.raise_for_no_sessdata()

        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        api = API["danmaku"]["get_history_danmaku_index"]
        params = {"oid": cid, "month": date.strftime("%Y-%m"), "type": 1}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def has_liked_danmakus(
        self,
        page_index: Union[int, None] = None,
        ids: Union[List[int], None] = None,
        cid: Union[int, None] = None
    ) -> dict:
        """
        是否已点赞弹幕。

        Args:
            page_index (int | None, optional): 分 P 号，从 0 开始。Defaults to None
            ids        (List[int] | None): 要查询的弹幕 ID 列表。
            cid        (int | None, optional): 分 P 的 ID。Defaults to None

        Returns:
            dict: 调用 API 返回的结果。
        """
        if ids is None or len(ids) == 0:
            raise ArgsException("请提供 ids 参数并至少有一个元素")

        self.credential.raise_for_no_sessdata()

        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        api = API["danmaku"]["has_liked_danmaku"]
        params = {"oid": cid, "ids": ",".join(ids)} # type: ignore
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def send_danmaku(
        self,
        page_index: Union[int, None] = None,
        danmaku: Union[Danmaku, None] = None,
        cid: Union[int, None] = None
    ) -> dict:
        """
        发送弹幕。

        Args:
            page_index (int | None, optional): 分 P 号，从 0 开始。Defaults to None
            danmaku    (Danmaku | None)      : Danmaku 类。
            cid        (int | None, optional): 分 P 的 ID。Defaults to None

        Returns:
            dict: 调用 API 返回的结果。
        """

        if danmaku is None:
            raise ArgsException("请提供 danmaku 参数")

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        api = API["danmaku"]["send_danmaku"]

        if danmaku.is_sub:
            pool = 1
        else:
            pool = 0
        data = {
            "type": 1,
            "oid": cid,
            "msg": danmaku.text,
            "aid": self.get_aid(),
            "bvid": self.get_bvid(),
            "progress": int(danmaku.dm_time * 1000),
            "color": int(danmaku.color, 16),
            "fontsize": danmaku.font_size,
            "pool": pool,
            "mode": danmaku.mode,
            "plat": 1,
        }
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def get_danmaku_xml(
        self,
        page_index: Union[int, None] = None,
        cid: Union[int, None] = None
    ) -> str:
        """
        获取所有弹幕的 xml 源文件（非装填）

        Args:
            page_index (int, optional)       : 分 P 序号. Defaults to 0.
            cid        (int | None, optional): cid. Defaults to None.

        Return:
            xml 文件源
        """
        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)
        url = f"https://comment.bilibili.com/{cid}.xml"
        sess = get_session()
        config: dict[Any, Any] = {"url": url}
        # 代理
        if settings.proxy:
            config["proxies"] = {"all://", settings.proxy}
        resp = await sess.get(**config)
        return resp.content.decode("utf-8")

    async def like_danmaku(
        self,
        page_index: Union[int, None] = None,
        dmid: Union[int, None] = None,
        status: Union[bool, None] = True,
        cid: Union[int, None] = None,
    ) -> dict:
        """
        点赞弹幕。

        Args:
            page_index (int | None, optional) : 分 P 号，从 0 开始。Defaults to None
            dmid       (int | None)           : 弹幕 ID。
            status     (bool | None, optional): 点赞状态。Defaults to True
            cid        (int | None, optional) : 分 P 的 ID。Defaults to None

        Returns:
            dict: 调用 API 返回的结果。
        """
        if dmid is None:
            raise ArgsException("请提供 dmid 参数")

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        api = API["danmaku"]["like_danmaku"]

        data = {
            "dmid": dmid,
            "oid": cid,
            "op": 1 if status else 2,
            "platform": "web_player",
        }
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def operate_danmaku(
        self,
        page_index: Union[int, None] = None,
        dmids: Union[List[int], None] = None,
        cid: Union[int, None] = None,
        type_: Union[DanmakuOperatorType, None] = None,
    ) -> dict:
        """
        操作弹幕

        Args:
            page_index (int | None, optional)      : 分 P 号，从 0 开始。Defaults to None
            dmids      (List[int] | None)          : 弹幕 ID 列表。
            cid        (int | None, optional)      : 分 P 的 ID。Defaults to None
            type_      (DanmakuOperatorType | None): 操作类型

        Returns:
            dict: 调用 API 返回的结果。
        """

        if dmids is None or len(dmids) == 0:
            raise ArgsException("请提供 dmid 参数")

        if type_ is None:
            raise ArgsException("请提供 type_ 参数")

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        api = API["danmaku"]["edit_danmaku"]

        data = {
            "type": 1,
            "dmids": ",".join(map(lambda x: str(x), dmids)),
            "oid": cid,
            "state": type_.value,
        }

        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def like(self, status: bool = True) -> dict:
        """
        点赞视频。

        Args:
            status (bool, optional): 点赞状态。Defaults to True.

        Returns:
            dict: 调用 API 返回的结果。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["like"]
        data = {"aid": self.get_aid(), "like": 1 if status else 2}
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def pay_coin(self, num: int = 1, like: bool = False) -> dict:
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
            "like": 1 if like else 0,
        }
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def add_tag(self, name: str) -> dict:
        """
        添加标签。

        Args:
            name (str): 标签名字。

        Returns:
            dict: 调用 API 返回的结果。会返回标签 ID。
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["add_tag"]
        data = {"aid": self.get_aid(), "bvid": self.get_bvid(), "tag_name": name}
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def delete_tag(self, tag_id: int) -> dict:
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

        data = {"tag_id": tag_id, "aid": self.get_aid(), "bvid": self.get_bvid()}
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def subscribe_tag(self, tag_id: int) -> dict:
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

        data = {"tag_id": tag_id}
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def unsubscribe_tag(self, tag_id: int) -> dict:
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

        data = {"tag_id": tag_id}
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def set_favorite(
        self, add_media_ids: List[int] = [], del_media_ids: List[int] = []
    ) -> dict:
        """
        设置视频收藏状况。

        Args:
            add_media_ids (List[int], optional): 要添加到的收藏夹 ID. Defaults to [].
            del_media_ids (List[int], optional): 要移出的收藏夹 ID. Defaults to [].

        Returns:
            dict: 调用 API 返回结果。
        """
        if len(add_media_ids) + len(del_media_ids) == 0:
            raise ArgsException("对收藏夹无修改。请至少提供 add_media_ids 和 del_media_ids 中的其中一个。")

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["favorite"]
        data = {
            "rid": self.get_aid(),
            "type": 2,
            "add_media_ids": ",".join(map(lambda x: str(x), add_media_ids)),
            "del_media_ids": ",".join(map(lambda x: str(x), del_media_ids)),
        }
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def get_subtitle(
        self,
        cid: Union[int, None] = None,
    ):
        """
        获取字幕信息

        Args:
            cid (int | None): 分 P ID,从视频信息中获取

        Returns:
            调用 API 返回的结果
        """
        if cid is None:
            raise ArgsException("需要 cid")
        api = API["info"]["get_player_info"]

        params = {
            "aid": self.get_aid(),
            "cid": cid,
        }
        result = await request(
            "GET", api["url"], params=params, credential=self.credential
        )
        return result.get("subtitle")

    async def submit_subtitle(
        self,
        lan: str,
        data: dict,
        submit: bool,
        sign: bool,
        page_index: Union[int, None] = None,
        cid: Union[int, None] = None,
    ):
        """
        上传字幕

        字幕数据 data 参考：

        ```json
        {
          "font_size": "float: 字体大小，默认 0.4",
          "font_color": "str: 字体颜色，默认 \"#FFFFFF\"",
          "background_alpha": "float: 背景不透明度，默认 0.5",
          "background_color": "str: 背景颜色，默认 \"#9C27B0\"",
          "Stroke": "str: 描边，目前作用未知，默认为 \"none\"",
          "body": [
            {
              "from": "int: 字幕开始时间（秒）",
              "to": "int: 字幕结束时间（秒）",
              "location": "int: 字幕位置，默认为 2",
              "content": "str: 字幕内容"
            }
          ]
        }
        ```

        Args:
            lan        (str)                 : 字幕语言代码，参考 http://www.lingoes.cn/zh/translator/langcode.htm
            data       (dict)                : 字幕数据
            submit     (bool)                : 是否提交，不提交为草稿
            sign       (bool)                : 是否署名
            page_index (int | None, optional): 分 P 索引. Defaults to None.
            cid        (int | None, optional): 分 P id. Defaults to None.

        Returns:
            dict: API 调用返回结果

        """
        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["submit_subtitle"]

        payload = {
            "type": 1,
            "oid": cid,
            "lan": lan,
            "data": json.dumps(data),
            "submit": submit,
            "sign": sign,
            "bvid": self.get_bvid(),
        }

        return await request(
            "POST", api["url"], data=payload, credential=self.credential
        )

    async def get_danmaku_snapshot(self) -> dict:
        """
        获取弹幕快照

        Returns:
            调用 API 返回的结果
        """
        api = API["danmaku"]["snapshot"]

        params = {"aid": self.get_aid()}

        return await request(
            "GET", api["url"], params=params, credential=self.credential
        )

    async def recall_danmaku(
        self,
        page_index: Union[int, None] = None,
        dmid: int = 0,
        cid: Union[int, None] = None
    ) -> dict:
        """
        撤回弹幕

        Args:
            page_index(int | None, optional): 分 P 号
            dmid(int)      : 弹幕 id
            cid(int | None, optional)       : 分 P 编码
        Returns:
            调用 API 返回的结果
        """
        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["danmaku"]["recall"]
        data = {"dmid": dmid, "cid": cid}

        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def get_pbp(
        self,
        page_index: Union[int, None] = None,
        cid: Union[int, None] = None
    ) -> dict:
        """
        获取高能进度条

        Args:
            page_index(int | None): 分 P 号
            cid(int | None)       : 分 P 编码

        Returns:
            调用 API 返回的结果
        """
        if cid is None:
            if page_index is None:
                raise ArgsException("page_index 和 cid 至少提供一个。")

            cid = await self.__get_page_id_by_index(page_index)

        api = API["info"]["pbp"]

        params = {"cid": cid}

        session = get_session()

        return json.loads(
            (
                await session.get(
                    api["url"], params=params, cookies=self.credential.get_cookies()
                )
            ).text
        )

    async def add_to_toview(self) -> dict:
        """
        添加视频至稍后再看列表

        Returns:
            调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()
        api = get_api("toview")["operate"]["add"]
        datas = {
            "aid": self.get_aid(),
        }
        return await request("POST", api["url"], data=datas, credential=self.credential)

    async def delete_from_toview(self) -> dict:
        """
        从稍后再看列表删除视频

        Returns:
            调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()
        api = get_api("toview")["operate"]["del"]
        datas = {"viewed": "false", "aid": self.get_aid()}
        return await request("POST", api["url"], data=datas, credential=self.credential)


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
        DANMAKU = 0x3E8

    def __init__(
        self,
        bvid: Union[str, None] = None,
        aid: Union[int, None] = None,
        page_index: int = 0,
        credential: Union[Credential, None] = None,
        debug: bool = False,
    ):
        """
        Args:
            bvid       (str | None, optional)       : BVID. Defaults to None.
            aid        (int | None, optional)       : AID. Defaults to None.
            page_index (int, optional)              : 分 P 序号. Defaults to 0.
            credential (Credential | None, optional): Credential 类. Defaults to None.
            debug      (bool, optional)             : 调试模式，将输出更详细信息. Defaults to False.
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
        self.logger = logging.getLogger(f"VideoOnlineMonitor-{id_showed}")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    "[" + str(id_showed) + "][%(asctime)s][%(levelname)s] %(message)s"
                )
            )
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
        cid = pages[self.__page_index]["cid"]

        # 获取服务器信息
        self.logger.debug(f"准备连接：{self.__video.get_bvid()}")
        self.logger.debug(f"获取服务器信息中...")
        resp = await request(
            "GET",
            "https://api.bilibili.com/x/web-interface/broadcast/servers?platform=pc",
            credential=self.credential,
        )

        uri = f"wss://{resp['domain']}:{resp['wss_port']}/sub"
        self.__heartbeat_interval = resp["heartbeat"]
        self.logger.debug(f"服务器信息获取成功，URI：{uri}")

        # 连接服务器
        self.logger.debug("准备连接服务器...")
        session = get_session_aiohttp()
        async with session.ws_connect(uri) as ws:
            self.__ws = ws

            # 发送认证信息
            self.logger.debug("服务器连接成功，准备发送认证信息...")
            verify_info = {
                "room_id": f"video://{self.__video.get_aid()}/{cid}",
                "platform": "web",
                "accepts": [1000, 1015],
            }
            verify_info = json.dumps(verify_info, separators=(",", ":"))
            await ws.send_bytes(
                self.__pack(
                    VideoOnlineMonitor.Datapack.CLIENT_VERIFY, 1, verify_info.encode()
                )
            )

            # 循环接收消息
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.BINARY:
                    data = self.__unpack(msg.data)
                    self.logger.debug(f"收到消息：{data}")
                    await self.__handle_data(data) # type: ignore

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    self.logger.warning("连接被异常断开")
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
            if d["type"] == VideoOnlineMonitor.Datapack.SERVER_VERIFY.value:
                # 服务器认证反馈。
                if d["data"]["code"] == 0:
                    # 创建心跳 Task
                    heartbeat = asyncio.create_task(self.__heartbeat_task())
                    self.__tasks.append(heartbeat)

                    self.logger.info("连接服务器并验证成功")

            elif d["type"] == VideoOnlineMonitor.Datapack.SERVER_HEARTBEAT.value:
                # 心跳包反馈，同时包含在线人数。
                self.logger.debug(f'收到服务器心跳包反馈，编号：{d["number"]}')
                self.logger.info(f'实时观看人数：{d["data"]["data"]["room"]["online"]}')
                self.dispatch("ONLINE", d["data"])

            elif d["type"] == VideoOnlineMonitor.Datapack.DANMAKU.value:
                # 实时弹幕。
                info = d["data"][0].split(",")
                text = d["data"][1]
                if info[5] == "0":
                    is_sub = False
                else:
                    is_sub = True
                dm = Danmaku(
                    dm_time=float(info[0]),
                    send_time=int(info[4]),
                    crc32_id=info[6],
                    color=info[3],
                    mode=info[1],
                    font_size=info[2],
                    is_sub=is_sub,
                    text=text,
                )
                self.logger.info(f"收到实时弹幕：{dm.text}")
                self.dispatch("DANMAKU", dm)

            else:
                # 未知类型数据包
                self.logger.warning("收到未知的数据包类型，无法解析：" + json.dumps(d))

    async def __heartbeat_task(self):
        """
        心跳 Task。
        """
        index = 2
        while True:
            self.logger.debug(f"发送心跳包，编号：{index}")
            await self.__ws.send_bytes(
                self.__pack(
                    VideoOnlineMonitor.Datapack.CLIENT_HEARTBEAT,
                    index,
                    b"[object Object]",
                )
            )
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
        | 4             | 4             | I    | 固定 0x00120001      |
        | 8             | 4             | I    | 数据包类型           |
        | 12            | 4             | I    | 递增数据包编号        |
        | 16            | 2             | H    | 固定 0x0000           |

        之后是有效载荷。

        # 数据包类型表：

        + 0x7    客户端发送认证信息
        + 0x8    服务端回应认证结果
        + 0x2    客户端发送心跳包，有效载荷：'[object Object]'
        + 0x3    服务端回应心跳包，会带上在线人数等信息，返回 JSON
        + 0x3e8  实时弹幕更新，返回列表，[0]弹幕信息，[1]弹幕文本

        Args:
            data_type (VideoOnlineMonitor.DataType):  数据包类型枚举。

        Returns:
            bytes: 打包好的数据。
        """
        packed_data = bytearray()
        packed_data += struct.pack(">I", 0x00120001)
        packed_data += struct.pack(">I", data_type.value)
        packed_data += struct.pack(">I", number)
        packed_data += struct.pack(">H", 0)
        packed_data += data
        packed_data = struct.pack(">I", len(packed_data) + 4) + packed_data
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
            region_header = struct.unpack(">IIII", data[:16])
            region_data = data[offset : offset + region_header[0]]
            real_data.append(
                {
                    "type": region_header[2],
                    "number": region_header[3],
                    "data": json.loads(
                        region_data[offset + 18 : offset + 18 + (region_header[0] - 16)]
                    ),
                }
            )
            offset += region_header[0]
        return tuple(real_data)
