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

API = get_api("manga")

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
        params = {
            "comic_id": self.__manga_id
        }
        return await request(
            "POST", api["url"], params=params, credential=self.credential,
            no_csrf=(False if (self.credential.has_sessdata() and self.credential.has_bili_jct()) else True)
        )

    async def __get_info_cached(self) -> dict:
        """
        获取漫画信息，如果有缓存则使用缓存。
        """
        if self.__info == None:
            self.__info = await self.get_info()
        return self.__info

    async def get_episode_info(self, episode_count: Optional[Union[int, float]] = None, episode_id: Optional[int] = None) -> dict:
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

    async def get_episode_id(self, episode_count: Optional[Union[int, float]] = None) -> int:
        """
        获取某一话的 id

        Args:
            episode_count (int | float | None): 第几话.

        Returns:
            int: 对应的话的 id
        """
        return (await self.get_episode_info(episode_count=episode_count))["id"]

    async def get_images_url(self, episode_count: Optional[Union[int, float]] = None, episode_id: Optional[int] = None) -> dict:
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
        params = {
            "ep_id": episode_id
        }
        return await request(
            "POST", api["url"], params=params,
            no_csrf=(False if (self.credential.has_sessdata() and self.credential.has_bili_jct()) else True),
            credential=self.credential
        )

    async def get_images(self, episode_count: Optional[Union[int, float]] = None, episode_id: Optional[int] = None) -> List[Dict]:
        """
        获取某一话的所有图片

        Args:
            episode_count (int | float | None): 第几话.
            episode_id    (int | None)        : 对应的话的 id. 可以通过 `get_episode_id` 获取。

        **注意：episode_count 和 episode_id 中必须提供一个参数。**

        Returns:
            List[Picture]: 所有的图片
        """
        data = await self.get_images_url(episode_count=episode_count, episode_id=episode_id)
        pictures: List[Dict] = []
        async def get_real_image_url(url: str) -> str:
            token_api = API["info"]["image_token"]
            datas = {
                "urls": f"[\"{url}\"]"
            }
            token_data = await request(
                "POST", token_api["url"], data=datas,
                no_csrf=(False if (self.credential.has_sessdata() and self.credential.has_bili_jct()) else True),
                credential=self.credential
            )
            return token_data[0]["url"] + "?token=" + token_data[0]["token"]
        for img in data["images"]:
            url = await get_real_image_url(img["path"])
            pictures.append({
                "x": img["x"],
                "y": img["y"],
                "picture": Picture.from_content(httpx.get(url, headers=HEADERS).content, "jpg")
            })
        return pictures


async def manga_image_url_turn_to_Picture(url: str, credential: Optional[Credential] = None) -> Picture:
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
        datas = {
            "urls": f"[\"{url}\"]"
        }
        token_data = await request(
            "POST", token_api["url"], data=datas,
            no_csrf=(False if (credential.has_sessdata() and credential.has_bili_jct()) else True)
        )
        return token_data[0]["url"] + "?token=" + token_data[0]["token"]
    url = await get_real_image_url(url)
    return Picture.from_url(url)

async def set_follow_manga(manga: Manga, status: bool = True, credential: Optional[Credential] = None) -> dict:
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
    data = {
        "comic_ids": str(manga.get_manga_id())
    }
    return await request("POST", api["url"], data=data, credential=credential)
