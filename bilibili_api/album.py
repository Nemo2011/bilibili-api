"""
bilibili_api.album

相簿相关
"""

from typing import Any, List, Union, Optional
from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.Credential import Credential
from .utils.Picture import Picture
from .exceptions import ArgsException
import enum

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


class Album:
    """
    相簿类，各种对相簿的操作均在其中。
    """

    def __init__(
        self,
        doc_id: Union[None, int] = None,
        credential: Union[None, Credential] = None
        ):
        """
        Args: 
            doc_id (int): 相簿 ID。
            credential (Credential): 用户凭证。
        """
        self.doc_id = doc_id
        self.credential: Credential = Credential() if credential is None else credential

        self.__info: Union[dict, None] = None

    async def get_raw_info(self) -> dict:
        """
        获取相簿完整信息。

        Returns:
            dict: 相簿信息。
        """
        api = API["info"]["detail"]
        params = {"doc_id": self.doc_id}
        resp = await request("GET", api["url"], params=params)
        self.__info = resp
        return resp
    
    async def __get_info_cached(self) -> dict:
        """
        获取相簿信息，如果已获取过则使用之前获取的信息，没有则重新获取。

        Returns:
            dict: 调用 API 返回的结果。
        """
        if self.__info is None:
            return await self.get_raw_info()
        return self.__info

    async def get_info(self) -> dict:
        """
        获取相簿状态。

        Returns:
            dict: 仅供相簿信息。
        """
        info = await self.__get_info_cached()
        return info["item"]
    
    async def get_author(self) -> dict:
        """
        获取相簿作者信息。

        Returns:
            dict: 相簿作者信息。
        """
        info = await self.__get_info_cached()
        return info["item"]["user"]

    async def get_pictures(self) -> List[Picture]:
        """
        获取相簿中的图片。

        Returns:
            List[Picture]: 相簿中的图片。
        """
        info = await self.get_info()
        pictures = []
        for picture in info["pictures"]:
            pictures.append(Picture(url=picture["img_src"], height=picture["img_height"], width=picture["img_width"], size=picture["img_size"]))
        return pictures


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
