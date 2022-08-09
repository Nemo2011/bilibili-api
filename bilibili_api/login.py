"""
bilibili_api.login

登录

**虽然可能有其他函数，但是请忽略他们，这些并不重要**

**login_with_qrcode 用到了 tkinter，linux 的小伙伴请注意安装**
"""

import json
import re
from typing import Union
import uuid
import hashlib
import webbrowser

import requests
from .exceptions.LoginError import LoginError

from .utils.Credential import Credential
from .utils.utils import get_api
from .utils.sync import sync
from .utils.network_httpx import get_session, request, to_form_urlencoded
from .utils.captcha import start_server, close_server, get_result
from . import settings
import qrcode
import os
import tempfile
import time
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

API = get_api("login")

# ----------------------------------------------------------------
# 二维码登录
# ----------------------------------------------------------------

photo = None  # 图片的全局变量

start = time.perf_counter()
login_key = ""
qrcode_image = None
credential = Credential()
is_destroy = False
id_ = 0  # 事件 id,用于取消 after 绑定


def make_qrcode(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    img = qr.make_image()
    img.save(os.path.join(tempfile.gettempdir(), "qrcode.png"))
    return os.path.join(tempfile.gettempdir(), "qrcode.png")


def login_with_qrcode(root=None):
    """
    扫描二维码登录

    Args:
        root: 根窗口，默认为 tkinter.Tk()，如果有需要可以换成 tkinter.Toplevel()
    Returns:
        Credential: 凭据
    """
    global start
    global photo
    global login_key, qrcode_image
    global credential
    global id_
    import tkinter
    import tkinter.font
    from PIL.ImageTk import PhotoImage
    if root == None:
        root = tkinter.Tk()
    root.title("扫码登录")
    qrcode_image = update_qrcode()
    photo = PhotoImage(file=qrcode_image)
    qrcode_label = tkinter.Label(root, image=photo, width=500, height=500)
    qrcode_label.pack()
    big_font = tkinter.font.Font(root, size=25)
    log = tkinter.Label(root, text="请扫描二维码↑", font=big_font, fg="red")
    log.pack()

    def update_events():
        global id_
        global start, credential, is_destroy
        # log.configure(text="点下确认啊！", fg="orange", font=big_font)
        events_api = API["qrcode"]["get_events"]
        data = {"oauthKey": login_key}
        events = json.loads(
            requests.post(
                events_api["url"],
                data=data,
                cookies={"buvid3": str(uuid.uuid1()), "Domain": ".bilibili.com"},
            ).text
        )
        if "code" in events.keys() and events["code"] == -412:
            raise LoginError(events["message"])
        if events["data"] == -4:
            log.configure(text="请扫描二维码↑", fg="red", font=big_font)
        elif events["data"] == -5:
            log.configure(text="点下确认啊！", fg="orange", font=big_font)
        elif isinstance(events["data"], dict):
            url = events["data"]["url"]
            cookies_list = url.split("?")[1].split("&")
            sessdata = ""
            bili_jct = ""
            dede = ""
            for cookie in cookies_list:
                if cookie[:8] == "SESSDATA":
                    sessdata = cookie[9:]
                if cookie[:8] == "bili_jct":
                    bili_jct = cookie[9:]
                if cookie[:11].upper() == "DEDEUSERID=":
                    dede = cookie[11:]
            c = Credential(sessdata, bili_jct, dedeuserid=dede)
            global credential
            credential = c
            log.configure(text="成功！", fg="green", font=big_font)
            global start
            start = time.perf_counter()
            root.after(1000, destroy)
        id_ = root.after(500, update_events)
        # 刷新
        if time.perf_counter() - start > 120:
            update_qrcode()
            start = time.perf_counter()
        root.update()

    def destroy():
        global id_
        root.after_cancel(id_)
        root.destroy()

    root.after(500, update_events)
    root.mainloop()
    root.after_cancel(id_)
    return credential


def update_qrcode():
    global login_key, qrcode_image
    api = API["qrcode"]["get_qrcode_and_token"]
    qrcode_login_data = sync(request("GET", api["url"]))
    login_key = qrcode_login_data["oauthKey"]
    qrcode = qrcode_login_data["url"]
    qrcode_image = make_qrcode(qrcode)
    return qrcode_image


# ----------------------------------------------------------------
# 密码登录
# ----------------------------------------------------------------


def encrypt(_hash, key, password):
    encryptor = PKCS1_v1_5.new(RSA.importKey(bytes(key, "utf-8")))
    return str(
        base64.b64encode(encryptor.encrypt(bytes(_hash + password, "utf-8"))), "utf-8"
    )


def get_geetest():
    if get_result() != -1:
        return get_result()
    thread = start_server()
    if settings.geetest_auto_open:
        webbrowser.open(thread.url)
    try:
        while True:
            result = get_result()
            if result != -1:
                close_server()
                return result
    except KeyboardInterrupt:
        close_server()
        exit()


def login_with_password(username: str, password: str):
    """
    密码登录。

    Args:
        username(str): 用户手机号、邮箱
        password(str): 密码

    Returns:
        Union[Credential, Check]: 如果需要验证，会返回 [`Check`](#check) 类，否则返回 `Credential` 类。
    """
    api_token = API["password"]["get_token"]
    sess = get_session()
    token_data = json.loads(sync(sess.get(api_token["url"])).text)
    hash_ = token_data["data"]["hash"]
    key = token_data["data"]["key"]
    final_password = encrypt(hash_, key, password)
    login_api = API["password"]["login"]
    appkey = "bca7e84c2d947ac6"
    appsec = "60698ba2f68e01ce44738920a0ffe768"
    datas = {
        "actionKey": "appkey",
        "appkey": appkey,
        "build": 6270200,
        "captcha": "",
        "challenge": "",
        "channel": "bili",
        "device": "phone",
        "mobi_app": "android",
        "password": final_password,
        "permission": "ALL",
        "platform": "android",
        "seccode": "",
        "subid": 1,
        "ts": int(time.time()),
        "username": username,
        "validate": ""
    }
    form_urlencoded = to_form_urlencoded(datas)
    md5_string = form_urlencoded + appsec
    hasher = hashlib.md5(md5_string.encode(encoding='utf-8'))
    datas['sign'] = hasher.hexdigest()
    login_data = json.loads(
        sync(
            sess.request(
                "POST",
                login_api["url"],
                data=datas,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Mozilla/5.0",
                    "Referer": "https://passport.bilibili.com/login",
                },
                cookies={
                    "buvid3": str(uuid.uuid1())
                }
            )
        ).text
    )
    if login_data["code"] == 0:
        if login_data['data']['status'] == 2:
            return Check(login_data['data']['url'], username)
        sessdata = login_data['data']['cookie_info']['cookies'][0]['value']
        bili_jct = login_data['data']['cookie_info']['cookies'][1]['value']
        dede = login_data['data']['cookie_info']['cookies'][2]['value']
        c = Credential(sessdata, bili_jct, dedeuserid=dede)
        return c
    else:
        raise LoginError(login_data["message"])


# ----------------------------------------------------------------
# 验证码登录
# ----------------------------------------------------------------

captcha_id = None


def get_countries_list():
    """
    获取国际地区代码列表

    Returns:
        List[dict]: 地区列表
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/countries_codes.json"),
        encoding="utf8",
    ) as f:
        codes_list = json.loads(f.read())
    countries = []
    for country in codes_list:
        name = country["cname"]
        id_ = country["country_id"]
        code = country["id"]
        countries.append({"name": name, "id": code, "code": int(id_)})
    return countries


def search_countries(keyword: str):
    """
    搜索一个地区及其国际地区代码

    Args:
        keyword(str): 关键词
    Returns:
        List[dict]: 地区列表
    """
    list_ = get_countries_list()
    countries = []
    for country in list_:
        if keyword in country["name"] or keyword.lstrip("+") in country["code"]:
            countries.append(country)
    return countries


def have_country(keyword: str):
    """
    是否有地区

    Args:
        keyword(str): 关键词

    Returns:
        bool: 是否存在
    """
    list_ = get_countries_list()
    for country in list_:
        if country["name"] == keyword:
            return True
    return False


def have_code(code: Union[str, int]):
    """
    是否存在地区代码

    Args:
        code(Union[str, int]): 代码

    Returns:
        bool: 是否存在
    """
    list_ = get_countries_list()
    if isinstance(code, str):
        code = code.lstrip("+")
        try:
            int_code = int(code)
        except ValueError:
            raise ValueError("地区代码参数错误")
    elif isinstance(code, int):
        int_code = code
    else:
        return False
    for country in list_:
        if country["code"] == int_code:
            return True
    return False


def get_code_by_country(country: str):
    """
    获取地区对应代码

    Args:
        country(str): 地区名

    Returns:
        int: 对应的代码，没有返回 -1
    """
    list_ = get_countries_list()
    for country_ in list_:
        if country_["name"] == country:
            return country_["code"]
    return -1


def get_id_by_code(code: int):
    """
    获取地区码对应的地区 id

    Args:
        code(int): 地区吗

    Returns:
        int: 对应的代码，没有返回 -1
    """
    list_ = get_countries_list()
    for country_ in list_:
        if country_["code"] == code:
            return country_["id"]
    return -1


class PhoneNumber:
    def __init__(self, number: str, country: Union[str, int] = "+86"):
        """
        number(string): 手机号
        country(string): 地区/地区码，如 +86
        """
        number = number.replace("-", "")
        if not have_country(country):
            if not have_code(country):
                raise ValueError("地区代码或地区名错误")
            else:
                code = country if isinstance(country, int) else int(country.lstrip("+"))
        else:
            code = get_code_by_country(country)
        self.number = number
        self.code = code
        self.id_ = get_id_by_code(self.code)

    def __str__(self):
        return f"+{self.code} {self.number} (bilibili 地区 id {self.id_})"


def send_sms(phonenumber: PhoneNumber):
    """
    发送验证码

    Args:
        phonenumber: 手机号类

    Returns:
        None
    """
    global captcha_id
    api = API["sms"]["send"]
    code = phonenumber.code
    tell = phonenumber.number
    geetest_data = get_geetest()
    sess = get_session()
    return_data = json.loads(
        sync(
            sess.post(
                url=api["url"],
                data={
                    "tel": tell,
                    "cid": code,
                    "source": "main_web",
                    "token": geetest_data["token"],
                    "challenge": geetest_data["challenge"],
                    "validate": geetest_data["validate"],
                    "seccode": geetest_data["seccode"],
                },
            )
        ).text
    )
    if return_data["code"] == 0:
        captcha_id = return_data["data"]["captcha_key"]
    else:
        raise LoginError(return_data["message"])


def login_with_sms(phonenumber: PhoneNumber, code: str):
    """
    验证码登录

    Args:
        phonenumber(string): 手机号类
        code(string)       : 验证码

    Returns:
        Credential: 凭据类
    """
    global captcha_id
    sess = get_session()
    api = API["sms"]["login"]
    if captcha_id == None:
        raise LoginError("请申请或重新申请发送验证码")
    return_data = json.loads(
        sync(
            sess.request(
                "POST",
                url=api["url"],
                data={
                    "tel": phonenumber.number,
                    "cid": phonenumber.code,
                    "code": code,
                    "source": "main_web",
                    "captcha_key": captcha_id,
                    "keep": "true",
                },
            )
        ).text
    )
    if return_data["code"] == 0:
        captcha_id = None
        url = return_data["data"]["url"]
        cookies_list = url.split("?")[1].split("&")
        sessdata = ""
        bili_jct = ""
        dede = ""
        for cookie in cookies_list:
            if cookie[:8] == "SESSDATA":
                sessdata = cookie[9:]
            if cookie[:8] == "bili_jct":
                bili_jct = cookie[9:]
            if cookie[:11].upper() == "DEDEUSERID=":
                dede = cookie[11:]
        c = Credential(sessdata, bili_jct, dedeuserid=dede)
        return c
    else:
        raise LoginError(return_data["message"])


# 验证类


class Check:
    """
    验证类，如果密码登录需要验证会返回此类
    """

    def __init__(self, check_url, username):
        self.check_url = check_url
        self.now_time = time.perf_counter()
        self.phonenumber = None

    def set_phone(self, phonenumber):
        """
        设置手机号

        Args:
            phonenumber: 手机号类

        Returns:
            None
        """
        self.phonenumber = phonenumber

    def send_code(self):
        """
        发送验证码

        Returns:
            None
        """
        if self.phonenumber == None:
            raise LoginError("请使用 self.set_phone 函数设置手机号")
        send_sms(self.phonenumber)

    def login(self, code: str):
        """
        登录

        Args:
            code(string)       : 验证码

        Returns:
            Credential: 凭据类
        """
        if self.phonenumber == None:
            raise LoginError("请使用 self.set_phone 函数设置手机号")
        return login_with_sms(self.phonenumber, code)
