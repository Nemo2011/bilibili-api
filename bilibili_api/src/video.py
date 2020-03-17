from . import exception, utils
import requests
import json
from xml.dom.minidom import parseString
import math
from .utils import Danmaku, Verify, Get, Post
import re

headers = utils.default_headers
apis = utils.get_apis()


class Video:
    def __init__(self, aid):
        self.aid = aid


class VideoInfo(Video):
    def __init__(self, aid: int, verify: Verify = Verify()):
        Video.__init__(self, aid)
        if type(verify) != utils.Verify:
            raise Exception("请传入Verify类")
        else:
            self.verify = verify
        self.info = None

    def __get_self_info(self):
        if self.info is None:
            self.info = self.get_video_info()

    def get_video_info(self, is_simple: bool = False):
        if is_simple:
            api = apis["video"]["info"]["info_simple"]
        else:
            api = apis["video"]["info"]["info_detail"]
        params = {
            "aid": self.aid
        }
        get = Get(url=api["url"], params=params)
        self.info = get()
        return self.info

    # sort=0 按弹幕出现时间正序排序，其他按发送时间正序排序
    def get_danmaku(self, sort: int = 0, page: int = 0):
        api = apis["video"]["info"]["danmaku"]
        self.__get_self_info()
        page_id = self.info["pages"][page]["cid"]
        params = {
            "oid": page_id
        }
        req = requests.get(api["url"], params=params, headers=headers)
        if req.ok:
            con = req.content.decode("utf-8")
            xml = parseString(con)
            danmaku = xml.getElementsByTagName("d")
            py_danmaku = []
            for d in danmaku:
                self.info = d.getAttribute("p").split(",")
                text = d.childNodes[0].data
                if self.info[5] == '0':
                    is_sub = False
                else:
                    is_sub = True
                dm = Danmaku(
                    dm_time=self.info[0],
                    send_time=self.info[4],
                    id=self.info[6],
                    color=self.info[3],
                    mode=self.info[1],
                    font_size=self.info[2],
                    is_sub=is_sub,
                    text=text
                )
                py_danmaku.append(dm)
            if sort == 0:
                py_danmaku.sort(key=lambda x: x.dm_time.seconds)
            else:
                py_danmaku.sort(key=lambda x: x.send_time.timestamp())
            return py_danmaku
        else:
            raise exception.NetworkException(req.status_code)

    def get_history_danmaku(self, date: str, sort: int = 0, page: int = 0):
        if not self.verify.has_sess():
            raise exception.NoPermissionException("需要验证：SESSDATA")

        api = apis["video"]["info"]["history_danmaku"]
        self.__get_self_info()
        page_id = self.info["pages"][page]["cid"]
        params = {
            "type": 1,
            "date": date,
            "oid": page_id
        }
        req = requests.get(api["url"], params=params, headers=headers, cookies=self.verify.get_cookies())
        if req.ok:
            if req.headers["Content-Type"] == "application/json":
                con = req.json()
                raise exception.BiliException(con["code"], con["message"])
            con = req.content.decode("utf-8")
            xml = parseString(con)
            danmaku = xml.getElementsByTagName("d")
            py_danmaku = []
            for d in danmaku:
                self.info = d.getAttribute("p").split(",")
                text = d.childNodes[0].data
                if self.info[5] == '0':
                    is_sub = False
                else:
                    is_sub = True
                dm = Danmaku(
                    dm_time=self.info[0],
                    send_time=self.info[4],
                    id=self.info[6],
                    color=self.info[3],
                    mode=self.info[1],
                    font_size=self.info[2],
                    is_sub=is_sub,
                    text=text
                )
                py_danmaku.append(dm)
            if sort == 0:
                py_danmaku.sort(key=lambda x: x.dm_time.seconds)
            else:
                py_danmaku.sort(key=lambda x: x.send_time.timestamp())
            return py_danmaku
        else:
            raise exception.NetworkException(req.status_code)

    def get_tags(self):
        api = apis["video"]["info"]["tags"]
        params = {
            "aid": self.aid
        }
        get = Get(url=api["url"], params=params)
        return get()

    def get_history_danmaku_index(self, month: str, page: int = 0):
        if not self.verify.has_sess():
            raise exception.NoPermissionException("需要验证：SESSDATA")

        self.__get_self_info()
        page_id = self.info["pages"][page]["cid"]
        api = apis["video"]["info"]["history_danmaku_index"]
        params = {
            "oid": page_id,
            "month": month,
            "type": 1
        }
        get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        return get()

    def get_chargers(self):
        api = apis["video"]["info"]["charge"]
        self.__get_self_info()
        mid = self.info["owner"]["mid"]
        params = {
            "aid": self.aid,
            "mid": mid
        }
        get = Get(url=api["url"], params=params)
        return get()

    def get_pages(self):
        api = apis["video"]["info"]["pages"]
        params = {
            "aid": self.aid
        }
        get = Get(url=api["url"], params=params)
        return get()

    def get_playurl(self, page=0):
        self.__get_self_info()
        if page + 1 > len(self.info["pages"]):
            raise exception.bilibiliApiException("不存在该分P（page）")
        headers["Referer"] = "https://www.bilibili.com"
        url = "https://www.bilibili.com/video/av%s" % self.aid
        if self.verify.has_sess():
            req = requests.get(url, cookies=self.verify.get_cookies(), headers=headers, params={"p": page + 1})
        else:
            req = requests.get(url, headers=headers, params={"p": page + 1})
        if req.ok:
            match = re.search("<script>window.__playinfo__=(.*?)</script>", req.text)
            text = match.group(1)
            if text is not None:
                video_info = json.loads(text)
            else:
                raise Exception("出现错误")
            if video_info["code"] != 0:
                raise exception.BiliException(video_info["code"], video_info["message"])
            else:
                return video_info["data"]
        else:
            raise exception.NetworkException(req.status_code)

    # sort=0 评论时间正序排序，其他按评论点赞数倒序排序
    def get_comments(self, sort: int = 0, limit: int = 1919810):
        def get_page(page):
            api = apis["video"]["info"]["comments"]
            params = {
                "oid": self.aid,
                "type": 1,
                "sort": 2,
                "pn": page
            }
            get = Get(url=api["url"], params=params)
            return get()

        count = 0
        first_get = get_page(1)
        count += len(first_get["replies"])
        page_num = math.ceil(first_get["page"]["count"] / first_get["page"]["size"])
        replies = first_get["replies"]
        if page_num > 1 and count < limit:
            for p in range(2, page_num + 1):
                rep = get_page(p)
                replies += rep["replies"]
                count += len(rep["replies"])
                if count >= limit:
                    break
        if sort == 0:
            replies.sort(key=lambda x: x["ctime"])
        else:
            replies.sort(key=lambda x: x["like"], reverse=True)
        return replies[:limit]

    def get_related(self):
        api = apis["video"]["info"]["related"]
        params = {
            "aid": self.aid
        }
        get = Get(url=api["url"], params=params)
        return get()

    def is_liked(self):
        if not self.verify.has_sess():
            raise exception.NoPermissionException("需要验证：SESSDATA")

        api = apis["video"]["info"]["is_liked"]
        params = {
            "aid": self.aid
        }
        get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        value = get()
        if value == 1:
            return True
        else:
            return False

    def get_added_coins(self):
        if not self.verify.has_sess():
            raise exception.NoPermissionException("需要验证：SESSDATA")

        api = apis["video"]["info"]["is_coins"]
        params = {
            "aid": self.aid
        }
        get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        value = get()["multiply"]
        return value

    def is_favoured(self):
        if not self.verify.has_sess():
            raise exception.NoPermissionException("需要验证：SESSDATA")

        api = apis["video"]["info"]["is_favoured"]
        params = {
            "aid": self.aid
        }
        get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        value = get()["favoured"]
        return value

    # 获取收藏夹列表以及当视频收藏情况，供对视频收藏操作用
    def get_media_list(self):
        if not self.verify.has_sess():
            raise exception.NoPermissionException("需要验证：SESSDATA")

        self.__get_self_info()
        up_mid = self.info["owner"]["mid"]
        api = apis["video"]["info"]["get_media_list"]
        params = {
            "rid": self.aid,
            "up_mid": up_mid,
            "type": 2,
            "ps": 100,
            "pn": 1
        }
        my_headers = headers
        my_headers["Referer"] = "https://www.bilibili.com/av%s" % self.aid
        get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies(), headers=my_headers)
        value = get()["list"]
        return value


class VideoOperate(Video):
    def __init__(self, aid: int, verify: Verify):
        Video.__init__(self, aid=aid)
        if type(verify) != Verify:
            raise Exception("请传入Verify类")
        else:
            self.verify = verify

    def like(self, is_like: bool = True):
        api = apis["video"]["operate"]["like"]
        data = {
            "aid": self.aid,
            "like": 0,
            "csrf": self.verify.csrf
        }
        if is_like:
            data["like"] = 1
        else:
            data["like"] = 2
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()

    def coin(self, num: int = 2, like: bool = False):
        if num not in (1, 2):
            raise Exception("硬币必须是1个或2个")
        if like:
            l = 1
        else:
            l = 0
        api = apis["video"]["operate"]["coin"]
        data = {
            "aid": self.aid,
            "multiply": num,
            "select_like": l,
            "csrf": self.verify.csrf
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()

    # mode=0，添加到收藏夹，其他从收藏夹移除
    def favorite(self, media_list: list, mode: int = 0):
        api = apis["video"]["operate"]["favorite"]
        if media_list is str:
            m = media_list
        else:
            m = ""
            i = 1
            for media in media_list:
                m += str(media)
                if i < len(media_list):
                    m += ","
                i += 1
        data = {
            "rid": self.aid,
            "type": 2,
            "add_media_ids": "",
            "del_media_ids": "",
            "csrf": self.verify.csrf
        }
        if mode == 0:
            data["add_media_ids"] = m
        else:
            data["del_media_ids"] = m
        my_headers = headers
        my_headers["Referer"] = "https://www.bilibili.com/av%s" % self.aid
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies(), headers=my_headers)
        post()

    def send_comment(self, text: str):
        api = apis["video"]["operate"]["send_comment"]
        data = {
            "oid": self.aid,
            "type": 1,
            "message": text,
            "plat": 1,
            "csrf": self.verify.csrf
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()

    # 评论操作，mode：like, hate, top, del。action: 1是0否（del没有）
    def operate_comment(self, rpid: int, mode: str, action: int):
        api = apis["video"]["operate"][mode + "_comment"]
        if mode == "del":
            data = {
                "rpid": rpid,
                "oid": self.aid,
                "type": 1,
                "csrf": self.verify.csrf
            }
        else:
            data = {
                "rpid": rpid,
                "oid": self.aid,
                "type": 1,
                "action": action,
                "csrf": self.verify.csrf
            }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()

    def send_danmaku(self, page: int, danmaku: Danmaku):
        page_info = VideoInfo(aid=self.aid).get_pages()
        oid = page_info[page]["cid"]
        api = apis["video"]["operate"]["send_danmaku"]
        if danmaku.is_sub:
            pool = 1
        else:
            pool = 0
        data = {
            "type": 1,
            "oid": oid,
            "msg": danmaku.text,
            "aid": self.aid,
            "bvid": "",
            "progress": int(danmaku.dm_time.seconds * 1000),
            "color": danmaku.color,
            "fontsize": danmaku.font_size,
            "pool": pool,
            "mode": danmaku.mode,
            "plat": 1,
            "csrf": self.verify.csrf
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()

    def add_tag(self, tag_name: str):
        api = apis["video"]["operate"]["add_tag"]
        data = {
            "aid": self.aid,
            "tag_name": tag_name,
            "csrf": self.verify.csrf
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        value = post()
        return value["tid"]

    def del_tag(self, tag_id: int):
        api = apis["video"]["operate"]["del_tag"]
        data = {
            "aid": self.aid,
            "tag_id": tag_id,
            "csrf": self.verify.csrf
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()
