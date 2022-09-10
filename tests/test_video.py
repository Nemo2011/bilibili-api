# bilibili_api.video

import asyncio
from sqlite3 import DatabaseError
import time
from bilibili_api.utils.Danmaku import Danmaku
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException
from bilibili_api import video as video_m, exceptions
from .common import get_credential
import datetime

BVID = "BV1N34y1Y7ds"
AID = 811248323
video = video_m.Video(BVID, credential=get_credential())


async def test_Video_set_bvid():
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


async def test_Video_set_aid():
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


async def test_Video_get_info():
    info = await video.get_info()
    return info


async def test_Video_get_stat():
    info = await video.get_stat()
    return info


async def test_Video_get_tags():
    tags = await video.get_tags()
    return tags


async def test_Video_get_chargers():
    chargers = await video.get_chargers()
    return chargers


async def test_Video_get_pages():
    pages = await video.get_pages()
    return pages


async def test_Video_get_download_url():
    pages = await video.get_download_url(0)
    return pages


async def test_Video_get_related():
    data = await video.get_related()
    return data


async def test_Video_has_liked():
    data = await video.has_liked()
    return data


async def test_Video_get_pay_coins():
    data = await video.get_pay_coins()
    return data


async def test_Video_has_favoured():
    data = await video.has_favoured()
    return data


async def test_Video_get_media_list():
    data = await video.get_media_list()
    return data


async def test_Video_get_danmaku_view():
    data = await video.get_danmaku_view(0)
    return data


async def test_Video_get_danmaku():
    data = await video.get_danmakus(0)
    return data


async def test_Video_get_danmaku_history():
    data = await video.get_danmakus(0, date=datetime.date(2020, 1, 1))
    return data


async def test_Video_get_danmaku_xml():
    return await video.get_danmaku_xml(0)


async def test_Video_get_danmaku_snapshot():
    return await video.get_danmaku_snapshot()


async def test_Video_get_pbp():
    return await video.get_pbp(0)


async def test_Video_get_history_danmaku_index():
    return await video.get_history_danmaku_index(0, datetime.date(2022, 9, 1))


async def test_Video_send_danmaku():
    dm = Danmaku("TESTING" + str(int(time.time())))
    data = await video.send_danmaku(0, dm)
    return data


async def test_Video_like():
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


async def test_Video_pay_coin():
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


async def test_Video_add_tag():
    try:
        data = await video.add_tag("测试标签")
        return data
    except ResponseCodeException as e:
        # 16070  只有 UP 才能添加
        if e.code != 16070:
            raise e
        else:
            return e.raw


async def test_Video_del_tag():
    try:
        data = await video.delete_tag(99999999)
        return data
    except ResponseCodeException as e:
        # 16070  只有 UP 才能添加
        if e.code != 16070:
            raise e
        else:
            return e.raw


async def test_Video_subscribe_and_unsubscribe_tag():
    data = await video.subscribe_tag(8583026)
    await video.unsubscribe_tag(8583026)
    return data


async def test_Video_set_favorite():
    data = await video.set_favorite([1626035955])
    await asyncio.sleep(0.5)
    await video.set_favorite(del_media_ids=[1626035955])
    return data
