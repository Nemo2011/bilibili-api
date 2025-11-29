"""
bilibili_api.utils.initial_state

用于获取页码的初始化信息
"""

from enum import Enum
import json

from ..exceptions import InitialStateException
from .network import Api, Credential


class InitialDataType(Enum):
    """
    识别返回类型
    """

    INITIAL_STATE = "window.__INITIAL_STATE__"
    NEXT_DATA = "__NEXT_DATA__"
    RENDER_DATA = "__RENDER_DATA__"


def find_json(content: str) -> str:
    patterns = [
        ("window.__INITIAL_STATE__=", InitialDataType.INITIAL_STATE),
        ('window.__initialState = JSON.parse("', InitialDataType.INITIAL_STATE),
        ("window.__initialState = ", InitialDataType.INITIAL_STATE),
        (
            '<script id="__NEXT_DATA__" type="application/json">',
            InitialDataType.NEXT_DATA,
        ),
        (
            '<script id="__RENDER_DATA__" type="application/json">',
            InitialDataType.RENDER_DATA,
        ),
        ("<script>window._render_data_ = ", InitialDataType.RENDER_DATA),
    ]
    for pattern, content_type in patterns:
        pos = content.find(pattern)
        if pos != -1:
            pos += len(pattern)
            return pos, content_type
    return -1, None


async def get_initial_state(
    url: str, credential: Credential = Credential(), strict: bool = True
) -> tuple[dict, InitialDataType]:
    """
    异步获取初始化信息

    Args:
        url (str): 链接

        credential (Credential, optional): 用户凭证. Defaults to Credential().

        strict (bool): 无结果时报错。Defaults to True.
    """
    try:
        resp = await Api(
            url=url, method="GET", credential=credential, comment="[获取初始化信息]"
        ).request(byte=True)
    except Exception as e:
        raise e
    else:
        content = resp.decode("utf-8")
        pos, content_type = find_json(content)
        if pos == -1:
            if strict:
                raise InitialStateException("未找到相关信息")
            return None, None
        try:
            detected_content = content[pos:].strip().strip("\n").strip("\r")
            if detected_content.startswith('{\\"'):  # 暂时都是字典
                detected_content = detected_content.replace(
                    '\\"', '"'
                )  # 存在转义且不在正文内
            content = json.JSONDecoder().raw_decode(detected_content)[0]
        except json.JSONDecodeError:
            raise InitialStateException("信息解析错误")
        return content, content_type
