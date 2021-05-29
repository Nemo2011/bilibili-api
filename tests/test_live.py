from bilibili_api.utils.Danmaku import Danmaku
from bilibili_api import live
from .common import get_credential
import random

l = live.LiveRoom(22544798, get_credential())

async def test_a_get_room_info():
    return await l.get_room_info()

async def test_b_get_room_play_info():
    return await l.get_room_play_info()

async def test_c_get_room_play_info_v2():
    return await l.get_room_play_info_v2()

async def test_d_get_room_play_url():
    return await l.get_room_play_url()

async def test_e_get_user_info_in_room():
    return await l.get_user_info_in_room()

async def test_f_get_dahanghai():
    return await l.get_dahanghai()

async def test_g_get_serven_rank():
    return await l.get_seven_rank()

async def test_h_get_fans_medal_rank():
    return await l.get_fans_medal_rank()

async def test_i_get_self_info():
    return await l.get_self_info()

async def test_j_get_chat_conf():
    return await l.get_chat_conf()

banid = None

async def test_k_ban_user():
    resp = await l.ban_user(1)
    global banid
    banid = resp['id']
    return resp

async def test_l_get_black_list():
    return await l.get_black_list()

async def test_m_unban_user():
    return await l.unban_user(banid)

async def test_n_send_danmaku():
    return await l.send_danmaku(Danmaku(f'test_{random.randint(10000, 99999)}'))

async def test_o_LiveDanmaku():
    async def on_msg(data):
        print(data)
        await room.disconnect()

    room = live.LiveDanmaku(22544798, True)
    room.add_event_listener('ALL', on_msg)
    await room.connect()
    
