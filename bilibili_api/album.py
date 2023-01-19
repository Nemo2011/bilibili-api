"""
bilibili_api.album

相簿相关
"""

from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.Credential import Credential
from .utils.Picture import Picture
from .exceptions import ArgsException
import enum
from typing import Optional

API = get_api("album")


class AlbumCategory(enum.Enum):
    """
    相簿分区枚举。

    - ALL   : 全部
    - PAINTS: 画友
    - PHOTOS: 摄影
    """
    ALL = 0
    PAINTS = 1
    PHOTOS = 2


class AlbumOrder(enum.Enum):
    """
    相簿排序顺序枚举。

    - RECOMMEND: 推荐
    - HOT      : 最火（并非所有函数均对此项支持）
    - NEW      : 最新（并非所有函数均对此项支持）
    """
    RECOMMEND = "recommend"
    HOT = "hot"
    NEW = "new"

async def get_homepage_albums_list(
    category: AlbumCategory = AlbumCategory.ALL,
    order: AlbumOrder = AlbumOrder.RECOMMEND,
    page_num: int = 1,
    page_size: int = 45,
    credential: Optional[Credential] = None
) -> dict:
    """
    """
    async def get_painter() -> dict:
        api = API["info"]["homepage_painter_albums_list"]
        if order != AlbumOrder.RECOMMEND:
            raise ArgsException("摄影相簿暂不支持以热度/以时间排序。")
        params = {
            "type": order.value,
            "page_num": page_num,
            "page_size": page_size
        }
        return await request(
            "GET",
            api["url"],
            params=params,
            credential=credential
        )
    async def get_photos() -> dict:
        api = API["info"]["homepage_photos_albums_list"]
        if order != AlbumOrder.RECOMMEND:
            raise ArgsException("摄影相簿暂不支持以热度/以时间排序。")
        params = {
            "type": order.value,
            "page_num": page_num,
            "page_size": page_size
        }
        return await request(
            "GET",
            api["url"],
            params=params,
            credential=credential
        )
    if category == AlbumCategory.PAINTS:
        return await get_painter()
    elif category == AlbumCategory.PHOTOS:
        return await get_photos()
    else:
        result = await get_painter()
        result["items"] += (await get_photos())["items"] # type: ignore
        result["total_count"] += (await get_photos())["total_count"] # type: ignore
        return result
