"""
bilibili_api.homepage

主页相关操作。
"""

from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.Credential import Credential

API = get_api("homepage")

async def get_top_photo():
    """
    获取主页最上方的图像。
    例如：b 站的风叶穿行，通过这个 API 获取的图片就是风叶穿行的图片。
    Returns:
        调用 API 返回的结果。
    """
    api = API['info']['top_photo']
    params = {
        "resource_id": 142
    }
    return await request("GET", api['url'], params=params)

async def get_links(credential: Credential=None):
    """
    获取主页左面的链接。
    可能和个人喜好有关。
    Args:
        credential(Credential): 凭据类
    Returns:
        调用 API 返回的结果
    """
    api = API['info']['links']
    params = {
        "pf": 0, 
        "ids": 4694
    }
    return await request("GET", api['url'], params=params, credential=credential)

async def get_popularize(credential: Credential=None):
    """
    获取推广的项目。
    ~~有视频有广告~~
    Args:
        credential(Credential): 凭据类
    Returns:
        调用 API 返回的结果
    """
    api = API['info']['popularize']
    params = {
        "pf": 0, 
        "ids": 34
    }
    return await request("GET", api['url'], params=params, credential=credential)

async def get_videos(credential: Credential=None):
    """
    获取首页推荐的视频。
    Args:
        credential(Credential): 凭据类
    Returns:
        调用 API 返回的结果
    """
    api = API['info']['videos']
    params = {
        "fresh_type": 0, 
        "version": 1, 
        "ps": 10, 
        "fresh_idx": 0, 
        "fresh_idx_1h": 0, 
        "homepage_ver": 1
    }
    return await request("GET", api['url'], params=params, credential=credential)
