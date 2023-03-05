# bilibili_api.black_room

from bilibili_api import black_room
from . import common

room = black_room.BlackRoom(2656141)

case_id = "AC2Pfk6Phllf"

credential = common.get_credential()

async def test_a_get_list():
    return await black_room.get_blocked_list(type_=black_room.BlackType.VIDEO)


async def test_b_get_room_detail():
    return await room.get_details()


async def test_c_get_room_reason():
    return await room.get_reason()


# async def test_d_get_jury_case():
#     return await black_room.JuryCase(case_id, credential=credential).get_details()

# 不便加入 action 测试，账户需要为风纪委员...