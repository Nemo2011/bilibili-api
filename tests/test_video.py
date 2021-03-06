from bilibili_api import video, exceptions
from .common import get_credential
import datetime

BVID = "BV1xx411c7Xg"
AID = 271
video = video.Video(BVID, credential=get_credential())


async def test_set_bvid():
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


async def test_set_aid():
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


async def test_get_info():
    info = await video.get_info()
    return info


async def test_get_stat():
    info = await video.get_stat()
    return info

async def test_get_tags():
    tags = await video.get_tags()
    return tags

async def test_get_chargers():
    chargers = await video.get_chargers()
    return chargers

async def test_get_pages():
    pages = await video.get_pages()
    return pages

async def test_get_download_url():
    pages = await video.get_download_url(0)
    return pages

async def test_get_related():
    data = await video.get_related()
    return data

async def test_has_liked():
    data = await video.has_liked()
    return data

async def test_get_pay_coins():
    data = await video.get_pay_coins()
    return data

async def test_has_favoured():
    data = await video.has_favoured()
    return data

async def test_get_media_list():
    data = await video.get_media_list()
    return data

async def test_get_danmaku_view():
    data = await video.get_danmaku_view(0)
    return data

async def test_get_danmaku():
    data = await video.get_danmaku(0)
    return data

async def test_get_danmaku_history():
    data = await video.get_danmaku(0, date=datetime.date(2020, 1, 1))
    return data

async def after_all():
    pass

async def before_all():
    pass

