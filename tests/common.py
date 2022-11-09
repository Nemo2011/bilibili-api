import asyncio
from bilibili_api import Credential
import os


def get_credential():
    return Credential(
        "c7b2cf77%2C1683501469%2C41f27%2Ab2", 
        "62d9c7f9f25e8ff4599c2d1e06ad4f28", 
        "CE60F42D-7D97-081C-E818-0F96DC47826549832infoc",
        "1666311555"
    )
    BILI_SESSDATA = os.getenv("BILI_SESSDATA")
    BILI_CSRF = os.getenv("BILI_CSRF")
    BILI_BUVID3 = os.getenv("BILI_BUVID3")
    BILI_DEDEUSERID = os.getenv("BILI_DEDEUSERID")

    if not BILI_SESSDATA or not BILI_CSRF or not BILI_BUVID3 or not BILI_DEDEUSERID:
        raise Exception("缺少环境变量")

    return Credential(BILI_SESSDATA, BILI_CSRF, BILI_BUVID3, BILI_DEDEUSERID)


async def delay():
    await asyncio.sleep(float(os.getenv("BILI_RATELIMIT")))
