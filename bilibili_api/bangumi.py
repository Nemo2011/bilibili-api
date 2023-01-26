"""
bilibili_api.bangumi

番剧相关

概念：
+ media_id: 番剧本身的 ID，有时候也是每季度的 ID，如 https://www.bilibili.com/bangumi/media/md28231846/
+ season_id: 每季度的 ID
+ episode_id: 每集的 ID，如 https://www.bilibili.com/bangumi/play/ep374717

"""

import datetime
import os
from enum import Enum
from typing import Any, Tuple, Union, List
import httpx

import requests

from bilibili_api.utils.Danmaku import Danmaku

from . import settings

from .utils.utils import get_api
from .utils.Credential import Credential
from .utils.network_httpx import get_session, request
from .exceptions.ResponseException import ResponseException
from .exceptions.ApiException import ApiException
from .video import Video

import json
import re

API = get_api("bangumi")


episode_data_cache = {}


class BangumiCommentOrder(Enum):
    """
    短评 / 长评 排序方式

    + DEFAULT: 默认
    + CTIME: 发布时间倒序
    """

    DEFAULT = 0
    CTIME = 1


class BangumiType(Enum):
    """
    番剧类型

    + BANGUMI: 番剧
    + FT: 影视
    + GUOCHUANG: 国创
    """
    BANGUMI = 1
    FT = 3
    GUOCHUANG = 4


async def get_timeline(type_: BangumiType, before: int = 7, after: int = 0) -> dict:
    """
    获取番剧时间线

    Args:
        type_(BangumiType): 番剧类型
        before(int)       : 几天前开始(0~7), defaults to 7
        after(int)        : 几天后结束(0~7), defaults to 0
    """
    api = API["info"]["timeline"]
    params = {
        "types": type_.value,
        "before": before,
        "after": after
    }
    return await request("GET", api["url"], params=params)


class INDEX_FILTER:
    '''
    番剧索引相关固定参数以及值
    '''
    class Style:
        '''
        Style 请手动传值
        '''
        Anime = [
            {"value": -1, "name": "全部"},
            {"value": 10010, "name": "原创"},
            {"value": 10011, "name": "漫画改"},
            {"value": 10012, "name": "小说改"},
            {"value": 10013, "name": "游戏改"},
            {"value": 10102, "name": "特摄"},
            {"value": 10015, "name": "布袋戏"},
            {"value": 10016, "name": "热血"},
            {"value": 10017, "name": "穿越"},
            {"value": 10018, "name": "奇幻"},
            {"value": 10020, "name": "战斗"},
            {"value": 10021, "name": "搞笑"},
            {"value": 10022, "name": "日常"},
            {"value": 10023, "name": "科幻"},
            {"value": 10024, "name": "萌系"},
            {"value": 10025, "name": "治愈"},
            {"value": 10026, "name": "校园"},
            {"value": 10027, "name": "少儿"},
            {"value": 10028, "name": "泡面"},
            {"value": 10029, "name": "恋爱"},
            {"value": 10030, "name": "少女"},
            {"value": 10031, "name": "魔法"},
            {"value": 10032, "name": "冒险"},
            {"value": 10033, "name": "历史"},
            {"value": 10034, "name": "架空"},
            {"value": 10035, "name": "机战"},
            {"value": 10036, "name": "神魔"},
            {"value": 10037, "name": "声控"},
            {"value": 10038, "name": "运动"},
            {"value": 10039, "name": "励志"},
            {"value": 10040, "name": "音乐"},
            {"value": 10041, "name": "推理"},
            {"value": 10042, "name": "社团"},
            {"value": 10043, "name": "智斗"},
            {"value": 10044, "name": "催泪"},
            {"value": 10045, "name": "美食"},
            {"value": 10046, "name": "偶像"},
            {"value": 10047, "name": "乙女"},
            {"value": 10048, "name": "职场"}
        ]
        Movie = [
            {"value": -1, "name": "全部"},
            {"value": 10104, "name": "短片"},
            {"value": 10050, "name": "剧情"},
            {"value": 10051, "name": "喜剧"},
            {"value": 10052, "name": "爱情"},
            {"value": 10053, "name": "动作"},
            {"value": 10054, "name": "恐怖"},
            {"value": 10023, "name": "科幻"},
            {"value": 10055, "name": "犯罪"},
            {"value": 10056, "name": "惊悚"},
            {"value": 10057, "name": "悬疑"},
            {"value": 10018, "name": "奇幻"},
            {"value": 10058, "name": "战争"},
            {"value": 10059, "name": "动画"},
            {"value": 10060, "name": "传记"},
            {"value": 10061, "name": "家庭"},
            {"value": 10062, "name": "歌舞"},
            {"value": 10033, "name": "历史"},
            {"value": 10032, "name": "冒险"},
            {"value": 10063, "name": "纪实"},
            {"value": 10064, "name": "灾难"},
            {"value": 10011, "name": "漫画改"},
            {"value": 10012, "name": "小说改"}
        ]
        Documentary = [
            {"value": -1, "name": "全部"},
            {"value": 10033, "name": "历史"},
            {"value": 10045, "name": "美食"},
            {"value": 10065, "name": "人文"},
            {"value": 10066, "name": "科技"},
            {"value": 10067, "name": "探险"},
            {"value": 10068, "name": "宇宙"},
            {"value": 10069, "name": "萌宠"},
            {"value": 10070, "name": "社会"},
            {"value": 10071, "name": "动物"},
            {"value": 10072, "name": "自然"},
            {"value": 10073, "name": "医疗"},
            {"value": 10074, "name": "军事"},
            {"value": 10064, "name": "灾难"},
            {"value": 10075, "name": "罪案"},
            {"value": 10076, "name": "神秘"},
            {"value": 10077, "name": "旅行"},
            {"value": 10038, "name": "运动"},
            {"value": -10, "name": "电影"}
        ]
        Guochuang = [
            {"value": -1, "name": "全部"},
            {"value": 10010, "name": "原创"},
            {"value": 10011, "name": "漫画改"},
            {"value": 10012, "name": "小说改"},
            {"value": 10013, "name": "游戏改"},
            {"value": 10014, "name": "动态漫"},
            {"value": 10015, "name": "布袋戏"},
            {"value": 10016, "name": "热血"},
            {"value": 10018, "name": "奇幻"},
            {"value": 10019, "name": "玄幻"},
            {"value": 10020, "name": "战斗"},
            {"value": 10021, "name": "搞笑"},
            {"value": 10078, "name": "武侠"},
            {"value": 10022, "name": "日常"},
            {"value": 10023, "name": "科幻"},
            {"value": 10024, "name": "萌系"},
            {"value": 10025, "name": "治愈"},
            {"value": 10057, "name": "悬疑"},
            {"value": 10026, "name": "校园"},
            {"value": 10027, "name": "少儿"},
            {"value": 10028, "name": "泡面"},
            {"value": 10029, "name": "恋爱"},
            {"value": 10030, "name": "少女"},
            {"value": 10031, "name": "魔法"},
            {"value": 10033, "name": "历史"},
            {"value": 10035, "name": "机战"},
            {"value": 10036, "name": "神魔"},
            {"value": 10037, "name": "声控"},
            {"value": 10038, "name": "运动"},
            {"value": 10039, "name": "励志"},
            {"value": 10040, "name": "音乐"},
            {"value": 10041, "name": "推理"},
            {"value": 10042, "name": "社团"},
            {"value": 10043, "name": "智斗"},
            {"value": 10044, "name": "催泪"},
            {"value": 10045, "name": "美食"},
            {"value": 10046, "name": "偶像"},
            {"value": 10047, "name": "乙女"},
            {"value": 10048, "name": "职场"},
            {"value": 10049, "name": "古风"}
        ]
        TV = [
            {"value": -1, "name": "全部"},
            {"value": 10010, "name": "原创"},
            {"value": 10011, "name": "漫画改"},
            {"value": 10012, "name": "小说改"},
            {"value": 10013, "name": "游戏改"},
            {"value": 10014, "name": "动态漫"},
            {"value": 10015, "name": "布袋戏"},
            {"value": 10016, "name": "热血"},
            {"value": 10018, "name": "奇幻"},
            {"value": 10019, "name": "玄幻"},
            {"value": 10020, "name": "战斗"},
            {"value": 10021, "name": "搞笑"},
            {"value": 10078, "name": "武侠"},
            {"value": 10022, "name": "日常"},
            {"value": 10023, "name": "科幻"},
            {"value": 10024, "name": "萌系"},
            {"value": 10025, "name": "治愈"},
            {"value": 10057, "name": "悬疑"},
            {"value": 10026, "name": "校园"},
            {"value": 10027, "name": "少儿"},
            {"value": 10028, "name": "泡面"},
            {"value": 10029, "name": "恋爱"},
            {"value": 10030, "name": "少女"},
            {"value": 10031, "name": "魔法"},
            {"value": 10033, "name": "历史"},
            {"value": 10035, "name": "机战"},
            {"value": 10036, "name": "神魔"},
            {"value": 10037, "name": "声控"},
            {"value": 10038, "name": "运动"},
            {"value": 10039, "name": "励志"},
            {"value": 10040, "name": "音乐"},
            {"value": 10041, "name": "推理"},
            {"value": 10042, "name": "社团"},
            {"value": 10043, "name": "智斗"},
            {"value": 10044, "name": "催泪"},
            {"value": 10045, "name": "美食"},
            {"value": 10046, "name": "偶像"},
            {"value": 10047, "name": "乙女"},
            {"value": 10048, "name": "职场"},
            {"value": 10049, "name": "古风"}
        ]

    class Type(Enum):
        ANIME = 1
        MOVIE = 2
        DOCUMENTARY = 3
        GUOCHUANG = 4
        TV = 5

    class VERSION(Enum):
        '''
        番剧版本
        '''
        ALL = -1
        MAIN = 1
        FILM = 2
        OTHER = 3

    class SPOKEN_LANGUAGE_TYPE(Enum):
        '''
        配音
        '''
        ALL = -1
        ORIGINAL = 1
        CHINESE = 2

    class FINISH_STATUS(Enum):
        '''
        番剧状态
        '''
        ALL = -1
        FINISHED = 1
        UNFINISHED = 0

    class COPYRIGHT(Enum):
        '''
        版权方
        '''
        ALL = -1
        EXCLUSIVE = 3
        OTHER = "1,2,4"

    class SEASON(Enum):
        '''
        季度
        '''
        ALL = -1
        SUMMER = 7
        AUTUMN = 10
        WINTER = 1
        SPRING = 4

    class YEAR(Enum):
        '''
        年份
        '''
        ALL = -1
        YEAR_2023 = "[2023,2024)"
        YEAR_2022 = "[2022,2023)"
        YEAR_2021 = "[2021,2022)"
        YEAR_2020 = "[2020,2021)"
        YEAR_2019 = "[2019,2020)"
        YEAR_2018 = "[2018,2019)"
        YEAR_2017 = "[2017,2018)"
        YEAR_2016 = "[2016,2017)"
        YEAR_2015 = "[2015,2016)"
        YEAR_FROM_2014_TO_2010 = "[2010,2015)"
        YEAR_FROM_2009_TO_2005 = "[2005,2010)"
        YEAR_FROM_2004_TO_2000 = "[2000,2005)"
        YEAR_1990S = "[1990,2000)"
        YEAR_1980S = "[1980,1990)"
        YEAR_BEFORE_1980 = "[,1980)"

    class RELEASE_DATE(Enum):
        '''
        发布日期
        '''
        ALL = -1
        YEAR_2023 = "[2023-01-01 00:00:00,2024-01-01 00:00:00)"
        YEAR_2022 = "[2022-01-01 00:00:00,2023-01-01 00:00:00)"
        YEAR_2021 = "[2021-01-01 00:00:00,2022-01-01 00:00:00)"
        YEAR_2020 = "[2020-01-01 00:00:00,2021-01-01 00:00:00)"
        YEAR_2019 = "[2019-01-01 00:00:00,2020-01-01 00:00:00)"
        YEAR_2018 = "[2018-01-01 00:00:00,2019-01-01 00:00:00)"
        YEAR_2017 = "[2017-01-01 00:00:00,2018-01-01 00:00:00)"
        YEAR_2016 = "[2016-01-01 00:00:00,2017-01-01 00:00:00)"
        YEAR_FROM_2015_TO_2010 = "[2010-01-01 00:00:00,2016-01-01 00:00:00)"
        YEAR_FROM_2009_TO_2005 = "[2005-01-01 00:00:00,2010-01-01 00:00:00)"
        YEAR_FROM_2004_TO_2000 = "[2000-01-01 00:00:00,2005-01-01 00:00:00)"
        YEAR_1990S = "[1990-01-01 00:00:00,2000-01-01 00:00:00)"
        YEAR_1980S = "[1980-01-01 00:00:00,1990-01-01 00:00:00)"
        YEAR_BEFORE_1980 = "[,1980-01-01 00:00:00)"

    class PRODUCER(Enum):
        '''
        制作方
        '''
        ALL = -1
        CCTV = 4
        BBC = 1
        DISCOVERY = 7
        NATIONAL_GEOGRAPHIC = 14
        NHK = 2
        HISTORY = 6
        SATELLITE = 8
        SELF = 9
        ITV = 5
        SKY = 3
        ZDF = 10
        PARTNER = 11
        DOMESTIC_OTHER = 12
        FOREIGN_OTHER = 13

    class PAYMENT(Enum):
        '''
        观看条件
        '''
        ALL = -1
        FREE = 1
        PAID = "2,6"
        VIP = "4,6"

    class AREA(Enum):
        '''
        地区
        '''
        ALL = "-1"
        CHINA = "1,6,7"
        CHINESE_MAINLAND = "1"
        CHINESE_HONGKONG_AND_MACAO = "6,7"
        JAPAN = "2"
        AMERICA = "3"
        UK = "4"
        KOREA = "8"
        FRANCE = "9"
        THAILAND = "10"
        GERMANY = "15"
        ITALY = "35"
        SPAIN = "13"
        OTHER = "5,11,12,14,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70"

    class SORT(Enum):
        '''
        排序方式
        '''
        DESC = "0"
        ASC = "1"

    class ORDER(Enum):
        '''
        更新时间 0
        排序字段
        弹幕数量 1
        播放数量 2
        追番人数 3
        最高评分 4
        开播时间 5
        上映日期 6
        '''
        UPDATE = "0"
        DANMAKU = "1"
        PLAY = "2"
        FOLLOWER = "3"
        SCORE = "4"
        RELEASE = "5"
        Movie_RELEASE = "6"


def get_style_list(index_type: INDEX_FILTER.Type) -> list:
    if index_type == INDEX_FILTER.Type.ANIME:
        return INDEX_FILTER.Style.Anime
    elif index_type == INDEX_FILTER.Type.MOVIE:
        return INDEX_FILTER.Style.Movie
    elif index_type == INDEX_FILTER.Type.TV:
        return INDEX_FILTER.Style.TV
    elif index_type == INDEX_FILTER.Type.DOCUMENTARY:
        return INDEX_FILTER.Style.Documentary
    elif index_type == INDEX_FILTER.Type.GUOCHUANG:
        return INDEX_FILTER.Style.Guochuang
    else:
        raise ValueError("index_type 参数错误")


def get_style(index_type: INDEX_FILTER.Type, style: Union[int, str]) -> int:
    '''
    检查 style 是否存在或通过 style 获取 style_id
    '''
    style_list = get_style_list(index_type)
    if isinstance(style, int):
        for style in style_list:
            if style["value"] == style:
                return style["value"]
    elif isinstance(style, str) is not None:
        for style in style_list:
            if style["name"] == style:
                return style["value"]
    else:
        raise ValueError("style 不存在")


class Index_Filter_Meta:
    '''
    Index Filter 元数据
    用于补全有哪些参数可传入
    '''
    class Anime:
        def __init__(self,
                     season_version: INDEX_FILTER.VERSION = INDEX_FILTER.VERSION.ALL,
                     spoken_language_type: INDEX_FILTER.SPOKEN_LANGUAGE_TYPE = INDEX_FILTER.SPOKEN_LANGUAGE_TYPE.ALL,
                     area: INDEX_FILTER.AREA = INDEX_FILTER.AREA.ALL,
                     is_finish: INDEX_FILTER.FINISH_STATUS = INDEX_FILTER.FINISH_STATUS.ALL,
                     copyright: INDEX_FILTER.COPYRIGHT = INDEX_FILTER.COPYRIGHT.ALL,
                     payment: INDEX_FILTER.PAYMENT = INDEX_FILTER.PAYMENT.ALL,
                     season_month: INDEX_FILTER.SEASON = INDEX_FILTER.SEASON.ALL,
                     year: INDEX_FILTER.YEAR = INDEX_FILTER.YEAR.ALL,
                     style_id: Union[int, str] = -1
                     ) -> None:
            '''
            Anime Meta
            Args:
                style_id (int, str): 为 style 的 name 或 value
            '''
            self.season_version = season_version
            self.spoken_language_type = spoken_language_type
            self.area = area
            self.is_finish = is_finish
            self.copyright = copyright
            self.season_status = payment
            self.season_month = season_month
            self.year = year
            self.style_id = get_style(
                index_type=INDEX_FILTER.Type.ANIME, style=style_id)

    class Movie:
        def __init__(self,
                     area: INDEX_FILTER.AREA = INDEX_FILTER.AREA.ALL,
                     release_date: INDEX_FILTER.RELEASE_DATE = INDEX_FILTER.RELEASE_DATE.ALL,
                     style_id: Union[int, str] = -1,
                     payment: INDEX_FILTER.PAYMENT = INDEX_FILTER.PAYMENT.ALL
                     ) -> None:
            '''
            Movie Meta
            Args:
                style_id (int, str): 为 style 的 name 或 value
            '''
            self.area = area
            self.release_date = release_date
            self.style_id = get_style(
                index_type=INDEX_FILTER.Type.MOVIE, style=style_id)
            self.season_status = payment

    class Documentary:
        def __init__(self,
                     release_date: INDEX_FILTER.RELEASE_DATE = INDEX_FILTER.RELEASE_DATE.ALL,
                     style_id: Union[int, str] = -1,
                     payment: INDEX_FILTER.PAYMENT = INDEX_FILTER.PAYMENT.ALL,
                     producer_id: INDEX_FILTER.PRODUCER = INDEX_FILTER.PRODUCER.ALL
                     ) -> None:
            '''
            Documentary Meta
            Args:
                style_id (int, str): 为 style 的 name 或 value
            '''
            self.release_date = release_date
            self.style_id = get_style(
                index_type=INDEX_FILTER.Type.DOCUMENTARY, style=style_id)
            self.season_status = payment
            self.producer_id = producer_id

    class TV:
        def __init__(self,
                     area: INDEX_FILTER.AREA = INDEX_FILTER.AREA.ALL,
                     release_date: INDEX_FILTER.RELEASE_DATE = INDEX_FILTER.RELEASE_DATE.ALL,
                     style_id: Union[int, str] = -1,
                     payment: INDEX_FILTER.PAYMENT = INDEX_FILTER.PAYMENT.ALL
                     ) -> None:
            '''
            TV Meta
            Args:
                style_id (int, str): 为 style 的 name 或 value
            '''
            self.area = area
            self.release_date = release_date
            self.style_id = get_style(
                index_type=INDEX_FILTER.Type.TV, style=style_id)
            self.season_status = payment

    class Guochuang:
        def __init__(self,
                     season_version: INDEX_FILTER.VERSION = INDEX_FILTER.VERSION.ALL,
                     is_finish: INDEX_FILTER.FINISH_STATUS = INDEX_FILTER.FINISH_STATUS.ALL,
                     copyright: INDEX_FILTER.COPYRIGHT = INDEX_FILTER.COPYRIGHT.ALL,
                     payment: INDEX_FILTER.PAYMENT = INDEX_FILTER.PAYMENT.ALL,
                     year: INDEX_FILTER.YEAR = INDEX_FILTER.YEAR.ALL,
                     style_id: Union[int, str] = -1,
                     ) -> None:
            '''
            Guochuang Meta
            Args:
                style_id (int, str): 为 style 的 name 或 value
            '''
            self.season_version = season_version
            self.is_finish = is_finish
            self.copyright = copyright
            self.season_status = payment
            self.year = year
            self.style_id = get_style(
                index_type=INDEX_FILTER.Type.GUOCHUANG, style=style_id)


async def get_index_by_filters(filters: Index_Filter_Meta = Index_Filter_Meta.Anime(),
                               order: INDEX_FILTER.ORDER = INDEX_FILTER.ORDER.FOLLOWER,
                               sort: INDEX_FILTER.SORT = INDEX_FILTER.SORT.DESC,
                               pn: int = 1,
                               ps: int = 20,
                               ) -> dict:
    '''
    查询番剧索引
    请先通过 Index_Filter_Meta 选择需要的索引，构造 filters

    Args:
        filters (Index_Filter_Meta, optional): 筛选条件. Defaults to Index_Filter_Meta.Anime().
        order (BANGUMI_INDEX.ORDER, optional): 排序字段. Defaults to Follower.
        sort (BANGUMI_INDEX.SORT, optional): 排序方式. Defaults to DESC.
        pn (int, optional): 页数. Defaults to 1.
        ps (int, optional): 每页数量. Defaults to 20.

    Returns:
        dict: 调用 API 返回的结果
    '''
    api = API["info"]["index"]

    # 必要参数 season_type、type
    params = {}
    if isinstance(filters, Index_Filter_Meta.Anime):
        params["season_type"] = INDEX_FILTER.Type.ANIME.value
    elif isinstance(filters, Index_Filter_Meta.Movie):
        params["season_type"] = INDEX_FILTER.Type.MOVIE.value
    elif isinstance(filters, Index_Filter_Meta.Documentary):
        params["season_type"] = INDEX_FILTER.Type.DOCUMENTARY.value
    elif isinstance(filters, Index_Filter_Meta.TV):
        params["season_type"] = INDEX_FILTER.Type.TV.value
    elif isinstance(filters, Index_Filter_Meta.Guochuang):
        params["season_type"] = INDEX_FILTER.Type.GUOCHUANG.value
    else:
        raise ValueError("参数 season_type 的值不在 INDEX_FILTER.Type 内")

    for key, value in filters.__dict__.items():
        if value is not None:
            params[key] = value.value

    if order in params:
        if order == INDEX_FILTER.ORDER.SCORE.value and sort == INDEX_FILTER.SORT.ASC.value:
            raise ValueError(
                "order 为 INDEX_FILTER.ORDER.SCORE 时，sort 不能为 INDEX_FILTER.SORT.ASC")
    # 常规参数
    params["order"] = order.value
    params["sort"] = sort.value
    params["page"] = pn
    params["pagesize"] = ps

    # params["st"] 未知参数，暂时不传
    # params["type"] 未知参数，为 1
    params["type"] = 1

    return await request("GET", api["url"], params=params)


class Bangumi:
    """
    番剧类

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(
        self,
        media_id: int = -1,
        ssid: int = -1,
        epid: int = -1,
        oversea: bool = False,
        credential: Union[Credential, None] = None,
    ):
        """
        Args:
            media_id   (int, optional)              : 番剧本身的 ID. Defaults to -1.
            ssid       (int, optional)              : 每季度的 ID. Defaults to -1.
            epid       (int, optional)              : 每集的 ID. Defaults to -1.
            oversea    (bool, optional)             : 是否要采用兼容的港澳台Api,用于仅限港澳台地区番剧的信息请求. Defaults to False.
            credential (Credential | None, optional): 凭据类. Defaults to None.
        """
        if media_id == -1 and ssid == -1 and epid == -1:
            raise ValueError("需要 Media_id 或 Season_id 或 epid 中的一个 !")
        self.credential = credential if credential else Credential()
        # 处理极端情况
        params = {}
        self.__ssid = ssid
        if self.__ssid == -1 and epid == -1:
            api = API["info"]["meta"]
            params = {"media_id": media_id}
            meta = requests.get(
                url=api["url"], params=params, cookies=self.credential.get_cookies()
            )
            meta.raise_for_status()
            # print(meta.json())
            self.__ssid = meta.json()["result"]["media"]["season_id"]
            params["media_id"] = media_id
        # 处理正常情况
        if self.__ssid != -1:
            params["season_id"] = self.__ssid
        if epid != -1:
            params["ep_id"] = epid
        self.oversea = oversea
        if oversea:
            api = API["info"]["collective_info_oversea"]
        else:
            api = API["info"]["collective_info"]
        req = requests.get(
            url=api["url"], params=params, cookies=self.credential.get_cookies()
        )
        req.raise_for_status()
        self.__raw = req.json()
        self.__epid = epid
        if not self.__raw.get("result"):
            raise ApiException("Api没有返回预期的结果")
        # 确认有结果后，取出数据
        self.__ssid = req.json()["result"]["season_id"]
        self.__media_id = req.json()["result"]["media_id"]
        if "up_info" in req.json()["result"]:
            self.__up_info = req.json()["result"]["up_info"]
        else:
            self.__up_info = {}
        # 获取剧集相关
        self.ep_list = req.json()["result"].get("episodes")
        self.ep_item = [{}]
        # 出海 Api 和国内的字段有些不同
        if self.ep_list:
            if self.oversea:
                self.ep_item = [
                    item for item in self.ep_list if item["ep_id"] == self.__epid
                ]
            else:
                self.ep_item = [
                    item for item in self.ep_list if item["id"] == self.__epid
                ]

    def get_media_id(self) -> int:
        return self.__media_id

    def get_season_id(self) -> int:
        return self.__ssid

    def get_up_info(self) -> dict:
        """
        番剧上传者信息 出差或者原版

        Returns:
            Api 相关字段
        """
        return self.__up_info

    def get_raw(self) -> Tuple[dict, bool]:
        """
        原始初始化数据

        Returns:
            Api 相关字段
        """
        return self.__raw, self.oversea

    def set_media_id(self, media_id: int) -> None:
        self.__init__(media_id=media_id, credential=self.credential)

    def set_ssid(self, ssid: int) -> None:
        self.__init__(ssid=ssid, credential=self.credential)

    async def get_meta(self) -> dict:
        """
        获取番剧元数据信息（评分，封面 URL，标题等）

        Returns:
            dict: 调用 API 返回的结果
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["meta"]
        params = {"media_id": self.__media_id}
        return await request("GET", api["url"], params, credential=credential)

    async def get_short_comment_list(
        self, order: BangumiCommentOrder = BangumiCommentOrder.DEFAULT, next: Union[str, None] = None
    ) -> dict:
        """
        获取短评列表

        Args:
            order      (BangumiCommentOrder, optional): 排序方式。Defaults to BangumiCommentOrder.DEFAULT
            next       (str | None, optional)         : 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None

        Returns:
            dict: 调用 API 返回的结果
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["short_comment"]
        params = {"media_id": self.__media_id, "ps": 20, "sort": order.value}
        if next is not None:
            params["cursor"] = next

        return await request("GET", api["url"], params, credential=credential)

    async def get_long_comment_list(
        self, order: BangumiCommentOrder = BangumiCommentOrder.DEFAULT, next: Union[str, None] = None
    ) -> dict:
        """
        获取长评列表

        Args:
            order      (BangumiCommentOrder, optional): 排序方式。Defaults to BangumiCommentOrder.DEFAULT
            next       (str | None, optional)         : 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None

        Returns:
            dict: 调用 API 返回的结果
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["long_comment"]
        params = {"media_id": self.__media_id, "ps": 20, "sort": order.value}
        if next is not None:
            params["cursor"] = next

        return await request("GET", api["url"], params, credential=credential)

    async def get_episode_list(self) -> dict:
        """
        获取季度分集列表，自动转换出海Api的字段，适配部分，但是键还是有不同

        Returns:
            dict: 调用 API 返回的结果
        """
        if self.oversea:
            # 转换 ep_id->id ，index_title->longtitle ，index->title
            fix_ep_list = []
            for item in self.ep_list:
                item["id"] = item.get("ep_id")
                item["longtitle"] = item.get("index_title")
                item["title"] = item.get("index")
                fix_ep_list.append(item)
            return {"main_section": {"episodes": fix_ep_list}}
        else:
            credential = (
                self.credential if self.credential is not None else Credential()
            )
            api = API["info"]["episodes_list"]
            params = {"season_id": self.__ssid}
            return await request("GET", api["url"], params, credential=credential)

    async def get_episodes(self) -> List["Episode"]:
        """
        获取番剧所有的剧集，自动生成类。
        """
        global episode_data_cache
        episode_list = await self.get_episode_list()
        if len(episode_list["main_section"]["episodes"]) == 0:
            return []
        first_epid = episode_list["main_section"]["episodes"][0]["id"]

        async def get_episode_info(epid: int):
            credential = self.credential if self.credential else Credential()
            session = get_session()

            try:
                resp = await session.get(
                    f"https://www.bilibili.com/bangumi/play/ep{epid}",
                    cookies=credential.get_cookies(),
                    headers={"User-Agent": "Mozilla/5.0"},
                )
            except Exception as e:
                raise ResponseException(str(e))
            else:
                content = resp.text

                pattern = re.compile(r"window.__INITIAL_STATE__=(\{.*?\});")
                match = re.search(pattern, content)
                if match is None:
                    raise ApiException("未找到番剧信息")
                try:
                    content = json.loads(match.group(1))
                except json.JSONDecodeError:
                    raise ApiException("信息解析错误")

                return content
        bangumi_meta = await get_episode_info(first_epid)
        bangumi_meta["media_id"] = self.get_media_id()

        episodes = []
        for ep in episode_list["main_section"]["episodes"]:
            episode_data_cache[ep["id"]] = {
                "bangumi_meta": bangumi_meta,
                "bangumi_class": self,
            }
            episodes.append(Episode(
                epid=ep["id"],
                credential=self.credential
            ))
        return episodes

    async def get_stat(self) -> dict:
        """
        获取番剧播放量，追番等信息

        Returns:
            dict: 调用 API 返回的结果
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["season_status"]
        params = {"season_id": self.__ssid}
        return await request("GET", api["url"], params, credential=credential)

    async def get_overview(self) -> dict:
        """
        获取番剧全面概括信息，包括发布时间、剧集情况、stat 等情况

        Returns:
            dict: 调用 API 返回的结果
        """
        credential = self.credential if self.credential is not None else Credential()
        if self.oversea:
            api = API["info"]["collective_info_oversea"]
        else:
            api = API["info"]["collective_info"]
        params = {"season_id": self.__ssid}
        return await request("GET", api["url"], params, credential=credential)


async def set_follow(
    bangumi: Bangumi, status: bool = True, credential: Union[Credential, None] = None
) -> dict:
    """
    追番状态设置

    Args:
        bangumi    (Bangumi)                    : 番剧类
        status     (bool, optional)             : 追番状态. Defaults to True.
        credential (Credential | None, optional): 凭据. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential is not None else Credential()
    credential.raise_for_no_sessdata()

    api = API["operate"]["follow_add"] if status else API["operate"]["follow_del"]
    data = {"season_id": bangumi.get_season_id()}
    return await request("POST", api["url"], data=data, credential=credential)


async def update_follow_status(
    bangumi: Bangumi, status: int, credential: Union[Credential, None] = None
) -> dict:
    """
    更新追番状态

    Args:
        bangumi    (Bangumi)                    : 番剧类
        credential (Credential | None, optional): 凭据. Defaults to None.
        status     (int)                        : 追番状态 1 想看 2 在看 3 已看
    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential is not None else Credential()
    credential.raise_for_no_sessdata()

    api = API["operate"]["follow_status"]
    data = {"season_id": bangumi.get_season_id(), "status": status}
    return await request("POST", api["url"], data=data, credential=credential)


class Episode(Video):
    """
    番剧剧集类

    Attributes:
        credential  (Credential): 凭据类
        video_class (Video)     : 视频类
        bangumi     (Bangumi)   : 所属番剧
    """

    def __init__(self, epid: int, credential: Union[Credential, None] = None):
        """
        Args:
            epid       (int)                 : 番剧 epid
            credential (Credential, optional): 凭据. Defaults to None.
        """
        global episode_data_cache
        self.credential = credential if credential else Credential()
        self.__epid = epid

        if not epid in episode_data_cache.keys():
            try:
                resp = httpx.get(
                    f"https://www.bilibili.com/bangumi/play/ep{self.__epid}",
                    cookies=self.credential.get_cookies(),
                    headers={"User-Agent": "Mozilla/5.0"},
                )
            except Exception as e:
                raise ResponseException(str(e))
            content = resp.text
            pattern = re.compile(r"window.__INITIAL_STATE__=(\{.*?\});")
            match = re.search(pattern, content)
            if match is None:
                raise ApiException("未找到番剧信息")
            try:
                content = json.loads(match.group(1))
            except json.JSONDecodeError:
                raise ApiException("信息解析错误")
        else:
            content = episode_data_cache[epid]["bangumi_meta"]

        bvid = content["epInfo"]["bvid"]
        if not epid in episode_data_cache.keys():
            self.bangumi = Bangumi(ssid=content["mediaInfo"]["season_id"])
        else:
            self.bangumi = episode_data_cache[epid]["bangumi_class"]

        self.video_class = Video(bvid=bvid, credential=self.credential)
        super().__init__(bvid=bvid)
        self.set_aid = self.set_aid_e
        self.set_bvid = self.set_bvid_e

    def get_epid(self) -> int:
        """
        获取 epid
        """
        return self.__epid

    def set_aid_e(self, aid: int) -> None:
        print("Set aid is not allowed in Episode")

    def set_bvid_e(self, bvid: str) -> None:
        print("Set bvid is not allowed in Episode")

    async def get_cid(self) -> int:
        """
        获取稿件 cid

        Returns:
            int: cid
        """
        return (await self.get_episode_info())["epInfo"]["cid"]

    def get_bangumi(self) -> "Bangumi":
        """
        获取对应的番剧

        Returns:
            Bangumi: 番剧类
        """
        return self.bangumi  # type: ignore

    def set_epid(self, epid: int) -> None:
        self.__init__(epid, self.credential)

    async def get_episode_info(self) -> dict:
        """
        获取番剧单集信息

        Returns:
            HTML 中的数据
        """
        credential = self.credential if self.credential else Credential()
        session = get_session()

        try:
            resp = await session.get(
                f"https://www.bilibili.com/bangumi/play/ep{self.__epid}",
                cookies=credential.get_cookies(),
                headers={"User-Agent": "Mozilla/5.0"},
            )
        except Exception as e:
            raise ResponseException(str(e))
        else:
            content = resp.text

            pattern = re.compile(r"window.__INITIAL_STATE__=(\{.*?\});")
            match = re.search(pattern, content)
            if match is None:
                raise ApiException("未找到番剧信息")
            try:
                content = json.loads(match.group(1))
            except json.JSONDecodeError:
                raise ApiException("信息解析错误")

            return content

    async def get_bangumi_from_episode(self) -> "Bangumi":
        """
        获取剧集对应的番剧

        Returns:
            Bangumi: 输入的集对应的番剧类
        """
        info = await self.get_episode_info()
        ssid = info["mediaInfo"]["season_id"]
        return Bangumi(ssid=ssid)

    async def get_download_url(self) -> dict:
        """
        获取番剧剧集下载信息。

        Returns:
            dict: 调用 API 返回的结果。
        """
        url = API["info"]["playurl"]["url"]
        if True:
            params = {
                "avid": self.get_aid(),
                "ep_id": self.get_epid(),
                "qn": "127",
                "otype": "json",
                "fnval": 4048,
                "fourk": 1,
            }
        return await request("GET", url, params=params, credential=self.credential)

    async def get_danmaku_xml(self) -> str:
        """
        获取所有弹幕的 xml 源文件（非装填）

        Returns:
            str: 文件源
        """
        cid = await self.get_cid()
        url = f"https://comment.bilibili.com/{cid}.xml"
        sess = get_session()
        config: dict[str, Any] = {"url": url}
        # 代理
        if settings.proxy:
            config["proxies"] = {"all://", settings.proxy}
        resp = await sess.get(**config)
        return resp.content.decode("utf-8")

    async def get_danmaku_view(self) -> dict:
        """
        获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。

        Returns:
            dict: 二进制流解析结果
        """
        return await self.video_class.get_danmaku_view(0)

    async def get_danmakus(self, date: Union[datetime.date, None] = None) -> List["Danmaku"]:
        """
        获取弹幕

        Args:
            date (datetime.date | None, optional): 指定某一天查询弹幕. Defaults to None. (不指定某一天)

        Returns:
            dict[Danmaku]: 弹幕列表
        """
        return await self.video_class.get_danmakus(0, date)

    async def get_history_danmaku_index(self, date: Union[datetime.date, None] = None) -> Union[None, List[str]]:
        """
        获取特定月份存在历史弹幕的日期。

        Args:
            date (datetime.date | None, optional): 精确到年月. Defaults to None。

        Returns:
            None | List[str]: 调用 API 返回的结果。不存在时为 None。
        """
        return await self.video_class.get_history_danmaku_index(0, date)
