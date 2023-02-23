# bilibili_api.vote

from bilibili_api import vote

try:
    from . import common

    credential = common.get_credential()
except:
    credential = None
    print("导入凭据未成功")

vote_id = 5322590

async def test_a_get_vote_info():
    return await vote.Vote(vote_id=5322590).get_info()

async def test_b_create_vote():
    cr_vote = await vote.create_vote(
        title="测试投票",
        _type=vote.VoteType.TEXT,
        choice_cnt=2,
        duration=259200,
        choices=vote.VoteChoices().add_choice("选项1").add_choice("选项2"),
        credential=credential, # type: ignore 
        desc="测试投票"
    )
    global vote_id
    vote_id = cr_vote.vote_id
    return cr_vote

async def test_c_update_vote():
    return await vote.Vote(vote_id=vote_id).update_vote(
        title="测试投票2",
        _type=vote.VoteType.TEXT,
        choice_cnt=2,
        duration=259200,
        choices=vote.VoteChoices().add_choice("选项1C").add_choice("选项2c"),
        desc="测试投票2"
    )