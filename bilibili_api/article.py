"""
bilibili_api.article

专栏相关
"""

from copy import copy
import json
from enum import Enum
from typing import List, overload, Union

import httpx
from .utils.utils import get_api
from .utils.credential import Credential
from .note import Note, NoteType
import re
from html import unescape

import yaml
from yarl import URL
from .utils.network_httpx import get_session, request
from .exceptions.NetworkException import NetworkException, ApiException
from bs4 import BeautifulSoup, element
from datetime import datetime
from urllib.parse import unquote
from typing import TypeVar

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

    - ARTICLE        : 普通专栏
    - NOTE           : 笔记专栏
    - SPECIAL_ARTICLE: 特殊专栏，采用笔记格式
    """

    ARTICLE = 0
    NOTE = 2
    SPECIAL_ARTICLE = 3


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
    return await request("GET", api["url"], params=params)


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
        self.credential = credential

    def get_rlid(self) -> int:
        return self.__rlid

    async def get_content(self) -> dict:
        """
        获取专栏文集文章列表

        Returns:
            dict: 调用 API 返回的结果
        """
        credential = self.credential if self.credential is not None else Credential()

        api = API["info"]["list"]
        params = {"id": self.__rlid}
        return await request("GET", api["url"], params, credential=credential)


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
        api = API["info"]["view"]
        params = {"id": self.__cvid}
        resp = httpx.request(
            "GET", api["url"], params=params, cookies=self.credential.get_cookies()
        ).json()

        # 设置专栏类别
        if resp["code"] != 0:
            self.__type = ArticleType.ARTICLE
        elif resp["data"]["type"] == 0:
            self.__type = ArticleType.ARTICLE
        elif resp["data"]["type"] == 2:
            self.__type = ArticleType.NOTE
        else:
            self.__type = ArticleType.SPECIAL_ARTICLE

    def get_cvid(self) -> int:
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
        return self.__type == ArticleType.NOTE

    def turn_to_note(self) -> Note:
        assert self.__type == ArticleType.NOTE
        return Note(
            cvid=self.__cvid, note_type=NoteType.PUBLIC, credential=self.credential
        )

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
                                # print(e.text.replace("\n", ""))
                                # print()
                                node = TextNode(e.text)
                                # print("Add a text node: ", e.text)
                                node_list.append(node)
                                node.children = parse(e)  # type: ignore

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
                        from .utils.parse_link import parse_link, ResourceType

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
                        node.aid = json.loads(
                            httpx.get(
                                "https://hd.biliplus.com/api/cidinfo?cid="
                                + str(field["insert"]["tag"]["cid"])
                            ).text
                        )["data"]["cid"]
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

        # 解析正文
        if self.__type != ArticleType.SPECIAL_ARTICLE:
            self.__children = await parse(document.find("div"))  # type: ignore
        else:
            s = resp["readInfo"]["content"]
            s = unescape(s)
            parse_note(json.loads(s)["ops"])

        self.__has_parsed = True

    async def get_info(self) -> dict:
        """
        获取专栏信息

        Returns:
            dict: 调用 API 返回的结果
        """

        api = API["info"]["view"]
        params = {"id": self.__cvid}
        resp = await request(
            "GET", api["url"], params=params, credential=self.credential
        )
        return resp

    async def get_all(self) -> dict:
        """
        一次性获取专栏尽可能详细数据，包括原始内容、标签、发布时间、标题、相关专栏推荐等

        Returns:
            dict: 调用 API 返回的结果
        """
        sess = get_session()
        resp = await sess.get(
            f"https://www.bilibili.com/read/cv{self.__cvid}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
                "cookie": "opus-goback=1",
            },
        )
        if resp.status_code == 200:
            html = resp.text

            match = re.search("window\.__INITIAL_STATE__=(\{.+?\});", html, re.I)  # type: ignore

            if not match:
                raise ApiException("找不到信息")

            data = json.loads(match[1])

            return data

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
        return await request("POST", api["url"], data=data, credential=self.credential)

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
        return await request("POST", api["url"], data=data, credential=self.credential)

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
        return await request("POST", api["url"], data=data, credential=self.credential)

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
        return f" *{text}*"

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
