# bilibili_api.vote

from bilibili_api import vote


async def test_get_vote_info():
    return await vote.get_vote_info(2773489)
