# bilibili_api.video

import time
import asyncio
from sqlite3 import DatabaseError

from bilibili_api import exceptions
from bilibili_api import video as video_m
from bilibili_api.utils.danmaku import Danmaku
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException

# 调试兼容
try:
    from .common import get_credential

    crd = get_credential()
except:
    print("未认证")
    crd = None

import datetime

BVID = "BV1N34y1Y7ds"
AID = 811248323
video = video_m.Video(aid=AID, credential=crd)


async def test_a_Video_set_bvid():
    # 设置正确 bvid
    video.set_bvid(BVID)
    assert video.get_bvid() == BVID, "bvid 应该被修改"
    assert video.get_aid() == AID, "aid 应该从 bvid 转换"

    # 设置错误 bvid
    try:
        video.set_bvid("BVajsdoiajinsodn")
        assert False, "设置了错误 bvid 但未报错"
    except exceptions.ArgsException:
        video.set_bvid(BVID)


async def test_b_Video_set_aid():
    # 设置正确 aid
    video.set_aid(AID)
    assert video.get_aid() == AID, "aid 应该被修改"
    assert video.get_bvid() == BVID, "bvid 应该从 aid 转换"

    # 设置错误 aid
    # 设置错误 bvid
    try:
        video.set_aid(-1)
        assert False, "设置了错误 aid 但未报错"
    except exceptions.ArgsException:
        video.set_aid(AID)
        pass


async def test_c_Video_get_info():
    info = await video.get_info()
    return info


# async def test_d_Video_get_stat():
#     info = await video.get_stat()
#     return info


async def test_e_Video_get_tags():
    tags = await video.get_tags()
    return tags


async def test_f_Video_get_download_url():
    try:
        return await video.get_download_url(0)
    except ResponseCodeException as e:
        if e.code == -404:
            return e.raw
        else:
            raise e


async def test_g_Video_get_chargers():
    chargers = await video.get_chargers()
    return chargers


async def test_h_Video_get_pages():
    pages = await video.get_pages()
    return pages


async def test_i_Video_get_related():
    data = await video.get_related()
    return data


async def test_j_Video_has_liked():
    data = await video.has_liked()
    return data


async def test_k_Video_get_pay_coins():
    data = await video.get_pay_coins()
    return data


async def test_l_Video_has_favoured():
    data = await video.has_favoured()
    return data


async def test_n_Video_get_danmaku_view():
    data = await video.get_danmaku_view(0)
    return data


async def test_o_Video_get_danmaku():
    data = await video.get_danmakus(0)
    return data


async def test_p_Video_get_danmaku_history():
    data = await video.get_danmakus(0, date=datetime.date(2020, 1, 1))
    return data


async def test_q_Video_get_danmaku_xml():
    return await video.get_danmaku_xml(0)


async def test_r_Video_get_danmaku_snapshot():
    return await video.get_danmaku_snapshot()


async def test_s_Video_get_pbp():
    return await video.get_pbp(0)


async def test_t_Video_get_history_danmaku_index():
    return await video.get_history_danmaku_index(0, datetime.date(2022, 9, 1))


async def test_u_Video_send_danmaku():
    dm = Danmaku("TESTING" + str(int(time.time())))
    data = await video.send_danmaku(0, dm)
    return data


async def test_v_Video_like():
    try:
        data = await video.like(True)

        # Clean up
        await video.like(False)
        return data
    except ResponseCodeException as e:
        # 忽略已点赞和未点赞
        if e.code not in (65004, 65006):
            raise e
        else:
            return e.raw


async def test_w_Video_pay_coin():
    try:
        data = await video.pay_coin(2)
        return data
    except ResponseCodeException as e:
        # 不接受以下错误 code
        # -104 硬币不足
        # 34005 视频投币上限
        if e.code not in (-104, 34005):
            raise e
        else:
            return e.raw


# async def test_x_Video_add_tag():
#    try:
#        data = await video.add_tag("测试标签")
#        return data
#    except ResponseCodeException as e:
#        # 16070  只有 UP 才能添加
#        if e.code != 16070:
#            raise e
#        else:
#            return e.raw


async def test_y_Video_del_tag():
    try:
        data = await video.delete_tag(99999999)
        return data
    except ResponseCodeException as e:
        # 16070  只有 UP 才能添加
        if e.code != 16070:
            raise e
        else:
            return e.raw


# async def test_z_Video_subscribe_and_unsubscribe_tag():
#     data = await video.subscribe_tag(8583026)
#     await video.unsubscribe_tag(8583026)
#     return data


async def test_za_Video_set_favorite():
    data = await video.set_favorite([1626035955])
    await asyncio.sleep(0.5)
    await video.set_favorite(del_media_ids=[1626035955])
    return data


async def test_zb_Video_add_to_toview():
    return await video.add_to_toview()


async def test_zc_Video_delete_from_toview():
    return await video.delete_from_toview()


async def test_zd_video_snapshot():
    return await video.get_video_snapshot(pvideo=False)


async def test_zf_get_subtitle():
    videos = video_m.Video(aid=288571926)
    return await videos.get_subtitle(cid=281031471)


# from bilibili_api import sync
#
# res = sync(test_zf_get_subtitle())
# print(res)


async def test_zg_triple():
    return await video.triple()


async def test_zh_get_cid_info():
    return await video_m.get_cid_info(62131)
