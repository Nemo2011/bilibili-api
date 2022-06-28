import asyncio
from asyncio.exceptions import CancelledError
from asyncio.tasks import Task, create_task
import os
from . import settings
from .utils.Credential import Credential
from copy import copy, deepcopy
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException
import json
from enum import Enum

from .exceptions.ApiException import ApiException
from .exceptions.NetworkException import NetworkException
from typing import TypedDict, List
from hashlib import md5
import base64
from urllib.parse import quote_plus
import mimetypes

from .utils.AsyncEvent import AsyncEvent
from .utils.network import get_session, request, to_form_urlencoded
from .utils.utils import chunk, get_api

# import ffmpeg

_API = get_api("video_uploader")


class VideoUploaderPage:
    """
    分 P 对象
    """

    def __init__(self, path: str, title: str, description: str = ""):
        """
        Args:
            path (str): 视频文件路径
            title        (str)           : 视频标题
            description  (str, optional) : 视频简介. Defaults to "".
        """
        self.path = path
        self.title: str = title
        self.description: str = description

        self.cached_size: int = None

    def get_size(self) -> int:
        """
        获取文件大小

        Returns:
            int: 文件大小
        """
        if self.cached_size is not None:
            return self.cached_size

        size: int = 0
        stream = open(self.path, "rb")
        while True:
            s: bytes = stream.read(1024)

            if not s:
                break

            size += len(s)

        stream.close()

        self.cached_size = size
        return size


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


class VideoUploader(AsyncEvent):
    """
    视频上传
    """

    def __init__(
        self,
        pages: List[VideoUploaderPage],
        meta: dict,
        credential: Credential,
        cover_path: str = None,
        #  ffprobe_path: str = 'ffprobe'
    ):
        """
        Args:
            pages        (List[VideoUploaderPage]): 分 P 列表
            meta         (dict)                   : 视频信息
            credential   (Credential)             : 凭据
            cover_path   (str)                    : 封面路径

        meta 参数示例：

        ```json
        {
            "act_reserve_create": "const int: 0",
            "copyright": "int, 投稿类型。1 自制，2 转载。",
            "source": "str: 视频来源。投稿类型为转载时注明来源，为原创时为空。",
            "cover": "str: 封面 URL",
            "desc": "str: 视频简介。",
            "desc_format_id": "const int: 0",
            "dynamic": "str: 动态信息。",
            "interactive": "const int: 0",
            "no_reprint": "int: 显示未经作者授权禁止转载，仅当为原创视频时有效。1 为启用，0 为关闭。",
            "open_elec": "int: 是否展示充电信息。1 为是，0 为否。",
            "origin_state": "const int: 0",
            "subtitles # 字幕设置": {
                "lan": "str: 字幕投稿语言，不清楚作用请将该项设置为空",
                "open": "int: 是否启用字幕投稿，1 or 0"
            },
            "tag": "str: 视频标签。使用英文半角逗号分隔的标签组。示例：标签 1,标签 1,标签 1",
            "tid": "int: 分区 ID。可以使用 channel 模块进行查询。",
            "title": "str: 视频标题",
            "up_close_danmaku": "bool: 是否关闭弹幕。",
            "up_close_reply": "bool: 是否关闭评论。",
            "up_selection_reply": "bool: 是否开启评论精选",
            "videos # 分 P 列表": [
                {
                "title": "str: 标题",
                "desc": "str: 简介",
                "filename": "str: preupload 时返回的 filename"
                }
            ],
            "dtime": "int?: 可选，定时发布时间戳（秒）"
        }
        ```

        meta 保留字段：videos, cover
        """
        super().__init__()
        self.meta = meta
        self.pages = pages
        self.credential = credential
        self.cover_path = cover_path
        # self.ffprobe_path = ffprobe_path
        self.__task: Task = None

    async def _preupload(self, page: VideoUploaderPage) -> dict:
        """
        分 P 上传初始化

        Returns:
            dict: 初始化信息
        """
        self.dispatch(VideoUploaderEvents.PREUPLOAD.value, {page: page})
        api = _API["preupload"]

        # 首先获取视频文件预检信息
        session = get_session()

        async with session.get(
            api["url"],
            params={
                "profile": "ugcfx/bup",
                "name": os.path.basename(page.path),
                "size": page.get_size(),
                "r": "upos",
                "ssl": "0",
                "version": "2.10.4",
                "build": "2100400",
                "upcdn": "bda2",
                "probe_version": "20211012",
            },
            cookies=self.credential.get_cookies(),
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://www.bilibili.com",
            },
            proxy=settings.proxy,
        ) as resp:
            if resp.status >= 400:
                self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
                raise NetworkException(resp.status, resp.reason)

            preupload = await resp.json()

            if preupload["OK"] != 1:
                self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
                raise ApiException(json.dumps(preupload))

        url = self._get_upload_url(preupload)

        # 获取 upload_id
        async with session.post(
            url,
            headers={
                "x-upos-auth": preupload["auth"],
                "user-agent": "Mozilla/5.0",
                "referer": "https://www.bilibili.com",
            },
            params={
                "uploads": "",
                "output": "json",
                "profile": "ugcfx/bup",
                "filesize": page.get_size(),
                "partsize": preupload["chunk_size"],
                "biz_id": preupload["biz_id"],
            },
            proxy=settings.proxy,
        ) as resp:
            if resp.status >= 400:
                self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
                raise ApiException("获取 upload_id 错误")

            data = json.loads(await resp.text())

            if data["OK"] != 1:
                self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
                raise ApiException("获取 upload_id 错误：" + json.dumps(data))

            preupload["upload_id"] = data["upload_id"]

        # # 读取并上传视频元数据，这段代码暂时用不上
        # meta = ffmpeg.probe(page.path)
        # meta_format = meta["format"]
        # meta_video = list(map(lambda x: x if x["codec_type"] == "video" else None, meta["streams"]))
        # meta_video.remove(None)
        # meta_video = meta_video[0]

        # meta_audio = list(map(lambda x: x if x["codec_type"] == "audio" else None, meta["streams"]))
        # meta_audio.remove(None)
        # meta_audio = meta_audio[0]

        # meta_to_upload = json.dumps({
        #     "code": 0,
        #     "filename": os.path.splitext(os.path.basename(preupload["upos_uri"]))[0],
        #     "filesize": int(meta_format["size"]),
        #     "key_frames": [],
        #     "meta": {
        #         "audio_meta": meta_audio,
        #         "video_meta": meta_video,
        #         "container_meta": {
        #             "duration": round(float(meta_format["duration"]), 2),
        #             "format_name": meta_format["format_name"]
        #         }
        #     },
        #     "version": "2.3.7",
        #     "webVersion": "1.0.0"
        # })

        # # 预检元数据上传
        # async with session.get(api["url"], params={
        #     "name": "BUploader_meta.txt",
        #     "size": len(meta_to_upload),
        #     "r": "upos",
        #     "profile": "fxmeta/bup",
        #     "ssl": "0",
        #     "version": "2.10.3",
        #     "build": "2100300",
        # }, cookies=self.credential.get_cookies(),
        #     headers={
        #         "User-Agent": "Mozilla/5.0",
        #         "Referer": "https://www.bilibili.com"
        #     }, proxy=settings.proxy
        # ) as resp:
        #     if resp.status >= 400:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise NetworkException(resp.status, resp.reason)

        #     preupload_m = await resp.json()

        #     if preupload_m['OK'] != 1:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise ApiException(json.dumps(preupload_m))

        # url = self._get_upload_url(preupload_m)

        # # 获取 upload_id
        # async with session.post(url, params={
        #     "uploads": "",
        #     "output": "json"
        # }, headers={
        #     "x-upos-auth": preupload_m["auth"]
        # }, proxy=settings.proxy) as resp:
        #     if resp.status >= 400:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise NetworkException(resp.status, resp.reason)

        #     data = json.loads(await resp.text())
        #     if preupload_m['OK'] != 1:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise ApiException(json.dumps(preupload_m))

        #     upload_id = data["upload_id"]

        # size = len(meta_to_upload)
        # async with session.put(url, params={
        #     "partNumber": 1,
        #     "uploadId": upload_id,
        #     "chunk": 0,
        #     "chunks": 1,
        #     "size": size,
        #     "start": 0,
        #     "end": size,
        #     "total": size
        # }, headers={
        #     "x-upos-auth": preupload_m["auth"]
        # }, data=meta_to_upload, proxy=settings.proxy) as resp:
        #     if resp.status >= 400:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise NetworkException(resp.status, resp.reason)

        #     data = await resp.text()

        #     if data != 'MULTIPART_PUT_SUCCESS':
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise ApiException(json.dumps(preupload_m))

        # async with session.post(url,
        #     data=json.dumps({"parts": [{"partNumber": 1, "eTag": "etag"}]}),
        #     params={
        #         "output": "json",
        #         "name": "BUploader_meta.txt",
        #         "profile": "",
        #         "uploadId": upload_id,
        #         "biz_id": ""
        #     },
        #     headers={
        #         "x-upos-auth": preupload_m["auth"]
        #     }, proxy=settings.proxy
        # ) as resp:
        #     if resp.status >= 400:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise NetworkException(resp.status, resp.reason)

        #     data = json.loads(await resp.text())

        #     if data['OK'] != 1:
        #         self.dispatch(VideoUploaderEvents.PREUPLOAD_FAILED.value, {page: page})
        #         raise ApiException(json.dumps(data))

        return preupload

    async def _main(self) -> dict:
        videos = []
        for page in self.pages:
            data = await self._upload_page(page)
            videos.append(
                {
                    "title": page.title,
                    "desc": page.description,
                    "filename": data["filename"],
                    "cid": data["cid"],
                }
            )

        cover_url = ""

        if self.cover_path:
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
        api = _API["cover_up"]
        mime = mimetypes.guess_type(self.cover_path)[0]

        with open(self.cover_path, "rb") as f:
            data = {
                "cover": f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"
            }

        try:
            resp = await request(
                "POST", api["url"], data=data, credential=self.credential
            )
            self.dispatch(VideoUploaderEvents.AFTER_COVER.value, {"url": resp["url"]})
            return resp["url"]

        except Exception as e:
            self.dispatch(VideoUploaderEvents.COVER_FAILED.value, {"err": e})
            raise e

    async def _upload_page(self, page: VideoUploaderPage) -> str:
        """
        上传分 P

        Args:
            page (VideoUploaderPage): 分 P 对象

        Returns:
            str: 分 P 文件 ID，用于 submit 时的 $.videos[n].filename 字段使用。
        """
        preupload = await self._preupload(page)
        self.dispatch(VideoUploaderEvents.PRE_PAGE.value, {"page": page})

        page_size = page.get_size()
        # 所有分块起始位置
        chunk_offset_list = list(range(0, page_size, preupload["chunk_size"]))
        # 分块总数
        total_chunk_count = len(chunk_offset_list)
        # 并发上传分块
        chunk_number = 0
        # 上传队列
        chunks_pending = []
        # 缓存 upload_id，这玩意只能从上传的分块预检结果获得
        upload_id = preupload["upload_id"]
        for offset in chunk_offset_list:
            chunks_pending.insert(
                0,
                self._upload_chunk(
                    page, offset, chunk_number, total_chunk_count, preupload
                ),
            )
            chunk_number += 1

        while chunks_pending:
            tasks = []

            while len(tasks) < preupload["threads"] and len(chunks_pending) > 0:
                tasks.append(create_task(chunks_pending.pop()))

            result = await asyncio.gather(*tasks)

            for r in result:
                if not r["ok"]:
                    chunks_pending.insert(
                        0,
                        self._upload_chunk(
                            page,
                            r["offset"],
                            r["chunk_number"],
                            total_chunk_count,
                            preupload,
                        ),
                    )

        data = await self._complete_page(page, total_chunk_count, preupload, upload_id)

        self.dispatch(VideoUploaderEvents.AFTER_PAGE.value, {"page": page})

        return data

    @staticmethod
    def _get_upload_url(preupload: dict) -> str:
        # 上传目标 URL
        return (
            "https:"
            + preupload["endpoint"]
            + "/"
            + preupload["upos_uri"].removeprefix("upos://")
        )

    async def _upload_chunk(
        self,
        page: VideoUploaderPage,
        offset: int,
        chunk_number: int,
        total_chunk_count: int,
        preupload: dict,
    ) -> dict:
        """
        上传视频分块

        Args:
            page (VideoUploaderPage): 分 P 对象
            offset (int): 分块起始位置
            chunk_number (int): 分块编号
            total_chunk_count (int): 总分块数
            preupload (dict): preupload 数据

        Returns:
            dict: 上传结果和分块信息。
        """
        chunk_event_callback_data = {
            "page": page,
            "offset": offset,
            "chunk_number": chunk_number,
            "total_chunk_count": total_chunk_count,
        }
        self.dispatch(VideoUploaderEvents.PRE_CHUNK.value, chunk_event_callback_data)
        session = get_session()

        stream = open(page.path, "rb")
        stream.seek(offset)
        chunk = stream.read(preupload["chunk_size"])
        stream.close()

        # 上传目标 URL
        url = self._get_upload_url(preupload)

        err_return = {
            "ok": False,
            "chunk_number": chunk_number,
            "offset": offset,
            "page": page,
        }

        real_chunk_size = len(chunk)

        params = {
            "partNumber": str(chunk_number + 1),
            "uploadId": str(preupload["upload_id"]),
            "chunk": str(chunk_number),
            "chunks": str(total_chunk_count),
            "size": str(real_chunk_size),
            "start": str(offset),
            "end": str(offset + real_chunk_size),
            "total": page.get_size(),
        }

        ok_return = {
            "ok": True,
            "chunk_number": chunk_number,
            "offset": offset,
            "page": page,
        }

        try:
            async with session.put(
                url,
                data=chunk,
                params=params,
                headers={"x-upos-auth": preupload["auth"]},
                proxy=settings.proxy,
            ) as resp:
                if resp.status >= 400:
                    chunk_event_callback_data["info"] = f"Status {resp.status}"
                    self.dispatch(
                        VideoUploaderEvents.CHUNK_FAILED.value,
                        chunk_event_callback_data,
                    )
                    return err_return

                data = await resp.text()

                if data != "MULTIPART_PUT_SUCCESS":
                    chunk_event_callback_data["info"] = "分块上传失败"
                    self.dispatch(
                        VideoUploaderEvents.CHUNK_FAILED.value,
                        chunk_event_callback_data,
                    )
                    return err_return

        except Exception as e:
            chunk_event_callback_data["info"] = str(e)
            self.dispatch(
                VideoUploaderEvents.CHUNK_FAILED.value, chunk_event_callback_data
            )
            return err_return

        self.dispatch(VideoUploaderEvents.AFTER_CHUNK.value, chunk_event_callback_data)
        return ok_return

    async def _complete_page(
        self, page: VideoUploaderPage, chunks: int, preupload: dict, upload_id: str
    ) -> None:
        """
        提交分 P 上传

        Args:
            page (VideoUploaderPage): 分 P 对象
            chunks (int): 分块数量
            preupload (dict): preupload 数据
            upload_id (str): upload_id

        Returns:
            dict: filename: 该分 P 的标识符，用于最后提交视频。cid: 分 P 的 cid
        """
        self.dispatch(VideoUploaderEvents.PRE_PAGE_SUBMIT.value, {"page": page})

        data = {
            "parts": list(
                map(lambda x: {"partNumber": x, "eTag": "etag"}, range(1, chunks + 1))
            )
        }

        params = {
            "output": "json",
            "name": os.path.basename(page.path),
            "profile": "ugcfx/bup",
            "uploadId": upload_id,
            "biz_id": preupload["biz_id"],
        }

        url = self._get_upload_url(preupload)

        session = get_session()

        async with session.post(
            url=url,
            data=json.dumps(data),
            headers={
                "x-upos-auth": preupload["auth"],
                "content-type": "application/json; charset=UTF-8",
            },
            params=params,
            proxy=settings.proxy,
        ) as resp:
            if resp.status >= 400:
                err = NetworkException(resp.status, "状态码错误，提交分 P 失败")
                self.dispatch(
                    VideoUploaderEvents.PAGE_SUBMIT_FAILED.value,
                    {"page": page, "err": err},
                )
                raise err

            data = json.loads(await resp.read())

            if data["OK"] != 1:
                err = ResponseCodeException(-1, f'提交分 P 失败，原因: {data["message"]}')
                self.dispatch(
                    VideoUploaderEvents.PAGE_SUBMIT_FAILED.value,
                    {"page": page, "err": err},
                )
                raise err

        self.dispatch(VideoUploaderEvents.AFTER_PAGE_SUBMIT.value, {"page": page})

        return {
            "filename": os.path.splitext(data["key"].removeprefix("/"))[0],
            "cid": preupload["biz_id"],
        }

    async def _submit(self, videos: list, cover_url: str = "") -> dict:
        """
        提交视频

        Args:
            videos (list): 视频列表
            cover_url (str, optional): 封面 URL.

        Returns:
            dict: 含 bvid 和 aid 的字典
        """
        meta = copy(self.meta)
        meta["cover"] = cover_url
        meta["videos"] = videos

        self.dispatch(VideoUploaderEvents.PRE_SUBMIT.value, deepcopy(meta))
        api = _API["submit"]

        try:
            resp = await request(
                "POST",
                api["url"],
                params={"csrf": self.credential.bili_jct},
                data=json.dumps(meta),
                headers={"content-type": "application/json"},
                credential=self.credential,
                no_csrf=True,
            )

            self.dispatch(VideoUploaderEvents.AFTER_SUBMIT.value, resp)
            return resp

        except Exception as err:
            self.dispatch(VideoUploaderEvents.SUBMIT_FAILED.value, {"err": err})
            raise err

    async def abort(self):
        """
        中断上传
        """
        if self.__task:
            self.__task.cancel("用户手动取消")

        self.dispatch(VideoUploaderEvents.ABORTED.value, None)


async def get_missions(tid: int = 0, credential: Credential = None):
    """
    获取活动信息

    Args:
        tid        (int, optional)       : 分区 ID. Defaults to 0.
        credential (Credential, optional): 凭据. Defaults to None.

    Returns:
        dict API 调用返回结果
    """
    api = _API["missions"]

    params = {"tid": tid}

    return await request("GET", api["url"], params=params, credential=credential)
