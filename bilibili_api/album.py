"""
bilibili_api.album

相簿相关
"""

from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.Picture import Picture
import enum

API = get_api("album")


class AlbumCategories(enum.Enum):
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
