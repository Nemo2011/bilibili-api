import asyncio
from bilibili_api import user
from . import common
import time
import random
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException


UID = 660303135

credential = common.get_credential()
u = user.User(UID, credential=credential)


async def test_a_get_user_info():
    return await u.get_user_info()


async def test_b_get_relation_info():
    return await u.get_relation_info()


async def test_c_get_up_info():
    return await u.get_up_stat()


async def test_d_get_live_info():
    return await u.get_live_info()


async def test_e_get_videos():
    return await u.get_videos()


async def test_f_get_audios():
    return await u.get_audios()


async def test_g_get_articles():
    return await u.get_articles()


async def test_h_article_list():
    return await u.get_article_list()


async def test_l_get_dynamics():
    return await u.get_dynamics()


async def test_j_subscribed_bangumis():
    return await u.get_subscribed_bangumis()


async def test_k_get_followers():
    return await u.get_followers()


async def test_l_get_followings():
    try:
        return await u.get_followers()
    except ResponseCodeException as e:
        if e.code != 22115:
            raise e

        return e.raw


async def test_m_get_overview_stat():
    return await u.get_overview_stat()


async def test_n_modify_relation():
    # 后面 test_r_set_subscribe_group 会用到
    result = await u.modify_relation(user.RelationType.SUBSCRIBE)
    await asyncio.sleep(0.5)
    return result


async def test_o_send_msg():
    return await u.send_msg("THIS IS A TEST MSG. " + str(time.time()))

subscribe_id = None


async def test_p_create_subscribe_group():
    name = f"TEST{random.randint(100000, 999999)}"
    result = await user.create_subscribe_group(name, credential)
    global subscribe_id
    subscribe_id = result["tagid"]
    return result


async def test_q_rename_subscribe_group():
    name = f"TEST{random.randint(100000, 999999)}"
    result = await user.rename_subscribe_group(subscribe_id, name, credential)
    return result


async def test_r_set_subscribe_group():
    result = await user.set_subscribe_group([UID], [subscribe_id], credential)
    return result


async def test_s_delete_subscribe_group():
    result = await user.delete_subscribe_group(subscribe_id, credential)
    return result

page_num = 1
per_page_item = 10


async def test_t_get_self_history():
    return await user.get_self_history(page_num, per_page_item, credential)

async def test_u_get_channel():
    return await u.get_channel()

async def test_v_get_channel_list():
    return await u.get_channel_list()

async def test_w_get_channel_video():
    return await u.get_channel_videos(202263)

async def after_all():
    await u.modify_relation(user.RelationType.UNSUBSCRIBE)
