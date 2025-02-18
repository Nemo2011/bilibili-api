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

import yaml

from .utils import utils
from .utils.picture import Picture
from . import user, vote
from .utils.network import Api, Credential
from .exceptions import ArgsException
from .article import Article
from .opus import Opus
from .utils import cache_pool

API = utils.get_api("dynamic")
API_opus = utils.get_api("opus")
raise_for_statement = utils.raise_for_statement

uid2uname = {}
uname2uid = {}


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


class SendDynamicType(Enum):
    """
    发送动态类型
    scene 参数

    + TEXT: 纯文本
    + IMAGE: 图片
    """

    TEXT = 1
    IMAGE = 2


class DynamicContentType(Enum):
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


async def _name2uid(uname: str, credential: Credential) -> int:
    global uname2uid
    if uname2uid.get(uname) is None:
        resp = (await user.name2uid(uname, credential=credential))["uid_list"]
        if len(resp) == 0:
            return 0
        if resp[0]["name"] != uname:
            return 0
        uname2uid[uname] = resp[0]["uid"]
    return uname2uid[uname]


async def _uid2name(uid: int, credential: Credential) -> str:
    global uid2uname
    if uid2uname.get(uid) is None:
        uid2uname[uid] = (await user.User(uid, credential=credential).get_user_info())[
            "name"
        ]
    return uid2uname[uid]


async def _parse_at(text: str, credential: Credential) -> Tuple[str, str, str]:
    """
    @人格式：“@用户名 ”(注意最后有空格）

    Args:
        text       (str)       : 原始文本
        credential (Credential): 凭据类，必须提供

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
        uid = await _name2uid(uname, credential=credential)
        if uid == 0:
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


async def _get_text_data(text: str, credential: Credential) -> dict:
    """
    获取文本动态请求参数

    Args:
        text       (str)       : 文本内容
        credential (Credential): 凭据类。必须提供。

    Returns:
        dict: 文本动态请求数据
    """
    new_text, at_uids, ctrl = await _parse_at(text, credential=credential)
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

    if data is None:
        data = {"biz": "new_dyn", "category": "daily"}

    files = {"file_up": image._to_biliapifile()}
    return_info = (
        await Api(**api, credential=credential)
        .update_data(**data)
        .update_files(**files)
        .result
    )
    return return_info


class BuildDynamic:
    """
    构建动态内容. 提供两种 API.

    - 1. 链式调用构建

    ``` python
    BuildDynamic.empty().add_plain_text("114514").add_image(await Picture.load_url("https://www.bilibili.com/favicon.ico"))
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
        return BuildDynamic()

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
        dyn = BuildDynamic()
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

    def add_plain_text(self, text: str) -> "BuildDynamic":
        """
        添加纯文本

        Args:
            text (str): 文本内容
        """
        self.contents.append(
            {"biz_id": "", "type": DynamicContentType.TEXT.value, "raw_text": text}
        )
        return self

    def add_at(self, uid: int = 0, uname: str = "") -> "BuildDynamic":
        """
        添加@用户，支持传入 用户名或 UID

        Args:
            uid   (int): 用户ID
            uname (str): 用户名称. Defaults to "".
        """
        self.contents.append(
            {
                "biz_id": uid,
                "type": DynamicContentType.AT.value,
                "raw_text": f"@{uname}",
            }
        )
        return self

    def add_emoji(self, emoji: str) -> "BuildDynamic":
        """
        添加表情

        Args:
            emoji (str): 表情文字
        """
        self.contents.append(
            {
                "biz_id": "",
                "type": DynamicContentType.EMOJI.value,
                "raw_text": emoji,
            }
        )
        return self

    def add_vote(self, vote_id: int) -> "BuildDynamic":
        """
        添加投票

        Args:
            vote_id (int): 投票对象
        """
        self.contents.append(
            {
                "biz_id": vote_id,
                "type": DynamicContentType.VOTE.value,
                "raw_text": "",
            }
        )
        return self

    def add_image(self, image: Union[List[Picture], Picture]) -> "BuildDynamic":
        """
        添加图片

        Args:
            image (Picture | List[Picture]): 图片类
        """
        if isinstance(image, Picture):
            image = [image]
        self.pics += image
        return self

    def add_text(self, text: str) -> "BuildDynamic":
        """
        添加文本 (可包括 at, 表情包)

        Args:
            text (str): 文本内容
        """

        def _get_ats(text: str) -> List:
            text += " "
            pattern = re.compile(r"(?<=@).*?(?=\s)")
            match_result = re.finditer(pattern, text)
            names = []
            for match in match_result:
                names.append(match.group())
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
                        "text": f"@{name}",
                        "type": "at",
                        "uid": 0,
                    }
                )
            return data

        def _get_emojis(text: str) -> List:
            pattern = re.compile(r"(?<=\[).*?(?=\])")
            match_result = re.finditer(pattern, text)
            emotes = []
            for match in match_result:
                emote = match.group(0)
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
                        "type": DynamicContentType.AT.value,
                        "raw_text": piece["text"],
                    }
                )
            else:
                self.contents.append(
                    {
                        "biz_id": "",
                        "type": DynamicContentType.EMOJI.value,
                        "raw_text": piece["text"],
                    }
                )
        return self

    def set_attach_card(self, oid: int) -> "BuildDynamic":
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

    def set_topic(self, topic_id: int) -> "BuildDynamic":
        """
        设置话题

        Args:
            topic_id (int): 话题ID
        """
        self.topic = {"id": topic_id}
        return self

    def set_options(
        self, up_choose_comment: bool = False, close_comment: bool = False
    ) -> "BuildDynamic":
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

    def get_dynamic_type(self) -> SendDynamicType:
        """
        获取动态类型

        Returns:
            SendDynamicType: 动态类型
        """
        if len(self.pics) != 0:
            return SendDynamicType.IMAGE
        return SendDynamicType.TEXT

    async def get_contents(self, credential: Credential) -> list:
        """
        获取动态内容，通过请求完善字段后返回

        Args:
            credential (Credential): 凭据类。必需。

        Returns:
            list: 动态内容
        """
        contents = self.contents
        for idx, content in enumerate(contents):
            if content["type"] == DynamicContentType.AT.value:
                if content["biz_id"] == 0:
                    if content["raw_text"] == "@":
                        contents[idx] = {
                            "biz_id": "",
                            "type": DynamicContentType.EMOJI.value,
                            "raw_text": "@",
                        }
                        continue
                    uid = await _name2uid(content["raw_text"][1:], credential)
                    if uid == 0:
                        contents[idx] = {
                            "biz_id": "",
                            "type": DynamicContentType.TEXT.value,
                            "raw_text": content["raw_text"],
                        }
                    else:
                        contents[idx]["biz_id"] = str(uid)
                elif content["raw_text"] == "@":
                    contents[idx]["raw_text"] = "@" + await _uid2name(
                        content["biz_id"], credential=credential
                    )
            if content["type"] == DynamicContentType.VOTE.value:
                contents[idx]["raw_text"] = (
                    await vote.Vote(vote_id=content["biz_id"]).get_info()
                )["info"]["title"]
        for idx, content in enumerate(contents):
            contents[idx]["biz_id"] = str(contents[idx]["biz_id"])
        return contents

    def get_pics(self) -> list:
        """
        获取动态图片

        Returns:
            list: 动态图片
        """
        return self.pics

    def get_attach_card(self) -> Optional[dict]:
        """
        获取动态预约

        Returns:
            Optional[dict]: 动态预约
        """
        return self.attach_card

    def get_topic(self) -> Optional[dict]:
        """
        获取动态话题

        Returns:
            Optional[dict]: 动态话题
        """
        return self.topic

    def get_options(self) -> dict:
        """
        获取动态选项

        Returns:
            dict: 动态选项
        """
        return self.options


async def send_dynamic(info: BuildDynamic, credential: Credential):
    """
    发送动态

    Args:
        info (BuildDynamic): 动态内容

        credential (Credential): 凭据

    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    pic_data = []
    for image in info.pics:
        await image.upload(credential)
        pic_data.append(
            {"img_src": image.url, "img_width": image.width, "img_height": image.height}
        )

    api = API["send"]["instant"]
    data = {
        "dyn_req": {
            "content": {
                "contents": await info.get_contents(credential=credential)
            },  # 必要参数
            "scene": info.get_dynamic_type().value,  # 必要参数
            "meta": {
                "app_meta": {"from": "create.dynamic.web", "mobi_app": "web"},
            },
        }
    }
    if info.time:
        data["dyn_req"]["option"] = {"timer_pub_time": int(info.time.timestamp())}
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
        self.__detail = None
        self.credential: Credential = (
            credential if credential is not None else Credential()
        )

    def get_dynamic_id(self) -> None:
        """
        获取 动态 ID。

        Returns:
            int: 动态 ID。
        """
        return self.__dynamic_id

    async def get_info(self) -> dict:
        """
        获取动态信息

        Returns:
            dict: 调用 API 返回的结果
        """
        if not self.__detail:
            api = API["info"]["detail"]
            params = {
                "id": self.__dynamic_id,
                "timezone_offset": -480,
                "platform": "web",
                "gaia_source": "main_web",
                "features": "itemOpusStyle,opusBigCover,onlyfansVote,endFooterHidden,decorationCard,onlyfansAssetsV2,ugcDelete",
                "web_location": "333.1368",
                "x-bili-device-req-json": '{"platform":"web","device":"pc"}',
                "x-bili-web-req-json": '{"spm_id":"333.1368"}',
            }
            self.__detail = (
                await Api(**api, credential=self.credential)
                .update_params(**params)
                .result
            )
            cache_pool.dynamic_is_article[self.__dynamic_id] = (
                self.__detail["item"]["basic"]["comment_type"] == 12
            )
            if cache_pool.dynamic_is_article[self.__dynamic_id]:
                cache_pool.dynamic2article[self.__dynamic_id] = int(
                    self.__detail["item"]["basic"]["rid_str"]
                )
                cache_pool.article2dynamic[
                    cache_pool.dynamic2article[self.__dynamic_id]
                ] = self.__dynamic_id
            module_dynamic = self.__detail["item"]["modules"]["module_dynamic"]
            if module_dynamic.get("major") is None:
                cache_pool.dynamic_is_opus[self.__dynamic_id] = False
            else:
                cache_pool.dynamic_is_opus[self.__dynamic_id] = (
                    module_dynamic["major"]["type"] == "MAJOR_TYPE_OPUS"
                )
        return self.__detail

    async def is_article(self) -> bool:
        """
        判断动态是否为专栏发布动态（评论、点赞等数据专栏/动态/图文共享）

        Returns:
            bool: 是否为专栏
        """
        if cache_pool.dynamic_is_article.get(self.get_dynamic_id()) is None:
            await self.get_info()
        return cache_pool.dynamic_is_article[self.get_dynamic_id()]

    async def turn_to_article(self) -> "Article":
        """
        将专栏发布动态转为对应专栏（评论、点赞等数据专栏/动态/图文共享）

        如动态无对应专栏将报错。

        转换后可投币。

        Returns:
            Article: 专栏实例
        """
        if cache_pool.dynamic2article.get(self.get_dynamic_id()) is None:
            await self.get_info()
            if not await self.is_article():
                raise ArgsException("提供的动态无对应专栏")
        return Article(
            cvid=cache_pool.dynamic2article[self.get_dynamic_id()],
            credential=self.credential,
        )

    async def is_opus(self) -> bool:
        """
        判断动态是否为图文

        如果是图文，则动态/图文评论/点赞/转发数据共享

        Returns:
            bool: 是否为图文
        """
        if cache_pool.dynamic_is_opus.get(self.__dynamic_id) is None:
            await self.get_info()
        return cache_pool.dynamic_is_opus[self.__dynamic_id]

    def turn_to_opus(self) -> "Opus":
        """
        对图文动态，转换为图文

        此函数不会核验动态是否为图文

        Returns:
            Opus: 图文对象
        """
        return Opus(opus_id=self.__dynamic_id, credential=self.credential)

    async def markdown(self) -> str:
        """
        生成动态富文本对应 markdown

        Returns:
            str: markdown
        """
        info = await self.get_info()

        def parse_module_dynamic(module: dict):
            if module["major"] is None:
                # 转发动态
                nodes = module["desc"]["rich_text_nodes"]
                pics = []
                title = ""
            else:
                if module["major"]["type"] == "MAJOR_TYPE_OPUS":
                    # 图文
                    nodes = module["major"]["opus"]["summary"]["rich_text_nodes"]
                    pics = module["major"]["opus"]["pics"]
                    title = module["major"]["opus"]["title"]
                else:
                    # 按投稿
                    keys = module["major"].keys()
                    for key in keys:
                        if (
                            module["major"][key].get("cover") is not None
                            and module["major"][key].get("jump_url") is not None
                            and module["major"][key].get("title") is not None
                        ):
                            cover = module["major"][key].get("cover")
                            if jump_url.startswith("//"):
                                jump_url = "https:" + module["major"][key].get(
                                    "jump_url"
                                )
                            title = module["major"][key].get("title")
                            return f"# {title}\n\n![]({cover})\n\n<{jump_url}>\n"
            ret = "" if title is None else "# " + title + "\n\n"
            for node in nodes:
                text = node["text"]
                jump_url = node.get("jump_url")
                if jump_url is not None:
                    if jump_url.startswith("//"):
                        jump_url = f"https:{jump_url}"
                text = text.replace("\t", " ")
                text = text.replace(" ", "&emsp;")
                text = text.replace(chr(160), "&emsp;")
                special_chars = [
                    "\\",
                    "*",
                    "$",
                    "<",
                    ">",
                    "|",
                    "~",
                    "_",
                ]
                for c in special_chars:
                    text = text.replace(c, "\\" + c)
                if node["type"] == "RICH_TEXT_NODE_TYPE_AT":
                    rid = node["rid"]
                    ret += f"[{text}](https://space.bilibili.com/{rid}) "
                elif node["type"] == "RICH_TEXT_NODE_TYPE_EMOJI":
                    icon_url = node["emoji"]["icon_url"]
                    if icon_url.startswith("//"):
                        icon_url = f"https:{icon_url}"
                    ret += f"<img width=50px height=50px src={icon_url}> "
                elif jump_url is not None:
                    ret += f"[{text}]({jump_url})"
                else:
                    ret += f"{text} "
            ret += "\n\n"
            for pic in pics:
                width = pic["width"]
                height = pic["height"]
                url = pic["url"]
                if url.startswith("//"):
                    url = f"https:{url}"
                ret += f"![]({url}) \n"
            return ret

        content = parse_module_dynamic(info["item"]["modules"]["module_dynamic"])
        content += "\n\n"
        if info["item"].get("orig"):
            orig_content = parse_module_dynamic(
                info["item"]["orig"]["modules"]["module_dynamic"]
            )
            for line in orig_content.split("\n"):
                content += f"> {line}\n"
        meta_yaml = yaml.safe_dump(info["item"], allow_unicode=True)
        content = f"---\n{meta_yaml}\n---\n\n{content}"
        return content

    async def get_reaction(self, offset: str = "") -> dict:
        """
        获取点赞、转发

        Args:
            offset (str, optional): 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to ""

        Returns:
            dict: 调用 API 返回的结果
        """

        api = API["info"]["reaction"]
        params = {"web_location": "333.1369", "offset": offset, "id": self.__dynamic_id}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

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

    async def get_rid(self) -> int:
        """
        获取 rid，以传入 `comment.get_comments_lazy` 等函数 oid 参数对评论区进行操作

        Returns:
            int: rid
        """
        return int((await self.get_info())["item"]["basic"]["rid_str"])

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
        data = await _get_text_data(text, self.credential)
        data["dynamic_id"] = self.__dynamic_id
        return await Api(**api, credential=self.credential).update_data(**data).result

    async def set_favorite(self, status: bool = True) -> dict:
        """
        设置动态（图文）收藏状态

        Args:
            status (bool, optional): 收藏状态. Defaults to True

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API_opus["operate"]["simple_action"]
        params = {
            "csrf": self.credential.bili_jct,
        }
        data = {
            "meta": {
                "spmid": "444.42.0.0",
                "from_spmid": "333.1365.0.0",
                "from": "unknown",
            },
            "entity": {
                "object_id_str": str(self.__dynamic_id),
                "type": {
                    "biz": 2,
                },
            },
            "action": 3 if status else 4,
        }
        return (
            await Api(**api, credential=self.credential)
            .update_params(**params)
            .update_data(**data)
            .result
        )

    async def get_lottery_info(self) -> dict:
        """
        获取动态抽奖信息

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["info"]["lottery"]
        params = {
            "business_id": self.get_dynamic_id(),
            "business_type": 1,
            "csrf": self.credential.bili_jct,
            "web_location": "333.1330",
        }
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )


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
    features: str = "itemOpusStyle",
    pn: int = 1,
    offset: Optional[int] = None,
) -> dict:
    """
    获取动态页动态信息

    获取全部动态或者相应类型需传入 _type

    获取指定 UP 主动态需传入 host_mid

    Args:
        credential (Credential): 凭据类.

        _type      (DynamicType, optional): 动态类型. Defaults to DynamicType.ALL.

        host_mid   (int, optional): 获取对应 UP 主动态的 mid. Defaults to None.

        features   (str, optional): 默认 itemOpusStyle.

        pn         (int, optional): 页码. Defaults to 1.

        offset     (int, optional): 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """

    api = API["info"]["dynamic_page_info"]
    params = {
        "timezone_offset": -480,
        "features": features,
        "page": pn,
    }
    params.update({"offset": offset} if offset else {})
    if _type:  # 全部动态
        params["type"] = _type.value
    elif host_mid:  # 指定 UP 主动态
        params["host_mid"] = host_mid
    elif not _type:
        api["params"].pop("type")
    elif not host_mid:
        api["params"].pop("host_mid")

    return await Api(**api, credential=credential).update_params(**params).result


async def get_dynamic_page_list(
    credential: Credential,
    _type: Optional[DynamicType] = None,
    host_mid: Optional[int] = None,
    features: str = "itemOpusStyle",
    pn: int = 1,
    offset: Optional[int] = None,
) -> List[Dynamic]:
    """
    获取动态页动态列表

    获取全部动态或者相应类型需传入 _type

    获取指定 UP 主动态需传入 host_mid

    Args:
        credential (Credential): 凭据类.

        _type      (DynamicType, optional): 动态类型. Defaults to DynamicType.ALL.

        host_mid   (int, optional): 获取对应 UP 主动态的 mid. Defaults to None.

        features   (str, optional): 默认 itemOpusStyle.

        pn         (int, optional): 页码. Defaults to 1.

        offset     (int, optional): 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to None.

    Returns:
        list[Dynamic]: 动态类列表
    """

    api = API["info"]["dynamic_page_info"]
    params = {
        "timezone_offset": -480,
        "features": features,
        "page": pn,
    }
    params.update({"offset": offset} if offset else {})
    if _type:  # 全部动态
        params["type"] = _type.value
    elif host_mid:  # 指定 UP 主动态
        params["host_mid"] = host_mid
    elif not _type:
        api["params"].pop("type")
    elif not host_mid:
        api["params"].pop("host_mid")

    dynmaic_data = (
        await Api(**api, credential=credential).update_params(**params).result
    )
    return [
        Dynamic(dynamic_id=int(dynamic["id_str"]), credential=credential)
        for dynamic in dynmaic_data["items"]
    ]
