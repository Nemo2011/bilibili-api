"""
bilibili_api.show

展出相关
"""
import json
import random
import time
from dataclasses import dataclass, field
from typing import List

from .utils.credential import Credential
from .utils.network import Api
from .utils.utils import get_api, get_deviceid

API = get_api("show")


@dataclass
class Ticket:
    """
    票对象

    id (int): 场次id

    price (float): 价格(RMB)

    desc (str): 描述

    sale_start (str): 开售开始时间

    sale_end (str): 开售结束时间
    """
    id: int
    price: int
    desc: str
    sale_start: str
    sale_end: str


@dataclass
class Session:
    """
    场次对象

    id (int): 场次id

    start_time (int): 场次开始时间戳

    formatted_time (str): 格式化start_time后的时间格式: YYYY-MM-DD dddd

    ticket_list (list[Ticket]): 存放Ticket对象的list
    """
    id: int
    start_time: int
    formatted_time: str
    ticket_list: List[Ticket] = field(default_factory=list)


@dataclass
class BuyerInfo:
    """
    购买人信息

    id (int): 信息序号

    uid (int): 用户 ID

    account_channel (str): 默认为空

    personal_id (str): 身份证号

    name (str): 姓名

    id_card_front (str): 未知

    id_card_back (str): 未知

    is_default (bool): 是否为默认信息

    tel (str): 电话号码

    error_code (str): 错误代码

    id_type (int): 默认 0

    verify_status (int): 认证状态

    accountId (int): 用户 ID

    isBuyerInfoVerified (bool): 默认为 True

    isBuyerValid (bool): 默认为 True
    """
    id: int
    uid: int
    account_channel: str
    personal_id: str
    name: str
    id_card_front: str
    id_card_back: str
    is_default: int
    tel: str
    error_code: str
    id_type: int
    verify_status: int
    accountId: int
    isBuyerInfoVerified: bool = True
    isBuyerValid: bool = True


async def get_project_info(project_id: int) -> dict:
    """
    返回项目全部信息

    Args:
        project_id (int): 项目id

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["get"]
    return await Api(**api).update_params(id=project_id).result


async def get_available_sessions(project_id: int) -> List[Session]:
    """
    返回该项目的所有可用场次

    Args:
        project_id (int): 项目id

    Returns:
        list[Session]: 存放场次对象的list
    """
    rtn_list = []
    project_info = await get_project_info(project_id)
    for v in project_info["screen_list"]:
        sess_obj = Session(id=v["id"], start_time=v["start_time"], formatted_time=v["name"])
        for t in v["ticket_list"]:
            sess_obj.ticket_list.append(
                Ticket(
                    id=t["id"],
                    price=t["price"],
                    desc=t["desc"],
                    sale_start=t["sale_start"],
                    sale_end=t["sale_end"],
                )
            )
        rtn_list.append(sess_obj)
    return rtn_list


async def get_ticket_buyer_list(credential: Credential) -> dict:
    """
    返回账号的全部身份信息

    Args:
        credential (Credential): 登录凭证

    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()
    api = API["info"]["buyer_info"]
    return await Api(**api, credential=credential).result


async def get_all_buyer_info(credential: Credential) -> List[BuyerInfo]:
    """
    返回账号的全部身份信息

    Args:
        credential (Credential): 登录凭证

    Returns:
        list[BuyerInfo]: BuyerInfo对象列表
    """
    res = await get_ticket_buyer_list(credential)
    return [BuyerInfo(**v) for v in res["list"]]


class OrderTicket:
    """
    购票类

    Args:
        credential (Credential): Credential 对象

        buyer_info (BuyerInfo): BuyerInfo 对象

        project_id (int): 展出id

        session (Session): Session 对象

        ticket (Ticket): Ticket 对象
    """

    def __init__(
        self,
        credential: Credential,
        buyer_list: List[BuyerInfo],
        target_buyer: BuyerInfo,
        project_id: int,
        session: Session,
        ticket: Ticket
    ):
        self.credential = credential
        self.buyer_list = buyer_list
        self.target_buyer = target_buyer
        self.project_id = project_id
        self.session = session
        self.ticket = ticket

    async def get_token(self):
        """
        获取购票Token

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()
        api = API["info"]["token"]
        payload = {
            "count": "1",
            "order_type": 1,
            "project_id": self.project_id,
            "screen_id": self.session.id,
            "sku_id": self.ticket.id
        }
        return await Api(**api, credential=self.credential).update_data(**payload).result

    async def create_order(self):
        def _generate_clickPosition():
            # 生成随机的 x 和 y 坐标，以下范围大概是1920x1080屏幕下可能的坐标
            x = random.randint(1320, 1330)
            y = random.randint(880, 890)
            # 生成随机的起始时间和结束时间（或当前时间）
            origin_timestamp = int(time.time() * 1000)
            now_timestamp = origin_timestamp + random.randint(5000, 10000)  # 添加一些随机时间差 (5s ~ 10s)
            click_position = {
                "x": x,
                "y": y,
                "origin": origin_timestamp,
                "now": now_timestamp
            }
            return json.dumps(click_position)

        """
        创建购买订单

        Returns:
            dict: 调用 API 返回的结果
        """
        res = await self.get_token()
        payload = {
            "buyer_info": json.dumps([b.__dict__ for b in self.buyer_list]),
            "count": 1,
            "order_type": 1,
            "pay_money": self.ticket.price,
            "project_id": self.project_id,
            "screen_id": self.session.id,
            "sku_id": self.ticket.id,
            "timestamp": int(time.time() * 1000),
            "token": res["token"],
            "deviceId": get_deviceid('', True),
            "clickPosition": _generate_clickPosition(),
            "tel": self.target_buyer.tel,
            "buyer": self.target_buyer.name
        }
        api = API["operate"]["order"]
        return await Api(**api, credential=self.credential).update_params(project_id=self.project_id).update_data(
            **payload).result
