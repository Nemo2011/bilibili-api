# bilibili_api.dynamic

from datetime import datetime
from time import time
from bilibili_api import dynamic, user, Picture
from . import common

credential = common.get_credential()

dy = None

draft_ids = []


async def test_a_send_dynamic():
    # 测试发送动态
    print("测试立即发送纯文本动态")
    text_dynamic_build = dynamic.BuildDynmaic().add_text("测试立即发送纯文本动态").add_image(Picture.from_file("./design/logo.png"))
    global dy
    dy = await dynamic.send_dynamic(text_dynamic_build, credential=credential)


async def test_b_get_schedules_list():
    return await dynamic.get_schedules_list(credential=credential)


async def test_e_Dynamic_get_info():
    global dy
    return await dy.get_info() # type: ignore

async def test_f_Dynamic_get_reposts():
    return await dy.get_reposts() # type: ignore


async def test_g_Dynamic_set_like():
    return await dy.set_like() # type: ignore

async def test_i_Dynamic_delete():
    return await dy.delete() # type: ignore

async def test_j_get_new_dynamic_users():
    return await dynamic.get_new_dynamic_users(common.get_credential())

async def test_k_get_live_users():
    return await dynamic.get_live_users(credential = common.get_credential())

async def test_l_get_dynamic_page_UPs_info():
    return await dynamic.get_dynamic_page_UPs_info(credential = common.get_credential())

async def test_m_get_dynamic_page_info_by_type():
    return await dynamic.get_dynamic_page_info(credential = common.get_credential(), _type=dynamic.DynamicType.ALL)

async def test_m_get_dynamic_page_info_by_mid():
    return await dynamic.get_dynamic_page_info(credential = common.get_credential(), host_mid=12434430)
