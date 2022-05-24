from .utils.network import set_session, get_session, request
from .utils.Credential import Credential
from .utils.sync import sync
from .utils.short import get_real_url
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.Danmaku import Danmaku


import platform
import asyncio

# 如果系统为 Windows，则修改默认策略，以解决代理报错问题
if "windows" in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
