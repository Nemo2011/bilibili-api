r"""
模块：bangumi
功能：番剧相关
项目GitHub地址：https://github.com/Passkou/bilibili_api
项目主页：https://passkou.com/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""

from . import utils, exceptions, common
from .common import get_vote_info

API = utils.get_api()


def get_meta(media_id: int, verify: utils.Verify = None):
    """
    获取番剧元数据信息（评分，封面URL，标题等）
    :param media_id: media_id（URL中的/md*****）
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["bangumi"]["info"]["meta"]
    params = {
        "media_id": media_id
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_short_comments_raw(media_id: int, ps: int = 20, sort: str = "default",
                           cursor: str = None, verify: utils.Verify = None):
    """
    低层级API获取短评列表
    :param media_id:
    :param ps: 默认20即可
    :param sort: 排序方式0默认1按时间倒序
    :param cursor: 循环获取用，第一次调用本API返回中的next值
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    ORDER_MAP = {
        "default": 0,
        "time": 1
    }
    if sort not in ORDER_MAP:
        raise exceptions.BilibiliApiException("不支持的排序方式。支持：default（默认排序）time（时间倒序）")

    api = API["bangumi"]["info"]["short_comment"]
    params = {
        "media_id": media_id,
        "ps": ps,
        "sort": ORDER_MAP[sort]
    }
    if cursor is not None:
        params["cursor"] = cursor
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_short_comments(media_id: int, order: str = "default", limit: int = 114514,
                       callback=None, verify: utils.Verify = None):
    """
    自动循环获取短评
    :param callback: 回调函数，每次获取到一页会将该页数据传入指定的函数
    :param media_id:
    :param order: default（默认排序）time（时间倒序）
    :param limit: 限制获取数量
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    cursor = None
    count = 0
    comments = []
    while count < limit:
        resp = get_short_comments_raw(media_id=media_id, sort=order, cursor=cursor, verify=verify)
        if "list" not in resp:
            break
        if resp["list"] is None:
            break
        if len(resp["list"]) == 0:
            break

        count += len(resp["list"])
        comments += resp["list"]
        if callable(callback):
            callback(resp["list"])

        if "next" not in resp:
            break
        cursor = resp["next"]
    return comments[:limit]


def get_long_comments_raw(media_id: int, ps: int = 20, sort: str = "default",
                          cursor: str = None, verify: utils.Verify = None):
    """
    低层级API获取长评列表
    :param media_id:
    :param ps: 默认20即可
    :param sort: 排序方式0默认1按时间倒序
    :param cursor: 循环获取用，第一次调用本API返回中的next值
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    ORDER_MAP = {
        "default": 0,
        "time": 1
    }
    if sort not in ORDER_MAP:
        raise exceptions.BilibiliApiException("不支持的排序方式。支持：default（默认排序）time（时间倒序）")

    api = API["bangumi"]["info"]["long_comment"]
    params = {
        "media_id": media_id,
        "ps": ps,
        "sort": ORDER_MAP[sort]
    }
    if cursor is not None:
        params["cursor"] = cursor
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_long_comments(media_id: int, order: str = "default", limit: int = 114514,
                      callback=None, verify: utils.Verify = None):
    """
    自动循环获取长评
    :param callback: 回调函数，每次获取到一页会将该页数据传入指定的函数
    :param media_id:
    :param order: default（默认排序）time（时间倒序）
    :param limit: 限制获取数量
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    cursor = None
    count = 0
    comments = []
    while count < limit:
        resp = get_long_comments_raw(media_id=media_id, sort=order, cursor=cursor, verify=verify)
        if "list" not in resp:
            break
        if resp["list"] is None:
            break
        if len(resp["list"]) == 0:
            break

        count += len(resp["list"])
        comments += resp["list"]
        if callable(callback):
            callback(resp["list"])

        if "next" not in resp:
            break
        cursor = resp["next"]
    return comments[:limit]


def get_episodes_list(season_id: int, verify: utils.Verify = None):
    """
    获取季度分集列表
    :param season_id: season_id，从get_meta中获取
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["bangumi"]["info"]["episodes_list"]
    params = {
        "season_id": season_id
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_interact_data(season_id: int, verify: utils.Verify = None):
    """
    获取番剧播放量，追番等信息
    :param season_id:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["bangumi"]["info"]["season_status"]
    params = {
        "season_id": season_id
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


# 番剧操作


def set_follow(season_id: int, status: bool = True, verify: utils.Verify = None):
    """
    追番状态设置
    :param season_id:
    :param status: True追番False取消
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["bangumi"]["operate"]["follow_add"] if status else API["bangumi"]["operate"]["follow_del"]
    data = {
        "season_id": season_id,
        "csrf": verify.csrf
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def set_follow_status(season_id: int, status: int = 2, verify: utils.Verify = None):
    """
    追番状态设置
    :param season_id:
    :param status: 1想看2在看3已看
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])
    if status not in (1, 2, 3):
        raise exceptions.BilibiliApiException("不支持的追番状态。1想看2在看3已看")

    api = API["bangumi"]["operate"]["follow_status"]
    data = {
        "season_id": season_id,
        "csrf": verify.csrf,
        "status": status
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def share_to_dynamic(epid: int, content: str, verify: utils.Verify = None):
    """
    专栏转发
    :param epid: EP号
    :param content:
    :param verify:
    :return:
    """
    resp = common.dynamic_share("bangumi", epid, content, verify=verify)
    return resp

"""
こころぴょんぴょん待ち  考えるふりして  もうちょっと近づいちゃえ　♪
ーー「ご注文はうさぎですか？」
"""