"""
bilibili_api
"""

import asyncio
import platform

# Modules
from . import (app, article, ass, audio, bangumi, black_room, channel, cheese,
               comment, dynamic, favorite_list, game, homepage,
               interactive_video, live, login, login_func, rank, search,
               settings, topic, user, video, video_uploader)
from .article import ARTICLE_COLOR_MAP
from .black_room import BLACK_TYPE
# CONSTANTS
from .video import AUDIO_QUALITY, VIDEO_CODECS, VIDEO_QUALITY
HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"}
# Errors
from .errors import *
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
# Models
from .utils.Credential import Credential
from .utils.Danmaku import Danmaku, DmFontSize, DmMode, SpecialDanmaku
from .utils.get_item import GetItemObjectType, get_item
# Functions
from .utils.parse_link import ResourceType, parse_link
from .utils.short import get_real_url
from .utils.sync import sync

# 如果系统为 Windows，则修改默认策略，以解决代理报错问题
if "windows" in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
del asyncio, platform
