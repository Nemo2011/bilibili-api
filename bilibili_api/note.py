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

from typing import List, Union

API = get_api("note")

class Note:
    '''
    笔记相关
    '''

    def __init__(self, cvid: int = None, oid: int = None, note_id: int = None, type: str = "public", credential: Union[Credential, None] = None):
        '''
        Args:
            type       (str)                 : 笔记类型 (private, public)
            cvid       (int)                 : 公开笔记 ID
            oid        (int)                 : 稿件 ID（oid_type 为 0 时是 avid）
            note_id    (int)                 : 私有笔记 ID
            credential (Credential, optional): Credential. Defaults to None.
        '''
        # type 检查
        if type not in ["public", "private"]:
            raise ArgsException("type 只能是 public 或 private")
        self.type = type
        
        # ID 检查
        if type == "private":
            if not oid or not note_id:
                raise ArgsException("私有笔记需要 oid 和 note_id")
            self.set_oid(oid=oid)
            self.set_note_id(note_id=note_id)
        else:
            if not cvid:
                raise ArgsException("公开笔记需要 cvid")
            self.set_cvid(cvid=cvid)
        
        # 未提供 credential 时初始化该类
        # 私有笔记需要 credential
        self.credential: Credential = Credential() if credential is None else credential

        # 用于存储视频信息，避免接口依赖视频信息时重复调用
        self.__info: Union[dict, None] = None

    def set_oid(self, oid: int) -> None:
        '''
        为私有笔记设置稿件 ID

        Args:
            oid (int): 稿件 ID
        '''

        self.__oid = oid

    def set_note_id(self, note_id: int) -> None:
        '''
        设置私有笔记 ID

        Args:
            note_id (int): 私有笔记 ID
        '''

        self.__note_id = note_id

    def set_cvid(self, cvid: int) -> None:
        '''
        设置 cvid

        Args:
            cvid (int): cvid
        '''

        self.__cvid = cvid

    def get_cvid(self) -> str:
        '''
        获取 cvid

        Returns:
            str: cvid
        '''

        return self.__cvid

    def get_oid(self) -> str:
        '''
        获取 oid

        Returns:
            str: oid
        '''

        return self.__oid

    def get_note_id(self) -> str:
        '''
        获取笔记 ID

        Returns:
            str: 笔记 ID
        '''

        return self.__note_id
    
    async def get_info(self) -> dict:
        '''
        获取笔记信息

        Returns:
            dict: 笔记信息
        '''

        if self.type == "private":
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
        api = API["private"]["detail"]
        # oid 为 0 时指 avid
        params = {"oid": self.get_oid(), "note_id": self.get_note_id(), "oid_type": 0}
        resp = await request(
            "GET", api["url"], params=params, credential=self.credential
        )
        # 存入 self.__info 中以备后续调用
        self.__info = resp
        return resp
        
    async def get_public_note_info(self) -> dict:
        """
        获取私有笔记信息。

        Returns:
            dict: 调用 API 返回的结果。
        """
        api = API["public"]["detail"]
        params = {"cvid": self.get_cvid()}
        resp = await request(
            "GET", api["url"], params=params, credential=self.credential
        )
        # 存入 self.__info 中以备后续调用
        self.__info = resp
        return resp

    async def get_content(self) -> list:
        '''
        获取原始内容

        Returns:
            List[dict]: 原始内容
        '''

        return json.loads((await self.__get_info_cached())["content"].replace('\n', '\\n'))

    async def get_summary(self) -> str:
        '''
        获取摘要

        Returns:
            str: 摘要
        '''

        return (await self.__get_info_cached())["summary"]

    async def get_images(self) -> list:
        '''
        获取图片

        Returns:
            list: 图片信息
        '''
        result = []
        content = await self.get_content()
        for line in content:
            if type(line["insert"]) == dict:
                if 'imageUpload' in line["insert"]:
                    result.append(line["insert"]["imageUpload"])
        return result

    async def get_title(self) -> str:
        '''
        获取标题

        Returns:
            str: 标题
        '''

        return (await self.__get_info_cached())["title"]

    async def get_author(self) -> dict:
        '''
        获取作者信息

        Returns:
            dict: 作者信息
        '''

        return (await self.__get_info_cached())["author"]
    
    async def get_video(self) -> dict:
        '''
        获取视频信息

        Returns:
            dict: 视频信息
        '''

        return (await self.__get_info_cached())["arc"]
