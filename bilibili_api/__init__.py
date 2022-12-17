"""
bilibili_api
"""

import asyncio
import platform

from . import (app, article, ass, audio, bangumi, black_room, channel, cheese,
               comment, dynamic, favorite_list, game, homepage,
               interactive_video, live, login, login_func, rank, search,
               settings, topic, user, video, video_uploader)
HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"}
from .errors import *
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.Credential import Credential
from .utils.Danmaku import Danmaku, DmFontSize, DmMode, SpecialDanmaku
from .utils.get_item import GetItemObjectType, get_item
from .utils.parse_link import ResourceType, parse_link
from .utils.short import get_real_url
from .utils.sync import sync
from .utils.AsyncEvent import AsyncEvent

# 如果系统为 Windows，则修改默认策略，以解决代理报错问题
if "windows" in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
del asyncio, platform

__all__ = ['ApiException', 'ArgsException', 'AsyncEvent', 'Credentia\
    l', 'CredentialNoBiliJctException', 'CredentialNoBuvid3Exception\
    ', 'CredentialNoDedeUserIDException', 'CredentialNoSessdataExcep\
    tion', 'Danmaku', 'DanmakuClosedException', 'DmFontSize', 'DmMod\
    e', 'DynamicExceedImagesException', 'GetItemObjectType', 'HEADER\
    S', 'LiveException', 'LoginError', 'NetworkException', 'Resource\
    Type', 'ResponseCodeException', 'ResponseException', 'SpecialDan\
    maku', 'VideoUploadException', '__builtins__', '__cached__', '__\
    doc__', '__file__', '__loader__', '__name__', '__package__', '__\
    path__', '__spec__', 'aid2bvid', 'app', 'article', 'ass', 'audio\
    ', 'bangumi', 'black_room', 'bvid2aid', 'channel', 'cheese', 'co\
    mment', 'dynamic', 'errors', 'exceptions', 'favorite_list', 'gam\
    e', 'get_item', 'get_real_url', 'homepage', 'interactive_video',\
     'live', 'login', 'login_func', 'parse_link', 'rank', 'search', \
    'settings', 'sync', 'topic', 'user', 'utils', 'video', 'video_up\
    loader']
