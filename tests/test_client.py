# bilibili_api.client

from bilibili_api import client

async def test_a_get_zone():
    return await client.get_zone()


async def test_b_get_client_info():
    return await client.get_client_info()
