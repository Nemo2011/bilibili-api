"""
bilibili_api.user

笔记相关
"""

import json
from enum import Enum

from .utils.utils import get_api, join
from .utils.Credential import Credential
from .utils.network_httpx import request, get_session
from .exceptions import ArgsException
from .utils.Picture import Picture
from typing import List, Union

API = get_api("note")

class NoteType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"

class Note:
    """
    笔记相关
    """

    def __init__(
        self, 
        cvid: Union[int, None] = None, 
        aid: Union[int, None] = None, 
        note_id: Union[int, None] = None, 
        note_type: NoteType = NoteType.PUBLIC, 
        credential: Union[Credential, None] = None
    ):
        """
        Args:
            type_       (str)                 : 笔记类型 (private, public)
            cvid       (int)                  : 公开笔记 ID
            oid        (int)                  : 稿件 ID（oid_type 为 0 时是 avid）
            note_id    (int)                  : 私有笔记 ID
            credential (Credential, optional) : Credential. Defaults to None.
        """

        # ID 和 type 检查
        if note_type == NoteType.PRIVATE:
            if not aid or not note_id:
                raise ArgsException("私有笔记需要 oid 和 note_id")
            self.set_aid(aid=aid)
            self.set_note_id(note_id=note_id)
        elif type == NoteType.PUBLIC:
            if not cvid:
                raise ArgsException("公开笔记需要 cvid")
            self.set_cvid(cvid=cvid)
        else:
            raise ArgsException("type_ 只能是 public 或 private")

        self.__type = note_type
        
        # 未提供 credential 时初始化该类
        # 私有笔记需要 credential
        self.credential: Credential = Credential() if credential is None else credential

        # 用于存储视频信息，避免接口依赖视频信息时重复调用
        self.__info: Union[dict, None] = None

    def set_aid(self, aid: int) -> None:
        """
        为私有笔记设置稿件 ID

        Args:
            oid (int): 稿件 ID
        """

        self.__oid = aid

    def set_note_id(self, note_id: int) -> None:
        """
        设置私有笔记 ID

        Args:
            note_id (int): 私有笔记 ID
            
        """

        self.__note_id = note_id

    def set_cvid(self, cvid: int) -> None:
        """
        设置 cvid

        Args:
            cvid (int): cvid
        """

        self.__cvid = cvid

    def get_cvid(self) -> int:
        """
        获取 cvid

        Returns:
            str: cvid
        """

        return self.__cvid

    def get_aid(self) -> int:
        """
        获取 oid

        Returns:
            str: oid
        """

        return self.__oid

    def get_note_id(self) -> int:
        """
        获取笔记 ID

        Returns:
            str: 笔记 ID
        """

        return self.__note_id
    
    async def get_info(self) -> dict:
        """
        获取笔记信息

        Returns:
            dict: 笔记信息
        """

        if self.__type == NoteType.PRIVATE:
            return await self.get_private_note_info()
        else:
            return await self.get_public_note_info()

    async def __get_info_cached(self) -> dict:
        """
        获取视频信息，如果已获取过则使用之前获取的信息，没有则重新获取。

        Returns:
            dict: 调用 API 返回的结果。
        """
        if self.__info is None:
            return await self.get_info()
        return self.__info

    async def get_private_note_info(self) -> dict:
        """
        获取私有笔记信息。

        Returns:
            dict: 调用 API 返回的结果。
        """

        assert self.__type == NoteType.PRIVATE

        api = API["private"]["detail"]
        # oid 为 0 时指 avid
        params = {"oid": self.get_aid(), "note_id": self.get_note_id(), "oid_type": 0}
        resp = await request(
            "GET", api["url"], params=params, credential=self.credential
        )
        # 存入 self.__info 中以备后续调用
        self.__info = resp
        return resp
        
    async def get_public_note_info(self) -> dict:
        """
        获取公有笔记信息。

        Returns:
            dict: 调用 API 返回的结果。
        """

        assert self.__type == NoteType.PUBLIC

        api = API["public"]["detail"]
        params = {"cvid": self.get_cvid()}
        resp = await request(
            "GET", api["url"], params=params, credential=self.credential
        )
        # 存入 self.__info 中以备后续调用
        self.__info = resp
        return resp

    async def get_content(self) -> List[dict]:
        """
        获取原始内容

        Returns:
            List[dict]: 原始内容
        """

        return (await self.__get_info_cached())["content"].replace('\n', '\\n')

    async def get_summary(self) -> str:
        """
        获取摘要

        Returns:
            str: 摘要
        """

        return (await self.__get_info_cached())["summary"]

    async def get_images_raw_info(self) -> List["dict"]:
        """
        获取笔记所有图片原始信息

        Returns:
            list: 图片信息
        """

        result = []
        content = await self.get_content()
        for line in content:
            if type(line["insert"]) == dict:
                if 'imageUpload' in line["insert"]:
                    img_info = line["insert"]["imageUpload"]
                    result.append(img_info)
        return result

    async def get_images(self) -> List["Picture"]:
        """
        获取笔记所有图片并转为 Picture 类

        Returns:
            list: 图片信息
        """

        result = []
        images_raw_info = await self.get_images_raw_info()
        for image in images_raw_info:
            result.append(Picture().from_url(url=f'https:{image["url"]}'))
        return result

    async def get_title(self) -> str:
        """
        获取标题

        Returns:
            str: 标题
        """

        return (await self.__get_info_cached())["title"]

    async def get_author(self) -> dict:
        """
        获取作者信息

        Returns:
            dict: 作者信息
        """

        return (await self.__get_info_cached())["author"]
    
    async def get_video(self) -> dict:
        """
        获取视频信息

        Returns:
            dict: 视频信息
        """

        return (await self.__get_info_cached())["arc"]
