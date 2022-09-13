"""
bilibili_api
"""

import asyncio
import platform

from .shortcuts import *
from .shortcuts import __all__ as __shortcuts_all

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
] + __shortcuts_all
