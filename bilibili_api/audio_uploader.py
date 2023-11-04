"""
bilibili_api.audio_uploader

音频上传
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

from .video import Video
from .utils.utils import get_api
from .dynamic import upload_image
from .utils.picture import Picture
from .utils.AsyncEvent import AsyncEvent
from .utils.credential import Credential
from .utils.aid_bvid_transformer import bvid2aid
from .exceptions.ApiException import ApiException
from .utils.network import Api, get_session
from .exceptions.NetworkException import NetworkException
from .exceptions.ResponseCodeException import ResponseCodeException

from enum import Enum

class VoiceType(Enum):
    """
    声音类型

    + HUMAN_SINGING: 人声演唱
    + VOCALOID_SINGER: VOCALOID歌手
    + HUMAN_KICHUKU: 人力鬼畜
    + PURE_MUSIC: 纯音乐
    """
    HUMAN_SINGING = 102 
    VOCALOID_SINGER = 103 
    HUMAN_KICHUKU = 104 
    PURE_MUSIC = 105 


class CreationType(Enum):
    """
    创作类型

    + ORIGINAL: 原创
    + COVER: 翻唱/翻奏
    + REMIX: 改编/remix
    """
    ORIGINAL = 106
    COVER = 107
    REMIX = 108

class LanguageType(Enum):
    """
    语种

    + CHINESE: 中文
    + JAPANESE: 日语
    + ENGLISH: 英语
    + KOREAN: 韩语
    + CANTONESE: 粤语
    + OTHER_LANGUAGES: 其他语种
    """
    CHINESE = 109
    JAPANESE = 110
    ENGLISH = 111
    KOREAN = 112
    CANTONESE = 113
    OTHER_LANGUAGES = 114

class ThemeSource(Enum):
    """
    主题来源
    
    + GAME: 游戏
    + ANIMATION: 动画
    + FILM_AND_TELEVISION: 影视
    + NETWORK_SONG: 网络歌曲
    + DERIVATIVE_WORK: 同人
    + IDOL: 偶像
    """
    ANIMATION = 115
    GAME = 116
    FILM_AND_TELEVISION = 117
    NETWORK_SONG = 118
    DERIVATIVE_WORK = 119
    IDOL = 120

class StyleType(Enum):
    """
    风格

    + POP: 流行
    + ANCIENT_STYLE: 古风
    + ROCK: 摇滚
    + FOLK_SONG: 民谣
    + ELECTRONIC: 电子
    + DANCE_MUSIC: 舞曲
    + RAP: 说唱
    + LIGHT_MUSIC: 轻音乐
    + A_CAPPELLA: 阿卡贝拉
    + JAZZ: 爵士
    + COUNTRY_MUSIC: 乡村
    + R_AND_B: R&B/Soul
    + CLASSICAL: 古典
    + CLASSICAL: 古典
    + ETHNIC: 民族
    + BRITISH: 英伦
    + METAL: 金属
    + PUNK: 朋克
    + BLUES: 蓝调
    + REGGAE: 雷鬼
    + WORLD_MUSIC: 世界音乐
    + LATIN: 拉丁
    + ALTERNATIVE: 另类/独立
    + NEW_AGE: New Age
    + POST_ROCK: 后摇
    + BOSSA_NOVA: Bossa Nova
    """
    POP = 121
    ANCIENT_STYLE = 122
    ROCK = 123
    FOLK_SONG = 124
    ELECTRONIC = 125
    DANCE_MUSIC = 126
    RAP = 127
    LIGHT_MUSIC = 128
    A_CAPPELLA = 129
    JAZZ = 130
    COUNTRY_MUSIC = 131
    R_AND_B = 132
    CLASSICAL = 133
    ETHNIC = 134
    BRITISH = 135
    METAL = 136
    PUNK = 137
    BLUES = 138
    REGGAE = 139
    WORLD_MUSIC = 140
    LATIN = 141
    ALTERNATIVE = 142
    NEW_AGE = 143
    POST_ROCK = 144
    BOSSA_NOVA = 145

class ContentType(Enum):
    """
    内容类型

    + MUSIC: 音乐
    + AUDIO_PROGRAM: 有声节目
    """
    MUSIC = 146
    AUDIO_PROGRAM = 147

class VoiceType(Enum):
    """
    声音类型

    + RADIO_DRAMA: 广播剧
    + AUDIO_STORY: 有声故事
    + ASMR: ASMR
    + OTHER: 其他
    """
    RADIO_DRAMA = 148
    AUDIO_STORY = 149
    ASMR = 150
    OTHER = 151