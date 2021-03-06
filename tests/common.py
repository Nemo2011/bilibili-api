from bilibili_api import Credential
import os


def get_credential():
    BILI_SESSDATA = os.getenv("BILI_SESSDATA")
    BILI_CSRF = os.getenv("BILI_CSRF")
    print(BILI_SESSDATA)
    if not BILI_SESSDATA and not BILI_CSRF:
        raise Exception("请在环境变量提供 BILI_SESSDATA 和 BILI_CSRF")
    return Credential(BILI_SESSDATA, BILI_CSRF)

