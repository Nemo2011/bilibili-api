"""
番剧相关

概念：
+ media_id: 番剧本身的 ID，有时候也是每季度的 ID，如 https://www.bilibili.com/bangumi/media/md28231846/
+ season_id: 每季度的 ID，只能通过 get_meta() 获取。
+ episode_id: 每集的 ID，如 https://www.bilibili.com/bangumi/play/ep374717

"""

from enum import Enum
from .utils.utils import get_api
from .utils.Credential import Credential
from .utils.network import get_session, request
from .exceptions.ResponseException import ResponseException
from .exceptions.ApiException import ApiException

import json
import re

API = get_api('bangumi')

class BangumiCommentOrder(Enum):
    """
    短评 / 长评 排序方式

    + DEFAULT: 默认
    + CTIME: 发布时间倒序
    """
    DEFAULT = 0
    CTIME = 1


async def get_meta(media_id: int, credential: Credential = None):
    """
    获取番剧元数据信息（评分，封面 URL，标题等）

    Args:
        media_id (int): media_id
        credential (Credential, optional): 凭据. Defaults to None.
    """
    credential = credential if credential is not None else Credential()

    api = API["info"]["meta"]
    params = {
        "media_id": media_id
    }
    return await request('GET', api['url'], params, credential=credential)



async def get_short_comment_list(media_id: int, order: BangumiCommentOrder = BangumiCommentOrder.DEFAULT,
                           next: str = None, credential: Credential = None):
    """
    获取短评列表

    Args:
        media_id   (int)                          : media_id
        order      (BangumiCommentOrder, optional): 排序方式。Defaults to BangumiCommentOrder.DEFAULT
        next       (str, optional)                : 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None
        credential (Credential, optional)         : 凭据. Defaults to None
    """
    credential = credential if credential is not None else Credential()

    api = API["info"]["short_comment"]
    params = {
        "media_id": media_id,
        "ps": 20,
        "sort": order.value
    }
    if next is not None:
        params["cursor"] = next

    return await request('GET', api['url'], params, credential=credential)



async def get_long_comment_list(media_id: int, order: BangumiCommentOrder = BangumiCommentOrder.DEFAULT,
                           next: str = None, credential: Credential = None):
    """
    获取长评列表

    Args:
        media_id   (int)                          : media_id
        order      (BangumiCommentOrder, optional): 排序方式。Defaults to BangumiCommentOrder.DEFAULT
        next       (str, optional)                : 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None
        credential (Credential, optional)         : 凭据. Defaults to None
    """
    credential = credential if credential is not None else Credential()

    api = API["info"]["long_comment"]
    params = {
        "media_id": media_id,
        "ps": 20,
        "sort": order.value
    }
    if next is not None:
        params["cursor"] = next

    return await request('GET', api['url'], params, credential=credential)



async def get_episode_list(season_id: int, credential: Credential = None):
    """
    获取季度分集列表

    Args:
        season_id  (int)                 : season_id，从 get_meta() 中获取
        credential (Credential, optional): 凭据. Defaults to None
    """
    credential = credential if credential is not None else Credential()

    api = API["info"]["episodes_list"]
    params = {
        "season_id": season_id
    }
    return await request('GET', api['url'], params, credential=credential)


async def get_stat(season_id: int, credential: Credential = None):
    """
    获取番剧播放量，追番等信息

    Args:
        season_id  (int)                 : season_id，从 get_meta() 中获取
        credential (Credential, optional): 凭据. Defaults to None
    """
    credential = credential if credential is not None else Credential()

    api = API["info"]["season_status"]
    params = {
        "season_id": season_id
    }
    return await request('GET', api['url'], params, credential=credential)


async def get_episode_info(epid: int, credential: Credential = None):
    """
    获取番剧单集信息

    Args:
        epid       (int)                 : episode_id
        credential (Credential, optional): 凭据. Defaults to None
    """
    credential = credential if credential is not None else Credential()
    session = get_session()

    async with session.get(f"https://www.bilibili.com/bangumi/play/ep{epid}", cookies=credential.get_cookies(), headers={
        "User-Agent": "Mozilla/5.0"
    }) as resp:
        if resp.status != 200:
            raise ResponseException(resp.status)

        content = await resp.text()

        pattern = re.compile(r"window.__INITIAL_STATE__=(\{.*?\});")
        match = re.search(pattern, content)
        if match is None:
            raise ApiException("未找到番剧信息")
        try:
            content = json.loads(match.group(1))
        except json.JSONDecodeError:
            raise ApiException("信息解析错误")

        return content


async def get_overview(season_id: int, credential: Credential = None):
    """
    获取番剧全面概括信息，包括发布时间、剧集情况、stat 等情况

    Args:
        season_id  (int)                 : season_id，从 get_meta() 中获取
        credential (Credential, optional): 凭据. Defaults to None
    """
    credential = credential if credential is not None else Credential()

    api = API["info"]["collective_info"]
    params = {
        "season_id": season_id
    }
    return await request('GET', api['url'], params, credential=credential)


# 番剧操作


async def set_follow(season_id: int, status: bool = True, credential: Credential = None):
    """
    追番状态设置

    Args:
        season_id  (int)                 : season_id，从 get_meta() 中获取
        status     (bool, optional)      : 追番状态，Defaults to True
        credential (Credential, optional): 凭据. Defaults to None
    """
    credential = credential if credential is not None else Credential()
    credential.raise_for_no_sessdata()

    api = API["operate"]["follow_add"] if status else API["operate"]["follow_del"]
    data = {
        "season_id": season_id
    }
    return await request('POST', api['url'], data=data, credential=credential)
