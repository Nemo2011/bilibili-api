"""
bilibili_api.channel_series

用户合集与列表相关
"""
from enum import Enum
from typing import Union, List
from .utils.Credential import Credential
from .utils.utils import get_api
from .utils.network_httpx import request
import json
import httpx

API_USER = get_api("user")

# 1704

channel_meta_cache = {}

class ChannelOrder(Enum):
    """
    合集视频排序顺序。
    + DEFAULT: 默认排序
    + CHANGE : 升序排序
    """

    DEFAULT = "false"
    CHANGE = "true"


class ChannelSeriesType(Enum):
    """
    合集与列表类型

    + SERIES: 相同视频分类
    + SEASON: 新概念多 P

    **SEASON 类合集与列表名字为`合集·XXX`，请注意区别**
    """

    SERIES = 0
    SEASON = 1


class ChannelSeries:
    """
    合集与列表类

    Attributes:
        credential (Credential): 凭据类. Defaults to None.
    """

    def __init__(
        self,
        uid: int = -1,
        type_: ChannelSeriesType = ChannelSeriesType.SERIES,
        id_: int = -1,
        credential: Union[Credential, None] = None
    ):
        """
        Args:
            uid(int)                : 用户 uid. Defaults to -1.
            type_(ChannelSeriesType): 合集与列表类型. Defaults to ChannelSeriesType.SERIES.
            id_(int)                : season_id 或 series_id. Defaults to -1.
            credential(Credential)  : 凭证. Defaults to None.
        """
        global channel_meta_cache
        assert id_ != -1
        assert type_ != None
        from .user import User
        self.__uid = uid
        self.is_new = type_.value
        self.id_ = id_
        self.owner = User(self.__uid, credential=credential)
        self.credential = credential
        self.meta = None
        if channel_meta_cache[f"{type_.value}-{id_}"] is None:
            if self.is_new:
                api = API_USER["channel_series"]["season_info"]
                params = {
                    "season_id": self.id_
                }
            else:
                api = API_USER["channel_series"]["info"]
                params = {
                    "series_id": self.id_
                }
            resp = json.loads(httpx.get(api["url"], params = params).text)["data"]
            if self.is_new:
                self.meta = resp["info"]
                self.meta["mid"] = resp["info"]["upper"]["mid"]
                self.__uid = self.meta["mid"]
                self.owner = User(self.__uid, credential=credential)
            else:
                self.meta = resp["meta"]
                self.__uid = self.meta["mid"]
                self.owner = User(self.__uid, credential=credential)
        else:
            self.meta = channel_meta_cache[f"{type_.value}-{id_}"]

    def get_meta(self) -> dict:
        """
        获取元数据

        Returns:
            调用 API 返回的结果
        """
        return self.meta # type: ignore

    async def get_videos(
        self, sort: ChannelOrder = ChannelOrder.DEFAULT, pn: int = 1, ps: int = 100
    ) -> dict:
        """
        获取合集视频
        Args:
            sort(ChannelOrder): 排序方式，在旧版列表此参数不起效果。
            pn(int)           : 页数，默认为 1
            ps(int)           : 每一页显示的视频数量

        Returns:
            调用 API 返回的结果
        """
        if self.is_new:
            return await self.owner.get_channel_videos_season(self.id_, sort, pn, ps)
        else:
            return await self.owner.get_channel_videos_series(self.id_, sort, pn, ps)


async def create_channel_series(
    name: str,
    aids: List[int] = [],
    keywords: List[str] = [],
    description: str = "",
    credential: Union[Credential, None] = None
) -> dict:
    """
    新建一个视频列表 (旧版合集)

    Args:
        name (str): 列表名称。
        aids (List[int]): 要加入列表的视频的 aid 列表。
        keywords (List[str]): 列表的关键词。
        description (str): 列表的描述。
        credential (Credential | None): 凭据类。

    Returns:
        dict: 调用 API 返回的结果
    """
    from .user import get_self_info
    credential = credential if credential else Credential()
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    api = API_USER["channel_series"]["create"]
    info = await get_self_info(credential)
    data = {
        "mid": info["mid"],
        "aids": ",".join(map(lambda x: str(x), aids)),
        "name": name,
        "keywords": ",".join(keywords),
        "description": description
    }
    return await request(
        "POST", api["url"], data=data, credential=credential
    )


async def del_channel_series(
    series_id: int,
    credential: Credential
) -> dict:
    """
    删除视频列表(旧版合集)

    Args:
        series_id  (int)       : 旧版合集 id。
        credential (Credential): 凭据类。

    Returns:
        dict: 调用 API 返回的结果
    """
    from .user import get_self_info, User
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    series_total = ChannelSeries(
        type_=ChannelSeriesType.SERIES,
        id_=series_id,
        credential=credential
    ).get_meta()["total"]
    self_uid = (await get_self_info(credential))["mid"]
    aids = []
    pages = series_total // 20 + (1 if (series_total % 20 != 0) else 0)
    for page in range(1, pages + 1, 1):
        page_info = \
            await User(self_uid, credential).get_channel_videos_series(
                series_id,
                page,
                20
            )
        for aid in page_info["aids"]:
            aids.append(aid)
    api = API_USER["channel_series"]["del_channel_series"]
    data = {
        "mid": self_uid,
        "series_id": series_id,
        "aids": ",".join(map(lambda x: str(x), aids))
    }
    return await request(
        "POST", api["url"], data=data, credential=credential
    )


async def add_aids_to_series(
    series_id: int,
    aids: List[int],
    credential: Credential
) -> dict:
    """
    添加视频至视频列表(旧版合集)

    Args:
        series_id  (int)       : 旧版合集 id。
        aids       (List[int]) : 视频 aid 列表。
        credential (Credential): 凭据类。

    Returns:
        dict: 调用 API 返回的结果
    """
    from .user import get_self_info
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    self_info = await get_self_info(credential)
    api = API_USER["channel_series"]["add_channel_aids_series"]
    data = {
        "mid": self_info["mid"],
        "series_id": series_id,
        "aids": ",".join(map(lambda x: str(x), aids))
    }
    return await request(
        "POST", api["url"], data=data, credential=credential
    )


async def del_aids_from_series(
    series_id: int,
    aids: List[int],
    credential: Credential
) -> dict:
    """
    从视频列表(旧版合集)删除视频

    Args:
        series_id  (int)       : 旧版合集 id。
        aids       (List[int]) : 视频 aid 列表。
        credential (Credential): 凭据类。

    Returns:
        dict: 调用 API 返回的结果
    """
    from .user import get_self_info
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    self_info = await get_self_info(credential)
    api = API_USER["channel_series"]["del_channel_aids_series"]
    data = {
        "mid": self_info["mid"],
        "series_id": series_id,
        "aids": ",".join(map(lambda x: str(x), aids))
    }
    return await request(
        "POST", api["url"], data=data, credential=credential
    )
