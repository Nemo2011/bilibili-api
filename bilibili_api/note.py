"""
bilibili_api.note

笔记相关
"""

import json
from enum import Enum
from html import unescape
from typing import List, Union, overload

import yaml
from yarl import URL

from .utils.initial_state import get_initial_state

from .utils.utils import get_api, raise_for_statement, img_auto_scheme
from .utils.picture import Picture
from .exceptions import ApiException, ArgsException
from .utils.network import Api, Credential
from .utils import cache_pool
from . import article

API = get_api("note")
API_ARTICLE = get_api("article")


async def upload_image(img: Picture, credential: Credential) -> dict:
    """
    上传笔记图片

    Args:
        img        (Picture)   : 图片
        credential (Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    api = API["operate"]["upload_img"]
    files = {"file": img._to_biliapifile()}
    return await Api(**api, credential=credential).update_files(**files).result


class NoteType(Enum):
    """
    笔记类型
    """

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
        credential: Union[Credential, None] = None,
    ):
        """
        Args:
            cvid       (int)                  : 公开笔记 ID (对应专栏的 cvid) (公开笔记必要)

            aid        (int)                  : 稿件 ID（oid_type 为 0 时是 avid） (私有笔记必要)

            note_id    (int)                  : 私有笔记 ID (私有笔记必要)

            note_type  (str)                  : 笔记类型 (private, public)

            credential (Credential, optional) : Credential. Defaults to None.
        """
        self.__oid = -1
        self.__note_id = -1
        self.__cvid = -1
        # ID 和 type 检查
        if note_type == NoteType.PRIVATE:
            if not aid or not note_id:
                raise ArgsException("私有笔记需要 oid 和 note_id")
            self.__oid = aid
            self.__note_id = note_id
        elif note_type == NoteType.PUBLIC:
            if not cvid:
                raise ArgsException("公开笔记需要 cvid")
            self.__cvid = cvid
        else:
            raise ArgsException("type_ 只能是 public 或 private")

        self.__type = note_type

        # 未提供 credential 时初始化该类
        # 私有笔记需要 credential
        self.credential: Credential = Credential() if credential is None else credential

        # 用于存储视频信息，避免接口依赖视频信息时重复调用
        self.__info: Union[dict, None] = None

        # 用于存储正文的节点
        self.__children: List[Node] = []
        # 用于存储是否解析
        self.__has_parsed: bool = False
        # 用于存储转换为 markdown 和 json 时使用的信息
        self.__meta: dict = {}

    def get_cvid(self) -> int:
        """
        获取公开笔记 cvid

        Returns:
            int: 公开笔记 cvid
        """
        return self.__cvid

    def get_aid(self) -> int:
        """
        获取私有笔记对应视频 aid

        Returns:
            int: aid
        """
        return self.__oid

    def get_note_id(self) -> int:
        """
        获取私有笔记 note_id

        Returns:
            int: note_id
        """
        return self.__note_id

    def turn_to_article(self) -> "article.Article":
        """
        将笔记类转为专栏类。需要保证笔记是公开笔记。

        Returns:
            Note: 专栏类
        """
        raise_for_statement(self.__type == NoteType.PUBLIC)
        return article.Article(cvid=self.get_cvid(), credential=self.credential)

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
        raise_for_statement(self.__type == NoteType.PRIVATE)

        api = API["private"]["detail"]
        # oid 为 0 时指 avid
        params = {"oid": self.get_aid(), "note_id": self.get_note_id(), "oid_type": 0}
        resp = (
            await Api(**api, credential=self.credential).update_params(**params).result
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

        raise_for_statement(self.__type == NoteType.PUBLIC)

        api = API["public"]["detail"]
        params = {"cvid": self.get_cvid()}
        resp = (
            await Api(**api, credential=self.credential).update_params(**params).result
        )
        # 存入 self.__info 中以备后续调用
        self.__info = resp
        cache_pool.article_is_note[self.__cvid] = True
        return resp

    async def get_images_raw_info(self) -> List["dict"]:
        """
        获取笔记所有图片原始信息

        Returns:
            list: 图片信息
        """

        result = []
        content = (await self.__get_info_cached())["content"]
        for line in content:
            if type(line["insert"]) == dict:
                if "imageUpload" in line["insert"]:
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
            result.append(await Picture().load_url(url=img_auto_scheme(image["url"])))
        return result

    async def get_all(self) -> dict:
        """
        (仅供公开笔记)

        一次性获取专栏尽可能详细数据，包括原始内容、标签、发布时间、标题、相关专栏推荐等

        Returns:
            dict: 调用 API 返回的结果
        """
        raise_for_statement(self.__type == NoteType.PUBLIC)
        return await get_initial_state(f"https://www.bilibili.com/read/cv{self.__cvid}")

    async def set_like(self, status: bool = True) -> dict:
        """
        (仅供公开笔记)

        设置专栏点赞状态

        Args:
            status (bool, optional): 点赞状态. Defaults to True

        Returns:
            dict: 调用 API 返回的结果
        """
        raise_for_statement(self.__type == NoteType.PUBLIC)

        self.credential.raise_for_no_sessdata()

        api = API_ARTICLE["operate"]["like"]
        data = {"id": self.__cvid, "type": 1 if status else 2}
        return await Api(**api, credential=self.credential).update_data(**data).result

    async def set_favorite(self, status: bool = True) -> dict:
        """
        (仅供公开笔记)

        设置专栏收藏状态

        Args:
            status (bool, optional): 收藏状态. Defaults to True

        Returns:
            dict: 调用 API 返回的结果
        """
        raise_for_statement(self.__type == NoteType.PUBLIC)

        self.credential.raise_for_no_sessdata()

        api = (
            API_ARTICLE["operate"]["add_favorite"]
            if status
            else API_ARTICLE["operate"]["del_favorite"]
        )

        data = {"id": self.__cvid}
        return await Api(**api, credential=self.credential).update_data(**data).result

    async def add_coins(self) -> dict:
        """
        (仅供公开笔记)

        给笔记投币，目前只能投一个。

        Returns:
            dict: 调用 API 返回的结果
        """
        raise_for_statement(self.__type == NoteType.PUBLIC)

        self.credential.raise_for_no_sessdata()

        upid = (await self.get_info())["mid"]
        api = API_ARTICLE["operate"]["coin"]
        data = {"aid": self.__cvid, "multiply": 1, "upid": upid, "avtype": 2}
        return await Api(**api, credential=self.credential).update_data(**data).result

    async def fetch_content(self) -> None:
        """
        获取并解析笔记内容

        该返回不会返回任何值，调用该方法后请再调用 `self.markdown()` 或 `self.json()` 来获取你需要的值。
        """

        async def parse_note(data: List[dict]):
            for field in data:
                if not isinstance(field["insert"], str):
                    if "imageUpload" in field["insert"].keys():
                        node = ImageNode()
                        node.url = field["insert"]["imageUpload"]["url"]
                        self.__children.append(node)
                    elif "cut-off" in field["insert"].keys():
                        node = ImageNode()
                        node.url = field["insert"]["cut-off"]["url"]
                        self.__children.append(node)
                else:
                    node = TextNode(field["insert"])
                    if "attributes" in field.keys():
                        if field["attributes"].get("bold") == True:
                            bold = BoldNode()
                            bold.children = [node]
                            node = bold
                        if field["attributes"].get("strike") == True:
                            delete = DelNode()
                            delete.children = [node]
                            node = delete
                        if field["attributes"].get("underline") == True:
                            underline = UnderlineNode()
                            underline.children = [node]
                            node = underline
                        if field["attributes"].get("background") == True:
                            # FIXME: 暂不支持背景颜色
                            pass
                        if field["attributes"].get("color") != None:
                            color = ColorNode()
                            color.color = field["attributes"]["color"].replace("#", "")
                            color.children = [node]
                            node = color
                        if field["attributes"].get("size") != None:
                            size = FontSizeNode()
                            size.size = field["attributes"]["size"]
                            size.children = [node]
                            node = size
                    else:
                        pass
                    self.__children.append(node)

        info = await self.get_info()
        content = info["content"]
        content = unescape(content)
        await parse_note(json.loads(content))
        self.__has_parsed = True
        self.__meta = await self.__get_info_cached()
        del self.__meta["content"]

    def markdown(self) -> str:
        """
        转换为 Markdown

        请先调用 fetch_content()

        Returns:
            str: Markdown 内容
        """
        if not self.__has_parsed:
            raise ApiException("请先调用 fetch_content()")

        content = ""

        for node in self.__children:
            try:
                markdown_text = node.markdown()
            except Exception as e:
                pass
            else:
                content += markdown_text

        meta_yaml = yaml.safe_dump(self.__meta, allow_unicode=True)
        content = f"---\n{meta_yaml}\n---\n\n{content}"
        return content

    def json(self) -> dict:
        """
        转换为 JSON 数据

        请先调用 fetch_content()

        Returns:
            dict: JSON 数据
        """
        if not self.__has_parsed:
            raise ApiException("请先调用 fetch_content()")

        return {
            "type": "Note",
            "meta": self.__meta,
            "children": list(map(lambda x: x.json(), self.__children)),
        }

    # TODO: 笔记上传/编辑/删除


class Node:
    def __init__(self):
        pass

    @overload
    def markdown(self) -> str:  # type: ignore
        pass

    @overload
    def json(self) -> dict:  # type: ignore
        pass


class BoldNode(Node):
    def __init__(self):
        self.children = []

    def markdown(self):
        t = "".join([node.markdown() for node in self.children])
        if len(t) == 0:
            return ""
        return f" **{t.lstrip().rstrip()}** "

    def json(self):
        return {
            "type": "BoldNode",
            "children": list(map(lambda x: x.json(), self.children)),
        }


class DelNode(Node):
    def __init__(self):
        self.children = []

    def markdown(self):
        text = "".join([node.markdown() for node in self.children])
        if len(text) == 0:
            return ""
        return f" ~~{text}~~"

    def json(self):
        return {
            "type": "DelNode",
            "children": list(map(lambda x: x.json(), self.children)),
        }


class UnderlineNode(Node):
    def __init__(self):
        self.children = []

    def markdown(self):
        text = "".join([node.markdown() for node in self.children])
        if len(text) == 0:
            return ""
        return " $\\underline{" + text + "}$ "


class ColorNode(Node):
    def __init__(self):
        self.color = "000000"
        self.children = []

    def markdown(self):
        return "".join([node.markdown() for node in self.children])

    def json(self):
        return {
            "type": "ColorNode",
            "color": self.color,
            "children": list(map(lambda x: x.json(), self.children)),
        }


class FontSizeNode(Node):
    def __init__(self):
        self.size = 16
        self.children = []

    def markdown(self):
        return "".join([node.markdown() for node in self.children])

    def json(self):
        return {
            "type": "FontSizeNode",
            "size": self.size,
            "children": list(map(lambda x: x.json(), self.children)),
        }


# 特殊节点，即无子节点


class TextNode(Node):
    def __init__(self, text: str):
        self.text = text

    def markdown(self):
        return self.text

    def json(self):
        return {"type": "TextNode", "text": self.text}


class ImageNode(Node):
    def __init__(self):
        self.url = ""
        self.alt = ""

    def markdown(self):
        if URL(self.url).scheme == "":
            self.url = "https:" + self.url
        alt = self.alt.replace("[", "\\[")
        return f"![{alt}]({self.url})\n\n"

    def json(self):
        if URL(self.url).scheme == "":
            self.url = "https:" + self.url
        return {"type": "ImageNode", "url": self.url, "alt": self.alt}
