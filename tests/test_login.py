# bilibili_api.login

import os

from bilibili_api import login
from bilibili_api.login import login_with_qrcode

username = os.getenv("BILI_PHONE")
password = os.getenv("BILI_PASSWORD")


# async def test_a_password_login():
#     return login.login_with_password(username, password)


login_with_qrcode()
