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


def get_api():
    with open(os.path.join(os.path.dirname(__file__), "api.json"), "r", encoding="utf-8") as f:
        apis = json.loads(f.read())
        f.close()
    return apis


class Danmaku:
    FONT_SIZE_SMALL = 18
    FONT_SIZE_BIG = 36
    FONT_SIZE_NORMAL = 25
    MODE_FLY = 1
    MODE_TOP = 5
    MODE_BOTTOM = 4

    def __init__(self, text: str, dm_time: float = 0.0, send_time: float = time.time(), crc32_id: str = None
                 , color="FFFFFF",
                 mode: int = MODE_FLY, font_size: int = FONT_SIZE_NORMAL, is_sub: bool = False):
        self.dm_time = datetime.timedelta(seconds=dm_time)
        self.send_time = datetime.datetime.fromtimestamp(send_time)
        self.crc32_id = crc32_id
        self.uid = None

        self.__color = None
        if type(color) == str:
            self.set_hex_color(color)
        elif type(color) == tuple or type(color) == list:
            self.set_rgb_color(int(color[0]), int(color[1]), int(color[2]))
        elif type(color) == int:
            if 0 <= int(color) <= 16777215:
                self.__color = color
            else:
                raise ValueError("范围0~16777215")
        else:
            raise exceptions.BilibiliApiException("不支持的颜色类型，支持：十六进制颜色（\"66CCFF\"），"
                                                  "RGB颜色（tuple([255,255,255]), list([255,255,255])）")
        self.mode = mode
        self.font_size = font_size
        self.is_sub = is_sub
        self.text = text

    def __str__(self):
        ret = "%s, %s, %s" % (self.send_time, self.dm_time, self.text)
        return ret

    def __len__(self):
        return len(self.text)

    def set_hex_color(self, hex_color: str):
        dec = int(hex_color, 16)
        self.__color = dec

    def set_rgb_color(self, r: int, g: int, b: int):
        if not all([0 <= r < 256, 0 <= g < 256, 0 <= b < 256]):
            raise ValueError("值范围0~255")
        self.__color = (r << 8*2) + (g << 8) + b

    def get_hex_color(self):
        # 补零
        h = hex(int(self.__color)).lstrip("0x")
        h = "0" * (6 - len(h)) + h
        return h

    def get_rgb_color(self):
        h = hex(int(self.__color)).lstrip("0x")
        # 补零
        h = "0" * (6 - len(h)) + h
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        return r, g, b

    def get_dec_color(self):
        return self.__color

    def crack_uid(self):
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
        cookies = {}
        if self.has_sess():
            cookies["SESSDATA"] = self.sessdata
        if self.has_csrf():
            cookies["bili_jct"] = self.csrf
        return cookies

    def has_sess(self):
        if self.sessdata is None:
            return False
        else:
            return True

    def has_csrf(self):
        if self.csrf is None:
            return False
        else:
            return True

    def check(self):
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


def get(url, params=None, cookies=None, headers=None, **kwargs):
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


# 代码来源：https://www.zhihu.com/question/381784377/answer/1099438784
def bvid2aid(bv: str):
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

    return dec(bv)


# 代码来源：https://www.zhihu.com/question/381784377/answer/1099438784
def aid2bvid(aid: int):
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


"""
みゃーねか？どうしたみゃーね～
"""