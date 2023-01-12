# bilibili_api.login

import os
from bilibili_api import login

username = os.getenv("BILI_PHONE")
password = os.getenv("BILI_PASSWORD")


# async def test_a_password_login():
#     return login.login_with_password(username, password)
