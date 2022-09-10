# bilibili_api.user

import asyncio
from bilibili_api import user
from . import common
import time
import random
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException


UID = 660303135

credential = common.get_credential()
u = user.User(UID, credential=credential)


async def test_a_User_get_user_info():
    return await u.get_user_info()


async def test_b_User_get_relation_info():
    return await u.get_relation_info()


async def test_c_User_get_up_info():
    return await u.get_up_stat()


async def test_d_User_get_live_info():
    return await u.get_live_info()


async def test_e_User_get_videos():
    return await u.get_videos()


async def test_f_User_get_audios():
    return await u.get_audios()


async def test_g_User_get_articles():
    return await u.get_articles()


async def test_h_User_article_list():
    return await u.get_article_list()


async def test_l_User_get_dynamics():
    return await u.get_dynamics()


async def test_j_User_subscribed_bangumis():
    return await u.get_subscribed_bangumi()


async def test_k_User_get_followers():
    return await u.get_followers()


async def test_l_User_get_followings():
    try:
        return await u.get_followers()
    except ResponseCodeException as e:
        if e.code != 22115:
            raise e

        return e.raw


async def test_m_User_get_all_followers():
    return await u.get_all_followings()


async def test_n_User_get_cheese():
    return await u.get_cheese()


async def test_o_User_get_channel_series():
    return await u.get_channels()


async def test_p_User_get_channel_video_series():
    return await u.get_channel_videos_series(589023)


async def test_q_User_get_channel_video_season():
    return await u.get_channel_videos_season(193515)


async def test_r_User_get_top_followers():
    return await u.top_followers()


async def test_s_User_get_overview_stat():
    return await u.get_overview_stat()


async def test_t_User_modify_relation():
    # 后面 test_r_set_subscribe_group 会用到
    result = await u.modify_relation(user.RelationType.SUBSCRIBE)
    await asyncio.sleep(0.5)
    return result


subscribe_id = None


async def test_u_create_subscribe_group():
    name = f"TEST{random.randint(100000, 999999)}"
    result = await user.create_subscribe_group(name, credential)
    global subscribe_id
    subscribe_id = result["tagid"]
    return result


async def test_v_rename_subscribe_group():
    name = f"TEST{random.randint(100000, 999999)}"
    result = await user.rename_subscribe_group(subscribe_id, name, credential)
    return result


async def test_w_set_subscribe_group():
    result = await user.set_subscribe_group([UID], [subscribe_id], credential)
    return result


async def test_x_delete_subscribe_group():
    result = await user.delete_subscribe_group(subscribe_id, credential)
    return result


page_num = 1
per_page_item = 10


async def test_y_get_self_info():
    return await user.get_self_info(common.get_credential())


async def test_z_get_self_history():
    return await user.get_self_history(page_num, per_page_item, credential)


async def test_za_get_self_events():
    return await user.get_self_events(0, common.get_credential())


async def test_zb_get_self_coins():
    return await user.get_self_coins(common.get_credential())


async def after_all():
    await u.modify_relation(user.RelationType.UNSUBSCRIBE)
