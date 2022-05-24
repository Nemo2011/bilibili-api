"""
bilibili_api.utils.short
一个很简单的处理短链接的模块，主要是读取跳转链接。
"""
import aiohttp
from .network import get_session

async def get_real_url(short_url: str):
    """
    获取短链接跳转目标，以进行操作。
    Params:
        short_url(str): 短链接。
    Returns:
        目标链接（如果不是有效的链接会报错）
    """
    try:
        async with get_session().request("GET", url=short_url, allow_redirects=False) as rep:
            return rep.headers['Location']
    except:
        raise ValueError("无法查看目标链接！")
