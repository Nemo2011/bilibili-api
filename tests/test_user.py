# bilibili_api.user

import asyncio
from bilibili_api import user, bvid2aid

try:
    from . import common

    credential = common.get_credential()
except:
    credential = None
    print("导入凭据未成功")
import time
import random
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException

UID = 660303135
UID2 = 1033942996
UID3 = 7949629
UID_Model_Test = 12344667

u = user.User(UID_Model_Test, credential=credential)


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


# async def test_j_User_subscribed_bangumis():
#    return await u.get_subscribed_bangumi()


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


async def test_zc_get_toview_list():
    return await user.get_toview_list(common.get_credential())


async def test_zd_delete_viewed_video_in_toview_list():
    return await user.delete_viewed_videos_from_toview(common.get_credential())


async def test_ze_clean_toview_list():
    return await user.clear_toview_list(common.get_credential())


async def test_zf_get_space_notice():
    return await u.get_space_notice()


async def test_zg_get_album():
    return await u.get_album()


async def test_zh_get_user_fav_tag():
    return await u.get_user_fav_tag()


async def test_zi_get_user_medal():
    return await u.get_user_medal()


# async def test_zj_get_user_top_videos():
#     return await u.get_top_videos()


async def test_zk_get_reservation():
    return await u.get_reservation()


async def test_zl_name2uid():
    return await user.name2uid("田所こうじ")


# series_id = None
#
# async def test_zm_create_channel_series():
#     global series_id
#     data = await user.create_channel_series(name="什么都没有", credential=credential)
#     series_id = data["series_id"]
#     return data
#
#
# async def test_zo_add_video_to_channal_series():
#     global series_id
#     return await user.add_aids_to_series(series_id=series_id, aids=[bvid2aid("BV1fG4y1g7wE")], credential=credential)
#
#
# async def test_zp_del_video_from_channel_series():
#     global series_id
#     return await user.del_aids_from_series(series_id=series_id, aids=[bvid2aid("BV1fG4y1g7wE")], credential=credential)
#
#
# async def test_zq_del_channel_series():
#     global series_id
#     return await user.del_channel_series(series_id=series_id, credential=credential)
#
#
async def test_zr_get_self_same_followings():
    return await u.get_self_same_followers()


async def test_zs_get_self_black_list():
    return await user.get_self_black_list(credential)


async def test_zt_get_self_friends():
    return await user.get_self_friends(credential)


async def test_zu_get_self_whisper_followings():
    return await user.get_self_whisper_followings(credential)


async def test_zv_get_self_special_followings():
    return await user.get_self_special_followings(credential)


async def after_all():
    await u.modify_relation(user.RelationType.UNSUBSCRIBE)
