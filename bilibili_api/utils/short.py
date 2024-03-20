"""
bilibili_api.utils.short

一个很简单的处理短链接的模块，主要是读取跳转链接。
"""
from typing import Optional

from .. import settings
from .credential import Credential
from .network import get_session, get_aiohttp_session, HEADERS
from ..exceptions import ApiException, ArgsException

import re
import random
import string


def acquire_buvid(credential: Optional[Credential] = None) -> str:
    """
    从Credential中取出buvid3，若不存在则生成一个随机的buvid3。

    Args:
        credential(Credential \| None): 凭据类。

    Returns:
        buvid3的字符串
    """

    # return given buvid3 if possible
    if credential:
        buvid3 = credential.get_cookies()['buvid3']

        if buvid3 is not None:
            return buvid3

    # random generation
    buvid3_pattern = '8-4-4-4-17'  # current buvid3 char-length pattern, might be changed later
    parts = buvid3_pattern.split('-')

    buvid3_rand_gen = ["".join(random.choices(string.digits + string.ascii_letters, k=int(part))) for part in parts]

    return "-".join(buvid3_rand_gen) + "infoc"


async def get_short_url(real_url: str, credential: Optional[Credential] = None) -> str:
    """
    获取目标链接的短链接。支持bilibili.com的相关链接。

    Args:
        real_url(str): 目标链接。

        credential(Credential \| None): 凭据类。

    Returns:
        目标链接的b23.tv短链接。

        尽管目标链接可能不存在，但仍然会生成短链接。

        相同的目标链接重复调用此方法会获得不同的短链接。
    """

    # validate the starting part of url
    url_start_pattern = re.compile(pattern=r'^https?:\/\/(?:www\.)?bilibili\.com')

    if not re.match(pattern=url_start_pattern, string=real_url):
        raise ArgsException(msg=f"提供的real_url {real_url} 不符合格式。"
                                f"支持的格式为bilibili.com的相关链接并含有http或https协议。")

    # POST request
    try:
        post_data = {
            'build': str(random.randint(6000000, 10000000)),
            'buvid': acquire_buvid(credential=credential),
            'oid': real_url,
            'platform': random.choice(['android', 'ios']),
            'share_channel': 'COPY',
            'share_id': 'public.webview.0.0.pv',
            'share_mode': str(random.randint(1, 10))
        }

        api_url = 'https://api.biliapi.net/x/share/click'

        if settings.http_client == settings.HTTPClient.HTTPX:
            resp_content = (await get_session().post(url=api_url, headers=HEADERS, data=post_data)).json()
        else:
            resp = await get_aiohttp_session().post(
                url=api_url, data=post_data, headers=HEADERS
            )
            resp_content = await resp.json()

        # the 'content' sometimes will not be in the returned content due to build version, real_url, or buvid (rarely)
        if 'content' not in resp_content['data']:
            raise ApiException(msg="生成短链接失败。若提供的目标链接格式确认正确，请反馈此bug以更新相应params")

        return resp_content['data']['content']

    except Exception as e:
        raise e


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
