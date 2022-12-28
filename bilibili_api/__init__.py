"""
bilibili_api

哔哩哔哩的各种 API 调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。
"""

import asyncio
import platform

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
    game,
    homepage,
    interactive_video,
    live,
    login,
    login_func,
    rank,
    search,
    settings,
    topic,
    user,
    video,
    emoji,
    session,
    vote,
    video_uploader,
)
from .errors import (
    ApiException,
    ResponseCodeException,
    ResponseException,
    NetworkException,
    ArgsException,
    CredentialNoSessdataException,
    CredentialNoBiliJctException,
    CredentialNoBuvid3Exception,
    CredentialNoDedeUserIDException,
    DanmakuClosedException,
    VideoUploadException,
    LoginError,
    LiveException,
    DynamicExceedImagesException,
)
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.Credential import Credential
from .utils.Danmaku import Danmaku, DmFontSize, DmMode, SpecialDanmaku
from .utils.get_item import GetItemObjectType, get_item
from .utils.parse_link import ResourceType, parse_link
from .utils.short import get_real_url
from .utils.sync import sync
from .utils.network_httpx import get_session, set_session, HEADERS

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
    "emoji",
    "session",
    "vote",
]
