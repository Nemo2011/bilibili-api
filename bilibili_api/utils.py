import json
from functools import wraps
import datetime
import time
import os

__path = os.path.dirname(__file__)


def get_apis():
    with open(os.path.join(__path, "api.json"), "r", encoding="utf-8") as f:
        apis = json.loads(f.read())
        f.close()
    return apis


def verify(sessdata, csrf="False"):
    def decoration(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cookies = {
                "SESSDATA": sessdata
            }
            if csrf == "False":
                ret = func(*args, **kwargs, cookies=cookies)
            else:
                ret = func(*args, **kwargs, cookies=cookies, csrf=csrf)
            return ret
        return wrapper
    return decoration


def use_headers(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }
        ret = func(*args, **kwargs, headers=headers)
        return ret
    return wrapper


class Danmaku:
    def __init__(self, text, dm_time=0.0, send_time=time.time(), id="False", color=int("FFFFFF", 16),
                 mode=1, font_size=25, is_sub=False):
        self.dm_time = datetime.timedelta(seconds=float(dm_time))
        self.send_time = datetime.datetime.fromtimestamp(int(send_time))
        self.id = id
        self.color = int(color)
        self.mode = int(mode)
        self.font_size = int(font_size)
        self.is_sub = is_sub
        self.text = text
        self.font_size_map = {
            "small": 18,
            "normal": 25,
            "big": 36
        }
        self.mode_map = {
            "fly": 1,
            "top": 5,
            "bottom": 4
        }

    def __str__(self):
        ret = "%s, %s, %s" % (self.send_time, self.dm_time, self.text)
        return ret

    def __len__(self):
        return len(self.text)

    def set_hex_color(self, hex_color):
        dec = int(hex_color, 16)
        self.color = dec

    def set_mode(self, mode):
        self.mode = self.mode_map[mode]

    def set_font_size(self, font_size):
        self.font_size = self.font_size_map[font_size]

    def get_hex_color(self):
        return hex(self.color)

