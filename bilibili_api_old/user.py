r"""
模块：user
功能：获取用户各种信息以及操作用户
项目GitHub地址：https://github.com/Passkou/bilibili_api
  _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""
import json
from . import utils, exceptions, common
import time

API = utils.get_api()


def get_user_info(uid: int, verify: utils.Verify = None):
    """
    获取用户信息（昵称，性别，生日，签名，头像URL，空间横幅URL等）
    :param uid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["user"]["info"]["info"]
    params = {
        "mid": uid
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_self_info(verify: utils.Verify = None):
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException("需要验证：SESSDATA")
    url = "https://api.bilibili.com/x/web-interface/nav"
    resp = utils.get(url, cookies=verify.get_cookies())
    return resp


def get_relation_info(uid: int, verify: utils.Verify = None):
    """
    获取用户关系信息（关注数，粉丝数，悄悄关注，黑名单数）
    B站API太乱了。。。
    :param uid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["user"]["info"]["relation"]
    params = {
        "vmid": uid
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_up_info(uid: int, verify: utils.Verify = None):
    """
    获取UP主数据信息（视频总播放量，文章总阅读量，总点赞数）
    B站API太乱了。。。
    :param uid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["user"]["info"]["upstat"]
    params = {
        "mid": uid
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_live_info(uid: int, verify: utils.Verify = None):
    """
    获取用户直播间信息
    :param uid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["user"]["info"]["live"]
    params = {
        "mid": uid
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_videos_g(uid: int, order: str = "pubdate", verify: utils.Verify = None):
    """
    自动循环获取用户投稿视频信息
    :param uid:
    :param order: 排序，接受"pubdate", "view", "favorite"
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    page = 1
    while True:
        data = get_videos_raw(uid=uid, order=order, pn=page, verify=verify)
        if not data["list"]["vlist"]:
            break
        for v in data["list"]["vlist"]:
            yield v
        page += 1


def get_videos_raw(uid: int, ps: int = 30, tid: int = 0, pn: int = 1, keyword: str = "",
                   order: str = "pubdate", verify: utils.Verify = None):
    """
    低层级API，获取视频信息API的原始返回
    :param uid:
    :param ps: 每页最多几个视频，保持默认30即可
    :param tid: 分区ID
    :param pn: 第几页，从1开始
    :param keyword: 搜索关键词
    :param order: 排序，接受"pubdate", "view", "favorite"
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    ORDER_MAP = {
        "pubdate": "pubdate",
        "view": "click",
        "favorite": "stow"
    }
    if order not in ORDER_MAP:
        raise exceptions.BilibiliApiException("排序方式无效，可用值：pubdate（上传日期）、view（播放量）、favorite（收藏量）")

    api = API["user"]["info"]["video"]
    params = {
        "mid": uid,
        "ps": ps,
        "tid": tid,
        "pn": pn,
        "keyword": keyword,
        "order": ORDER_MAP[order]
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_audios_g(uid: int, order: str = "pubdate", verify: utils.Verify = None):
    """
    获取用户音频投稿
    :param uid:
    :param order: 排序，接受"pubdate", "view", "favorite"
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    page = 1
    while True:
        data = get_audios_raw(uid=uid, order=order, pn=page, verify=verify)
        if not data["data"]:
            break
        for au in data["data"]:
            yield au
        page += 1


def get_audios_raw(uid: int, order: str = "pubdate", ps: int = 30,
                   pn: int = 1, verify: utils.Verify = None):
    """
    低层级API，获取用户音频投稿API原始返回
    :param uid:
    :param order:
    :param ps:
    :param pn:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    ORDER_MAP = {
        "pubdate": 1,
        "view": 2,
        "favorite": 3
    }
    if order not in ORDER_MAP:
        raise exceptions.BilibiliApiException("排序方式无效，可用值：pubdate（上传日期）、view（播放量）、favorite（收藏量）")
    api = API["user"]["info"]["audio"]
    params = {
        "uid": uid,
        "ps": ps,
        "pn": pn,
        "order": ORDER_MAP[order]
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_articles_g(uid: int, order: str = "pubdate", verify: utils.Verify = None):
    """
    自动循环获取专栏投稿
    :param uid:
    :param order: 排序方式，pubdate（上传日期）、view（播放量）、favorite（收藏量）
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    page = 1
    while True:
        data = get_articles_raw(uid=uid, order=order, verify=verify, pn=page)
        if "articles" not in data:
            break
        else:
            for ar in data["articles"]:
                yield ar
            page += 1


def get_articles_raw(uid: int, pn: int = 1, ps: int = 30, order: str = "pubdate", verify: utils.Verify = None):
    """
    低层级API，获取专栏投稿API原始返回
    :param ps: 一页多少，保持30默认即可
    :param pn: 页码
    :param uid:
    :param order: 排序方式，pubdate（上传日期）、view（播放量）、favorite（收藏量）
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    ORDER_MAP = {
        "pubdate": "publish_time",
        "view": "view",
        "favorite": "fav"
    }
    if order not in ORDER_MAP:
        raise exceptions.BilibiliApiException("排序方式无效，可用值：pubdate（上传日期）、view（播放量）、favorite（收藏量）")

    api = API["user"]["info"]["article"]
    params = {
        "mid": uid,
        "ps": ps,
        "pn": pn,
        "sort": ORDER_MAP[order]
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_article_list(uid: int, order: str = "latest", verify: utils.Verify = None):
    """
    获取专栏文集
    :param uid:
    :param order: 排序方式，接受 "latest"（最近更新），"view"（最多阅读）
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    ORDER_MAP = {
        "latest": 0,
        "view": 1
    }
    if order not in ORDER_MAP:
        raise exceptions.BilibiliApiException("排序方式无效，可用值：\"latest\"（最近更新），\"view\"（最多阅读）")

    api = API["user"]["info"]["article_lists"]
    params = {
        "mid": uid,
        "sort": ORDER_MAP[order]
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_dynamic_raw(uid: int, offset: str = 0, need_top: bool = False, verify: utils.Verify = None):
    if verify is None:
        verify = utils.Verify()
    api = API["user"]["info"]["dynamic"]
    params = {
        "host_uid": uid,
        "offset_dynamic_id": offset,
        "need_top": 1 if need_top else 0
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    if data['has_more'] != 1:
        return data
    for card in data["cards"]:
        card["card"] = json.loads(card["card"])
        card["extend_json"] = json.loads(card["extend_json"])

    return data


def get_dynamic_g(uid: int, verify: utils.Verify = None):
    """
    自动循环获取用户动态
    :param uid:
    :param verify:
    :return:
    """

    offset = "0"
    while True:
        data = get_dynamic_raw(uid, offset, verify=verify)
        if 'cards' not in data:
            break
        for c in data["cards"]:
            yield c
        if data["has_more"] != 1:
            break
        offset = data["next_offset"]


def get_bangumi_g(uid: int, type_: str = "bangumi", verify: utils.Verify = None):
    """
    自动循环获取追番/追剧列表
    :param uid:
    :param type_:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    page = 1
    while True:
        data = get_bangumi_raw(uid=uid, pn=page, type_=type_, verify=verify)
        if len(data["list"]) == 0:
            break
        for b in data["list"]:
            yield b
        page += 1


def get_bangumi_raw(uid: int, pn: int = 1, ps: int = 15, type_: str = "bangumi", verify: utils.Verify = None):
    """
    低层级API，获取追番/追剧列表原始API返回
    :param uid:
    :param pn: 页码
    :param ps: 每页多少，保持默认15
    :param type_: 类型：bangumi（番剧），drama（追剧）
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    TYPE_MAP = {
        "bangumi": 1,
        "drama": 2
    }
    if type_ not in TYPE_MAP:
        raise exceptions.BilibiliApiException("type_类型错误。接受：bangumi（番剧），drama（追剧）")

    api = API["user"]["info"]["bangumi"]
    params = {
        "vmid": uid,
        "pn": pn,
        "ps": ps,
        "type": TYPE_MAP[type_]
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_favorite_list_content_raw(media_id: int, pn: int = 1, ps: int = 20, keyword: str = "",
                                  order: str = "mtime", type_: int = 0, tid: int = 0, verify: utils.Verify = None):
    """
    获取收藏夹内容
    :param media_id: 收藏夹id
    :param pn:
    :param ps:
    :param keyword: 搜索关键词
    :param order: 排序依据。mtime最近收藏，view最多播放，pubtime最新投稿
    :param type_:
    :param tid: 分区ID，0为全部
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["common"]["favorite"]["get_favorite_list_content"]
    params = {
        "media_id": media_id,
        "pn": pn,
        "ps": ps,
        "keyword": keyword,
        "order": order,
        "type": type_,
        "tid": tid
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_favorite_list_content_g(media_id: int, order: str = "mtime", verify: utils.Verify = None):
    """
    自动循环获取收藏夹内容
    :param media_id: 收藏夹分类ID
    :param order: 排序方式，接受值：mtime（最近收藏）、view（最多播放）、pubtime（最近投稿）
    :param verify:
    :return:
    """
    page = 1
    while True:
        data = get_favorite_list_content_raw(media_id=media_id, order=order, pn=page, verify=verify)
        if "medias" not in data:
            break
        if data["medias"] is None:
            break
        for m in data["medias"]:
            yield m
        page += 1


def get_favorite_list(uid: int, verify: utils.Verify = None):
    """
    获取收藏夹列表
    :param uid:
    :param verify:
    :return:
    """
    resp = common.get_favorite_list(uid, verify=verify)
    return resp


def get_followings_raw(uid: int, ps: int = 20, pn: int = 1, order: str = "desc", verify: utils.Verify = None):
    """
    低层级API,获取用户关注列表（不是自己只能访问前5页）
    :param order: desc倒序,asc正序
    :param pn: 页码
    :param ps: 每页数量
    :param uid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    assert order in ("desc", "asc"), exceptions.BilibiliApiException("不支持的排序方式")

    api = API["user"]["info"]["followings"]
    params = {
        "vmid": uid,
        "ps": ps,
        "pn": pn,
        "order": order
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_followings_g(uid: int, order: str = "desc", verify: utils.Verify = None):
    """
    获取用户关注列表
    :param uid:
    :param order: desc倒序,asc正序
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    page = 1
    while True:
        try:
            data = get_followings_raw(uid=uid, order=order, pn=page, verify=verify)
        except exceptions.BilibiliException as e:
            if e.code == 22007:
                break
            else:
                raise e
        if len(data["list"]) == 0:
            break
        for f in data["list"]:
            yield f
        page += 1


def get_followers_raw(uid: int, ps: int = 20, pn: int = 1, order: str = "desc", verify: utils.Verify = None):
    """
    低层级API,获取用户粉丝列表（不是自己只能访问前5页，是自己也不能获取全部的样子）
    :param order: desc倒序,asc正序
    :param pn: 页码
    :param ps: 每页数量
    :param uid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    assert order in ("desc", "asc"), exceptions.BilibiliApiException("不支持的排序方式")

    api = API["user"]["info"]["followers"]
    params = {
        "vmid": uid,
        "ps": ps,
        "pn": pn,
        "order": order
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


def get_followers_g(uid: int, order: str = "desc", verify: utils.Verify = None):
    """
    获取用户粉丝列表（不是自己只能访问前5页，是自己也不能获取全部的样子）
    :param uid:
    :param order: desc倒序,asc正序
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    page = 1
    while True:
        try:
            data = get_followers_raw(uid=uid, order=order, pn=page, verify=verify)
        except exceptions.BilibiliException as e:
            if e.code == 22007:
                break
            else:
                raise e
        if len(data["list"]) == 0:
            break
        for f in data["list"]:
            yield f
        page += 1


def get_overview(uid: int, verify: utils.Verify = None):
    """
    获取用户的简易订阅和投稿信息
    :param uid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    api = API["user"]["info"]["overview"]
    params = {
        "mid": uid,
        "jsonp": "jsonp",
        "callback": "__jp8"
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return data


# 操作用户


def set_subscribe(uid: int, status: bool = True, whisper: bool = False, verify: utils.Verify = None):
    """
    设置用户关注状态
    :param whisper: 设置关注时是否为悄悄关注
    :param uid:
    :param status: 状态，True or False
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["user"]["operate"]["modify"]
    data = {
        "fid": uid,
        "act": 1 if status else 2,
        "re_src": 11,
        "csrf": verify.csrf
    }
    if status and whisper:
        data["act"] = 3
    data = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return data


def set_black(uid: int, status: bool = True, verify: utils.Verify = None):
    """
    设置用户拉黑状态
    :param uid:
    :param status: 状态，True or False
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["user"]["operate"]["modify"]
    data = {
        "fid": uid,
        "act": 5 if status else 6,
        "re_src": 11,
        "csrf": verify.csrf
    }
    data = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return data


def remove_fans(uid: int, verify: utils.Verify = None):
    """
    移除粉丝
    :param uid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["user"]["operate"]["modify"]
    data = {
        "fid": uid,
        "act": 7,
        "re_src": 11,
        "csrf": verify.csrf
    }
    data = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return data


def send_msg(uid: int, text: str, self_uid: int = None, verify: utils.Verify = None):
    """
    给用户发送私聊信息
    :param uid:
    :param text: 内容
    :param self_uid: 自己的UID，若不提供将自动获取
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["user"]["operate"]["send_msg"]
    if self_uid is None:
        self_info = get_self_info(verify)
        sender_uid = self_info["mid"]
    else:
        sender_uid = self_uid
    data = {
        "msg[sender_uid]": sender_uid,
        "msg[receiver_id]": uid,
        "msg[receiver_type]": 1,
        "msg[msg_type]": 1,
        "msg[msg_status]": 0,
        "msg[content]": json.dumps({"content": text}),
        "msg[dev_id]": "1369CA35-1771-4B80-B6D4-D7EB975B7F8A",
        "msg[new_face_version]": "0",
        "msg[timestamp]": int(time.time()),
        "csrf_token": verify.csrf,
        "csrf": verify.csrf
    }
    data = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return data

# 分组操作


def get_self_subscribe_group(verify: utils.Verify):
    """
    获取自己的关注分组列表
    :param verify:
    :return:
    """
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["user"]["info"]["self_subscribe_group"]
    resp = utils.get(api["url"], cookies=verify.get_cookies())
    return resp


def get_user_in_which_subscribe_groups(uid: int, verify: utils.Verify):
    """
    获取用户在哪些关注分组列表
    :param uid:
    :param verify:
    :return:
    """
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["user"]["info"]["get_user_in_which_subscribe_groups"]
    params = {
        "fid": uid
    }
    resp = utils.get(api["url"], params=params, cookies=verify.get_cookies())
    return resp


def add_subscribe_group(name: str, verify: utils.Verify):
    """
    添加关注分组
    :param name: 分组名
    :param verify:
    :return:
    """
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["user"]["operate"]["add_subscribe_group"]
    payload = {
        "tag": name,
        "csrf": verify.csrf
    }
    resp = utils.post(api["url"], data=payload, cookies=verify.get_cookies())
    return resp


def del_subscribe_group(group_id: int, verify: utils.Verify):
    """
    删除关注分组
    :param group_id: 分组ID
    :param verify:
    :return:
    """
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["user"]["operate"]["del_subscribe_group"]
    payload = {
        "tagid": group_id,
        "csrf": verify.csrf
    }
    resp = utils.post(api["url"], data=payload, cookies=verify.get_cookies())
    return resp


def rename_subscribe_group(group_id: int, new_name: str, verify: utils.Verify):
    """
    重命名关注分组
    :param new_name: 新的分组名
    :param group_id: 分组ID
    :param verify:
    :return:
    """
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["user"]["operate"]["rename_subscribe_group"]
    payload = {
        "tagid": group_id,
        "name": new_name,
        "csrf": verify.csrf
    }
    resp = utils.post(api["url"], data=payload, cookies=verify.get_cookies())
    return resp


def move_user_subscribe_group(uid: int, group_ids: list, verify: utils.Verify):
    """
    移动用户到特定的关注分组
    :param uid:
    :param group_ids: 分组id列表，为空时移动到默认分组
    :param verify:
    :return:
    """
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["user"]["operate"]["move_user_subscribe_group"]
    payload = {
        "fids": uid,
        "tagids": ",".join(list(map(lambda x: str(x), group_ids))) if len(group_ids) != 0 else "0",
        "csrf": verify.csrf
    }
    resp = utils.post(api["url"], data=payload, cookies=verify.get_cookies())
    return resp


"""
もしかしてうちは、田舎に住んでいるん？
ーー「のんのんびより」
"""
