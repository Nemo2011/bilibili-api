"""
bilibili_api.show

展出相关
"""
from dataclasses import dataclass, field
from typing import List, Union

from bilibili_api import Api, Credential
from bilibili_api.utils.utils import get_api

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
    price: float
    desc: str
    sale_start: str
    sale_end: str


@dataclass
class Session:
    """
    场次对象

    id (int): 场次id
    start_time (int): 场次开始时间戳
    formatted_time (int): 格式化start_time后的时间格式: YYYY-MM-DD dddd
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

    personal_id (str): 身份证ID
    name (str): 姓名
    tel (str): 电话号码
    is_fault (bool): 是否为默认
    org (str): 原始数据
    """

    personal_id: str
    name: str
    tel: str
    is_default: bool
    org: str


async def get_project_info(project_id: int) -> dict:
    """
    返回项目全部信息

    Args:
        project_id (int): 项目id

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["get"]
    params = {"id": project_id}
    return await Api(**api, ignore_code=True).update_params(**params).result


async def get_available_sessions(project_id: int):
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
        sess_obj = Session(id=int(v["id"]), start_time=int(v["start_time"]), formatted_time=str(v["name"]))
        for t in v["ticket_list"]:
            sess_obj.ticket_list.append(
                Ticket(
                    id=int(t["id"]),
                    price=int(t["price"]) / 100,
                    desc=t["desc"],
                    sale_start=t["sale_start"],
                    sale_end=t["sale_end"],
                )
            )
        rtn_list.append(sess_obj)
    return rtn_list


async def get_all_buyer_info(credential: Credential, rtn_buyer_info=False) -> Union[dict, List[BuyerInfo]]:
    """
    返回账号的全部身份信息

    Args:
        credential (Credential): 登录凭证
        rtn_buyer_info (bool): 是否以BuyerInfo对象返回

    Returns:
        dict or list[BuyerInfo]: 调用 API 返回的结果 或者 BuyerInfo对象列表
    """
    credential.raise_for_no_sessdata()
    api = API["info"]["buyer_info"]
    result = await Api(**api, credential=credential, ignore_code=True).result
    if rtn_buyer_info:
        rtn_list: List[BuyerInfo] = []
        for v in result["list"]:
            rtn_list.append(
                BuyerInfo(personal_id=v["personal_id"], name=v["name"], tel=v["tel"], is_default=v["is_default"], org=v)
            )
        return rtn_list
    return result
