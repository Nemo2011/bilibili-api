# bilibili_api.client

from bilibili_api import client


async def test_a_get_zone():
    return await client.get_zone()
