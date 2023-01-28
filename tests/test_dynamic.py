# bilibili_api.dynamic

from datetime import datetime
from time import time
from bilibili_api import dynamic, user, Picture
from . import common

credential = common.get_credential()

dyid = []

draft_ids = []


async def test_a_send_dynamic():
    # 测试发送动态
    print("测试立即发送纯文本动态")
    resp = await dynamic.send_dynamic(
        text="测试立即发送纯文本动态 @1882430995 ", credential=credential
    )
    print(resp)
    dyid.append(resp["dynamic_id"])

    print("测试立即发送图片动态")
    resp = await dynamic.send_dynamic(
        text="测试立即发送图片动态",
        images=[Picture.from_file("./design/logo.png")],
        credential=credential,
    )
    dyid.append(resp["dynamic_id"])
    print(resp)


async def test_b_get_schedules_list():
    return await dynamic.get_schedules_list(credential=credential)


dy = None


async def test_e_Dynamic_get_info():
    global dy
    dy = dynamic.Dynamic(dyid.pop(), credential)

    return await dy.get_info()


async def test_f_Dynamic_get_reposts():
    return await dy.get_reposts()


async def test_g_Dynamic_set_like():
    return await dy.set_like()


# async def test_h_Dynamic_repost():
#    resp = await dy.repost()
#
#    print(resp)
#    return resp


async def test_i_Dynamic_delete():
    return await dy.delete()

async def test_j_get_new_dynamic_users():
    return await dynamic.get_new_dynamic_users(common.get_credential())

async def test_k_get_live_users():
    return await dynamic.get_live_users(credential = common.get_credential())

async def test_l_get_dynamic_page_info():
    return await dynamic.get_dynamic_page_info(credential = common.get_credential())

async def after_all():
    print("删除所有动态")
    for i in dyid:
        d = dynamic.Dynamic(i, credential)
        await d.delete()
