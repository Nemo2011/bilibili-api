from . import user
from . import exception, utils
import requests
import re
import json
from .utils import Get, Post, logger
import math

headers = utils.default_headers
apis = utils.get_apis()


class SendDynamic:
    def __init__(self, text: str, verify: utils.Verify):
        self.verify = verify
        self._text = ""
        self._ctrl = None
        self._origin_text = text
        self.set_text(text)

    def set_text(self, text: str):
        pattern = re.compile(r"@\d*@")
        match = re.findall(pattern, text)
        at_users = {}
        for m in match:
            uid = m.replace("@", "")
            info = user.UserInfo(uid).get_info()
            at_users[uid] = info["name"]
        new_text = text
        for u in at_users.items():
            user_pattern = re.compile("@%s@" % u[0])
            new_text = re.sub(user_pattern, "@%s" % u[1], new_text)
        ctrl = []
        for u in at_users.items():
            user_pattern = "@%s" % u[1]
            length = 2 + len(u[1])
            location = new_text.find(user_pattern)
            at = {
                "location": location,
                "type": 1,
                "length": length,
                "data": str(u[0])
            }
            ctrl.append(at)
        self._ctrl = ctrl
        self._text = new_text
        self._origin_text = text

    def get_text(self):
        return self._text

    def get_origin_text(self):
        return self._origin_text

    def get_at_uids(self):
        at_uids = [i["data"] for i in self._ctrl]
        at_uids_str = ""
        if len(at_uids) > 0:
            i = 0
            for uid in at_uids:
                at_uids_str += str(uid)
                i += 1
                if i < len(at_uids):
                    at_uids_str += ","
        return at_uids_str


class UploadImages:
    def __init__(self, images_path: list, verify: utils.Verify):
        if type(verify) != utils.Verify:
            raise exception.bilibiliApiException("请传入Verify类")
        else:
            self.verify = verify
        if len(images_path) > 9:
            raise exception.bilibiliApiException("图片最多 9 张")
        elif type(images_path) != list:
            raise exception.bilibiliApiException("图片必须传入list")
        else:
            self.__images_path = images_path
        self.bilibili_path = []

    def add_image(self, image_path: str):
        if len(self.__images_path) >= 9:
            raise exception.bilibiliApiException("图片最多 9 张")
        else:
            self.__images_path.append(image_path)

    def del_image(self, image_path: str):
        if len(self.__images_path) == 0:
            raise exception.bilibiliApiException("没有图片")
        else:
            self.__images_path.remove(image_path)

    def pop_image(self, index: int):
        self.__images_path.pop(index)

    def get_images(self):
        return self.__images_path

    def clear_images(self):
        self.__images_path = []

    def upload(self):
        api = apis["dynamic"]["send"]["upload_img"]
        data = {
            "biz": "draw",
            "category": "daily"
        }
        for img in self.__images_path:
            files = {
                "file_up": open(img, "rb")
            }
            logger.debug("正在上传图片", img)
            req = requests.post(url=api["url"], data=data, files=files, cookies=self.verify.get_cookies())
            if req.ok:
                con = req.json()
                if con["code"] != 0:
                    raise exception.BiliException(con["code"], con["message"])
                else:
                    pic = {
                        "img_src": con["data"]["image_url"],
                        "img_height": con["data"]["image_height"],
                        "img_width": con["data"]["image_width"]
                    }
                    self.bilibili_path.append(pic)
            else:
                raise exception.NetworkException(req.status_code)


class TextDynamic(SendDynamic):
    def __init__(self, text: str, verify: utils.Verify):
        super().__init__(text, verify)

    def get_data(self):
        data = {
            "dynamic_id": 0,
            "type": 4,
            "rid": 0,
            "content": self._text,
            "extension": "{\"emoji_type\":1}",
            "at_uids": self.get_at_uids(),
            "ctrl": json.dumps(self._ctrl)
        }
        return data


class DrawDynamic(SendDynamic):
    def __init__(self, text: str, upload_images: UploadImages, verify: utils.Verify):
        super().__init__(text, verify)
        self.upload_images = upload_images

    def get_data(self):
        data = {
            "biz": 3,
            "category": 3,
            "type": 0,
            "title": "",
            "tags": "",
            "pictures": json.dumps(self.upload_images.bilibili_path),
            "description": self._text,
            "content": self._text,
            "from": "create.dynamic.web",
            "extension": "{\"emoji_type\":1}",
            "at_uids": self.get_at_uids(),
            "at_control": json.dumps(self._ctrl)
        }
        return data

    def upload(self):
        self.upload_images.upload()


# 如果要@人，格式为 “@用户UID@ ”
class ScheduleDynamic:
    def __init__(self, dynamic: (TextDynamic, DrawDynamic), timestamp: int):
        self.timestamp = timestamp
        self.dynamic = dynamic

    def send(self):
        if type(self.dynamic) == DrawDynamic:
            type_ = 4
            self.dynamic.upload()
        elif type(self.dynamic) == TextDynamic:
            type_ = 2
        else:
            raise exception.bilibiliApiException("未知的动态类型")
        data = {"type": type_, "publish_time": self.timestamp, "request": json.dumps(self.dynamic.get_data()),
                "csrf_token": self.dynamic.verify.csrf}
        api = apis["dynamic"]["send"]["schedule"]
        post = Post(url=api["url"], data=data, cookies=self.dynamic.verify.get_cookies())
        post()


class InstantDynamic:
    def __init__(self, dynamic):
        if isinstance(dynamic, (DrawDynamic, TextDynamic)):
            self.dynamic = dynamic
        else:
            raise exception.bilibiliApiException("传入参数非法")

    def send(self):
        if type(self.dynamic) == DrawDynamic:
            api = apis["dynamic"]["send"]["instant_draw"]
            self.dynamic.upload()
        else:
            api = apis["dynamic"]["send"]["instant_text"]
        request = self.dynamic.get_data()
        setting = {
            "copy_forbidden": 0,
            "cachedTime": 0
        }
        data = {
            "csrf_token": self.dynamic.verify.csrf,
            "setting": json.dumps(setting)
        }
        data.update(request)
        post = Post(url=api["url"], data=data, cookies=self.dynamic.verify.get_cookies())
        post()


class DynamicInfo:
    def __init__(self, dyid: int, verify: utils.Verify = utils.Verify()):
        self.dyid = dyid
        self.info = None
        self.verify = verify

    def __get_self_info(self):
        if self.info is None:
            self.info = self.get_info()
            if self.info["desc"]["type"] == 2:
                self.oid = self.info["desc"]["rid"]
                self.is_draw = True
            else:
                self.is_draw = False

    def get_info(self):
        api = apis["dynamic"]["info"]["detail"]
        params = {
            "dynamic_id": self.dyid
        }
        get = Get(url=api["url"], params=params)
        data = get()
        data["card"]["card"] = json.loads(data["card"]["card"])
        data["card"]["extend_json"] = json.loads(data["card"]["extend_json"])
        self.info = data["card"]
        return data["card"]

    def get_reposts(self, limit: int = 560):
        def get(offset):
            api = apis["dynamic"]["info"]["repost"]
            params = {"dynamic_id": self.dyid, "offset": offset}
            g = Get(url=api["url"], params=params)
            data = g()
            if data["total"] == 0:
                return {"has_more": False, "items": []}
            items = data["items"]
            for i in items:
                i["card"] = json.loads(i["card"])
                i["extend_json"] = json.loads(i["extend_json"])
            total = data["total"]
            ret = {
                "items": items,
                "total": total
            }
            if data["has_more"] == 1:
                ret["next_offset"] = data["offset"]
                ret["has_more"] = True
            else:
                ret["has_more"] = False
            return ret

        offset = ""
        reposts_list = []
        sum_ = 0
        while True:
            reposts = get(offset)
            if reposts["has_more"]:
                offset = reposts["next_offset"]
            reposts_list += reposts["items"]
            sum_ += len(reposts["items"])
            if not reposts["has_more"] or sum_ >= 560 or sum_ >= limit:
                break
        return reposts_list[:limit]

    def get_replies(self, limit: int = 114514):
        def get(pn):
            api = apis["dynamic"]["info"]["reply"]
            if self.is_draw:
                ty = 11
                oid = self.oid
            else:
                ty = 17
                oid = self.dyid
            params = {
                "pn": pn,
                "type": ty,
                "oid": oid,
                "sort": 0
            }
            g = Get(url=api["url"], params=params)
            data = g()
            return data
        if self.info is None:
            self.__get_self_info()
        replies = []
        first = get(0)
        total_pages = math.ceil(first["page"]["count"] / first["page"]["size"])
        replies += first["replies"]
        sum_ = len(first["replies"])
        if sum_ < limit and total_pages > 1:
            for page in range(2, total_pages + 1):
                data = get(page)
                replies += data["replies"]
                sum_ += len(data["replies"])
                if sum_ >= limit:
                    break
        return replies[:limit]


class DynamicOperate:
    def __init__(self, dyid: int, verify: utils.Verify):
        self.dyid = dyid
        self.verify = verify
        self.__uid = None
        self.__info = None

    def __get_self_info(self):
        if self.__info is None:
            self.__info = DynamicInfo(dyid=self.dyid).get_info()
            if self.__info["desc"]["type"] == 2:
                self.oid = self.__info["desc"]["rid"]
                self.__is_draw = True
            else:
                self.__is_draw = False

    def like(self, mode: bool = True):
        api = apis["dynamic"]["operate"]["like"]
        if self.__uid is None:
            my_info = Get(url=apis["user"]["info"]["my_info"]["url"], cookies=self.verify.get_cookies())
            self.__uid = my_info()["mid"]
        if mode:
            up = 1
        else:
            up = 2
        data = {
            "dynamic_id": self.dyid,
            "up": up,
            "uid": self.__uid
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()

    def reply(self, text: str):
        api = apis["dynamic"]["operate"]["reply"]
        self.__get_self_info()
        if self.__is_draw:
            type_ = 11
            oid = self.oid
        else:
            type_ = 17
            oid = self.dyid

        data = {
            "oid": oid,
            "type": type_,
            "message": text,
            "plat": 1,
            "csrf": self.verify.csrf
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()

    def delete(self):
        api = apis["dynamic"]["operate"]["delete"]
        data =  {
            "dynamic_id": self.dyid
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()

    def repost(self, text: str):
        api = apis["dynamic"]["operate"]["repost"]
        data = {
            "dynamic_id": self.dyid,
            "content": text,
            "extension": "{\"emoji_type\":1}",
            "csrf_token": self.verify.csrf
        }
        post = Post(url=api["url"], data=data, cookies=self.verify.get_cookies())
        post()