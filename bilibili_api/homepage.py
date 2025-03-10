"""
bilibili_api.homepage

主页相关操作。
"""

from typing import Union

from .utils.utils import get_api
from .utils.network import Api, Credential

API = get_api("homepage")


async def get_top_photo() -> dict:
    """
    获取主页最上方的图像。
    例如：b 站的风叶穿行，通过这个 API 获取的图片就是风叶穿行的图片。

    Returns:
        dict: 调用 API 返回的结果。
    """
    api = API["info"]["top_photo"]
    params = {"resource_id": 142}
    return await Api(**api).update_params(**params).result


async def get_links(credential: Union[Credential, None] = None) -> dict:
    """
    获取主页左面的链接。
    可能和个人喜好有关。

    Args:
        credential (Credential | None): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["links"]
    params = {"pf": 0, "ids": 4694}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_popularize(credential: Union[Credential, None] = None) -> dict:
    """
    获取推广的项目。
    (有视频有广告)

    Args:
        credential(Credential | None): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["popularize"]
    params = {"pf": 0, "ids": 34}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_videos(credential: Union[Credential, None] = None) -> dict:
    """
    获取首页推荐的视频。

    Args:
        credential (Credential | None): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["videos"]
    return await Api(**api, credential=credential).result


async def get_favorite_list_and_toview(credential: Credential) -> dict:
    """
    获取首页右上角视频相关列表（收藏夹+稍后再看）

    收藏夹具体内容在 `get_favorite_list_content` 接口

    Args:
        credential (Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()
    api = API["list"]["folder"]
    return await Api(**api, credential=credential).result


async def get_favorite_list_content(media_id: int, credential: Union[Credential, None] = None) -> dict:
    """
    获取首页右上角视频相关列表（收藏夹+稍后再看）的具体内容

    稍后再看具体内容在 `get_favorite_list_and_toview` 接口

    Args:
        media_id   (int)       : 收藏夹 id
        credential (Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["list"]["resource"]
    params = {
        "web_location": "333.1007",
        "platform": "web",
        "media_id": media_id
    }
    return await Api(**api, credential=credential).update_params(**params).result
