r"""
模块：utils
功能：基础工具库
项目GitHub地址：https://github.com/Passkou/bilibili_api
项目主页：https://passkou.com/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/4
"""
import json
import datetime
import re
import time
import os
import requests
from bilibili_api import exceptions
import urllib3
import copy

request_settings = {
    "use_https": True,
    "proxies": None
}
urllib3.disable_warnings()

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com/"
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


class Color(object):
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
            hex_color = "".join([x + "0" for x in hex_color])
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


_crack_uid = None


class Danmaku(object):
    FONT_SIZE_EXTREME_SMALL = 12
    FONT_SIZE_SUPER_SMALL = 16
    FONT_SIZE_SMALL = 18
    FONT_SIZE_NORMAL = 25
    FONT_SIZE_BIG = 36
    FONT_SIZE_SUPER_BIG = 45
    FONT_SIZE_EXTREME_BIG = 64
    MODE_FLY = 1
    MODE_TOP = 5
    MODE_BOTTOM = 4
    MODE_REVERSE = 6
    TYPE_NORMAL = 0
    TYPE_SUBTITLE = 1

    def __init__(self, text: str, dm_time: float = 0.0, send_time: float = time.time(), crc32_id: str = None
                 , color: Color = None, weight: int = -1, id_: int = -1, id_str: str = "", action: str = '',
                 mode: int = MODE_FLY, font_size: int = FONT_SIZE_NORMAL, is_sub: bool = False, pool: int = -1,
                 attr: int = -1):
        self.dm_time = datetime.timedelta(seconds=dm_time)
        self.send_time = datetime.datetime.fromtimestamp(send_time)
        self.crc32_id = crc32_id
        self.uid = None

        self.color = color if color else Color()

        self.mode = mode
        self.font_size = font_size
        self.is_sub = is_sub
        self.text = text

        self.weight = weight
        self.id = id_
        self.id_str = id_str
        self.action = action
        self.pool = pool
        self.attr = attr

    def __str__(self):
        ret = "%s, %s, %s" % (self.send_time, self.dm_time, self.text)
        return ret

    def __len__(self):
        return len(self.text)

    def crack_uid(self):
        """
        暴力破解UID
        :return:
        """
        global _crack_uid
        if _crack_uid is None:
            _crack_uid = CrackUid()
        uid = _crack_uid(self.crc32_id)
        self.uid = int(uid)
        return self.uid


class Verify(object):
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


class CrackUid(object):
    """
    弹幕中的CRC32 ID转换成用户UID
    代码翻译自：https://github.com/esterTion/BiliBili_crc2mid
    """
    def __init__(self):
        self.__CRCPOLYNOMIAL = 0xEDB88320
        self.__crctable = [None] * 256
        self.__create_table()
        self.__index = [None] * 4

    def __create_table(self):
        for i in range(256):
            crcreg = i
            for j in range(8):
                if (crcreg & 1) != 0:
                    crcreg = self.__CRCPOLYNOMIAL ^ (crcreg >> 1)
                else:
                    crcreg >>= 1
            self.__crctable[i] = crcreg

    def __crc32(self, input_):
        if type(input_) != str:
            input_ = str(input_)
        crcstart = 0xFFFFFFFF
        len_ = len(input_)
        for i in range(len_):
            index = (crcstart ^ ord(input_[i])) & 0xFF
            crcstart = (crcstart >> 8) ^ self.__crctable[index]
        return crcstart

    def __crc32lastindex(self, input_):
        if type(input_) != str:
            input_ = str(input_)
        crcstart = 0xFFFFFFFF
        len_ = len(input_)
        index = None
        for i in range(len_):
            index = (crcstart ^ ord(input_[i])) & 0xFF
            crcstart = (crcstart >> 8) ^ self.__crctable[index]
        return index

    def __getcrcindex(self, t):
        for i in range(256):
            if self.__crctable[i] >> 24 == t:
                return i
        return -1

    def __deepCheck(self, i, index):
        tc = 0x00
        str_ = ""
        hash_ = self.__crc32(i)
        tc = hash_ & 0xFF ^ index[2]
        if not (57 >= tc >= 48):
            return [0]
        str_ += str(tc - 48)
        hash_ = self.__crctable[index[2]] ^ (hash_ >> 8)

        tc = hash_ & 0xFF ^ index[1]
        if not (57 >= tc >= 48):
            return [0]
        str_ += str(tc - 48)
        hash_ = self.__crctable[index[1]] ^ (hash_ >> 8)

        tc = hash_ & 0xFF ^ index[0]
        if not (57 >= tc >= 48):
            return [0]
        str_ += str(tc - 48)
        hash_ = self.__crctable[index[0]] ^ (hash_ >> 8)

        return [1, str_]

    def __call__(self, input_):
        ht = int(input_, 16) ^ 0xFFFFFFFF
        i = 3
        while i >= 0:
            self.__index[3-i] = self.__getcrcindex(ht >> (i*8))
            snum = self.__crctable[self.__index[3-i]]
            ht ^= snum >> ((3-i)*8)
            i -= 1
        for i in range(10000000):
            lastindex = self.__crc32lastindex(i)
            if lastindex == self.__index[3]:
                deepCheckData = self.__deepCheck(i, self.__index)
                if deepCheckData[0]:
                    break
        if i == 10000000:
            return -1
        return str(i) + deepCheckData[1]

# 请求相关


def request(method: str, url: str, params=None, data=None, cookies=None, headers=None, data_type: str = "form", **kwargs):
    if params is None:
        params = {}
    if data is None:
        data = {}
    if cookies is None:
        cookies = {}
    if headers is None:
        headers = copy.deepcopy(DEFAULT_HEADERS)
    if data_type.lower() == "json":
        headers['Content-Type'] = "application/json"
    st = {
        "url": url,
        "params": params,
        "headers": headers,
        "verify": request_settings["use_https"],
        "data": data,
        "proxies": request_settings["proxies"],
        "cookies": cookies
    }
    st.update(kwargs)

    req = requests.request(method, **st)
    if req.ok:
        content = req.content.decode("utf8")
        if req.headers.get("content-length") == 0:
            return None
        if 'jsonp' in params and 'callback' in params:
            con = json.loads(re.match(".*?({.*}).*", content, re.S).group(1))
        else:
            con = json.loads(content)
        if con["code"] != 0:
            if "message" in con:
                msg = con["message"]
            elif "msg" in con:
                msg = con["msg"]
            else:
                msg = "请求失败，服务器未返回失败原因"
            raise exceptions.BilibiliException(con["code"], msg)
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


def get(url, params=None, cookies=None, headers=None, data_type: str = "form", **kwargs):
    """
    专用GET请求
    :param data_type:
    :param url:
    :param params:
    :param cookies:
    :param headers:
    :param kwargs:
    :return:
    """
    resp = request("GET", url=url, params=params, cookies=cookies, headers=headers, data_type=data_type, **kwargs)
    return resp


def post(url, cookies, data=None, headers=None, data_type: str = "form", **kwargs):
    """
    专用POST请求
    :param data_type:
    :param url:
    :param cookies:
    :param data:
    :param headers:
    :param kwargs:
    :return:
    """
    resp = request("POST", url=url, data=data, cookies=cookies, headers=headers, data_type=data_type, **kwargs)
    return resp


def delete(url, params=None, data=None, cookies=None, headers=None, data_type: str = "form", **kwargs):
    """
    专用DELETE请求
    :param data_type:
    :param url:
    :param params:
    :param data:
    :param cookies:
    :param headers:
    :param kwargs:
    :return:
    """
    resp = request("DELETE", url=url, params=params, data=data, cookies=cookies, headers=headers, data_type=data_type, **kwargs)
    return resp


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


def upload_image(image_path: str, verify: Verify):
    """
    上传图片
    :param verify:
    :param image_path: 图片路径列表
    :return:
    """
    if not verify.has_sess():
        raise exceptions.NoPermissionException(MESSAGES["no_sess"])

    api = get_api()["dynamic"]["send"]["upload_img"]
    data = {
        "biz": "draw",
        "category": "daily"
    }
    files = {
        "file_up": open(image_path, "rb")
    }
    resp = post(url=api["url"], data=data, cookies=verify.get_cookies(), files=files)
    return resp


def read_varint(stream: bytes):
    """
    读取varint
    :param stream:
    :return: value（真实值）, length（varint长度）
    """
    value = 0
    position = 0
    shift = 0
    while True:
        if position >= len(stream):
            break
        byte = stream[position]
        value += (byte & 0b01111111) << shift
        if byte & 0b10000000 == 0:
            break
        position += 1
        shift += 7
    return value, position + 1

"""
みゃーねか？どうしたみゃーね～
ーー「私に天使が舞い降りた！」
"""
