"""
bilibili_api.utils.upos
"""
import os
import json
import httpx
import asyncio
from asyncio.tasks import create_task

from .utils import get_api
from .network import get_session
from ..exceptions.NetworkException import NetworkException
from ..exceptions.ResponseCodeException import ResponseCodeException
from ..exceptions.ApiException import ApiException


class UposFile:
    """
    Upos 文件对象
    """

    path: str
    size: int

    def __init__(self, path: str) -> None:
        self.path = path
        self.size = self._get_size(self.path)

    def _get_size(path: str) -> int:
        """
        获取文件大小

        Returns:
            int: 文件大小
        """

        size: int = 0
        stream = open(path, "rb")
        while True:
            s: bytes = stream.read(1024)

            if not s:
                break

            size += len(s)

        stream.close()
        return size


class UposFileUploader:
    """
    Upos 文件上传
    """

    _upload_id: str
    _upload_url: str
    _session: httpx.AsyncClient

    def __init__(self, file: UposFile, preupload: dict) -> None:
        self.file = file
        self.preupload = preupload
        self._upload_id = preupload["upload_id"]
        self._upload_url = f'https:{preupload["endpoint"]}/{preupload["upos_uri"].removeprefix("upos://")}'
        self._session = get_session()

    async def upload(self) -> dict:
        """
        上传文件

        Returns:
            dict: filename, cid
        """
        page_size = self.file.size
        # 所有分块起始位置
        chunk_offset_list = list(range(0, page_size, self.preupload["chunk_size"]))
        # 分块总数
        total_chunk_count = len(chunk_offset_list)
        # 并发上传分块
        chunk_number = 0
        # 上传队列
        chunks_pending = []

        for offset in chunk_offset_list:
            chunks_pending.insert(
                0,
                self._upload_chunk(offset, chunk_number, total_chunk_count),
            )
            chunk_number += 1

        while chunks_pending:
            tasks = []

            while len(tasks) < self.preupload["threads"] and len(chunks_pending) > 0:
                tasks.append(create_task(chunks_pending.pop()))

            result = await asyncio.gather(*tasks)

            for r in result:
                if not r["ok"]:
                    chunks_pending.insert(
                        0,
                        self._upload_chunk(
                            r["offset"],
                            r["chunk_number"],
                            total_chunk_count,
                        ),
                    )

        data = await self._complete_file(total_chunk_count)

        return data



    async def _upload_chunk(
        self,
        offset: int,
        chunk_number: int,
        total_chunk_count: int,
    ) -> dict:
        """
        上传视频分块

        Args:
            offset (int): 分块起始位置

            chunk_number (int): 分块编号

            total_chunk_count (int): 总分块数


        Returns:
            dict: 上传结果和分块信息。
        """
        chunk_event_callback_data = {
            "offset": offset,
            "chunk_number": chunk_number,
            "total_chunk_count": total_chunk_count,
        }

        stream = open(self.file.path, "rb")
        stream.seek(offset)
        chunk = stream.read(self.preupload["chunk_size"])
        stream.close()

        err_return = {
            "ok": False,
            "chunk_number": chunk_number,
            "offset": offset,
        }

        real_chunk_size = len(chunk)

        params = {
            "partNumber": str(chunk_number + 1),
            "uploadId": str(self._upload_id),
            "chunk": str(chunk_number),
            "chunks": str(total_chunk_count),
            "size": str(real_chunk_size),
            "start": str(offset),
            "end": str(offset + real_chunk_size),
            "total": self.file.size,
        }

        ok_return = {
            "ok": True,
            "chunk_number": chunk_number,
            "offset": offset,
        }

        try:
            resp = await self._session.put(
                self._upload_url,
                data=chunk,  # type: ignore
                params=params,
                headers={"x-upos-auth": self.preupload["auth"]},
            )
            if resp.status_code >= 400:
                chunk_event_callback_data["info"] = f"Status {resp.status_code}"
                return err_return

            data = resp.text

            if data != "MULTIPART_PUT_SUCCESS" and data != "":
                chunk_event_callback_data["info"] = "分块上传失败"
                return err_return

        except Exception as e:
            chunk_event_callback_data["info"] = str(e)
            return err_return

        return ok_return

    async def _complete_file(self, chunks: int) -> dict:
        """
        提交文件

        Args:
            chunks (int): 分块数量

        Returns:
            dict: filename: 该分 P 的标识符，用于最后提交视频。cid: 分 P 的 cid
        """

        data = {
            "parts": list(
                map(lambda x: {"partNumber": x, "eTag": "etag"}, range(1, chunks + 1))
            )
        }

        params = {
            "output": "json",
            "name": os.path.basename(os.path.split(self.file.path)[1]),
            "profile": "ugcfx/bup",
            "uploadId": self._upload_id,
            "biz_id": self.preupload["biz_id"],
        }

        resp = await self._session.post(
            url=self._upload_url,
            data=json.dumps(data),  # type: ignore
            headers={
                "x-upos-auth": self.preupload["auth"],
                "content-type": "application/json; charset=UTF-8",
            },
            params=params,
        )
        if resp.status_code >= 400:
            err = NetworkException(resp.status_code, "状态码错误，提交分 P 失败")
            raise err

        data = json.loads(resp.read())

        if data["OK"] != 1:
            err = ResponseCodeException(-1, f'提交分 P 失败，原因: {data["message"]}')
            raise err