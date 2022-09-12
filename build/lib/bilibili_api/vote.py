"""
bilibili_api.vote

投票相关操作。

需要 vote_id,获取 vote_id: 
"""

from .utils.utils import get_api
from .utils.network_httpx import request

API = get_api("common")


async def get_vote_info(vote_id: int):
    """
    获取投票详情

    Args:
        vote_id: vote_id,获取：nemo2011.github.io/bilibili-api/#/vote_id
    Returns:
        调用 API 返回的结果
    """
    api = API["vote"]["info"]["get_info"]
    params = {"vote_id": vote_id}
    return await request("GET", api["url"], params=params)
