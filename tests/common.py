from bilibili_api import Credential, login
import os


def get_credential():
    BILI_SESSDATA = os.getenv("BILI_SESSDATA")
    BILI_CSRF = os.getenv("BILI_CSRF")
    BILI_BUVID3 = os.getenv("BILI_BUVID3")
    BILI_DEDEUSERID = os.getenv("BILI_DEDEUSERID")

    if not BILI_SESSDATA or not BILI_CSRF or not BILI_BUVID3 or not BILI_DEDEUSERID:
        print(Exception("缺少环境变量"))
        cred = login.login_with_qrcode_term()
        os.environ["BILI_SESSDATA"] = cred.sessdata
        os.environ["BILI_CSRF"] = cred.bili_jct
        os.environ["BILI_BUVID3"] = cred.buvid3
        os.environ["BILI_DEDEUSERID"] = cred.dedeuserid
        BILI_SESSDATA = os.getenv("BILI_SESSDATA")
        BILI_CSRF = os.getenv("BILI_CSRF")
        BILI_BUVID3 = os.getenv("BILI_BUVID3")
        BILI_DEDEUSERID = os.getenv("BILI_DEDEUSERID")
    
    return Credential(BILI_SESSDATA, BILI_CSRF, BILI_BUVID3, BILI_DEDEUSERID)
    