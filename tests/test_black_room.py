# bilibili_api.black_room

from bilibili_api import black_room

room = black_room.BlackRoom(2656141)


async def test_a_get_list():
    return await black_room.get_blocked_list(type_=black_room.BlackType.VIDEO)


async def test_b_get_room_detail():
    return await room.get_details()


async def test_c_get_room_reason():
    return await room.get_reason()
