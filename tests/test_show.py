# bilibili_api.show

from bilibili_api import show

from .common import get_credential

PROJECT_ID = 75650


async def test_a_get_all_buyer_info():
    return await show.get_all_buyer_info(get_credential())


async def test_b_get_available_sessions():
    return await show.get_available_sessions(PROJECT_ID)


async def test_c_order_ticket():
    buyers = (await test_a_get_all_buyer_info())
    session = (await test_b_get_available_sessions())[0]
    ticket = session.ticket_list[0]
    ot = show.OrderTicket(get_credential(), buyers, buyers[0], PROJECT_ID, session, ticket)
    return await ot.create_order()
