"""
bilibili_api.channel

分区相关操作。
"""

import json
import os
import copy
import enum

from .exceptions import ArgsException
from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.Credential import Credential

API = get_api("channel")


def get_channel_info_by_tid(tid: int):
    """
    根据 tid 获取频道信息。

    Args:
        tid (int): 频道的 tid。

    Returns:
        `tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if "tid" not in main_ch:
            continue
        if tid == int(main_ch["tid"]):
            return main_ch, None

        # 搜索子分区
        if "sub" in main_ch.keys():
            for sub_ch in main_ch["sub"]:
                if "tid" not in sub_ch:
                    continue
                if tid == sub_ch["tid"]:
                    return main_ch, sub_ch
    else:
        return None, None


def get_channel_info_by_name(name: str):
    """
    根据频道名称获取频道信息。

    Args:
        name (str): 频道的名称。

    Returns:
        tuple[dict | None, dict | None]: 第一个是主分区，第二个是子分区，没有时返回 None。
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())

    for main_ch in channel:
        if name in main_ch["name"]:
            return main_ch, None
        if "sub" in main_ch.keys():
            for sub_ch in main_ch["sub"]:
                if name in sub_ch["name"]:
                    return main_ch, sub_ch
    else:
        return None, None


async def get_top10(tid: int, day: int = 7, credential: Credential = None):
    """
    获取分区前十排行榜。

    Args:
        tid        (int)                 : 频道的 tid。
        day        (int, optional)       : 3 天排行还是 7 天排行。 Defaults to 7.
        credential (Credential, optional): Credential 类。Defaults to None.

    Returns:
        list: 前 10 的视频信息。
    """
    if credential is None:
        credential = Credential()
    if day not in (3, 7):
        raise ArgsException("参数 day 只能是 3，7。")

    url = API["ranking"]["get_top10"]["url"]
    params = {"rid": tid, "day": day}
    return await request("GET", url, params=params, credential=credential)


def get_channel_list():
    """
    获取所有分区的数据

    Returns:
        dict: 所有分区的数据
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())
    channel_list = []
    for channel_big in channel:
        channel_big_copy = copy.copy(channel_big)
        channel_list.append(channel_big_copy)
        if "sub" in channel_big.keys():
            channel_big_copy.pop("sub")
            for channel_sub in channel_big["sub"]:
                channel_sub_copy = copy.copy(channel_sub)
                channel_sub_copy["father"] = channel_big_copy
                channel_list.append(channel_sub_copy)
    return channel_list


def get_channel_list_sub():
    """
    获取所有分区的数据
    含父子关系（即一层次只有主分区）

    Returns:
        dict: 所有分区的数据
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8"
    ) as f:
        channel = json.loads(f.read())
    return channel


async def get_channel_videos_count_today(credential: Credential = None):
    """
    获取每个分区当日最新投稿数量

    Args:
        credential(Credential): 凭据类
    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    api = API["count"]
    return (await request("GET", api["url"], credential=credential))["region_count"]


async def get_channel_new_videos(tid: int, credential: Credential = None):
    """
    获取分区最新投稿

    Args:
        tid(int)              : 分区 id
        credential(Credential): 凭据类
    
    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    api = API["new"]
    params = {"rid": tid}
    return await request("GET", api["url"], params=params, credential=credential)


class ChannelTypes(enum.Enum):
    """
    所有分区枚举

    - MAINPAGE: 主页
    - ANIME: 番剧
        - ANIME_SERIAL: 连载中番剧
        - ANIME_FINISH: 已完结番剧
        - ANIME_INFORMATION: 资讯
        - ANIME_OFFICAL: 官方延伸
    - MOVIE: 电影
    - GUOCHUANG: 国创
        - GUOCHUANG_CHINESE: 国产动画
        - GUOCHUANG_ORIGINAL: 国产原创相关
        - GUOCHUANG_PUPPETRY: 布袋戏
        - GUOCHUANG_MOTIONCOMIC: 动态漫·广播剧
        - GUOCHUANG_INFORMATION: 资讯
    - TELEPLAY: 电视剧
    - DOCUMENTARY: 纪录片
    - DOUGA: 动画
        - DOUGA_MAD: MAD·AMV
        - DOUGA_MMD: MMD·3D
        - DOUGA_VOICE: 短片·手书·配音
        - DOUGA_GARAGE_KIT: 手办·模玩
        - DOUGA_TOKUSATSU: 特摄
        - DOUGA_ACGNTALKS: 动漫杂谈
        - DOUGA_OTHER: 综合
    - GAME: 游戏
        - GAME_STAND_ALONE: 单机游戏
        - GAME_ESPORTS: 电子竞技
        - GAME_MOBILE: 手机游戏
        - GAME_ONLINE: 网络游戏
        - GAME_BOARD: 桌游棋牌
        - GAME_GMV: GMV
        - GAME_MUSIC: 音游
        - GAME_MUGEN: Mugen
    - KICHIKU: 鬼畜
        - KICHIKU_GUIDE: 鬼畜调教
        - KICHIKU_MAD: 音MAD
        - KICHIKU_MANUAL_VOCALOID: 人力VOCALOID
        - KICHIKU_THEATRE: 鬼畜剧场
        - KICHIKU_COURSE: 教程演示
    - MUSIC: 音乐
        - MUSIC_ORIGINAL: 原创音乐
        - MUSIC_COVER: 翻唱
        - MUSIC_PERFORM: 演奏
        - MUSIC_VOCALOID: VOCALOID·UTAU
        - MUSIC_LIVE: 音乐现场
        - MUSIC_MV: MV
        - MUSIC_COMMENTARY: 乐评盘点
        - MUSIC_TUTORIAL: 音乐教学
        - MUSIC_OTHER: 音乐综合
    - DANCE: 舞蹈
        - DANCE_OTAKU: 宅舞
        - DANCE_HIPHOP: 街舞
        - DANCE_STAR: 明星舞蹈
        - DANCE_CHINA: 中国舞
        - DANCE_THREE_D: 舞蹈综合
        - DANCE_DEMO: 舞蹈教程
    - CINEPHILE: 影视
        - CINEPHILE_CINECISM: 影视杂谈
        - CINEPHILE_MONTAGE: 影视剪辑
        - CINEPHILE_SHORTFILM: 小剧场
        - CINEPHILE_TRAILER_INFO: 预告·资讯
    - ENT: 娱乐
        - ENT_VARIETY: 综艺 
        - ENT_TALKER: 娱乐杂谈
        - ENT_FANS: 粉丝创作
        - ENT_CELEBRITY: 明星综合
    - KNOWLEDGE: 知识
        - KNOWLEDGE_SCIENCE: 科学科普
        - KNOWLEDGE_SOCIAL_SCIENCE: 社科·法律·心理
        - KNOWLEDGE_HUMANITY_HISTORY: 人文历史
        - KNOWLEDGE_BUSINESS: 财经商业
        - KNOWLEDGE_CAMPUS: 校园学习
        - KNOWLEDGE_CAREER: 职业职场
        - KNOWLEDGE_DESIGN: 设计·创意
        - KNOWLEDGE_SKILL: 野生技能协会
    - TECH: 科技
        - TECH_DIGITAL: 数码
        - TECH_APPLICATION: 软件应用
        - TECH_COMPUTER_TECH: 计算机技术
        - TECH_INDUSTRY: 科工机械
    - INFORMATION: 资讯
        - INFORMATION_HOTSPOT: 热点
        - INFORMATION_GLOBAL: 环球
        - INFORMATION_SOCIAL: 社会
        - INFORMATION_MULTIPLE: 综合
    - FOOD: 美食
        - FOOD_MAKE: 美食制作
        - FOOD_DETECTIVE: 美食侦探
        - FOOD_MEASUREMENT: 美食测评
        - FOOD_RURAL: 田园美食
        - FOOD_RECORD: 美食记录
    - LIFE: 生活
        - LIFE_FUNNY: 搞笑
        - LIFE_TRAVEL: 出行
        - LIFE_RURALLIFE: 三农
        - LIFE_HOME: 家居房产
        - LIFE_HANDMAKE: 手工
        - LIFE_PAINTING: 绘画
        - LIFE_DAILY: 日常
    - CAR: 汽车
        - CAR_RACING: 赛车
        - CAR_MODIFIEDVEHICLE: 改装玩车
        - CAR_NEWENERGYVEHICLE: 新能源车
        - CAR_TOURINGCAR: 房车
        - CAR_MOTORCYCLE: 摩托车
        - CAR_STRATEGY: 购车攻略
        - CAR_LIFE: 汽车生活
    - FASHION: 时尚
        - FASHION_MAKEUP: 美妆护肤
        - FASHION_COS: 仿妆cos
        - FASHION_CLOTHING: 穿搭
        - FASHION_TREND: 时尚潮流
    - SPORTS: 运动
        - SPORTS_BASKETBALL: 篮球
        - SPORTS_FOOTBALL: 足球
        - SPORTS_AEROBICS: 健身
        - SPORTS_ATHLETIC: 竞技体育 
        - SPORTS_CULTURE: 运动文化
        - SPORTS_COMPREHENSIVE: 运动综合
    - ANIMAL: 动物圈
        - ANIMAL_CAT: 喵星人
        - ANIMAL_DOG: 汪星人
        - ANIMAL_PANDA: 大熊猫
        - ANIMAL_WILD_ANIMAL: 野生动物
        - ANIMAL_REPTILES: 爬宠
        - ANIMAL_COMPOSITE: 动物综合
    - VLOG: VLOG
    """
    MAINPAGE = 0

    ANIME = 13
    ANIME_SERIAL = 33
    ANIME_FINISH = 32
    ANIME_INFORMATION = 51
    ANIME_OFFICAL = 152
    
    MOVIE = 23

    GUOCHUANG = 167
    GUOCHUANG_CHINESE = 153
    GUOCHUANG_ORIGINAL = 168
    GUOCHUANG_PUPPETRY = 169
    GUOCHUANG_MOTIONCOMIC = 195
    GUOCHUANG_INFORMATION = 170

    TELEPLAY = 11

    DOCUMENTARY = 177

    DOUGA = 1
    DOUGA_MAD = 24
    DOUGA_MMD = 25
    DOUGA_VOICE = 47
    DOUGA_GARAGE_KIT = 210
    DOUGA_TOKUSATSU = 86
    DOUGA_ACGNTALKS = 253
    DOUGA_OTHER = 27
    
    GAME = 4
    GAME_STAND_ALONE = 17
    GAME_ESPORTS = 171
    GAME_MOBILE = 172
    GAME_ONLINE = 65
    GAME_BOARD = 173
    GAME_GMV = 121
    GAME_MUSIC = 136
    GAME_MUGEN = 19

    KICHIKU = 119
    KICHIKU_GUIDE = 22
    KICHIKU_MAD = 26
    KICHIKU_MANUAL_VOCALOID = 126
    KICHIKU_THEATRE = 216
    KICHIKU_COURSE = 127

    MUSIC = 3
    MUSIC_ORIGINAL = 28
    MUSIC_COVER = 31
    MUSIC_PERFORM = 59
    MUSIC_VOCALOID = 30
    MUSIC_LIVE = 29
    MUSIC_MV = 193
    MUSIC_COMMENTARY = 243
    MUSIC_TUTORIAL = 244
    MUSIC_OTHER = 130

    DANCE = 129
    DANCE_OTAKU = 20
    DANCE_HIPHOP = 198
    DANCE_STAR = 199
    DANCE_CHINA = 200
    DANCE_THREE_D = 154
    DANCE_DEMO = 156

    CINEPHILE = 181
    CINEPHILE_CINECISM = 182
    CINEPHILE_MONTAGE = 183
    CINEPHILE_SHORTFILM = 85
    CINEPHILE_TRAILER_INFO = 184

    ENT = 5
    ENT_VARIETY = 71
    ENT_TALKER = 241
    ENT_FANS = 242
    ENT_CELEBRITY = 137

    KNOWLEDGE = 36
    KNOWLEDGE_SCIENCE = 201
    KNOWLEDGE_SOCIAL_SCIENCE = 124
    KNOWLEDGE_HUMANITY_HISTORY = 228
    KNOWLEDGE_BUSINESS = 207
    KNOWLEDGE_CAMPUS = 208
    KNOWLEDGE_CAREER = 209
    KNOWLEDGE_DESIGN = 229
    KNOWLEDGE_SKILL = 122

    TECH = 188
    TECH_DIGITAL = 95
    TECH_APPLICATION = 230
    TECH_COMPUTER_TECH = 231
    TECH_INDUSTRY = 232

    INFORMATION = 202
    INFORMATION_HOTSPOT = 203
    INFORMATION_GLOBAL = 204
    INFORMATION_SOCIAL = 205
    INFORMATION_MULTIPLE = 206

    FOOD = 211
    FOOD_MAKE = 76
    FOOD_DETECTIVE = 212
    FOOD_MEASUREMENT = 213
    FOOD_RURAL = 214
    FOOD_RECORD = 215

    LIFE = 160
    LIFE_FUNNY = 138
    LIFE_TRAVEL = 250
    LIFE_RURALLIFE = 251
    LIFE_HOME = 239
    LIFE_HANDMAKE = 161
    LIFE_PAINTING = 162
    LIFE_DAILY = 21

    CAR = 223
    CAR_RACING = 245
    CAR_MODIFIEDVEHICLE = 246
    CAR_NEWENERGYVEHICLE = 247
    CAR_TOURINGCAR = 248
    CAR_MOTORCYCLE = 240
    CAR_STRATEGY = 227
    CAR_LIFE = 176

    FASHION = 155
    FASHION_MAKEUP = 157
    FASHION_COS = 252
    FASHION_CLOTHING = 158
    FASHION_TREND = 159

    SPORTS = 234
    SPORTS_BASKETBALL = 235
    SPORTS_FOOTBALL = 249
    SPORTS_AEROBICS = 164
    SPORTS_ATHLETIC = 236
    SPORTS_CULTURE = 237
    SPORTS_COMPREHENSIVE = 238

    ANIMAL = 217
    ANIMAL_CAT = 218
    ANIMAL_DOG = 219
    ANIMAL_PANDA = 220
    ANIMAL_WILD_ANIMAL = 221
    ANIMAL_REPTILES = 222
    ANIMAL_COMPOSITE = 75
    
    VLOG = 19
