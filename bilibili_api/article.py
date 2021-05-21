

from bilibili_api.utils.utils import get_api
from bilibili_api.utils.Credential import Credential
from bilibili_api_old.exceptions import BilibiliApiException
import json
import re

import yaml
from bilibili_api.utils.network import get_session, request
from bilibili_api.exceptions.NetworkException import NetworkException
from bs4 import BeautifulSoup, element
from datetime import datetime
from bilibili_api.utils.Color import Color
from copy import copy
from urllib.parse import unquote

API = get_api('article')


ARTICLE_COLOR_MAP = {
    'blue-01': Color('56c1fe'),
    'lblue-01': Color('73fdea'),
    'green-01': Color('89fa4e'),
    'yellow-01': Color('fff359'),
    'pink-01': Color('ff968d'),
    'purple-01': Color('ff8cc6'),

    'blue-02': Color('02a2ff'),
    'lblue-02': Color('18e7cf'),
    'green-02': Color('60d837'),
    'yellow-02': Color('fbe231'),
    'pink-02': Color('ff654e'),
    'purple-02': Color('ef5fa8'),

    'blue-03': Color('0176ba'),
    'lblue-03': Color('068f86'),
    'green-03': Color('1db100'),
    'yellow-03': Color('f8ba00'),
    'pink-03': Color('ee230d'),
    'purple-03': Color('cb297a'),

    'blue-04': Color('004e80'),
    'lblue-04': Color('017c76'),
    'green-04': Color('017001'),
    'yellow-04': Color('ff9201'),
    'pink-04': Color('b41700'),
    'purple-04': Color('99195e'),

    'gray-01': Color('d6d5d5'),
    'gray-02': Color('929292'),
    'gray-03': Color('5f5f5f'),
}

class Article:
    def __init__(self, cvid: int, credential: Credential = None):
        self.children = []
        self.credential = credential if credential is not None else Credential()
        self.meta = {
            "title": None,
            "author_name": None,
            "author_space": None,
            "ctime": None,
            "banner": None,
            "category": None,
            "tags": None,
            "cvid": cvid
        }
        self._has_parsed = False

    def markdown(self):
        """
        转换为 Markdon

        Returns:
            str
        """
        if not self._has_parsed: raise BilibiliApiException('请先调用 get_content()')

        content = "".join([node.markdown() for node in self.children])

        meta_yaml = yaml.safe_dump(self.meta, allow_unicode=True)
        content = f"---\n{meta_yaml}\n---\n\n{content}"
        return content

    def json(self):
        """
        转换为 JSON 数据
        """
        if not self._has_parsed: raise BilibiliApiException('请先调用 get_content()')

        return {
            "type": "Article",
            "meta": self.meta,
            "children": list(map(lambda x: x.json(), self.children))
        }

    async def get_content(self):
        """
        解析专栏内容

        Args:
            cv (int): [description]
        """
        session = get_session()
        resp = await session.get(f'https://www.bilibili.com/read/cv{self.meta["cvid"]}')

        resp.raise_for_status()
        html = (await resp.read()).decode()

        if '页面不存在或已被删除' in html:
            raise NetworkException(404, '专栏不存在')

        document = BeautifulSoup(html, 'lxml')

        def find_meta():
            """
            收集元数据
            """
            meta = {}

            head_el: BeautifulSoup = document.select_one('.head-container')
            ldjson_el: BeautifulSoup = document.select_one('script[type="application/ld+json"]')

            ldjson_text: str = ldjson_el.contents[0]

            meta['cvid'] = self.meta['cvid']

            # 替换制表符为空格
            ldjson_text = ldjson_text.replace('\t', '    ')
            ldjson = json.loads(ldjson_text)

            # 标题
            meta['title'] = ldjson['title']

            # 分区
            category_el: BeautifulSoup = head_el.select_one('.category-link')
            meta['category'] = category_el.text.strip()

            # 发布时间
            ctime_el: BeautifulSoup = head_el.select_one('.create-time')
            meta['ctime'] = datetime.fromtimestamp(int(ctime_el.attrs['data-ts'])).strftime("%Y-%m-%d %H:%M:%S")

            author_el: BeautifulSoup = document.select_one('.author-container')

            # 作者名字
            author_name_el: BeautifulSoup = author_el.select_one('.author-name')
            meta['author_name'] = author_name_el.text.strip()

            # 作者空间地址
            meta['author_space'] = 'https:' + author_name_el.attrs['href']

            # 头图
            meta['banner'] = ldjson['images']

            # 标签
            tags_items_el = document.select('.tag-container .tag-content')
            meta['tags'] = []
            for tag_el in tags_items_el:
                meta['tags'].append(tag_el.contents[0].strip())

            return meta

        def parse(el: BeautifulSoup):
            node_list = []

            for e in el.contents:
                if type(e) == element.NavigableString:
                    # 文本节点
                    node = TextNode(e)
                    node_list.append(node)
                    continue

                e: BeautifulSoup = e
                if e.name == 'p':
                    # 段落
                    node = ParagraphNode()
                    node_list.append(node)

                    if 'style' in e.attrs:
                        if 'text-align: center' in e.attrs['style']:
                            node.align = 'center'

                        elif 'text-align: right' in e.attrs['style']:
                            node.align = 'right'

                        else:
                            node.align = 'left'

                    node.children = parse(e)

                elif e.name == 'h1':
                    # 标题
                    node = HeadingNode()
                    node_list.append(node)

                    node.children = parse(e)

                elif e.name == 'strong':
                    # 粗体
                    node = BoldNode()
                    node_list.append(node)

                    node.children = parse(e)

                elif e.name == 'span':
                    # 各种样式

                    if 'style' in e.attrs:
                        style = e.attrs['style']

                        if 'text-decoration: line-through' in style:
                            # 删除线
                            node = DelNode()
                            node_list.append(node)

                            node.children = parse(e)

                    elif 'class' in e.attrs:
                        className = e.attrs['class'][0]

                        if 'font-size' in className:
                            # 字体大小
                            node = FontSizeNode()
                            node_list.append(node)

                            node.size = int(re.search('font-size-(\d\d)', className)[1])
                            node.children = parse(e)

                        elif 'color' in className:
                            # 字体颜色
                            node = ColorNode()
                            node_list.append(node)

                            color_text = re.search('color-(.*);?', className)[1]
                            node.color = copy(ARTICLE_COLOR_MAP[color_text])

                            node.children = parse(e)

                elif e.name == 'blockquote':
                    # 引用块
                    node = BlockquoteNode()
                    node_list.append(node)

                    node.children = parse(e)

                elif e.name == 'figure':
                    if 'class' in e.attrs:
                        className = e.attrs['class']

                        if 'img-box' in className:
                            img_el: BeautifulSoup = e.find('img')

                            if 'class' in img_el.attrs:
                                className = img_el.attrs['class']

                                if 'cut-off' in className:
                                    # 分割线
                                    node = SeparatorNode()
                                    node_list.append(node)

                                if 'aid' in img_el.attrs:
                                    # 各种卡片
                                    aid = img_el.attrs['aid']

                                    if 'video-card' in className:
                                        # 视频卡片，考虑有两列视频
                                        for a in aid.split(','):
                                            node = VideoCardNode()
                                            node_list.append(node)

                                            node.aid = int(a)

                                    elif 'article-card' in className:
                                        # 文章卡片
                                        node = ArticleCardNode()
                                        node_list.append(node)

                                        node.cvid = int(aid)

                                    elif 'fanju-card' in className:
                                        # 番剧卡片
                                        node = BangumiCardNode()
                                        node_list.append(node)

                                        node.epid = int(aid[2:])

                                    elif 'music-card' in className:
                                        # 音乐卡片
                                        node = MusicCardNode()
                                        node_list.append(node)

                                        node.auid = int(aid[2:])

                                    elif 'shop-card' in className:
                                        # 会员购卡片
                                        node = ShopCardNode()
                                        node_list.append(node)

                                        node.pwid = int(aid[2:])

                                    elif 'caricature-card' in className:
                                        # 漫画卡片，考虑有两列

                                        for i in aid.split(','):
                                            node = ComicCardNode()
                                            node_list.append(node)

                                            node.mcid = int(i)

                                    elif 'live-card' in className:
                                        # 直播卡片
                                        node = LiveCardNode()
                                        node_list.append(node)

                                        node.room_id = int(aid)
                            else:
                                # 图片节点
                                node = ImageNode()
                                node_list.append(node)

                                node.url = "https:" + e.find('img').attrs['data-src']

                                figcaption_el: BeautifulSoup = e.find('figcaption')

                                if figcaption_el.contents:
                                    node.alt = figcaption_el.contents[0]

                        elif 'code-box' in className:
                            # 代码块
                            node = CodeNode()
                            node_list.append(node)

                            pre_el: BeautifulSoup = e.find('pre')
                            node.lang = pre_el.attrs['data-lang'].split('@')[0].lower()
                            node.code = unquote(pre_el.attrs['codecontent'])

                elif e.name == 'ol':
                    # 有序列表
                    node = OlNode()
                    node_list.append(node)

                    node.children = parse(e)

                elif e.name == 'li':
                    # 列表元素
                    node = LiNode()
                    node_list.append(node)

                    node.children = parse(e)

                elif e.name == 'ul':
                    # 无序列表
                    node = UlNode()
                    node_list.append(node)

                    node.children = parse(e)

                elif e.name == 'a':
                    # 超链接
                    node = AnchorNode()
                    node_list.append(node)

                    node.url = e.attrs['href']
                    node.text = e.contents[0]

                elif e.name == 'img':
                    className = e.attrs['class']

                    if 'latex' in className:
                        # 公式
                        node = LatexNode()
                        node_list.append(node)

                        node.code = unquote(e['alt'])

            return node_list

        # 解析文章元数据
        self.meta = find_meta()

        # 解析正文
        body = document.select_one('.article-holder')
        self.children =  parse(body)

        self._has_parsed = True

    async def get_info(self):
        """
        获取专栏信息
        """

        api = API["info"]["view"]
        params = {
            "id": self.meta['cvid']
        }
        return await request('GET', api['url'], params=params, credential=self.credential)


    async def set_like(self, status: bool = True):
        """
        设置专栏点赞状态

        Args:
            status (bool, optional): 点赞状态. Defaults to True
        """
        self.credential.raise_for_no_sessdata()

        api = API["operate"]["like"]
        data = {
            "id": self.meta['cvid'],
            "type": 1 if status else 2
        }
        return await request('POST', api['url'], data=data, credential=self.credential)


    async def set_favorite(self, status: bool = True):
        """
        设置专栏收藏状态

        Args:
            status (bool, optional): 收藏状态. Defaults to True
        """
        self.credential.raise_for_no_sessdata()

        api = API["operate"]["add_favorite"] if status else API["operate"]["del_favorite"]
        data = {
            "id": self.meta['cvid']
        }
        return await request('POST', api['url'], data=data, credential=self.credential)


    async def add_coins(self):
        """
        给专栏投币
        """
        self.credential.raise_for_no_sessdata()

        upid = (await self.get_info())["mid"]
        api = API["operate"]["coin"]
        data = {
            "aid": self.meta['cvid'],
            "multiply": 1,
            "upid": upid,
            "avtype": 2
        }
        return await request('POST', api['url'], data=data, credential=self.credential)

class ParagraphNode:
    def __init__(self):
        self.children = []
        self.align = 'left'

    def markdown(self):
        content = "".join([node.markdown() for node in self.children])
        return content + '\n\n'

    def json(self):
        return {
            "type": "ParagraphNode",
            "children": list(map(lambda x: x.json(), self.children))
        }

class HeadingNode:
    def __init__(self):
        self.children = []

    def markdown(self):
        text = ''.join([node.markdown() for node in self.children])
        if len(text) == 0:
            return ""
        return f"## {text}\n\n"

    def json(self):
        return {
            "type": "HeadingNode",
            "children": list(map(lambda x: x.json(), self.children))
        }


class BlockquoteNode:
    def __init__(self):
        self.children = []

    def markdown(self):
        t = ''.join([node.markdown() for node in self.children])

        # 填补空白行的 > 并加上标识符
        t = '\n'.join(['> ' + line for line in t.split('\n')])

        return t

    def json(self):
        return {
            "type": "BlockquoteNode",
            "children": list(map(lambda x: x.json(), self.children))
        }


class ItalicNode:
    def __init__(self):
        self.children = []

    def markdown(self):
        text = ''.join([node.markdown() for node in self.children])
        if len(text) == 0:
            return ""
        return f" *{text}*"

    def json(self):
        return {
            "type": "ItalicNode",
            "children": list(map(lambda x: x.json(), self.children))
        }

class BoldNode:
    def __init__(self):
        self.children = []

    def markdown(self):
        t = ''.join([node.markdown() for node in self.children])
        if len(t) == 0:
            return ''
        return f" **{t}**"

    def json(self):
        return {
            "type": "BoldNode",
            "children": list(map(lambda x: x.json(), self.children))
        }


class DelNode:
    def __init__(self):
        self.children = []

    def markdown(self):
        text = ''.join([node.markdown() for node in self.children])
        if len(text) == 0:
            return ""
        return f" ~~{text}~~"

    def json(self):
        return {
            "type": "DelNode",
            "children": list(map(lambda x: x.json(), self.children))
        }

class UlNode:
    def __init__(self):
        self.children = []

    def markdown(self):
        return '\n'.join(["- " + node.markdown() for node in self.children])

    def json(self):
        return {
            "type": "UlNode",
            "children": list(map(lambda x: x.json(), self.children))
        }


class OlNode:
    def __init__(self):
        self.children = []

    def markdown(self):
        t = []
        for i, node in enumerate(self.children):
            t.append(f"{i + 1}. {node.markdown()}")
        return '\n'.join(t)

    def json(self):
        return {
            "type": "OlNode",
            "children": list(map(lambda x: x.json(), self.children))
        }

class LiNode:
    def __init__(self):
        self.children = []

    def markdown(self):
        return "".join([node.markdown() for node in self.children])

    def json(self):
        return {
            "type": "LiNode",
            "children": list(map(lambda x: x.json(), self.children))
        }

class ColorNode:
    def __init__(self):
        self.color = Color('000000')
        self.children = []

    def markdown(self):
        return "".join([node.markdown() for node in self.children])

    def json(self):
        return {
            "type": "ColorNode",
            "color": self.color.get_hex_color(),
            "children": list(map(lambda x: x.json(), self.children))
        }


class FontSizeNode:
    def __init__(self):
        self.size = 16
        self.children = []

    def markdown(self):
        return "".join([node.markdown() for node in self.children])

    def json(self):
        return {
            "type": "FontSizeNode",
            "size": self.size,
            "children": list(map(lambda x: x.json(), self.children))
        }


## 特殊节点，即无子节点

class TextNode:
    def __init__(self, text: str):
        self.text = text

    def markdown(self):
        return self.text

    def json(self):
        return {
            "type": "TextNode",
            "text": self.text
        }


class ImageNode:
    def __init__(self):
        self.url = ''
        self.alt = ''

    def markdown(self):
        alt = self.alt.replace('[', '\\[')
        return f"![{alt}]({self.url})\n\n"

    def json(self):
        return {
            "type": "ImageNode",
            "url": self.url,
            "alt": self.alt
        }

class LatexNode:
    def __init__(self):
        self.code = ''

    def markdown(self):
        if ("\n" in self.code):
            # 块级公式
            return f"$$\n{self.code}\n$$"
        else:
            # 行内公式
            return f"${self.code}$"

    def json(self):
        return {
            "type": "LatexNode",
            "code": self.code
        }

class CodeNode:
    def __init__(self):
        self.code = ''
        self.lang = ''

    def markdown(self):
        return f"```{self.lang if self.lang else ''}\n{self.code}\n```\n\n"

    def json(self):
        return {
            "type": "CodeNode",
            "code": self.code,
            "lang": self.lang
        }

# 卡片


class VideoCardNode:
    def __init__(self):
        self.aid = 0

    def markdown(self):
        return f"[视频 av{self.aid}](https://www.bilibili.com/av{self.aid})\n\n"

    def json(self):
        return {
            "type": "VideoCardNode",
            "aid": self.aid
        }


class ArticleCardNode:
    def __init__(self):
        self.cvid = 0

    def markdown(self):
        return f"[文章 cv{self.cvid}](https://www.bilibili.com/read/cv{self.cvid})\n\n"

    def json(self):
        return {
            "type": "ArticleCardNode",
            "cvid": self.cvid
        }


class BangumiCardNode:
    def __init__(self):
        self.epid = 0

    def markdown(self):
        return f"[番剧 ep{self.epid}](https://www.bilibili.com/bangumi/play/ep{self.epid})\n\n"

    def json(self):
        return {
            "type": "BangumiCardNode",
            "epid": self.epid
        }


class MusicCardNode:
    def __init__(self):
        self.auid = 0

    def markdown(self):
        return f"[音乐 au{self.auid}](https://www.bilibili.com/audio/au{self.auid})\n\n"

    def json(self):
        return {
            "type": "MusicCardNode",
            "auid": self.auid
        }


class ShopCardNode:
    def __init__(self):
        self.pwid = 0

    def markdown(self):
        return f"[会员购 {self.pwid}](https://show.bilibili.com/platform/detail.html?id={self.pwid})\n\n"

    def json(self):
        return {
            "type": "ShopCardNode",
            "pwid": self.pwid
        }


class ComicCardNode:
    def __init__(self):
        self.mcid = 0

    def markdown(self):
        return f"[漫画 mc{self.mcid}](https://manga.bilibili.com/m/detail/mc{self.mcid})\n\n"

    def json(self):
        return {
            "type": "ComicCardNode",
            "mcid": self.mcid
        }


class LiveCardNode:
    def __init__(self):
        self.room_id = 0

    def markdown(self):
        return f"[直播 {self.room_id}](https://live.bilibili.com/{self.room_id})\n\n"

    def json(self):
        return {
            "type": "LiveCardNode",
            "room_id": self.room_id
        }


class AnchorNode:
    def __init__(self):
        self.url = ''
        self.text = ''

    def markdown(self):
        text = self.text.replace('[', '\\[')
        return f"[{text}]({self.url})"

    def json(self):
        return {
            "type": "AnchorNode",
            "url": self.url,
            "text": self.text
        }


class SeparatorNode:
    def __init__(self):
        pass

    def markdown(self):
        return "\n------\n"

    def json(self):
        return {
            "type": "SeparatorNode"
        }

