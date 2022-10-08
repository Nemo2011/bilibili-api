"""
bilibili_api.utils.get_item

通过名称获取资源
"""

from enum import Enum
from .Credential import Credential
from ..search import search_by_type
from ..user import User
from ..live import LiveRoom
from ..article import Article
from ..bangumi import Bangumi
from ..video import Video

class GetItemObjectType(Enum):
    """
    资源类型。(仅供 get_item 使用)
    + VIDEO : 视频
    + BANGUMI : 番剧
    + FT : 影视
    + LIVE : 直播
    + ARTICLE : 专栏
    + USER : 用户
    + LIVEUSER : 直播间用户
    """
    VIDEO = "video"
    BANGUMI = "media_bangumi"
    FT = "media_ft"
    LIVE = "live"
    ARTICLE = "article"
    USER = "bili_user"
    LIVEUSER = "live_user"

async def get_item(name: str, obj_type: GetItemObjectType, credential: Credential = None):
    """
    通过名称及类型获取对应资源。

    支持：视频，番剧，影视，直播间，专栏，用户，直播用户

    如：名称是"碧诗", 类型是用户, 就能得到 User(uid = 2)

    Args:
        name(str)                  : 名称
        obj_type(GetItemObjectType): 资源类型
        credential(Credential)     : 凭据

    Returns:
        对应资源或 -1 (无匹配资源)
    """
    credential = credential if credential else Credential()
    try:
        result = (await search_by_type(name, obj_type))["result"]
        if obj_type == GetItemObjectType.USER:
            return User(uid = result[0]["mid"])
        elif obj_type == GetItemObjectType.LIVEUSER:
            return User(uid = result[0]["uid"])
        elif obj_type == GetItemObjectType.LIVE:
            return LiveRoom(result["live_room"][0]["roomid"])
        elif obj_type == GetItemObjectType.ARTICLE:
            return Article(result[0]["id"])
        elif obj_type == GetItemObjectType.FT:
            return Bangumi(result[0]["media_id"])
        elif obj_type == GetItemObjectType.BANGUMI:
            return Bangumi(result[0]["media_id"])
        elif obj_type == GetItemObjectType.VIDEO:
            return Video(result[0]["bvid"])
        else:
            return result
    except Exception as e:
        return -1
