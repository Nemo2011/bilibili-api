"""
bilibili_api
"""

import asyncio
import platform

# Modules
from . import (
    app,
    article,
    ass,
    audio,
    bangumi,
    black_room,
    channel,
    cheese,
    comment,
    dynamic,
    favorite_list,
    homepage,
    interactive_video,
    live,
    login_func,
    login,
    rank,
    search,
    settings,
    user,
    video_uploader,
    video,
)

# CONSTANTS
from .video import AUDIO_QUALITY, VIDEO_CODECS, VIDEO_QUALITY
from .article import ARTICLE_COLOR_MAP
from .black_room import BLACK_TYPE

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

# 如果系统为 Windows，则修改默认策略，以解决代理报错问题
if "windows" in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
del asyncio, platform

# ALL
__all__ = [
    "app",
    "article",
    "ass",
    "audio",
    "bangumi",
    "black_room",
    "channel",
    "cheese",
    "comment",
    "dynamic",
    "favorite_list",
    "homepage",
    "interactive_video",
    "live",
    "login_func",
    "login",
    "rank",
    "search",
    "settings",
    "user",
    "video_uploader",
    "video",
    "ARTICLE_COLOR_MAP",
    "AUDIO_QUALITY",
    "ApiException",
    "ArgsException",
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
