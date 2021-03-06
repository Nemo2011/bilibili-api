r"""
模块：app
功能：客户端API
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
import time

API = utils.get_api()


def get_loading_images(mobi_app: str = "android", platform: str = "android",
                           height: int = 1920, width: int = 1080,
                           build: int = 999999999, birth: str = "",
                           verify: utils.Verify = None):
    """
    获取开屏启动画面
    :param build: 客户端内部版本号
    :param mobi_app: android / iphone / ipad
    :param platform: android / ios    / ios
    :param height: 屏幕高度
    :param width: 屏幕宽度
    :param birth: 生日日期(四位数，例 0101)
    :param verify:
    :return:
    :注意：返回的图片受到许多参数影响，详细对应表请参考 docs/模块/app.md
    """
    if verify is None:
        verify = utils.Verify()
    
    api = API["app"]["splash"]["list"]
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

def get_loading_images_special(mobi_app: str = "android", platform: str = "android",
                           height: int = 1920, width: int = 1080,
                           ts: int = int(time.time()),
                           appkey: str = "1d8b6e7d45233436",
                           appsec: str = "560c52ccd288fed045859ed18bffd973",
                           verify: utils.Verify = None):
    """
    获取特殊开屏启动画面
    :param appkey:
    :param appsec:
    :param mobi_app: android / iphone / ipad
    :param platform: android / ios    / ios
    :param height: 屏幕高度
    :param width: 屏幕宽度
    :param ts:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["app"]["splash"]["brand"]
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
