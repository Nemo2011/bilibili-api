"""
bilibili_api.utils.initial_state

用于获取页码的初始化信息
"""

import re
import json
from enum import Enum
from typing import Tuple

from ..exceptions import *
from .network import Api, Credential, HEADERS


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
        pos = content.find("window.__INITIAL_STATE__=")
        if pos == -1:
            pos = content.find('window.__initialState = JSON.parse("')
            if pos == -1:
                pos = content.find("window.__initialState = ")
                if pos == -1:
                    pos = content.find('<script id="__NEXT_DATA__" type="application/json">')
                    if pos == -1:
                        raise ApiException("未找到相关信息")
                    else:
                        content_type = InitialDataType.NEXT_DATA
                        pos += len('<script id="__NEXT_DATA__" type="application/json">')
                else:
                    content_type = InitialDataType.INITIAL_STATE
                    pos += len("window.__initialState = ")
            else:
                content_type = InitialDataType.INITIAL_STATE
                pos += len('window.__initialState = JSON.parse("')
        else:
            content_type = InitialDataType.INITIAL_STATE
            pos += len("window.__INITIAL_STATE__=")
        try:
            detected_content = content[pos:].strip().strip("\n").strip("\r")
            if detected_content.startswith("{\\\""): # 暂时都是字典
                detected_content = detected_content.replace("\\\"", "\"") # 存在转义且不在正文内
            content = json.JSONDecoder().raw_decode(detected_content)[0]
        except json.JSONDecodeError as e:
            raise ApiException("信息解析错误")
        return content, content_type
