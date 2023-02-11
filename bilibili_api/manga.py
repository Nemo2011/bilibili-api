"""
bilibili_api.manga

漫画相关操作
"""

from bilibili_api.utils.network_httpx import request, HEADERS
from bilibili_api.utils.utils import get_api
from bilibili_api.utils.Credential import Credential
from bilibili_api.errors import ArgsException
from bilibili_api.utils.Picture import Picture
from typing import Optional, List, Dict, Union
from urllib.parse import urlparse
import httpx
from enum import Enum
import datetime

API = get_api("manga")


class MangaIndexFilter:
    """
    漫画索引筛选器类。
    """

    class Area(Enum):
        """
        漫画索引筛选器的地区枚举类。

        - ALL: 全部
        - CHINA: 大陆
        - JAPAN: 日本
        - SOUTHKOREA: 韩国
        - OTHER: 其他
        """

        ALL = -1
        CHINA = 1
        JAPAN = 2
        SOUTHKOREA = 6
        OTHER = 5

    class Order(Enum):
        """
        漫画索引筛选器的排序枚举类。

        - HOT: 人气推荐
        - UPDATE: 更新时间
        - RELEASE_DATE: 上架时间
        """

        HOT = 0
        UPDATE = 1
        RELEASE_DATE = 3

    class Status(Enum):
        """
        漫画索引筛选器的状态枚举类。

        - ALL: 全部
        - FINISHED: 完结
        - UNFINISHED: 连载
        """

        ALL = -1
        FINISHED = 1
        UNFINISHED = 0

    class Payment(Enum):
        """
        漫画索引筛选器的付费枚举类。

        - ALL: 全部
        - FREE: 免费
        - PAID: 付费
        - WILL_BE_FREE: 等就免费
        """

        ALL = -1
        FREE = 1
        PAID = 2
        WILL_BE_FREE = 3

    class Style(Enum):
        """
        漫画索引筛选器的风格枚举类。

        - ALL: 全部
        - WARM: 热血
        - ANCIENT: 古风
        - FANTASY: 玄幻
        - IMAGING: 奇幻
        - SUSPENSE: 悬疑
        - CITY: 都市
        - HISTORY: 历史
        - WUXIA: 武侠仙侠
        - GAME: 游戏竞技
        - PARANORMAL: 悬疑灵异
        - ALTERNATE: 架空
        - YOUTH: 青春
        - WEST_MAGIC: 西幻
        - MORDEN: 现代
        - POSITIVE: 正能量
        - SCIENCE_FICTION: 科幻
        """

        ALL = -1
        WARM = 999
        ANCIENT = 997
        FANTASY = 1016
        IMAGING = 998
        SUSPENSE = 1023
        CITY = 1002
        HISTORY = 1096
        WUXIA = 1092
        GAME = 1088
        PARANORMAL = 1081
        ALTERNATE = 1063
        YOUTH = 1060
        WEST_MAGIC = 1054
        MORDEN = 1048
        POSITIVE = 1028
        SCIENCE_FICTION = 1027


class Manga:
    """
    漫画类

    Attributes:
        credential (Credential): 凭据类。
    """

    def __init__(self, manga_id: int, credential: Optional[Credential] = None):
        """
        Args:
            manga_id   (int)              : 漫画 id
            credential (Credential | None): 凭据类. Defaults to None.
        """
        credential = credential if credential else Credential()
        self.__manga_id = manga_id
        self.credential = credential
        self.__info: Optional[Dict] = None

    def get_manga_id(self) -> int:
        return self.__manga_id

    async def get_info(self) -> dict:
        """
        获取漫画信息

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["detail"]
        params = {"comic_id": self.__manga_id}
        return await request(
            "POST",
            api["url"],
            params=params,
            credential=self.credential,
            no_csrf=(
                False
                if (self.credential.has_sessdata() and self.credential.has_bili_jct())
                else True
            ),
        )

    async def __get_info_cached(self) -> dict:
        """
        获取漫画信息，如果有缓存则使用缓存。
        """
        if self.__info == None:
            self.__info = await self.get_info()
        return self.__info

    async def get_episode_info(
        self,
        episode_count: Optional[Union[int, float]] = None,
        episode_id: Optional[int] = None,
    ) -> dict:
        """
        获取某一话的详细信息

        Args:
            episode_count (int | float | None): 第几话.
            episode_id    (int | None)        : 对应的话的 id. 可以通过 `get_episode_id` 获取。

        **注意：episode_count 和 episode_id 中必须提供一个参数。**

        Returns:
            dict: 对应的话的详细信息
        """
        info = await self.__get_info_cached()
        for ep in info["ep_list"]:
            if episode_count == None:
                if ep["id"] == episode_id:
                    return ep
            elif episode_id == None:
                if ep["ord"] == episode_count:
                    return ep
            else:
                raise ArgsException("episode_count 和 episode_id 中必须提供一个参数。")
        raise ArgsException("未找到对应的话")

    async def get_episode_id(
        self, episode_count: Optional[Union[int, float]] = None
    ) -> int:
        """
        获取某一话的 id

        Args:
            episode_count (int | float | None): 第几话.

        Returns:
            int: 对应的话的 id
        """
        return (await self.get_episode_info(episode_count=episode_count))["id"]

    async def get_images_url(
        self,
        episode_count: Optional[Union[int, float]] = None,
        episode_id: Optional[int] = None,
    ) -> dict:
        """
        获取某一话的图片链接。(未经过处理，所有的链接无法直接访问)

        获取的图片 url 请传入 `manga.manga_image_url_turn_to_Picture` 函数以转换为 `Picture` 类。

        Args:
            episode_count (int | float | None): 第几话.
            episode_id    (int | None)        : 对应的话的 id. 可以通过 `get_episode_id` 获取。

        **注意：episode_count 和 episode_id 中必须提供一个参数。**

        Returns:
            dict: 调用 API 返回的结果
        """
        if episode_id == None:
            if episode_count == None:
                raise ArgsException("episode_count 和 episode_id 中必须提供一个参数。")
            episode_id = await self.get_episode_id(episode_count)
        api = API["info"]["episode_images"]
        params = {"ep_id": episode_id}
        return await request(
            "POST",
            api["url"],
            params=params,
            no_csrf=(
                False
                if (self.credential.has_sessdata() and self.credential.has_bili_jct())
                else True
            ),
            credential=self.credential,
        )

    async def get_images(
        self,
        episode_count: Optional[Union[int, float]] = None,
        episode_id: Optional[int] = None,
    ) -> List[Dict]:
        """
        获取某一话的所有图片

        Args:
            episode_count (int | float | None): 第几话.
            episode_id    (int | None)        : 对应的话的 id. 可以通过 `get_episode_id` 获取。

        **注意：episode_count 和 episode_id 中必须提供一个参数。**

        Returns:
            List[Picture]: 所有的图片
        """
        data = await self.get_images_url(
            episode_count=episode_count, episode_id=episode_id
        )
        pictures: List[Dict] = []

        async def get_real_image_url(url: str) -> str:
            token_api = API["info"]["image_token"]
            datas = {"urls": f'["{url}"]'}
            token_data = await request(
                "POST",
                token_api["url"],
                data=datas,
                no_csrf=(
                    False
                    if (
                        self.credential.has_sessdata()
                        and self.credential.has_bili_jct()
                    )
                    else True
                ),
                credential=self.credential,
            )
            return token_data[0]["url"] + "?token=" + token_data[0]["token"]

        for img in data["images"]:
            url = await get_real_image_url(img["path"])
            pictures.append(
                {
                    "x": img["x"],
                    "y": img["y"],
                    "picture": Picture.from_content(
                        httpx.get(url, headers=HEADERS).content, "jpg"
                    ),
                }
            )
        return pictures


async def manga_image_url_turn_to_Picture(
    url: str, credential: Optional[Credential] = None
) -> Picture:
    """
    将 Manga.get_images_url 函数获得的图片 url 转换为 Picture 类。

    Args:
        url        (str)               : 未经处理的漫画图片链接。
        credential (Credential \| None): 凭据类. Defaults to None.

    Returns:
        Picture: 图片类。
    """
    url = urlparse(url).path
    credential = credential if credential else Credential()

    async def get_real_image_url(url: str) -> str:
        token_api = API["info"]["image_token"]
        datas = {"urls": f'["{url}"]'}
        token_data = await request(
            "POST",
            token_api["url"],
            data=datas,
            no_csrf=(
                False
                if (credential.has_sessdata() and credential.has_bili_jct())
                else True
            ),
        )
        return f'{token_data[0]["url"]}?token={token_data[0]["token"]}'

    url = await get_real_image_url(url)
    return Picture.from_url(url)


async def set_follow_manga(
    manga: Manga, status: bool = True, credential: Optional[Credential] = None
) -> dict:
    """
    设置追漫

    Args:
        manga      (Manga)     : 漫画类。
        status     (bool)      : 设置是否追漫。是为 True，否为 False。Defaults to True.
        credential (Credential): 凭据类。
    """
    if credential == None:
        if manga.credential.has_sessdata() and manga.credential.has_bili_jct():
            credential = manga.credential
        else:
            credential = Credential()
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    if status == True:
        api = API["operate"]["add_favorite"]
    else:
        api = API["operate"]["del_favorite"]
    data = {"comic_ids": str(manga.get_manga_id())}
    return await request("POST", api["url"], data=data, credential=credential)


async def get_raw_manga_index(
    area: MangaIndexFilter.Area = MangaIndexFilter.Area.ALL,
    order: MangaIndexFilter.Order = MangaIndexFilter.Order.HOT,
    status: MangaIndexFilter.Status = MangaIndexFilter.Status.ALL,
    payment: MangaIndexFilter.Payment = MangaIndexFilter.Payment.ALL,
    style: MangaIndexFilter.Style = MangaIndexFilter.Style.ALL,
    pn: int = 1,
    ps: int = 18,
) -> list:
    """
    获取漫画索引

    Args:
        area    (MangaIndexFilter.Area)   : 地区。Defaults to MangaIndexFilter.Area.ALL.
        order   (MangaIndexFilter.Order)  : 排序。Defaults to MangaIndexFilter.Order.HOT.
        status  (MangaIndexFilter.Status) : 状态。Defaults to MangaIndexFilter.Status.ALL.
        payment (MangaIndexFilter.Payment): 支付。Defaults to MangaIndexFilter.Payment.ALL.
        style   (MangaIndexFilter.Style)  : 风格。Defaults to MangaIndexFilter.Style.ALL.
        pn      (int)                     : 页码。Defaults to 1.
        ps      (int)                     : 每页数量。Defaults to 18.

    Returns:
        list: 调用 API 返回的结果
    """
    api = API["info"]["index"]
    params = {"device": "pc", "platform": "web"}
    data = {
        "area_id": area.value,
        "order": order.value,
        "is_finish": status.value,
        "is_free": payment.value,
        "style_id": style.value,
        "page_num": pn,
        "page_size": ps,
    }
    return await request("POST", api["url"], data=data, params=params, no_csrf=True)


async def get_manga_index(
    area: MangaIndexFilter.Area = MangaIndexFilter.Area.ALL,
    order: MangaIndexFilter.Order = MangaIndexFilter.Order.HOT,
    status: MangaIndexFilter.Status = MangaIndexFilter.Status.ALL,
    payment: MangaIndexFilter.Payment = MangaIndexFilter.Payment.ALL,
    style: MangaIndexFilter.Style = MangaIndexFilter.Style.ALL,
    pn: int = 1,
    ps: int = 18,
) -> List[Manga]:
    """
    获取漫画索引

    Args:
        area    (MangaIndexFilter.Area)   : 地区。Defaults to MangaIndexFilter.Area.ALL.
        order   (MangaIndexFilter.Order)  : 排序。Defaults to MangaIndexFilter.Order.HOT.
        status  (MangaIndexFilter.Status) : 状态。Defaults to MangaIndexFilter.Status.ALL.
        payment (MangaIndexFilter.Payment): 支付。Defaults to MangaIndexFilter.Payment.ALL.
        style   (MangaIndexFilter.Style)  : 风格。Defaults to MangaIndexFilter.Style.ALL.
        pn      (int)                     : 页码。Defaults to 1.
        ps      (int)                     : 每页数量。Defaults to 18.

    Returns:
        List[Manga]: 漫画索引
    """
    data = await get_raw_manga_index(area, order, status, payment, style, pn, ps)
    return [Manga(manga_data["season_id"]) for manga_data in data]


async def get_manga_update(date: Union[str, datetime.datetime] = datetime.datetime.now(), pn: int = 1, ps: int = 8) -> List[Manga]:
    """
    获取更新推荐的漫画

    Args:
        date (Union[str, datetime.datetime]): 日期，默认为今日。
        pn   (int)                          : 页码。Defaults to 1.
        ps   (int)                          : 每页数量。Defaults to 8.
    Returns:
        List[Manga]: 漫画列表
    """
    api = API["info"]["update"]
    params = {"device": "pc", "platform": "web"}
    if isinstance(date, datetime.datetime):
        date = date.strftime("%Y-%m-%d")
    data = {"date": date, "page_num": pn, "page_size": ps}
    manga_data = await request("POST", api["url"], no_csrf=True, params=params, data=data)
    return [Manga(manga["comic_id"]) for manga in manga_data["list"]]