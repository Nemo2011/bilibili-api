"""
bilibili_api.utils.short

一个很简单的处理短链接的模块，主要是读取跳转链接。
"""

from typing import Optional

from .. import settings
from .credential import Credential
from .network import get_session, get_aiohttp_session, get_spi_buvid, HEADERS
from ..exceptions import ApiException, ArgsException

import re
import random
import string


async def acquire_buvid(credential: Optional[Credential] = None) -> str:
    """
    从Credential中取出buvid3，若不存在则通过spi获取buvid，若都不存在则随机生成一个的buvid3。

    Args:
        credential(Credential | None): 凭据类。

    Returns:
        buvid3的字符串
    """

    # return given buvid3 if possible
    if credential:
        buvid3 = credential.get_cookies()["buvid3"]

        if buvid3 is not None:
            return buvid3

    # use spi to get buvid3
    try:
        return (await get_spi_buvid())["data"]["b_3"]

    except KeyError:  # if data or b_3 does not exist by spi
        pass

    # random generation if spi is not possible
    buvid3_pattern = (
        "8-4-4-4-17"  # current buvid3 char-length pattern, might be changed later
    )
    parts = buvid3_pattern.split("-")

    buvid3_rand_gen = [
        "".join(random.choices(string.digits + string.ascii_letters, k=int(part)))
        for part in parts
    ]

    return "-".join(buvid3_rand_gen) + "infoc"


async def get_short_url(
    oid: Optional[int] = None,
    share_content: Optional[str] = None,
    share_title: Optional[str] = None,
    share_origin: Optional[str] = "vinfo_share",
    share_mode: Optional[int] = 3,
    share_id: Optional[str] = "public.webview.0.0.pv",
    platform: Optional[str] = "android",
    mobi_app: Optional[str] = "android",
    panel_type: Optional[int] = 1,
    # regex_real_url: Optional[bool] = False,
    credential: Optional[Credential] = None,
) -> str:
    """
    获取目标链接的短链接。支持 bilibili.com 的相关链接。

    尽管目标链接可能不存在，但仍然会生成短链接。

    相同的目标链接重复调用此方法会获得不同的短链接。

    Args:
        oid            (int | None): 内容 oid。

        share_content  (str | None): 分享内容。

        share_title    (str | None): 分享标题。

        share_origin   (str | None): 分享来源。

        share_mode     (int | None): 分享模式。

        share_id       (str | None): 分享 id。

        platform       (str | None): 平台。

        mobi_app       (str | None): 移动端应用。

        panel_type     (int | None): 面板类型。

        credential   (Credential | None): 凭据类。

    Returns:
        str: 目标链接的 b23.tv 短链接信息 (不一定为单独 URL)
    """
    # 应该具体为检测 oid 类型
    # if regex_real_url:
    #     # validate the starting part of url
    #     url_start_pattern = re.compile(pattern=r"^https?:\/\/(?:www\.)?bilibili\.com")

    #     if not re.match(pattern=url_start_pattern, string=share_content):
    #         raise ArgsException(
    #             msg=f"提供的 {share_content} 不符合格式。\
    #                                 支持的格式为 bilibili.com 的相关链接并含有 http 或 https 协议。"
    #         )

    post_data = {
        "build": 7300400,
        "buvid": await acquire_buvid(credential=credential),
        "oid": oid,
        "share_title": share_title,
        "share_content": share_content,
        "share_origin": share_origin,
        "mobi_app": mobi_app,
        "panel_type": panel_type,
        "platform": platform,
        "share_id": share_id,
        "share_mode": share_mode,
    }

    api_url = "https://api.biliapi.net/x/share/click"

    if settings.http_client == settings.HTTPClient.HTTPX:
        resp_content = (
            await get_session().post(url=api_url, headers=HEADERS, data=post_data)
        ).json()
    else:
        resp = await get_aiohttp_session().post(
            url=api_url, data=post_data, headers=HEADERS
        )
        resp_content = await resp.json()

    # the 'content' sometimes will not be in the returned content due to build version, real_url, or buvid (rarely)
    if "content" not in resp_content["data"]:
        raise ApiException(msg="生成短链接失败。")

    return resp_content["data"]["content"]


async def get_real_url(short_url: str) -> str:
    """
    获取短链接跳转目标，以进行操作。

    Args:
        short_url(str): 短链接。

    Returns:
        目标链接（如果不是有效的链接会报错）

        返回值为原 url 类型
    """

    try:
        if settings.http_client == settings.HTTPClient.HTTPX:
            resp = await get_session().head(url=str(short_url), follow_redirects=True)
        else:
            resp = await get_aiohttp_session().head(
                url=str(short_url), allow_redirects=True
            )
        u = resp.url

        return str(u)
    except Exception as e:
        raise e
