import os

from bilibili_api import Credential

_credential_instance = None


def get_credential():
    global _credential_instance

    if _credential_instance is not None:
        return _credential_instance

    BILI_SESSDATA = os.getenv("BILI_SESSDATA")
    BILI_CSRF = os.getenv("BILI_CSRF")
    BILI_BUVID3 = os.getenv("BILI_BUVID3")
    BILI_BUVID4 = os.getenv("BILI_BUVID4")
    BILI_DEDEUSERID = os.getenv("BILI_DEDEUSERID")

    if not BILI_SESSDATA or not BILI_CSRF or not BILI_DEDEUSERID:
        raise Exception("缺少环境变量")

    _credential_instance = Credential(
        BILI_SESSDATA, BILI_CSRF, BILI_BUVID3, BILI_BUVID4, BILI_DEDEUSERID
    )
    return _credential_instance
