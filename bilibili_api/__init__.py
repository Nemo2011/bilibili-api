"""
bilibili_api
"""

import asyncio
import platform

from .errors import *
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.Credential import Credential
from .utils.Danmaku import Danmaku, DmFontSize, DmMode, SpecialDanmaku
from .utils.short import get_real_url
from .utils.sync import sync
from .utils.network_httpx import get_session, set_session
from .utils.parse_link import parse_link, ResourceType
from .video import VIDEO_CODECS, VIDEO_QUALITY, AUDIO_QUALITY
from .article import ARTICLE_COLOR_MAP
from .black_room import BLACK_TYPE
from .utils.BytesReader import BytesReader
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

# UA 头 + Referer
HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"}

# 如果系统为 Windows，则修改默认策略，以解决代理报错问题
if "windows" in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
del asyncio, platform

# ALL
__all__ = [
    "ARTICLE_COLOR_MAP",
    "AUDIO_QUALITY",
    "ApiException",
    "ArgsException",
    "BLACK_TYPE",
    "BytesReader",
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
    "app",
    "article",
    "ass",
    "audio",
    "bangumi",
    "black_room",
    "bvid2aid",
    "channel",
    "cheese",
    "comment",
    "dynamic",
    "errors",
    "exceptions",
    "favorite_list",
    "get_real_url",
    "get_session",
    "homepage",
    "interactive_video",
    "live",
    "login",
    "login_func",
    "parse_link",
    "rank",
    "search",
    "set_session",
    "settings",
    "sync",
    "user",
    "utils",
    "video",
    "video_uploader",
]
