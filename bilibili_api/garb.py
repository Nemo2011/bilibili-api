"""
bilibili_api.garb

装扮/收藏集相关
"""

from enum import Enum
from typing import ClassVar

from .utils.network import Api, Credential
from .utils.utils import get_api

dlc_lottery_id = {}


API = get_api("garb")


class GarbType(Enum):
    """
    收藏集/装扮类型

    - GARB: 装扮
    - PENDANT: 头像挂件
    - CARD: 动态卡片
    """

    GARB: ClassVar[dict[str, int]] = {"group_id": 0, "part_id": 6}
    PENDANT: ClassVar[dict[str, int]] = {"group_id": 22, "part_id": 1}
    CARD: ClassVar[dict[str, int]] = {"group_id": 5, "part_id": 2}


class GarbSortType(Enum):
    """
    收藏集/装扮排序方式

    - DEFAULT: 默认排序
    - SELL: 按销量排序
    - LATEST: 按最新上架时间排序
    """

    DEFAULT = 0
    SELL = 1
    LATEST = 2


async def search_garb_dlc_raw(
    keyword: str, pn: int = 1, ps: int = 20, credential: Credential | None = None
) -> dict:
    """
    搜索装扮/收藏集

    Args:
        keyword    (str)                 : 关键词
        pn         (int)                 : 页码. Defaults to 1.
        ps         (int)                 : 每页大小. Defaults to 20.
        credential (Credential, optional): 凭据类. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果。
    """
    credential = credential if credential else Credential()
    api = API["common"]["search"]
    params = {
        "key_word": keyword,
        "pn": pn,
        "ps": ps,
        "csrf": credential.get_core_cookies()["bili_jct"],
    }
    return await Api(**api, credential=credential).update_params(**params).result


class DLC:
    """
    收藏集对象

    Attributes:
        credential (Credential): 凭据类。
    """

    def __init__(self, act_id: int, credential: Credential | None = None) -> None:
        """
        Args:
            act_id (int): 收藏集的 act_id。 (链接中 blackboard/activity-Mz9T5bO5Q3.html?id={act_id}... 即为 act_id)
            credential (Credential | None, optional): 凭据类。Defaults to None.
        """
        self.__act_id = act_id
        self.__lottery_id = None
        self.__basic_info = None
        self.credential = credential if credential else Credential()
        if dlc_lottery_id.get(self.__act_id):
            self.__lottery_id = dlc_lottery_id[self.__act_id]

    def get_act_id(self) -> int:
        """
        获取 act_id。

        Returns:
            int: act_id
        """
        return self.__act_id

    def set_act_id(self, act_id: int) -> int:
        """
        设置 act_id

        Args:
            act_id (int): act_id
        """
        self.__init__(act_id=act_id, credential=self.credential)

    async def get_info(self) -> dict:
        """
        获取收藏集信息

        Returns:
            dict: 调用 API 返回的结果
        """
        if not self.__basic_info:
            api = API["dlc"]["basic"]
            params = {
                "act_id": self.__act_id,
                "csrf": self.credential.get_core_cookies()["bili_jct"],
            }
            self.__basic_info = (
                await Api(**api, credential=self.credential)
                .update_params(**params)
                .result
            )
            self.__lottery_id = self.__basic_info["lottery_list"][0]["lottery_id"]
        return self.__basic_info

    async def get_lottery_id(self) -> int:
        """
        获取 lottery_id

        Returns:
            int: lottery_id
        """
        if not self.__lottery_id:
            await self.get_info()
        return self.__lottery_id

    async def get_detail(self) -> dict:
        """
        获取收藏集详情

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["dlc"]["detail"]
        params = {
            "act_id": self.__act_id,
            "lottery_id": await self.get_lottery_id(),
            "csrf": self.credential.get_core_cookies()["bili_jct"],
        }
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )


class Garb:
    """
    装扮类

    Attributes:
        credential (Credential): 凭据类。
    """

    def __init__(self, item_id: int, credential: Credential | None = None) -> None:
        """
        Args:
            act_id (int): 装扮的 item_id。(可通过 garb.search_garb_dlc_raw 获取)
            credential (Credential | None, optional): 凭据类。Defaults to None.
        """
        self.__item_id = item_id
        self.credential = credential if credential else Credential()

    def get_item_id(self) -> int:
        """
        获取 item_id

        Returns:
            int: item_id
        """
        return self.__item_id

    def set_item_id(self, item_id: int) -> None:
        """
        设置 item_id

        Args:
            item_id (int): item_id
        """
        self.__init__(item_id=item_id, credential=self.credential)

    async def get_detail(self) -> dict:
        """
        获取装扮详细

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["garb"]["detail"]
        params = {
            "item_id": self.__item_id,
            "csrf": self.credential.get_core_cookies()["bili_jct"],
        }
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )


async def search_garb_dlc_obj(
    keyword: str, pn: int = 1, ps: int = 20, credential: Credential | None = None
) -> list[DLC | Garb]:
    """
    搜索装扮/收藏集

    Args:
        keyword    (str)                 : 关键词
        pn         (int)                 : 页码. Defaults to 1.
        ps         (int)                 : 每页大小. Defaults to 20.
        credential (Credential, optional): 凭据类. Defaults to None.

    Returns:
        List[DLC | Garb]: 装扮/收藏集对象列表
    """
    credential = credential if credential else Credential()
    res = await search_garb_dlc_raw(
        keyword=keyword, pn=pn, ps=ps, credential=credential
    )
    ret = []
    for obj in res["list"]:
        if obj["item_id"] == 0:
            act_id = int(obj["properties"]["dlc_act_id"])
            dlc_lottery_id[act_id] = int(obj["properties"]["dlc_lottery_id"])
            ret.append(DLC(act_id, credential=credential))
        else:
            ret.append(Garb(obj["item_id"]))
    return ret


async def search_garb_dlc(
    keyword: str, pn: int = 1, ps: int = 20, credential: Credential | None = None
) -> list[tuple[dict, DLC | Garb]]:
    """
    搜索装扮/收藏集

    Args:
        keyword    (str)                 : 关键词
        pn         (int)                 : 页码. Defaults to 1.
        ps         (int)                 : 每页大小. Defaults to 20.
        credential (Credential, optional): 凭据类. Defaults to None.

    Returns:
        List[Tuple[dict, DLC | Garb]]: 装扮/收藏集信息与装扮/收藏集对象列表
    """
    credential = credential if credential else Credential()
    res = await search_garb_dlc_raw(
        keyword=keyword, pn=pn, ps=ps, credential=credential
    )
    ret = []
    for obj in res["list"]:
        if obj["item_id"] == 0:
            act_id = int(obj["properties"]["dlc_act_id"])
            dlc_lottery_id[act_id] = int(obj["properties"]["dlc_lottery_id"])
            ret.append((obj, DLC(act_id, credential=credential)))
        else:
            ret.append((obj, Garb(obj["item_id"])))
    return ret


async def get_garb_dlc_items_raw(
    type_: GarbType = GarbType.GARB,
    sort: GarbSortType = GarbSortType.DEFAULT,
    pn: int = 1,
    ps: int = 20,
    credential: Credential | None = None,
) -> dict:
    """
    装扮/收藏集列表

    Args:
        type_      (GarbType)            : 装扮/收藏集类型
        sort       (GarbSortType)        : 装扮/收藏集排序方式
        pn         (int)                 : 页码. Defaults to 1.
        ps         (int)                 : 每页大小. Defaults to 20.
        credential (Credential, optional): 凭据类. Defaults to None.

    Returns:
        List[Tuple[dict, DLC | Garb]]: 装扮/收藏集信息与装扮/收藏集对象列表
    """
    credential = credential if credential else Credential()
    api = API["common"]["list"]
    params = {
        "sort_type": sort.value,
        "pn": pn,
        "ps": ps,
        "csrf": credential.get_core_cookies()["bili_jct"],
    }
    params.update(type_.value)
    return await Api(**api, credential=credential).update_params(**params).result


async def get_garb_dlc_items_obj(
    type_: GarbType = GarbType.GARB,
    sort: GarbSortType = GarbSortType.DEFAULT,
    pn: int = 1,
    ps: int = 20,
    credential: Credential | None = None,
) -> dict:
    """
    装扮/收藏集列表

    Args:
        type_      (GarbType)            : 装扮/收藏集类型
        sort       (GarbSortType)        : 装扮/收藏集排序方式
        pn         (int)                 : 页码. Defaults to 1.
        ps         (int)                 : 每页大小. Defaults to 20.
        credential (Credential, optional): 凭据类. Defaults to None.

    Returns:
        List[DLC | Garb]: 装扮/收藏集对象列表
    """
    credential = credential if credential else Credential()
    res = await get_garb_dlc_items_raw(
        type_=type_, sort=sort, pn=pn, ps=ps, credential=credential
    )
    ret = []
    for obj in res["list"]:
        if obj["item_id"] == 0:
            act_id = int(obj["properties"]["dlc_act_id"])
            dlc_lottery_id[act_id] = int(obj["properties"]["dlc_lottery_id"])
            ret.append(DLC(act_id, credential=credential))
        else:
            ret.append(Garb(obj["item_id"]))
    return ret


async def get_garb_dlc_items(
    type_: GarbType = GarbType.GARB,
    sort: GarbSortType = GarbSortType.DEFAULT,
    pn: int = 1,
    ps: int = 20,
    credential: Credential | None = None,
) -> dict:
    """
    装扮/收藏集列表

    Args:
        type_      (GarbType)            : 装扮/收藏集类型
        sort       (GarbSortType)        : 装扮/收藏集排序方式
        pn         (int)                 : 页码. Defaults to 1.
        ps         (int)                 : 每页大小. Defaults to 20.
        credential (Credential, optional): 凭据类. Defaults to None.

    Returns:
        List[Tuple[dict, DLC | Garb]]: 装扮/收藏集信息与装扮/收藏集对象列表
    """
    credential = credential if credential else Credential()
    res = await get_garb_dlc_items_raw(
        type_=type_, sort=sort, pn=pn, ps=ps, credential=credential
    )
    ret = []
    for obj in res["list"]:
        if obj["item_id"] == 0:
            act_id = int(obj["properties"]["dlc_act_id"])
            dlc_lottery_id[act_id] = int(obj["properties"]["dlc_lottery_id"])
            ret.append((obj, DLC(act_id, credential=credential)))
        else:
            ret.append((obj, Garb(obj["item_id"])))
    return ret
