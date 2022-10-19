# bilibili_api.emoji

from bilibili_api import emoji


async def test_a_get_emoji_list():
    return await emoji.get_emoji_list()
