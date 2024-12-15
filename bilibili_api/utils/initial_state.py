"""
bilibili_api.utils.initial_state

用于获取页码的初始化信息
"""

import pprint
import re
import json
import httpx
from enum import Enum
from typing import Tuple

from ..exceptions import *
from .short import get_real_url
from .credential import Credential
from .network import get_session, Api
from .. import settings


class InitialDataType(Enum):
    """
    识别返回类型
    """

    INITIAL_STATE = "window.__INITIAL_STATE__"
    NEXT_DATA = "__NEXT_DATA__"


async def get_initial_state(
    url: str, credential: Credential = Credential()
) -> Tuple[dict, InitialDataType]:
    """
    异步获取初始化信息

    Args:
        url (str): 链接

        credential (Credential, optional): 用户凭证. Defaults to Credential().
    """
    try:
        resp = await Api(
            url=url, method="GET", credential=credential, comment="[获取初始化信息]"
        ).request(byte=True)
    except Exception as e:
        raise e
    else:
        content = resp.decode("utf-8")
        pattern = re.compile(r"window.__INITIAL_STATE__=(\{.*?\});")
        match = re.search(pattern, content)
        if match is None:
            pattern = re.compile(
                pattern=r'<script id="__NEXT_DATA__" type="application/json">\s*(.*?)\s*</script>'
            )
            match = re.search(pattern, content)
            content_type = InitialDataType.NEXT_DATA
            if match is None:
                raise ApiException("未找到相关信息")
        else:
            content_type = InitialDataType.INITIAL_STATE
        try:
            content = json.loads(match.group(1))
        except json.JSONDecodeError:
            raise ApiException("信息解析错误")
        if settings.request_log_show_response:
            settings.logger.info(
                f"获取到 {content_type.value} 初始化信息\n{pprint.pformat(content)}"
            )
        return content, content_type


def get_initial_state_sync(
    url: str, credential: Credential = Credential()
) -> Tuple[dict, InitialDataType]:
    """
    同步获取初始化信息

    Args:
        url (str): 链接

        credential (Credential, optional): 用户凭证. Defaults to Credential().
    """
    try:
        resp = httpx.get(
            url,
            cookies=credential.get_cookies(),
            headers={"User-Agent": "Mozilla/5.0"},
            follow_redirects=True,
        )
    except Exception as e:
        raise e
    else:
        content = resp.text
        pattern = re.compile(r"window.__INITIAL_STATE__=(\{.*?\});")
        match = re.search(pattern, content)
        if match is None:
            pattern = re.compile(
                pattern=r'<script id="__NEXT_DATA__" type="application/json">\s*(.*?)\s*</script>'
            )
            match = re.search(pattern, content)
            content_type = InitialDataType.NEXT_DATA
            if match is None:
                raise ApiException("未找到相关信息")
        else:
            content_type = InitialDataType.INITIAL_STATE
        try:
            content = json.loads(match.group(1))
        except json.JSONDecodeError:
            raise ApiException("信息解析错误")

        return content, content_type
