"""
bilibili_api.video_uploader

视频上传
"""
import os
import json
import time
import base64
import re
import asyncio
import httpx
from enum import Enum
from typing import List, Union, Optional
from copy import copy, deepcopy
from asyncio.tasks import Task, create_task
from asyncio.exceptions import CancelledError
from datetime import datetime

from .video import Video
from .topic import Topic
from .utils.utils import get_api
from .utils.picture import Picture
from .utils.AsyncEvent import AsyncEvent
from .utils.credential import Credential
from .utils.aid_bvid_transformer import bvid2aid
from .exceptions.ApiException import ApiException
from .utils.network import Api, get_session
from .exceptions.NetworkException import NetworkException
from .exceptions.ResponseCodeException import ResponseCodeException

_API = get_api("video_uploader")


async def upload_cover(cover: Picture, credential: Credential) -> str:
    """
    上传封面

    Returns:
        str: 封面 URL
    """
    credential.raise_for_no_bili_jct()
    api = _API["cover_up"]
    pic = cover if isinstance(cover, Picture) else Picture().from_file(cover)
    cover = pic.convert_format("png")
    data = {
        "cover": f'data:image/png;base64,{base64.b64encode(pic.content).decode("utf-8")}'
    }
    return (await Api(**api, credential=credential).update_data(**data).result)["url"]


class Lines(Enum):
    """
    可选线路

    bupfetch 模式下 kodo 目前弃用 `{'error': 'no such bucket'}`

    + BDA2：百度
    + QN：七牛
    + WS：网宿
    + BLDSA：bldsa
    """

    BDA2 = "bda2"
    QN = "qn"
    WS = "ws"
    BLDSA = "bldsa"


with open(
    os.path.join(os.path.dirname(__file__), "data/video_uploader_lines.json"),
    encoding="utf8",
) as f:
    LINES_INFO = json.loads(f.read())


async def _probe() -> dict:
    """
    测试所有线路

    测速网页 https://member.bilibili.com/preupload?r=ping
    """
    # api = _API["probe"]
    # info = await Api(**api).update_params(r="probe").result # 不实时获取线路直接用 LINES_INFO
    min_cost, fastest_line = 30, None
    for line in LINES_INFO.values():
        start = time.perf_counter()
        data = bytes(int(1024 * 0.1 * 1024))  # post 0.1MB
        httpx.post(f'https:{line["probe_url"]}', data=data, timeout=30)
        cost_time = time.perf_counter() - start
        if cost_time < min_cost:
            min_cost, fastest_line = cost_time, line
    return fastest_line


async def _choose_line(line: Lines) -> dict:
    """
    选择线路，不存在则直接测速自动选择
    """
    if isinstance(line, Lines):
        line_info = LINES_INFO.get(line.value)
        if line_info is not None:
            return line_info
    return await _probe()


class Lines(Enum):
    """
    可选线路

    bupfetch 模式下 kodo 目前弃用 `{'error': 'no such bucket'}`

    + BDA2：百度
    + QN：七牛
    + WS：网宿
    + BLDSA：bldsa
    """

    BDA2 = "bda2"
    QN = "qn"
    WS = "ws"
    BLDSA = "bldsa"

LINES_INFO = {
    "bda2": {
        "os": "upos",
        "upcdn": "bda2",
        "probe_version": 20221109,
        "query": "probe_version=20221109&upcdn=bda2",
        "probe_url": "//upos-cs-upcdnbda2.bilivideo.com/OK"
    },
    "bldsa": {
        "os": "upos",
        "upcdn": "bldsa",
        "probe_version": 20221109,
        "query": "upcdn=bldsa&probe_version=20221109",
        "probe_url": "//upos-cs-upcdnbldsa.bilivideo.com/OK"
    },
    "qn": {
        "os": "upos",
        "upcdn": "qn",
        "probe_version": 20221109,
        "query": "probe_version=20221109&upcdn=qn",
        "probe_url": "//upos-cs-upcdnqn.bilivideo.com/OK"
    },
    "ws": {
        "os": "upos",
        "upcdn": "ws",
        "probe_version": 20221109,
        "query": "upcdn=ws&probe_version=20221109",
        "probe_url": "//upos-cs-upcdnws.bilivideo.com/OK",
    }
}

async def _probe() -> dict:
    """
    测试所有线路

    测速网页 https://member.bilibili.com/preupload?r=ping
    """
    # api = _API["probe"]
    # info = await Api(**api).update_params(r="probe").result # 不实时获取线路直接用 LINES_INFO
    min_cost, fastest_line = 30, None
    for line in LINES_INFO.values():
        start = time.perf_counter()
        data = bytes(int(1024 * 0.1 * 1024))  # post 0.1MB
        httpx.post(f'https:{line["probe_url"]}', data=data, timeout=30)
        cost_time = time.perf_counter() - start
        if cost_time < min_cost:
            min_cost, fastest_line = cost_time, line
    return fastest_line


async def _choose_line(line: Lines) -> dict:
    """
    选择线路，不存在则直接测速自动选择
    """
    if isinstance(line, Lines):
        line_info = LINES_INFO.get(line.value)
        if line_info is not None:
            return line_info
    return await _probe()
    

class VideoUploaderPage:
    """
    分 P 对象
    """

    def __init__(self, path: str, title: str, description: str = ""):
        """
        Args:
            path (str): 视频文件路径
            title        (str)           : 视频标题
            description  (str, optional) : 视频简介. Defaults to "".
        """
        self.path = path
        self.title: str = title
        self.description: str = description

        self.cached_size: Union[int, None] = None

    def get_size(self) -> int:
        """
        获取文件大小

        Returns:
            int: 文件大小
        """
        if self.cached_size is not None:
            return self.cached_size

        size: int = 0
        stream = open(self.path, "rb")
        while True:
            s: bytes = stream.read(1024)

            if not s:
                break

            size += len(s)

        stream.close()

        self.cached_size = size
        return size


class VideoUploaderEvents(Enum):
    """
    上传事件枚举

    Events:
    + PRE_PAGE 上传分 P 前
    + PREUPLOAD  获取上传信息
    + PREUPLOAD_FAILED  获取上传信息失败
    + PRE_CHUNK  上传分块前
    + AFTER_CHUNK  上传分块后
    + CHUNK_FAILED  区块上传失败
    + PRE_PAGE_SUBMIT  提交分 P 前
    + PAGE_SUBMIT_FAILED  提交分 P 失败
    + AFTER_PAGE_SUBMIT  提交分 P 后
    + AFTER_PAGE  上传分 P 后
    + PRE_COVER  上传封面前
    + AFTER_COVER  上传封面后
    + COVER_FAILED  上传封面失败
    + PRE_SUBMIT  提交视频前
    + SUBMIT_FAILED  提交视频失败
    + AFTER_SUBMIT  提交视频后
    + COMPLETED  完成上传
    + ABORTED  用户中止
    + FAILED  上传失败
    """

    PREUPLOAD = "PREUPLOAD"
    PREUPLOAD_FAILED = "PREUPLOAD_FAILED"
    PRE_PAGE = "PRE_PAGE"

    PRE_CHUNK = "PRE_CHUNK"
    AFTER_CHUNK = "AFTER_CHUNK"
    CHUNK_FAILED = "CHUNK_FAILED"

    PRE_PAGE_SUBMIT = "PRE_PAGE_SUBMIT"
    PAGE_SUBMIT_FAILED = "PAGE_SUBMIT_FAILED"
    AFTER_PAGE_SUBMIT = "AFTER_PAGE_SUBMIT"

    AFTER_PAGE = "AFTER_PAGE"

    PRE_COVER = "PRE_COVER"
    AFTER_COVER = "AFTER_COVER"
    COVER_FAILED = "COVER_FAILED"

    PRE_SUBMIT = "PRE_SUBMIT"
    SUBMIT_FAILED = "SUBMIT_FAILED"
    AFTER_SUBMIT = "AFTER_SUBMIT"

    COMPLETED = "COMPLETE"
    ABORTED = "ABORTED"
    FAILED = "FAILED"


async def get_available_topics(tid: int, credential: Credential) -> List[dict]:
    """
    获取可用 topic 列表
    """
    credential.raise_for_no_sessdata()
    api = _API["available_topics"]
    params = {"type_id": tid, "pn": 0, "ps": 200}  # 一次性获取完
    return (await Api(**api, credential=credential).update_params(**params).result)[
        "topics"
    ]


class VideoPorderType:
    """
    视频商业类型

    + FIREWORK: 花火
    + OTHER: 其他
    """

    FIREWORK = {"flow_id": 1}
    OTHER = {
        "flow_id": 1,
        "industry_id": None,
        "official": None,
        "brand_name": None,
        "show_type": [],
    }


class VideoPorderIndustry(Enum):
    """
    商单行业

    + MOBILE_GAME: 手游
    + CONSOLE_GAME: 主机游戏
    + WEB_GAME: 网页游戏
    + PC_GAME: PC单机游戏
    + PC_NETWORK_GAME: PC网络游戏
    + SOFTWARE_APPLICATION: 软件应用
    + DAILY_NECESSITIES_AND_COSMETICS: 日用品化妆品
    + CLOTHING_SHOES_AND_HATS: 服装鞋帽
    + LUGGAGE_AND_ACCESSORIES: 箱包饰品
    + FOOD_AND_BEVERAGE: 食品饮料
    + PUBLISHING_AND_MEDIA: 出版传媒
    + COMPUTER_HARDWARE: 电脑硬件
    + OTHER: 其他
    + MEDICAL: 医疗类
    + FINANCE: 金融
    """

    MOBILE_GAME = 1
    CONSOLE_GAME = 20
    WEB_GAME = 21
    PC_GAME = 22
    PC_NETWORK_GAME = 23
    SOFTWARE_APPLICATION = 2
    DAILY_NECESSITIES_AND_COSMETICS = 3
    CLOTHING_SHOES_AND_HATS = 4
    LUGGAGE_AND_ACCESSORIES = 5
    FOOD_AND_BEVERAGE = 6
    PUBLISHING_AND_MEDIA = 7
    COMPUTER_HARDWARE = 8
    OTHER = 9
    MEDICAL = 213
    FINANCE = 214


class VideoPorderShowType(Enum):
    """
    商单形式

    + LOGO: Logo
    + OTHER: 其他
    + SPOKEN_AD: 口播
    + PATCH: 贴片
    + TVC_IMBEDDED: TVC植入
    + CUSTOMIZED_AD: 定制软广
    + PROGRAM_SPONSORSHIP: 节目赞助
    + SLOGAN: SLOGAN
    + QR_CODE: 二维码
    + SUBTITLE_PROMOTION: 字幕推广
    """

    LOGO = 15
    OTHER = 10
    SPOKEN_AD = 11
    PATCH = 12
    TVC_IMBEDDED = 14
    CUSTOMIZED_AD = 19
    PROGRAM_SPONSORSHIP = 18
    SLOGAN = 17
    QR_CODE = 16
    SUBTITLE_PROMOTION = 13


class VideoPorderMeta:
    flow_id: int
    industry_id: Optional[int] = None
    official: Optional[int] = None
    brand_name: Optional[str] = None
    show_types: List[VideoPorderShowType] = []

    __info: dict = None

    def __init__(
        self,
        porden_type: VideoPorderType = VideoPorderType.FIREWORK,
        industry_type: Optional[VideoPorderIndustry] = None,
        brand_name: Optional[str] = None,
        show_types: List[VideoPorderShowType] = [],
    ):
        self.flow_id = 1
        self.__info = porden_type.value
        if porden_type == VideoPorderType.OTHER:
            self.__info["industry"] = industry_type.value
            self.__info["brand_name"] = brand_name
            self.__info["show_types"] = ",".join(
                [show_type.value for show_type in show_types]
            )

    def __dict__(self) -> dict:
        return self.__info


class VideoMeta:
    tid: int  # 分区 ID。可以使用 channel 模块进行查询。
    title: str  # 视频标题
    desc: str  # 视频简介。
    cover: Picture  # 封面 URL
    tags: Union[List[str], str]  # 视频标签。使用英文半角逗号分隔的标签组。
    topic_id: Optional[int] = None  # 可选，话题 ID。
    mission_id: Optional[int] = None  # 可选，任务 ID。
    original: bool = True  # 可选，是否为原创视频。
    source: Optional[str] = None  # 可选，视频来源。
    recreate: Optional[bool] = False  # 可选，是否允许重新上传。
    no_reprint: Optional[bool] = False  # 可选，是否禁止转载。
    open_elec: Optional[bool] = False  # 可选，是否展示充电信息。
    up_selection_reply: Optional[bool] = False  # 可选，是否开启评论精选。
    up_close_danmu: Optional[bool] = False  # 可选，是否关闭弹幕。
    up_close_reply: Optional[bool] = False  # 可选，是否关闭评论。
    lossless_music: Optional[bool] = False  # 可选，是否启用无损音乐。
    dolby: Optional[bool] = False  # 可选，是否启用杜比音效。
    subtitle: Optional[dict] = None  # 可选，字幕设置。
    dynamic: Optional[str] = None  # 可选，动态信息。
    neutral_mark: Optional[str] = None  # 可选，创作者声明。
    delay_time: Optional[Union[int, datetime]] = None  # 可选，定时发布时间戳（秒）。
    porder: Optional[VideoPorderMeta] = None  # 可选，商业相关参数。

    __credential: Credential
    __pre_info = dict

    def __init__(
        self,
        tid: int,  # 分区 ID。可以使用 channel 模块进行查询。
        title: str,  # 视频标题
        desc: str,  # 视频简介。
        cover: Union[Picture, str],  # 封面 URL
        tags: Union[List[str], str],  # 视频标签。使用英文半角逗号分隔的标签组。
        topic: Optional[Union[int, Topic]] = None,  # 可选，话题 ID。
        mission_id: Optional[int] = None,  # 可选，任务 ID。
        original: bool = True,  # 可选，是否为原创视频。
        source: Optional[str] = None,  # 可选，视频来源。
        recreate: Optional[bool] = False,  # 可选，是否允许重新上传。
        no_reprint: Optional[bool] = False,  # 可选，是否禁止转载。
        open_elec: Optional[bool] = False,  # 可选，是否展示充电信息。
        up_selection_reply: Optional[bool] = False,  # 可选，是否开启评论精选。
        up_close_danmu: Optional[bool] = False,  # 可选，是否关闭弹幕。
        up_close_reply: Optional[bool] = False,  # 可选，是否关闭评论。
        lossless_music: Optional[bool] = False,  # 可选，是否启用无损音乐。
        dolby: Optional[bool] = False,  # 可选，是否启用杜比音效。
        subtitle: Optional[dict] = None,  # 可选，字幕设置。
        dynamic: Optional[str] = None,  # 可选，动态信息。
        neutral_mark: Optional[str] = None,  # 可选，中性化标签。
        delay_time: Optional[Union[int, datetime]] = None,  # 可选，定时发布时间戳（秒）。
        porder: Optional[VideoPorderMeta] = None,  # 可选，商业相关参数。
    ) -> None:
        """
        基本视频上传参数

        可调用 VideoMeta.verify() 验证部分参数是否可用

        Args:
            tid (int): 分区 id

            title (str): 视频标题，最多 80 字

            desc (str): 视频简介，最多 2000 字

            cover (Union[Picture, str]): 封面，可以传入路径

            tags (List[str], str): 标签列表，传入 List 或者传入 str 以 "," 为分隔符，至少 1 个 Tag，最多 10 个

            topic (Optional[Union[int, Topic]]): 活动主题，应该从 video_uploader.get_available_topics(tid) 获取，可选

            mission_id (Optional[int]): 任务 id，与 topic 一同获取传入

            original (bool): 是否原创，默认原创

            source (Optional[str]): 转载来源，非原创应该提供

            recreate (Optional[bool]): 是否允许转载. 可选，默认为不允许二创

            no_reprint (Optional[bool]): 未经允许是否禁止转载. 可选，默认为允许转载

            open_elec (Optional[bool]): 是否开启充电. 可选，默认为关闭充电

            up_selection_reply (Optional[bool]): 是否开启评论精选. 可选，默认为关闭评论精选

            up_close_danmu (Optional[bool]): 是否关闭弹幕. 可选，默认为开启弹幕

            up_close_reply (Optional[bool]): 是否关闭评论. 可选，默认为开启评论

            lossless_music (Optional[bool]): 是否开启无损音乐. 可选，默认为关闭无损音乐

            dolby (Optional[bool]): 是否开启杜比音效. 可选，默认为关闭杜比音效

            subtitle (Optional[dict]): 字幕信息，可选

            dynamic (Optional[str]): 粉丝动态，可选，最多 233 字

            neutral_mark (Optional[str]): 创作者声明，可选

            delay_time (Optional[Union[int, datetime]]): 定时发布时间，可选

            porder (Optional[VideoPorderMeta]): 商业相关参数，可选
        """
        if isinstance(tid, int):
            self.tid = tid
        if isinstance(title, str) and len(title) <= 80:
            self.title = title
        else:
            raise ValueError("title 不合法或者大于 80 字")

        if tags is None:
            raise ValueError("tags 不能为空")
        elif isinstance(tags, str):
            if "," in tags:
                self.tags = tags.split(",")
            else:
                self.tags = [tags]
        elif isinstance(tags, list) and len(tags) <= 10:
            self.tags = tags
        else:
            raise ValueError("tags 不合法或者多于 10 个")

        if isinstance(cover, str):
            self.cover = Picture().from_file(cover)
        elif isinstance(cover, Picture):
            self.cover = cover
        if topic is not None:
            self.mission_id = mission_id
            if isinstance(topic, int):
                self.topic_id = topic
            elif isinstance(topic, Topic):
                self.topic_id = topic.get_topic_id()

        if isinstance(desc, str) and len(desc) <= 2000:
            self.desc = desc
        else:
            raise ValueError("desc 不合法或者大于 2000 字")

        self.original = original if isinstance(original, bool) else True
        if not self.original:
            if source is not None:
                if isinstance(source, str) and len(source) <= 200:
                    self.source = source
                else:
                    raise ValueError("source 不合法或者大于 200 字")

        self.recreate = recreate if isinstance(recreate, bool) else False
        self.no_reprint = no_reprint if isinstance(no_reprint, bool) else False
        self.open_elec = open_elec if isinstance(open_elec, bool) else False
        self.up_selection_reply = (
            up_selection_reply if isinstance(up_selection_reply, bool) else False
        )
        self.up_close_danmu = (
            up_close_danmu if isinstance(up_close_danmu, bool) else False
        )
        self.up_close_reply = (
            up_close_reply if isinstance(up_close_reply, bool) else False
        )
        self.lossless_music = (
            lossless_music if isinstance(lossless_music, bool) else False
        )
        self.dolby = dolby if isinstance(dolby, bool) else False
        self.subtitle = subtitle if isinstance(subtitle, dict) else None
        self.dynamic = (
            dynamic if isinstance(dynamic, str) and len(dynamic) <= 233 else None
        )
        self.neutral_mark = neutral_mark if isinstance(neutral_mark, str) else None
        if isinstance(delay_time, int):
            self.delay_time = delay_time
        elif isinstance(delay_time, datetime):
            self.delay_time = int(delay_time.timestamp())
        self.porder = porder if isinstance(porder, dict) else None

    def __dict__(self) -> dict:
        meta = {
            "title": self.title,
            "copyright": 1 if self.original else 2,
            "tid": self.tid,
            "tag": ",".join(self.tags),
            "mission_id": self.mission_id,  # 根据 topic 对应任务
            "topic_id": self.topic_id,
            "topic_detail": {
                "from_topic_id": self.topic_id,
                "from_source": "arc.web.recommend",
            },
            "desc_format_id": 9999,
            "desc": self.desc,
            "dtime": self.delay_time,
            "recreate": 1 if self.recreate else -1,
            "dynamic": self.dynamic,
            "interactive": 0,
            "act_reserve_create": 0,  # unknown
            "no_disturbance": 0,  # unknown
            "porder": self.porder.__dict__(),
            "adorder_type": 9,  # unknown
            "no_reprint": 1 if self.no_reprint else 0,
            "subtitle": self.subtitle
            if self.subtitle is not None
            else {
                "open": 0,
                "lan": "",
            },  # 莫名其妙没法上传 srt 字幕，显示格式错误，不校验
            "subtitle": self.subtitle,
            "neutral_mark": self.neutral_mark,  # 不知道能不能随便写文本
            "dolby": 1 if self.dolby else 0,
            "lossless_music": 1 if self.lossless_music else 0,
            "up_selection_reply": self.up_close_reply,
            "up_close_reply": self.up_close_reply,
            "up_close_danmu": self.up_close_danmu,
            "web_os": 1,  # const 1
        }
        for k in copy(meta).keys():
            if meta[k] is None:
                del meta[k]
        return meta

    async def _pre(self) -> dict:
        """
        获取上传参数基本信息

        包括活动等在内，固定信息已经缓存于 bilibili_api\data\video_uploader_meta_pre.json
        """
        api = _API["pre"]
        self.__pre_info = await Api(**api, credential=self.__credential).result
        return self.__pre_info

    def _check_tid(self) -> bool:
        """
        检查 tid 是否合法
        """
        with open(
            os.path.join(os.path.dirname(__file__), "data/video_uploader_meta_pre.json"),
            encoding="utf8",
        ) as f:
            self.__pre_info = json.load(f)
        type_list = self.__pre_info["tid_list"]
        for parent_type in type_list:
            for child_type in parent_type["children"]:
                if child_type["id"] == self.tid:
                    return True
        return False

    async def _check_cover(self) -> bool:
        """
        检查封面是否合法
        """
        try:
            await upload_cover(self.cover, self.__credential)
            return True
        except Exception:
            return False

    @staticmethod
    async def _check_tag_name(name: str, credential: Credential) -> bool:
        """
        检查 tag 是否合法

        需要登录
        """
        api = _API["check_tag_name"]
        return (
            await Api(**api, credential=credential, ignore_code=True)
            .update_params(t=name)
            .result
        )["code"] == 0

    async def _check_tags(self) -> List[str]:
        """
        检查所有 tag 是否合法
        """
        return [
            tag
            for tag in self.tags
            if await self._check_tag_name(tag, self.__credential)
        ]

    async def _check_topic_to_mission(self) -> Union[int, bool]:
        """
        检查 topic -> mission 是否存在
        """
        # 只知道能从这里获取...不确定其他地方的 topic -> mission 能否传入
        all_topic_info = await get_available_topics(
            tid=self.tid, credential=self.__credential
        )
        for topic in all_topic_info:
            if topic["topic_id"] == self.topic_id:
                return topic["mission_id"]
        else:
            return False

    async def verify(self, credential: Credential) -> bool:
        """
        验证参数是否可用，仅供参考

        检测 tags、delay_time、topic -> mission、cover 和 tid

        验证失败会抛出异常
        """
        credential.raise_for_no_sessdata()
        self.__credential = credential

        # await self._pre() # 缓存于 bilibili_api\data\video_uploader_meta_pre.json
        error_tags = await self._check_tags()
        if len(error_tags) != 0:
            raise ValueError(f'以下 tags 不合法: {",".join(error_tags)}')

        if not self._check_tid():
            raise ValueError(f"tid {self.tid} 不合法")

        topic_to_mission = await self._check_topic_to_mission()
        if isinstance(topic_to_mission, int):
            self.mission_id = topic_to_mission
        elif not topic_to_mission:
            raise ValueError(
                f"topic -> mission 不存在: {self.topic_id} -> {self.mission_id}"
            )

        if not await self._check_cover():
            raise ValueError(f"封面不合法 {self.cover.__repr__()}")

        if self.delay_time is not None:
            if self.delay_time < int(time.time()) + 7200:
                raise ValueError("delay_time 不能小于两小时")
            if self.delay_time > int(time.time()) + 3600 * 24 * 15:
                raise ValueError("delay_time 不能大于十五天")
        return True


class VideoUploader(AsyncEvent):
    """
    视频上传

    Attributes:
        pages        (List[VideoUploaderPage]): 分 P 列表

        meta         (VideoMeta, dict)        : 视频信息

        credential   (Credential)             : 凭据

        cover_path   (str)                    : 封面路径

        line         (Lines, Optional)        : 线路. Defaults to None. 不选择则自动测速选择
    """

    def __init__(
        self,
        pages: List[VideoUploaderPage],
        meta: Union[VideoMeta, dict],
        credential: Credential,
        cover: Optional[Union[str, Picture]] = "",
        line: Optional[Lines] = None,
    ):
        """
        Args:
            pages        (List[VideoUploaderPage]): 分 P 列表

            meta         (VideoMeta, dict)        : 视频信息

            credential   (Credential)             : 凭据

            cover        (Union[str, Picture])    : 封面路径或者封面对象. Defaults to ""，传入 meta 类型为 VideoMeta 时可不传

            line:        (Lines, Optional)        : 线路. Defaults to None. 不选择则自动测速选择

        建议传入 VideoMeta 对象，避免参数有误

        meta 参数示例：

        ```json
        {
            "title": "",
            "copyright": 1,
            "tid": 130,
            "tag": "",
            "desc_format_id": 9999,
            "desc": "",
            "recreate": -1,
            "dynamic": "",
            "interactive": 0,
            "act_reserve_create": 0,
            "no_disturbance": 0,
            "no_reprint": 1,
            "subtitle": {
                "open": 0,
                "lan": "",
            },
            "dolby": 0,
            "lossless_music": 0,
            "web_os": 1,
        }
        ```

        meta 保留字段：videos, cover
        """
        super().__init__()
        self.meta = meta
        self.pages = pages
        self.credential = credential
        self.cover = (
            self.meta.cover
            if isinstance(self.meta, VideoMeta)
            else cover
            if isinstance(cover, Picture)
            else Picture().from_file(cover)
        )
        self.line = line
        self.__task: Union[Task, None] = None

    async def _preupload(self, page: VideoUploaderPage) -> dict:
        """
        分 P 上传初始化

        Returns:
            dict: 初始化信息
        """
        self.dispatch(VideoUploaderEvents.PREUPLOAD.value, {page: page})
        api = _API["preupload"]

        # 首先获取视频文件预检信息
        session = get_session()

        resp = await session.get(
            api["url"],
            params={
                "profile": "ugcfx/bup",
                "name": os.path.basename(page.path),
                "size": page.get_size(),
                "r": self.line["os"],
                "ssl": "0",
                "version": "2.14.0",
                "build": "2100400",
                "upcdn": self.line["upcdn"],
                "probe_version": self.line["probe_version"],
            },
            cookies=self.credential.get_cookies(),
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://www.bilibili.com",
            },
        )
        if resp.status_code >= 400:
            self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
            raise NetworkException(resp.status_code, resp.reason_phrase)

        preupload = resp.json()

        if preupload["OK"] != 1:
            self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
            raise ApiException(json.dumps(preupload))

        url = self._get_upload_url(self.line, preupload)

        # 获取 upload_id
        resp = await session.post(
            url,
            headers={
                "x-upos-auth": preupload["auth"],
                "user-agent": "Mozilla/5.0",
                "referer": "https://www.bilibili.com",
            },
            params={
                "uploads": "",
                "output": "json",
                "profile": "ugcfx/bup",
                "filesize": page.get_size(),
                "partsize": preupload["chunk_size"],
                "biz_id": preupload["biz_id"],
            },
        )
        if resp.status_code >= 400:
            self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
            raise ApiException("获取 upload_id 错误")

        data = json.loads(resp.text)

        if data["OK"] != 1:
            self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
            raise ApiException("获取 upload_id 错误：" + json.dumps(data))

        preupload["upload_id"] = data["upload_id"]

        # # 读取并上传视频元数据，这段代码暂时用不上
        # meta = ffmpeg.probe(page.path)
        # meta_format = meta["format"]
        # meta_video = list(map(lambda x: x if x["codec_type"] == "video" else None, meta["streams"]))
        # meta_video.remove(None)
        # meta_video = meta_video[0]

        # meta_audio = list(map(lambda x: x if x["codec_type"] == "audio" else None, meta["streams"]))
        # meta_audio.remove(None)
        # meta_audio = meta_audio[0]

        # meta_to_upload = json.dumps({
        #     "code": 0,
        #     "filename": os.path.splitext(os.path.basename(preupload["upos_uri"]))[0],
        #     "filesize": int(meta_format["size"]),
        #     "key_frames": [],
        #     "meta": {
        #         "audio_meta": meta_audio,
        #         "video_meta": meta_video,
        #         "container_meta": {
        #             "duration": round(float(meta_format["duration"]), 2),
        #             "format_name": meta_format["format_name"]
        #         }
        #     },
        #     "version": "2.3.7",
        #     "webVersion": "1.0.0"
        # })

        # # 预检元数据上传
        # async with session.get(api["url"], params={
        #     "name": "BUploader_meta.txt",
        #     "size": len(meta_to_upload),
        #     "r": "upos",
        #     "profile": "fxmeta/bup",
        #     "ssl": "0",
        #     "version": "2.10.3",
        #     "build": "2100300",
        # }, cookies=self.credential.get_cookies(),
        #     headers={
        #         "User-Agent": "Mozilla/5.0",
        #         "Referer": "https://www.bilibili.com"
        #     }, proxy=settings.proxy
        # ) as resp:
        #     if resp.status >= 400:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise NetworkException(resp.status, resp.reason)

        #     preupload_m = await resp.json()

        #     if preupload_m['OK'] != 1:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise ApiException(json.dumps(preupload_m))

        # url = self._get_upload_url(preupload_m)

        # # 获取 upload_id
        # async with session.post(url, params={
        #     "uploads": "",
        #     "output": "json"
        # }, headers={
        #     "x-upos-auth": preupload_m["auth"]
        # }, proxy=settings.proxy) as resp:
        #     if resp.status >= 400:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise NetworkException(resp.status, resp.reason)

        #     data = json.loads(await resp.text())
        #     if preupload_m['OK'] != 1:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise ApiException(json.dumps(preupload_m))

        #     upload_id = data["upload_id"]

        # size = len(meta_to_upload)
        # async with session.put(url, params={
        #     "partNumber": 1,
        #     "uploadId": upload_id,
        #     "chunk": 0,
        #     "chunks": 1,
        #     "size": size,
        #     "start": 0,
        #     "end": size,
        #     "total": size
        # }, headers={
        #     "x-upos-auth": preupload_m["auth"]
        # }, data=meta_to_upload, proxy=settings.proxy) as resp:
        #     if resp.status >= 400:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise NetworkException(resp.status, resp.reason)

        #     data = await resp.text()

        #     if data != 'MULTIPART_PUT_SUCCESS':
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise ApiException(json.dumps(preupload_m))

        # async with session.post(url,
        #     data=json.dumps({"parts": [{"partNumber": 1, "eTag": "etag"}]}),
        #     params={
        #         "output": "json",
        #         "name": "BUploader_meta.txt",
        #         "profile": "",
        #         "uploadId": upload_id,
        #         "biz_id": ""
        #     },
        #     headers={
        #         "x-upos-auth": preupload_m["auth"]
        #     }, proxy=settings.proxy
        # ) as resp:
        #     if resp.status >= 400:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise NetworkException(resp.status, resp.reason)

        #     data = json.loads(await resp.text())

        #     if data['OK'] != 1:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise ApiException(json.dumps(data))

        return preupload

    async def _main(self) -> dict:
        videos = []
        for page in self.pages:
            data = await self._upload_page(page)
            videos.append(
                {
                    "title": page.title,
                    "desc": page.description,
                    "filename": data["filename"],  # type: ignore
                    "cid": data["cid"],  # type: ignore
                }
            )

        cover_url = await self._upload_cover()

        result = await self._submit(videos, cover_url)

        self.dispatch(VideoUploaderEvents.COMPLETED.value, result)
        return result

    async def start(self) -> dict:  # type: ignore
        """
        开始上传

        Returns:
            dict: 返回带有 bvid 和 aid 的字典。
        """

        self.line = await _choose_line(self.line)
        task = create_task(self._main())
        self.__task = task

        try:
            result = await task
            self.__task = None
            return result
        except CancelledError:
            # 忽略 task 取消异常
            pass
        except Exception as e:
            self.dispatch(VideoUploaderEvents.FAILED.value, {"err": e})
            raise e

    async def _upload_cover(self) -> str:
        """
        上传封面

        Returns:
            str: 封面 URL
        """
        self.dispatch(VideoUploaderEvents.PRE_COVER.value, None)
        try:
            cover_url = await upload_cover(cover=self.cover, credential=self.credential)
            self.dispatch(VideoUploaderEvents.AFTER_COVER.value, {"url": cover_url})
            return cover_url
        except Exception as e:
            self.dispatch(VideoUploaderEvents.COVER_FAILED.value, {"err": e})
            raise e

    async def _upload_page(self, page: VideoUploaderPage) -> dict:
        """
        上传分 P

        Args:
            page (VideoUploaderPage): 分 P 对象

        Returns:
            str: 分 P 文件 ID，用于 submit 时的 $.videos[n].filename 字段使用。
        """
        preupload = await self._preupload(page)
        self.dispatch(VideoUploaderEvents.PRE_PAGE.value, {"page": page})

        page_size = page.get_size()
        # 所有分块起始位置
        chunk_offset_list = list(range(0, page_size, preupload["chunk_size"]))
        # 分块总数
        total_chunk_count = len(chunk_offset_list)
        # 并发上传分块
        chunk_number = 0
        # 上传队列
        chunks_pending = []
        # 缓存 upload_id，这玩意只能从上传的分块预检结果获得
        upload_id = preupload["upload_id"]
        for offset in chunk_offset_list:
            chunks_pending.insert(
                0,
                self._upload_chunk(
                    page, offset, chunk_number, total_chunk_count, preupload
                ),
            )
            chunk_number += 1

        while chunks_pending:
            tasks = []

            while len(tasks) < preupload["threads"] and len(chunks_pending) > 0:
                tasks.append(create_task(chunks_pending.pop()))

            result = await asyncio.gather(*tasks)

            for r in result:
                if not r["ok"]:
                    chunks_pending.insert(
                        0,
                        self._upload_chunk(
                            page,
                            r["offset"],
                            r["chunk_number"],
                            total_chunk_count,
                            preupload,
                        ),
                    )

        data = await self._complete_page(page, total_chunk_count, preupload, upload_id)

        self.dispatch(VideoUploaderEvents.AFTER_PAGE.value, {"page": page})

        return data

    @staticmethod
    def _get_upload_url(line: dict, preupload: dict) -> str:
        # 上传目标 URL
        if re.match(
            r"//upos-(sz|cs)-upcdn(bda2|ws|qn)\.bilivideo\.com", preupload["endpoint"]
        ):
            new_endpoint = re.sub(
                r"upcdn(bda2|qn|ws)", f'upcdn{line["upcdn"]}', preupload["endpoint"]
            )
            return (
                f'https:{new_endpoint}/{preupload["upos_uri"].removeprefix("upos://")}'
            )
        return f'https:{preupload["endpoint"]}/{preupload["upos_uri"].removeprefix("upos://")}'

    async def _upload_chunk(
        self,
        page: VideoUploaderPage,
        offset: int,
        chunk_number: int,
        total_chunk_count: int,
        preupload: dict,
    ) -> dict:
        """
        上传视频分块

        Args:
            page (VideoUploaderPage): 分 P 对象
            offset (int): 分块起始位置
            chunk_number (int): 分块编号
            total_chunk_count (int): 总分块数
            preupload (dict): preupload 数据

        Returns:
            dict: 上传结果和分块信息。
        """
        chunk_event_callback_data = {
            "page": page,
            "offset": offset,
            "chunk_number": chunk_number,
            "total_chunk_count": total_chunk_count,
        }
        self.dispatch(VideoUploaderEvents.PRE_CHUNK.value, chunk_event_callback_data)
        session = get_session()

        stream = open(page.path, "rb")
        stream.seek(offset)
        chunk = stream.read(preupload["chunk_size"])
        stream.close()

        # 上传目标 URL
        url = self._get_upload_url(self.line, preupload)

        err_return = {
            "ok": False,
            "chunk_number": chunk_number,
            "offset": offset,
            "page": page,
        }

        real_chunk_size = len(chunk)

        params = {
            "partNumber": str(chunk_number + 1),
            "uploadId": str(preupload["upload_id"]),
            "chunk": str(chunk_number),
            "chunks": str(total_chunk_count),
            "size": str(real_chunk_size),
            "start": str(offset),
            "end": str(offset + real_chunk_size),
            "total": page.get_size(),
        }

        ok_return = {
            "ok": True,
            "chunk_number": chunk_number,
            "offset": offset,
            "page": page,
        }

        try:
            resp = await session.put(
                url,
                data=chunk,  # type: ignore
                params=params,
                headers={"x-upos-auth": preupload["auth"]},
            )
            if resp.status_code >= 400:
                chunk_event_callback_data["info"] = f"Status {resp.status_code}"
                self.dispatch(
                    VideoUploaderEvents.CHUNK_FAILED.value,
                    chunk_event_callback_data,
                )
                return err_return

            data = resp.text

            if data != "MULTIPART_PUT_SUCCESS" and data != "":
                chunk_event_callback_data["info"] = "分块上传失败"
                self.dispatch(
                    VideoUploaderEvents.CHUNK_FAILED.value,
                    chunk_event_callback_data,
                )
                return err_return

        except Exception as e:
            chunk_event_callback_data["info"] = str(e)
            self.dispatch(
                VideoUploaderEvents.CHUNK_FAILED.value, chunk_event_callback_data
            )
            return err_return

        self.dispatch(VideoUploaderEvents.AFTER_CHUNK.value, chunk_event_callback_data)
        return ok_return

    async def _complete_page(
        self, page: VideoUploaderPage, chunks: int, preupload: dict, upload_id: str
    ) -> dict:
        """
        提交分 P 上传

        Args:
            page (VideoUploaderPage): 分 P 对象

            chunks (int): 分块数量

            preupload (dict): preupload 数据

            upload_id (str): upload_id

        Returns:
            dict: filename: 该分 P 的标识符，用于最后提交视频。cid: 分 P 的 cid
        """
        self.dispatch(VideoUploaderEvents.PRE_PAGE_SUBMIT.value, {"page": page})

        data = {
            "parts": list(
                map(lambda x: {"partNumber": x, "eTag": "etag"}, range(1, chunks + 1))
            )
        }

        params = {
            "output": "json",
            "name": os.path.basename(page.path),
            "profile": "ugcfx/bup",
            "uploadId": upload_id,
            "biz_id": preupload["biz_id"],
        }

        url = self._get_upload_url(self.line, preupload)

        session = get_session()

        resp = await session.post(
            url=url,
            data=json.dumps(data),  # type: ignore
            headers={
                "x-upos-auth": preupload["auth"],
                "content-type": "application/json; charset=UTF-8",
            },
            params=params,
        )
        if resp.status_code >= 400:
            err = NetworkException(resp.status_code, "状态码错误，提交分 P 失败")
            self.dispatch(
                VideoUploaderEvents.PAGE_SUBMIT_FAILED.value,
                {"page": page, "err": err},
            )
            raise err

        data = json.loads(resp.read())

        if data["OK"] != 1:
            err = ResponseCodeException(-1, f'提交分 P 失败，原因: {data["message"]}')
            self.dispatch(
                VideoUploaderEvents.PAGE_SUBMIT_FAILED.value,
                {"page": page, "err": err},
            )
            raise err

        self.dispatch(VideoUploaderEvents.AFTER_PAGE_SUBMIT.value, {"page": page})

        return {
            "filename": os.path.splitext(data["key"].removeprefix("/"))[0],
            "cid": preupload["biz_id"],
        }

    async def _submit(self, videos: list, cover_url: str = "") -> dict:
        """
        提交视频

        Args:
            videos (list): 视频列表

            cover_url (str, optional): 封面 URL.

        Returns:
            dict: 含 bvid 和 aid 的字典
        """
        meta = copy(
            self.meta.__dict__() if isinstance(self.meta, VideoMeta) else self.meta
        )
        meta["cover"] = cover_url
        meta["videos"] = videos

        self.dispatch(VideoUploaderEvents.PRE_SUBMIT.value, deepcopy(meta))

        meta["csrf"] = self.credential.bili_jct  # csrf 不需要 print
        api = _API["submit"]

        try:
            params = {"csrf": self.credential.bili_jct, "t": time.time() * 1000}
            # headers = {"content-type": "application/json"}
            # 已有 json_body，似乎不需要单独设置 content-type
            resp = (
                await Api(
                    **api, credential=self.credential, no_csrf=True, json_body=True
                )
                .update_params(**params)
                .update_data(**meta)
                # .update_headers(**headers)
                .result
            )
            self.dispatch(VideoUploaderEvents.AFTER_SUBMIT.value, resp)
            return resp

        except Exception as err:
            self.dispatch(VideoUploaderEvents.SUBMIT_FAILED.value, {"err": err})
            raise err

    async def abort(self):
        """
        中断上传
        """
        if self.__task:
            self.__task.cancel("用户手动取消")

        self.dispatch(VideoUploaderEvents.ABORTED.value, None)


async def get_missions(tid: int = 0, credential: Union[Credential, None] = None) -> dict:
    """
    获取活动信息

    Args:
        tid        (int, optional)       : 分区 ID. Defaults to 0.

        credential (Credential, optional): 凭据. Defaults to None.

    Returns:
        dict API 调用返回结果
    """
    api = _API["missions"]

    params = {"tid": tid}

    return await Api(**api, credential=credential).update_params(**params).result


class VideoEditorEvents(Enum):
    """
    视频稿件编辑事件枚举

    + PRELOAD       : 加载数据前
    + AFTER_PRELOAD : 加载成功
    + PRELOAD_FAILED: 加载失败
    + PRE_COVER     : 上传封面前
    + AFTER_COVER   : 上传封面后
    + COVER_FAILED  : 上传封面失败
    + PRE_SUBMIT    : 提交前
    + AFTER_SUBMIT  : 提交后
    + SUBMIT_FAILED : 提交失败
    + COMPLETED     : 完成
    + ABOTRED       : 停止
    + FAILED        : 失败
    """

    PRELOAD = "PRELOAD"
    AFTER_PRELOAD = "AFTER_PRELOAD"
    PRELOAD_FAILED = "PRELOAD_FAILED"

    PRE_COVER = "PRE_COVER"
    AFTER_COVER = "AFTER_COVER"
    COVER_FAILED = "COVER_FAILED"

    PRE_SUBMIT = "PRE_SUBMIT"
    SUBMIT_FAILED = "SUBMIT_FAILED"
    AFTER_SUBMIT = "AFTER_SUBMIT"

    COMPLETED = "COMPLETE"
    ABORTED = "ABORTED"
    FAILED = "FAILED"


class VideoEditor(AsyncEvent):
    """
    视频稿件编辑

    Attributes:
        bvid (str)             : 稿件 BVID

        meta (dict)            : 视频信息

        cover_path (str)       : 封面路径. Defaults to None(不更换封面).

        credential (Credential): 凭据类. Defaults to None.
    """

    def __init__(
        self,
        bvid: str,
        meta: dict,
        cover: Union[str, Picture] = "",
        credential: Union[Credential, None] = None,
    ):
        """
        Args:
            bvid (str)                    : 稿件 BVID

            meta (dict)                   : 视频信息

            cover (str | Picture)         : 封面地址. Defaults to None(不更改封面).

            credential (Credential | None): 凭据类. Defaults to None.

        meta 参数示例: (保留 video, cover, tid, aid 字段)

        ``` json
        {
            "title": "str: 标题",
            "copyright": "int: 是否原创，0 否 1 是",
            "tag": "标签. 用,隔开. ",
            "desc_format_id": "const int: 0",
            "desc": "str: 描述",
            "dynamic": "str: 动态信息",
            "interactive": "const int: 0",
            "new_web_edit": "const int: 1",
            "act_reserve_create": "const int: 0",
            "handle_staff": "const bool: false",
            "topic_grey": "const int: 1",
            "no_reprint": "int: 是否显示“未经允许禁止转载”. 0 否 1 是",
            "subtitles # 字幕设置": {
                "lan": "str: 字幕投稿语言，不清楚作用请将该项设置为空",
                "open": "int: 是否启用字幕投稿，1 or 0"
            },
            "web_os": "const int: 2"
        }
        ```
        """
        super().__init__()
        self.bvid = bvid
        self.meta = meta
        self.credential = credential if credential else Credential()
        self.cover_path = cover
        self.__old_configs = {}
        self.meta["aid"] = bvid2aid(bvid)
        self.__task: Union[Task, None] = None

    async def _fetch_configs(self):
        """
        在本地缓存原来的上传信息
        """
        self.dispatch(VideoEditorEvents.PRELOAD.value)
        try:
            api = _API["upload_args"]
            params = {"bvid": self.bvid}
            self.__old_configs = (
                await Api(**api, credential=self.credential)
                .update_params(**params)
                .result
            )
        except Exception as e:
            self.dispatch(VideoEditorEvents.PRELOAD_FAILED.value, {"err", e})
            raise e
        self.dispatch(
            VideoEditorEvents.AFTER_PRELOAD.value, {"data": self.__old_configs}
        )

    async def _change_cover(self) -> None:
        """
        更换封面

        Returns:
            None
        """
        if self.cover_path == "":
            return
        self.dispatch(VideoEditorEvents.PRE_COVER.value, None)
        try:
            pic = (
                self.cover_path
                if isinstance(self.cover_path, Picture)
                else Picture().from_file(self.cover_path)
            )
            resp = await upload_cover(pic, self.credential)
            self.dispatch(VideoEditorEvents.AFTER_COVER.value, {"url": resp["url"]})
            # not sure if this key changed to "url" as well
            self.meta["cover"] = resp["image_url"]
        except Exception as e:
            self.dispatch(VideoEditorEvents.COVER_FAILED.value, {"err": e})
            raise e

    async def _submit(self):
        api = _API["edit"]
        data = self.meta
        data["csrf"] = self.credential.bili_jct
        self.dispatch(VideoEditorEvents.PRE_SUBMIT.value)
        try:
            params = ({"csrf": self.credential.bili_jct, "t": int(time.time())},)
            headers = {
                "content-type": "application/json;charset=UTF-8",
                "referer": "https://member.bilibili.com",
                "user-agent": "Mozilla/5.0",
            }
            resp = (
                await Api(**api, credential=self.credential, no_csrf=True)
                .update_params(**params)
                .update_data(**data)
                .update_headers(**headers)
                .result
            )
            self.dispatch(VideoEditorEvents.AFTER_SUBMIT.value, resp)
        except Exception as e:
            self.dispatch(VideoEditorEvents.SUBMIT_FAILED.value, {"err", e})
            raise e

    async def _main(self) -> dict:
        await self._fetch_configs()
        self.meta["videos"] = []
        cnt = 0
        for v in self.__old_configs["videos"]:
            self.meta["videos"].append(
                {"title": v["title"], "desc": v["desc"], "filename": v["filename"]}
            )
            self.meta["videos"][-1]["cid"] = await Video(self.bvid).get_cid(cnt)
            cnt += 1
        self.meta["cover"] = self.__old_configs["archive"]["cover"]
        self.meta["tid"] = self.__old_configs["archive"]["tid"]
        await self._change_cover()
        await self._submit()
        self.dispatch(VideoEditorEvents.COMPLETED.value)
        return {"bvid": self.bvid}

    async def start(self) -> dict:  # type: ignore
        """
        开始更改

        Returns:
            dict: 返回带有 bvid 和 aid 的字典。
        """

        task = create_task(self._main())
        self.__task = task

        try:
            result = await task
            self.__task = None
            return result
        except CancelledError:
            # 忽略 task 取消异常
            pass
        except Exception as e:
            self.dispatch(VideoEditorEvents.FAILED.value, {"err": e})
            raise e

    async def abort(self):
        """
        中断更改
        """
        if self.__task:
            self.__task.cancel("用户手动取消")

        self.dispatch(VideoEditorEvents.ABORTED.value, None)
