"""
bilibili_api.clients.aiohttp

AioHTTPClient 实现
"""

import asyncio

import aiohttp
import anyio  # pylint: disable=E0401

from ..utils.network import (
    BiliAPIClient,
    BiliAPIFile,
    BiliAPIResponse,
    BiliWsMsgType,
)


class AioHTTPClient(BiliAPIClient):
    """
    aiohttp 模块请求客户端
    """

    def __init__(
        self,
        proxy="",
        timeout=0,
        verify_ssl=True,
        trust_env=True,
        session: aiohttp.ClientSession | None = None,
    ):
        self.__args: dict = {
            "proxy": proxy,
            "timeout": timeout,
            "verify_ssl": verify_ssl,
            "trust_env": trust_env,
        }
        self.__use_args: bool = True
        self.__need_update_session: bool = False
        self.__session: aiohttp.ClientSession
        if session:
            self.__use_args = False
            self.__session = session
        else:
            self.__session = aiohttp.ClientSession(
                loop=asyncio.get_event_loop(),
                trust_env=self.__args["trust_env"],
                connector=aiohttp.TCPConnector(verify_ssl=self.__args["verify_ssl"]),
            )
        self.__wss: dict[int, aiohttp.ClientWebSocketResponse] = {}
        self.__ws_cnt: int = 0
        self.__downloads: dict[int, aiohttp.ClientResponse] = {}
        self.__download_cnt: int = 0

        self.__session_update_lock = asyncio.Lock()
        self.__ws_cnt_lock = asyncio.Lock()
        self.__down_cnt_lock = asyncio.Lock()

    def get_wrapped_session(self) -> aiohttp.ClientSession:
        return self.__session

    def set_proxy(self, proxy: str = "") -> None:
        self.__use_args = True
        self.__args["proxy"] = proxy

    def set_timeout(self, timeout: float = 0) -> None:
        self.__use_args = True
        self.__args["timeout"] = timeout

    def set_verify_ssl(self, verify_ssl: bool = True) -> None:
        self.__use_args = True
        self.__args["verify_ssl"] = verify_ssl
        self.__need_update_session = True

    def set_trust_env(self, trust_env: bool = True) -> None:
        self.__use_args = True
        self.__args["trust_env"] = trust_env
        self.__need_update_session = True

    async def __auto_update_session(self) -> None:
        await self.__session_update_lock.acquire()
        if self.__need_update_session:
            await self.__session.close()
            self.__session = aiohttp.ClientSession(
                loop=asyncio.get_event_loop(),
                trust_env=self.__args["trust_env"],
                connector=aiohttp.TCPConnector(verify_ssl=self.__args["verify_ssl"]),
            )
            self.__need_update_session = False
        self.__session_update_lock.release()

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
        if files:
            form = aiohttp.FormData()
            if isinstance(data, str):
                raise NotImplementedError
            for key, value in data.items():
                form.add_field(name=key, value=value)
            for key, value in files.items():
                async with await anyio.open_file(value.path, "rb") as f:
                    content = await f.read()
                form.add_field(
                    name=key,
                    value=content,
                    content_type=value.mime_type,
                    filename=value.path.split("/")[-1],
                )
            data = form
        if self.__use_args:
            resp = await self.__session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                cookies=cookies,
                allow_redirects=allow_redirects,
                proxy=self.__args["proxy"],
                timeout=aiohttp.ClientTimeout(self.__args["timeout"]),
            )
        else:
            resp = await self.__session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                cookies=cookies,
                allow_redirects=allow_redirects,
            )
        resp_code = resp.status
        resp_headers = {}
        for key, item in resp.headers.items():
            resp_headers[key] = item
        resp_cookies = {}
        for key, item in resp.cookies.items():
            resp_cookies[key] = item.value
        bili_api_resp = BiliAPIResponse(
            code=resp_code,
            headers=resp_headers,
            cookies=resp_cookies,
            raw=await resp.read(),
            url=str(resp.url),
        )
        resp.release()
        await resp.wait_for_close()
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
        self.__downloads[cnt] = await self.__session.get(url=url, headers=headers)
        return cnt

    async def download_chunk(self, cnt: int) -> bytes:
        resp = self.__downloads[cnt]
        data = await anext(resp.content.iter_chunked(4096))
        return data

    def download_content_length(self, cnt: int) -> int:
        resp = self.__downloads[cnt]
        return int(resp.headers.get("content-length", "0"))

    async def download_close(self, cnt: int) -> None:
        resp = self.__downloads[cnt]
        resp.release()
        await resp.wait_for_close()
        del self.__downloads[cnt]

    async def ws_create(
        self, url: str = "", params: dict = {}, headers: dict = {}
    ) -> int:
        await self.__auto_update_session()
        await self.__ws_cnt_lock.acquire()
        self.__ws_cnt += 1
        cnt = self.__ws_cnt
        self.__ws_cnt_lock.release()
        self.__wss[cnt] = await self.__session.ws_connect(
            url=url, params=params, headers=headers
        )
        return cnt

    async def ws_recv(self, cnt: int) -> tuple[bytes, BiliWsMsgType]:
        msg = await self.__wss[cnt].receive()
        return msg.data, BiliWsMsgType(msg.type.value)

    async def ws_send(self, cnt: int, data: bytes) -> None:
        return await self.__wss[cnt].send_bytes(data)

    async def ws_close(self, cnt: int) -> None:
        await self.__wss[cnt].close()
        del self.__wss[cnt]

    async def close(self):
        await self.__session.close()
        del self.__session

    __init__.__doc__ = BiliAPIClient.__init__.__doc__
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
