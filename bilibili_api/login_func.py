from . import login
from .utils.Credential import Credential
from .utils.utils import get_api
import json
import requests
import uuid
from .exceptions import LoginError
import enum

API = get_api("login")


class QrCodeLoginEvents(enum.Enum):
    """
    二维码登录状态枚举

    + SCAN: 未扫描二维码
    + CONF: 未确认登录
    + DONE: 成功
    """

    SCAN = "scan"
    CONF = "confirm"
    DONE = "done"


def get_qrcode():
    """
    获取二维码及登录密钥（后面有用）

    Returns:
        tuple[dir, str]: 第一项是二维码图片地址（本地缓存）和登录密钥。登录密钥需要保存。
    """
    img = login.update_qrcode()
    login_key = login.login_key
    return (img, login_key)


def check_qrcode_events(login_key):
    """
    检查登录状态。（建议频率 1s，这个 API 也有风控！）

    Args:
        login_key (str): 登录密钥（get_qrcode 的返回值第二项)

    Returns:
        list[QrCodeLoginEvents, str|Credential]: 状态(第一项）和信息（第二项）（如果成功登录信息为凭据类）
    """
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
        return [QrCodeLoginEvents.SCAN, events["message"]]
    elif events["data"] == -5:
        return [QrCodeLoginEvents.CONF, events["message"]]
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
        return [QrCodeLoginEvents.DONE, c]


def start_geetest_server():
    """
    验证码服务打开服务器

    Returns:
        ServerThread: 服务进程

    返回值内函数及属性: 
        - url   (str)     : 验证码服务地址
        - start (Callable): 开启进程
        - stop  (Callable): 结束进程
    
    ``` python
    print(start_geetest_server().url)
    ```
    """
    return login.start_server()


def close_geetest_server():
    """
    关闭极验验证服务（打开极验验证服务后务必关闭掉它，否则会卡住）
    """
    return login.close_server()


def done_geetest():
    """
    检查是否完成了极验验证。
    
    如果没有完成极验验证码就开始短信登录发送短信，那么可能会让你的项目卡住。

    Returns:
        bool: 是否完成极验验证
    """
    result = login.get_result()
    if result != -1:
        return True
    else:
        return False


COUNTRIES_LIST = login.get_countries_list()
countries_list = COUNTRIES_LIST
