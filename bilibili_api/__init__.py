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
    game, 
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
from .utils.get_item import get_item

# Models
from .utils.Credential import Credential
from .utils.parse_link import ResourceType
from .utils.Danmaku import Danmaku, DmMode, DmFontSize, SpecialDanmaku
from .utils.get_item import GetItemObjectType

# Errors
from .errors import *

# 如果系统为 Windows，则修改默认策略，以解决代理报错问题
if "windows" in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
del asyncio, platform
