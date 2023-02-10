"""
bilibili_api

哔哩哔哩的各种 API 调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。
"""

import asyncio
import platform

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

BILIBILI_API_VERSION = "15.0.0"

# 如果系统为 Windows，则修改默认策略，以解决代理报错问题
if "windows" in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore

__all__ = [
    # Exceptions
    "ApiException", "ArgsException",
    "CredentialNoBiliJctException",
    "CredentialNoBuvid3Exception",
    "CredentialNoDedeUserIDException",
    "CredentialNoSessdataException",
    "DanmakuClosedException",
    "DynamicExceedImagesException",
    "LiveException", "LoginError",
    "NetworkException", "ResponseCodeException",
    "ResponseException", "VideoUploadException",
    # Functions
    "aid2bvid", "bvid2aid", "get_session", "set_session",
    "parse_link", "ResourceType", "get_real_url", "sync",
    # Models
    "Credential", "Danmaku", "DmFontSize", "DmMode",
    "SpecialDanmaku", "Picture",
    # Constants
    "HEADERS"
]
