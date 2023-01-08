"""
动态相关
"""

import re
import json
import datetime
import asyncio
from typing import Any, List, Tuple, Union
import io

from .exceptions.DynamicExceedImagesException import DynamicExceedImagesException
from .utils.network_httpx import request
from .utils.Credential import Credential
from . import user, exceptions
from .utils import utils
from .utils.Picture import Picture

API = utils.get_api("dynamic")


async def _parse_at(text: str) -> Tuple[str, str, str]:
    """
    @人格式：“@UID ”(注意最后有空格）

    Args:
        text (str): 原始文本

    Returns:
        tuple(str, str(int[]), str(dict)): 替换后文本，解析出艾特的 UID 列表，AT 数据
    """
    pattern = re.compile(r"(?<=@)\d*?(?=\s)")
    match_result = re.finditer(pattern, text)
    uid_list = []
    names = []
    new_text = text
    for match in match_result:
        uid = match.group()
        try:
            u = user.User(int(uid))
            user_info = await u.get_user_info()

        except exceptions.ResponseCodeException as e:
            if e.code == -404:
                raise exceptions.ResponseCodeException(-404, f"用户 uid={uid} 不存在")
            else:
                raise e

        name = user_info["name"]
        uid_list.append(uid)
        names.append(name)
        new_text = new_text.replace(f"@{uid} ", f"@{name} ")
    at_uids = ",".join(uid_list)
    ctrl = []

    for i, name in enumerate(names):
        index = new_text.index(f"@{name}")
        length = 2 + len(name)
        ctrl.append(
            {"location": index, "type": 1, "length": length, "data": int(uid_list[i])}
        )

    return new_text, at_uids, json.dumps(ctrl, ensure_ascii=False)


async def _get_text_data(text: str) -> dict:
    """
    获取文本动态请求参数

    Args:
        text (str): 文本内容

    Returns:
        dict: 文本动态请求数据
    """
    new_text, at_uids, ctrl = await _parse_at(text)
    data = {
        "dynamic_id": 0,
        "type": 4,
        "rid": 0,
        "content": new_text,
        "extension": '{"emoji_type":1}',
        "at_uids": at_uids,
        "ctrl": ctrl,
    }
    return data


async def upload_image(image: Picture, credential: Credential) -> dict:
    """
    上传动态图片

    Args:
        image_stream (Picture)   : 图片流
        credential   (Credential): 凭据

    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    api = API["send"]["upload_img"]
    data = {"biz": "draw", "category": "daily"}

    raw = image.content

    return await request(
        "POST",
        url=api["url"],
        data=data,
        files={"file_up": raw},
        credential=credential,
    )


async def _get_draw_data(
    text: str, image_streams: List[Picture], credential: Credential
) -> dict:
    """
    获取图片动态请求参数，将会自动上传图片

    Args:
        text (str): 文本内容
        image_streams (List[Picture]): 图片流
    """
    new_text, at_uids, ctrl = await _parse_at(text)
    images_info = await asyncio.gather(
        *[upload_image(stream, credential) for stream in image_streams]
    )

    def transformPicInfo(image):
        """
        转换图片信息

        Args:
            image ([type]): [description]

        Returns:
            [type]: [description]
        """
        return {
            "img_src": image["image_url"],
            "img_width": image["image_width"],
            "img_height": image["image_height"],
        }

    pictures = list(map(transformPicInfo, images_info))
    data = {
        "biz": 3,
        "category": 3,
        "type": 0,
        "pictures": json.dumps(pictures),
        "title": "",
        "tags": "",
        "description": new_text,
        "content": new_text,
        "from": "create.dynamic.web",
        "up_choose_comment": 0,
        "extension": json.dumps(
            {"emoji_type": 1, "from": {"emoji_type": 1}, "flag_cfg": {}}
        ),
        "at_uids": at_uids,
        "at_control": ctrl,
        "setting": json.dumps({"copy_forbidden": 0, "cachedTime": 0}),
    }
    return data


async def send_dynamic(
    text: str,
    image_streams: Union[List[Picture], None] = None,
    send_time: Union[datetime.datetime, None] = None,
    credential: Union[Credential, None] = None,
):
    """
    自动判断动态类型选择合适的 API 并发送动态

    如需 @ 人，请使用格式 "@UID "，注意最后有一个空格

    Args:
        text          (str)                              : 动态文本
        image_streams (List[Picture] | None, optional)   : 图片流列表. Defaults to None.
        send_time     (datetime.datetime | None, optional)      : 定时动态发送时间. Defaults to None.
        credential    (Credential | None, optional)             : 凭据. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """

    if credential is None:
        credential = Credential()

    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    async def instant_text():
        api = API["send"]["instant_text"]
        data = await _get_text_data(text)
        return await request("POST", api["url"], data=data, credential=credential)

    async def instant_draw():
        api = API["send"]["instant_draw"]
        data = await _get_draw_data(text, image_streams, credential) # type: ignore
        return await request("POST", api["url"], data=data, credential=credential)

    async def schedule(type_: int):
        api = API["send"]["schedule"]
        if type_ == 2:
            # 画册动态
            request_data = await _get_draw_data(text, image_streams, credential) # type: ignore
            request_data.pop("setting")
        else:
            # 文字动态
            request_data = await _get_text_data(text)

        data = {
            "type": type_,
            "publish_time": int(send_time.timestamp()), # type: ignore
            "request": json.dumps(request_data, ensure_ascii=False),
        }
        return await request("POST", api["url"], data=data, credential=credential)

    if image_streams is None:
        image_streams = []

    if len(image_streams) == 0:
        # 纯文本动态
        if send_time is None:
            ret = await instant_text()
        else:
            ret = await schedule(2)
    else:
        # 图片动态
        if len(image_streams) > 9:
            raise DynamicExceedImagesException()
        if send_time is None:
            ret = await instant_draw()
        else:
            ret = await schedule(4)
    return ret


# 定时动态操作


async def get_schedules_list(credential: Credential) -> dict:
    """
    获取待发送定时动态列表

    Args:
        credential  (Credential): 凭据

    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()

    api = API["schedule"]["list"]
    return await request("GET", api["url"], credential=credential)


async def send_schedule_now(draft_id: int, credential: Credential) -> dict:
    """
    立即发送定时动态

    Args:
        draft_id (int): 定时动态 ID
        credential  (Credential): 凭据

    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()

    api = API["schedule"]["publish_now"]
    data = {"draft_id": draft_id}
    return await request("POST", api["url"], data=data, credential=credential)


async def delete_schedule(draft_id: int, credential: Credential) -> dict:
    """
    删除定时动态

    Args:
        draft_id (int): 定时动态 ID
        credential  (Credential): 凭据
    
    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()

    api = API["schedule"]["delete"]
    data = {"draft_id": draft_id}
    return await request("POST", api["url"], data=data, credential=credential)


class Dynamic:
    """
    动态类

    Attributes: 
        credential (Credential): 凭据类
    """

    def __init__(self, dynamic_id: int, credential: Union[Credential, None] = None):
        """
        Args:
            dynamic_id (int)                        : 动态 ID
            credential (Credential | None, optional): 凭据类. Defaults to None.
        """
        self.__dynamic_id = dynamic_id
        self.credential = credential if credential is not None else Credential()

    def get_dynamic_id(self) -> int:
        return self.__dynamic_id

    async def get_info(self) -> dict:
        """
        获取动态信息

        Returns:
            dict: 调用 API 返回的结果
        """

        api = API["info"]["detail"]
        params = {"dynamic_id": self.__dynamic_id}
        data = await request(
            "GET", api["url"], params=params, credential=self.credential
        )

        data["card"]["card"] = json.loads(data["card"]["card"])
        data["card"]["extend_json"] = json.loads(data["card"]["extend_json"])
        return data["card"]

    async def get_reposts(self, offset: str = "0") -> dict:
        """
        获取动态转发列表

        Args:
            offset (str, optional): 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to "0"

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["repost"]
        params: dict[str, Any] = {"dynamic_id": self.__dynamic_id}
        if offset != "0":
            params["offset"] = offset
        return await request(
            "GET", api["url"], params=params, credential=self.credential
        )

    async def get_likes(self, pn: int = 1, ps: int = 30) -> dict:
        """
        获取动态点赞列表

        Args:
            pn (int, optional): 页码，defaults to 1
            ps (int, optional): 每页大小，defaults to 30

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["likes"]
        params = {"dynamic_id": self.__dynamic_id, "pn": pn, "ps": ps}
        return await request(
            "GET", api["url"], params=params, credential=self.credential
        )

    async def set_like(self, status: bool = True) -> dict:
        """
        设置动态点赞状态

        Args:
            status (bool, optional): 点赞状态. Defaults to True.
        
        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["like"]

        user_info = await user.get_self_info(credential=self.credential)

        self_uid = user_info["mid"]
        data = {
            "dynamic_id": self.__dynamic_id,
            "up": 1 if status else 2,
            "uid": self_uid,
        }
        return await request("POST", api["url"], data=data, credential=self.credential)

    async def delete(self) -> dict:
        """
        删除动态

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()

        api = API["operate"]["delete"]
        data = {"dynamic_id": self.__dynamic_id}
        return await request("POST", api["url"], data=data, credential=self.credential)

    async def repost(self, text: str = "转发动态") -> dict:
        """
        转发动态

        Args:
            text (str, optional): 转发动态时的文本内容. Defaults to "转发动态"
        
        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()

        api = API["operate"]["repost"]
        data = await _get_text_data(text)
        data["dynamic_id"] = self.__dynamic_id
        return await request("POST", api["url"], data=data, credential=self.credential)


async def get_new_dynamic_users(credential: Union[Credential, None] = None):
    """
    获取更新动态的关注者

    Args:
        credential (Credential | None): 凭据类. Defaults to None. 

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    credential.raise_for_no_sessdata()
    api = API["info"]["attention_new_dynamic"]
    return await request("GET", api["url"], credential = credential)


async def get_live_users(size: int = 10, credential: Union[Credential, None] = None):
    """
    获取正在直播的关注者

    Args:
        size       (int)       : 获取的数据数量. Defaults to 10. 
        credential (Credential | None): 凭据类. Defaults to None. 

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    credential.raise_for_no_sessdata()
    api = API["info"]["attention_live"]
    params = {
        "size": size
    }
    return await request("GET", api["url"], params = params, credential = credential)
