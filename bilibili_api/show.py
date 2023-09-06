from bilibili_api import Api
from bilibili_api.utils.utils import get_api

API = get_api("show")


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
