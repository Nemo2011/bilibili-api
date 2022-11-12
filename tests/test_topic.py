from bilibili_api import topic

t = topic.Topic(66571)

async def test_a_Topic_get_info():
    return await t.get_info()

async def test_b_Topic_get_cards():
    return await t.get_cards()
