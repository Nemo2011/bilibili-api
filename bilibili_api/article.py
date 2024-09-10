"""
bilibili_api.article

专栏相关
"""

import json
import random
import re
import time
from copy import copy
from enum import Enum, IntEnum
from html import unescape
from typing import List, Union, TypeVar, overload
from urllib.parse import unquote

import yaml
from bs4 import BeautifulSoup, element
from yarl import URL

from . import note, Picture
from . import opus
from .exceptions import ApiException
from .utils import cache_pool
from .utils.credential import Credential
from .utils.initial_state import get_initial_state, get_initial_state_sync
from .utils.network import Api
from .utils.utils import get_api, raise_for_statement
from .video import get_cid_info_sync

API = get_api("article")

# 文章颜色表
ARTICLE_COLOR_MAP = {
    "default": "222222",
    "blue-01": "56c1fe",
    "lblue-01": "73fdea",
    "green-01": "89fa4e",
    "yellow-01": "fff359",
    "pink-01": "ff968d",
    "purple-01": "ff8cc6",
    "blue-02": "02a2ff",
    "lblue-02": "18e7cf",
    "green-02": "60d837",
    "yellow-02": "fbe231",
    "pink-02": "ff654e",
    "purple-02": "ef5fa8",
    "blue-03": "0176ba",
    "lblue-03": "068f86",
    "green-03": "1db100",
    "yellow-03": "f8ba00",
    "pink-03": "ee230d",
    "purple-03": "cb297a",
    "blue-04": "004e80",
    "lblue-04": "017c76",
    "green-04": "017001",
    "yellow-04": "ff9201",
    "pink-04": "b41700",
    "purple-04": "99195e",
    "gray-01": "d6d5d5",
    "gray-02": "929292",
    "gray-03": "5f5f5f",
}


class ArticleType(Enum):
    """
    专栏类型

    - ARTICLE        : 普通专栏，不与 opus 图文兼容。
    - OPUS           : opus。
    - SPECIAL_ARTICLE: 特殊专栏，与 opus 兼容。
    """

    ARTICLE = 3
    OPUS = 4
    SPECIAL_ARTICLE = 5


class ArticleRankingType(Enum):
    """
    专栏排行榜类型枚举。

    + MONTH: 月榜
    + WEEK: 周榜
    + DAY_BEFORE_YESTERDAY: 前日榜
    + YESTERDAY: 昨日榜
    """

    MONTH = 1
    WEEK = 2
    DAY_BEFORE_YESTERDAY = 4
    YESTERDAY = 3


ArticleT = TypeVar("ArticleT", bound="Article")


async def get_article_rank(
    rank_type: ArticleRankingType = ArticleRankingType.YESTERDAY,
):
    """
    获取专栏排行榜

    Args:
        rank_type (ArticleRankingType): 排行榜类别. Defaults to ArticleRankingType.YESTERDAY.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["rank"]
    params = {"cid": rank_type.value}
    return await Api(**api).update_params(**params).result


class ArticleList:
    """
    文集类

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(self, rlid: int, credential: Union[Credential, None] = None):
        """
        Args:
            rlid       (int)                        : 文集 id

            credential (Credential | None, optional): 凭据类. Defaults to None.
        """
        self.__rlid = rlid
        self.credential: Credential = credential

    def get_rlid(self) -> int:
        """
        获取 rlid

        Returns:
            int: rlid
        """
        return self.__rlid

    async def get_content(self) -> dict:
        """
        获取专栏文集文章列表

        Returns:
            dict: 调用 API 返回的结果
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["list"]["get"]
        params = {"id": self.__rlid}
        return await Api(**api, credential=credential).update_params(**params).result


class Article:
    """
    专栏类

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(self, cvid: int, credential: Union[Credential, None] = None):
        """
        Args:
            cvid       (int)                        : cv 号

            credential (Credential | None, optional): 凭据. Defaults to None.
        """
        self.__children: List[Node] = []
        self.credential: Credential = (
            credential if credential is not None else Credential()
        )
        self.__meta = None
        self.__cvid = cvid
        self.__has_parsed: bool = False
        self.__is_note = False

        # 设置专栏类别
        if cache_pool.article_is_opus.get(self.__cvid):
            self.__type = ArticleType.SPECIAL_ARTICLE
            self.__is_note = cache_pool.article_is_note[self.__cvid]
        else:
            resp = get_initial_state_sync(f"https://www.bilibili.com/read/cv{self.__cvid}")[0]
            self.__dyn_id = int(resp["readInfo"]["dyn_id_str"])
            self.__type = ArticleType(resp["readInfo"]["template_id"])
            self.__is_note = resp["readInfo"]["type"] == 2

        if cache_pool.article_dyn_id.get(self.__cvid):
            self.__dyn_id = cache_pool.article_dyn_id[self.__cvid]

    def get_cvid(self) -> int:
        """
        获取 cvid

        Returns:
            int: cvid
        """
        return self.__cvid

    def get_type(self) -> ArticleType:
        """
        获取专栏类型(专栏/笔记)

        Returns:
            ArticleType: 专栏类型
        """
        return self.__type

    def is_note(self) -> bool:
        """
        检查专栏是否笔记

        Returns:
            bool: 是否笔记
        """
        return self.__is_note

    def turn_to_note(self) -> "note.Note":
        """
        对于完全与 opus 兼容的部分的特殊专栏，将 Article 对象转换为 Dynamic 对象。

        Returns:
            Note: 笔记类
        """
        raise_for_statement(
            self.is_note(), "仅支持公开笔记"
        )
        return note.Note(
            cvid=self.__cvid, note_type=note.NoteType.PUBLIC, credential=self.credential
        )

    def turn_to_opus(self) -> "opus.Opus":
        """
        对于 SPECIAL_ARTICLE，将其转为图文
        """
        raise_for_statement(
            self.__type != ArticleType.ARTICLE, "仅支持图文专栏"
        )
        cache_pool.opus_type[self.__dyn_id] = 1
        cache_pool.opus_is_note[self.__dyn_id] = self.is_note()
        cache_pool.opus_cvid[self.__dyn_id] = self.__cvid
        return opus.Opus(self.__dyn_id, credential=self.credential)

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
            except:
                continue
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
            "type": "Article",
            "meta": self.__meta,
            "children": list(map(lambda x: x.json(), self.__children)),
        }

    async def fetch_content(self) -> None:
        """
        获取并解析专栏内容

        该返回不会返回任何值，调用该方法后请再调用 `self.markdown()` 或 `self.json()` 来获取你需要的值。
        """

        resp = await self.get_all()

        document = BeautifulSoup(f"<div>{resp['readInfo']['content']}</div>", "lxml")

        async def parse(el: BeautifulSoup):
            node_list = []

            for e in el.contents:  # type: ignore
                if type(e) == element.NavigableString:
                    # 文本节点
                    node = TextNode(e)  # type: ignore
                    node_list.append(node)
                    continue

                e: BeautifulSoup = e
                if e.name == "p":
                    # 段落
                    node = ParagraphNode()
                    node_list.append(node)

                    if "style" in e.attrs:
                        if "text-align: center" in e.attrs["style"]:
                            node.align = "center"

                        elif "text-align: right" in e.attrs["style"]:
                            node.align = "right"

                        else:
                            node.align = "left"

                    node.children = await parse(e)

                elif e.name == "h1":
                    # 标题
                    node = HeadingNode()
                    node_list.append(node)

                    node.children = await parse(e)

                elif e.name == "strong":
                    # 粗体
                    node = BoldNode()
                    node_list.append(node)

                    node.children = await parse(e)

                elif e.name == "span":
                    # 各种样式
                    if "style" in e.attrs:
                        style = e.attrs["style"]

                        if "text-decoration: line-through" in style:
                            # 删除线
                            node = DelNode()
                            node_list.append(node)

                            node.children = await parse(e)
                        if e.text != "":
                            node_list += await parse(e)

                    elif "class" in e.attrs:
                        className = e.attrs["class"][0]

                        if "font-size" in className:
                            # 字体大小
                            node = FontSizeNode()
                            node_list.append(node)

                            node.size = int(re.search("font-size-(\d\d)", className)[1])  # type: ignore
                            node.children = await parse(e)

                        elif "color" in className:
                            # 字体颜色
                            node = ColorNode()
                            node_list.append(node)

                            color_text = re.search("color-(.*);?", className)[1]  # type: ignore
                            node.color = ARTICLE_COLOR_MAP[color_text]

                            node.children = await parse(e)
                        else:
                            if e.text != "":
                                node_list += (await parse(e))

                elif e.name == "blockquote":
                    # 引用块
                    # print(e.text)
                    node = BlockquoteNode()
                    node_list.append(node)
                    node.children = await parse(e)

                elif e.name == "figure":
                    if "class" in e.attrs:
                        className = e.attrs["class"]

                        if "img-box" in className:
                            img_el: BeautifulSoup = e.find("img")  # type: ignore
                            if img_el == None:
                                pass
                            elif "class" in img_el.attrs:
                                className = img_el.attrs["class"]

                                if "cut-off" in className:
                                    # 分割线
                                    node = SeparatorNode()
                                    node_list.append(node)

                                if "aid" in img_el.attrs:
                                    # 各种卡片
                                    aid = img_el.attrs["aid"]

                                    if "video-card" in className:
                                        # 视频卡片，考虑有两列视频
                                        for a in aid.split(","):
                                            node = VideoCardNode()
                                            node_list.append(node)

                                            node.aid = int(a)

                                    elif "article-card" in className:
                                        # 文章卡片
                                        node = ArticleCardNode()
                                        node_list.append(node)

                                        node.cvid = int(aid)

                                    elif "fanju-card" in className:
                                        # 番剧卡片
                                        node = BangumiCardNode()
                                        node_list.append(node)

                                        node.epid = int(aid[2:])

                                    elif "music-card" in className:
                                        # 音乐卡片
                                        node = MusicCardNode()
                                        node_list.append(node)

                                        node.auid = int(aid[2:])

                                    elif "shop-card" in className:
                                        # 会员购卡片
                                        node = ShopCardNode()
                                        node_list.append(node)

                                        node.pwid = int(aid[2:])

                                    elif "caricature-card" in className:
                                        # 漫画卡片，考虑有两列

                                        for i in aid.split(","):
                                            node = ComicCardNode()
                                            node_list.append(node)

                                            node.mcid = int(i)

                                    elif "live-card" in className:
                                        # 直播卡片
                                        node = LiveCardNode()
                                        node_list.append(node)

                                        node.room_id = int(aid)

                                if "seamless" in className:
                                    # 图片节点
                                    node = ImageNode()
                                    node_list.append(node)

                                    node.url = "https:" + e.find("img").attrs["data-src"]  # type: ignore

                                    figcaption_el: BeautifulSoup = e.find("figcaption")  # type: ignore

                                    if figcaption_el:
                                        if figcaption_el.contents:
                                            node.alt = figcaption_el.contents[0]  # type: ignore
                            else:
                                # 图片节点
                                node = ImageNode()
                                node_list.append(node)

                                node.url = "https:" + e.find("img").attrs["data-src"]  # type: ignore

                                figcaption_el: BeautifulSoup = e.find("figcaption")  # type: ignore

                                if figcaption_el:
                                    if figcaption_el.contents:
                                        node.alt = figcaption_el.contents[0]  # type: ignore

                        elif "code-box" in className:
                            # 代码块
                            node = CodeNode()
                            node_list.append(node)

                            pre_el: BeautifulSoup = e.find("pre")  # type: ignore
                            node.lang = pre_el.attrs["data-lang"].split("@")[0].lower()
                            node.code = unquote(pre_el.attrs["codecontent"])

                elif e.name == "ol":
                    # 有序列表
                    node = OlNode()
                    node_list.append(node)

                    node.children = await parse(e)

                elif e.name == "li":
                    # 列表元素
                    node = LiNode()
                    node_list.append(node)

                    node.children = await parse(e)

                elif e.name == "ul":
                    # 无序列表
                    node = UlNode()
                    node_list.append(node)

                    node.children = await parse(e)

                elif e.name == "a":
                    # 超链接
                    if len(e.contents) == 0:
                        from .utils.parse_link import ResourceType, parse_link

                        parse_link_res = await parse_link(e.attrs["href"])
                        if parse_link_res[1] == ResourceType.VIDEO:
                            node = VideoCardNode()
                            node.aid = parse_link_res[0].get_aid()
                            node_list.append(node)
                        elif parse_link_res[1] == ResourceType.AUDIO:
                            node = MusicCardNode()
                            node.auid = parse_link_res[0].get_auid()
                            node_list.append(node)
                        elif parse_link_res[1] == ResourceType.LIVE:
                            node = LiveCardNode()
                            node.room_id = parse_link_res[0].room_display_id
                            node_list.append(node)
                        elif parse_link_res[1] == ResourceType.ARTICLE:
                            node = ArticleCardNode()
                            node.cvid = parse_link_res[0].get_cvid()
                            node_list.append(node)
                        else:
                            # XXX: 暂不支持其他的站内链接
                            pass
                    else:
                        node = AnchorNode()
                        node_list.append(node)

                        node.url = e.attrs["href"]
                        node.text = e.contents[0]  # type: ignore

                elif e.name == "img":
                    className = e.attrs.get("class")

                    if not className:
                        # 图片
                        node = ImageNode()
                        node.url = e.attrs.get("data-src")  # type: ignore
                        node_list.append(node)

                    elif "latex" in className:
                        # 公式
                        node = LatexNode()
                        node_list.append(node)

                        node.code = unquote(e["alt"])  # type: ignore

            return node_list

        def parse_note(data: List[dict]):
            for field in data:
                if not isinstance(field["insert"], str):
                    if "tag" in field["insert"].keys():
                        node = VideoCardNode()
                        node.aid = get_cid_info_sync(field["insert"]["tag"]["cid"])[
                            "cid"
                        ]
                        self.__children.append(node)
                    elif "imageUpload" in field["insert"].keys():
                        node = ImageNode()
                        node.url = field["insert"]["imageUpload"]["url"]
                        self.__children.append(node)
                    elif "cut-off" in field["insert"].keys():
                        node = ImageNode()
                        node.url = field["insert"]["cut-off"]["url"]
                        self.__children.append(node)
                    elif "native-image" in field["insert"].keys():
                        node = ImageNode()
                        node.url = field["insert"]["native-image"]["url"]
                        self.__children.append(node)
                    else:
                        raise Exception()
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

        # 文章元数据
        self.__meta = copy(resp["readInfo"])
        del self.__meta["content"]

        self.__children = await parse(document.find("div"))

        self.__has_parsed = True

    async def get_info(self) -> dict:
        """
        获取专栏信息

        Returns:
            dict: 调用 API 返回的结果
        """

        api = API["info"]["view"]
        params = {"id": self.__cvid}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_all(self) -> dict:
        """
        一次性获取专栏尽可能详细数据，包括原始内容、标签、发布时间、标题、相关专栏推荐等

        Returns:
            dict: 调用 API 返回的结果
        """
        return (
            await get_initial_state(f"https://www.bilibili.com/read/cv{self.__cvid}")
        )[0]

    async def set_like(self, status: bool = True) -> dict:
        """
        设置专栏点赞状态

        Args:
            status (bool, optional): 点赞状态. Defaults to True

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()

        api = API["operate"]["like"]
        data = {"id": self.__cvid, "type": 1 if status else 2}
        return await Api(**api, credential=self.credential).update_data(**data).result

    async def set_favorite(self, status: bool = True) -> dict:
        """
        设置专栏收藏状态

        Args:
            status (bool, optional): 收藏状态. Defaults to True

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()

        api = (
            API["operate"]["add_favorite"] if status else API["operate"]["del_favorite"]
        )

        data = {"id": self.__cvid}
        return await Api(**api, credential=self.credential).update_data(**data).result

    async def add_coins(self) -> dict:
        """
        给专栏投币，目前只能投一个

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()

        upid = (await self.get_info())["mid"]
        api = API["operate"]["coin"]
        data = {"aid": self.__cvid, "multiply": 1, "upid": upid, "avtype": 2}
        return await Api(**api, credential=self.credential).update_data(**data).result

    # TODO: 专栏上传/编辑/删除


class Node:
    def __init__(self):
        pass

    @overload
    def markdown(self) -> str:  # type: ignore
        pass

    @overload
    def json(self) -> dict:  # type: ignore
        pass


class ParagraphNode(Node):
    def __init__(self):
        self.children = []
        self.align = "left"

    def markdown(self):
        content = "".join([node.markdown() for node in self.children])
        return content + "\n\n"

    def json(self):
        return {
            "type": "ParagraphNode",
            "children": list(map(lambda x: x.json(), self.children)),
        }


class HeadingNode(Node):
    def __init__(self):
        self.children = []

    def markdown(self):
        text = "".join([node.markdown() for node in self.children])
        if len(text) == 0:
            return ""
        return f"## {text}\n\n"

    def json(self):
        return {
            "type": "HeadingNode",
            "children": list(map(lambda x: x.json(), self.children)),
        }


class BlockquoteNode(Node):
    def __init__(self):
        self.children = []

    def markdown(self):
        t = "".join([node.markdown() for node in self.children])
        # 填补空白行的 > 并加上标识符
        t = "\n".join(["> " + line for line in t.split("\n")]) + "\n\n"

        return t

    def json(self):
        return {
            "type": "BlockquoteNode",
            "children": list(map(lambda x: x.json(), self.children)),
        }


class ItalicNode(Node):
    def __init__(self):
        self.children = []

    def markdown(self):
        text = "".join([node.markdown() for node in self.children])
        if len(text) == 0:
            return ""
        return f" *{text}* "

    def json(self):
        return {
            "type": "ItalicNode",
            "children": list(map(lambda x: x.json(), self.children)),
        }


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
        return f" ~~{text}~~ "

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

    def json(self):
        return {
            "type": "UnderlineNode",
            "children": list(map(lambda x: x.json(), self.children)),
        }


class UlNode(Node):
    def __init__(self):
        self.children = []

    def markdown(self):
        return "\n".join(["- " + node.markdown() for node in self.children])

    def json(self):
        return {
            "type": "UlNode",
            "children": list(map(lambda x: x.json(), self.children)),
        }


class OlNode(Node):
    def __init__(self):
        self.children = []

    def markdown(self):
        t = []
        for i, node in enumerate(self.children):
            t.append(f"{i + 1}. {node.markdown()}")
        return "\n".join(t)

    def json(self):
        return {
            "type": "OlNode",
            "children": list(map(lambda x: x.json(), self.children)),
        }


class LiNode(Node):
    def __init__(self):
        self.children = []

    def markdown(self):
        return "".join([node.markdown() for node in self.children])

    def json(self):
        return {
            "type": "LiNode",
            "children": list(map(lambda x: x.json(), self.children)),
        }


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
        txt = self.text
        txt = txt.replace("\t", " ")
        txt = txt.replace(" ", "&emsp;")
        txt = txt.replace(chr(160), "&emsp;")
        special_chars = ["\\", "*", "$", "<", ">", "|"]
        for c in special_chars:
            txt = txt.replace(c, "\\" + c)
        return txt

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


class LatexNode(Node):
    def __init__(self):
        self.code = ""

    def markdown(self):
        if "\n" in self.code:
            # 块级公式
            return f"$$\n{self.code}\n$$"
        else:
            # 行内公式
            return f"${self.code}$"

    def json(self):
        return {"type": "LatexNode", "code": self.code}


class CodeNode(Node):
    def __init__(self):
        self.code = ""
        self.lang = ""

    def markdown(self):
        return f"```{self.lang if self.lang else ''}\n{self.code}\n```\n\n"

    def json(self):
        return {"type": "CodeNode", "code": self.code, "lang": self.lang}


# 卡片


class VideoCardNode(Node):
    def __init__(self):
        self.aid = 0

    def markdown(self):
        return f"[视频 av{self.aid}](https://www.bilibili.com/av{self.aid})\n\n"

    def json(self):
        return {"type": "VideoCardNode", "aid": self.aid}


class ArticleCardNode(Node):
    def __init__(self):
        self.cvid = 0

    def markdown(self):
        return f"[文章 cv{self.cvid}](https://www.bilibili.com/read/cv{self.cvid})\n\n"

    def json(self):
        return {"type": "ArticleCardNode", "cvid": self.cvid}


class BangumiCardNode(Node):
    def __init__(self):
        self.epid = 0

    def markdown(self):
        return f"[番剧 ep{self.epid}](https://www.bilibili.com/bangumi/play/ep{self.epid})\n\n"

    def json(self):
        return {"type": "BangumiCardNode", "epid": self.epid}


class MusicCardNode(Node):
    def __init__(self):
        self.auid = 0

    def markdown(self):
        return f"[音乐 au{self.auid}](https://www.bilibili.com/audio/au{self.auid})\n\n"

    def json(self):
        return {"type": "MusicCardNode", "auid": self.auid}


class ShopCardNode(Node):
    def __init__(self):
        self.pwid = 0

    def markdown(self):
        return f"[会员购 {self.pwid}](https://show.bilibili.com/platform/detail.html?id={self.pwid})\n\n"

    def json(self):
        return {"type": "ShopCardNode", "pwid": self.pwid}


class ComicCardNode(Node):
    def __init__(self):
        self.mcid = 0

    def markdown(self):
        return (
            f"[漫画 mc{self.mcid}](https://manga.bilibili.com/m/detail/mc{self.mcid})\n\n"
        )

    def json(self):
        return {"type": "ComicCardNode", "mcid": self.mcid}


class LiveCardNode(Node):
    def __init__(self):
        self.room_id = 0

    def markdown(self):
        return f"[直播 {self.room_id}](https://live.bilibili.com/{self.room_id})\n\n"

    def json(self):
        return {"type": "LiveCardNode", "room_id": self.room_id}


class AnchorNode(Node):
    def __init__(self):
        self.url = ""
        self.text = ""

    def markdown(self):
        text = self.text.replace("[", "\\[")
        return f"[{text}]({self.url})"

    def json(self):
        return {"type": "AnchorNode", "url": self.url, "text": self.text}


class SeparatorNode(Node):
    def __init__(self):
        pass

    def markdown(self):
        return "\n------\n"

    def json(self):
        return {"type": "SeparatorNode"}


######################
#
#  以下是创建专栏的代码
#
######################


class LineType(Enum):
    """分割线枚举

    按新版编辑器分割线选项从上往下排列
    """
    L0 = {"url": "https://i0.hdslb.com/bfs/article/0117cbba35e51b0bce5f8c2f6a838e8a087e8ee7.png", "height": 1}
    L1 = {"url": "https://i0.hdslb.com/bfs/article/4aa545dccf7de8d4a93c2b2b8e3265ac0a26d216.png", "height": 2}
    L2 = {"url": "https://i0.hdslb.com/bfs/article/71bf2cd56882a2e97f8b3477c9256f8b09f361d3.png", "height": 4}
    L3 = {"url": "https://i0.hdslb.com/bfs/article/db75225feabec8d8b64ee7d3c7165cd639554cbc.png", "height": 16}
    L4 = {"url": "https://i0.hdslb.com/bfs/article/4adb9255ada5b97061e610b682b8636764fe50ed.png", "height": 16}
    L5 = {"url": "https://i0.hdslb.com/bfs/article/02db465212d3c374a43c60fa2625cc1caeaab796.png", "height": 64}


class FontSize(IntEnum):
    """字体大小枚举

    Attributes:
        Text: 正文
        Header_2: 标题 2
        Header_1: 标题 1
    """
    Text = 17
    Header_2 = 22
    Header_1 = 24


class Align(IntEnum):
    """段落对齐方向枚举

    """
    left = 0
    center = 1
    right = 2


class BaseNode2:
    """新 Node 基类

    Attributes:
        node_type: 1 纯文字小节 4 超链接小节
        font_size: 字体大小
    """
    node_type: int = None
    font_size: int

    def json2(self) -> dict:
        """转化为新版编辑器上传所需的数据格式

        """
        pass

    def to_insert2(self) -> dict:
        """转化为新版编辑器保存草稿所需的数据格式

        """
        pass


class TextNode2(BaseNode2):
    """纯文字 Node

    """

    node_type = 1

    def __init__(self, words: str,
                 font_size: FontSize = FontSize.Text,
                 bold: bool = None,
                 italic: bool = None,
                 strikethrough: bool = None,
                 color: str = None):
        """
        Args:
            words (str) : 文本内容
            font_size (FontSize) : 字体大小
            bold (bool) : 粗体
            italic (bool) : 斜体
            strikethrough (bool) : 删除线
            color (str) : 字体颜色，最好是 ARTICLE_COLOR_MAP 内的颜色定义
        """
        self.words = words
        self.font_size = font_size.value
        self.bold = bold
        self.italic = italic
        self.strikethrough = strikethrough
        self.color = color

    def json2(self) -> dict:
        word = {"node_type": self.node_type, "words": self.words, "font_size": self.font_size, "style": {}}
        if self.bold:
            word["style"]["bold"] = self.bold
        if self.italic:
            word["style"]["italic"] = self.italic
        if self.strikethrough:
            word["style"]["strikethrough"] = self.strikethrough

        if self.color:
            word["color"] = f"#{self.color}"
        return {"word": word}

    def to_insert2(self) -> dict:
        result = {"attributes": {}, "insert": self.words}
        if self.bold:
            result["attributes"]["bold"] = self.bold
        if self.italic:
            result["attributes"]["italic"] = self.italic
        if self.strikethrough:
            result["attributes"]["strike"] = self.strikethrough
        if self.color:
            result["attributes"]["color"] = f"#{self.color}"
        if len(result["attributes"]) == 0:
            result.pop("attributes")
        return result


class LinkNode2(BaseNode2):
    """超链接 Node

    """
    node_type = 4

    def __init__(self, show_text: str,
                 link: str,
                 bold: bool = None,
                 italic: bool = None,
                 strikethrough: bool = None,
                 font_size: FontSize = FontSize.Text):
        """
        Args:
            show_text (str) : 超链接显示文本
            link (str) : 超链接的链接
            bold (bool) : 粗体
            italic (bool) : 斜体
            strikethrough (bool): 删除线
            font_size (FontSize): 字体大小
        """

        self.link_type = 16
        self.show_text = show_text
        self.link = link
        self.bold = bold
        self.italic = italic
        self.strikethrough = strikethrough
        self.font_size = font_size.value

    def json2(self) -> dict:
        link = {"link_type": self.link_type, "show_text": self.show_text, "link": self.link, "style": {}}
        if self.bold:
            link["style"]["bold"] = self.bold
        if self.italic:
            link["style"]["italic"] = self.italic
        if self.strikethrough:
            link["style"]["strikethrough"] = self.strikethrough
        if self.font_size:
            link["style"]["font_size"] = self.font_size
        return {"node_type": self.node_type, "link": link}

    def to_insert2(self) -> dict:
        result = {"attributes": {"link": self.link}, "insert": self.show_text}
        if self.bold:
            result["attributes"]["bold"] = self.bold
        if self.italic:
            result["attributes"]["italic"] = self.italic
        if self.strikethrough:
            result["attributes"]["strike"] = self.strikethrough
        if self.font_size:
            result["attributes"]["font_size"] = self.font_size
        return result


async def upwatermark(image: Picture, credential: Credential) -> dict:
    """上传获取带水印专栏段落图片

    Args:
        image (Picture)   : 图片流. 有格式要求.
        credential (Credential): 凭据
    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_bili_jct()
    credential.raise_for_no_sessdata()
    api = API["send"]["upwatermark"]

    files = {"binary": open(image._write_to_temp_file(), "rb")}

    return_info = await Api(**api, credential=credential, wbi=True).request(files=files)
    return return_info


async def upcover(image: Picture, credential: Credential) -> dict:
    """上传专栏段落图片

    Args:
        image (Picture)   : 图片流. 有格式要求.
        credential (Credential): 凭据
    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_bili_jct()
    credential.raise_for_no_sessdata()
    api = API["send"]["upcover"]

    data = {"filename": f"read-editor-{int(time.time() * 1000)}"}
    files = {"binary": open(image._write_to_temp_file(), "rb")}

    return_info = await Api(**api, credential=credential, wbi=True).update_data(**data).request(files=files)
    return return_info


class Cover(Picture):
    """封面图片

    """

    def json2(self):
        """转化为新版编辑器上传所需的数据格式

        """
        result = {"url": self.url}
        if self.width:
            result["width"] = self.width
        if self.height:
            result["height"] = self.height
        if self.size:
            result["size"] = self.size
        return result

    def to_insert2(self) -> dict:
        """转化为新版编辑器保存草稿所需的数据格式

        """
        return {
            "attributes": {
                "class": "normal-img"
            },
            "insert": {
                "native-image": {
                    "alt": "read-normal-img",
                    "url": self.url,
                    "width": self.width,
                    "height": self.height,
                    "size": self.size,
                    "status": "loaded"
                }
            },
            "comment": "插入的图片"
        }

    async def upcover(self, credential: Credential):
        """上传专栏段落图片

        Args:
            credential (Credential) : 凭据类
        """
        res = await upcover(self, credential)
        self.url = res["url"]
        self.size = res["size"]
        self.content = self.from_url(self.url).content
        return self

    async def upwatermark(self, credential: Credential):
        """上传获取带水印专栏段落图片

        Args:
            credential (Credential) : 凭据类
        """
        res = await upwatermark(self, credential)
        self.url = res["url"]
        self.size = res["size"]
        self.content = self.from_url(self.url).content
        return self

    async def upload_bfs(self, credential: Credential):
        """上传封面图片

        Args:
            credential (Credential) : 凭据类
        """
        return await self.upload_file(credential, data={"biz": "article", "category": "daily"})


class BaseParagraph:
    """段落基类

    Attributes:
        para_type (int) : 1 文本 2 图片 3 超链接 4 引用 5 无序列表 6 有序列表
    """
    para_type: int = None

    def json2(self) -> dict:
        """转化为新版编辑器上传所需的数据格式

        """
        pass

    def to_insert2(self) -> list:
        """转化为新版编辑器保存草稿所需的数据格式

        """
        pass


class TextParagraph(BaseParagraph):
    """文本段落

    """
    para_type = 1

    def __init__(self, nodes: List[BaseNode2],
                 align: Align = Align.left):
        """
        Args:
            nodes (List[BaseNode2]) : BaseNode2 组成的列表
            align (Align) : 段落对齐方向
        """

        raise_for_statement(
            len(nodes) != 0,
            "nodes 至少包含一个 Node"
        )

        self.nodes = nodes
        self.align = align.value

    def json2(self) -> dict:
        result = {"para_type": self.para_type, "text": {"nodes": [i.json2() for i in self.nodes]}}
        if self.align:
            result["format"] = {"align": self.align}
        return result

    def to_insert2(self) -> list:
        insert_list = [i.to_insert2() for i in self.nodes]
        first_font_size = self.nodes[0].font_size
        last = {"attributes": {}}
        if self.align:
            last["attributes"]["align"] = Align(self.align).name
        if first_font_size == FontSize.Header_2:
            header = 2
        elif first_font_size == FontSize.Header_1:
            header = 1
        else:
            header = 0
        if header != 0:
            last["attributes"]["header"] = header
        if len(last["attributes"]) == 0:
            last.pop("attributes")
        last.update({"insert": "\n"})

        insert_list.append(last)
        return insert_list


class PicParagraph(BaseParagraph):
    """图片段落

    """
    para_type = 2

    def __init__(self, pics: List[Cover]):
        """
        Args:
            pics (List[Cover]) : Cover 组成的列表
        """
        raise_for_statement(
            len(pics) != 0,
            "pics 至少包含一个 Cover"
        )
        self.pics = pics

    def json2(self):
        return {
            "para_type": self.para_type,
            "pic": {
                "style": 1,
                "pics": [i.json2() for i in self.pics]
            }
        }

    def to_insert2(self) -> list:
        result = [i.to_insert2() for i in self.pics]
        result.append({"insert": "\n"})
        return result


class LineParagraph(BaseParagraph):
    """分割线段落

    """
    para_type = 3

    def __init__(self, line: LineType):
        """
        Args:
            line (LineType) : 分割线类型
        """
        self.line = line

    def json2(self):
        return {"para_type": self.para_type, "format": {"align": 1}, "line": self.line.value}

    def to_insert2(self) -> list:
        result = {
            "attributes": {
                "class": "cut-off"
            },
            "insert": {
                "cut-off": {
                    "type": self.line.name[1:],
                    "url": self.line.value["url"]
                }
            }
        }
        return [result, {"insert": "\n"}]


class TextQuoteParagraph(TextParagraph):
    """引用文本段落

    """
    para_type = 4

    def to_insert2(self) -> list:
        insert_list = [i.to_insert2() for i in self.nodes]
        last = {"attributes": {"blockquote": True}, "insert": "\n"}
        if self.align:
            last["attributes"]["align"] = Align(self.align).name
        insert_list.append(last)
        return insert_list


class ListOLParagraph(BaseParagraph):
    """无序列表段落

    """
    para_type = 5

    def __init__(self, nodes: List[BaseNode2],
                 order: int,
                 align: Align = Align.left):
        """
        Args:
            nodes (List[BaseNode2]) : BaseNode2 组成的列表
            align (Align) : 段落对齐方向
        """
        raise_for_statement(
            len(nodes) != 0,
            "nodes 至少包含一个 Node"
        )
        self.nodes = nodes
        self.order = order
        self.align = align.value

    def json2(self):
        result = {
            "para_type": self.para_type,
            "text": {"nodes": [i.json2() for i in self.nodes]},
            "format": {"list_format": {"level": 1, "order": self.order}}
        }
        if self.align:
            result["format"]["align"] = self.align
        return result

    def to_insert2(self) -> list:
        insert_list = [i.to_insert2() for i in self.nodes]
        last = {"attributes": {"list": "bullet"}, "insert": "\n"}
        if self.align:
            last["attributes"]["align"] = Align(self.align).name
        insert_list.append(last)
        return insert_list


class ListULParagraph(ListOLParagraph):
    """有序列表段落

    """
    para_type = 6

    def to_insert2(self) -> list:
        insert_list = [i.to_insert2() for i in self.nodes]
        last = {"attributes": {"list": "ordered"}, "insert": "\n"}
        if self.align:
            last["attributes"]["align"] = Align(self.align).name
        insert_list.append(last)
        return insert_list


class ArticleCreator:
    """创建专栏的类

    """

    def __init__(self, title: str,
                 category_id: int,
                 paragraphs: List[BaseParagraph] = (),
                 *,
                 list_id: int = 0,
                 originality: bool = False,
                 reproduced: bool = False,
                 cover: List[Cover] = (),
                 biz_tags: List[str] = (),
                 up_reply_closed: bool = False,
                 comment_selected: bool = False,
                 timer_pub_time: int = 0,
                 draft_id: int = None,
                 credential: Credential = None):
        """
        Args:
            title (str) : 专栏标题
            category_id (int) : 专栏所属分类
            paragraphs (List[BaseParagraph]) : BaseParagraph 组成的段落
            list_id (int) : 专栏所属文集的 id
            originality (bool) : 是否原创
            reproduced (bool) : 允许转载
            cover (List[Cover]) : 封面图片
            biz_tags (List[str]) : 标签列表
            up_reply_closed (bool) : 关闭评论区
            comment_selected (bool) : 精选评论
            timer_pub_time: (int) : 定时发布时间戳（秒），可选时间为当前+2小时~7天内，设置时间以北京时间UTC+8为准
            draft_id: (int) : 所用草稿的字符串 id，会同时删除该草稿
            credential (BaseParagraph) : 凭据类
        """
        self.credential: Credential = (
            credential if credential is not None else Credential()
        )
        self.__title = title
        self.__paragraphs = paragraphs
        self.__category_id = category_id
        self.__list_id = list_id
        self.__originality = originality
        self.__reproduced = reproduced
        self.__cover = cover
        self.__biz_tags = biz_tags
        self.__up_reply_closed = up_reply_closed
        if not up_reply_closed:
            self.__comment_selected = comment_selected
        self.__timer_pub_time = timer_pub_time
        self.__draft_id = draft_id
        self.__type = ArticleType.SPECIAL_ARTICLE
        self.__insert_list = []

        for i in self.__paragraphs:
            self.__insert_list += i.to_insert2()

    def add_paragraph(self, *args: BaseParagraph):
        """在已有段落后面新增段落

        Args:
            *args (BaseParagraph) : BaseParagraph 组成的元组
        """
        for paragraph in args:
            self.__paragraphs.append(paragraph)
            self.__insert_list += paragraph.to_insert2()

    async def create_opus(self):
        """创建专栏

        """
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_dedeuserid()
        self.credential.raise_for_no_bili_jct()

        raise_for_statement(
            len(self.__paragraphs) != 0,
            "专栏至少包含一个 BaseParagraph"
        )

        api = API["send"]["create"]

        data = {
            "raw_content": json.dumps({"ops": self.__insert_list}, ensure_ascii=False),
            "opus_req": {
                "upload_id": f"{self.credential.dedeuserid}_{int(time.time())}_{random.randint(1000, 9999)}",
                "opus": {
                    "opus_source": ArticleType.NOTE.value,
                    "title": self.__title,
                    "content": {
                        "paragraphs": [i.json2() for i in self.__paragraphs]
                    },
                    "article": {
                        "category_id": self.__category_id,
                        "list_id": self.__list_id,
                        "originality": 1 if self.__originality else 0,
                        "reproduced": 1 if self.__reproduced else 0,
                        "biz_tags": self.__biz_tags
                    },
                    "pub_info": {}
                },
                "scene": 12,
                "meta": {
                    "app_meta": {
                        "from": "create.article.web",
                        "mobi_app": "web"
                    }
                },
                "option": {}
            }
        }
        if len(self.__cover) != 0:
            data["opus_req"]["opus"]["article"]["cover"] = self.__cover
        if self.__up_reply_closed:
            data["opus_req"]["option"]["up_reply_closed"] = 1
        else:
            if self.__comment_selected:
                data["opus_req"]["option"]["comment_selected"] = 1
        if self.__timer_pub_time:
            data["opus_req"]["option"]["timer_pub_time"] = self.__timer_pub_time

        if self.__draft_id:
            data["draft_id_str"] = str(self.__draft_id)

        params = {"gaia_source": "main_web", "csrf": self.credential.bili_jct}

        return (await Api(**api, credential=self.credential, wbi=True, ensure_ascii=False)
                .update_params(**params)
                .update_data(**data).result)

    @property
    def _text_total_number(self):
        """总字数（包括不可见字符）

        """
        total = 0
        for i in self.__insert_list:
            if isinstance(i["insert"], str):
                total += len(i["insert"])
        return total - 1

    async def draft(self, banner_url: str = None):
        """保存草稿

        Args:
            banner_url (str) : 横幅封面
        """
        api = API["send"]["draft"]
        biz_tags = ""
        for i in self.__biz_tags:
            biz_tags += f",{i}"
        biz_tags = biz_tags[1:]
        data = {
            "type": 3,
            "aid": self.__draft_id,
            "title": self.__title,
            "banner_url": banner_url,
            "content": json.dumps({"ops": self.__insert_list}, ensure_ascii=False),
            "summary": None,
            "words": self._text_total_number,
            "category": self.__category_id,
            "list_id": self.__list_id,
            "tid": 3,
            "reprint": 1 if self.__reproduced else 0,
            "tags": biz_tags,
            "image_urls": self.__cover[0] if 0 < len(self.__cover) else None,
            "origin_image_urls": self.__cover[0] if 0 < len(self.__cover) else None,
            "media_id": 0,
            "spoiler": 0,
            "action": 1,
            "original": 1 if self.__originality else 0,
            "dynamic_intro": "",
            "top_video_bvid": None,
            "up_reply_closed": 1 if self.__up_reply_closed else 0,
            "comment_selected": 1 if self.__comment_selected else 0
        }

        return await Api(**api, credential=self.credential, wbi=True).update_data(**data).result
