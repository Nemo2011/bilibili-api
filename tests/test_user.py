import asyncio
from bilibili_api import user
from . import common
import time


UID = 660303135

credential = common.get_credential()
u = user.User(UID, credential=credential)


async def test_get_user_info():
    return await u.get_user_info()


async def test_get_relation_info():
    return await u.get_relation_info()


async def test_get_up_info():
    return await u.get_up_stat()


async def test_get_live_info():
    return await u.get_live_info()


async def test_get_videos():
    return await u.get_videos()


async def test_get_audios():
    return await u.get_audios()


async def test_get_articles():
    return await u.get_articles()


async def test_article_list():
    return await u.get_article_list()


async def test_get_dynamics():
    return await u.get_dynamics()


async def test_subscribed_bangumis():
    return await u.get_subscribed_bangumis()


async def test_get_followings():
    return await u.get_followings()


async def test_get_followings():
    return await u.get_followers()


async def test_get_overview_stat():
    return await u.get_overview_stat()


async def test_modify_relation():
    result = await u.modify_relation(user.RelationType.SUBSCRIBE)
    await asyncio.sleep(0.5)
    await u.modify_relation(user.RelationType.UNSUBSCRIBE)
    return result


async def test_send_msg():
    return await u.send_msg("THIS IS A TEST MSG. " + str(time.time()))

