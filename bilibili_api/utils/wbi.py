import hashlib
import time
from functools import reduce
from typing import Tuple, Optional

from httpx import get as httpx_get

HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"}

def getMixinKey() -> str:
    resp_json = httpx_get("https://api.bilibili.com/x/web-interface/nav", headers=HEADERS).json()
    wbi_img: dict = resp_json["data"]["wbi_img"]
    img_url: str = wbi_img.get("img_url") # type: ignore
    sub_url: str = wbi_img.get("sub_url") # type: ignore
    img_value = img_url.split("/")[-1].split(".")[0]
    sub_value = sub_url.split("/")[-1].split(".")[0]
    ae = img_value + sub_value
    oe = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41,
          13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52]
    le = reduce(lambda s, i: s + ae[i], oe, "")
    return le[:32]

def encWbi(params: dict, mixin_key: Optional[str] = None) -> Tuple[str, int, str]:
    if not mixin_key:
        mixin_key = getMixinKey()
    wts = int(time.time())
    params["wts"] = wts
    Ae = "&".join([f'{key}={value}' for key, value in params.items()])
    w_rid = hashlib.md5((Ae + mixin_key).encode(encoding='utf-8')).hexdigest()
    return w_rid, wts, mixin_key