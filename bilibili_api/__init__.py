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

# 如果系统为 Windows，则修改默认策略，以解决代理报错问题
if "windows" in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
del asyncio, platform
