r"""
模块：common
功能：通用API，一般用户用不上，不暴露给用户
项目GitHub地址：https://github.com/Passkou/bilibili_api
项目主页：https://passkou.com/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""

from . import exceptions, utils, user

API = utils.get_api()

COMMENT_TYPE_MAP = {
    "video": 1,
    "article": 12,
    "dynamic_draw": 11,
    "dynamic_text": 17,
    "audio": 14,
    "audio_list": 19
}
COMMENT_SORT_MAP = {
    "like": 2,
    "time": 0
}


def send_comment(text: str, oid: int, type_: str, root: int = None,
                 parent: int = None, verify: utils.Verify = None):
    """
    通用发送评论
    :param text:
    :param oid:
    :param type_:
    :param root:
    :param parent:
    :param verify:
    :return:
    """

    if verify is None:
        raise exceptions.BilibiliApiException("请提供verify")
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    type_ = COMMENT_TYPE_MAP.get(type_, None)
    if type_ is None:
        exceptions.BilibiliApiException("不支持的评论类型")

    # 参数检查完毕
    data = {
        "oid": oid,
        "type": type_,
        "message": text,
        "plat": 1,
        "csrf": verify.csrf
    }
    if parent is not None and root is None:
        # 直接回复媒体
        data["root"] = oid
        data["parent"] = parent
    elif parent is None and root is not None:
        # 回复动态下面的评论
        data["root"] = root
        data["parent"] = root
    elif parent is not None and root is not None:
        # 根据用户设置
        data["root"] = root
        data["parent"] = parent

    api = API["common"]["comment"]["send"]
    resp = utils.post(api["url"], data=data, cookies=verify.get_cookies())
    return resp


def operate_comment(action: str, oid: int, type_: str, rpid: int,
                    status: bool = True, verify: utils.Verify = None):
    """
    通用评论操作
    :param action: 操作类型，见api.json
    :param oid:
    :param type_:
    :param rpid:
    :param status: 设置状态
    :param verify:
    :return:
    """
    if verify is None:
        raise exceptions.BilibiliApiException("请提供verify")
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    type_ = COMMENT_TYPE_MAP.get(type_, None)
    assert type_ is not None, exceptions.BilibiliApiException("不支持的评论类型")

    comment_api = API["common"]["comment"]
    api = comment_api.get(action, None)
    assert api is not None, exceptions.BilibiliApiException("不支持的评论操作方式")
    # 参数检查完毕
    data = {
        "oid": oid,
        "type": type_,
        "rpid": rpid,
        "csrf": verify.csrf
    }
    if action != "del":
        data["action"] = 1 if status else 0

    resp = utils.post(api["url"], cookies=verify.get_cookies(), data=data)
    return resp


def get_comments_raw(oid: int, type_: str, order: str = "time", pn: int = 1, verify: utils.Verify = None):
    """
    通用获取评论
    :param oid:
    :param type_:
    :param order:
    :param pn:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    type_ = COMMENT_TYPE_MAP.get(type_, None)
    assert type_ is not None, exceptions.BilibiliApiException("不支持的评论类型")

    order = COMMENT_SORT_MAP.get(order, None)
    assert order is not None, exceptions.BilibiliApiException("不支持的排序方式，支持：time（时间倒序），like（热度倒序）")
    # 参数检查完毕
    params = {
        "oid": oid,
        "type": type_,
        "sort": order,
        "pn": pn
    }
    comment_api = API["common"]["comment"]
    api = comment_api.get("get", None)
    resp = utils.get(api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_comments(oid: int, type_: str, order: str = "time", verify: utils.Verify = None):
    """
    通用循环获取评论，使用生成器语法
    :param type_:
    :param order:
    :param oid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    page = 1
    while True:
        resp = get_comments_raw(oid=oid, pn=page, order=order, verify=verify, type_=type_)
        if "replies" not in resp:
            break
        if resp["replies"] is None:
            break
        for rep in resp["replies"]:
            yield rep
        page += 1


def get_sub_comments_raw(oid: int, type_: str, root: int, ps: int = 10, pn: int = 1, verify: utils.Verify = None):
    """
    通用获取子评论
    :param ps:
    :param root:
    :param oid:
    :param type_:
    :param pn:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    type_ = COMMENT_TYPE_MAP.get(type_, None)
    assert type_ is not None, exceptions.BilibiliApiException("不支持的评论类型")

    # 参数检查完毕
    params = {
        "oid": oid,
        "type": type_,
        "ps": ps,
        "pn": pn,
        "root": root
    }
    comment_api = API["common"]["comment"]
    api = comment_api.get("sub_reply", None)
    resp = utils.get(api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_sub_comments(oid: int, type_: str, root: int, ps: int = 10, verify: utils.Verify = None):
    """
    通用循环获取子评论，使用生成器语法
    :param ps:
    :param root:
    :param type_:
    :param oid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    page = 1
    while True:
        resp = get_sub_comments_raw(oid=oid, pn=page, root=root, ps=ps, verify=verify, type_=type_)
        if "replies" not in resp:
            break
        if resp["replies"] is None:
            break
        for rep in resp["replies"]:
            yield rep
        page += 1


def get_vote_info(vote_id: int, verify: utils.Verify = None):
    """
    获取投票信息
    :param vote_id:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["common"]["vote"]["info"]["get_info"]
    params = {
        "vote_id": vote_id
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


MEDIA_TYPE_MAP = {
    "audio": 12,
    "video": 2
}


def get_favorite_list_old(rid: int, up_mid: int, type_: str, pn: int = 1, ps: int = 100, verify: utils.Verify = None):
    """
    获取收藏夹列表，旧API
    :param rid:
    :param up_mid:
    :param type_:
    :param pn:
    :param ps:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    type_ = MEDIA_TYPE_MAP.get(type_, None)
    if type_ is None:
        raise exceptions.BilibiliApiException("不支持的类型")

    api = API["common"]["favorite"]["get_favorite_list_old"]
    params = {
        "up_mid": up_mid,
        "type": type_,
        "pn": pn,
        "ps": ps,
        "rid": rid
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_favorite_list(up_mid: int = None, rid: int = None, type_: str = None, verify: utils.Verify = None):
    """
    获取收藏夹列表
    :param up_mid:
    :param rid:
    :param type_:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    if rid is not None:
        if type_ is None:
            raise exceptions.BilibiliApiException("请指定type_")
        type_ = MEDIA_TYPE_MAP.get(type_, None)
        if type_ is None:
            raise exceptions.BilibiliApiException("不支持的类型")

    if up_mid is None:
        self_info = user.get_self_info(verify)
        up_mid = self_info["mid"]

    api = API["common"]["favorite"]["get_favorite_list"]
    params = {
        "up_mid": up_mid
    }
    if rid is not None:
        params.update({
            "type": type_,
            "rid": rid
        })
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def operate_favorite(rid: int, type_: str, add_media_ids: list = None,
                     del_media_ids: list = None, verify: utils.Verify = None):
    """
    操作收藏夹
    :param rid:
    :param type_:
    :param add_media_ids: 要添加的收藏夹内容列表
    :param del_media_ids: 要删除的收藏夹内容列表
    :param verify:
    :return:
    """
    if verify is None:
        raise exceptions.BilibiliApiException("请提供verify")
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])
    if add_media_ids is None:
        add_media_ids = []
    if del_media_ids is None:
        del_media_ids = []
    if len(add_media_ids) == 0 and len(del_media_ids) == 0:
        raise exceptions.BilibiliApiException("add_media_ids和del_media_ids至少提供一个")
    type_ = MEDIA_TYPE_MAP.get(type_, None)
    if type_ is None:
        raise exceptions.BilibiliApiException("不支持的类型")

    api = API["common"]["favorite"]["operate_favorite"]
    data = {
        "rid": rid,
        "type": type_,
        "add_media_ids": ",".join([str(i) for i in add_media_ids]),
        "del_media_ids": ",".join([str(i) for i in del_media_ids]),
        "csrf": verify.csrf
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def dynamic_share(type_: str, rid: int, content: str,
                  title: str = None, cover_url: str = None, target_url: str = None, verify: utils.Verify = None):
    """
    分享站内资源到动态
    :param type_:
    :param rid:
    :param content:
    :param title:
    :param cover_url:
    :param target_url:
    :param verify:
    :return:
    """
    if verify is None:
        raise exceptions.BilibiliApiException("请提供verify")
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    TYPE_MAP = {
        "video": 8,
        "article": 64,
        "audio": 256,
        "custom": 2048,
        "bangumi": 4097
    }
    type_ = TYPE_MAP.get(type_, None)
    if type_ is None:
        raise exceptions.BilibiliApiException("不支持的分享类型")

    api = API["common"]["dynamic_share"]
    data = {
        "type": type_,
        "content": content,
        "rid": rid,
        "csrf": verify.csrf,
        "csrf_token": verify.csrf,
        "uid": 0,
        "share_uid": 0
    }
    if type_ == TYPE_MAP["custom"]:
        # 自定义分享卡片
        if not all([title, cover_url, target_url]):
            raise exceptions.BilibiliApiException("自定义分享卡片需要传入完整参数")
        else:
            data.update({
                "sketch[title]": title,
                "sketch[biz_type]": 131,
                "sketch[cover_url]": cover_url,
                "sketch[target_url]": target_url
            })
    resp = utils.post(url=api["url"], cookies=verify.get_cookies(), data=data)
    return resp


def web_search(keyword: str):
    """
    只指定关键字在web进行搜索，返回未经处理的字典
    """
    api = API["common"]["search"]["web_search"]
    params = {
        "keyword": keyword
    }
    resp = utils.get(url=api["url"], params=params)
    return resp

def web_search_by_type(keyword: str, search_type: str):
    """
    指定关键字和类型在web进行搜索，返回未经处理的字典
    类型：视频(video)、番剧(media_bangumi)、影视(media_ft)、直播(live)、专栏(article)、话题(topic)、用户(bili_user)
    """
    api = API["common"]["search"]["web_search_by_type"]
    params = {
        "keyword": keyword,
        "search_type": search_type
    }
    resp = utils.get(url=api["url"], params=params)
    return resp
