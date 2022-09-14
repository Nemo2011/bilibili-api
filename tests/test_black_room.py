# bilibili_api.black_room

from bilibili_api import black_room

room = black_room.BlackRoom(2600321)

async def test_a_get_list():
    return await black_room.get_blocked_list()

async def test_b_get_room_detail():
    return await room.get_details()
