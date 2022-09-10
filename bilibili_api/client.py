from .utils.network_httpx import request
from .utils.utils import get_api

API = get_api("client")

async def get_zone():
    """
    通过 IP 获取地理位置
    """
    api = API["zone"]
    return await request("GET", api["url"])


async def get_client_info():
    """
    获取终端信息
    """
    api = API["info"]
    return await request("GET", api["url"])
