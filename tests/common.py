import asyncio
from bilibili_api import Credential
import os


def get_credential():
    BILI_SESSDATA = os.getenv("BILI_SESSDATA")
    BILI_CSRF = os.getenv("BILI_CSRF")
    BILI_BUVID3 = os.getenv("BILI_BUVID3")

    if not BILI_SESSDATA or not BILI_CSRF or not BILI_BUVID3:
        raise Exception("缺少环境变量")
    return Credential(BILI_SESSDATA, BILI_CSRF, BILI_BUVID3)


async def delay():
    await asyncio.sleep(float(os.getenv('BILI_RATELIMIT')))
