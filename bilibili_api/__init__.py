import asyncio
import platform

from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.Credential import Credential
from .utils.Danmaku import Danmaku, DmFontSize, DmMode
from .utils.short import get_real_url
from .utils.sync import sync
from .utils.network_httpx import get_session, set_session
from .utils.parse_link import parse_link, ResourceType

HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://bilibili.com"}

# 如果系统为 Windows，则修改默认策略，以解决代理报错问题
if "windows" in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

__all__ = [
    "Credential",
    "Danmaku",
    "DmFontSize",
    "DmMode",
    "HEADERS",
    "ResourceType",
    "aid2bvid",
    "app",
    "article",
    "bangumi",
    "bvid2aid",
    "channel",
    "cheese",
    "comment",
    "dynamic",
    "favorite_list",
    "get_real_url",
    "get_session",
    "homepage",
    "interactive_video",
    "live",
    "login",
    "parse_link",
    "rank",
    "search",
    "set_session",
    "settings",
    "sync",
    "user",
    "video_uploader",
    "video",
    "vote",
]
