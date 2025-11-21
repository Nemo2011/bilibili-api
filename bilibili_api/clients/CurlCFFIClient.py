"""
bilibili_api.clients.curl_cffi

CurlCFFIClient 实现
"""

import asyncio
from typing import AsyncGenerator, Dict, Optional, Tuple, Union

import curl_cffi  # pylint: disable=E0401
from curl_cffi import requests  # pylint: disable=E0401

from ..utils.network import (
    BiliAPIClient,
    BiliAPIFile,
    BiliAPIResponse,
    BiliWsMsgType,
)


class CurlCFFIClient(BiliAPIClient):
    """
    curl_cffi 模块请求客户端
    """

    def __init__(
        self,
        proxy: str = "",
        timeout: float = 0.0,
        verify_ssl: bool = True,
        trust_env: bool = True,
        impersonate: str = "",
        http2: bool = False,
        session: Optional[requests.AsyncSession] = None,
    ) -> None:
        """
        Args:
            proxy (str, optional): 代理地址. Defaults to "".
            timeout (float, optional): 请求超时时间. Defaults to 0.0.
            verify_ssl (bool, optional): 是否验证 SSL. Defaults to True.
            trust_env (bool, optional): `trust_env`. Defaults to True.
            impersonate (str, optional): 伪装的浏览器，可参考 curl_cffi 文档. Defaults to "".
            http2 (bool, optional): 是否使用 HTTP2. Defaults to False.
            session (object, optional): 会话对象. Defaults to None.

        Note: 仅当用户只提供 `session` 参数且用户中途未调用 `set_xxx` 函数才使用用户提供的 `session`。
        """
        if session:
            self.__session = session
        else:
            loop = asyncio.get_event_loop()
            self.__session = requests.AsyncSession(
                loop=loop,
                timeout=timeout,
                proxies={"all": proxy},
                verify=verify_ssl,
                trust_env=trust_env,
                impersonate=impersonate,
                http_version=(curl_cffi.CurlHttpVersion.V2_0 if http2 else None),
            )
        self.__ws: Dict[int, requests.AsyncWebSocket] = {}
        self.__ws_cnt: int = 0
        self.__ws_need_close: Dict[int, bool] = {}
        self.__ws_is_closed: Dict[int, bool] = {}
        self.__downloads: Dict[int, requests.Response] = {}
        self.__download_cnt: int = 0

        self.__ws_cnt_lock = asyncio.Lock()
        self.__down_cnt_lock = asyncio.Lock()

    def get_wrapped_session(self) -> requests.AsyncSession:
        return self.__session

    def set_proxy(self, proxy: str = "") -> None:
        self.__session.proxies = {"all": proxy}

    def set_timeout(self, timeout: float = 0.0) -> None:
        self.__session.timeout = timeout

    def set_verify_ssl(self, verify_ssl: bool = True) -> None:
        self.__session.verify = verify_ssl

    def set_trust_env(self, trust_env: bool = True) -> None:
        self.__session.trust_env = trust_env

    def set_impersonate(self, impersonate: str = "") -> None:
        """
        设置 curl_cffi 伪装的浏览器，可参考 curl_cffi 文档。

        Args:
            impersonate (str, optional): 伪装的浏览器. Defaults to "".
        """
        self.__session.impersonate = impersonate

    def set_http2(self, http2: bool = False) -> None:
        """
        设置是否使用 http2.

        Args:
            impersonate (str, optional): 是否使用 http2. Defaults to False.
        """
        self.__session.http_version = curl_cffi.CurlHttpVersion.V2_0 if http2 else None

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
        if headers.get("User-Agent") and self.__session.impersonate != "":
            headers.pop("User-Agent")
        if headers.get("user-agent") and self.__session.impersonate != "":
            headers.pop("user-agent")

        if files != {}:
            cnt = 1
            multipart = curl_cffi.CurlMime()
            for key, item in files.items():
                multipart.addpart(
                    name=key,
                    content_type=item.mime_type,
                    filename=f"{cnt}.{item.path.split('.')[1]}",
                    local_path=item.path,
                )
                cnt += 1
        else:
            multipart = None
        resp = await self.__session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            allow_redirects=allow_redirects,
            multipart=multipart,
        )
        if multipart:
            multipart.close()
        resp_header_items = resp.headers.multi_items()
        resp_headers = {}
        for item in resp_header_items:
            resp_headers[item[0]] = item[1]
        resp_cookies = {}
        for cookie in resp.cookies.jar:
            resp_cookies[cookie.name] = cookie.value
        bili_api_resp = BiliAPIResponse(
            code=resp.status_code,
            headers=resp_headers,
            cookies=resp_cookies,
            raw=resp.content,
            url=resp.url,
        )

        return bili_api_resp

    async def download_create(
        self,
        url: str = "",
        headers: dict = {},
    ) -> int:
        if headers.get("User-Agent") and self.__session.impersonate != "":
            headers.pop("User-Agent")
        if headers.get("user-agent") and self.__session.impersonate != "":
            headers.pop("user-agent")
        await self.__down_cnt_lock.acquire()
        self.__download_cnt += 1
        cnt = self.__download_cnt
        self.__down_cnt_lock.release()
        self.__downloads[cnt] = await self.__session.get(
            url=url, headers=headers, stream=True
        )
        return cnt

    async def download_chunk(self, cnt: int) -> bytes:
        resp = self.__downloads[cnt]
        data = await anext(resp.aiter_content())
        return data

    def download_content_length(self, cnt: int) -> int:
        resp = self.__downloads[cnt]
        return int(resp.headers.get("content-length", "0"))

    async def download_close(self, cnt: int) -> None:
        resp = self.__downloads[cnt]
        await resp.aclose()
        del self.__downloads[cnt]

    async def ws_create(
        self, url: str = "", params: dict = {}, headers: dict = {}
    ) -> int:
        if headers.get("User-Agent") and self.__session.impersonate != "":
            headers.pop("User-Agent")
        if headers.get("user-agent") and self.__session.impersonate != "":
            headers.pop("user-agent")
        await self.__ws_cnt_lock.acquire()
        self.__ws_cnt += 1
        cnt = self.__ws_cnt
        self.__ws_cnt_lock.release()
        ws = await self.__session.ws_connect(url, params=params, headers=headers)
        self.__ws[cnt] = ws
        self.__ws_is_closed[cnt] = False
        self.__ws_need_close[cnt] = False
        return cnt

    async def ws_send(self, cnt: int, data: bytes) -> None:
        if self.__ws_need_close[cnt] or self.__ws_is_closed[cnt]:
            return
        ws = self.__ws[cnt]
        await ws.send_binary(data)

    async def ws_recv(self, cnt: int) -> Tuple[bytes, BiliWsMsgType]:
        ws = self.__ws[cnt]
        try:
            msg, flags = await ws.recv()
        except curl_cffi.CurlError as e:
            if e.code == curl_cffi.CurlECode.GOT_NOTHING:
                return (b"", BiliWsMsgType.CLOSED)
            else:
                raise e
        if flags & curl_cffi.CurlWsFlag.CLOSE:
            return (b"", BiliWsMsgType.CLOSE)
        if flags & curl_cffi.CurlWsFlag.TEXT:
            return (msg, BiliWsMsgType.TEXT)
        if flags & curl_cffi.CurlWsFlag.PING:
            return (msg, BiliWsMsgType.PING)
        return (msg, BiliWsMsgType.BINARY)

    async def ws_close(self, cnt: int) -> None:
        ws = self.__ws[cnt]
        await ws.close()

    async def close(self) -> None:
        await self.__session.close()

    get_wrapped_session.__doc__ = BiliAPIClient.get_wrapped_session.__doc__
    set_proxy.__doc__ = BiliAPIClient.set_proxy.__doc__
    set_timeout.__doc__ = BiliAPIClient.set_timeout.__doc__
    set_verify_ssl.__doc__ = BiliAPIClient.set_verify_ssl.__doc__
    set_trust_env.__doc__ = BiliAPIClient.set_trust_env.__doc__
    request.__doc__ = BiliAPIClient.request.__doc__
    download_create.__doc__ = BiliAPIClient.download_create.__doc__
    download_chunk.__doc__ = BiliAPIClient.download_chunk.__doc__
    download_content_length.__doc__ = BiliAPIClient.download_content_length.__doc__
    ws_create.__doc__ = BiliAPIClient.ws_create.__doc__
    ws_recv.__doc__ = BiliAPIClient.ws_recv.__doc__
    ws_send.__doc__ = BiliAPIClient.ws_send.__doc__
    ws_close.__doc__ = BiliAPIClient.ws_close.__doc__
    close.__doc__ = BiliAPIClient.close.__doc__
