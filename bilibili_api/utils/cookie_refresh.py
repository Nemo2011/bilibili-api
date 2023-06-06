"""
bilibili_api.utils.refresh_cookies

Cookies 刷新相关

感谢 bilibili-API-collect 提供的刷新 Cookies 的思路

https://socialsisteryi.github.io/bilibili-API-collect/docs/login/cookie_refresh.html
"""
from .network_httpx import request, get_session
from .utils import get_api
from .credential import Credential
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import binascii
import time
import uuid
import re

key = RSA.importKey('''\
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDLgd2OAkcGVtoE3ThUREbio0Eg
Uc/prcajMKXvkCKFCWhJYJcLkcM2DKKcSeFpD/j6Boy538YXnR6VhcuUJOhH2x71
nzPjfdTcqMz7djHum0qSZA0AyCBDABUqCrfNgCiJ00Ra7GmRj+YCK1NJEuewlb40
JNrRuoEUXpabUzGB8QIDAQAB
-----END PUBLIC KEY-----''')

API = get_api('cookies_refresh')

async def check_cookies(credential: Credential) -> bool:
    """
    检查是否需要刷新 Cookies

    Args: 
        credential (Credential): 用户凭证

    Return:
        bool: 是否需要刷新 Cookies
    """
    api = API["info"]["check_cookies"]
    return (await request("GET", api["url"], credential=credential))["refresh"]

def getCorrespondPath() -> str:
    """
    根据时间生成 CorrespondPath

    Return:
        str: CorrespondPath
    """
    ts = round(time.time() * 1000)
    cipher = PKCS1_OAEP.new(key, SHA256)
    encrypted = cipher.encrypt(f'refresh_{ts}'.encode())
    return binascii.b2a_hex(encrypted).decode()

async def get_refresh_csrf(credential: Credential) -> str:
    """
    获取刷新 Cookies 的 csrf

    Return:
        str: csrf
    """
    correspond_path = getCorrespondPath()
    api = API["operate"]["get_refresh_csrf"]
    cookies = credential.get_cookies()
    cookies["buvid3"] = str(uuid.uuid1())
    cookies["Domain"] = ".bilibili.com"
    resp = await get_session().request(
        "GET", api["url"].replace("{correspondPath}", correspond_path), 
        cookies=cookies)
    if resp.status_code == 404:
        raise Exception("correspondPath 过期或错误。")
    elif resp.status_code == 200:
        text = resp.text
        refresh_csrf = re.findall('<div id="1-name">(.+?)</div>', text)[0]
        return refresh_csrf
    elif resp.status_code != 200:
        raise Exception("获取刷新 Cookies 的 csrf 失败。")
    
async def refresh_cookies(credential: Credential) -> Credential:
    """
    刷新 Cookies

    Args:
        credential (Credential): 用户凭证
    
    Return:
        Credential: 新的用户凭证
    """
    api = API["operate"]["refresh_cookies"]
    credential.raise_for_no_bili_jct()
    credential.raise_for_no_ac_time_value()
    refresh_csrf = await get_refresh_csrf(credential)
    data = {
        "csrf": credential.bili_jct,
        "refresh_csrf": refresh_csrf,
        "refresh_token": credential.ac_time_value,
        "source": "main_web"
    }
    cookies = credential.get_cookies()
    cookies["buvid3"] = str(uuid.uuid1())
    cookies["Domain"] = ".bilibili.com"
    resp = await get_session().request(
        "POST", 
        api["url"], 
        cookies=cookies, 
        data=data)
    new_credential = Credential(sessdata=resp.cookies["SESSDATA"], 
                      bili_jct=resp.cookies["bili_jct"], 
                      dedeuserid=resp.cookies["DedeUserID"], 
                      ac_time_value=resp.json()["data"]["refresh_token"])
    await confirm_refresh(credential, new_credential)
    return new_credential

async def confirm_refresh(old_credential: Credential, new_credential: Credential) -> None:
    """
    让旧的refresh_token对应的 Cookie 失效
    """
    api = API["operate"]["confirm_refresh"]
    data = {
        "csrf": new_credential.bili_jct,
        "refresh_token": old_credential.ac_time_value
    }
    return await request("POST", api["url"], data=data, credential=new_credential)