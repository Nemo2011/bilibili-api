"""
bilibili_api.bangumi

番剧相关

概念：
+ media_id: 番剧本身的 ID，有时候也是每季度的 ID，如 https://www.bilibili.com/bangumi/media/md28231846/
+ season_id: 每季度的 ID
+ episode_id: 每集的 ID，如 https://www.bilibili.com/bangumi/play/ep374717

"""

import datetime
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
    params = {"types": type_.value, "before": before, "after": after}
    return await request("GET", api["url"], params=params)


class IndexFilter:
    """
    番剧索引相关固定参数以及值
    """

    class Type(Enum):
        """
        索引类型

        + ANIME: 番剧
        + MOVIE: 电影
        + DOCUMENTARY: 纪录片
        + GUOCHUANG: 国创
        + TV: 电视剧
        + VARIETY: 综艺
        """

        ANIME = 1
        MOVIE = 2
        DOCUMENTARY = 3
        GUOCHUANG = 4
        TV = 5
        VARIETY = 7

    class Version(Enum):
        """
        番剧版本

        + ALL: 全部
        + MAIN: 正片
        + FILM: 电影
        + OTHER: 其他
        """

        ALL = -1
        MAIN = 1
        FILM = 2
        OTHER = 3

    class Spoken_Language(Enum):
        """
        配音

        + ALL: 全部
        + ORIGINAL: 原声
        + CHINESE: 中配
        """

        ALL = -1
        ORIGINAL = 1
        CHINESE = 2

    class Finish_Status(Enum):
        """
        完结状态

        + ALL: 全部
        + FINISHED: 完结
        + UNFINISHED: 连载
        """

        ALL = -1
        FINISHED = 1
        UNFINISHED = 0

    class Copyright(Enum):
        """
        版权方

        + ALL: 全部
        + EXCLUSIVE: 独家
        + OTHER: 其他
        """

        ALL = -1
        EXCLUSIVE = 3
        OTHER = "1,2,4"

    class Season(Enum):
        """
        季度

        + ALL: 全部
        + SPRING: 春季
        + SUMMER: 夏季
        + AUTUMN: 秋季
        + WINTER: 冬季
        """

        ALL = -1
        WINTER = 1
        SPRING = 4
        SUMMER = 7
        AUTUMN = 10

    @staticmethod
    def make_time_filter(
        start: Union[datetime.datetime, str, int] = None,
        end: Union[datetime.datetime, str, int] = None,
        include_start: bool = True,
        include_end: bool = False,
    ) -> str:
        """
        生成番剧索引所需的时间条件

        番剧、国创直接传入年份，为 int 或者 str 类型，如 `make_time_filter(start=2019, end=2020)`

        影视、纪录片、电视剧传入 datetime.datetime，如 `make_time_filter(start=datetime.datetime(2019, 1, 1), end=datetime.datetime(2020, 1, 1))`

        start 或 end 为 None 时则表示不设置开始或结尾

        Args:
            start (datetime, str, int): 开始时间. 如果是 None 则不设置开头.
            end   (datetime, str, int): 结束时间. 如果是 None 则不设置结尾.
            include_start (bool): 是否包含开始时间. 默认为 True.
            include_end   (bool): 是否包含结束时间. 默认为 False.

        Returns:
            str: 年代条件
        """
        start_str = ""
        end_str = ""

        if start != None:
            if isinstance(start, datetime.datetime):
                start_str = start.strftime("%Y-%m-%d %H:%M:%S")
            else:
                start_str = start
        if end != None:
            if isinstance(end, datetime.datetime):
                end_str = end.strftime("%Y-%m-%d %H:%M:%S")
            else:
                end_str = end

        # 是否包含边界
        if include_start:
            start_str = f"[{start_str}"
        else:
            start_str = f"({start_str}"
        if include_end:
            end_str = f"{end_str}]"
        else:
            end_str = f"{end_str})"

        return f"{start_str},{end_str}"

    class Producer(Enum):
        """
        制作方

        + ALL: 全部
        + CCTV: CCTV
        + BBC: BBC
        + DISCOVERY: 探索频道
        + NATIONAL_GEOGRAPHIC: 国家地理
        + NHK: NHK
        + HISTORY: 历史频道
        + SATELLITE: 卫视
        + SELF: 自制
        + ITV: ITV
        + SKY: SKY
        + ZDF: ZDF
        + PARTNER: 合作机构
        + SONY: 索尼
        + GLOBAL_NEWS: 环球
        + PARAMOUNT: 派拉蒙
        + WARNER: 华纳
        + DISNEY: 迪士尼
        + DOMESTIC_OTHER: 国内其他
        + FOREIGN_OTHER: 国外其他
        """

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
        SONY = 15
        GLOBAL_NEWS = 16
        PARAMOUNT = 17
        WARNER = 18
        DISNEY = 19

    class Payment(Enum):
        """
        观看条件

        + ALL: 全部
        + FREE: 免费
        + PAID: 付费
        + VIP: 大会员
        """

        ALL = -1
        FREE = 1
        PAID = "2,6"
        VIP = "4,6"

    class Area(Enum):
        """
        地区

        + ALL: 全部
        + CHINA: 中国
        + CHINA_MAINLAND: 中国大陆
        + CHINA_HONGKONG_AND_TAIWAN: 中国港台
        + JAPAN: 日本
        + USA: 美国
        + UK: 英国
        + SOUTH_KOREA: 韩国
        + FRANCE: 法国
        + THAILAND: 泰国
        + GERMANY: 德国
        + ITALY: 意大利
        + SPAIN: 西班牙
        + ANIME_OTHER: 番剧其他
        + MOVIE_OTHER: 影视其他
        + DOCUMENTARY_OTHER: 纪录片其他

        注意：各索引的 其他 表示的地区都不同
        """

        ALL = "-1"
        CHINA = "1,6,7"
        CHINA_MAINLAND = "1"
        CHINA_HONGKONG_AND_TAIWAN = "6,7"
        JAPAN = "2"
        USA = "3"
        UK = "4"
        SOUTH_KOREA = "8"
        FRANCE = "9"
        THAILAND = "10"
        GERMANY = "15"
        ITALY = "35"
        SPAIN = "13"
        ANIME_OTHER = "1,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70"
        TV_OTHER = "5,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70"
        MOVIE_OTHER = "5,11,12,14,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70"

    class Style:
        """
        风格，根据索引不同，可选的风格也不同
        """

        class Anime(Enum):
            """
            番剧风格

            + ALL: 全部
            + ORIGINAL: 原创
            + COMIC: 漫画改
            + NOVEL: 小说改
            + GAME: 游戏改
            + TOKUSATSU: 特摄
            + BUDAIXI: 布袋戏
            + WARM: 热血
            + TIMEBACK: 穿越
            + IMAGING: 奇幻
            + WAR: 战斗
            + FUNNY: 搞笑
            + DAILY: 日常
            + SCIENCE_FICTION: 科幻
            + MOE: 萌系
            + HEAL: 治愈
            + SCHOOL: 校园
            + CHILDREN: 儿童
            + NOODLES: 泡面
            + LOVE: 恋爱
            + GIRLISH: 少女
            + MAGIC: 魔法
            + ADVENTURE: 冒险
            + HISTORY: 历史
            + ALTERNATE: 架空
            + MACHINE_BATTLE: 机战
            + GODS_DEM: 神魔
            + VOICE: 声控
            + SPORT: 运动
            + INSPIRATION: 励志
            + MUSIC: 音乐
            + ILLATION: 推理
            + SOCIEITES: 社团
            + OUTWIT: 智斗
            + TEAR: 催泪
            + FOOD: 美食
            + IDOL: 偶像
            + OTOME: 乙女
            + WORK: 职场
            """

            ALL = -1
            ORIGINAL = 10010
            COMIC = 10011
            NOVEL = 10012
            GAME = 10013
            TOKUSATSU = 10102
            BUDAIXI = 10015
            WARM = 10016
            TIMEBACK = 10017
            IMAGING = 10018
            WAR = 10020
            FUNNY = 10021
            DAILY = 10022
            SCIENCE_FICTION = 10023
            MOE = 10024
            HEAL = 10025
            SCHOOL = 10026
            CHILDREN = 10027
            NOODLES = 10028
            LOVE = 10029
            GIRLISH = 10030
            MAGIC = 10031
            ADVENTURE = 10032
            HISTORY = 10033
            ALTERNATE = 10034
            MACHINE_BATTLE = 10035
            GODS_DEMONS = 10036
            VOICE = 10037
            SPORTS = 10038
            INSPIRATIONAL = 10039
            MUSIC = 10040
            ILLATION = 10041
            SOCIETIES = 10042
            OUTWIT = 10043
            TEAR = 10044
            FOODS = 10045
            IDOL = 10046
            OTOME = 10047
            WORK = 10048

        class Movie(Enum):
            """
            电影风格

            + ALL: 全部
            + SKETCH: 短片
            + PLOT: 剧情
            + COMEDY: 喜剧
            + ROMANTIC: 爱情
            + ACTION: 动作
            + SCAIRIER: 恐怖
            + SCIENCE_FICTION: 科幻
            + CRIME: 犯罪
            + TIRILLER: 惊悚
            + SUSPENSE: 悬疑
            + IMAGING: 奇幻
            + WAR: 战争
            + ANIME: 动画
            + BIOAGRAPHY: 传记
            + FAMILY: 家庭
            + SING_DANCE: 歌舞
            + HISTORY: 历史
            + DISCOVER: 探险
            + DOCUMENTARY: 纪录片
            + DISATER: 灾难
            + COMIC: 漫画改
            + NOVEL: 小说改
            """

            ALL = -1
            SKETCH = 10104
            PLOT = 10050
            COMEDY = 10051
            ROMANTIC = 10052
            ACTION = 10053
            SCAIRIER = 10054
            SCIENCE_FICTION = 10023
            CRIME = 10055
            TIRILLER = 10056
            SUSPENSE = 10057
            IMAGING = 10018
            WAR = 10058
            ANIME = 10059
            BIOAGRAPHY = 10060
            FAMILY = 10061
            SING_DANCE = 10062
            HISTORY = 10033
            DISCOVER = 10032
            DOCUMENTARY = 10063
            DISATER = 10064
            COMIC = 10011
            NOVEL = 10012

        class GuoChuang(Enum):
            """
            国创风格

            + ALL: 全部
            + ORIGINAL: 原创
            + COMIC: 漫画改
            + NOVEL: 小说改
            + GAME: 游戏改
            + DYNAMIC: 动态漫
            + BUDAIXI: 布袋戏
            + WARM: 热血
            + IMAGING: 奇幻
            + FANTASY: 玄幻
            + WAR: 战斗
            + FUNNY: 搞笑
            + WUXIA: 武侠
            + DAILY: 日常
            + SCIENCE_FICTION: 科幻
            + MOE: 萌系
            + HEAL: 治愈
            + SUSPENSE: 悬疑
            + SCHOOL: 校园
            + CHILDREN: 少儿
            + NOODLES: 泡面
            + LOVE: 恋爱
            + GIRLISH: 少女
            + MAGIC: 魔法
            + HISTORY: 历史
            + MACHINE_BATTLE: 机战
            + GODS_DEMONS: 神魔
            + VOICE: 声控
            + SPORT: 运动
            + INSPIRATION: 励志
            + MUSIC: 音乐
            + ILLATION: 推理
            + SOCIEITES: 社团
            + OUTWIT: 智斗
            + TEAR: 催泪
            + FOOD: 美食
            + IDOL: 偶像
            + OTOME: 乙女
            + WORK: 职场
            + ANCIENT: 古风
            """

            ALL = -1
            ORIGINAL = 10010
            COMIC = 10011
            NOVEL = 10012
            GAME = 10013
            DYNAMIC = 10014
            BUDAIXI = 10015
            WARM = 10016
            IMAGING = 10018
            FANTASY = 10019
            WAR = 10020
            FUNNY = 10021
            WUXIA = 10078
            DAILY = 10022
            SCIENCE_FICTION = 10023
            MOE = 10024
            HEAL = 10025
            SUSPENSE = 10057
            SCHOOL = 10026
            CHILDREN = 10027
            NOODLES = 10028
            LOVE = 10029
            GIRLISH = 10030
            MAGIC = 10031
            HISTORY = 10033
            MACHINE_BATTLE = 10035
            GODS_DEMONS = 10036
            VOICE = 10037
            SPORTS = 10038
            INSPIRATIONAL = 10039
            MUSIC = 10040
            ILLATION = 10041
            SOCIETIES = 10042
            OUTWIT = 10043
            TEAR = 10044
            FOODS = 10045
            IDOL = 10046
            OTOME = 10047
            WORK = 10048
            ANCIENT = 10049

        class TV(Enum):
            """
            电视剧风格

            + ALL: 全部
            + FUNNY: 搞笑
            + IMAGING: 奇幻
            + WAR: 战争
            + WUXIA: 武侠
            + YOUTH: 青春
            + SKETCH: 短剧
            + CITY: 都市
            + ANCIENT: 古装
            + SPY: 谍战
            + CLASSIC: 经典
            + EMOTION: 情感
            + SUSPENSE: 悬疑
            + INSPIRATION: 励志
            + MYTH: 神话
            + TIMEBACK: 穿越
            + YEAR: 年代
            + COUNTRYSIDE: 乡村
            + INVESTIGATION: 刑侦
            + PLOT: 剧情
            + FAMILY: 家庭
            + HISTORY: 历史
            + ARMY: 军旅
            """

            ALL = -1
            FUNNY = 10021
            IMAGING = 10018
            WAR = 10058
            WUXIA = 10078
            YOUTH = 10079
            SKETCH = 10103
            CITY = 10080
            COSTUME = 10081
            SPY = 10082
            CLASSIC = 10083
            EMOTION = 10084
            SUSPENSE = 10057
            INSPIRATIONAL = 10039
            MYTH = 10085
            TIMEBACK = 10017
            YEAR = 10086
            COUNTRYSIDE = 10087
            INVESTIGATION = 10088
            PLOT = 10050
            FAMILY = 10061
            HISTORY = 10033
            ARMY = 10089

        class Documentary(Enum):
            """
            纪录片风格

            + ALL: 全部
            + HISTORY: 历史
            + FOODS: 美食
            + HUMANITIES: 人文
            + TECHNOLOGY: 科技
            + DISCOVER: 探险
            + UNIVERSE: 宇宙
            + PETS: 萌宠
            + SOCIAL: 社会
            + ANIMALS: 动物
            + NATURE: 自然
            + MEDICAL: 医疗
            + WAR: 战争
            + DISATER: 灾难
            + INVESTIGATIONS: 罪案
            + MYSTERIOUS: 神秘
            + TRAVEL: 旅行
            + SPORTS: 运动
            + MOVIES: 电影
            """

            ALL = -1
            HISTORY = 10033
            FOODS = 10045
            HUMANITIES = 10065
            TECHNOLOGY = 10066
            DISCOVER = 10067
            UNIVERSE = 10068
            PETS = 10069
            SOCIAL = 10070
            ANIMALS = 10071
            NATURE = 10072
            MEDICAL = 10073
            WAR = 10074
            DISATER = 10064
            INVESTIGATIONS = 10075
            MYSTERIOUS = 10076
            TRAVEL = 10077
            SPORTS = 10038
            MOVIES = -10

        class Variety(Enum):
            """
            综艺风格

            + ALL: 全部
            + MUSIC: 音乐
            + TALK: 访谈
            + TALK_SHOW: 脱口秀
            + REALITY_SHOW: 真人秀
            + TALENT_SHOW: 选秀
            + FOOD: 美食
            + TRAVEL: 旅行
            + SOIREE: 晚会
            + CONCERT: 演唱会
            + EMOTION: 情感
            + COMEDY: 喜剧
            + PARENT_CHILD: 亲子
            + CULTURE: 文化
            + OFFICE: 职场
            + PET: 萌宠
            + CULTIVATE: 养成

            """

            ALL = -1
            MUSIC = 10040
            TALK = 10091
            TALK_SHOW = 10081
            REALITY_SHOW = 10092
            TALENT_SHOW = 10094
            FOOD = 10045
            TRAVEL = 10095
            SOIREE = 10098
            CONCERT = 10096
            EMOTION = 10084
            COMEDY = 10051
            PARENT_CHILD = 10097
            CULTURE = 10100
            OFFICE = 10048
            PET = 10069
            CULTIVATE = 10099

    class Sort(Enum):
        """
        排序方式

        + DESC: 降序
        + ASC: 升序
        """

        DESC = "0"
        ASC = "1"

    class Order(Enum):
        """
        排序字段

        + UPDATE: 更新时间
        + DANMAKU: 弹幕数量
        + PLAY: 播放数量
        + FOLLOWER: 追番人数
        + SOCRE: 最高评分
        + ANIME_RELEASE: 番剧开播日期
        + MOVIE_RELEASE: 电影上映日期
        """

        UPDATE = "0"
        DANMAKU = "1"
        PLAY = "2"
        FOLLOWER = "3"
        SCORE = "4"
        ANIME_RELEASE = "5"
        MOVIE_RELEASE = "6"


class IndexFilterMeta:
    """
    IndexFilter 元数据

    用于传入 get_index_info 方法
    """

    class Anime:
        def __init__(
            self,
            version: IndexFilter.Version = IndexFilter.Version.ALL,
            spoken_language: IndexFilter.Spoken_Language = IndexFilter.Spoken_Language.ALL,
            area: IndexFilter.Area = IndexFilter.Area.ALL,
            finish_status: IndexFilter.Finish_Status = IndexFilter.Finish_Status.ALL,
            copyright: IndexFilter.Copyright = IndexFilter.Copyright.ALL,
            payment: IndexFilter.Payment = IndexFilter.Payment.ALL,
            season: IndexFilter.Season = IndexFilter.Season.ALL,
            year: str = -1,
            style: IndexFilter.Style.Anime = IndexFilter.Style.Anime.ALL,
        ) -> None:
            """
            Anime Meta
            Args:
                version (Index_Filter.Version): 类型，如正片、电影等
                spoken_language (Index_Filter.Spoken_Language): 配音
                area (Index_Filter.Area): 地区
                finish_status (Index_Filter.Finish_Status): 是否完结
                copyright (Index_Filter.Copryright): 版权
                payment (Index_Filter.Payment): 付费门槛
                season (Index_Filter.Season): 季度
                year (str): 年份，调用 Index_Filter.make_time_filter() 传入年份 (int, str) 获取
                style (Index_Filter.Style.Anime): 风格
            """
            self.season_type = IndexFilter.Type.ANIME
            self.season_version = version
            self.spoken_language_type = spoken_language
            self.area = area
            self.is_finish = finish_status
            self.copyright = copyright
            self.season_status = payment
            self.season_month = season
            self.year = year
            self.style_id = style

    class Movie:
        def __init__(
            self,
            area: IndexFilter.Area = IndexFilter.Area.ALL,
            release_date: str = -1,
            style: IndexFilter.Style.Movie = IndexFilter.Style.Movie.ALL,
            payment: IndexFilter.Payment = IndexFilter.Payment.ALL,
        ) -> None:
            """
            Movie Meta
            Args:
                area (Index_Filter.Area): 地区
                payment (Index_Filter.Payment): 付费门槛
                season (Index_Filter.Season): 季度
                release_date (str): 上映时间，调用 Index_Filter.make_time_filter() 传入年份 (datetime.datetime) 获取
                style (Index_Filter.Style.Movie): 风格
            """
            self.season_type = IndexFilter.Type.MOVIE
            self.area = area
            self.release_date = release_date
            self.style_id = style
            self.season_status = payment

    class Documentary:
        def __init__(
            self,
            release_date: str = -1,
            style: IndexFilter.Style.Documentary = IndexFilter.Style.Documentary.ALL,
            payment: IndexFilter.Payment = IndexFilter.Payment.ALL,
            producer: IndexFilter.Producer = IndexFilter.Producer.ALL,
        ) -> None:
            """
            Documentary Meta
            Args:
                area (Index_Filter.Area): 地区
                release_date (str): 上映时间，调用 Index_Filter.make_time_filter() 传入年份 (datetime.datetime) 获取
                style (Index_Filter.Style.Documentary): 风格
                producer (Index_Filter.Producer): 制作方
            """
            self.season_type = IndexFilter.Type.DOCUMENTARY
            self.release_date = release_date
            self.style_id = style
            self.season_status = payment
            self.producer_id = producer

    class TV:
        def __init__(
            self,
            area: IndexFilter.Area = IndexFilter.Area.ALL,
            release_date: str = -1,
            style: IndexFilter.Style.TV = IndexFilter.Style.TV.ALL,
            payment: IndexFilter.Payment = IndexFilter.Payment.ALL,
        ) -> None:
            """
            TV Meta
            Args:
                area (Index_Filter.Area): 地区
                payment (Index_Filter.Payment): 付费门槛
                release_date (str): 上映时间，调用 Index_Filter.make_time_filter() 传入年份 (datetime.datetime) 获取
                style (Index_Filter.Style.TV): 风格
            """
            self.season_type = IndexFilter.Type.TV
            self.area = area
            self.release_date = release_date
            self.style_id = style
            self.season_status = payment

    class GuoChuang:
        def __init__(
            self,
            version: IndexFilter.Version = IndexFilter.Version.ALL,
            finish_status: IndexFilter.Finish_Status = IndexFilter.Finish_Status.ALL,
            copyright: IndexFilter.Copyright = IndexFilter.Copyright.ALL,
            payment: IndexFilter.Payment = IndexFilter.Payment.ALL,
            year: str = -1,
            style: IndexFilter.Style.GuoChuang = IndexFilter.Style.GuoChuang.ALL,
        ) -> None:
            """
            Guochuang Meta
            Args:
                version (Index_Filter.VERSION): 类型，如正片、电影等
                finish_status (Index_Filter.Finish_Status): 是否完结
                copyright (Index_Filter.Copyright): 版权
                payment (Index_Filter.Payment): 付费门槛
                year (str): 年份，调用 Index_Filter.make_time_filter() 传入年份 (int, str) 获取
                style (Index_Filter.Style.GuoChuang): 风格
            """
            self.season_type = IndexFilter.Type.GUOCHUANG
            self.season_version = version
            self.is_finish = finish_status
            self.copyright = copyright
            self.season_status = payment
            self.year = year
            self.style_id = style

    class Variety:
        def __init__(
            self,
            style: IndexFilter.Style.Variety = IndexFilter.Style.Variety.ALL,
            payment: IndexFilter.Payment = IndexFilter.Payment.ALL,
        ) -> None:
            """
            Variety Meta
            Args:
                payment (Index_Filter.Payment): 付费门槛
                style (Index_Filter.Style.Variety): 风格
            """
            self.season_type = IndexFilter.Type.VARIETY
            self.season_status = payment
            self.style_id = style


async def get_index_info(
    filters: IndexFilterMeta = IndexFilterMeta.Anime(),
    order: IndexFilter.Order = IndexFilter.Order.SCORE,
    sort: IndexFilter.Sort = IndexFilter.Sort.DESC,
    pn: int = 1,
    ps: int = 20,
) -> dict:
    """
    查询番剧索引，索引的详细参数信息见 `IndexFilterMeta`

    请先通过 `IndexFilterMeta` 构造 filters

    Args:
        filters (Index_Filter_Meta, optional): 筛选条件元数据. Defaults to Anime.
        order (BANGUMI_INDEX.ORDER, optional): 排序字段. Defaults to SCORE.
        sort (BANGUMI_INDEX.SORT, optional): 排序方式. Defaults to DESC.
        pn (int, optional): 页数. Defaults to 1.
        ps (int, optional): 每页数量. Defaults to 20.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["index"]
    params = {}

    for key, value in filters.__dict__.items():
        if value is not None:
            if isinstance(value, Enum):
                params[key] = value.value
            else:
                params[key] = value

    if order in params:
        if (
            order == IndexFilter.Order.SCORE.value
            and sort == IndexFilter.Sort.ASC.value
        ):
            raise ValueError(
                "order 为 Index_Filter.ORDER.SCORE 时，sort 不能为 Index_Filter.SORT.ASC"
            )

    # 必要参数 season_type、type
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
    ) -> None:
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
        self,
        order: BangumiCommentOrder = BangumiCommentOrder.DEFAULT,
        next: Union[str, None] = None,
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
        self,
        order: BangumiCommentOrder = BangumiCommentOrder.DEFAULT,
        next: Union[str, None] = None,
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
            episodes.append(Episode(epid=ep["id"], credential=self.credential))
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

    async def get_danmakus(
        self, date: Union[datetime.date, None] = None
    ) -> List["Danmaku"]:
        """
        获取弹幕

        Args:
            date (datetime.date | None, optional): 指定某一天查询弹幕. Defaults to None. (不指定某一天)

        Returns:
            dict[Danmaku]: 弹幕列表
        """
        return await self.video_class.get_danmakus(0, date)

    async def get_history_danmaku_index(
        self, date: Union[datetime.date, None] = None
    ) -> Union[None, List[str]]:
        """
        获取特定月份存在历史弹幕的日期。

        Args:
            date (datetime.date | None, optional): 精确到年月. Defaults to None。

        Returns:
            None | List[str]: 调用 API 返回的结果。不存在时为 None。
        """
        return await self.video_class.get_history_danmaku_index(0, date)
