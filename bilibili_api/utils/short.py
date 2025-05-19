"""
bilibili_api.utils.short

一个很简单的处理短链接的模块，主要是读取跳转链接。
"""

from typing import Optional

from .network import get_client, Credential


async def get_real_url(short_url: str, credential: Optional[Credential] = None) -> str:
    """
    获取短链接跳转目标，以进行操作。

    Args:
        short_url (str): 短链接。

        credential (Credential | None): 凭据类。

    Returns:
        str: 目标链接（如果不是有效的链接会报错）
    """
    credential = credential if credential else Credential()

    try:
        resp = await get_client().request(method="HEAD", url=short_url)
        u = resp.url

        return str(u)
    except Exception as e:
        raise e
