# bilibili_api.show
import json

from bilibili_api import Credential
from show import BuyerInfo, Session, Ticket, OrderTicket, get_available_sessions, get_all_buyer_info


async def test_get_user_info(project_id, sessdata):
    cre = Credential(sessdata=sessdata)
    buyer: BuyerInfo = (await get_all_buyer_info(cre, True))[0]
    session: Session = (await get_available_sessions(project_id))[0]
    ticket: Ticket = session.ticket_list[0]
    ot = OrderTicket(credential=cre, buyer_info=buyer, project_id=project_id, session=session, ticket=ticket)
    print(json.dumps((await ot.get_token())))


async def test_create_order(project_id, sessdata):
    cre = Credential(sessdata=sessdata)
    buyer: BuyerInfo = (await get_all_buyer_info(cre, True))[0]
    session: Session = (await get_available_sessions(project_id))[0]
    ticket: Ticket = session.ticket_list[0]
    ot = OrderTicket(credential=cre, buyer_info=buyer, project_id=project_id, session=session, ticket=ticket)
    res = await ot.create_order()
    print(res)
