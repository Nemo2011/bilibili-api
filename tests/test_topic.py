from bilibili_api import topic
from .common import get_credential

t = topic.Topic(66571, get_credential())


async def test_a_Topic_get_info():
    return await t.get_info()


async def test_b_Topic_get_cards():
    return await t.get_cards(sort_by=topic.TopicCardsSortBy.NEW)


async def test_c_Topic_like():
    return await t.like(status=True)


async def test_d_Topic_set_favorite():
    return await t.set_favorite(status=True)


async def test_e_get_hot_topics():
    return await topic.get_hot_topics()


async def test_f_search_topic():
    return await topic.search_topic("bilibili-api")


async def after_all():
    await t.like(status=False)
    await t.set_favorite(status=False)
