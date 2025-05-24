"""
bilibili_api.utils.network

与网络请求相关的模块。能对会话进行管理（复用 TCP 连接）。
"""

import asyncio
import atexit
import binascii
import hashlib
import hmac
import io
import json
import logging
import random
import re
import struct
import time
import urllib.parse
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from functools import reduce
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA

from ..exceptions import (
    ArgsException,
    CookiesRefreshException,
    CredentialNoAcTimeValueException,
    CredentialNoBiliJctException,
    CredentialNoBuvid3Exception,
    CredentialNoBuvid4Exception,
    CredentialNoDedeUserIDException,
    CredentialNoSessdataException,
    ExClimbWuzhiException,
    ResponseCodeException,
    WbiRetryTimesExceedException,
    NetworkException,
)
from .AsyncEvent import AsyncEvent
from .utils import get_api, raise_for_statement

################################################## BEGIN Logger ##################################################


class RequestLog(AsyncEvent):
    def __init__(self) -> None:
        super().__init__()
        self.logger: logging.Logger = logging.getLogger("bilibili-api-request")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    "[BILIBILI_API][%(asctime)s][%(levelname)s] %(message)s"
                )
            )
            self.logger.addHandler(handler)
        self.__on = False
        self.__on_events: List[str] = [
            "API_REQUEST",
            "API_RESPONSE",
            "ANTI_SPIDER",
            "WS_CONNECT",
            "WS_RECV",
            "WS_SEND",
            "WS_CLOSE",
        ]
        self.__ignore_events: List[str] = []
        self.add_event_listener("__ALL__", self.__handle_events)

    def get_on_events(self) -> List[str]:
        """
        获取日志输出支持的事件类型

        Returns:
            List[str]: 日志输出支持的事件类型
        """
        return self.__on_events

    def set_on_events(self, events: List[str]) -> None:
        """
        设置日志输出支持的事件类型

        Args:
            events (List[str]): 日志输出支持的事件类型
        """
        self.__on_events = events

    def get_ignore_events(self) -> List[str]:
        """
        获取日志输出排除的事件类型

        Returns:
            List[str]: 日志输出排除的事件类型
        """
        return self.__ignore_events

    def set_ignore_events(self, events: List[str]) -> None:
        """
        设置日志输出排除的事件类型

        Args:
            events (List[str]): 日志输出排除的事件类型
        """
        self.__ignore_events = events

    def is_on(self) -> bool:
        """
        获取日志输出是否启用

        Returns:
            bool: 是否启用
        """
        return self.__on

    def set_on(self, status: bool) -> None:
        """
        设置日志输出是否启用

        Args:
            status (bool): 是否启用
        """
        self.__on = status

    def __handle_events(self, data: dict) -> None:
        evt = data["name"]
        desc, real_data = data["data"]
        if (
            self.__on
            and evt in self.get_on_events()
            and not evt in self.get_ignore_events()
        ):
            if evt.startswith("WS_"):
                ws_id = real_data.pop("id")
                self.logger.info(f"WS #{ws_id} {desc}: {real_data}")
            elif evt.startswith("DWN_"):
                dwn_id = real_data.pop("id")
                self.logger.info(f"DWN #{dwn_id} {desc}: {real_data}")
            elif evt == "ANTI_SPIDER":
                self.logger.info(f"{real_data['msg']}")
            else:
                self.logger.info(f"{desc}: {real_data}")


request_log = RequestLog()
"""
请求日志支持，默认支持输出到指定 I/O 对象。

可以添加更多监听器达到更多效果。

Logger: request_log.logger

Extends: AsyncEvent

Events:

- (模块自带 BiliAPIClient)
- REQUEST:     HTTP 请求。
- RESPONSE:    HTTP 响应。
- WS_CREATE:   新建的 Websocket 请求。
- WS_RECV:     获得到 WebSocket 请求。
- WS_SEND:     发送了 WebSocket 请求。
- WS_CLOSE:    关闭 WebSocket 请求。
- DWN_CREATE:  新建下载。
- DWN_PART:    部分下载。
- (Api)
- API_REQUEST: Api 请求。
- API_RESPONSE: Api 响应。
- (反爬虫)
- ANTI_SPIDER: 反爬虫相关信息。

CallbackData: 描述 (str) 数据 (dict)

示例：

``` python
@request_log.on("REQUEST")
async def handle(desc: str, data: dict) -> None:
    print(desc, data)
```

默认启用 Api 和 Anti-Spider 相关信息。
"""
request_log.__doc__ = """
请求日志支持，默认支持输出到指定 I/O 对象。

可以添加更多监听器达到更多效果。

Logger: request_log.logger

Extends: AsyncEvent

Events:

- (模块自带 BiliAPIClient)
- REQUEST:     HTTP 请求。
- RESPONSE:    HTTP 响应。
- WS_CREATE:   新建的 Websocket 请求。
- WS_RECV:     获得到 WebSocket 请求。
- WS_SEND:     发送了 WebSocket 请求。
- WS_CLOSE:    关闭 WebSocket 请求。
- DWN_CREATE:  新建下载。
- DWN_PART:    部分下载。
- (Api)
- API_REQUEST: Api 请求。
- API_RESPONSE: Api 响应。
- (反爬虫)
- ANTI_SPIDER: 反爬虫相关信息。

CallbackData: 描述 (str) 数据 (dict)

示例：

``` python
@request_log.on("REQUEST")
async def handle(desc: str, data: dict) -> None:
    print(desc, data)
```

默认启用 Api 和 Anti-Spider 相关信息。
"""


################################################## END Logger ##################################################


################################################## BEGIN Session Management ##################################################


sessions: Dict[str, Type["BiliAPIClient"]] = {}
session_pool: Dict[str, Dict[asyncio.AbstractEventLoop, "BiliAPIClient"]] = {}
client_settings: Dict[str, list] = {}
selected_client: str = ""


class RequestSettings:
    def __init__(self):
        self.__settings: dict = {
            "proxy": "",
            "timeout": 5.0,
            "verify_ssl": True,
            "trust_env": True,
        }
        self.__wbi_retry_times = 3
        self.__enable_auto_buvid = True
        self.__enable_bili_ticket = False

    def get(self, name: str) -> Any:
        """
        获取某项设置

        不可用于 `wbi_retry_times` `enable_auto_buvid` `enable_bili_ticket`

        默认设置名称：`proxy` `timeout` `verify_ssl` `trust_env`

        Args:
            name (str): 设置名称

        Returns:
            Any: 设置的值
        """
        return self.__settings[name]

    def set(self, name: str, value: Any) -> None:
        """
        设置某项设置

        不可用于 `wbi_retry_times` `enable_auto_buvid` `enable_bili_ticket`

        默认设置名称：`proxy` `timeout` `verify_ssl` `trust_env`

        Args:
            name  (str): 设置名称
            value (str): 设置的值
        """
        global session_pool
        self.__settings[name] = value
        for _, pool in session_pool.items():
            for _, client in pool.items():
                client.__getattribute__(f"set_{name}")(value)

    def get_proxy(self) -> str:
        """
        获取设置的代理

        Returns:
            str: 代理地址. Defaults to "".
        """
        return self.get("proxy")

    def set_proxy(self, proxy: str):
        """
        修改设置的代理

        Args:
            proxy (str): 代理地址
        """
        self.set("proxy", proxy)

    def get_timeout(self) -> float:
        """
        获取设置的 web 请求超时时间

        Returns:
            float: 超时时间. Defaults to 5.0.
        """
        return self.get("timeout")

    def set_timeout(self, timeout: float):
        """
        修改设置的 web 请求超时时间

        Args:
            timeout (float): 超时时间
        """
        self.set("timeout", timeout)

    def get_verify_ssl(self) -> bool:
        """
        获取设置的是否验证 SSL

        Returns:
            bool: 是否验证 SSL. Defaults to True.
        """
        return self.get("verify_ssl")

    def set_verify_ssl(self, verify_ssl: bool):
        """
        修改设置的是否验证 SSL

        Args:
            verify_ssl (bool): 是否验证 SSL
        """
        self.set("verify_ssl", verify_ssl)

    def get_trust_env(self) -> bool:
        """
        获取设置的 `trust_env`

        Returns:
            bool: `trust_env`. Defaults to True.
        """
        return self.get("trust_env")

    def set_trust_env(self, trust_env: bool):
        """
        修改设置的 `trust_env`

        Args:
            verify_ssl (bool): `trust_env`
        """
        self.set("trust_env", trust_env)

    def get_wbi_retry_times(self) -> int:
        """
        获取设置的 wbi 重试次数

        Returns:
            int: wbi 重试次数. Defaults to 3.
        """
        return self.__wbi_retry_times

    def set_wbi_retry_times(self, wbi_retry_times: int) -> None:
        """
        修改设置的 wbi 重试次数

        Args:
            wbi_retry_times (int): wbi 重试次数.
        """
        self.__wbi_retry_times = wbi_retry_times

    def get_enable_auto_buvid(self) -> bool:
        """
        获取设置的是否自动生成 buvid

        Returns:
            bool: 是否自动生成 buvid. Defaults to True.
        """
        return self.__enable_auto_buvid

    def set_enable_auto_buvid(self, enable_auto_buvid: bool) -> None:
        """
        设置是否自动生成 buvid

        Args:
            enable_auto_buvid (bool): 是否自动生成 buvid.
        """
        self.__enable_auto_buvid = enable_auto_buvid

    def get_enable_bili_ticket(self) -> bool:
        """
        获取设置的是否使用 bili_ticket

        Returns:
            bool: 是否使用 bili_ticket. Defaults to True.
        """
        return self.__enable_bili_ticket

    def set_enable_bili_ticket(self, enable_bili_ticket: bool) -> None:
        """
        设置是否使用 bili_ticket

        Args:
            enable_bili_ticket (bool): 是否使用 bili_ticket.
        """
        self.__enable_bili_ticket = enable_bili_ticket

    def get_all(self) -> dict:
        """
        获取目前所有的设置项

        不可用于 `wbi_retry_times` `enable_auto_buvid` `enable_bili_ticket`

        Returns:
            dict: 所有的设置项
        """
        return self.__settings


request_settings = RequestSettings()
"请求参数设置"
request_settings.__doc__ = "请求参数设置"

DEFAULT_SETTINGS = ["proxy", "timeout", "verify_ssl", "trust_env"]


@dataclass
class BiliAPIResponse:
    """
    响应对象类。

    Attributes:
        code    (int)  : 响应码
        headers (dict) : 响应头
        cookies (dict) : 当前状态的 cookies
        raw     (bytes): 响应数据
        url     (str)  : 当前 url
    """

    code: int
    headers: dict
    cookies: dict
    raw: bytes
    url: str

    def utf8_text(self) -> str:
        """
        转为 utf8 文字

        Returns:
            str: utf8 文字
        """
        return self.raw.decode("utf-8")

    def json(self) -> object:
        """
        解析 json

        Returns:
            object: 解析后的 json
        """
        return json.loads(self.utf8_text())


class BiliWsMsgType(Enum):
    """
    WebSocket 状态枚举

    - CONTINUATION: 延续
    - TEXT: 文字
    - BINARY: 字节
    - PING: ping
    - PONG: pong
    - CLOSE: 关闭

    - CLOSING: 正在关闭
    - CLOSED: 已关闭
    """

    CONTINUATION = 0x0
    TEXT = 0x1
    BINARY = 0x2
    PING = 0x9
    PONG = 0xA
    CLOSE = 0x8
    CLOSING = 0x100
    CLOSED = 0x101


@dataclass
class BiliAPIFile:
    """
    上传文件类。

    Attributes:
        path      (str): 文件地址
        mime_type (str): 文件类型
    """

    path: str
    mime_type: str


class BiliAPIClient(ABC):
    '''
    请求客户端抽象类。通过对第三方模块请求客户端的封装令模块可对其进行调用。

    ``` python
    class BiliAPIClient(ABC):
        """
        请求客户端抽象类。通过对第三方模块请求客户端的封装令模块可对其进行调用。
        """

        @abstractmethod
        def __init__(
            self,
            proxy: str = "",
            timeout: float = 0.0,
            verify_ssl: bool = True,
            trust_env: bool = True,
            session: Optional[object] = None,
        ) -> None:
            """
            Args:
                proxy (str, optional): 代理地址. Defaults to "".
                timeout (float, optional): 请求超时时间. Defaults to 0.0.
                verify_ssl (bool, optional): 是否验证 SSL. Defaults to True.
                trust_env (bool, optional): `trust_env`. Defaults to True.
                session (object, optional): 会话对象. Defaults to None.

            Note: 仅当用户只提供 `session` 参数且用户中途未调用 `set_xxx` 函数才使用用户提供的 `session`。
            """
            raise NotImplementedError

        @abstractmethod
        def get_wrapped_session(self) -> object:
            """
            获取封装的第三方会话对象

            Returns:
                object: 第三方会话对象
            """
            raise NotImplementedError

        @abstractmethod
        def set_timeout(self, timeout: float = 0.0) -> None:
            """
            设置请求超时时间

            Args:
                timeout (float, optional): 请求超时时间. Defaults to 0.0.
            """
            raise NotImplementedError

        @abstractmethod
        def set_proxy(self, proxy: str = "") -> None:
            """
            设置代理地址

            Args:
                proxy (str, optional): 代理地址. Defaults to "".
            """
            raise NotImplementedError

        @abstractmethod
        def set_verify_ssl(self, verify_ssl: bool = True) -> None:
            """
            设置是否验证 SSL

            Args:
                verify_ssl (bool, optional): 是否验证 SSL. Defaults to True.
            """
            raise NotImplementedError

        @abstractmethod
        def set_trust_env(self, trust_env: bool = True) -> None:
            """
            设置 `trust_env`

            Args:
                trust_env (bool, optional): `trust_env`. Defaults to True.
            """
            raise NotImplementedError

        @abstractmethod
        async def request(
            self,
            method: str = "",
            url: str = "",
            params: dict = {},
            data: Union[dict, str, bytes] = {},
            files: Dict[str, BiliAPIFile] = {},
            headers: dict = {},
            cookies: dict = {},
            allow_redirects: bool = True,
        ) -> BiliAPIResponse:
            """
            进行 HTTP 请求

            Args:
                method (str, optional): 请求方法. Defaults to "".
                url (str, optional): 请求地址. Defaults to "".
                params (dict, optional): 请求参数. Defaults to {}.
                data (Union[dict, str, bytes], optional): 请求数据. Defaults to {}.
                files (Dict[str, BiliAPIFile], optional): 请求文件. Defaults to {}.
                headers (dict, optional): 请求头. Defaults to {}.
                cookies (dict, optional): 请求 Cookies. Defaults to {}.
                allow_redirects (bool, optional): 是否允许重定向. Defaults to True.

            Returns:
                BiliAPIResponse: 响应对象

            Note: 无需实现 data 为 str 且 files 不为空的情况。
            """
            raise NotImplementedError

        @abstractmethod
        async def download_create(
            self,
            url: str = "",
            headers: dict = {},
        ) -> int:
            """
            开始下载文件

            Args:
                url     (str, optional) : 请求地址. Defaults to "".
                headers (dict, optional): 请求头. Defaults to {}.

            Returns:
                int: 下载编号，用于后续操作。
            """
            raise NotImplementedError

        @abstractmethod
        async def download_chunk(self, cnt: int) -> bytes:
            """
            下载部分文件

            Args:
                cnt    (int): 下载编号

            Returns:
                bytes: 字节
            """
            raise NotImplementedError

        @abstractmethod
        def download_content_length(self, cnt: int) -> int:
            """
            获取下载总字节数

            Args:
                cnt    (int): 下载编号

            Returns:
                int: 下载总字节数
            """
            raise NotImplementedError

        @abstractmethod
        async def ws_create(
            self, url: str = "", params: dict = {}, headers: dict = {}
        ) -> int:
            """
            创建 WebSocket 连接

            Args:
                url (str, optional): WebSocket 地址. Defaults to "".
                params (dict, optional): WebSocket 参数. Defaults to {}.
                headers (dict, optional): WebSocket 头. Defaults to {}.

            Returns:
                int: WebSocket 连接编号，用于后续操作。
            """
            raise NotImplementedError

        @abstractmethod
        async def ws_send(self, cnt: int, data: bytes) -> None:
            """
            发送 WebSocket 数据

            Args:
                cnt (int): WebSocket 连接编号
                data (bytes): WebSocket 数据
            """
            raise NotImplementedError

        @abstractmethod
        async def ws_recv(self, cnt: int) -> Tuple[bytes, BiliWsMsgType]:
            """
            接受 WebSocket 数据

            Args:
                cnt (int): WebSocket 连接编号

            Returns:
                Tuple[bytes, BiliWsMsgType]: WebSocket 数据和状态

            Note: 建议实现此函数时支持其他线程关闭不阻塞，除基础状态同时实现 CLOSING, CLOSED。
            """
            raise NotImplementedError

        @abstractmethod
        async def ws_close(self, cnt: int) -> None:
            """
            关闭 WebSocket 连接

            Args:
                cnt (int): WebSocket 连接编号
            """
            raise NotImplementedError

        @abstractmethod
        async def close(self):
            """
            关闭请求客户端，即关闭封装的第三方会话对象
            """
            raise NotImplementedError
    ```
    '''

    @abstractmethod
    def __init__(
        self,
        proxy: str = "",
        timeout: float = 0.0,
        verify_ssl: bool = True,
        trust_env: bool = True,
        session: Optional[object] = None,
    ) -> None:
        """
        Args:
            proxy (str, optional): 代理地址. Defaults to "".
            timeout (float, optional): 请求超时时间. Defaults to 0.0.
            verify_ssl (bool, optional): 是否验证 SSL. Defaults to True.
            trust_env (bool, optional): `trust_env`. Defaults to True.
            session (object, optional): 会话对象. Defaults to None.

        Note: 仅当用户只提供 `session` 参数且用户中途未调用 `set_xxx` 函数才使用用户提供的 `session`。
        """
        raise NotImplementedError

    @abstractmethod
    def get_wrapped_session(self) -> object:
        """
        获取封装的第三方会话对象

        Returns:
            object: 第三方会话对象
        """
        raise NotImplementedError

    @abstractmethod
    def set_timeout(self, timeout: float = 0.0) -> None:
        """
        设置请求超时时间

        Args:
            timeout (float, optional): 请求超时时间. Defaults to 0.0.
        """
        raise NotImplementedError

    @abstractmethod
    def set_proxy(self, proxy: str = "") -> None:
        """
        设置代理地址

        Args:
            proxy (str, optional): 代理地址. Defaults to "".
        """
        raise NotImplementedError

    @abstractmethod
    def set_verify_ssl(self, verify_ssl: bool = True) -> None:
        """
        设置是否验证 SSL

        Args:
            verify_ssl (bool, optional): 是否验证 SSL. Defaults to True.
        """
        raise NotImplementedError

    @abstractmethod
    def set_trust_env(self, trust_env: bool = True) -> None:
        """
        设置 `trust_env`

        Args:
            trust_env (bool, optional): `trust_env`. Defaults to True.
        """
        raise NotImplementedError

    @abstractmethod
    async def request(
        self,
        method: str = "",
        url: str = "",
        params: dict = {},
        data: Union[dict, str, bytes] = {},
        files: Dict[str, BiliAPIFile] = {},
        headers: dict = {},
        cookies: dict = {},
        allow_redirects: bool = True,
    ) -> BiliAPIResponse:
        """
        进行 HTTP 请求

        Args:
            method (str, optional): 请求方法. Defaults to "".
            url (str, optional): 请求地址. Defaults to "".
            params (dict, optional): 请求参数. Defaults to {}.
            data (Union[dict, str, bytes], optional): 请求数据. Defaults to {}.
            files (Dict[str, BiliAPIFile], optional): 请求文件. Defaults to {}.
            headers (dict, optional): 请求头. Defaults to {}.
            cookies (dict, optional): 请求 Cookies. Defaults to {}.
            allow_redirects (bool, optional): 是否允许重定向. Defaults to True.

        Returns:
            BiliAPIResponse: 响应对象

        Note: 无需实现 data 为 str 且 files 不为空的情况。
        """
        raise NotImplementedError

    @abstractmethod
    async def download_create(
        self,
        url: str = "",
        headers: dict = {},
    ) -> int:
        """
        开始下载文件

        Args:
            url     (str, optional) : 请求地址. Defaults to "".
            headers (dict, optional): 请求头. Defaults to {}.

        Returns:
            int: 下载编号，用于后续操作。
        """
        raise NotImplementedError

    @abstractmethod
    async def download_chunk(self, cnt: int) -> bytes:
        """
        下载部分文件

        Args:
            cnt    (int): 下载编号

        Returns:
            bytes: 字节
        """
        raise NotImplementedError

    @abstractmethod
    def download_content_length(self, cnt: int) -> int:
        """
        获取下载总字节数

        Args:
            cnt    (int): 下载编号

        Returns:
            int: 下载总字节数
        """
        raise NotImplementedError

    @abstractmethod
    async def ws_create(
        self, url: str = "", params: dict = {}, headers: dict = {}
    ) -> int:
        """
        创建 WebSocket 连接

        Args:
            url (str, optional): WebSocket 地址. Defaults to "".
            params (dict, optional): WebSocket 参数. Defaults to {}.
            headers (dict, optional): WebSocket 头. Defaults to {}.

        Returns:
            int: WebSocket 连接编号，用于后续操作。
        """
        raise NotImplementedError

    @abstractmethod
    async def ws_send(self, cnt: int, data: bytes) -> None:
        """
        发送 WebSocket 数据

        Args:
            cnt (int): WebSocket 连接编号
            data (bytes): WebSocket 数据
        """
        raise NotImplementedError

    @abstractmethod
    async def ws_recv(self, cnt: int) -> Tuple[bytes, BiliWsMsgType]:
        """
        接受 WebSocket 数据

        Args:
            cnt (int): WebSocket 连接编号

        Returns:
            Tuple[bytes, BiliWsMsgType]: WebSocket 数据和状态

        Note: 建议实现此函数时支持其他线程关闭不阻塞，除基础状态同时实现 CLOSING, CLOSED。
        """
        raise NotImplementedError

    @abstractmethod
    async def ws_close(self, cnt: int) -> None:
        """
        关闭 WebSocket 连接

        Args:
            cnt (int): WebSocket 连接编号
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        """
        关闭请求客户端，即关闭封装的第三方会话对象
        """
        raise NotImplementedError


def register_client(name: str, cls: type, settings: dict = {}) -> None:
    """
    注册请求客户端并切换，可用于用户自定义请求客户端。

    Args:
        name     (str): 请求客户端类型名称，用户自定义命名。
        cls      (type): 基于 BiliAPIClient 重写后的请求客户端类。
        settings (dict): 请求客户端在基础设置外的其他设置，键为设置名称，值为设置默认值。Defaults to {}.
    """
    global sessions, session_pool
    raise_for_statement(
        issubclass(cls, BiliAPIClient), "传入的类型需要继承 BiliAPIClient"
    )
    sessions[name] = cls
    session_pool[name] = {}
    select_client(name)
    for key, value in settings.items():
        request_settings.set(key, value)
    client_settings[name] = DEFAULT_SETTINGS.copy()
    client_settings[name] += list(settings.keys())


def unregister_client(name: str) -> None:
    """
    取消注册请求客户端，可用于用户自定义请求客户端。

    Args:
        name (str): 请求客户端类型名称，用户自定义命名。
    """
    global sessions, session_pool
    try:
        sessions.pop(name)
        session_pool.pop(name)
    except KeyError:
        raise ArgsException("未找到指定请求客户端。")


def select_client(name: str) -> None:
    """
    选择模块使用的注册过的请求客户端，可用于用户自定义请求客户端。

    Args:
        name (str): 请求客户端类型名称，用户自定义命名。
    """
    if not sessions.get(name):
        raise ArgsException(f"未注册过 {name}。")
    global selected_client
    selected_client = name


def get_selected_client() -> Tuple[str, Type[BiliAPIClient]]:
    """
    获取用户选择的请求客户端名称和对应的类

    Returns:
        Tuple[str, Type[BiliAPIClient]]: 第 0 项为客户端名称，第 1 项为对应的类
    """
    if selected_client == "":
        raise ArgsException(
            "尚未安装第三方请求库或未注册自定义第三方请求库。\n$ pip3 install (curl_cffi|httpx|aiohttp)"
        )
    return selected_client, sessions[selected_client]


def get_available_settings() -> List[str]:
    """
    获取当前支持的设置项

    Returns:
        List[str]: 支持的设置项名称
    """
    if selected_client == "":
        raise ArgsException(
            "尚未安装第三方请求库或未注册自定义第三方请求库。\n$ pip3 install (curl_cffi|httpx|aiohttp)"
        )
    return client_settings[selected_client]


def get_registered_clients() -> Dict[str, Type[BiliAPIClient]]:
    """
    获取所有注册过的 BiliAPIClient

    Returns:
        Dict[str, Type[BiliAPIClient]]: 注册过的 BiliAPIClient
    """
    return sessions


def get_registered_available_settings() -> Dict[str, List[str]]:
    """
    获取所有注册过的 BiliAPIClient 所支持的设置项

    Returns:
        Dict[str, List[str]]: 所有注册过的 BiliAPIClient 所支持的设置项
    """
    return client_settings


def get_client() -> BiliAPIClient:
    """
    在当前事件循环下获取模块正在使用的请求客户端

    Returns:
        BiliAPIClient: 请求客户端
    """
    if selected_client == "":
        raise ArgsException(
            "尚未安装第三方请求库或未注册自定义第三方请求库。\n$ pip3 install (curl_cffi|httpx|aiohttp)"
        )
    global session_pool
    pool = session_pool.get(selected_client)
    if pool is None:
        raise ArgsException("未找到用户指定的请求客户端。")
    loop = asyncio.get_event_loop()
    session = pool.get(loop)
    if session is None:
        kwargs = {}
        for piece in client_settings[selected_client]:
            kwargs[piece] = request_settings.get(piece)
        session = sessions[selected_client](**kwargs)
        session_pool[selected_client][loop] = session
    return session


def get_session() -> object:
    """
    在当前事件循环下获取请求客户端的会话对象。

    Returns:
        object: 会话对象
    """
    return get_client().get_wrapped_session()


def set_session(session: object) -> None:
    """
    在当前事件循环下设置请求客户端的会话对象。

    Args:
        session (object): 会话对象
    """
    global session_pool
    pool = session_pool.get(selected_client)
    if not pool:
        raise ArgsException("未找到用户指定的请求客户端。")
    loop = asyncio.get_event_loop()
    session_pool[selected_client][loop] = sessions[selected_client](session=session)


@atexit.register
def __clean() -> None:
    """
    程序退出清理操作。
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        return

    async def __clean_task():
        for _, pool in session_pool.items():
            for _, client in pool.items():
                await client.close()

    if loop.is_closed():
        loop.run_until_complete(__clean_task())
    else:
        loop.create_task(__clean_task())


################################################## END Session Management ##################################################


################################################## BEGIN Credential ##################################################


class Credential:
    """
    凭据类，用于各种请求操作的验证。
    """

    def __init__(
        self,
        sessdata: Union[str, None] = None,
        bili_jct: Union[str, None] = None,
        buvid3: Union[str, None] = None,
        buvid4: Union[str, None] = None,
        dedeuserid: Union[str, None] = None,
        ac_time_value: Union[str, None] = None,
    ) -> None:
        """
        各字段获取方式查看：https://nemo2011.github.io/bilibili-api/#/get-credential.md

        Args:
            sessdata   (str | None, optional): 浏览器 Cookies 中的 SESSDATA 字段值. Defaults to None.

            bili_jct   (str | None, optional): 浏览器 Cookies 中的 bili_jct 字段值. Defaults to None.

            buvid3     (str | None, optional): 浏览器 Cookies 中的 BUVID3 字段值. Defaults to None.

            buvid4     (str | None, optional): 浏览器 Cookies 中的 BUVID4 字段值. Defaults to None.

            dedeuserid (str | None, optional): 浏览器 Cookies 中的 DedeUserID 字段值. Defaults to None.

            ac_time_value (str | None, optional): 浏览器 Cookies 中的 ac_time_value 字段值. Defaults to None.
        """
        self.sessdata = (
            None
            if sessdata is None
            else (
                sessdata if sessdata.find("%") != -1 else urllib.parse.quote(sessdata)
            )
        )
        self.bili_jct = bili_jct
        self.buvid3 = buvid3
        self.buvid4 = buvid4
        self.dedeuserid = dedeuserid
        self.ac_time_value = ac_time_value

    def get_cookies(self) -> dict:
        """
        获取请求 Cookies 字典

        Returns:
            dict: 请求 Cookies 字典
        """
        cookies = {
            "SESSDATA": self.sessdata if self.sessdata else "",
            "buvid3": self.buvid3 if self.buvid3 else "",
            "buvid4": self.buvid4 if self.buvid4 else "",
            "bili_jct": self.bili_jct if self.bili_jct else "",
            "ac_time_value": self.ac_time_value if self.ac_time_value else "",
        }
        if self.dedeuserid:
            cookies.update({"DedeUserID": self.dedeuserid})

        return cookies

    async def get_buvid_cookies(self) -> dict:
        """
        获取请求 Cookies 字典，自动补充 buvid 字段

        Returns:
            dict: 请求 Cookies 字典
        """
        cookies = {
            "SESSDATA": self.sessdata if self.sessdata else "",
            "buvid3": self.buvid3 if self.buvid3 else (await get_buvid())[0],
            "buvid4": self.buvid4 if self.buvid4 else (await get_buvid())[1],
            "bili_jct": self.bili_jct if self.bili_jct else "",
            "ac_time_value": self.ac_time_value if self.ac_time_value else "",
        }
        if self.dedeuserid:
            cookies.update({"DedeUserID": self.dedeuserid})

        return cookies

    def has_dedeuserid(self) -> bool:
        """
        是否提供 dedeuserid。

        Returns:
            bool: 是否提供 dedeuserid。
        """
        return self.dedeuserid is not None and self.dedeuserid != ""

    def has_sessdata(self) -> bool:
        """
        是否提供 sessdata。

        Returns:
            bool: 是否提供 sessdata。
        """
        return self.sessdata is not None and self.sessdata != ""

    def has_bili_jct(self) -> bool:
        """
        是否提供 bili_jct。

        Returns:
            bool: 是否提供 bili_jct。
        """
        return self.bili_jct is not None and self.bili_jct != ""

    def has_buvid3(self) -> bool:
        """
        是否提供 buvid3

        Returns:
            bool: 是否提供 buvid3
        """
        return self.buvid3 is not None and self.buvid3 != ""

    def has_buvid4(self) -> bool:
        """
        是否提供 buvid4

        Returns:
            bool: 是否提供 buvid4
        """
        return self.buvid4 is not None and self.buvid4 != ""

    def has_ac_time_value(self) -> bool:
        """
        是否提供 ac_time_value

        Returns:
            bool: 是否提供 ac_time_value
        """
        return self.ac_time_value is not None and self.ac_time_value != ""

    def raise_for_no_sessdata(self):
        """
        没有提供 sessdata 则抛出异常。
        """
        if not self.has_sessdata():
            raise CredentialNoSessdataException()

    def raise_for_no_bili_jct(self):
        """
        没有提供 bili_jct 则抛出异常。
        """
        if not self.has_bili_jct():
            raise CredentialNoBiliJctException()

    def raise_for_no_buvid3(self):
        """
        没有提供 buvid3 时抛出异常。
        """
        if not self.has_buvid3():
            raise CredentialNoBuvid3Exception()

    def raise_for_no_buvid4(self):
        """
        没有提供 buvid3 时抛出异常。
        """
        if not self.has_buvid4():
            raise CredentialNoBuvid4Exception()

    def raise_for_no_dedeuserid(self):
        """
        没有提供 DedeUserID 时抛出异常。
        """
        if not self.has_dedeuserid():
            raise CredentialNoDedeUserIDException()

    def raise_for_no_ac_time_value(self):
        """
        没有提供 ac_time_value 时抛出异常。
        """
        if not self.has_ac_time_value():
            raise CredentialNoAcTimeValueException()

    async def check_valid(self):
        """
        检查 cookies 是否有效

        Returns:
            bool: cookies 是否有效
        """
        return await _check_valid(self)

    async def check_refresh(self) -> bool:
        """
        检查是否需要刷新 cookies

        Returns:
            bool: cookies 是否需要刷新
        """
        return await _check_cookies(self)

    async def refresh(self) -> None:
        """
        刷新 cookies
        """
        new_cred: Credential = await _refresh_cookies(self)
        self.sessdata = new_cred.sessdata
        self.bili_jct = new_cred.bili_jct
        self.dedeuserid = new_cred.dedeuserid
        self.ac_time_value = new_cred.ac_time_value

    @staticmethod
    def from_cookies(cookies: dict = {}) -> "Credential":
        """
        从 cookies 新建 Credential

        Args:
            cookies (dict, optional): Cookies. Defaults to {}.

        Returns:
            Credential: 凭据类
        """
        c = Credential()
        c.sessdata = cookies.get("SESSDATA")
        c.bili_jct = cookies.get("bili_jct")
        c.buvid3 = cookies.get("buvid3")
        c.buvid4 = cookies.get("buvid4")
        c.dedeuserid = cookies.get("DedeUserID")
        c.ac_time_value = cookies.get("ac_time_value")
        return c

    def __str__(self):
        return f"SESSDATA: {self.sessdata}; bili_jct: {self.bili_jct}; buvid3: {self.buvid3}; buvid4: {self.buvid4}; DedeUserID: {self.dedeuserid}; ac_time_value: {self.ac_time_value}"


"""
Cookies 刷新相关

感谢 bilibili-API-collect 提供的刷新 Cookies 的思路

https://socialsisteryi.github.io/bilibili-API-collect/docs/login/cookie_refresh.html
"""


async def _check_valid(credential: Credential) -> bool:
    api = API["info"]["valid"]
    return (await Api(**api, credential=credential).result)["isLogin"]


async def _check_cookies(credential: Credential) -> bool:
    api = API["info"]["check_cookies"]
    return (await Api(**api, credential=credential).result)["refresh"]


def _getCorrespondPath() -> str:
    key = RSA.importKey(
        """\
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDLgd2OAkcGVtoE3ThUREbio0Eg
Uc/prcajMKXvkCKFCWhJYJcLkcM2DKKcSeFpD/j6Boy538YXnR6VhcuUJOhH2x71
nzPjfdTcqMz7djHum0qSZA0AyCBDABUqCrfNgCiJ00Ra7GmRj+YCK1NJEuewlb40
JNrRuoEUXpabUzGB8QIDAQAB
-----END PUBLIC KEY-----"""
    )
    ts = round(time.time() * 1000)
    cipher = PKCS1_OAEP.new(key, SHA256)
    encrypted = cipher.encrypt(f"refresh_{ts}".encode())
    return binascii.b2a_hex(encrypted).decode()


async def _get_refresh_csrf(credential: Credential) -> str:
    correspond_path = _getCorrespondPath()
    api = API["operate"]["get_refresh_csrf"]
    cookies = credential.get_cookies()
    cookies["buvid3"] = str(uuid.uuid1())
    client = get_client()
    resp = await client.request(
        method="GET",
        url=api["url"].replace("{correspondPath}", correspond_path),
        cookies=cookies,
        headers=HEADERS.copy(),
    )
    if resp.code == 404:
        raise CookiesRefreshException("correspondPath 过期或错误。")
    elif resp.code == 200:
        text = resp.utf8_text()
        refresh_csrf = re.findall('<div id="1-name">(.+?)</div>', text)[0]
        return refresh_csrf
    elif resp.code != 200:
        raise CookiesRefreshException("获取刷新 Cookies 的 csrf 失败。")


async def _refresh_cookies(credential: Credential) -> Credential:
    api = API["operate"]["refresh_cookies"]
    credential.raise_for_no_bili_jct()
    credential.raise_for_no_ac_time_value()
    refresh_csrf = await _get_refresh_csrf(credential)
    data = {
        "csrf": credential.bili_jct,
        "refresh_csrf": refresh_csrf,
        "refresh_token": credential.ac_time_value,
        "source": "main_web",
    }
    cookies = credential.get_cookies()
    cookies["buvid3"] = str(uuid.uuid1())
    client = get_client()
    resp = await client.request(
        method="POST",
        url=api["url"],
        cookies=cookies,
        data=data,
        headers=HEADERS.copy(),
    )
    if resp.code != 200 or resp.json()["code"] != 0:
        raise CookiesRefreshException("刷新 Cookies 失败")
    new_credential = Credential(
        sessdata=resp.cookies["SESSDATA"],
        bili_jct=resp.cookies["bili_jct"],
        dedeuserid=resp.cookies["DedeUserID"],
        ac_time_value=resp.json()["data"]["refresh_token"],
    )
    await _confirm_refresh(credential, new_credential)
    return new_credential


async def _confirm_refresh(
    old_credential: Credential, new_credential: Credential
) -> None:
    api = API["operate"]["confirm_refresh"]
    data = {
        "csrf": new_credential.bili_jct,
        "refresh_token": old_credential.ac_time_value,
    }
    await Api(**api, credential=new_credential).update_data(**data).result


################################################## END Credential ##################################################


################################################## BEGIN Anti-Spider ##################################################


OE = [
    46,
    47,
    18,
    2,
    53,
    8,
    23,
    32,
    15,
    50,
    10,
    31,
    58,
    3,
    45,
    35,
    27,
    43,
    5,
    49,
    33,
    9,
    42,
    19,
    29,
    28,
    14,
    39,
    12,
    38,
    41,
    13,
    37,
    48,
    7,
    16,
    24,
    55,
    40,
    61,
    26,
    17,
    0,
    1,
    60,
    51,
    30,
    4,
    22,
    25,
    54,
    21,
    56,
    59,
    6,
    63,
    57,
    62,
    11,
    36,
    20,
    34,
    44,
    52,
]
APPKEY = "4409e2ce8ffd12b8"
APPSEC = "59b43e04ad6965f34319062b478f83dd"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Referer": "https://www.bilibili.com",
}
API = get_api("credential")


async def _get_spi_buvid() -> dict:
    api = API["info"]["spi"]
    client = get_client()
    return (
        await client.request(method="GET", url=api["url"], headers=HEADERS.copy())
    ).json()["data"]


"""
思路来源：https://github.com/SocialSisterYi/bilibili-API-collect/issues/933
"""


async def _active_buvid(buvid3: str, buvid4: str) -> dict:
    MOD = 1 << 64

    def get_time_milli() -> int:
        return int(time.time() * 1000)

    def rotate_left(x: int, k: int) -> int:
        bin_str = bin(x)[2:].rjust(64, "0")
        return int(bin_str[k:] + bin_str[:k], base=2)

    def gen_uuid_infoc() -> str:
        t = get_time_milli() % 100000
        mp = list("123456789ABCDEF") + ["10"]
        pck = [8, 4, 4, 4, 12]
        gen_part = lambda x: "".join([random.choice(mp) for _ in range(x)])
        return "-".join([gen_part(l) for l in pck]) + str(t).ljust(5, "0") + "infoc"

    def gen_b_lsid() -> str:
        ret = ""
        for _ in range(8):
            ret += hex(random.randint(0, 15))[2:].upper()
        ret = f"{ret}_{hex(get_time_milli())[2:].upper()}"
        return ret

    def gen_buvid_fp(key: str, seed: int):
        source = io.BytesIO(bytes(key, "ascii"))
        m = murmur3_x64_128(source, seed)
        return "{}{}".format(hex(m & (MOD - 1))[2:], hex(m >> 64)[2:])

    def murmur3_x64_128(source: io.BufferedIOBase, seed: int) -> str:
        C1 = 0x87C3_7B91_1142_53D5
        C2 = 0x4CF5_AD43_2745_937F
        C3 = 0x52DC_E729
        C4 = 0x3849_5AB5
        R1, R2, R3, M = 27, 31, 33, 5
        h1, h2 = seed, seed
        processed = 0
        while 1:
            read = source.read(16)
            processed += len(read)
            if len(read) == 16:
                k1 = struct.unpack("<q", read[:8])[0]
                k2 = struct.unpack("<q", read[8:])[0]
                h1 ^= rotate_left(k1 * C1 % MOD, R2) * C2 % MOD
                h1 = ((rotate_left(h1, R1) + h2) * M + C3) % MOD
                h2 ^= rotate_left(k2 * C2 % MOD, R3) * C1 % MOD
                h2 = ((rotate_left(h2, R2) + h1) * M + C4) % MOD
            elif len(read) == 0:
                h1 ^= processed
                h2 ^= processed
                h1 = (h1 + h2) % MOD
                h2 = (h2 + h1) % MOD
                h1 = fmix64(h1)
                h2 = fmix64(h2)
                h1 = (h1 + h2) % MOD
                h2 = (h2 + h1) % MOD
                return (h2 << 64) | h1
            else:
                k1 = 0
                k2 = 0
                if len(read) >= 15:
                    k2 ^= int(read[14]) << 48
                if len(read) >= 14:
                    k2 ^= int(read[13]) << 40
                if len(read) >= 13:
                    k2 ^= int(read[12]) << 32
                if len(read) >= 12:
                    k2 ^= int(read[11]) << 24
                if len(read) >= 11:
                    k2 ^= int(read[10]) << 16
                if len(read) >= 10:
                    k2 ^= int(read[9]) << 8
                if len(read) >= 9:
                    k2 ^= int(read[8])
                    k2 = rotate_left(k2 * C2 % MOD, R3) * C1 % MOD
                    h2 ^= k2
                if len(read) >= 8:
                    k1 ^= int(read[7]) << 56
                if len(read) >= 7:
                    k1 ^= int(read[6]) << 48
                if len(read) >= 6:
                    k1 ^= int(read[5]) << 40
                if len(read) >= 5:
                    k1 ^= int(read[4]) << 32
                if len(read) >= 4:
                    k1 ^= int(read[3]) << 24
                if len(read) >= 3:
                    k1 ^= int(read[2]) << 16
                if len(read) >= 2:
                    k1 ^= int(read[1]) << 8
                if len(read) >= 1:
                    k1 ^= int(read[0])
                k1 = rotate_left(k1 * C1 % MOD, R2) * C2 % MOD
                h1 ^= k1

    def fmix64(k: int) -> int:
        C1 = 0xFF51_AFD7_ED55_8CCD
        C2 = 0xC4CE_B9FE_1A85_EC53
        R = 33
        tmp = k
        tmp ^= tmp >> R
        tmp = tmp * C1 % MOD
        tmp ^= tmp >> R
        tmp = tmp * C2 % MOD
        tmp ^= tmp >> R
        return tmp

    def get_payload(uuid: str) -> str:
        content = {
            "3064": 1,
            "5062": get_time_milli(),
            "03bf": "https%3A%2F%2Fwww.bilibili.com%2F",
            "39c8": "333.788.fp.risk",
            "34f1": "",
            "d402": "",
            "654a": "",
            "6e7c": "839x959",
            "3c43": {
                "2673": 0,
                "5766": 24,
                "6527": 0,
                "7003": 1,
                "807e": 1,
                "b8ce": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
                "641c": 0,
                "07a4": "en-US",
                "1c57": "not available",
                "0bd0": 8,
                "748e": [900, 1440],
                "d61f": [875, 1440],
                "fc9d": -480,
                "6aa9": "Asia/Shanghai",
                "75b8": 1,
                "3b21": 1,
                "8a1c": 0,
                "d52f": "not available",
                "adca": "MacIntel",
                "80c9": [
                    [
                        "PDF Viewer",
                        "Portable Document Format",
                        [["application/pdf", "pdf"], ["text/pdf", "pdf"]],
                    ],
                    [
                        "Chrome PDF Viewer",
                        "Portable Document Format",
                        [["application/pdf", "pdf"], ["text/pdf", "pdf"]],
                    ],
                    [
                        "Chromium PDF Viewer",
                        "Portable Document Format",
                        [["application/pdf", "pdf"], ["text/pdf", "pdf"]],
                    ],
                    [
                        "Microsoft Edge PDF Viewer",
                        "Portable Document Format",
                        [["application/pdf", "pdf"], ["text/pdf", "pdf"]],
                    ],
                    [
                        "WebKit built-in PDF",
                        "Portable Document Format",
                        [["application/pdf", "pdf"], ["text/pdf", "pdf"]],
                    ],
                ],
                "13ab": "0dAAAAAASUVORK5CYII=",
                "bfe9": "QgAAEIQAACEIAABCCQN4FXANGq7S8KTZayAAAAAElFTkSuQmCC",
                "a3c1": [
                    "extensions:ANGLE_instanced_arrays;EXT_blend_minmax;EXT_color_buffer_half_float;EXT_float_blend;EXT_frag_depth;EXT_shader_texture_lod;EXT_texture_compression_bptc;EXT_texture_compression_rgtc;EXT_texture_filter_anisotropic;EXT_sRGB;KHR_parallel_shader_compile;OES_element_index_uint;OES_fbo_render_mipmap;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_color_buffer_float;WEBGL_compressed_texture_astc;WEBGL_compressed_texture_etc;WEBGL_compressed_texture_etc1;WEBGL_compressed_texture_pvrtc;WEBKIT_WEBGL_compressed_texture_pvrtc;WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBGL_multi_draw",
                    "webgl aliased line width range:[1, 1]",
                    "webgl aliased point size range:[1, 511]",
                    "webgl alpha bits:8",
                    "webgl antialiasing:yes",
                    "webgl blue bits:8",
                    "webgl depth bits:24",
                    "webgl green bits:8",
                    "webgl max anisotropy:16",
                    "webgl max combined texture image units:32",
                    "webgl max cube map texture size:16384",
                    "webgl max fragment uniform vectors:1024",
                    "webgl max render buffer size:16384",
                    "webgl max texture image units:16",
                    "webgl max texture size:16384",
                    "webgl max varying vectors:30",
                    "webgl max vertex attribs:16",
                    "webgl max vertex texture image units:16",
                    "webgl max vertex uniform vectors:1024",
                    "webgl max viewport dims:[16384, 16384]",
                    "webgl red bits:8",
                    "webgl renderer:WebKit WebGL",
                    "webgl shading language version:WebGL GLSL ES 1.0 (1.0)",
                    "webgl stencil bits:0",
                    "webgl vendor:WebKit",
                    "webgl version:WebGL 1.0",
                    "webgl unmasked vendor:Apple Inc.",
                    "webgl unmasked renderer:Apple GPU",
                    "webgl vertex shader high float precision:23",
                    "webgl vertex shader high float precision rangeMin:127",
                    "webgl vertex shader high float precision rangeMax:127",
                    "webgl vertex shader medium float precision:23",
                    "webgl vertex shader medium float precision rangeMin:127",
                    "webgl vertex shader medium float precision rangeMax:127",
                    "webgl vertex shader low float precision:23",
                    "webgl vertex shader low float precision rangeMin:127",
                    "webgl vertex shader low float precision rangeMax:127",
                    "webgl fragment shader high float precision:23",
                    "webgl fragment shader high float precision rangeMin:127",
                    "webgl fragment shader high float precision rangeMax:127",
                    "webgl fragment shader medium float precision:23",
                    "webgl fragment shader medium float precision rangeMin:127",
                    "webgl fragment shader medium float precision rangeMax:127",
                    "webgl fragment shader low float precision:23",
                    "webgl fragment shader low float precision rangeMin:127",
                    "webgl fragment shader low float precision rangeMax:127",
                    "webgl vertex shader high int precision:0",
                    "webgl vertex shader high int precision rangeMin:31",
                    "webgl vertex shader high int precision rangeMax:30",
                    "webgl vertex shader medium int precision:0",
                    "webgl vertex shader medium int precision rangeMin:31",
                    "webgl vertex shader medium int precision rangeMax:30",
                    "webgl vertex shader low int precision:0",
                    "webgl vertex shader low int precision rangeMin:31",
                    "webgl vertex shader low int precision rangeMax:30",
                    "webgl fragment shader high int precision:0",
                    "webgl fragment shader high int precision rangeMin:31",
                    "webgl fragment shader high int precision rangeMax:30",
                    "webgl fragment shader medium int precision:0",
                    "webgl fragment shader medium int precision rangeMin:31",
                    "webgl fragment shader medium int precision rangeMax:30",
                    "webgl fragment shader low int precision:0",
                    "webgl fragment shader low int precision rangeMin:31",
                    "webgl fragment shader low int precision rangeMax:30",
                ],
                "6bc5": "Apple Inc.~Apple GPU",
                "ed31": 0,
                "72bd": 0,
                "097b": 0,
                "52cd": [0, 0, 0],
                "a658": [
                    "Andale Mono",
                    "Arial",
                    "Arial Black",
                    "Arial Hebrew",
                    "Arial Narrow",
                    "Arial Rounded MT Bold",
                    "Arial Unicode MS",
                    "Comic Sans MS",
                    "Courier",
                    "Courier New",
                    "Geneva",
                    "Georgia",
                    "Helvetica",
                    "Helvetica Neue",
                    "Impact",
                    "LUCIDA GRANDE",
                    "Microsoft Sans Serif",
                    "Monaco",
                    "Palatino",
                    "Tahoma",
                    "Times",
                    "Times New Roman",
                    "Trebuchet MS",
                    "Verdana",
                    "Wingdings",
                    "Wingdings 2",
                    "Wingdings 3",
                ],
                "d02f": "124.04345259929687",
            },
            "54ef": '{"in_new_ab":true,"ab_version":{"remove_back_version":"REMOVE","login_dialog_version":"V_PLAYER_PLAY_TOAST","open_recommend_blank":"SELF","storage_back_btn":"HIDE","call_pc_app":"FORBID","clean_version_old":"GO_NEW","optimize_fmp_version":"LOADED_METADATA","for_ai_home_version":"V_OTHER","bmg_fallback_version":"DEFAULT","ai_summary_version":"SHOW","weixin_popup_block":"ENABLE","rcmd_tab_version":"DISABLE","in_new_ab":true},"ab_split_num":{"remove_back_version":11,"login_dialog_version":43,"open_recommend_blank":90,"storage_back_btn":87,"call_pc_app":47,"clean_version_old":46,"optimize_fmp_version":28,"for_ai_home_version":38,"bmg_fallback_version":86,"ai_summary_version":466,"weixin_popup_block":45,"rcmd_tab_version":90,"in_new_ab":0},"pageVersion":"new_video","videoGoOldVersion":-1}',
            "8b94": "https%3A%2F%2Fwww.bilibili.com%2F",
            "df35": uuid,
            "07a4": "en-US",
            "5f45": None,
            "db46": 0,
        }
        return json.dumps(
            {"payload": json.dumps(content, separators=(",", ":"))},
            separators=(",", ":"),
        )

    api = API["operate"]["active"]
    client = get_client()
    uuid = gen_uuid_infoc()
    payload = get_payload(uuid)
    buvid_fp = gen_buvid_fp(payload, 31)
    headers = HEADERS.copy()
    headers["Content-Type"] = "application/json"
    resp = await client.request(
        method="POST",
        url=api["url"],
        data=payload,
        headers=headers,
        cookies={
            "buvid3": buvid3,
            "buvid4": buvid4,
            "buvid_fp": buvid_fp,
            "_uuid": uuid,
        },
    )
    data = resp.json()
    if data["code"] != 0:
        raise ExClimbWuzhiException(data["code"], data["msg"])


async def _get_nav(credential: Optional[Credential] = None) -> dict:
    credential = credential if credential else Credential()
    api = API["info"]["valid"]
    client = get_client()
    return (
        await client.request(
            method="GET",
            url=api["url"],
            headers=HEADERS.copy(),
            cookies=credential.get_cookies(),
        )
    ).json()["data"]


async def _get_mixin_key(credential: Optional[Credential] = None) -> str:
    data = await _get_nav(credential=credential)
    wbi_img: Dict[str, str] = data["wbi_img"]

    def split(key):
        return wbi_img.get(key).split("/")[-1].split(".")[0]

    ae = split("img_url") + split("sub_url")
    le = reduce(lambda s, i: s + (ae[i] if i < len(ae) else ""), OE, "")
    return le[:32]


def _enc_wbi(params: dict, mixin_key: str) -> dict:
    params.pop("w_rid", None)  # 重试时先把原有 w_rid 去除
    params["wts"] = int(time.time())
    # web_location 因为没被列入参数可能炸一些接口 比如 video.get_ai_conclusion
    # 但 video.get_download_url 的 web_location 不是这东西
    # 因此此处默认提供 1550101，具体哪些一些也不清楚。
    if not params.get("web_location"):
        params["web_location"] = 1550101
    Ae = urllib.parse.urlencode(sorted(params.items()))
    params["w_rid"] = hashlib.md5((Ae + mixin_key).encode(encoding="utf-8")).hexdigest()
    return params


def _enc_wbi2(params: dict) -> dict:
    dm_rand = "ABCDEFGHIJK"
    params.update(
        {
            "dm_img_list": "[]",  # 鼠标/键盘操作记录
            "dm_img_str": "".join(random.sample(dm_rand, 2)),
            "dm_cover_img_str": "".join(random.sample(dm_rand, 2)),
            "dm_img_inter": '{"ds":[],"wh":[0,0,0],"of":[0,0,0]}',
        }
    )
    return params


def _enc_sign(paramsordata: dict) -> dict:
    paramsordata["appkey"] = APPKEY
    paramsordata = dict(sorted(paramsordata.items()))
    paramsordata["sign"] = hashlib.md5(
        (urllib.parse.urlencode(paramsordata) + APPSEC).encode("utf-8")
    ).hexdigest()
    return paramsordata


"""
算法来源：https://github.com/SocialSisterYi/bilibili-API-collect/issues/903
"""


async def _get_bili_ticket(credential: Optional[Credential] = None) -> str:
    def hmac_sha256(key: str, message: str) -> str:
        key = key.encode("utf-8")
        message = message.encode("utf-8")
        hmac_obj = hmac.new(key, message, hashlib.sha256)
        return hmac_obj.digest().hex()

    credential = credential if credential else Credential()
    o = hmac_sha256("XgwSnGZ1p", f"ts{int(time.time())}")
    api = API["info"]["ticket"]
    params = {
        "key_id": "ec02",
        "hexsign": o,
        "context[ts]": f"{int(time.time())}",
        "csrf": "",
    }
    client = get_client()
    resp = await client.request(
        method="POST",
        url=api["url"],
        params=params,
        headers=HEADERS.copy(),
        cookies=credential.get_cookies(),
    )
    return resp.json()["data"]["ticket"]


################################################## END Anti-Spider ##################################################


################################################## BEGIN Api ##################################################


__buvid3 = ""
__buvid4 = ""
__bili_ticket = ""
__bili_ticket_expires = 0
__wbi_mixin_key = ""


def refresh_buvid() -> None:
    """
    刷新模块自动生成的 buvid3 和 buvid4
    """
    global __buvid3, __buvid4
    __buvid3 = ""
    __buvid4 = ""


def refresh_bili_ticket() -> None:
    """
    刷新 bili_ticket
    """
    global __bili_ticket, __bili_ticket_expires
    __bili_ticket = ""
    __bili_ticket_expires = 0


def recalculate_wbi() -> None:
    """
    重新计算 wbi 的参数
    """
    global __wbi_mixin_key
    __wbi_mixin_key = ""


async def get_buvid() -> Tuple[str, str]:
    """
    获取 buvid3 和 buvid4

    Returns:
        Tuple[str, str]: 第 0 项为 buvid3，第 1 项为 buvid4。
    """
    global __buvid3, __buvid4
    if __buvid3 == "" or __buvid4 == "":
        spi = await _get_spi_buvid()
        __buvid3 = spi["b_3"]
        __buvid4 = spi["b_4"]
        await _active_buvid(__buvid3, __buvid4)
        request_log.dispatch(
            "ANTI_SPIDER",
            "反爬虫",
            {"msg": f"激活 buvid3 / buvid4 成功: 3 [{__buvid3}] 4 [{__buvid4}]"},
        )
    return (__buvid3, __buvid4)


async def get_bili_ticket(credential: Optional[Credential] = None) -> Tuple[str, str]:
    """
    获取 bili_ticket

    Args:
        credential (Credential, optional): 凭据. Defaults to None.

    Returns:
        Tuple[str, str]: bili_ticket, bili_ticket_expires
    """
    global __bili_ticket, __bili_ticket_expires
    if time.time() > int(__bili_ticket_expires):
        refresh_bili_ticket()
    if __bili_ticket == "":
        __bili_ticket = await _get_bili_ticket(credential)
        __bili_ticket_expires = str(int(time.time()) + 3 * 86400)
        request_log.dispatch(
            "ANTI_SPIDER",
            "反爬虫",
            {"msg": f"获取 bili_ticket 成功: [{__bili_ticket}]"},
        )
    return __bili_ticket, __bili_ticket_expires


async def get_wbi_mixin_key(credential: Optional[Credential] = None) -> str:
    """
    获取 wbi mixin key

    Args:
        credential (Credential, optional): 凭据. Defaults to None.

    Returns:
        str: wbi mixin key
    """
    global __wbi_mixin_key
    if __wbi_mixin_key == "":
        __wbi_mixin_key = await _get_mixin_key(credential)
        request_log.dispatch(
            "ANTI_SPIDER",
            "反爬虫",
            {"msg": f"获取 wbi mixin key: [{__wbi_mixin_key}]"},
        )
    return __wbi_mixin_key


@dataclass
class Api:
    """
    用于请求的 Api 类

    Args:
        url (str): 请求地址

        method (str): 请求方法

        comment (str, optional): 注释. Defaults to "".

        wbi (bool, optional): 是否使用 wbi 鉴权. Defaults to False.

        wbi2 (bool, optional): 是否使用参数进一步的 wbi 鉴权. Defaults to False.

        verify (bool, optional): 是否验证凭据. Defaults to False.

        no_csrf (bool, optional): 是否不使用 csrf. Defaults to False.

        json_body (bool, optional): 是否使用 json 作为载荷. Defaults to False.

        ignore_code (bool, optional): 是否忽略返回值 code 的检验. Defaults to False.

        data (dict, optional): 请求载荷. Defaults to {}.

        params (dict, optional): 请求参数. Defaults to {}.

        credential (Credential, optional): 凭据. Defaults to Credential().
    """

    url: str
    method: str
    comment: str = ""
    wbi: bool = False
    wbi2: bool = False
    verify: bool = False
    no_csrf: bool = False
    json_body: bool = False
    ignore_code: bool = False
    sign: bool = False
    data: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    files: Dict[str, BiliAPIFile] = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    credential: Credential = field(default_factory=Credential)

    def __post_init__(self) -> None:
        self.method = self.method.upper()
        self.original_data = self.data.copy()
        self.original_params = self.params.copy()
        self.data = {k: "" for k in self.data.keys()}
        self.params = {k: "" for k in self.params.keys()}
        self.files = {k: "" for k in self.files.keys()}
        self.headers = {k: "" for k in self.headers.keys()}
        self.credential = self.credential if self.credential else Credential()

    def update_data(self, **kwargs) -> "Api":
        """
        更新 data

        Returns:
            Api: 返回自身
        """
        self.data = kwargs
        return self

    def update_params(self, **kwargs) -> "Api":
        """
        更新 params

        Returns:
            Api: 返回自身
        """
        self.params = kwargs
        return self

    def update_files(self, **kwargs) -> "Api":
        """
        更新 files

        Returns:
            Api: 返回自身
        """
        self.files = kwargs
        return self

    def update_headers(self, **kwargs) -> "Api":
        """
        更新 headers

        Returns:
            Api: 返回自身
        """
        self.headers = kwargs
        return self

    async def _prepare_request(self) -> dict:
        # 处理 bool
        new_params, new_data = {}, {}
        for key, value in self.params.items():
            if isinstance(value, bool):
                new_params[key] = int(value)
            elif value != None:
                new_params[key] = value
        for key, value in self.data.items():
            if isinstance(value, bool):
                new_params[key] = int(value)
            elif value != None:
                new_data[key] = value
        self.params, self.data = new_params, new_data
        # 如果接口需要 Credential 且未传入 sessdata 鉴权则报错
        if self.verify:
            self.credential.raise_for_no_sessdata()
        # 请求为非 GET 且 no_csrf 不为 True 时要求 bili_jct
        if self.method != "GET" and not self.no_csrf:
            self.credential.raise_for_no_bili_jct()
        # jsonp
        if self.params.get("jsonp") == "jsonp":
            self.params["callback"] = "callback"
        # 鼠标移动 wbi 风控 (这东西不放在前面工作不了)
        # (https://github.com/Nemo2011/bilibili-api/issues/595)
        if self.wbi2:
            self.params = _enc_wbi2(self.params)
        # 普遍存在的 wbi 鉴权
        if self.wbi:
            self.params = _enc_wbi(
                self.params, await get_wbi_mixin_key(self.credential)
            )
        # 自动添加 csrf
        if (
            not self.no_csrf
            and self.verify
            and self.method in ["POST", "DELETE", "PATCH"]
        ) and isinstance(self.data, dict):
            self.data["csrf"] = self.credential.bili_jct
            self.data["csrf_token"] = self.credential.bili_jct
        # 处理 cookies
        cookies = self.credential.get_cookies()
        if (cookies["buvid3"] == "" or cookies["buvid4"] == "") and request_settings.get_enable_auto_buvid():
            buvids = await get_buvid()
            cookies["buvid3"] = buvids[0]
            cookies["buvid4"] = buvids[1]
        cookies["opus-goback"] = "1"
        # bili_ticket
        if request_settings.get_enable_bili_ticket():
            cookies["bili_ticket"], cookies["bili_ticket_expires"] = await get_bili_ticket(self.credential)
        # APP 鉴权
        if self.sign:
            if self.method in ["POST", "DELETE", "PATCH"]:
                self.data = _enc_sign(self.data)
            else:
                self.params = _enc_sign(self.params)
        # 初步 params
        config = {
            "method": self.method,
            "url": self.url,
            "params": self.params,
            "data": self.data,
            "files": self.files,
            "cookies": cookies,
            "headers": HEADERS.copy() if len(self.headers) == 0 else self.headers,
        }
        # json_body
        if self.json_body:
            config["headers"]["Content-Type"] = "application/json"
            config["data"] = json.dumps(config["data"])

        return config

    def _process_response(
        self, resp: BiliAPIResponse, raw: bool = False
    ) -> Union[int, str, dict, None]:
        # 检查状态码
        if resp.code != 200:
            raise NetworkException(resp.code, resp.utf8_text())
        # 检查响应头 Content-Length
        content_length = resp.headers.get("content-length")
        if content_length and int(content_length) == 0:
            return None
        # 提取 json
        resp_text = resp.utf8_text()
        if "callback" in self.params:
            # JSONP 请求
            resp_data: dict = json.loads(
                re.match("^.*?({.*}).*$", resp_text, re.S).group(1)
            )
        else:
            # JSON
            resp_data: dict = json.loads(resp_text)
        if raw:
            return resp_data
        # 检查状态
        OK = resp_data.get("OK")
        if not self.ignore_code:
            if OK is None:
                code = resp_data.get("code")
                if code is None:
                    raise ResponseCodeException(
                        -1, "API 返回数据未含 code 字段", resp_data
                    )
                if code != 0:
                    msg = resp_data.get("msg")
                    if msg is None:
                        msg = resp_data.get("message")
                    if msg is None:
                        msg = "接口未返回错误信息"
                    raise ResponseCodeException(code, msg, resp_data)
            elif OK != 1:
                raise ResponseCodeException(-1, "API 返回数据 OK 不为 1", resp_data)
        # 自动提取 data / result 字段
        real_data = resp_data
        if OK is None:
            real_data = resp_data.get("data")
            if real_data is None:
                real_data = resp_data.get("result")
        return real_data

    async def _request(
        self, raw: bool = False, byte: bool = False
    ) -> Union[int, str, dict, bytes, None]:
        request_log.dispatch(
            "API_REQUEST",
            "Api 发起请求",
            self.__dict__,
        )
        config: dict = await self._prepare_request()
        client: BiliAPIClient = get_client()
        resp: BiliAPIResponse = await client.request(**config)
        ret: Union[int, str, dict, bytes, None]
        if byte:
            ret = resp.raw
        else:
            ret = self._process_response(resp=resp, raw=raw)
        request_log.dispatch(
            "API_RESPONSE",
            "Api 获得响应",
            {"result": ret},
        )
        return ret

    async def request(
        self, raw: bool = False, byte: bool = False
    ) -> Union[int, str, dict, bytes, None]:
        """
        向接口发送请求。

        Args:
            raw  (bool): 是否不提取 data 或 result 字段。 Defaults to False.
            byte (bool): 是否直接返回字节数据。 Defaults to False.

        Returns:
            接口未返回数据时，返回 None，否则返回该接口提供的 data 或 result 字段的数据。
        """
        times = request_settings.get_wbi_retry_times()
        loop = times
        while loop != 0:
            if loop != times:
                request_log.dispatch(
                    "ANTI_SPIDER",
                    "反爬虫",
                    {"msg": f"wbi 第 {times - loop} 次重试"},
                )
            loop -= 1
            try:
                return await self._request(raw=raw, byte=byte)
            except ResponseCodeException as e:
                # -403 时尝试重新获取 wbi_mixin_key 可能过期了
                if e.code == -403 and self.wbi:
                    recalculate_wbi()
                    continue
                # 不是 -403 错误直接报错
                raise e
            except Exception as e:
                raise e
        raise WbiRetryTimesExceedException()

    @property
    async def result(self) -> Union[int, str, dict, bytes, None]:
        """
        获取请求结果
        """
        return await self.request()


async def bili_simple_download(url: str, out: str, intro: str):
    """
    适用于下载 bilibili 链接的简易终端下载函数

    默认会携带 HEADERS 访问链接，避免 403

    用途举例：下载 video.get_download_url 返回结果中的链接

    Args:
        url   (str): 链接
        out   (str): 输出地址
        intro (str): 下载简述
    """
    dwn_id = await get_client().download_create(url, HEADERS)
    bts = 0
    tot = get_client().download_content_length(dwn_id)
    with open(out, "wb") as file:
        while True:
            bts += file.write(await get_client().download_chunk(dwn_id))
            print(f"{intro} - {out} [{bts} / {tot}]", end="\r")
            if bts == tot:
                break
    print()


################################################## END Api ##################################################
