"""
bilibili_api.utils.short

一个很简单的处理短链接的模块，主要是读取跳转链接。
"""

from .. import settings
from .credential import Credential
from .network import get_session, get_aiohttp_session


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
