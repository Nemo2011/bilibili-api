"""
bilibili_api.clients.httpx

HTTPXClient 实现
"""

import asyncio
from collections.abc import AsyncGenerator

import anyio
import httpx  # pylint: disable=E0401

from ..exceptions import ApiException
from ..utils.network import (
    BiliAPIClient,
    BiliAPIFile,
    BiliAPIResponse,
)


class HTTPXClient(BiliAPIClient):
    """
    httpx 模块请求客户端
    """

    def __init__(
        self,
        proxy: str = "",
        timeout: float = 0.0,
        verify_ssl: bool = True,
        trust_env: bool = True,
        http2: bool = False,
        session: httpx.AsyncClient | None = None,
    ) -> None:
        """
        Args:
            proxy (str, optional): 代理地址. Defaults to "".
            timeout (float, optional): 请求超时时间. Defaults to 0.0.
            verify_ssl (bool, optional): 是否验证 SSL. Defaults to True.
            trust_env (bool, optional): `trust_env`. Defaults to True.
            http2 (bool, optional): 是否使用 HTTP2. Defaults to False.
            session (object, optional): 会话对象. Defaults to None.

        Note: 仅当用户只提供 `session` 参数且用户中途未调用 `set_xxx` 函数才使用用户提供的 `session`。
        """
        self.__proxy = proxy
        self.__timeout = timeout
        self.__verify_ssl = verify_ssl
        self.__trust_env = trust_env
        self.__http2 = http2
        if session:
            self.__session = session
        else:
            self.__session = httpx.AsyncClient(
                timeout=self.__timeout,
                proxy=self.__proxy if self.__proxy != "" else None,
                verify=self.__verify_ssl,
                trust_env=self.__trust_env,
                http2=self.__http2,
            )
        self.__downloads: dict[int, httpx.Response] = {}
        self.__download_iter: dict[int, AsyncGenerator] = {}
        self.__download_cnt: int = 0

        self.__need_update_session: bool = False
        self.__session_update_lock = asyncio.Lock()
        self.__down_cnt_lock = asyncio.Lock()

    def get_wrapped_session(self) -> httpx.AsyncClient:
        return self.__session

    def set_proxy(self, proxy: str = "") -> None:
        self.__proxy = proxy
        self.__need_update_session = True

    def set_timeout(self, timeout: float = 0.0) -> None:
        self.__timeout = timeout
        self.__session.timeout = timeout

    def set_verify_ssl(self, verify_ssl: bool = True) -> None:
        self.__verify_ssl = verify_ssl
        self.__need_update_session = True

    def set_trust_env(self, trust_env: bool = True) -> None:
        self.__trust_env = trust_env
        self.__session.trust_env = trust_env

    async def __auto_update_session(self) -> None:
        await self.__session_update_lock.acquire()
        if self.__need_update_session:
            await self.__session.aclose()
            self.__session = httpx.AsyncClient(
                timeout=self.__timeout,
                proxy=self.__proxy if self.__proxy != "" else None,
                verify=self.__verify_ssl,
                trust_env=self.__trust_env,
                http2=self.__http2,
            )
            self.__need_update_session = False
        self.__session_update_lock.release()

    def set_http2(self, http2: bool = False) -> None:
        """
        设置是否使用 http2.

        Args:
            http2 (str, optional): 是否使用 http2. Defaults to False.
        """
        self.__http2 = http2
        self.__session = httpx.AsyncClient(
            timeout=self.__timeout,
            proxy=self.__proxy if self.__proxy != "" else None,
            verify=self.__verify_ssl,
            trust_env=self.__trust_env,
            http2=self.__http2,
        )

    async def request(
        self,
        method: str = "",
        url: str = "",
        params: dict = {},
        data: dict | str | bytes = {},
        files: dict[str, BiliAPIFile] = {},
        headers: dict = {},
        cookies: dict = {},
        allow_redirects: bool = True,
    ) -> BiliAPIResponse:
        await self.__auto_update_session()
        if files != {}:
            requests_like_files = {}
            for key, item in files.items():
                async with await anyio.open_file(item.path, "rb") as f:
                    requests_like_files[key] = (
                        item.path,
                        await f.read(),
                        item.mime_type,
                    )
            files = requests_like_files
        resp: httpx.Response = await self.__session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            files=files,
            headers=headers,
            cookies=cookies,
            follow_redirects=allow_redirects,
        )
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
        await self.__auto_update_session()
        await self.__down_cnt_lock.acquire()
        self.__download_cnt += 1
        cnt = self.__download_cnt
        self.__down_cnt_lock.release()
        req = self.__session.build_request(method="GET", url=url, headers=headers)
        self.__downloads[cnt] = await self.__session.send(
            req, stream=True, follow_redirects=True
        )
        self.__download_iter[cnt] = self.__downloads[cnt].aiter_bytes(4096)
        return cnt

    async def download_chunk(self, cnt: int) -> bytes:
        iter = self.__download_iter[cnt]
        data = await anext(iter)
        return data

    def download_content_length(self, cnt: int) -> int:
        resp = self.__downloads[cnt]
        return int(resp.headers.get("content-length", "0"))

    async def download_close(self, cnt: int) -> None:
        resp = self.__downloads[cnt]
        await resp.aclose()
        del self.__downloads[cnt]
        del self.__download_iter[cnt]

    async def ws_create(self, *args, **kwargs) -> None:
        """
        httpx 库暂未实现 WebSocket。相关讨论：<https://github.com/encode/httpx/issues/304>
        """
        raise ApiException(
            "httpx 库暂未实现 WebSocket。相关讨论：<https://github.com/encode/httpx/issues/304>"
        )

    async def ws_send(self, *args, **kwargs) -> None:
        """
        httpx 库暂未实现 WebSocket。相关讨论：<https://github.com/encode/httpx/issues/304>
        """
        raise ApiException(
            "httpx 库暂未实现 WebSocket。相关讨论：<https://github.com/encode/httpx/issues/304>"
        )

    async def ws_recv(self, *args, **kwargs) -> None:
        """
        httpx 库暂未实现 WebSocket。相关讨论：<https://github.com/encode/httpx/issues/304>
        """
        raise ApiException(
            "httpx 库暂未实现 WebSocket。相关讨论：<https://github.com/encode/httpx/issues/304>"
        )

    async def ws_close(self, *args, **kwargs) -> None:
        """
        httpx 库暂未实现 WebSocket。相关讨论：<https://github.com/encode/httpx/issues/304>
        """
        raise ApiException(
            "httpx 库暂未实现 WebSocket。相关讨论：<https://github.com/encode/httpx/issues/304>"
        )

    async def close(self) -> None:
        await self.__session.aclose()
        del self.__session

    get_wrapped_session.__doc__ = BiliAPIClient.get_wrapped_session.__doc__
    set_proxy.__doc__ = BiliAPIClient.set_proxy.__doc__
    set_timeout.__doc__ = BiliAPIClient.set_timeout.__doc__
    set_verify_ssl.__doc__ = BiliAPIClient.set_verify_ssl.__doc__
    set_trust_env.__doc__ = BiliAPIClient.set_trust_env.__doc__
    request.__doc__ = BiliAPIClient.request.__doc__
    download_create.__doc__ = BiliAPIClient.download_create.__doc__
    download_chunk.__doc__ = BiliAPIClient.download_chunk.__doc__
    download_content_length.__doc__ = BiliAPIClient.download_content_length.__doc__
    close.__doc__ = BiliAPIClient.close.__doc__
