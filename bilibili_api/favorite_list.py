"""
bilibili_api.favorite_list

收藏夹操作。
"""

from enum import Enum
from typing import List, Union, Optional

from . import user
from .video import Video
from .utils.utils import join, get_api
from .utils.credential import Credential
from .utils.network_httpx import request
from .exceptions.ArgsException import ArgsException

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


class FavoriteListType(Enum):
    """
    收藏夹类型枚举

    + VIDEO  : 视频收藏夹
    + ARTICLE: 专栏收藏夹
    + CHEESE : 课程收藏夹
    """

    VIDEO = "video"
    ARTICLE = "articles"
    CHEESE = "pugvfav"


class SearchFavoriteListMode(Enum):
    """
    收藏夹搜索模式枚举

    + ONLY : 仅当前收藏夹
    + ALL  : 该用户所有收藏夹
    """

    ONLY = 0
    ALL = 1


class FavoriteList:
    """
    收藏夹类

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(
        self,
        type_: FavoriteListType = FavoriteListType.VIDEO,
        media_id: Union[int, None] = None,
        credential: Union[Credential, None] = None,
    ) -> None:
        """
        Args:
            type_      (FavoriteListType, optional): 收藏夹类型. Defaults to FavoriteListType.VIDEO.

            media_id   (int, optional)             : 收藏夹号（仅为视频收藏夹时提供）. Defaults to None.

            credential (Credential, optional)      : 凭据类. Defaults to Credential().
        """
        self.__type = type_
        self.__media_id = media_id
        self.credential = credential if credential else Credential()

    def is_video_favorite_list(self) -> bool:
        """
        收藏夹是否为视频收藏夹

        Returns:
            bool: 是否为视频收藏夹
        """
        return self.__type == FavoriteListType.VIDEO

    def get_media_id(self) -> Union[int, None]:
        return self.__media_id

    def get_favorite_list_type(self) -> FavoriteListType:
        return self.__type

    async def get_info(self):
        """
        获取收藏夹信息。

        Returns:
            dict: 调用 API 返回的结果
        """
        assert self.__media_id != None, "视频收藏夹需要 media_id"

        api = API["info"]["info"]
        params = {"media_id": self.__media_id}

        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_content_video(
        self,
        page: int = 1,
        keyword: Union[str, None] = None,
        order: FavoriteListContentOrder = FavoriteListContentOrder.MTIME,
        tid=0,
    ) -> dict:
        """
        获取视频收藏夹内容。

        Args:
            page    (int, optional)                     : 页码. Defaults to 1.

            keyword (str | None, optional)              : 搜索关键词. Defaults to None.

            order   (FavoriteListContentOrder, optional): 排序方式. Defaults to FavoriteListContentOrder.MTIME.

            tid     (int, optional)                     : 分区 ID. Defaults to 0.

        Returns:
            dict: 调用 API 返回的结果
        """
        assert self.__type != FavoriteListType.VIDEO, "此函数仅在收藏夹为视频收藏家时可用"
        assert self.__media_id != None, "视频收藏夹需要 media_id"

        return await get_video_favorite_list_content(
            self.__media_id, page, keyword, order, tid, self.credential
        )

    async def get_content(self, page: int = 1) -> dict:
        """
        获取收藏夹内容。

        Args:
            page (int, optional): 页码. Defaults to 1.

        Returns:
            dict: 调用 API 返回的结果
        """
        if self.__type == FavoriteListType.ARTICLE:
            return await get_article_favorite_list(page, self.credential)
        elif self.__type == FavoriteListType.CHEESE:
            return await get_course_favorite_list(page, self.credential)
        elif self.__type == FavoriteListType.VIDEO:
            assert self.__media_id != None, "视频收藏夹需要 media_id"
            return await get_video_favorite_list_content(
                self.__media_id, page, credential=self.credential
            )
        else:
            raise ArgsException("无法识别传入的类型")

    async def get_content_ids_info(self) -> dict:
        """
        获取收藏夹所有内容的 ID。

        Returns:
            dict: 调用 API 返回的结果
        """
        assert self.__media_id != None, "视频收藏夹需要 media_id"

        api = API["info"]["list_content_id_list"]
        params = {"media_id": self.__media_id}

        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )


async def get_video_favorite_list(
    uid: int,
    video: Union[Video, None] = None,
    credential: Union[Credential, None] = None,
) -> dict:
    """
    获取视频收藏夹列表。

    Args:
        uid        (int)                   : 用户 UID。

        video      (Video | None, optional): 视频类。若提供该参数则结果会附带该收藏夹是否存在该视频。Defaults to None.

        credential (Credential | None, optional)  : 凭据. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["list_list"]
    params = {"up_mid": uid, "type": 2}

    if video is not None:
        params["rid"] = video.get_aid()

    return await request("GET", url=api["url"], params=params, credential=credential)


async def get_video_favorite_list_content(
    media_id: int,
    page: int = 1,
    keyword: Union[str, None] = None,
    order: FavoriteListContentOrder = FavoriteListContentOrder.MTIME,
    tid: int = 0,
    mode: SearchFavoriteListMode = SearchFavoriteListMode.ONLY,
    credential: Union[Credential, None] = None,
) -> dict:
    """
    获取视频收藏夹列表内容，也可用于搜索收藏夹内容。

    mode 参数见 SearchFavoriteListMode 枚举。

    Args:
        media_id   (int)                               : 收藏夹 ID。

        page       (int, optional)                     : 页码. Defaults to 1.

        keyword    (str, optional)                     : 搜索关键词. Defaults to None.

        order      (FavoriteListContentOrder, optional): 排序方式. Defaults to FavoriteListContentOrder.MTIME.

        tid        (int, optional)                     : 分区 ID. Defaults to 0.

        mode       (SearchFavoriteListMode, optional)  : 搜索模式，默认仅当前收藏夹.

        credential (Credential, optional)              : Credential. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["list_content"]
    params = {
        "media_id": media_id,
        "pn": page,
        "ps": 20,
        "order": order.value,
        "tid": tid,
        "type": mode.value,
    }

    if keyword is not None:
        params["keyword"] = keyword

    return await request("GET", api["url"], params=params, credential=credential)


async def get_topic_favorite_list(
    page: int = 1, credential: Union[None, Credential] = None
) -> dict:
    """
    获取自己的话题收藏夹内容。

    Args:
        page       (int, optional)              : 页码. Defaults to 1.

        credential (Credential | None, optional): Credential

    Returns:
        dict: 调用 API 返回的结果
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()

    api = API["info"]["list_topics"]
    params = {"page_num": page, "page_size": 16}

    return await request("GET", api["url"], params=params, credential=credential)


async def get_article_favorite_list(
    page: int = 1, credential: Union[None, Credential] = None
) -> dict:
    """
    获取自己的专栏收藏夹内容。

    Args:
        page       (int, optional)              : 页码. Defaults to 1.

        credential (Credential | None, optional): Credential. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()

    api = API["info"]["list_articles"]
    params = {"pn": page, "ps": 16}

    return await request("GET", api["url"], params=params, credential=credential)


async def get_album_favorite_list(
    page: int = 1, credential: Union[None, Credential] = None
) -> dict:
    """
    获取自己的相簿收藏夹内容。

    Args:
        page       (int, optional)              : 页码. Defaults to 1.

        credential (Credential | None, optional): Credential. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()

    api = API["info"]["list_albums"]
    params = {"page": page, "pagesize": 30, "biz_type": 2}

    return await request("GET", api["url"], params=params, credential=credential)


async def get_course_favorite_list(
    page: int = 1, credential: Union[None, Credential] = None
) -> dict:
    """
    获取自己的课程收藏夹内容。

    Args:
        page       (int, optional)       : 页码. Defaults to 1.

        credential (Credential | None, optional): Credential. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()

    api = API["info"]["list_courses"]
    self_info = await user.get_self_info(credential)
    params = {"pn": page, "ps": 10, "mid": self_info["mid"]}

    return await request("GET", api["url"], params=params, credential=credential)


async def get_note_favorite_list(
    page: int = 1, credential: Union[None, Credential] = None
) -> dict:
    """
    获取自己的笔记收藏夹内容。

    Args:
        page       (int, optional)       : 页码. Defaults to 1.

        credential (Credential | None, optional): Credential. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
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
    credential: Union[None, Credential] = None,
) -> dict:
    """
    新建视频收藏夹列表。

    Args:
        title        (str)                 : 收藏夹名。

        introduction (str, optional)       : 收藏夹简介. Defaults to ''.

        private      (bool, optional)      : 是否为私有. Defaults to False.

        credential   (Credential, optional): 凭据. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
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
    credential: Union[None, Credential] = None,
) -> dict:
    """
    修改视频收藏夹信息。

    Args:
        media_id     (int)                 : 收藏夹 ID.

        title        (str)                 : 收藏夹名。

        introduction (str, optional)       : 收藏夹简介. Defaults to ''.

        private      (bool, optional)      : 是否为私有. Defaults to False.

        credential   (Credential, optional): Credential. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
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


async def delete_video_favorite_list(
    media_ids: List[int], credential: Credential
) -> dict:
    """
    删除视频收藏夹，可批量删除。

    Args:
        media_ids  (List[int]) : 收藏夹 ID 列表。

        credential (Credential): Credential.

    Returns:
        dict: 调用 API 返回的结果
    """

    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    data = {"media_ids": join(",", media_ids)}
    api = API["operate"]["delete"]

    return await request("POST", api["url"], data=data, credential=credential)


async def copy_video_favorite_list_content(
    media_id_from: int, media_id_to: int, aids: List[int], credential: Credential
) -> dict:
    """
    复制视频收藏夹内容

    Args:
        media_id_from (int)       : 要复制的源收藏夹 ID。

        media_id_to   (int)       : 目标收藏夹 ID。

        aids          (List[int]) : 被复制的视频 ID 列表。

        credential    (Credential): 凭据

    Returns:
        dict: 调用 API 返回的结果
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
) -> dict:
    """
    移动视频收藏夹内容

    Args:
        media_id_from (int)       : 要移动的源收藏夹 ID。

        media_id_to   (int)       : 目标收藏夹 ID。

        aids          (List[int]) : 被移动的视频 ID 列表。

        credential    (Credential): 凭据

    Returns:
        dict: 调用 API 返回的结果
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
) -> dict:
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


async def clean_video_favorite_list_content(
    media_id: int, credential: Credential
) -> dict:
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


async def get_favorite_collected(
    uid: int,
    pn: int = 1,
    ps: int = 20,
    credential: Union[Credential, None] = None,
) -> dict:
    """
    获取收藏合集列表

    Args:
        uid        (int)                               : 用户 UID。

        pn         (int, optional)                     : 页码. Defaults to 1.

        ps         (int, optional)                     : 每页数据大小. Defaults to 20.

        credential (Credential | None, optional)       : Credential. Defaults to None.
    """
    api = API["info"]["collected"]
    params = {"up_mid": uid, "platform": "web", "pn": pn, "ps": ps}
    return await request("GET", api["url"], params=params, credential=credential)
