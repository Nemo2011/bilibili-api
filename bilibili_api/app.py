"""
bilibili_api.app

手机 APP 相关
"""

import time
from hashlib import md5
from typing import Union

from .utils.utils import get_api
from .utils.network import Api, Credential

API = get_api("app")


async def get_loading_images(
    mobi_app: str = "android",
    platform: str = "android",
    height: int = 1920,
    width: int = 1080,
    build: int = 999999999,
    birth: str = "",
    credential: Union[Credential, None] = None,
):
    """
    获取开屏启动画面

    Args:
        build      (int, optional)              : 客户端内部版本号

        mobi_app   (str, optional)              : android / iphone / ipad

        platform   (str, optional)              : android / ios    / ios

        height     (int, optional)              : 屏幕高度

        width      (int, optional)              : 屏幕宽度

        birth      (str, optional)              : 生日日期(四位数，例 0101)

        credential (Credential | None, optional): 凭据. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential is not None else Credential()

    api = API["splash"]["list"]
    params = {
        "build": build,
        "mobi_app": mobi_app,
        "platform": platform,
        "height": height,
        "width": width,
        "birth": birth,
    }
    return await Api(**api, credential=credential).update_params(**params).result


async def get_loading_images_special(
    mobi_app: str = "android",
    platform: str = "android",
    height: int = 1920,
    width: int = 1080,
    credential: Union[Credential, None] = None,
):
    """
    获取特殊开屏启动画面

    Args:
        mobi_app   (str, optional)              : android / iphone / ipad

        platform   (str, optional)              : android / ios    / ios

        height     (str, optional)              : 屏幕高度

        width      (str, optional)              : 屏幕宽度

        credential (Credential | None, optional): 凭据. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    ts = int(time.time())

    credential = credential if credential is not None else Credential()

    api = API["splash"]["brand"]
    params = {
        "mobi_app": mobi_app,
        "platform": platform,
        "screen_height": height,
        "screen_width": width,
        "ts": ts,
    }
    return await Api(**api, credential=credential).update_params(**params).result
