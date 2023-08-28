"""
bilibili_api.login

登录

**虽然可能有其他函数，但是请忽略他们，这些并不重要**

**login_with_qrcode 用到了 tkinter，linux 的小伙伴请注意安装**
"""

import os
import sys
import json
import time
import uuid
import base64
import tempfile
import webbrowser
from typing import Dict, List, Union

import rsa
import httpx
import qrcode
from yarl import URL

from . import settings
from .utils.sync import sync
from .utils.utils import get_api
from .utils.credential import Credential
from .exceptions.LoginError import LoginError
from .utils.network import to_form_urlencoded
from .utils.network_httpx import HEADERS, get_session, get_spi_buvid_sync
from .utils.captcha import get_result, close_server, start_server
from .utils.safecenter_captcha import get_result as safecenter_get_result
from .utils.safecenter_captcha import close_server as safecenter_close_server
from .utils.safecenter_captcha import start_server as safecenter_start_server

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

def parse_credential_url(events: dict) -> Credential:
    url = events["data"]["url"]
    cookies_list = url.split("?")[1].split("&")
    sessdata = ""
    bili_jct = ""
    dedeuserid = ""
    for cookie in cookies_list:
        if cookie[:8] == "SESSDATA":
            sessdata = cookie[9:]
        if cookie[:8] == "bili_jct":
            bili_jct = cookie[9:]
        if cookie[:11].upper() == "DEDEUSERID=":
            dedeuserid = cookie[11:]
    ac_time_value=events["data"]["refresh_token"]
    buvid3=get_spi_buvid_sync()["b_3"]
    return Credential(sessdata=sessdata, 
                        bili_jct=bili_jct, 
                        buvid3=buvid3, 
                        dedeuserid=dedeuserid, 
                        ac_time_value=ac_time_value)
    
def make_qrcode(url) -> str:
    qr = qrcode.QRCode()
    qr.add_data(url)
    img = qr.make_image()
    img.save(os.path.join(tempfile.gettempdir(), "qrcode.png"))
    print("二维码已保存至", os.path.join(tempfile.gettempdir(), "qrcode.png"))
    return os.path.join(tempfile.gettempdir(), "qrcode.png")

def update_qrcode_data() -> dict:
    api = API["qrcode"]["get_qrcode_and_token"]
    qrcode_data = httpx.get(api["url"], follow_redirects=True).json()['data']
    return qrcode_data


def login_with_qrcode(root=None) -> Credential:
    """
    扫描二维码登录

    Args:
        root (tkinter.Tk | tkinter.Toplevel, optional): 根窗口，默认为 tkinter.Tk()，如果有需要可以换成 tkinter.Toplevel(). Defaults to None.

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
    qrcode_data = update_qrcode_data()
    login_key = qrcode_data["qrcode_key"]
    qrcode_image = make_qrcode(qrcode_data["url"])
    photo = PhotoImage(file=qrcode_image)
    qrcode_label = tkinter.Label(root, image=photo, width=600, height=600)
    qrcode_label.pack()
    big_font = tkinter.font.Font(root, size=25)
    log = tkinter.Label(root, text="请扫描二维码↑", font=big_font, fg="red")
    log.pack()

    def update_events():
        global id_
        global start, credential, is_destroy, login_key
        events = login_with_key(login_key)
        if "code" in events.keys() and events["code"] == 0:
            if events["data"]["code"] == 86101:
                log.configure(text="请扫描二维码↑", fg="red", font=big_font)
            elif events["data"]["code"] == 86090:
                log.configure(text="点下确认啊！", fg="orange", font=big_font)
            elif events["data"]["code"] == 86038:
                raise LoginError("二维码过期，请扫新二维码！")
            elif events["data"]["code"] == 0:
                log.configure(text="成功！", fg="green", font=big_font)
                credential = parse_credential_url(events)
                root.after(1000, destroy) 
                return 0
            id_ = root.after(500, update_events)
            if time.perf_counter() - start > 120: # 刷新
                qrcode_data = update_qrcode_data()
                login_key = qrcode_data["qrcode_key"]
                qrcode_image = make_qrcode(qrcode_data["url"])
                photo = PhotoImage(file=qrcode_image)
                qrcode_label = tkinter.Label(root, image=photo, width=600, height=600)
                qrcode_label.pack()
                start = time.perf_counter()

        root.update()

    def destroy():
        global id_
        root.after_cancel(id_)  # type: ignore
        root.destroy()

    root.after(500, update_events)
    root.mainloop()
    root.after_cancel(id_)  # type: ignore
    return credential

def login_with_qrcode_term() -> Credential:
    """
    终端扫描二维码登录

    Args:

    Returns:
        Credential: 凭据
    """
    import qrcode_terminal
    qrcode_data = update_qrcode_data()
    qrcode_url = qrcode_data["url"]
    login_key = qrcode_data["qrcode_key"]
    print(qrcode_terminal.qr_terminal_str(qrcode_url) + "\n")
    while True:
        events = login_with_key(login_key)
        if "code" in events.keys() and events["code"] == 0:
            if events["data"]["code"] == 86101:
                sys.stdout.write('\r 请扫描二维码↑') 
                sys.stdout.flush()
            elif events["data"]["code"] == 86090:
                sys.stdout.write('\r 点下确认啊！') 
                sys.stdout.flush()
            elif events["data"]["code"] == 86038:
                print("二维码过期，请扫新二维码！")
                qrcode_data = update_qrcode_data()
                qrcode_url = qrcode_data["url"]
                print(qrcode_terminal.qr_terminal_str(qrcode_url) + "\n")
            elif events["data"]["code"] == 0:
                sys.stdout.write('\r 成功！') 
                sys.stdout.flush()
                return parse_credential_url(events)
            elif "code" in events.keys():
                raise LoginError(events["message"])
        time.sleep(0.5)


def login_with_key(key: str) -> dict:
    params = {"qrcode_key": key, "source": "main-fe-header"}
    events_api = API["qrcode"]["get_events"]
    events = httpx.get(
            events_api["url"],
            params=params,
            cookies={"buvid3": str(uuid.uuid1()), "Domain": ".bilibili.com"},
        ).json()
    return events




# ----------------------------------------------------------------
# 密码登录
# ----------------------------------------------------------------


def encrypt(_hash, key, password) -> str:
    rsa_key = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode("utf-8"))
    data = str(
        base64.b64encode(rsa.encrypt(bytes(_hash + password, "utf-8"), rsa_key)),
        "utf-8",
    )
    return data


def get_geetest() -> object:
    if get_result() != -1:
        return get_result()
    thread = start_server()
    if settings.geetest_auto_open:
        webbrowser.open(thread.url)  # type: ignore
    try:
        while True:
            result = get_result()
            if result != -1:
                close_server()
                return result
    except KeyboardInterrupt:
        close_server()
        exit()


def login_with_password(username: str, password: str) -> Union[Credential, "Check"]:
    """
    密码登录。

    Args:
        username (str): 用户手机号、邮箱

        password (str): 密码

    Returns:
        Union[Credential, Check]: 如果需要验证，会返回 `Check` 类，否则返回 `Credential` 类。
    """
    api_token = API["password"]["get_token"]
    geetest_data = get_geetest()
    sess = httpx.Client()
    token_data = json.loads(sess.get(api_token["url"]).text)
    hash_ = token_data["data"]["hash"]
    key = token_data["data"]["key"]
    final_password = encrypt(hash_, key, password)
    login_api = API["password"]["login"]
    data = {
        "username": username,
        "password": final_password,
        "keep": True,
        "token": geetest_data["token"],  # type: ignore
        "challenge": geetest_data["challenge"],  # type: ignore
        "validate": geetest_data["validate"],  # type: ignore
        "seccode": geetest_data["seccode"],  # type: ignore
    }
    resp = sess.request(
        "POST",
        login_api["url"],
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://passport.bilibili.com/login",
        },
        cookies={"buvid3": str(uuid.uuid1())},
    )
    login_data = resp.json()
    if login_data["code"] == 0:
        if login_data["data"]["status"] == 1:
            return Check(login_data["data"]["url"])
        elif login_data["data"]["status"] == 2:
            raise LoginError("需要手机号进一步验证码验证，请直接通过验证码登录")
        return Credential(
            sessdata=resp.cookies.get("SESSDATA"),
            bili_jct=resp.cookies.get("bili_jct"),
            dedeuserid=resp.cookies.get("DedeUserID"),
            ac_time_value=login_data["data"]["refresh_token"],
        )
    else:
        raise LoginError(login_data["message"])


# ----------------------------------------------------------------
# 验证码登录
# ----------------------------------------------------------------

captcha_id = None


def get_countries_list() -> List[Dict]:
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


def search_countries(keyword: str) -> List[Dict]:
    """
    搜索一个地区及其国际地区代码

    Args:
        keyword (str): 关键词

    Returns:
        List[dict]: 地区列表
    """
    list_ = get_countries_list()
    countries = []
    for country in list_:
        if keyword in country["name"] or keyword.lstrip("+") in country["code"]:
            countries.append(country)
    return countries


def have_country(keyword: str) -> bool:
    """
    是否有地区

    Args:
        keyword (str): 关键词

    Returns:
        bool: 是否存在
    """
    list_ = get_countries_list()
    for country in list_:
        if country["name"] == keyword:
            return True
    return False


def have_code(code: Union[str, int]) -> bool:
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


def get_code_by_country(country: str) -> int:
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


def get_id_by_code(code: int) -> int:
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
    """
    手机号类
    """

    def __init__(self, number: str, country: Union[str, int] = "+86"):
        """
        Args:
            number(str): 手机号

            country(str): 地区/地区码，如 +86
        """
        number = number.replace("-", "")
        if not have_country(country):  # type: ignore
            if not have_code(country):
                raise ValueError("地区代码或地区名错误")
            else:
                code = country if isinstance(country, int) else int(country.lstrip("+"))
        else:
            code = get_code_by_country(country)  # type: ignore
        self.number = number
        self.code = code
        self.id_ = get_id_by_code(self.code)

    def __str__(self):
        return f"+{self.code} {self.number} (bilibili 地区 id {self.id_})"


def send_sms(phonenumber: PhoneNumber) -> None:
    """
    发送验证码

    Args:
        phonenumber (PhoneNumber): 手机号类
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
                data=to_form_urlencoded(
                    {
                        "source": "main-fe-header",
                        "tel": tell,
                        "cid": code,
                        "validate": geetest_data["validate"],  # type: ignore
                        "token": geetest_data["token"],  # type: ignore
                        "seccode": geetest_data["seccode"],  # type: ignore
                        "challenge": geetest_data["challenge"],  # type: ignore
                    }
                ),
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Referer": "https://www.bilibili.com",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                cookies={"buvid3": "E9BAB99E-FE1E-981E-F772-958B7F572FF487330infoc"},
            )
        ).text
    )
    if return_data["code"] == 0:
        captcha_id = return_data["data"]["captcha_key"]
    else:
        raise LoginError(return_data["message"])


def login_with_sms(phonenumber: PhoneNumber, code: str) -> Credential:
    """
    验证码登录

    Args:
        phonenumber (str): 手机号类
        code        (str): 验证码

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
                headers=HEADERS,
            )
        ).text
    )
    # return_data["status"] 已改为 return_data["data"]["status"]
    # {'code': 0, 'message': '0', 'ttl': 1, 'data': {'is_new': False, 'status': 0, 'message': '', 'url': '', 'hint': '登录成功', 'in_reg_audit': 0, 'refresh_token': '', 'timestamp': }}
    if return_data["code"] == 0 and return_data["data"]["status"] != 5:
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
        c = Credential(
            sessdata=sessdata,
            bili_jct=bili_jct,
            dedeuserid=dede,
            ac_time_value=return_data["data"]["refresh_token"],
        )
        return c
    elif return_data["data"]["status"] == 5:
        return Check(return_data["data"]["url"])  # type: ignore
    else:
        raise LoginError(return_data["message"])


# 验证类


def get_safecenter_geetest() -> object:
    if safecenter_get_result() != -1:
        return safecenter_get_result()
    thread = safecenter_start_server()
    if settings.geetest_auto_open:
        webbrowser.open(thread.url)  # type: ignore
    try:
        while True:
            result = safecenter_get_result()
            if result != -1:
                safecenter_close_server()
                return result
    except KeyboardInterrupt:
        safecenter_close_server()
        exit()


class Check:
    """
    验证类，如果密码登录需要验证会返回此类

    Attributes:
        check_url (str): 验证 url
        tmp_token (str): 验证 token
    """

    def __init__(self, check_url):
        self.check_url = check_url
        self.yarl_url = URL(self.check_url)
        self.tmp_token = self.yarl_url.query.get("tmp_token")
        self.geetest_result = None
        self.captcha_key = None

    def fetch_info(self) -> dict:
        """
        获取验证信息

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["safecenter"]["check_info"]
        self.tmp_token = self.check_url.split("?")[1].split("&")[0][10:]
        params = {"tmp_code": self.tmp_token}
        return json.loads(httpx.get(api["url"], params=params).text)["data"]
