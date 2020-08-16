r"""
模块：user
功能：获取用户各种信息以及操作用户
项目GitHub地址：https://github.com/Passkou/bilibili_api
项目主页：https://passkou.com/bilibili_api
  _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""
import json
from . import utils, exceptions, common

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


def get_videos(uid: int, order: str = "pubdate", limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    自动循环获取用户投稿视频信息
    :param callback: 回调函数
    :param uid:
    :param order: 排序，接受"pubdate", "view", "favorite"
    :param limit: 限制数量
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    count = 0
    page = 1
    videos = []
    while count < limit:
        data = get_videos_raw(uid=uid, order=order, pn=page, verify=verify)
        if not data["list"]["vlist"]:
            break
        count += len(data["list"]["vlist"])
        videos += data["list"]["vlist"]
        if callable(callback):
            callback(data["list"]["vlist"])
        page += 1
    return videos[:limit]


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


def get_audios(uid: int, order: str = "pubdate", limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    获取用户音频投稿
    :param callback:
    :param uid:
    :param order: 排序，接受"pubdate", "view", "favorite"
    :param limit: 数量限制
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    count = 0
    page = 1
    audios = []
    while count < limit:
        data = get_audios_raw(uid=uid, order=order, pn=page, verify=verify)
        if not data["data"]:
            break
        count += len(data["data"])
        audios += data["data"]
        if callable(callback):
            callback(data["data"])
        page += 1
    return audios[:limit]


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


def get_articles(uid: int, order: str = "pubdate", limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    自动循环获取专栏投稿
    :param callback: 回调函数
    :param uid:
    :param order: 排序方式，pubdate（上传日期）、view（播放量）、favorite（收藏量）
    :param limit: 限制数量
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    count = 0
    page = 1
    articles = []
    while count < limit:
        data = get_articles_raw(uid=uid, order=order, verify=verify, pn=page)
        if "articles" not in data:
            break
        else:
            articles += data["articles"]
            if callable(callback):
                callback(data["articles"])
            count += len(data["articles"])
            page += 1
    return articles[:limit]


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
    for card in data["cards"]:
        card["card"] = json.loads(card["card"])
        card["extend_json"] = json.loads(card["extend_json"])

    return data


def get_dynamic(uid: int, limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    自动循环获取用户动态
    :param callback:
    :param uid:
    :param limit: 限制数量
    :param verify:
    :return:
    """

    offset = "0"
    count = 0
    dynamic = []
    while count < limit:
        data = get_dynamic_raw(uid, offset, verify=verify)
        dynamic += data["cards"]
        if callable(callback):
            callback(data["cards"])
        if data["has_more"] != 1:
            break
        count += len(data["cards"])
        offset = data["next_offset"]

    return dynamic[:limit]


def get_bangumi(uid: int, type_: str = "bangumi", limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    自动循环获取追番/追剧列表
    :param callback: 回调函数
    :param uid:
    :param type_:
    :param limit:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    bangumi = []
    page = 1
    count = 0
    while count < limit:
        data = get_bangumi_raw(uid=uid, pn=page, type_=type_, verify=verify)
        if len(data["list"]) == 0:
            break
        bangumi += data["list"]
        if callable(callback):
            callback(data["list"])
        count += len(data["list"])
        page += 1
    return bangumi[:limit]


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


def get_favorite_list_content(media_id: int, order: str = "mtime",
                              limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    自动循环获取收藏夹内容
    :param callback: 回调函数
    :param media_id: 收藏夹分类ID
    :param order: 排序方式，接受值：mtime（最近收藏）、view（最多播放）、pubtime（最近投稿）
    :param limit: 限制数量
    :param verify:
    :return:
    """
    count = 0
    page = 1
    content = []
    while count < limit:
        data = get_favorite_list_content_raw(media_id=media_id, order=order, pn=page, verify=verify)
        if "medias" not in data:
            break
        if data["medias"] is None:
            break
        count += len(data["medias"])
        content += data["medias"]
        if callable(callback):
            callback(data["medias"])
        page += 1
    return content[:limit]


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


def get_followings(uid: int, order: str = "desc", limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    获取用户关注列表
    :param callback: 回调
    :param uid:
    :param order: desc倒序,asc正序
    :param limit: 数量限制
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    count = 0
    page = 1
    followings = []
    while count < limit:
        try:
            data = get_followings_raw(uid=uid, order=order, pn=page, verify=verify)
        except exceptions.BilibiliException as e:
            if e.code == 22007:
                break
            else:
                raise e
        if len(data["list"]) == 0:
            break
        count += len(data["list"])
        if callable(callback):
            callback(data["list"])
        followings += data["list"]
        if callable(callback):
            callback(data["list"])
        page += 1
    return followings[:limit]


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


def get_followers(uid: int, order: str = "desc", limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    获取用户粉丝列表（不是自己只能访问前5页，是自己也不能获取全部的样子）
    :param callback: 回调
    :param uid:
    :param order: desc倒序,asc正序
    :param limit: 数量限制
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    count = 0
    page = 1
    followings = []
    while count < limit:
        try:
            data = get_followers_raw(uid=uid, order=order, pn=page, verify=verify)
        except exceptions.BilibiliException as e:
            if e.code == 22007:
                break
            else:
                raise e
        if len(data["list"]) == 0:
            break
        if callable(callback):
            callback(data["list"])
        count += len(data["list"])
        followings += data["list"]
        if callable(callback):
            callback(data["list"])
        page += 1
    return followings[:limit]


def get_navnum(uid: int, verify: utils.Verify = None):
    """
    获取用户的简易订阅和投稿信息
    :param uid:
    :param verify:
    :return:
    """
    api = API["user"]["info"]["navnum"]
    params = {
        "mid": uid,
        "jsonp": "jsonp",
        "callback": "__jp8"  #必须带有这个默认的参数
    }
    data = utils.get(url=api["url"], params=params, verify=verify, data_type='text')
    json_data = json.loads(data[6:-1])['data']  # 转为json格式处理最后返回data
    return json_data


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
        "csrf_token": verify.csrf
    }
    data = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return data


"""
もしかしてうちは、田舎に住んでいるん？
ーー「のんのんびより」
"""