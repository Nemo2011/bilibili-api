r"""
模块：splash
功能：客户端开屏图
此模块作者：david082321
项目GitHub地址：https://github.com/Passkou/bilibili_api
项目主页：https://passkou.com/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""

from . import utils, exceptions, common
import requests
import re
import json

API = utils.get_api()


def get_splash_list(mobi_app: str = "android", platform: str = "android",
                           height: int = 1920, width: int = 1080,
                           build: int = 999999999, birth: str = "",
                           verify: utils.Verify = None):
    """
    获取开屏启动画面
    :param build: 客户端内部版本号
    :param mobi_app: android/iphone/ipad
    :param platform: android/ios
    :param height: 高
    :param width: 宽
    :param birth: 生日日期
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    
    api = API["splash"]["splash"]["list"]
    params = {
        "build": build,
        "mobi_app": mobi_app,
        "platform": platform,
        "height": height,
        "width": width,
        "birth": birth
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp

def get_splash_bread(mobi_app: str = "android", platform: str = "android",
                           height: int = 1920, width: int = 1080,
                           ts: int = 1609430400, verify: utils.Verify = None,
                           appkey: str = "1d8b6e7d45233436",
                           appsec: str = "560c52ccd288fed045859ed18bffd973"):
    """
    获取新版开屏启动画面
    :param appkey:
    :param appsec:
    :param mobi_app: android/iphone/ipad
    :param platform: android/ios
    :param height: 高
    :param width: 宽
    :param ts: 当前UNIX秒
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["splash"]["splash"]["brand"]
    sign_params = "appkey="+appkey+"&mobi_app="+mobi_app+"&platform="+platform+"&screen_height="+str(height)+"&screen_width="+str(width)+"&ts="+str(ts)+appsec
    from sys import version_info
    if(version_info.major==2):
        import md5
        singing = md5.new()
        singing.update(sign_params.encode(encoding='utf-8'))
        sign = singing.hexdigest()
    else:
        import hashlib
        singing = hashlib.md5()
        singing.update(sign_params.encode(encoding='utf-8'))
        sign = singing.hexdigest()
    params = {
        "appkey": appkey,
        "mobi_app": mobi_app,
        "platform": platform,
        "screen_height": height,
        "screen_width": width,
        "ts": ts,
        "sign": sign
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp
