# bilibili_api.live_area

from bilibili_api import live_area

async def test_a_get_list_by_area_id():
    return await live_area.get_list_by_area(
        area_id=live_area.get_area_info_by_name("虚拟主播")[0]["id"],
        page=1,
        order=live_area.LiveRoomOrder.NEW
    )
