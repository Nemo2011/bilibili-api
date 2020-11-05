r"""
模块： article
功能： 专栏各种信息操作
项目GitHub地址：https://github.com/Passkou/bilibili_api
项目主页：https://passkou.com/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/

"""
import os

from . import exceptions, utils, common
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
import datetime
import json
import re

API = utils.get_api()


# 评论相关


def get_comments_g(cv: int, order: str = "time", verify: utils.Verify = None):
    """
    获取评论
    :param cv: cv号
    :param order:
    :param verify:
    :return:
    """
    replies = common.get_comments(cv, "article", order, verify)
    return replies


def get_sub_comments_g(cv: int, root: int, verify: utils.Verify = None):
    """
    获取评论下的评论
    :param cv:
    :param root: 根评论ID
    :param verify:
    :return:
    """
    return common.get_sub_comments(cv, "article", root, verify=verify)


def send_comment(text: str, cv: int, root: int = None, parent: int = None,
                 verify: utils.Verify = None):
    """
    发送评论
    :param cv:
    :param parent: 回复谁的评论的rpid（若不填则对方无法收到回复消息提醒）
    :param root: 根评论rpid，即在哪个评论下面回复
    :param text: 评论内容，为回复评论时不会自动使用`回复 @%用户名%：%回复内容%`这种格式，目前没有发现根据rpid获取评论信息的API
    :param verify:
    :return:
    """
    resp = common.send_comment(text, cv, "article", root, parent, verify=verify)
    return resp


def set_like_comment(rpid: int, cv: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论点赞状态
    :param cv:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    resp = common.operate_comment("like", cv, "article", rpid, status, verify=verify)
    return resp


def set_hate_comment(rpid: int, cv: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论点踩状态
    :param cv:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    resp = common.operate_comment("hate", cv, "article", rpid, status, verify=verify)
    return resp


def set_top_comment(rpid: int, cv: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论置顶状态
    :param cv:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    resp = common.operate_comment("top", cv, "article", rpid, status, verify=verify)
    return resp


def del_comment(rpid: int, cv: int, verify: utils.Verify = None):
    """
    删除评论
    :param cv:
    :param rpid:
    :param verify:
    :return:
    """
    resp = common.operate_comment("del", cv, "article", rpid, verify=verify)
    return resp


# 评论相关结束


def get_info(cv: int, verify: utils.Verify = None):
    """
    获取专栏信息
    :param cv:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["article"]["info"]["view"]
    params = {
        "id": cv
    }
    resp = utils.get(api["url"], params=params, cookies=verify.get_cookies())
    return resp


def set_like(cv: int, status: bool = True, verify: utils.Verify = None):
    """
    设置专栏点赞状态
    :param cv:
    :param status:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    assert verify.has_sess(), exceptions.BilibiliApiException(utils.MESSAGES["no_sess"])
    assert verify.has_csrf(), exceptions.BilibiliApiException(utils.MESSAGES["no_csrf"])

    api = API["article"]["operate"]["like"]
    data = {
        "id": cv,
        "type": 1 if status else 2,
        "csrf": verify.csrf
    }
    resp = utils.post(api["url"], data=data, cookies=verify.get_cookies())
    return resp


def set_favorite(cv: int, status: bool = True, verify: utils.Verify = None):
    """
    设置专栏收藏状态
    :param cv:
    :param status:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    assert verify.has_sess(), exceptions.BilibiliApiException(utils.MESSAGES["no_sess"])
    assert verify.has_csrf(), exceptions.BilibiliApiException(utils.MESSAGES["no_csrf"])

    api = API["article"]["operate"]["add_favorite"] if status else API["article"]["info"]["del_favorite"]
    data = {
        "id": cv
    }
    resp = utils.post(api["url"], data=data, cookies=verify.get_cookies())
    return resp


def add_coins(cv: int, num: int = 1, verify: utils.Verify = None):
    """
    给专栏投币
    :param cv:
    :param num:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    assert verify.has_sess(), exceptions.BilibiliApiException(utils.MESSAGES["no_sess"])
    assert verify.has_csrf(), exceptions.BilibiliApiException(utils.MESSAGES["no_csrf"])

    upid = get_info(cv)["mid"]
    api = API["article"]["operate"]["coin"]
    data = {
        "aid": cv,
        "multiply": num,
        "upid": upid,
        "avtype": 2,
        "csrf": verify.csrf
    }
    resp = utils.post(api["url"], data=data, cookies=verify.get_cookies())
    return resp


def share_to_dynamic(cv: int, content: str, verify: utils.Verify = None):
    """
    专栏转发
    :param cv:
    :param content:
    :param verify:
    :return:
    """
    resp = common.dynamic_share("article", cv, content, verify=verify)
    return resp


# 专栏爬虫


def get_content(cid: int, preview: bool = False, verify: utils.Verify = None):
    """
    获取专栏内容
    :param verify:
    :param preview: 是否为草稿ID，调试用
    :param cid:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    if not preview:
        # 拉取数据
        protocol = "https" if utils.request_settings['use_https'] else "http"
        url = f"{protocol}://www.bilibili.com/read/cv{cid}"
        resp = requests.get(url, headers=utils.DEFAULT_HEADERS, cookies=verify.get_cookies())
        if "error" in resp.url:
            raise exceptions.BilibiliException(-404, "专栏不存在")
        raw_content = resp.content.decode()
        soup = BeautifulSoup(raw_content, "lxml")

        # 分离主体并转换css为行内样式
        body = soup.select_one(".article-holder")

        # 获取标题等信息
        stat = get_info(cid)
        ld_json = json.loads(soup.select_one("script[type='application/ld+json']").string)
        meta = {}
        meta["cid"] = cid
        meta["title"] = stat["title"]
        meta["head_image"] = stat["banner_url"]
        meta["author"] = {
            "name": stat["author_name"],
            "uid": stat["mid"]
        }
        meta["stats"] = stat["stats"]
        fetch_time = datetime.datetime.strptime(resp.headers.get("date"), "%a, %d %b %Y %H:%M:%S GMT")
        meta["fetch_time"] = (fetch_time - datetime.timedelta(seconds=time.timezone)).strftime("%Y-%m-%d %H:%M:%S")
        meta["ctime"] = ld_json["pubDate"] if ld_json is not None else ""

        meta["tags"] = []
        tags = soup.select(".tag-container .tag-content")
        for tag in tags:
            meta["tags"].append(tag.string)
    else:
        # 获取草稿的数据，调试用
        stat = utils.get(f"https://api.bilibili.com/x/article/creative/draft/view?aid={cid}",
                         cookies=verify.get_cookies())
        meta = {}
        meta["cid"] = cid
        meta["title"] = stat["title"]
        meta["head_image"] = stat["banner_url"]
        meta["author"] = {
            "name": "测试用户",
            "uid": stat["author"]["mid"]
        }
        meta["stats"] = None
        meta["fetch_time"] = "None"
        meta["ctime"] = "未发布"

        meta["tags"] = stat["tags"]

        body = BeautifulSoup(f"<div>{stat['content']}</div>", "lxml")

    # 准备解析文章
    STYLE_MAP = json.loads(open(os.path.join(os.path.dirname(__file__), "data/article_style.json")).read())

    def node_handle(node, prev):
        if node is None:
            return
        if not hasattr(node, "children"):
            # 文本节点
            prev.node_list.append(TextNode(str(node)))
            return

        if node.name == "blockquote":
            # 引用
            obj = BlockquoteNode()
            prev.node_list.append(obj)
        elif node.name == "ul":
            # 无序列表
            obj = UlNode()
            prev.node_list.append(obj)
        elif node.name == "ol":
            # 有序列表
            obj = OlNode()
            prev.node_list.append(obj)
        elif node.name == "h1":
            # 标题
            obj = HeadNode(text=node.string)
            prev.node_list.append(obj)
        elif node.name == "strong":
            # 加粗
            obj = BoldNode()
            prev.node_list.append(obj)
        elif node.name == "a":
            # 链接
            u = node["href"]
            obj = UrlNode(u)
            prev.node_list.append(obj)
        elif node.name == "h1":
            # 标题
            obj = HeadNode(text=node.string)
            prev.node_list.append(obj)
        elif node.name == "span":
            style = node.get("style", [])
            cls = node.get("class", [])
            if "text-decoration: line-through;" in style:
                # 删除线
                obj = DelNode()
                prev.node_list.append(obj)
            if len(cls) > 0:
                # 行内样式处理
                obj = StyleNode()
                prev.node_list.append(obj)
                for c in cls:
                    if "font-size" in c:
                        obj.style.update(STYLE_MAP.get(c, "#000"))
                    elif "color" in c:
                        obj.style.update(STYLE_MAP.get(c, "16px"))
        elif node.name == "img":
            cls = node.get("class", [])
            if "video-card" in cls:
                # 视频卡片
                aids = node["aid"].split(",")
                for aid in aids:
                    bvid = utils.aid2bvid(int(aid))
                    obj = VideoCardNode(id_=bvid)
                    prev.node_list.append(obj)
            elif "article-card" in cls:
                # 专栏卡片
                aids = node["aid"].split(",")
                for aid in aids:
                    obj = ArticleCardNode(id_=aid)
                    prev.node_list.append(obj)
            elif "fanju-card" in cls:
                # 番剧卡片
                aids = node["aid"].split(",")
                for aid in aids:
                    obj = BangumiCardNode(id_=aid)
                    prev.node_list.append(obj)
            elif "music-card" in cls:
                # 音乐卡片
                aids = node["aid"].split(",")
                for aid in aids:
                    obj = MusicCardNode(id_=aid)
                    prev.node_list.append(obj)
            elif "shop-card" in cls:
                # 会员购卡片
                aids = node["aid"].split(",")
                for aid in aids:
                    obj = ShopCardNode(id_=aid)
                    prev.node_list.append(obj)
            elif "live-card" in cls:
                # 直播卡片
                aids = node["aid"].split(",")
                for aid in aids:
                    obj = LiveCardNode(id_=aid)
                    prev.node_list.append(obj)
            elif "caricature-card" in cls:
                # 漫画卡片
                aids = node["aid"].split(",")
                for aid in aids:
                    obj = ComicCardNode(id_=aid)
                    prev.node_list.append(obj)
            elif "vote-display" in cls:
                # 投票卡片
                vote_id = int(node["data-vote-id"])
                info = common.get_vote_info(vote_id)["info"]
                obj = VoteNode(vote_id, info)
                prev.node_list.append(obj)
            else:
                if len(cls) > 0:
                    if "cut-off" in cls[0]:
                        # 分割线
                        obj = SeparatorNode()
                        prev.node_list.append(obj)
                else:
                    # 图片
                    u = node["data-src"] if node["data-src"].startswith("http:") \
                                             or node["data-src"].startswith("https:") \
                        else "https:" + node["data-src"]
                    obj = ImageNode(url=u, alt=node.next.string)
                    prev.node_list.append(obj)
        elif node.name == "li":
            # 列表元素
            obj = LiNode()
            prev.node_list.append(obj)
        elif node.name == "p":
            # 对齐方式处理
            obj = prev
            style = node.get("style", "").split(";")
            for sty in style:
                if "text-align" in sty:
                    name, value = sty.split(": ")
                    if type(obj) == Paragraph:
                        obj.align = value
        elif node.name in ["figcaption"]:
            # 忽略处理节点
            return
        else:
            # 其他节点
            obj = prev

        for child in node.children:
            # 处理子节点
            node_handle(child, obj)

    article = Article(meta=meta)
    for p in body.children:
        para = Paragraph()
        article.paragraphs.append(para)
        node_handle(p, para)
    return article


async def _image_downloader(session, url, save_path):
    async with session.request("GET", url) as resp:
        with open(os.path.join(save_path, url.split("/")[-1]), "wb") as f:
            content = await resp.read()
            f.write(content)


async def _image_downloader_main(urls, save_path):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(_image_downloader(session, url, save_path))
            tasks.append(task)
        for task in tasks:
            await task


class Article(object):
    def __init__(self, meta: dict = None, paragraphs: list = None):
        self.meta = meta if meta else {}
        self.paragraphs = paragraphs if paragraphs else []

    def __str__(self):
        t = ""
        if len(self.meta['head_image']) > 0:
            t += f"![头图]({self.meta['head_image']})\n"
        t += f"# {self.meta['title']}"
        t += "\n\n"
        t += f"[原文链接](https://www.bilibili.com/read/cv{self.meta['cid']})"
        t += "\n\n"
        t += f"作者：[{self.meta['author']['name']}](https://space.bilibili.com/{self.meta['author']['uid']})    " \
             f"发布时间：{self.meta['ctime']}    抓取时间：{self.meta['fetch_time']}"
        t += f"\n\n"
        t += f"标签：{' '.join(self.meta['tags'])}"
        t += f"\n\n"
        t += "***\n"
        # 正文
        t += "\n\n".join([str(node) for node in self.paragraphs])
        return t

    def save_as_markdown(self, path: str):
        save_path = os.path.join(path, f"cv{self.meta['cid']}")
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        # 图片替换成本地路径
        urls = []
        for para in self.paragraphs:
            for node in para.node_list:
                if type(node) == ImageNode:
                    urls.append(node.url)
                    img_name = node.url.split('/')[-1]
                    node.url = "./" + img_name
        # 头图替换
        if len(self.meta['head_image']) > 0:
            urls.append(self.meta['head_image'])
            img_name = self.meta['head_image'].split('/')[-1]
            self.meta['head_image'] = "./" + img_name
        # 开始请求
        asyncio.get_event_loop().run_until_complete(_image_downloader_main(urls, save_path))
        # 保存markdown
        md = self.__str__()
        with open(os.path.join(save_path, f"cv{self.meta['cid']}.md"), "w", encoding="utf8") as f:
            f.write(md)

        # 保存meta
        with open(os.path.join(save_path, "meta.json"), "w", encoding="utf8") as f:
            f.write(json.dumps(self.meta, indent=4, ensure_ascii=False))


class Paragraph(object):
    def __init__(self, align: str = "left", node_list: list = None):
        self.node_list = node_list if node_list else []
        self.align = align

    def __len__(self):
        return len(self.node_list)

    def __str__(self):
        content = "".join([str(node) for node in self.node_list])
        if self.align == "left":
            t = content
        else:
            t = f"<p style='text-align: {self.align}'>{content}</p>"
        return t


class AbstractNode(object):
    def __init__(self, **kwargs):
        pass


class TextNode(AbstractNode):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)


class AbstractListNode(AbstractNode):
    def __init__(self, node_list: list = None, **kwargs):
        self.node_list = node_list if node_list else []
        super().__init__(**kwargs)

    def __len__(self):
        return len(self.node_list)

    def __str__(self):
        return "\n".join([str(node) for node in self.node_list])


class StyleNode(AbstractListNode):
    def __init__(self, style: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.style = style if style else {}

    def __str__(self):
        text = "".join([str(node) for node in self.node_list])
        style = ";".join([f"{name}: {value}" for name, value in self.style.items()])
        if len(text) == 0:
            return ""
        node_name = "p" if "text-align" in self.style else "span"
        return f'<{node_name} style="{style}">{text}</{node_name}>'


class HeadNode(AbstractListNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        text = ''.join([str(node) for node in self.node_list])
        if len(text) == 0:
            return ""
        return f"## {text}"


class ItalicNode(AbstractListNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        text = ''.join([str(node) for node in self.node_list])
        if len(text) == 0:
            return ""
        return f"*{text}*"


class BoldNode(AbstractListNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        t = ''.join([str(node) for node in self.node_list])
        if len(t) == 0 or re.match(r"\s+", t):
            t = " "
        else:
            t = f" **{t}**"
        return t


class DelNode(AbstractListNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        text = ''.join([str(node) for node in self.node_list])
        if len(text) == 0:
            return ""
        return f"~~{text}~~"


class BlockquoteNode(AbstractListNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return '\n'.join(['> ' + str(node) for node in self.node_list])


class UlNode(AbstractListNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return '\n'.join(["- " + str(node) for node in self.node_list])


class OlNode(AbstractListNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        t = []
        for i, node in enumerate(self.node_list):
            t.append(f"{i + 1}. {str(node)}")
        return '\n'.join(t)


class LiNode(AbstractListNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return "".join([str(node) for node in self.node_list])


class ImageNode(AbstractNode):
    def __init__(self, url: str, alt: str, **kwargs):
        self.url = url
        self.alt = alt if alt else ""
        super().__init__(**kwargs)

    def __str__(self):
        return f"![{self.alt}]({self.url} \"{self.alt}\")"


# 卡片


class AbstractCardNode(AbstractNode):
    def __init__(self, id_: str, **kwargs):
        self.id = id_
        super().__init__(**kwargs)


class VideoCardNode(AbstractCardNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"<https://www.bilibili.com/{self.id}>"


class ArticleCardNode(AbstractCardNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"<https://www.bilibili.com/read/cv{self.id}>"


class BangumiCardNode(AbstractCardNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"<https://www.bilibili.com/bangumi/play/{self.id}>"


class MusicCardNode(AbstractCardNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"<https://www.bilibili.com/audio/{self.id}>"


class ShopCardNode(AbstractCardNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"<https://show.bilibili.com/platform/detail.html?id={self.id[2:]}>"


class ComicCardNode(AbstractCardNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"<https://manga.bilibili.com/m/detail/mc{self.id}>"


class LiveCardNode(AbstractCardNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return f"<https://live.bilibili.com/{self.id}>"


class VoteNode(AbstractNode):
    def __init__(self, vote_id: int, info: dict, **kwargs):
        self.info = info
        self.vote_id = vote_id
        super().__init__(**kwargs)

    def __str__(self):
        t = [
            "## 投票",
            f"{self.info['title']}\n",
            f"发起者： [{self.info['name']}](https://space.bilibili.com/{self.info['uid']})\n",
            f"选项：",
            "\n".join(["- " + op['desc'] for op in self.info["options"]]),
            "\n---"
        ]
        return "\n".join(t)


class UrlNode(AbstractListNode):
    def __init__(self, url: str, **kwargs):
        self.url = url
        super().__init__(**kwargs)

    def __str__(self):
        text = "".join([str(node) for node in self.node_list])
        return f"<{self.url}>" if len(text) == 0 else f"[{text}]({self.url})"


class SeparatorNode(AbstractNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return "\n***\n"
