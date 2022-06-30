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
import qrcode
import os
import tempfile
import tkinter
import tkinter.font
import time

API = get_api("login")

global photo

def make_qrcode(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    img = qr.make_image()
    img.save(os.path.join(tempfile.gettempdir(), "qrcode.png"))
    return os.path.join(tempfile.gettempdir(), "qrcode.png")

start = time.perf_counter()
login_key = ""
qrcode_image = None
credential = None

def login_with_qrcode(root=None):
    """
    扫描二维码登录

    Args:
        root: 根窗口，默认为 tkinter.Tk()，如果有需要可以换成 tkinter.Toplevel()
    Returns:
        Cookies(凭据类)
    """
    global start
    global photo
    global login_key, qrcode_image
    global credential
    if root == None:
        root = tkinter.Tk()
    root.title("扫码登录")
    qrcode_image = update_qrcode()
    photo = tkinter.PhotoImage(file=qrcode_image)
    qrcode_label = tkinter.Label(root, image=photo, width=500, height=500)
    qrcode_label.pack()
    big_font = tkinter.font.Font(root, size=25)
    log = tkinter.Label(root, text="请扫描二维码↑", font=big_font, fg="red")
    log.pack()
    def update_events():
        global start
        events_api = API['qrcode']['get_events']
        data = {
            "oauthKey": login_key
        }
        session = get_session()
        events = json.loads(sync(session.request("POST", events_api['url'], data=data)).text)
        if events["data"] == -4:
            log.configure(text="请扫描二维码↑", fg="red", font=big_font)
        elif events["data"] == -5:
            log.configure(text="点下确认啊！", fg="orange", font=big_font)
        elif events["data"] == -2:
            qrcode_image = update_qrcode()
            photo = tkinter.PhotoImage(file=qrcode_image)
            qrcode_label.configure(image=photo)
            qrcode_label.grid()
            start = time.perf_counter()
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
            root.after(2000, root.destroy)
        root.after(1000, update_events)
    root.after(1000, update_events)
    while True:
        root.update()
        if credential != None:
            return credential


def update_qrcode():
    global login_key, qrcode_image
    api = API['qrcode']['get_qrcode_and_token']
    qrcode_login_data = sync(request("GET", api['url']))
    login_key = qrcode_login_data['oauthKey']
    qrcode = qrcode_login_data['url']
    qrcode_image = make_qrcode(qrcode)
    return qrcode_image
