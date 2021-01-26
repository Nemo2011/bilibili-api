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
    """
    补充获取结果关系图
    mobi_app	platform	width	height	result(width x height)
    android	android	200	300	320x480
    android	android	400	700	375x647
    android	android	300	400	480x640
    android	android	2900	4400	480x728
    android	android	300	500	480x800
    android	android	0	100	480x854
    android	android	800	1300	600x976
    android	android	600	900	640x960
    android	android	1300	2300	640x1136
    android	android	1100	1800	720x1184
    android	android	1000	1700	720x1208
    android	android	900	1600	720x1280
    iphone	ios	500	900	750x1334
    android	android	0	0	768x976
    android	android	900	1200	768x1024
    android	android	900	1500	768x1280
    android	android	1700	2600	800x1216
    android	android	900	1400	800x1232
    android	android	500	800	800x1280
    ipad	ios	400	300	1024x768
    android	android	1700	2800	1080x1776
    android	android	1080	1920	1080x1920
    iphone	ios	0	100	1125x2436
    android	android	1200	2000	1152x1920
    iphone	ios	900	1600	1242x2208
    android	android	1800	3200	1440x2560
    android	android	1500	2000	1536x2048
    android	android	1500	2500	1536x2560
    android	android	1500	2400	1600x2560
    ipad	ios	0	100	2048x1536
    android	android	500	700	2048x2732
    ipad	ios	0	0	2732x2048
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
                           screen_height: int = 1920, screen_width: int = 1080,
                           ts: int = 1609430400, verify: utils.Verify = None):
    """
    获取新版开屏启动画面
    :param mobi_app: android/iphone/ipad
    :param platform: android/ios
    :param screen_height: 高
    :param screen_width: 宽
    :param ts: 当前UNIX秒
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["splash"]["splash"]["brand"]
    sign_params = "appkey=1d8b6e7d45233436&mobi_app="+mobi_app+"&platform="+platform+"&screen_height="+str(screen_height)+"&screen_width="+str(screen_width)+"&ts="+str(ts)+"560c52ccd288fed045859ed18bffd973"
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
        "appkey": "1d8b6e7d45233436",
        "mobi_app": mobi_app,
        "platform": platform,
        "screen_height": screen_height,
        "screen_width": screen_width,
        "ts": ts,
        "sign": sign
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp
