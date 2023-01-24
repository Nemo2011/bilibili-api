"""
bilibili_api

哔哩哔哩的各种 API 调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。
"""

import asyncio
import platform
import os

from . import (album, app, article, ass, audio, bangumi, black_room, channel,
               cheese, client, comment, dynamic, emoji, favorite_list, game,
               homepage, interactive_video, live, live_area, login, login_func,
               manga, note, rank, search, session, settings, topic, user,
               video, video_uploader, vote)
from .errors import (ApiException, ArgsException, CredentialNoBiliJctException,
                     CredentialNoBuvid3Exception,
                     CredentialNoDedeUserIDException,
                     CredentialNoSessdataException, DanmakuClosedException,
                     DynamicExceedImagesException, LiveException, LoginError,
                     NetworkException, ResponseCodeException,
                     ResponseException, VideoUploadException)
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.Credential import Credential
from .utils.Danmaku import Danmaku, DmFontSize, DmMode, SpecialDanmaku
from .utils.network_httpx import HEADERS, get_session, set_session
from .utils.parse_link import ResourceType, parse_link
from .utils.Picture import Picture
from .utils.short import get_real_url
from .utils.sync import sync

BILIBILI_API_VERSION = "15.0.0.dev"

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
    "bvid2aid", "channel", "cheese",
    "client", "comment", "dynamic",
    "emoji", "favorite_list",
    "game", "get_real_url",
    "get_session", "homepage",
    "interactive_video",
    "live", "live_area", "login", "login_func",
    "manga", "note", "parse_link", "platform",
    "rank", "search", "session", "set_session",
    "settings", "sync", "topic", "user", "video",
    "video_uploader", "vote",
    "BILIBILI_API_VERSION"
]
