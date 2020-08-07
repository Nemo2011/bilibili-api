r"""
模块： dynamic
功能： 动态发送、操作、信息获取等
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""
from . import user, exceptions, utils
import re
import json
import datetime

API = utils.get_api()


def __upload_images(images_path: list, verify: utils.Verify):
    """
    上传图片
    :param images_path: 图片路径列表
    :return:
    """
    api = API["dynamic"]["send"]["upload_img"]
    data = {
        "biz": "draw",
        "category": "daily"
    }
    images_info = []
    for path in images_path:
        files = {
            "file_up": open(path, "rb")
        }
        resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies(), files=files)
        images_info.append(resp)
    return images_info


def __parse_at(text: str):
    """
    @人格式：“@UID ”(注意最后有空格）
    :param text: 原始文本
    :return:
    """
    pattern = re.compile(r"(?<=@)\d*?(?=\s)")
    match_result = re.finditer(pattern, text)
    uid_list = []
    names = []
    new_text = text
    for match in match_result:
        uid = match.group()
        user_info = user.get_user_info(int(uid))
        name = user_info["name"]
        uid_list.append(uid)
        names.append(name)
        new_text = new_text.replace(f"@{uid} ", f"@{name} ")
    at_uids = ",".join(uid_list)
    ctrl = []
    for i, name in enumerate(names):
        index = new_text.index(f"@{name}")
        length = 2 + len(name)
        ctrl.append({
            "location": index,
            "type": 1,
            "length": length,
            "data": int(uid_list[i])
        })
    return new_text, at_uids, json.dumps(ctrl, ensure_ascii=False)


def __get_text_data(text: str, verify: utils.Verify):
    """
    获取文本动态请求参数
    :param text: 原始文本内容
    :param verify:
    :return:
    """
    new_text, at_uids, ctrl = __parse_at(text)
    data = {
        "dynamic_id": 0,
        "type": 4,
        "rid": 0,
        "content": new_text,
        "extension": "{\"emoji_type\":1}",
        "at_uids": at_uids,
        "ctrl": ctrl,
        "csrf_token": verify.csrf
    }
    return data


def __get_draw_data(text: str, images_path: list, verify: utils.Verify):
    """
    获取图片动态请求参数
    :param text:
    :param images_path:
    :param verify:
    :return:
    """
    new_text, at_uids, ctrl = __parse_at(text)
    images_info = __upload_images(images_path, verify)

    def pic(image):
        return {"img_src": image["image_url"], "img_width": image["image_width"],
                "img_height": image["image_height"]}

    pictures = list(map(pic, images_info))
    data = {
        "biz": 3,
        "category": 3,
        "type": 0,
        "pictures": json.dumps(pictures),
        "title": "",
        "tags": "",
        "description": new_text,
        "content": new_text,
        "from": "create.dynamic.web",
        "up_choose_comment": 0,
        "extension": json.dumps({"emoji_type": 1, "from": {"emoji_type": 1}, "flag_cfg": {}}),
        "at_uids": at_uids,
        "at_control": ctrl,
        "setting": json.dumps({
            "copy_forbidden": 0,
            "cachedTime": 0
        }),
        "csrf_token": verify.csrf
    }
    return data


def send_dynamic(text: str, images_path: list = None, send_time: datetime.datetime = None, verify: utils.Verify = None):
    """
    自动判断动态类型选择合适的API并发送动态
    :param text: 动态文本
    :param images_path: 图片路径列表
    :param send_time: 发送时间datatime类
    :param verify:
    :return:
    """

    def instant_text():
        api = API["dynamic"]["send"]["instant_text"]
        data = __get_text_data(text, verify)
        resp = utils.post(api["url"], data=data, cookies=verify.get_cookies())
        return resp

    def instant_draw():
        api = API["dynamic"]["send"]["instant_draw"]
        data = __get_draw_data(text, images_path, verify)
        resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
        return resp

    def schedule(type_: int):
        api = API["dynamic"]["send"]["schedule"]
        if type_ == 4:
            # 画册动态
            request = __get_draw_data(text, images_path, verify)
            request.pop("setting")
        elif type_ == 2:
            # 文字动态
            request = __get_text_data(text, verify)
        else:
            raise exceptions.BilibiliApiException("暂不支持的动态类型")
        data = {
            "type": type_,
            "publish_time": int(send_time.timestamp()),
            "request": json.dumps(request, ensure_ascii=False),
            "csrf_token": verify.csrf
        }
        resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
        return resp

    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    if images_path is None:
        images_path = []

    if len(images_path) == 0:
        if send_time is None:
            ret = instant_text()
        else:
            ret = schedule(2)
    else:
        if len(images_path) > 9:
            raise exceptions.BilibiliApiException("最多上传9张图片")
        if send_time is None:
            ret = instant_draw()
        else:
            ret = schedule(4)
    return ret


# 定时动态操作


def get_schedules_list(verify: utils.Verify = None):
    """
    获取待发送定时动态列表
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["dynamic"]["schedule"]["list"]
    resp = utils.get(url=api["url"], cookies=verify.get_cookies())
    return resp


def send_schedule_now(draft_id: int, verify: utils.Verify = None):
    """
    立即发送定时动态
    :param draft_id: 定时动态ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["dynamic"]["schedule"]["publish_now"]
    data = {
        "draft_id": draft_id,
        "csrf_token": verify.csrf
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def delete_schedule(draft_id: int, verify: utils.Verify = None):
    """
    删除定时动态
    :param draft_id: 定时动态ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["dynamic"]["schedule"]["delete"]
    data = {
        "draft_id": draft_id,
        "csrf_token": verify.csrf
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp

# 动态信息


def get_info(dynamic_id: int, verify: utils.Verify = None):
    """
    获取动态信息
    :param dynamic_id: 动态ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["dynamic"]["info"]["detail"]
    params = {
        "dynamic_id": dynamic_id
    }
    data = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    data["card"]["card"] = json.loads(data["card"]["card"])
    data["card"]["extend_json"] = json.loads(data["card"]["extend_json"])
    return data["card"]


def get_reposts_raw(dynamic_id: int, offset: str = "0", verify: utils.Verify = None):
    """
    低层级API，获取动态转发列表
    :param dynamic_id: 动态ID
    :param offset: 偏移值（下一页的第一个动态ID）
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["dynamic"]["info"]["repost"]
    resp = utils.get(url=api["url"], params={"dynamic_id": dynamic_id, "offset": offset}, cookies=verify.get_cookies())
    return resp


def get_reposts(dynamic_id: int, limit: int = 114514, callback=None, verify: utils.Verify = None):
    """
    自动循环获取动态转发列表
    :param callback: 回调函数
    :param dynamic_id: 动态ID
    :param limit: 限制数量，注意b站API有获取数量限制，大概在560个左右就获取不到了
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    offset = ""
    reposts = []
    count = 0
    while count < limit:
        data = get_reposts_raw(dynamic_id, offset, verify)
        if "items" not in data:
            break
        items = data["items"]
        count += len(items)
        for i in items:
            i["card"] = json.loads(i["card"])
            i["extend_json"] = json.loads(i["extend_json"])
        reposts += items
        if callable(callback):
            callback(items)
        if "offset" not in data:
            break
        offset = data["offset"]
    return reposts[:limit]


def get_replies_raw(dynamic_id: int, type_: int, pn: int = 1, sort: int = 0, verify: utils.Verify = None):
    """
    低层级API，获取动态评论
    :param dynamic_id: 动态ID（画册动态和文字动态要求不同，画册动态ID较短，文字动态ID较长）
    :param type_: 动态类型，11画册17文字
    :param pn: 页码
    :param sort: 排序方式 2按热度0按时间
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["dynamic"]["info"]["reply"]
    params = {
        "pn": pn,
        "type": type_,
        "oid": dynamic_id,
        "sort": sort
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_replies(dynamic_id: int, limit: int = 114514, order: str = "time", callback=None, verify: utils.Verify = None):
    """
    自动循环获取动态评论列表
    :param callback: 回调函数
    :param dynamic_id: 动态ID
    :param limit: 限制
    :param order: 排序方式，"time"按时间，"like"按热度
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    ORDER_MAP = {
        "time": 0,
        "like": 2
    }
    order = ORDER_MAP.get(order, None)
    if order is None:
        raise exceptions.BilibiliApiException("不支持的排序方式")

    dy_info = get_info(dynamic_id)
    TYPE_MAP = {
        2: 11,
        4: 17
    }
    type_ = TYPE_MAP.get(dy_info["desc"]["type"], 17)
    rid = dy_info["desc"]["rid"] if type_ == 11 else dynamic_id
    replies = []
    count = 0
    page = 1
    while count < limit:
        resp = get_replies_raw(rid, type_, page, order, verify)
        if resp["replies"] is None:
            break
        count += len(resp["replies"])
        replies += resp["replies"]
        if callable(callback):
            callback(resp["replies"])
        page += 1
    return replies[:limit]


# 动态操作

def set_like(dynamic_id: int, status: bool = True, verify: utils.Verify = None):
    """
    设置动态点赞状态
    :param dynamic_id: 动态ID
    :param status: 点赞状态
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["dynamic"]["operate"]["like"]
    self_uid = user.get_self_info(verify)["mid"]
    data = {
        "dynamic_id": dynamic_id,
        "up": 1 if status else 2,
        "uid": self_uid
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def reply(text: str, dynamic_id: int, verify: utils.Verify = None):
    """
    回复动态
    :param text: 内容
    :param dynamic_id: 动态ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["dynamic"]["operate"]["reply"]
    dy_info = get_info(dynamic_id)
    TYPE_MAP = {
        2: 11,
        4: 17
    }
    type_ = TYPE_MAP.get(dy_info["desc"]["type"], 17)
    rid = dy_info["desc"]["rid"] if type_ == 11 else dynamic_id
    data = {
        "oid": rid,
        "type": type_,
        "message": text,
        "plat": 1,
        "csrf": verify.csrf
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def delete(dynamic_id: int, verify: utils.Verify = None):
    """
    删除动态
    :param dynamic_id: 动态ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["dynamic"]["operate"]["delete"]
    data = {
        "dynamic_id": dynamic_id
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def repost(dynamic_id: int, text: str = "转发动态", verify: utils.Verify = None):
    """
    转发动态
    :param text: 转发内容
    :param dynamic_id:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["dynamic"]["operate"]["repost"]
    data = {
        "dynamic_id": dynamic_id,
        "content": text,
        "extension": "{\"emoji_type\":1}",
        "csrf_token": verify.csrf
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def operate_comment(dynamic_id: int, rpid: int, mode: str, status: bool = True, verify: utils.Verify = None):
    """
    操作动态评论，和视频评论用的同一个API
    :param dynamic_id: 动态ID
    :param rpid: 评论id
    :param mode: 评论操作，like, hate, top, del
    :param status: 操作状态，如当status为like时，True点赞，False取消点赞，其他以此类推，del不支持
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])
    mode = mode.lower()

    # 和视频评论用的一个API
    api = API["video"]["operate"].get(mode + "_comment", None)
    if api is None:
        raise exceptions.BilibiliApiException("不支持的评论操作，支持的值：like, hate, top, del")
    dy_info = get_info(dynamic_id)
    TYPE_MAP = {
        2: 11,
        4: 17
    }
    type_ = TYPE_MAP.get(dy_info["desc"]["type"], 17)
    rid = dy_info["desc"]["rid"] if type_ == 11 else dynamic_id
    data = {
        "rpid": rpid,
        "oid": rid,
        "type": type_,
        "csrf": verify.csrf
    }
    if mode != "del":
        data["action"] = 1 if status else 0,
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp
