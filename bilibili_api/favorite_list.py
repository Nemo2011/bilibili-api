"""
bilibili_api.favorite_list

收藏夹操作。
"""

from enum import Enum

from .video import Video
from . import user
from .utils.network_httpx import request
from .exceptions.ArgsException import ArgsException
from .utils.Credential import Credential
from .utils.utils import get_api, join
from typing import List

API = get_api("favorite-list")


class FavoriteListContentOrder(Enum):
    """
    收藏夹列表内容排序方式枚举。

    + MTIME  : 最近收藏
    + VIEW   : 最多播放
    + PUBTIME: 最新投稿
    """

    MTIME = "mtime"
    VIEW = "view"
    PUBTIME = "pubtime"


class VideoFavoriteList:
    """
    一个简单的视频收藏夹类
    """

    def __init__(self, media_id, credential: Credential = None):
        self.media_id = media_id
        self.credential = credential

    async def get_content(
        self,
        page=1,
        keyword=None,
        order: FavoriteListContentOrder = FavoriteListContentOrder.MTIME,
        tid=0,
    ):
        """
        获取视频收藏夹列表元数据。

        Args:
            page       (int, optional)                     : 页码. Defaults to 1.
            keyword    (str, optional)                     : 搜索关键词. Defaults to None.
            order      (FavoriteListContentOrder, optional): 排序方式. Defaults to FavoriteListContentOrder.MTIME.
            tid        (int, optional)                     : 分区 ID. Defaults to 0.

        Returns:
            dict: 调用 API 返回结果。
        """
        return await get_video_favorite_list_content(
            self.media_id, page, keyword, order, tid, self.credential
        )


async def get_video_favorite_list(
    uid: int, video: Video = None, credential: Credential = None
):
    """
    获取视频收藏夹列表。

    Args:
        uid        (int)                 : 用户 UID。
        video      (Video)               : 视频类。若提供该参数则结果会附带该收藏夹是否存在该视频。Defaults to None.
        credential (Credential, optional): 凭据. Defaults to None.

    Returns:
        dict: API 调用结果。
    """
    api = API["info"]["list_list"]
    params = {"up_mid": uid, "type": 2}

    if video is not None:
        params["rid"] = video.get_aid()

    return await request("GET", url=api["url"], params=params, credential=credential)


async def get_video_favorite_list_content(
    media_id: int,
    page: int = 1,
    keyword: str = None,
    order: FavoriteListContentOrder = FavoriteListContentOrder.MTIME,
    tid: int = 0,
    credential: Credential = None,
):
    """
    获取视频收藏夹列表内容。

    Args:
        media_id   (int)                               : 收藏夹 ID。
        page       (int, optional)                     : 页码. Defaults to 1.
        keyword    (str, optional)                     : 搜索关键词. Defaults to None.
        order      (FavoriteListContentOrder, optional): 排序方式. Defaults to FavoriteListContentOrder.MTIME.
        tid        (int, optional)                     : 分区 ID. Defaults to 0.
        credential (Credential, optional)              : Credential. Defaults to None.

    Returns:
        dict: 调用 API 返回结果。
    """
    api = API["info"]["list_content"]
    params = {
        "media_id": media_id,
        "pn": page,
        "ps": 20,
        "order": order.value,
        "tid": tid,
    }

    if keyword is not None:
        params["keyword"] = keyword

    return await request("GET", api["url"], params=params, credential=credential)


async def get_topic_favorite_list(page: int = 1, credential: Credential = None):
    """
    获取自己的话题收藏夹内容。

    Args:
        page       (int, optional): 页码. Defaults to 1.
        credential (Credential)   : Credential
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()

    api = API["info"]["list_topics"]
    params = {"pn": page, "ps": 16}

    return await request("GET", api["url"], params=params, credential=credential)


async def get_article_favorite_list(page: int = 1, credential: Credential = None):
    """
    获取自己的专栏收藏夹内容。

    Args:
        page       (int, optional)       : 页码. Defaults to 1.
        credential (Credential, optional): Credential. Defaults to None.
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()

    api = API["info"]["list_articles"]
    params = {"pn": page, "ps": 16}

    return await request("GET", api["url"], params=params, credential=credential)


async def get_album_favorite_list(page: int = 1, credential: Credential = None):
    """
    获取自己的相簿收藏夹内容。

    Args:
        page       (int, optional)       : 页码. Defaults to 1.
        credential (Credential, optional): Credential. Defaults to None.
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()

    api = API["info"]["list_albums"]
    params = {"page": page, "pagesize": 30, "biz_type": 2}

    return await request("GET", api["url"], params=params, credential=credential)


async def get_course_favorite_list(page: int = 1, credential: Credential = None):
    """
    获取自己的课程收藏夹内容。

    Args:
        page       (int, optional)       : 页码. Defaults to 1.
        credential (Credential, optional): Credential. Defaults to None.
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()

    api = API["info"]["list_courses"]
    self_info = await user.get_self_info(credential)
    params = {"pn": page, "ps": 10, "mid": self_info["mid"]}

    return await request("GET", api["url"], params=params, credential=credential)


async def get_note_favorite_list(page: int = 1, credential: Credential = None):
    """
    获取自己的笔记收藏夹内容。

    Args:
        page       (int, optional)       : 页码. Defaults to 1.
        credential (Credential, optional): Credential. Defaults to None.
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()

    api = API["info"]["list_notes"]
    params = {"pn": page, "ps": 16}

    return await request("GET", api["url"], params=params, credential=credential)


async def create_video_favorite_list(
    title: str,
    introduction: str = "",
    private: bool = False,
    credential: Credential = None,
):
    """
    新建视频收藏夹列表。

    Args:
        title        (str)                 : 收藏夹名。
        introduction (str, optional)       : 收藏夹简介. Defaults to ''.
        private      (bool, optional)      : 是否为私有. Defaults to False.
        credential   (Credential, optional): 凭据. Defaults to None.

    Returns:
        dict: API 调用结果。
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    api = API["operate"]["new"]
    data = {
        "title": title,
        "intro": introduction,
        "privacy": 1 if private else 0,
        "cover": "",
    }

    return await request("POST", api["url"], data=data, credential=credential)


async def modify_video_favorite_list(
    media_id: int,
    title: str,
    introduction: str = "",
    private: bool = False,
    credential: Credential = None,
):
    """
    修改视频收藏夹信息。

    Args:
        media_id     (int)                 : 收藏夹 ID.
        title        (str)                 : 收藏夹名。
        introduction (str, optional)       : 收藏夹简介. Defaults to ''.
        private      (bool, optional)      : 是否为私有. Defaults to False.
        credential   (Credential, optional): Credential. Defaults to None.

    Returns:
        dict: API 调用结果。
    """

    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    api = API["operate"]["modify"]
    data = {
        "title": title,
        "intro": introduction,
        "privacy": 1 if private else 0,
        "cover": "",
        "media_id": media_id,
    }

    return await request("POST", api["url"], data=data, credential=credential)


async def delete_video_favorite_list(media_ids: List[int], credential: Credential):
    """
    删除视频收藏夹，可批量删除。

    Args:
        media_ids  (List[int]) : 收藏夹 ID 列表。
        credential (Credential): Credential.

    Returns:
        dict: API 调用结果。
    """

    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    data = {"media_ids": join(",", media_ids)}
    api = API["operate"]["delete"]

    return await request("POST", api["url"], data=data, credential=credential)


async def copy_video_favorite_list_content(
    media_id_from: int, media_id_to: int, aids: List[int], credential: Credential
):
    """
    复制视频收藏夹内容

    Args:
        media_id_from (int)       : 要复制的源收藏夹 ID。
        media_id_to   (int)       : 目标收藏夹 ID。
        aids          (List[int]) : 被复制的视频 ID 列表。
        credential    (Credential): 凭据

    Returns:
        dict: API 调用结果。
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    api = API["operate"]["content_copy"]

    self_info = await user.get_self_info(credential=credential)

    data = {
        "src_media_id": media_id_from,
        "tar_media_id": media_id_to,
        "mid": self_info["mid"],
        "resources": ",".join(map(lambda x: f"{str(x)}:2", aids)),
    }

    return await request("POST", api["url"], data=data, credential=credential)


async def move_video_favorite_list_content(
    media_id_from: int, media_id_to: int, aids: List[int], credential: Credential
):
    """
    移动视频收藏夹内容

    Args:
        media_id_from (int)       : 要移动的源收藏夹 ID。
        media_id_to   (int)       : 目标收藏夹 ID。
        aids          (List[int]) : 被移动的视频 ID 列表。
        credential    (Credential): 凭据

    Returns:
        dict: API 调用结果。
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    api = API["operate"]["content_move"]

    data = {
        "src_media_id": media_id_from,
        "tar_media_id": media_id_to,
        "resources": ",".join(map(lambda x: f"{str(x)}:2", aids)),
    }

    return await request("POST", api["url"], data=data, credential=credential)


async def delete_video_favorite_list_content(
    media_id: int, aids: List[int], credential: Credential
):
    """
    删除视频收藏夹内容

    Args:
        media_id   (int)       : 收藏夹 ID。
        aids       (List[int]) : 被删除的视频 ID 列表。
        credential (Credential): 凭据

    Returns:
        dict: API 调用结果。
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    api = API["operate"]["content_rm"]

    data = {
        "media_id": media_id,
        "resources": ",".join(map(lambda x: f"{str(x)}:2", aids)),
    }

    return await request("POST", api["url"], data=data, credential=credential)


async def clean_video_favorite_list_content(media_id: int, credential: Credential):
    """
    清除视频收藏夹失效内容

    Args:
        media_id   (int)       : 收藏夹 ID
        credential (Credential): 凭据

    Returns:
        dict: API 调用结果。
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    api = API["operate"]["content_clean"]

    data = {"media_id": media_id}

    return await request("POST", api["url"], data=data, credential=credential)
