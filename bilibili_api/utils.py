r"""
模块：utils
功能：基础工具库
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/4
"""
import json
import datetime
import time
import os
import requests
from bilibili_api import exceptions
import urllib3
from zlib import crc32

use_https = True
urllib3.disable_warnings()

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/79.0.3945.130 Safari/537.36",
    "Referer": "https://www.bilibili.com"
}

MESSAGES = {
    "no_sess": "需要提供：SESSDATA（Cookies里头的`SESSDATA`键对应的值）",
    "no_csrf": "需要提供：csrf（Cookies里头的`bili_jct`键对应的值）"
}


def get_project_path():
    return os.path.dirname(__file__)


def get_api():
    """
    获取API
    :return:
    """
    with open(os.path.join(os.path.dirname(__file__), "data/api.json"), "r", encoding="utf-8") as f:
        apis = json.loads(f.read())
        f.close()
    return apis


class Color:
    def __init__(self, hex_: str = "FFFFFF"):
        self.__color = 0
        self.set_hex_color(hex_)

    def set_hex_color(self, hex_color: str):
        """
        设置十六进制RGB颜色
        :param hex_color:
        :return:
        """
        if len(hex_color) == 3:
            hex_color = "".join(x + "0" for x in hex_color)
        dec = int(hex_color, 16)
        self.__color = dec

    def set_rgb_color(self, r: int, g: int, b: int):
        """
        根据RGB三个分量设置颜色
        :param r: 红色分量
        :param g: 绿色分量
        :param b: 蓝色分量
        :return:
        """
        if not all([0 <= r < 256, 0 <= g < 256, 0 <= b < 256]):
            raise ValueError("值范围0~255")
        self.__color = (r << 8*2) + (g << 8) + b

    def set_dec_color(self, color: int):
        """
        设置十进制颜色
        :param color:
        :return:
        """
        if 0 <= int(color) <= 16777215:
            self.__color = color
        else:
            raise ValueError("范围0~16777215")

    def get_hex_color(self):
        """
        获取十六进制颜色
        :return:
        """
        # 补零
        h = hex(int(self.__color)).lstrip("0x")
        h = "0" * (6 - len(h)) + h
        return h

    def get_rgb_color(self):
        """
        获取RGB三个分量颜色
        :return:
        """
        h = hex(int(self.__color)).lstrip("0x")
        # 补零
        h = "0" * (6 - len(h)) + h
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        return r, g, b

    def get_dec_color(self):
        """
        获取十进制颜色
        :return:
        """
        return self.__color

    def __str__(self):
        return self.get_hex_color()


class Danmaku:
    FONT_SIZE_SMALL = 18
    FONT_SIZE_BIG = 36
    FONT_SIZE_NORMAL = 25
    MODE_FLY = 1
    MODE_TOP = 5
    MODE_BOTTOM = 4

    def __init__(self, text: str, dm_time: float = 0.0, send_time: float = time.time(), crc32_id: str = None
                 , color: Color = None,
                 mode: int = MODE_FLY, font_size: int = FONT_SIZE_NORMAL, is_sub: bool = False):
        self.dm_time = datetime.timedelta(seconds=dm_time)
        self.send_time = datetime.datetime.fromtimestamp(send_time)
        self.crc32_id = crc32_id
        self.uid = None

        self.__color = color if color else Color()

        self.mode = mode
        self.font_size = font_size
        self.is_sub = is_sub
        self.text = text

    def __str__(self):
        ret = "%s, %s, %s" % (self.send_time, self.dm_time, self.text)
        return ret

    def __len__(self):
        return len(self.text)

    def crack_uid(self):
        """
        暴力破解UID，耗时较长不要大量使用
        :return:
        """
        crc_dec = int(self.crc32_id, 16)
        uid = 1
        while True:
            crc = crc32(str(uid).encode())
            if crc == crc_dec:
                break
            uid += 1
        self.uid = uid
        return uid


class Verify:
    def __init__(self, sessdata: str = None, csrf: str = None):
        self.sessdata = sessdata
        self.csrf = csrf

    def get_cookies(self):
        """
        获取cookies
        :return:
        """
        cookies = {}
        if self.has_sess():
            cookies["SESSDATA"] = self.sessdata
        if self.has_csrf():
            cookies["bili_jct"] = self.csrf
        return cookies

    def has_sess(self):
        """
        是否提供SESSDATA
        :return:
        """
        if self.sessdata is None:
            return False
        else:
            return True

    def has_csrf(self):
        """
        是否提供CSRF
        :return:
        """
        if self.csrf is None:
            return False
        else:
            return True

    def check(self):
        """
        检查权限情况
        -1: csrf 校验失败
        -2: SESSDATA值有误
        -3: 未提供SESSDATA
        :return:
        """
        ret = {
            "code": -2,
            "message": ""
        }
        if not self.has_sess():
            ret["code"] = -3
            ret["message"] = "未提供SESSDATA"
        else:
            api = "https://api.bilibili.com/x/web-interface/archive/like"
            data = {"bvid": "BV1uv411q7Mv", "like": 1, "csrf": self.csrf}
            req = requests.post(url=api, data=data, cookies=self.get_cookies())
            if req.ok:
                con = req.json()
                if con["code"] == -111:
                    ret["code"] = -1
                    ret["message"] = "csrf 校验失败"
                elif con["code"] == -101 or con["code"] == -400:
                    ret["code"] = -2
                    ret["message"] = "SESSDATA值有误"
                else:
                    ret["code"] = 0
                    ret["message"] = "0"
            else:
                raise exceptions.NetworkException(req.status_code)
        return ret


# 请求相关


def get(url, params=None, cookies=None, headers=None, **kwargs):
    """
    专用GET请求
    :param url:
    :param params:
    :param cookies:
    :param headers:
    :param kwargs:
    :return:
    """
    if headers is None:
        headers = DEFAULT_HEADERS
    if use_https:
        req = requests.get(url=url, params=params, headers=headers, cookies=cookies, verify=True, **kwargs)
    else:
        req = requests.get(url=url, params=params, headers=headers, cookies=cookies, verify=False, **kwargs)
    if req.ok:
        content = req.content.decode("utf8")
        if req.headers.get("content-length") == 0:
            return None
        con = json.loads(content)
        if con["code"] != 0:
            raise exceptions.BilibiliException(con["code"], con["message"])
        else:
            if 'data' in con.keys():
                return con['data']
            else:
                if 'result' in con.keys():
                    return con["result"]
                else:
                    return None
    else:
        raise exceptions.NetworkException(req.status_code)


def post(url, cookies, data=None, headers=None, **kwargs):
    """
    专用POST请求
    :param url:
    :param cookies:
    :param data:
    :param headers:
    :param kwargs:
    :return:
    """
    if headers is None:
        headers = DEFAULT_HEADERS
    if use_https:
        req = requests.post(url=url, data=data, headers=headers, cookies=cookies, verify=True, **kwargs)
    else:
        req = requests.post(url=url, data=data, headers=headers, cookies=cookies, verify=False, **kwargs)
    if req.ok:
        content = req.content.decode("utf8")
        if req.headers.get("content-length") == 0:
            return None
        con = json.loads(content)
        if con["code"] != 0:
            raise exceptions.BilibiliException(con["code"], con["message"])
        else:
            if "data" in con:
                return con["data"]
            else:
                if 'result' in con.keys():
                    return con["result"]
                else:
                    return None
    else:
        raise exceptions.NetworkException(req.status_code)


def bvid2aid(bvid: str):
    """
    BV号转AV号
    代码来源：https://www.zhihu.com/question/381784377/answer/1099438784
    :param bvid:
    :return:
    """
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    def dec(x):
        r = 0
        for i in range(6):
            r += tr[x[s[i]]] * 58 ** i
        return (r - add) ^ xor

    return dec(bvid)


def aid2bvid(aid: int):
    """
    AV号转BV号
    代码来源：https://www.zhihu.com/question/381784377/answer/1099438784
    :param aid:
    :return:
    """
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    def enc(x):
        x = (x ^ xor) + add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]] = table[x // 58 ** i % 58]
        return ''.join(r)

    return enc(aid)


# 评论相关


COMMENT_TYPE_MAP = {
    "video": 1,
    "article": 12,
    "dynamic_draw": 11,
    "dynamic_text": 17
}

COMMENT_SORT_MAP = {
    "like": 2,
    "time": 0
}


def send_comment(text: str, oid: int, type_: str, root: int = None,
                    parent: int = None, verify: Verify = None):
    """
    通用发送评论
    :param text:
    :param oid:
    :param type_:
    :param root:
    :param parent:
    :param verify:
    :return:
    """
    if verify is None:
        raise exceptions.BilibiliApiException("请提供verify")
    assert verify.has_sess(), exceptions.BilibiliApiException(MESSAGES["no_sess"])
    assert verify.has_csrf(), exceptions.BilibiliApiException(MESSAGES["no_csrf"])

    type_ = COMMENT_TYPE_MAP.get(type_, None)
    assert type_ is not None, exceptions.BilibiliApiException("不支持的评论类型")

    # 参数检查完毕
    data = {
        "oid": oid,
        "type": type_,
        "message": text,
        "plat": 1,
        "csrf": verify.csrf
    }
    if root is not None:
        data["root"] = data["parent"] = root
        if parent is not None:
            data["parent"] = parent
    api = get_api()["common"]["comment"]["send"]
    resp = post(api["url"], data=data, cookies=verify.get_cookies())
    return resp


def operate_comment(action: str, oid: int, type_: str, rpid: int,
                    status: bool = True, verify: Verify = None):
    """
    通用评论操作
    :param action: 操作类型，见api.json
    :param oid:
    :param type_:
    :param rpid:
    :param status: 设置状态
    :param verify:
    :return:
    """
    if verify is None:
        raise exceptions.BilibiliApiException("请提供verify")
    assert verify.has_sess(), exceptions.BilibiliApiException(MESSAGES["no_sess"])
    assert verify.has_csrf(), exceptions.BilibiliApiException(MESSAGES["no_csrf"])

    type_ = COMMENT_TYPE_MAP.get(type_, None)
    assert type_ is not None, exceptions.BilibiliApiException("不支持的评论类型")

    comment_api = get_api()["common"]["comment"]
    api = comment_api.get(action, None)
    assert api is not None, exceptions.BilibiliApiException("不支持的评论操作方式")
    # 参数检查完毕
    data = {
        "oid": oid,
        "type": type_,
        "rpid": rpid,
        "csrf": verify.csrf
    }
    if action != "del":
        data["action"] = 1 if status else 0

    resp = post(api["url"], cookies=verify.get_cookies(), data=data)
    return resp


def get_comments_raw(oid: int, type_: str, order: str = "time", pn: int = 1, verify: Verify = None):
    """
    通用获取评论
    :param oid:
    :param type_:
    :param order:
    :param pn:
    :param verify:
    :return:
    """
    if verify is None:
        verify = Verify()

    type_ = COMMENT_TYPE_MAP.get(type_, None)
    assert type_ is not None, exceptions.BilibiliApiException("不支持的评论类型")

    order = COMMENT_SORT_MAP.get(order, None)
    assert order is not None, exceptions.BilibiliApiException("不支持的排序方式，支持：time（时间倒序），like（热度倒序）")
    # 参数检查完毕
    params = {
        "oid": oid,
        "type": type_,
        "sort": order,
        "pn": pn
    }
    comment_api = get_api()["common"]["comment"]
    api = comment_api.get("get", None)
    resp = get(api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_comments(oid: int, type_: str, order: str = "time", limit: int = 1919810, callback=None, verify: Verify = None):
    """
    通用循环获取评论
    :param type_:
    :param order:
    :param callback: 回调函数
    :param oid:
    :param limit: 限制数量
    :param verify:
    :return:
    """
    if verify is None:
        verify = Verify()

    count = 0
    replies = []
    page = 1
    while count < limit:
        resp = get_comments_raw(oid=oid, pn=page, order=order, verify=verify, type_=type_)
        if "replies" not in resp:
            break
        if resp["replies"] is None:
            break
        count += len(resp["replies"])
        replies += resp["replies"]
        if callable(callback):
            callback(resp["replies"])
        page += 1
    return replies[:limit]


def get_vote_info(vote_id: int, verify: Verify = None):
    """
    获取投票信息
    :param vote_id:
    :param verify:
    :return:
    """
    if verify is None:
        verify = Verify()

    api = get_api()["common"]["vote"]["info"]["get_info"]
    params = {
        "vote_id": vote_id
    }
    resp = get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


"""
みゃーねか？どうしたみゃーね～
ーー「私に天使が舞い降りた！」
"""