"""
bilibili_api.shortcuts

一些常用的类、常量、函数
"""

# CONSTANTS
from .video import AUDIO_QUALITY, VIDEO_CODECS, VIDEO_QUALITY
from .article import ARTICLE_COLOR_MAP
from .black_room import BLACK_FROM, BLACK_TYPE
from .session import SESSION_TYPE

HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"}

# Functions
from .utils.parse_link import parse_link
from .utils.short import get_real_url
from .utils.sync import sync
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid

# Models
from .utils.Credential import Credential
from .utils.parse_link import ResourceType
from .utils.Danmaku import Danmaku, DmMode, DmFontSize, SpecialDanmaku

# Errors
from .errors import *

__all__ = [
    "ARTICLE_COLOR_MAP",
    "AUDIO_QUALITY",
    "ApiException",
    "ArgsException",
    "BLACK_FROM",
    "BLACK_TYPE",
    "Credential",
    "CredentialNoBiliJctException",
    "CredentialNoBuvid3Exception",
    "CredentialNoDedeUserIDException",
    "CredentialNoSessdataException",
    "Danmaku",
    "DanmakuClosedException",
    "DmFontSize",
    "DmMode",
    "HEADERS",
    "LoginError",
    "NetworkException",
    "ResourceType",
    "ResponseCodeException",
    "ResponseException",
    "SESSION_TYPE",
    "SpecialDanmaku",
    "VIDEO_CODECS",
    "VIDEO_QUALITY",
    "VideoUploadException",
    "aid2bvid",
    "bvid2aid",
    "get_real_url",
    "parse_link",
    "sync",
]
