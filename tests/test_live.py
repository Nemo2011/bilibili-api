# bilibili_api.live

import time
import random

from bilibili_api import live
from bilibili_api.utils.danmaku import Danmaku
from bilibili_api.exceptions import ResponseCodeException

from .common import get_credential

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
    return await live.get_self_info(get_credential())


async def test_j_get_danmu_info():
    return await l.get_danmu_info()


async def test_k_ban_user():
    try:
        return await l.ban_user(1)
    except ResponseCodeException as e:
        if e.code == 1200000:
            return e.raw
        else:
            raise e


black_list = None


async def test_l_get_black_list():
    try:
        global black_list
        black_list = await l.get_black_list()
        return black_list
    except ResponseCodeException as e:
        if e.code == 10002:
            return e.raw
        else:
            raise e


async def test_m_unban_user():
    if black_list == None:
        return
    for item in black_list["data"]:
        if item["tuid"] == 1:
            return await l.unban_user(item["id"])


async def test_n_send_danmaku():
    return await l.send_danmaku(Danmaku(f"test_{random.randint(10000, 99999)}"))


async def test_o_LiveDanmaku():
    async def on_msg(data):
        print(data)
        await room.disconnect()

    room = live.LiveDanmaku(22544798, True, credential=get_credential())
    room.add_event_listener("ALL", on_msg)
    await room.connect()


async def test_p_sign_up_dahanghai():
    return await l.sign_up_dahanghai()


async def test_q_send_gift_from_bag():
    try:
        return await l.send_gift_from_bag(5702480, 255051127, 30607, 1)
    except ResponseCodeException as e:
        if e.code != 200161:
            raise e
        return e.raw


async def test_r_receive_reward():
    return await l.receive_reward(2)


async def test_s_get_general_info():
    return await l.get_general_info()


async def test_t_get_self_live_info():
    return await live.get_self_live_info(get_credential())


async def test_u_get_self_guards():
    return await live.get_self_dahanghai_info(credential=get_credential())


async def test_v_get_self_bag():
    return await live.get_self_bag(get_credential())


async def test_w_get_gift_config():
    return await live.get_gift_config()


async def test_x_get_gift_common():
    return await l.get_gift_common()


async def test_y_get_gift_sepcial():
    return await l.get_gift_special(tab_id=2)


async def test_z_send_gift_gold():
    try:
        return await l.send_gift_gold(5702480, 31060, 1, 100)
    except ResponseCodeException as e:
        print(e.code)
        if e.code == 200013 or e.code == 200036:
            return e.raw
        raise e


async def test_za_send_gift_silver():
    try:
        return await l.send_gift_silver(5702480, 1, 1, 100)
    except ResponseCodeException as e:
        if e.code == 200013 or e.code == 200036:
            return e.raw
        raise e


async def test_zb_get_area_info():
    return await live.get_area_info()


async def test_zc_get_gaonengbang():
    return await l.get_gaonengbang()


async def test_zc_get_live_followers_info():
    return await live.get_live_followers_info(credential=get_credential())


async def test_zd_get_unlive_followers_info():
    return await live.get_unlive_followers_info(page=1, credential=get_credential())


async def test_ze_get_following_live():
    return await live.create_live_reserve(
        credential=get_credential(),
        title="测试",
        start_time=round(time.time()) + (60 * 60 * 4),
    )


async def test_zf_get_get_popular_ticket_num():
    return await l.get_popular_ticket_num()


async def test_zg_popular_rank_free_score_incr():
    return await l.send_popular_ticket()

