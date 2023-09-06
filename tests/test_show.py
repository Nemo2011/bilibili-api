# bilibili_api.show

from bilibili_api import show

from .common import get_credential

PROJECT_ID = 75650


async def test_a_get_all_buyer_info():
    return await show.get_all_buyer_info(get_credential(), True)


async def test_b_get_available_sessions():
    return await show.get_available_sessions(PROJECT_ID)
