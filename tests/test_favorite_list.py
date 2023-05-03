# bilibili_api.favorite_list

import random

from bilibili_api import favorite_list, video, bvid2aid
from . import common

media_id = None
aids = [bvid2aid("BV1yQ4y117m3"), 975842744]
uid = 1666311555
default_media_id = 1626035955

credential = common.get_credential()


async def test_a_get_video_favorite_list():
    data = await favorite_list.get_video_favorite_list(uid, credential=credential)
    return data


async def test_b_get_video_favorite_list_content():
    data = await favorite_list.get_video_favorite_list_content(
        1195349595, credential=credential
    )
    return data


async def test_c_get_topic_favorite_list():
    data = await favorite_list.get_topic_favorite_list(credential=credential)
    return data


async def test_d_get_article_favorite_list():
    data = await favorite_list.get_article_favorite_list(credential=credential)
    return data


async def test_e_get_album_favorite_list():
    data = await favorite_list.get_album_favorite_list(credential=credential)
    return data


async def test_f_get_course_favorite_list():
    data = await favorite_list.get_course_favorite_list(credential=credential)
    return data


async def test_g_get_note_favorite_list():
    data = await favorite_list.get_note_favorite_list(credential=credential)
    return data


async def test_h_create_video_favorite_list():
    # 创建临时收藏夹
    rnd_name = random.randint(100000, 999999)
    data = await favorite_list.create_video_favorite_list(
        f"TESTING_{rnd_name}", "", False, credential=credential
    )
    global media_id
    media_id = data["id"]

    # 收藏两个视频供测试
    for aid in aids:
        v = video.Video(aid=aid, credential=credential)
        await v.set_favorite([media_id])
    return data


async def test_i_modify_video_favorite_list():
    rnd_name = random.randint(100000, 999999)
    data = await favorite_list.modify_video_favorite_list(
        media_id, f"TESTING_{rnd_name}", credential=credential
    )
    return data


async def test_j_copy_video_favorite_list_content():
    data = await favorite_list.copy_video_favorite_list_content(
        media_id, default_media_id, [aids[0]], credential=credential
    )
    return data


async def test_k_move_video_favorite_list_content():
    data = await favorite_list.move_video_favorite_list_content(
        media_id, default_media_id, [aids[1]], credential=credential
    )
    return data


async def test_l_clean_video_favorite_list_content():
    data = await favorite_list.clean_video_favorite_list_content(media_id, credential)
    return data


async def test_m_delete_video_favorite_list_content():
    data = await favorite_list.delete_video_favorite_list_content(
        default_media_id, [aids[0]], credential=credential
    )
    return data


async def test_n_delete_video_favorite_list():
    data = await favorite_list.delete_video_favorite_list([media_id], credential)
    return data


async def test_get_favorite_collected():
    data = await favorite_list.get_favorite_collected(uid, 1, credential)
    return data


async def after_all():
    # 清理默认收藏夹中的视频
    v = video.Video(aid=aids[0], credential=credential)
    await v.set_favorite(del_media_ids=[default_media_id])
