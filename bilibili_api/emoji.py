"""
bilibili_api.emoji

表情包相关
"""

from .utils.utils import get_api
from .utils.network import Api, Credential

from typing import Union, List

import os
import json

API = get_api("emoji")


async def get_emoji_list(
    business: str = "reply", credential: Credential = None
) -> dict:
    """
    获取表情包列表

    Args:
        business   (str): 使用场景, reply / dynamic
        credential (Credential): 登录凭证. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    api = API["list"]
    params = {"business": business}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_emoji_detail(id: Union[int, List[int]], business: str = "reply") -> dict:
    """
    获取表情包详情

    Args:
        id       (Union[int, List[int]]): 表情包 id，可通过 `get_emoji_list` 或 `get_all_emoji` 查询。
        business (str): 使用场景, reply / dynamic

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["detail"]
    params = {
        "ids": ",".join([str(i) for i in id]) if isinstance(id, list) else id,
        "business": business,
    }
    return await Api(**api).update_params(**params).result


async def get_all_emoji(business: str = "reply", credential: Credential = None) -> dict:
    """
    获取所有表情包

    Args:
        business   (str): 使用场景, reply / dynamic
        credential (Credential): 登录凭证. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    credential.raise_for_no_sessdata()
    api = API["all"]
    params = {"business": business}
    return await Api(**api, credential=credential).update_params(**params).result

async def add_emoji(package_id: int, credential: Credential = None) -> dict:
    """
    添加表情包

    Args:
        package_id (Union[int, List[int]]): 表情包 id，可通过 `get_emoji_list` 或 `get_all_emoji` 查询。
        credential    (Credential): 登录凭证. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    credential.raise_for_no_sessdata()
    api = API["add"]
    params = {
        'package_id': package_id,
        'business': 'reply',
        'csrf': credential.bili_jct,
    }
    return await Api(**api, credential=credential).update_params(**params).result
