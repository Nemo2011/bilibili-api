import json
from . import utils
import math
from .utils import Get, Post

headers = utils.default_headers
apis = utils.get_apis()


# 把你资料给我交了（迫真）
class UserInfo:
    def __init__(self, uid: int, verify: utils.Verify = utils.Verify()):
        self.uid = uid
        self.verify = verify

    def get_info(self):
        api = apis["user"]["info"]["info"]
        api1 = apis["user"]["info"]["stat"]
        params = {
            "mid": self.uid
        }
        params1 = {
            "vmid": self.uid
        }
        get = Get(url=api["url"], params=params)
        get1 = Get(url=api1["url"], params=params1)
        data = get()
        data.update(get1())
        return data

    def get_live_info(self):
        api = apis["user"]["info"]["live"]
        params = {
            "mid": self.uid
        }
        get = Get(url=api["url"], params=params)
        con = get()
        return con

    # sort: 0-上传日期，1-播放量，2-收藏量
    def get_video(self, sort: int = 0, limit: int = 114514):
        def get(page):
            if sort == 0:
                sort_str = "pubdate"
            elif sort == 1:
                sort_str = "click"
            else:
                sort_str = "stow"
            api = apis["user"]["info"]["video"]
            params = {
                "mid": self.uid,
                "ps": 30,
                "tid": 0,
                "pn": page,
                "keyword": "",
                "order": sort_str
            }
            get1 = Get(url=api["url"], params=params)
            con = get1()
            return con
        first_page = get(1)
        count = 0
        if first_page["page"]["count"] > first_page["page"]["ps"]:
            pages = math.ceil(first_page["page"]["count"] / first_page["page"]["ps"])
            video_list = first_page["list"]["vlist"]
            count += len(video_list)
            if count < limit:
                for page in range(2, pages + 1):
                    data = get(page)["list"]["vlist"]
                    video_list += data
                    count += len(data)
                    if count > limit:
                        break
            return video_list[:limit]
        else:
            return first_page["list"]["vlist"][:limit]

    # sort: 0-上传日期，1-播放量，2-收藏量
    def get_audio(self, sort: int = 0, limit: int = 114514):
        def get(page):
            if sort == 0:
                sort_str = 1
            elif sort == 1:
                sort_str = 2
            else:
                sort_str = 3
            api = apis["user"]["info"]["audio"]
            params = {
                "uid": self.uid,
                "ps": 30,
                "pn": page,
                "order": sort_str
            }
            get1 = Get(url=api["url"], params=params)
            con = get1()
            return con
        count = 0
        first_page = get(1)
        page_count = first_page["pageCount"]
        count += page_count
        if first_page["pageCount"] > 1 and count < limit:
            audio_list = first_page["data"]
            for page in range(2, page_count + 1):
                data = get(page)["data"]
                count += len(data)
                audio_list += data
                if count >= limit:
                    break
            return audio_list[:limit]
        else:
            return first_page["data"][:limit]

    def get_article(self, sort: int = 0, limit: int = 114514):
        def get(page):
            if sort == 0:
                sort_str = "publish_time"
            elif sort == 1:
                sort_str = "view"
            else:
                sort_str = "fav"
            api = apis["user"]["info"]["article"]
            params = {
                "mid": self.uid,
                "ps": 30,
                "pn": page,
                "sort": sort_str
            }
            get1 = Get(url=api["url"], params=params)
            con = get1()
            return con

        first_page = get(1)
        page_count = math.ceil(first_page["count"] / first_page["ps"])
        count = len(first_page["articles"])
        if page_count > 1 and count < limit:
            article_list = first_page["articles"]
            for page in range(2, page_count + 1):
                data = get(page)["articles"]
                article_list += data
                count += len(data)
                if count >= limit:
                    break
            return article_list[:limit]
        else:
            return first_page["articles"][:limit]

    # sort: 0最近更新，1最多阅读
    def get_article_list(self, sort: int = 0):
        api = apis["user"]["info"]["article_lists"]
        params = {
            "mid": self.uid,
            "sort": sort
        }
        get = Get(url=api["url"], params=params)
        con = get()
        return con

    def get_dynamic(self, limit: int = 114514):
        def get(offset):
            api = apis["user"]["info"]["dynamic"]
            params = {
                "host_uid": self.uid,
                "offset_dynamic_id": offset,
                "need_top": 0
            }
            get1 = Get(url=api["url"], params=params)
            con = get1()
            return con
        p = 0
        first = get(0)
        cards = first["cards"]
        next_offset = first["next_offset"]
        has_more = first["has_more"]
        count = limit
        while has_more == 1 and count > 0:
            p += 1
            this = get(next_offset)
            next_offset = this["next_offset"]
            cards += this.get("cards", [])
            has_more = this["has_more"]
            count -= len(this.get("cards", []))
        return cards[:limit]

    # "type": "1追番，2追剧"
    def get_bangumi(self, type_: int = 1):
        def get(page):
            api = apis["user"]["info"]["bangumi"]
            params = {
                "vmid": self.uid,
                "pn": page,
                "ps": 15,
                "type": type_
            }
            if self.verify.has_sess():
                get1 = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
            else:
                get1 = Get(url=api["url"], params=params)
            con = get1()
            return con
        first = get(1)
        if first["total"] > first["ps"]:
            pages = math.ceil(first["total"] / first["ps"])
            bangumi = first["list"]
            for p in range(2, pages + 1):
                g = get(p)
                bangumi += g["list"]
            return bangumi
        else:
            return first["list"]

    def get_media_list(self):
        def get(page):
            api = apis["user"]["info"]["media_list"]
            params = {
                "up_mid": self.uid,
                "pn": page,
                "ps": 100,
                "is_space": 0
            }
            if self.verify.has_sess():
                get1 = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
            else:
                get1 = Get(url=api["url"], params=params)
            con = get1()
            return con
        first = get(1)
        if first["count"] > 100:
            pages = math.ceil(first["count"] / 100.0)
            me = first["list"]
            for p in range(2, pages + 1):
                g = get(p)
                me += g["list"]
            return me
        else:
            return first["list"]

    def get_media_list_content(self, media_id: int, sort: int = 0, limit=114514):
        def get(page):
            if sort == 0:
                sort_str = "mtime"
            elif sort == 1:
                sort_str = "view"
            else:
                sort_str = "pubtime"
            api = apis["user"]["info"]["media_list_content"]
            params = {
                "media_id": media_id,
                "pn": page,
                "ps": 20,
                "order": sort_str,
                "keyword": "",
                "type": 0,
                "tid": 0
            }
            if self.verify.has_sess():
                get1 = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
            else:
                get1 = Get(url=api["url"], params=params)
            con = get1()
            return con
        first = get(1)
        ret = first
        count = 0
        if first["info"]["media_count"] > 20:
            pages = math.ceil(first["info"]["media_count"] / 20.0)
            me = first["medias"]
            count += len(first["medias"])
            if count < limit:
                for p in range(2, pages + 1):
                    g = get(p)
                    me += g["medias"]
                    count += len(g["medias"])
                    if count >= limit:
                        break
                ret["medias"] = me[:limit]
            return ret
        else:
            return ret


class UserOperate:
    def __init__(self, uid: int, verify: utils.Verify = utils.Verify()):
        self.uid = uid
        self.verify = verify
        self.__my_info = Get(url=apis["user"]["info"]["my_info"]["url"], cookies=self.verify.get_cookies())()

    def subscribe(self, mode: bool = True):
        api = apis["user"]["operate"]["modify"]
        if mode == 0:
            act = 2
        else:
            act = 1
        data = {
            "fid": self.uid,
            "act": act,
            "re_src": 11,
            "csrf": self.verify.csrf
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()

    def send_msg(self, text: str):
        api = apis["user"]["operate"]["send_msg"]
        data = {
            "msg[sender_uid]": self.__my_info["mid"],
            "msg[receiver_id]": self.uid,
            "msg[receiver_type]": 1,
            "msg[msg_type]": 1,
            "msg[msg_status]": 0,
            "msg[content]": ""
        }
        msg = {
            "content": text
        }
        data["msg[content]"] = json.dumps(msg)
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()

    def set_black(self, mode: bool = True):
        api = apis["user"]["operate"]["modify"]
        if mode == 0:
            act = 6
        else:
            act = 5
        data = {
            "fid": self.uid,
            "act": act,
            "re_src": 11,
            "csrf": self.verify.csrf
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()


