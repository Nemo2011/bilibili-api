from bilibili_api import video_tag
from .common import get_credential

tag = video_tag.Tag(tag_name="真白花音", credential=get_credential())


async def test_a_get_tag_info():
    return await tag.get_tag_info()


async def test_b_get_similar_tags():
    return await tag.get_similar_tags()


async def test_c_get_cards():
    return await tag.get_cards()


async def test_d_subscribe_tag():
    return await tag.subscribe_tag()


async def test_e_unsubscribe_tag():
    return await tag.unsubscribe_tag()


async def test_f_get_history_cards():
    first_offset_dynamic_id = (await tag.get_cards())["cards"][0]["desc"]["dynamic_id"] # tag下第一个视频/动态的dynamic id
    return await tag.get_history_cards(offset_dynamic_id=first_offset_dynamic_id)
