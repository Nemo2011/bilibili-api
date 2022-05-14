from datetime import datetime
from time import time
from bilibili_api import dynamic, user
from . import common

credential = common.get_credential()

dyid = []

draft_ids = []

async def test_a_send_dynamic():
    # 测试发送动态
    print('测试立即发送纯文本动态')
    resp = await dynamic.send_dynamic(text="测试立即发送纯文本动态 @1882430995 ", credential=credential)
    print(resp)
    dyid.append(resp["dynamic_id"])

    print('测试立即发送图片动态')
    resp = await dynamic.send_dynamic(text="测试立即发送图片动态", image_streams=[open('./design/logo.png', 'rb')], credential=credential)
    dyid.append(resp["dynamic_id"])
    print(resp)

    print('测试定时发布纯文本动态')
    date = datetime.fromtimestamp(time() + 86400)
    resp = await dynamic.send_dynamic(text="测试定时发布纯文本动态", send_time=date, credential=credential)
    print(resp)
    draft_ids.append(resp['draft_id'])

    print('测试定时发布图片动态')
    resp = await dynamic.send_dynamic(text="测试定时发送图片动态", send_time=date, image_streams=[open('./design/logo.png', 'rb')], credential=credential)
    print(resp)
    draft_ids.append(resp['draft_id'])


async def test_b_get_schedules_list():
    return await dynamic.get_schedules_list(credential=credential)

async def test_c_send_schedule_now():
    draft_id = draft_ids.pop()

    resp = await dynamic.send_schedule_now(draft_id, credential)
    dyid.append(resp["dynamic_id"])

    return resp;

async def test_d_delete_schedule():
    draft_id = draft_ids.pop()

    resp = await dynamic.delete_schedule(draft_id, credential)
    return resp

dy = None

async def test_e_Dynamic_get_info():
    global dy
    dy = dynamic.Dynamic(dyid.pop(), credential)

    return await dy.get_info()

async def test_f_Dynamic_get_reposts():
    return await dy.get_reposts()

async def test_g_Dynamic_set_like():
    return await dy.set_like()

async def test_h_Dynamic_repost():
    resp = await dy.repost()

    print(resp)
    return resp

async def test_i_Dynamic_delete():
    return await dy.delete()

async def after_all():
    print('删除所有未发定时动态')
    for i in draft_ids:
        await dynamic.delete_schedule(i, credential)

    print('删除所有动态')
    for i in dyid:
        d = dynamic.Dynamic(i, credential)
        await d.delete()

    print('删除转发动态')
    u = user.User(1882430995, credential=credential)
    dy = await u.get_dynamics()
    dyid1 = dy['cards'][0]['desc']['dynamic_id']
    d = dynamic.Dynamic(dyid1, credential)
    await d.delete()
