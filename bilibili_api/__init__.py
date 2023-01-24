"""
bilibili_api

哔哩哔哩的各种 API 调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。
"""

import asyncio
import platform

from . import (
    album,
    app,
    article,
    ass,
    audio,
    bangumi,
    black_room,
    cheese,
    client,
    comment,
    dynamic,
    emoji,
    favorite_list,
    game,
    homepage,
    interactive_video,
    live_area,
    live,
    login_func,
    login,
    manga,
    note,
    rank,
    search,
    session,
    settings,
    topic,
    user,
    video_tag,
    video_uploader,
    video,
    video_zone,
    vote,
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
from .utils.Picture import Picture
from .utils.parse_link import ResourceType, parse_link
from .utils.short import get_real_url
from .utils.sync import sync
from .utils.network_httpx import get_session, set_session, HEADERS

# 如果系统为 Windows，则修改默认策略，以解决代理报错问题
if "windows" in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore

# ALL
__all__ = [
    "ApiException", "ArgsException",
    "Credential",
    "CredentialNoBiliJctException",
    "CredentialNoBuvid3Exception",
    "CredentialNoDedeUserIDException",
    "CredentialNoSessdataException",
    "Danmaku", "DanmakuClosedException",
    "DmFontSize", "DmMode",
    "DynamicExceedImagesException",
    "HEADERS", "LiveException",
    "LoginError", "NetworkException",
    "Picture", "ResourceType",
    "ResponseCodeException",
    "ResponseException",
    "SpecialDanmaku",
    "VideoUploadException",
    "aid2bvid", "album", "app",
    "article", "ass", "asyncio",
    "audio", "bangumi", "black_room",
    "bvid2aid", "video_zone", "cheese",
    "client", "comment", "dynamic",
    "emoji", "favorite_list",
    "game", "get_real_url",
    "get_session", "homepage",
    "interactive_video",
    "live", "live_area", "login", "login_func",
    "manga", "note", "parse_link", "platform",
    "rank", "search", "session", "set_session",
    "settings", "sync", "topic", "user", "video",
    "video_tag", "video_uploader", "video_zone", "vote",
]
