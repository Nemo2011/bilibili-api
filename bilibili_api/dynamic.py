"""
bilibili_api.dynamic

动态相关
"""

import os
import re
import sys
import json
import asyncio
from enum import Enum
from datetime import datetime
from typing import Any, List, Tuple, Union, Optional

import httpx

from .utils import utils
from .utils.sync import sync
from .utils.picture import Picture
from . import user, vote, exceptions
from .utils.credential import Credential
from .utils.network import Api
from .exceptions.DynamicExceedImagesException import DynamicExceedImagesException

API = utils.get_api("dynamic")


class DynamicType(Enum):
    """
    动态类型

    + ALL: 所有动态
    + ANIME: 追番追剧
    + ARTICLE: 文章
    + VIDEO: 视频投稿
    """

    ALL = "all"
    ANIME = "pgc"
    ARTICLE = "article"
    VIDEO = "video"


class SendDynmaicType(Enum):
    """
    发送动态类型
    scene 参数

    + TEXT: 纯文本
    + IMAGE: 图片
    """

    TEXT = 1
    IMAGE = 2


class DynmaicContentType(Enum):
    """
    动态内容类型

    + TEXT: 文本
    + EMOJI: 表情
    + AT: @User
    + VOTE: 投票
    """

    TEXT = 1
    EMOJI = 9
    AT = 2
    VOTE = 4


async def _parse_at(text: str) -> Tuple[str, str, str]:
    """
    @人格式：“@用户名 ”(注意最后有空格）

    Args:
        text (str): 原始文本

    Returns:
        tuple(str, str(int[]), str(dict)): 替换后文本，解析出艾特的 UID 列表，AT 数据
    """
    text += " "
    pattern = re.compile(r"(?<=@).*?(?=\s)")
    match_result = re.finditer(pattern, text)
    uid_list = []
    names = []
    for match in match_result:
        uname = match.group()
        try:
            uid = (await user.name2uid(uname))["uid_list"][0]["uid"]
        except KeyError:
            # 没有此用户
            continue

        uid_list.append(str(uid))
        names.append(uname + " ")
    at_uids = ",".join(uid_list)
    ctrl = []
    last_index = 0
    for i, name in enumerate(names):
        index = text.index(f"@{name}", last_index)
        last_index = index + 1
        length = 2 + len(name)
        ctrl.append(
            {"location": index, "type": 1, "length": length, "data": int(uid_list[i])}
        )

    return text, at_uids, json.dumps(ctrl, ensure_ascii=False)


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


async def _get_draw_data(
    text: str, images: List[Picture], credential: Credential
) -> dict:
    """
    获取图片动态请求参数，将会自动上传图片

    Args:
        text   (str)          : 文本内容

        images (List[Picture]): 图片流
    """
    new_text, at_uids, ctrl = await _parse_at(text)
    images_info = await asyncio.gather(
        *[upload_image(stream, credential) for stream in images]
    )

    def transformPicInfo(image: dict):
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


async def upload_image(
    image: Picture, credential: Credential, data: dict = None
) -> dict:
    """
    上传动态图片

    Args:
        image (Picture)   : 图片流. 有格式要求.

        credential (Credential): 凭据

        data (dict): 自定义请求体
    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    api = API["send"]["upload_img"]
    raw = image.content

    if data is None:
        data = {"biz": "new_dyn", "category": "daily"}

    files = {"file_up": raw}
    return_info = (
        await Api(**api, credential=credential).update_data(**data).request(files=files)
    )
    return return_info


class BuildDynmaic:
    """
    构建动态内容. 提供两种 API.

    - 1. 链式调用构建

    ``` python
    BuildDynamic.empty().add_plain_text("114514").add_image(Picture.from_url("https://www.bilibili.com/favicon.ico"))
    ```

    - 2. 参数构建

    ``` python
    BuildDynamic.create_by_args(text="114514", topic_id=114514)
    ```
    """

    def __init__(self) -> None:
        """
        构建动态内容
        """
        self.contents: list = []
        self.pics: List[Picture] = []
        self.attach_card: Optional[dict] = None
        self.topic: Optional[dict] = None
        self.options: dict = {}
        self.time: Optional[datetime] = None

    @staticmethod
    def empty():
        """
        新建空的动态以链式逐步构建
        """
        return BuildDynmaic()

    @staticmethod
    def create_by_args(
        text: str = "",
        pics: List[Picture] = [],
        topic_id: int = -1,
        vote_id: int = -1,
        live_reserve_id: int = -1,
        send_time: Union[datetime, None] = None,
    ):
        """
        通过参数构建动态

        Args:
            text            (str            , optional): 动态文字. Defaults to "".

            pics            (List[Picture]  , optional): 动态图片列表. Defaults to [].

            topic_id        (int            , optional): 动态话题 id. Defaults to -1.

            vote_id         (int            , optional): 动态中的投票的 id. 将放在整个动态的最后面. Defaults to -1.

            live_reserve_id (int            , optional): 直播预约 oid. 通过 `live.create_live_reserve` 获取. Defaults to -1.

            send_time       (datetime | None, optional): 发送时间. Defaults to None.
        """
        dyn = BuildDynmaic()
        dyn.add_text(text)
        dyn.add_image(pics)
        if topic_id != -1:
            dyn.set_topic(topic_id)
        if vote_id != -1:
            dyn.add_vote(vote.Vote(vote_id=vote_id))
        if live_reserve_id != -1:
            dyn.set_attach_card(live_reserve_id)
        if send_time != None:
            dyn.set_send_time(send_time)
        return dyn

    def add_plain_text(self, text: str) -> "BuildDynmaic":
        """
        添加纯文本

        Args:
            text (str): 文本内容
        """
        self.contents.append(
            {"biz_id": "", "type": DynmaicContentType.TEXT.value, "raw_text": text}
        )
        return self

    def add_at(self, uid: Union[int, user.User]) -> "BuildDynmaic":
        """
        添加@用户，支持传入 User 类或 UID

        Args:
            uid (Union[int, user.User]): 用户ID
        """
        if isinstance(uid, user.User):
            uid = uid.__uid
        name = httpx.get(
            "https://api.bilibili.com/x/space/acc/info",
            params={"mid": uid},
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://www.bilibili.com",
            },
        ).json()["data"]["name"]
        self.contents.append(
            {"biz_id": uid, "type": DynmaicContentType.AT.value, "raw_text": f"@{name}"}
        )
        return self

    def add_emoji(self, emoji_id: int) -> "BuildDynmaic":
        """
        添加表情

        Args:
            emoji_id (int): 表情ID
        """
        with open(
            os.path.join(os.path.dirname(__file__), "data/emote.json"), encoding="UTF-8"
        ) as f:
            emote_info = json.load(f)
        if str(emoji_id) not in emote_info:
            raise ValueError("不存在此表情")
        self.contents.append(
            {
                "biz_id": "",
                "type": DynmaicContentType.EMOJI.value,
                "raw_text": emote_info[str(emoji_id)],
            }
        )
        return self

    def add_vote(self, vote: vote.Vote) -> "BuildDynmaic":
        vote_info = httpx.get(
            "https://api.vc.bilibili.com/vote_svr/v1/vote_svr/vote_info?vote_id={}".format(
                vote.get_vote_id()
            )
        ).json()
        title = vote_info["data"]["info"]["title"]
        self.contents.append(
            {
                "biz_id": str(vote.get_vote_id()),
                "type": DynmaicContentType.VOTE.value,
                "raw_text": title,
            }
        )
        return self

    def add_image(self, image: Union[List[Picture], Picture]) -> "BuildDynmaic":
        """
        添加图片

        Args:
            image (Picture | List[Picture]): 图片类
        """
        if isinstance(image, Picture):
            image = [image]
        self.pics += image
        return self

    def add_text(self, text: str) -> "BuildDynmaic":
        """
        添加文本 (可包括 at, 表情包)

        Args:
            text (str): 文本内容
        """

        def _get_ats(text: str) -> List:
            text += " "
            pattern = re.compile(r"(?<=@).*?(?=\s)")
            match_result = re.finditer(pattern, text)
            uid_list = []
            names = []
            for match in match_result:
                uname = match.group()
                try:
                    name_to_uid_resp = httpx.get(
                        "https://api.vc.bilibili.com/dynamic_mix/v1/dynamic_mix/name_to_uid?",
                        params={"names": uname},
                    )
                    uid = name_to_uid_resp.json()["data"]["uid_list"][0]["uid"]
                except KeyError:
                    # 没有此用户
                    continue
                uid_list.append(str(uid))
                names.append(uname)
            data = []
            last_index = 0
            for i, name in enumerate(names):
                index = text.index(f"@{name}", last_index)
                last_index = index + 1
                length = 2 + len(name)
                data.append(
                    {
                        "location": index,
                        "length": length,
                        "text": f"@{name} ",
                        "type": "at",
                        "uid": uid_list[i],
                    }
                )
            return data

        def _get_emojis(text: str) -> List:
            with open(
                os.path.join(os.path.dirname(__file__), "data/emote.json"),
                encoding="UTF-8",
            ) as f:
                emote_info = json.load(f)
            all_emojis = []
            for key, item in emote_info.items():
                all_emojis.append(item)
            pattern = re.compile(r"(?<=\[).*?(?=\])")
            match_result = re.finditer(pattern, text)
            emotes = []
            for match in match_result:
                emote = match.group(0)
                if f"[{emote}]" not in all_emojis:
                    continue
                emotes.append(f"[{emote}]")
            data = []
            last_index = 0
            for i, emoji in enumerate(emotes):
                index = text.index(emoji, last_index)
                last_index = index + 1
                length = len(emoji)
                data.append(
                    {
                        "location": index,
                        "length": length,
                        "text": emoji,
                        "type": "emoji",
                    }
                )
            return data

        all_at_and_emoji = _get_ats(text) + _get_emojis(text)

        def split_text_to_plain_at_and_emoji(text: str, at_and_emoji: List):
            def base_split(texts: List[str], at_and_emoji: List, last_length: int):
                if len(at_and_emoji) == 0:
                    return texts
                last_piece_of_text = texts.pop(-1)
                next_at_or_emoji = at_and_emoji.pop(0)
                texts += [
                    last_piece_of_text[: next_at_or_emoji["location"] - last_length],
                    next_at_or_emoji,
                    last_piece_of_text[
                        next_at_or_emoji["location"]
                        + next_at_or_emoji["length"]
                        - last_length :
                    ],
                ]
                last_length += (
                    next_at_or_emoji["length"]
                    + next_at_or_emoji["location"]
                    - last_length
                )
                return base_split(texts, at_and_emoji, last_length)

            old_recursion_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(100000)
            all_pieces = base_split([text], at_and_emoji, 0)
            sys.setrecursionlimit(old_recursion_limit)
            return all_pieces

        all_pieces = split_text_to_plain_at_and_emoji(text, all_at_and_emoji)
        for piece in all_pieces:
            if isinstance(piece, str):
                self.add_plain_text(piece)
            elif piece["type"] == "at":
                self.contents.append(
                    {
                        "biz_id": piece["uid"],
                        "type": DynmaicContentType.AT.value,
                        "raw_text": piece["text"],
                    }
                )
            else:
                self.contents.append(
                    {
                        "biz_id": "",
                        "type": DynmaicContentType.EMOJI.value,
                        "raw_text": piece["text"],
                    }
                )
        return self

    def set_attach_card(self, oid: int) -> "BuildDynmaic":
        """
        设置直播预约

        在 live.create_live_reserve 中获取 oid

        Args:
            oid (int): 卡片oid
        """
        self.attach_card = {
            "type": 14,
            "biz_id": oid,
            "reserve_source": 1,  # 疑似0为视频预告但没法验证...
            "reserve_lottery": 0,
        }
        return self

    def set_topic(self, topic_id: int) -> "BuildDynmaic":
        """
        设置话题

        Args:
            topic_id (int): 话题ID
        """
        self.topic = {"id": topic_id}
        return self

    def set_options(
        self, up_choose_comment: bool = False, close_comment: bool = False
    ) -> "BuildDynmaic":
        """
        设置选项

        Args:
            up_choose_comment	(bool): 	精选评论flag

            close_comment	    (bool): 	关闭评论flag
        """
        if up_choose_comment:
            self.options["up_choose_comment"] = 1
        if close_comment:
            self.options["close_comment"] = 1
        return self

    def set_send_time(self, time: datetime):
        """
        设置发送时间

        Args:
            time (datetime): 发送时间
        """
        self.time = time
        return self

    def get_dynamic_type(self) -> SendDynmaicType:
        if len(self.pics) != 0:
            return SendDynmaicType.IMAGE
        return SendDynmaicType.TEXT

    def get_contents(self) -> list:
        return self.contents

    def get_pics(self) -> list:
        return self.pics

    def get_attach_card(self) -> Optional[dict]:
        return self.attach_card

    def get_topic(self) -> Optional[dict]:
        return self.topic

    def get_options(self) -> dict:
        return self.options


async def send_dynamic(info: BuildDynmaic, credential: Credential):
    """
    发送动态

    Args:
        info (BuildDynmaic): 动态内容

        credential (Credential): 凭据

    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    pic_data = []
    for image in info.pics:
        await image.upload_file(credential)
        pic_data.append(
            {"img_src": image.url, "img_width": image.width, "img_height": image.height}
        )

    async def schedule(type_: int):
        api = API["send"]["schedule"]
        text = "".join(
            [part["raw_text"] for part in info.contents if part["type"] != 4]
        )
        send_time = info.time
        if len(info.pics) > 0:
            # 画册动态
            request_data = await _get_draw_data(text, info.pics, credential)  # type: ignore
            request_data.pop("setting")
        else:
            # 文字动态
            request_data = await _get_text_data(text)
        data = {
            "type": type_,
            "publish_time": int(send_time.timestamp()),  # type: ignore
            "request": json.dumps(request_data, ensure_ascii=False),
        }
        return await Api(**api, credential=credential).update_data(**data).result

    if info.time != None:
        return await schedule(2 if len(info.pics) == 0 else 4)
    api = API["send"]["instant"]
    data = {
        "dyn_req": {
            "content": {"contents": info.get_contents()},  # 必要参数
            "scene": info.get_dynamic_type().value,  # 必要参数
            "meta": {
                "app_meta": {"from": "create.dynamic.web", "mobi_app": "web"},
            },
        }
    }
    if len(info.get_pics()) != 0:
        data["dyn_req"]["pics"] = pic_data
    if info.get_topic() is not None:
        data["dyn_req"]["topic"] = info.get_topic()
    if len(info.get_options()) > 0:
        data["dyn_req"]["option"] = info.get_options()
    if info.get_attach_card() is not None:
        data["dyn_req"]["attach_card"] = {}
        data["dyn_req"]["attach_card"]["common_card"] = info.get_attach_card()
    else:
        data["dyn_req"]["attach_card"] = None
    params = {"csrf": credential.bili_jct}
    send_result = (
        await Api(**api, credential=credential, json_body=True)
        .update_data(**data)
        .update_params(**params)
        .result
    )
    return send_result


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
    return await Api(**api, credential=credential).result


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
    return await Api(**api, credential=credential).update_data(**data).result


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
    return await Api(**api, credential=credential).update_data(**data).result


class Dynamic:
    """
    动态类

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(
        self, dynamic_id: int, credential: Union[Credential, None] = None
    ) -> None:
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
        params = {
            "id": self.__dynamic_id,
            "timezone_offset": -480,
            "features": "itemOpusStyle",
        }
        data = (
            await Api(**api, credential=self.credential).update_params(**params).result
        )
        return data

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
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
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
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
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
        return await Api(**api, credential=self.credential).update_data(**data).result

    async def delete(self) -> dict:
        """
        删除动态

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()

        api = API["operate"]["delete"]
        data = {"dynamic_id": self.__dynamic_id}
        return await Api(**api, credential=self.credential).update_data(**data).result

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
        return await Api(**api, credential=self.credential).update_data(**data).result


async def get_new_dynamic_users(credential: Union[Credential, None] = None) -> dict:
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
    return await Api(**api, credential=credential).result


async def get_live_users(
    size: int = 10, credential: Union[Credential, None] = None
) -> dict:
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
    params = {"size": size}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_dynamic_page_UPs_info(credential: Credential) -> dict:
    """
    获取动态页 UP 主列表

    Args:
        credential (Credential): 凭据类.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["dynamic_page_UPs_info"]
    return await Api(**api, credential=credential).result


async def get_dynamic_page_info(
    credential: Credential,
    _type: Optional[DynamicType] = None,
    host_mid: Optional[int] = None,
    pn: int = 1,
    offset: Optional[int] = None,
) -> List[Dynamic]:
    """
    获取动态页动态信息

    获取全部动态或者相应类型需传入 _type

    获取指定 UP 主动态需传入 host_mid

    Args:
        credential (Credential): 凭据类.

        _type      (DynamicType, optional): 动态类型. Defaults to DynamicType.ALL.

        host_mid   (int, optional): 获取对应 UP 主动态的 mid. Defaults to None.

        pn         (int, optional): 页码. Defaults to 1.

        offset     (int, optional): 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to None.

    Returns:
        list[Dynamic]: 动态类列表
    """

    api = API["info"]["dynamic_page_info"]
    params = {
        "timezone_offset": -480,
        "features": "itemOpusStyle",
        "offset": offset,
        "page": pn,
    }
    if _type:  # 全部动态
        params["type"] = _type.value
    elif host_mid:  # 指定 UP 主动态
        params["host_mid"] = host_mid

    dynmaic_data = (
        await Api(**api, credential=credential).update_params(**params).result
    )
    return [
        Dynamic(dynamic_id=int(dynamic["id_str"]), credential=credential)
        for dynamic in dynmaic_data["items"]
    ]
