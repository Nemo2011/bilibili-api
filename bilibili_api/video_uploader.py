import asyncio
from asyncio.exceptions import CancelledError
from asyncio.tasks import Task, create_task
from copy import copy, deepcopy
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException
import json
from enum import Enum

from yarl import URL
from bilibili_api.exceptions.ApiException import ApiException
from bilibili_api.exceptions.NetworkException import NetworkException
from bilibili_api.exceptions.ArgsException import ArgsException
from io import BufferedIOBase
from typing import TypedDict, List
from hashlib import md5
import rsa
import time
import base64
import random
import string
from urllib.parse import quote_plus
from aiohttp import FormData
import mimetypes

from .utils.AsyncEvent import AsyncEvent
from .utils.network import get_session, to_form_urlencoded
from .utils.utils import get_api

_APP_KEY = "aae92bc66f3edfab"
_APP_SIGN_SALT = "af125a0d5279fd576c1b4418a3e8276d"

_API = get_api("video_uploader")


def _sign(data: str) -> str:
    """
    签名请求

    参考：https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/other/API_auth.md

    Args:
        data (str): 要签名的请求参数

    Returns:
        str: 签名后的 md5 hex
    """
    string_to_sign = data + _APP_SIGN_SALT

    return md5(string_to_sign.encode('utf8')).hexdigest()


def _get_ts() -> str:
    return str(int(time.time()))


class VideoUploaderCredential:
    """
    视频上传凭据
    """
    def __init__(self, access_key: str = None, account: str = None, password: str = None) -> None:
        """
        必须满足 access_key or (account and password)

        Args:
            access_key (str, optional): access_key. Defaults to None.
            account    (str, optional): 账号. Defaults to None.
            password   (str, optional): 密码. Defaults to None.
        """
        if not (access_key or (account and password)):
            raise ArgsException('参数未满足 access_key or (account and password)')

        self.access_key: str = access_key
        self.account: str = account
        self.password: str = password

    async def _prelogin(self) -> str:
        """
        获取登录时加密密码的 RSA 公钥和盐值

        Returns:
            str: 登录时加密密码的 RSA 公钥和盐值
        """
        api = _API['prelogin']
        data = await _request('GET', api['url'])

        return data

    async def login(self) -> None:
        """
        使用账号密码登录获取 access_key，并设置 self.access_key

        注意：大部分时候不需要验证码，但是请求过于频繁可能需要，请尽量使用 access_key

        """
        if not all([self.account, self.password]):
            raise ArgsException("请提供 account 和 password")

        api = _API['login']

        prelogin = await self._prelogin()

        pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(
            prelogin['key'].encode('utf8'))
        msg = prelogin['hash'] + self.password
        encryptedPassword = base64.b64encode(rsa.encrypt(
            msg.encode('utf8'), pub_key)).decode('utf8')

        random_device_id = ''.join(random.sample(
            string.ascii_uppercase + string.digits, 12))
        random_buvid = ''.join(random.sample(
            string.ascii_uppercase + string.digits, 8)) + '-' + random_device_id

        data = {
            "appkey": _APP_KEY,
            "buvid": random_buvid,
            "device_id": random_device_id,
            "device_name": "Fuck YILU",
            "device_platform": "Windows 10",
            "password": encryptedPassword,
            "platform": "pc"
        }

        data = to_form_urlencoded(data)
        extraData = f'&ts={_get_ts()}&username={quote_plus(self.account)}'

        # sign 必须在这个位置才校验正确，迷惑，服了
        data += f'&sign={_sign(data + extraData)}'
        data += extraData

        resp = await _request('POST', api['url'], data=data, raw=True, headers={
            'content-type': 'application/x-www-form-urlencoded',
        })

        self.access_key = resp['token_info']['access_token']

    async def get_access_key(self) -> str:
        """
        获取 access_key，若未登录将会自动登录

        Returns:
            str: access_key
        """
        if self.access_key:
            return self.access_key

        await self.login()

        return self.access_key


async def _request(method: str,
                   url: str,
                   params: dict = None,
                   data: dict = None,
                   headers: dict = None,
                   raw: bool = False,
                   credential: VideoUploaderCredential = None):
    if headers is None:
        headers = {}

    if not raw:
        if method == 'GET':
            if params is None:
                params = {}

            params["appkey"] = _APP_KEY
            params["ts"] = _get_ts()
            params = to_form_urlencoded(params)

            if credential is not None:
                params = f'access_key={await credential.get_access_key()}&' + params

            params += '&sign=' + _sign(params)

        else:
            if data is None:
                data = {}

            data["appkey"] = _APP_KEY
            data["ts"] = _get_ts()

            if credential is not None:
                data["access_key"] = await credential.get_access_key()

            data = to_form_urlencoded(data)
            data += '&sign=' + _sign(data)

            headers['content-type'] = 'application/x-www-form-urlencoded'

    session = get_session()

    async with session.request(method,
                               url + ('?' + params if type(params)
                                      == str and params else ''),
                               params=params if type(params) == dict else None,
                               data=data,
                               headers=headers) as resp:
        if resp.status >= 400:
            raise NetworkException(resp.status, resp.reason)

        r = await resp.json()
        if r["code"] < 0:
            raise ApiException(r["message"])

        return r["data"]


class VideoUploaderPage:
    """
    分 P 对象
    """
    def __init__(self, video_stream: BufferedIOBase, title: str, description: str = "", extension: str = "mp4"):
        """
        Args:
            video_stream (BufferedIOBase): 视频流
            title        (str)           : 视频标题
            description  (str, optional) : 视频简介. Defaults to "".
            extension    (str, optional) : 视频流扩展名. Defaults to "mp4".
        """
        self.video_stream: BufferedIOBase = video_stream
        self.title: str = title
        self.description: str = description
        self.extension = extension

    def get_size(self) -> int:
        """
        获取文件大小

        Returns:
            int: 文件大小
        """
        size: int = 0
        self.video_stream.seek(0)
        while True:
            s: bytes = self.video_stream.read(1024)

            if not s:
                break

            size += len(s)

        return size

    def get_md5(self) -> str:
        """
        获取文件 MD5

        Returns:
            str: md5
        """
        self.video_stream.seek(0)
        h = md5()

        while True:
            s: bytes = self.video_stream.read(1024)

            if not s:
                break

            h.update(s)

        return h.hexdigest()


class VideoUploaderEvents(Enum):
    """
    上传事件枚举

    Events:
    + PRE_PAGE 上传分 P 前
    + PREUPLOAD  获取上传信息
    + PREUPLOAD_FAILED  获取上传信息失败
    + PRE_CHUNK  上传分块前
    + AFTER_CHUNK  上传分块后
    + CHUNK_FAILED  区块上传失败
    + PRE_PAGE_SUBMIT  提交分 P 前
    + PAGE_SUBMIT_FAILED  提交分 P 失败
    + AFTER_PAGE_SUBMIT  提交分 P 后
    + AFTER_PAGE  上传分 P 后
    + PRE_COVER  上传封面前
    + AFTER_COVER  上传封面后
    + COVER_FAILED  上传封面失败
    + PRE_SUBMIT  提交视频前
    + SUBMIT_FAILED  提交视频失败
    + AFTER_SUBMIT  提交视频后
    + COMPLETED  完成上传
    + ABORTED  用户中止
    + FAILED  上传失败
    """
    PREUPLOAD = "PREUPLOAD"
    PREUPLOAD_FAILED = "PREUPLOAD_FAILED"
    PRE_PAGE = "PRE_PAGE"

    PRE_CHUNK = "PRE_CHUNK"
    AFTER_CHUNK = "AFTER_CHUNK"
    CHUNK_FAILED = "CHUNK_FAILED"

    PRE_PAGE_SUBMIT = "PRE_PAGE_SUBMIT"
    PAGE_SUBMIT_FAILED = "PAGE_SUBMIT_FAILED"
    AFTER_PAGE_SUBMIT = "AFTER_PAGE_SUBMIT"

    AFTER_PAGE = "AFTER_PAGE"

    PRE_COVER = "PRE_COVER"
    AFTER_COVER = "AFTER_COVER"
    COVER_FAILED = "COVER_FAILED"

    PRE_SUBMIT = "PRE_SUBMIT"
    SUBMIT_FAILED = "SUBMIT_FAILED"
    AFTER_SUBMIT = "AFTER_SUBMIT"

    COMPLETED = "COMPLETE"
    ABORTED = "ABORTED"
    FAILED = "FAILED"

_VERSION = '2.3.0.1066'


class _ChunkResult(TypedDict):
    ok: bool
    chunk_number: int
    offset: int
    page: VideoUploaderPage
    info: str


class VideoUploader(AsyncEvent):
    """
    视频上传
    """
    def __init__(self,
                 pages: List[VideoUploaderPage],
                 meta: dict,
                 credential: VideoUploaderCredential,
                 threads: int = 5,
                 chunk_size: int = 2048 * 1024,
                 cover_stream: BufferedIOBase = None,
                 cover_type: str = 'image/jpeg'):
        """
        Args:
            pages        (List[VideoUploaderPage]): 分 P 列表
            meta         (dict)                   : 视频信息
            credential   (VideoUploaderCredential): 凭据（注意，是 VideoUploaderCredential）
            threads      (int, optional)          : 最大并发. Defaults to 5.
            chunk_size   (int, optional)          : 分块大小（字节），不知道什么意思请保持默认. Defaults to 2048*1024.
            cover_stream (BufferedIOBase)         : 封面流
            cover_type   (str)                    : 封面 MIME 类型，常见后缀对应：jpg: image/jpeg; png: image/png; webp: image/webp. Defaults to "image/jpeg"

        meta 参数示例：

        ```json
        {
            "copyright": "int, 投稿类型。1 自制，2 转载。",
            "source": "str, 视频来源。投稿类型为转载时注明来源，为原创时为空。",
            "desc": "str, 视频简介。",
            "desc_format_id": 0,
            "dynamic": "str, 动态信息。",
            "interactive": 0,
            "open_elec": "int, 是否展示充电信息。1 为是，0 为否。",
            "no_reprint": "int, 显示未经作者授权禁止转载，仅当为原创视频时有效。1 为启用，0 为关闭。",
            "subtitles": {
                "lan": "str: 字幕投稿语言，不清楚作用请将该项设置为空",
                "open": "int: 是否启用字幕投稿，1 or 0"
            },
            "tag": "str, 视频标签。使用英文半角逗号分隔的标签组。示例：标签 1,标签 1,标签 1",
            "tid": "int, 分区 ID。可以使用 channel 模块进行查询。",
            "title": "str: 视频标题",
            "up_close_danmaku": "bool, 是否关闭弹幕。",
            "up_close_reply": "bool, 是否关闭评论。",
            "dtime": "int?: 可选，定时发布时间戳（秒）"
        }
        ```

        meta 保留字段：videos, cover
        """
        super().__init__()
        self.meta = meta
        self.pages = pages
        self.credential = credential
        self.threads = threads
        self.chunk_size = chunk_size
        self.cover_stream = cover_stream
        self.cover_type = cover_type
        self.__task: Task = None

    async def _preupload(self) -> dict:
        """
        分 P 上传初始化

        Returns:
            dict: 初始化信息
        """
        self.dispatch(VideoUploaderEvents.PREUPLOAD.value)
        api = _API['preupload']

        session = get_session()

        async with session.get(api["url"], params={
            "access_key": await self.credential.get_access_key(),
            "mid": 0,
            "profile": "ugcfr/pc3"
        }) as resp:
            if resp.status >= 400:
                self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value)
                raise NetworkException(resp.status, resp.reason)

            data = await resp.json()

            if data['OK'] != 1:
                self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value)
                raise ApiException(json.dumps(data))

            return data

    async def _main(self) -> dict:
        videos = []
        for page in self.pages:
            filename = await self._upload_page(page)
            videos.append({
                "title": page.title,
                "desc": page.description,
                "filename": filename
            })

        cover_url = ''

        if self.cover_stream:
            cover_url = await self._upload_cover()

        result = await self._submit(videos, cover_url)

        self.dispatch(VideoUploaderEvents.COMPLETED.value, result)
        return result

    async def start(self) -> dict:
        """
        开始上传

        Returns:
            dict: 返回带有 bvid 和 aid 的字典。
        """

        task = create_task(self._main())
        self.__task = task

        try:
            result = await task
            self.__task = None
            return result
        except CancelledError:
            # 忽略 task 取消异常
            pass
        except Exception as e:
            raise e

    async def _upload_cover(self) -> str:
        """
        上传封面

        Returns:
            str: 封面 URL
        """
        self.dispatch(VideoUploaderEvents.PRE_COVER.value, None)
        api = _API['cover_up']
        form = FormData()

        form.add_field('file',
                        self.cover_stream,
                        filename=f'cover.{mimetypes.guess_extension(self.cover_type)}',
                        content_type=self.cover_type)

        params = f'access_key={await self.credential.get_access_key()}'
        params += f'&sign={_sign(params)}'

        session = get_session()

        async with session.post(api['url'], params=params, data=form) as resp:
            if resp.status >= 400:
                err = NetworkException(resp.status, f'状态码错误，上传封面失败')
                self.dispatch(VideoUploaderEvents.COVER_FAILED.value, {"err": err})
                raise err

            data = await resp.json()

            if data['code'] < 0:
                err = ResponseCodeException(data['code'], data['message'])
                self.dispatch(VideoUploaderEvents.COVER_FAILED.value, {"err": err})
                raise err

            self.dispatch(VideoUploaderEvents.AFTER_COVER.value, {"url": data['data']['url']})
            return data['data']['url']

    async def _upload_page(self, page: VideoUploaderPage) -> str:
        """
        上传分 P

        Args:
            page (VideoUploaderPage): 分 P 对象

        Returns:
            str: 分 P 文件 ID，用于 submit 时的 $.videos[n].filename 字段使用。
        """
        preupload = await self._preupload()
        self.dispatch(VideoUploaderEvents.PRE_PAGE.value, {"page": page})

        page_size = page.get_size()
        # 所有区块起始位置
        chunk_offset_list = list(range(0, page_size, self.chunk_size))
        # 区块总数
        total_chunk_count = len(chunk_offset_list)
        # 并发上传区块
        chunk_number = 0
        # 上传队列
        chunks_pending = []
        for offset in chunk_offset_list:
            chunks_pending.insert(0, self._upload_chunk(
                page, offset, preupload['url'], chunk_number, total_chunk_count))
            chunk_number += 1

        while chunks_pending:
            tasks = []

            while len(tasks) < self.threads and len(chunks_pending) > 0:
                tasks.append(create_task(chunks_pending.pop()))

            result = await asyncio.gather(*tasks)

            for r in result:
                if not r['ok']:
                    chunks_pending.insert(0, self._upload_chunk(
                        page, r['offset'], preupload['url'], r['chunk_number'], total_chunk_count))

        await self._complete_page(page, total_chunk_count, preupload['complete'])

        self.dispatch(VideoUploaderEvents.AFTER_PAGE.value, {"page": page})

        return preupload['filename']

    async def _upload_chunk(self, page: VideoUploaderPage, offset: int, url: str, chunk_number: int, total_chunk_count: int) -> _ChunkResult:
        """
        上传视频分块

        Args:
            page (VideoUploaderPage): 分 P 对象
            offset (int): 分块起始位置
            url (str): 目标 URL
            chunk_number (int): 分块编号
            total_chunk_count (int): 总分块数

        Returns:
            _ChunkResult: 上传结果和分块信息。
        """
        chunk_event_callback_data = {"page": page, "offset": offset,
                                     "chunk_number": chunk_number, "total_chunk_count": total_chunk_count}
        self.dispatch(VideoUploaderEvents.PRE_CHUNK.value,
                      chunk_event_callback_data)
        session = get_session()
        page.video_stream.seek(offset)
        chunk = page.video_stream.read(self.chunk_size)

        form = FormData()
        form.add_field('version', _VERSION)
        form.add_field('filesize', str(len(chunk)))
        form.add_field('chunk', str(chunk_number))
        form.add_field('chunks', str(total_chunk_count))
        form.add_field('md5', md5(chunk).hexdigest())
        form.add_field('file', chunk, content_type='application/octet-stream',
                       filename=page.title + '.' + page.extension)

        err_return: _ChunkResult = {
            "ok": False,
            "chunk_number": chunk_number,
            "offset": offset,
            "page": page
        }

        ok_return: _ChunkResult = {
            "ok": True,
            "chunk_number": chunk_number,
            "offset": offset,
            "page": page
        }

        # 阻止 aiohttp 自动转义造成错误
        url = URL(url, encoded=True)

        try:
            async with session.post(url, data=form) as resp:
                if resp.status >= 400:
                    chunk_event_callback_data['info'] = f'Status {resp.status}'
                    self.dispatch(VideoUploaderEvents.CHUNK_FAILED.value,
                                chunk_event_callback_data)
                    return err_return

                data = json.loads(await resp.read())

                if data['OK'] != 1:
                    chunk_event_callback_data['info'] = data['info']
                    self.dispatch(VideoUploaderEvents.CHUNK_FAILED.value,
                                chunk_event_callback_data)
                    return err_return

        except Exception as e:
            chunk_event_callback_data['info'] = str(e)
            self.dispatch(VideoUploaderEvents.CHUNK_FAILED.value,
                                chunk_event_callback_data)
            return err_return

        self.dispatch(VideoUploaderEvents.AFTER_CHUNK.value,
                      chunk_event_callback_data)
        return ok_return

    async def _complete_page(self, page: VideoUploaderPage, chunks: int, url: str) -> None:
        """
        提交分 P 上传

        Args:
            page (VideoUploaderPage): 分 P 对象
            chunks (int): 分块数量
            url (str): 提交 URL
        """
        self.dispatch(VideoUploaderEvents.PRE_PAGE_SUBMIT.value,
                      {"page": page})

        page.video_stream.seek(0)
        page_md5 = page.get_md5()
        page_size = page.get_size()
        page_name = page.title + '.' + page.extension

        data = {
            "chunks": chunks,
            "filesize": page_size,
            "md5": page_md5,
            "name": page_name,
            "version": _VERSION
        }

        session = get_session()

        async with session.post(url=URL(url, encoded=True), data=data) as resp:
            if resp.status >= 400:
                err = NetworkException(resp.status, '状态码错误，提交分 P 失败')
                self.dispatch(VideoUploaderEvents.PAGE_SUBMIT_FAILED.value, {"page": page, "err": err})
                raise err

            data = json.loads(await resp.read())

            if data['OK'] != 1:
                err = ResponseCodeException(-1, f'提交分 P 失败，原因: {data["message"]}')
                self.dispatch(VideoUploaderEvents.PAGE_SUBMIT_FAILED.value, {"page": page, "err": err})
                raise err

        self.dispatch(
            VideoUploaderEvents.AFTER_PAGE_SUBMIT.value, {"page": page})

    async def _submit(self, videos: list, cover_url: str = '') -> dict:
        """
        提交视频

        Args:
            videos (list): 视频列表
            cover_url (str, optional): 封面 URL.

        Returns:
            dict: 含 bvid 和 aid 的字典
        """
        meta = copy(self.meta)
        meta['cover'] = cover_url
        meta['videos'] = videos

        self.dispatch(VideoUploaderEvents.PRE_SUBMIT.value, deepcopy(meta))
        api = _API['submit']

        params = f'access_key={await self.credential.get_access_key()}'
        params += f'&sign={_sign(params)}'

        session = get_session()

        async with session.post(api['url'], params=params, data=json.dumps(meta), headers={
            'content-type': 'application/json'
        }) as resp:
            if resp.status >= 400:
                err = NetworkException(resp.status, f'状态码错误，提交视频失败')
                self.dispatch(VideoUploaderEvents.SUBMIT_FAILED.value, {"err": err})
                raise err

            data = await resp.json()

            if data['code'] < 0:
                err = ResponseCodeException(data['code'], data['message'])
                self.dispatch(VideoUploaderEvents.SUBMIT_FAILED.value, {"err": err})
                raise err

            self.dispatch(VideoUploaderEvents.AFTER_SUBMIT.value, data['data'])
            return data['data']

    async def abort(self):
        """
        中断上传
        """
        if self.__task:
            self.__task.cancel('用户手动取消')

        self.dispatch(VideoUploaderEvents.ABORTED.value, None)
