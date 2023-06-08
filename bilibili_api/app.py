"""
bilibili_api.app

手机 APP 相关
"""

from .utils.utils import get_api
from .utils.credential import Credential
from .utils.network_httpx import request
from hashlib import md5
import time
from typing import Union

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
    return await request("GET", api["url"], params, credential=credential)


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
    APPKEY = "1d8b6e7d45233436"
    APPSEC = "560c52ccd288fed045859ed18bffd973"

    ts = int(time.time())

    credential = credential if credential is not None else Credential()

    api = API["splash"]["brand"]
    sign_params = (
        "appkey="
        + APPKEY
        + "&mobi_app="
        + mobi_app
        + "&platform="
        + platform
        + "&screen_height="
        + str(height)
        + "&screen_width="
        + str(width)
        + "&ts="
        + str(ts)
        + APPSEC
    )

    sign = md5()
    sign.update(sign_params.encode(encoding="utf-8"))
    sign = sign.hexdigest()

    params = {
        "appkey": APPKEY,
        "mobi_app": mobi_app,
        "platform": platform,
        "screen_height": height,
        "screen_width": width,
        "ts": ts,
        "sign": sign,
    }
    return await request("GET", api["url"], params, credential=credential)
