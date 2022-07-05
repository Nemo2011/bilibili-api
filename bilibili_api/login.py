"""
bilibili_api.login

登录

**虽然可能有其他函数，但是请忽略他们，这些并不重要**

**login_with_qrcode 用到了 tkinter，linux 的小伙伴请注意安装**
"""

import json
from bilibili_api.utils.Credential import Credential
from bilibili_api.utils.utils import get_api
from bilibili_api.utils.sync import sync
from bilibili_api.utils.network_httpx import get_session, request
from bilibili_api.utils.captcha import start_server, close_server, get_result
from PIL.ImageTk import PhotoImage
import qrcode
import os
import tempfile
import tkinter
import tkinter.font
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
id_ = 0 # 事件 id,用于取消 after 绑定


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
        events_api = API["qrcode"]["get_events"]
        data = {"oauthKey": login_key}
        session = get_session()
        events = json.loads(
            sync(session.request("POST", events_api["url"], data=data)).text
        )
        if events["data"] == -4:
            log.configure(text="请扫描二维码↑", fg="red", font=big_font)
        elif events["data"] == -5:
            log.configure(text="点下确认啊！", fg="orange", font=big_font)
        elif isinstance(events["data"], dict):
            url = events["data"]["url"]
            cookies_list = url.split("&")
            sessdata = ""
            bili_jct = ""
            for cookie in cookies_list:
                if cookie[:8] == "SESSDATA":
                    sessdata = cookie[9:]
                if cookie[:8] == "bili_jct":
                    bili_jct = cookie[9:]
            c = Credential(sessdata, bili_jct)
            global credential
            credential = c
            log.configure(text="成功！", fg="green", font=big_font)
            global start
            start = time.perf_counter()
            root.after(2000, destroy)
        id_ = root.after(50, update_events)
        # 刷新
        if time.perf_counter() - start > 120:
            update_qrcode()
            start = time.perf_counter()
    def destroy():
        global id_
        root.after_cancel(id_)
        root.destroy()
    root.after(50, update_events)
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
    encryptor = PKCS1_v1_5.new(RSA.importKey(bytes(key,'utf-8')))
    return str(base64.b64encode(encryptor.encrypt(bytes(_hash + password,'utf-8'))),'utf-8')

def get_geetest():
    start_server()
    while True:
        result = get_result()
        if result != -1:
            close_server()
            return result

def login_with_password(username: str, password: str):
    """
    密码登录。

    Args:
        username(str): 用户手机号、邮箱
        password(str): 密码

    Returns:
        Credential: 凭据
    """
    geetest_data = get_geetest()
    api_token = API['password']['get_token']
    sess = get_session()
    token_data = json.loads(sync(sess.get(api_token['url'])).text)
    hash_ = token_data['data']['hash']
    key = token_data['data']['key']
    final_password = encrypt(hash_, key, password)
    login_api = API['password']['login']
    params = {
        "source": 'main_h5',
        "username": username, 
        "password": final_password, 
        "keep": "true", 
        "go_url": 'https://www.bilibili.com/',
        "token": geetest_data['token'],
        "challenge": geetest_data['challenge'], 
        "validate": geetest_data['validate'], 
        "seccode": geetest_data['seccode']
    }
    print(sync(sess.request("POST", login_api['url'], params=params, headers={
          'content-type': 'application/x-www-form-urlencoded', 
          'user-agent': 'Mozilla/5.0',
          "referer": "https://passport.bilibili.com/login"
        })).text)
