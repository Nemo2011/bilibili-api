# bilibili_api.vote

from bilibili_api import vote


async def test_a_get_vote_info():
    return await vote.Vote(vote_id=5322590).get_vote_info()
