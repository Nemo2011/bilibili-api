from . import utils, psk_exception
import requests
import json
from xml.dom.minidom import parseString
import math
from .utils import Danmaku
from bs4 import BeautifulSoup as bs

verify = utils.verify
use_headers = utils.use_headers
apis = utils.get_apis()


class Video:
    def __init__(self, aid):
        self.aid = aid


class VideoInfo(Video):
    def __init__(self, aid, sessdata="False"):
        Video.__init__(self, aid)
        self.__sessdata = sessdata
        self.info = None

    def __get_self_info(self):
        if self.info is None:
            self.info = self.get_video_info()

    def get_video_info(self, is_simple=False):
        @use_headers
        def wrapper(headers):
            if is_simple:
                api = apis["video"]["info"]["info_simple"]
            else:
                api = apis["video"]["info"]["info_detail"]
            params = {
                "aid": self.aid
            }
            req = requests.get(url=api["url"], params=params, headers=headers)
            if req.ok:
                con = json.loads(req.text)
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    self.info = con["data"]
                    return con["data"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()

    # sort=0 按弹幕出现时间正序排序，其他按发送时间正序排序
    def get_danmaku(self, page, sort=0):
        @use_headers
        def wrapper(headers):
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
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()

    def get_history_danmaku(self, page, date, sort=0):
        if self.__sessdata == "False":
            raise psk_exception.NoPermissionException("需要验证：SESSDATA")

        @verify(sessdata=self.__sessdata)
        @use_headers
        def wrapper(headers, cookies):
            api = apis["video"]["info"]["history_danmaku"]
            self.__get_self_info()
            page_id = self.info["pages"][page]["cid"]
            params = {
                "type": 1,
                "date": date,
                "oid": page_id
            }
            req = requests.get(api["url"], params=params, headers=headers, cookies=cookies)
            if req.ok:
                if req.headers["Content-Type"] == "application/json":
                    con = req.json()
                    raise psk_exception.BiliException(con["code"], con["message"])
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
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()

    def get_tags(self):
        @use_headers
        def wrappers(headers):
            api = apis["video"]["info"]["tags"]
            params = {
                "aid": self.aid
            }
            req = requests.get(api["url"], params=params, headers=headers)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    return con["data"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrappers()

    def get_history_danmaku_index(self, page, month):
        if self.__sessdata == "False":
            raise psk_exception.NoPermissionException("需要验证：SESSDATA")

        @use_headers
        @verify(sessdata=self.__sessdata)
        def wrappers(headers, cookies):
            self.__get_self_info()
            page_id = self.info["pages"][page]["cid"]
            api = apis["video"]["info"]["history_danmaku_index"]
            params = {
                "oid": page_id,
                "month": month,
                "type": 1
            }
            req = requests.get(api["url"], params=params, headers=headers, cookies=cookies)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    return con["data"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrappers()

    def get_chargers(self):
        @use_headers
        def wrappers(headers):
            api = apis["video"]["info"]["charge"]
            self.__get_self_info()
            mid = self.info["owner"]["mid"]
            params = {
                "aid": self.aid,
                "mid": mid
            }
            req = requests.get(api["url"], params=params, headers=headers)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    return con["data"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrappers()

    def get_pages(self):
        @use_headers
        def wrappers(headers):
            api = apis["video"]["info"]["pages"]
            params = {
                "aid": self.aid
            }
            req = requests.get(api["url"], params=params, headers=headers)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    return con["data"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrappers()

    def get_playurl(self):
        @use_headers
        def wrappers(headers):
            headers["Referer"] = "https://www.bilibili.com"
            url = "https://www.bilibili.com/video/av%s" % self.aid
            if self.__sessdata != "False":
                cookies = {
                    "SESSDATA": self.__sessdata
                }
                req = requests.get(url, cookies=cookies, headers=headers)
            else:
                req = requests.get(url)
            if req.ok:
                html = bs(req.text.replace("\n", ""), "html.parser")
                script = html.select("script")
                for s in script:
                    if "playinfo" in s.text:
                        tmp = s.text.replace("window.__playinfo__=", "")
                        video_info = json.loads(tmp)
                        break
                else:
                    raise Exception("下载链接获取出错")
                if video_info["code"] != 0:
                    raise psk_exception.BiliException(video_info["code"], video_info["message"])
                else:
                    return video_info["data"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrappers()

    # sort=0 评论时间正序排序，其他按评论点赞数倒序排序
    def get_comments(self, sort=0):
        @use_headers
        def wrappers(headers):
            def get_page(page):
                api = apis["video"]["info"]["comments"]
                params = {
                    "oid": self.aid,
                    "type": 1,
                    "sort": 2,
                    "pn": page
                }
                req = requests.get(api["url"], params=params, headers=headers)
                if req.ok:
                    con = req.json()
                    if con["code"] != 0:
                        raise psk_exception.BiliException(con["code"], con["message"])
                    else:
                        return con["data"]
                else:
                    raise psk_exception.NetworkException(req.status_code)

            first_get = get_page(1)
            page_num = math.ceil(first_get["page"]["count"] / first_get["page"]["size"])
            replies = first_get["replies"]
            if page_num > 1:
                for p in range(2, page_num + 1):
                    rep = get_page(p)
                    replies += rep["replies"]
            if sort == 0:
                replies.sort(key=lambda x: x["ctime"])
            else:
                replies.sort(key=lambda x: x["like"], reverse=True)
            return replies

        return wrappers()

    def get_related(self):
        @use_headers
        def wrappers(headers):
            api = apis["video"]["info"]["related"]
            params = {
                "aid": self.aid
            }
            req = requests.get(api["url"], params=params, headers=headers)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    return con["data"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrappers()

    def is_liked(self):
        if self.__sessdata == "False":
            raise psk_exception.NoPermissionException("需要验证：SESSDATA")

        @use_headers
        @verify(sessdata=self.__sessdata)
        def wrappers(headers, cookies):
            api = apis["video"]["info"]["is_liked"]
            params = {
                "aid": self.aid
            }
            req = requests.get(api["url"], params=params, headers=headers, cookies=cookies)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    if con["data"] == 1:
                        return True
                    else:
                        return False
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrappers()

    def get_added_coins(self):
        if self.__sessdata == "False":
            raise psk_exception.NoPermissionException("需要验证：SESSDATA")

        @use_headers
        @verify(sessdata=self.__sessdata)
        def wrappers(headers, cookies):
            api = apis["video"]["info"]["is_coins"]
            params = {
                "aid": self.aid
            }
            req = requests.get(api["url"], params=params, headers=headers, cookies=cookies)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    return con["data"]["multiply"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrappers()

    def is_favoured(self):
        if self.__sessdata == "False":
            raise psk_exception.NoPermissionException("需要验证：SESSDATA")

        @use_headers
        @verify(sessdata=self.__sessdata)
        def wrappers(headers, cookies):
            api = apis["video"]["info"]["is_favoured"]
            params = {
                "aid": self.aid
            }
            req = requests.get(api["url"], params=params, headers=headers, cookies=cookies)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    return con["data"]["favoured"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrappers()

    # 获取收藏夹列表以及当视频收藏情况，供对视频收藏操作用
    def get_media_list(self):

        @use_headers
        @verify(sessdata=self.__sessdata)
        def wrapper(cookies, headers):
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
            headers["Referer"] = "https://www.bilibili.com/av%s" % self.aid
            req = requests.get(api["url"], params=params, headers=headers, cookies=cookies)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    return con["data"]["list"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()


class VideoOperate(Video):
    def __init__(self, sessdata, csrf, aid):
        Video.__init__(self, aid=aid)
        self.__sessdata = sessdata
        self.__csrf = csrf

    def like(self, is_like=True):
        @verify(sessdata=self.__sessdata, csrf=self.__csrf)
        def wrapper(cookies, csrf):
            api = apis["video"]["operate"]["like"]
            if is_like:
                like = 1
            else:
                like = 0
            data = {
                "aid": self.aid,
                "like": like,
                "csrf": csrf
            }
            if is_like:
                data["like"] = 1
                req = requests.post(url=api["url"], data=data, cookies=cookies)
            else:
                data["like"] = 2
                req = requests.post(url=api["url"], data=data, cookies=cookies)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()

    def coin(self, num=2, like=False):
        if num not in (1, 2):
            raise Exception("硬币必须是1个或2个")

        @verify(sessdata=self.__sessdata, csrf=self.__csrf)
        def wrapper(cookies, csrf):
            if like:
                l = 1
            else:
                l = 0
            api = apis["video"]["operate"]["coin"]
            data = {
                "aid": self.aid,
                "multiply": num,
                "select_like": l,
                "csrf": csrf
            }
            req = requests.post(api["url"], cookies=cookies, data=data)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()

    # mode=0，添加到收藏夹，其他从收藏夹移除
    def favorite(self, media_list, mode=0):
        @use_headers
        @verify(sessdata=self.__sessdata, csrf=self.__csrf)
        def wrapper(cookies, csrf, headers):
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
                "csrf": csrf
            }
            if mode == 0:
                data["add_media_ids"] = m
            else:
                data["del_media_ids"] = m
            headers["Referer"] = "https://www.bilibili.com/av%s" % self.aid
            req = requests.post(api["url"], data=data, cookies=cookies, headers=headers)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()

    def send_comment(self, text):
        @verify(sessdata=self.__sessdata, csrf=self.__csrf)
        def wrapper(cookies, csrf):
            api = apis["video"]["operate"]["send_comment"]
            data = {
                "oid": self.aid,
                "type": 1,
                "message": text,
                "plat": 1,
                "csrf": csrf
            }
            req = requests.post(api["url"], data=data, cookies=cookies)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()

    # 评论操作，mode：like, hate, top, del。action: 1是0否（del没有）
    def operate_comment(self, rpid, mode, action):
        @verify(sessdata=self.__sessdata, csrf=self.__csrf)
        def wrapper(cookies, csrf):
            api = apis["video"]["operate"][mode + "_comment"]
            if mode == "del":
                data = {
                    "rpid": rpid,
                    "oid": self.aid,
                    "type": 1,
                    "csrf": csrf
                }
            else:
                data = {
                    "rpid": rpid,
                    "oid": self.aid,
                    "type": 1,
                    "action": action,
                    "csrf": csrf
                }
            req = requests.post(api["url"], data=data, cookies=cookies)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()

    def send_danmaku(self, page, danmaku):
        @use_headers
        @verify(sessdata=self.__sessdata, csrf=self.__csrf)
        def wrapper(cookies, csrf, headers):
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
                "csrf": csrf
            }
            req = requests.post(api["url"], data=data, cookies=cookies, headers=headers)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()

    def add_tag(self, tag_name):
        @verify(sessdata=self.__sessdata, csrf=self.__csrf)
        def wrapper(cookies, csrf):
            api = apis["video"]["operate"]["add_tag"]
            data = {
                "aid": self.aid,
                "tag_name": tag_name,
                "csrf": csrf
            }
            req = requests.post(api["url"], data=data, cookies=cookies)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
                else:
                    return con["tid"]
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()

    def del_tag(self, tag_id):
        @verify(sessdata=self.__sessdata, csrf=self.__csrf)
        def wrapper(cookies, csrf):
            api = apis["video"]["operate"]["del_tag"]
            data = {
                "aid": self.aid,
                "tag_id": tag_id,
                "csrf": csrf
            }
            req = requests.post(api["url"], data=data, cookies=cookies)
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise psk_exception.BiliException(con["code"], con["message"])
            else:
                raise psk_exception.NetworkException(req.status_code)

        return wrapper()
