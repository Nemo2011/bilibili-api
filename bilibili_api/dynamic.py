r"""
模块： dynamic
功能： 动态发送、操作、信息获取等
项目GitHub地址：https://github.com/Passkou/bilibili_api
项目主页：https://passkou.com/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""
import bilibili_api.common
from . import user, exceptions, utils
import re
import json
import datetime

API = utils.get_api()


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
        try:
            user_info = user.get_user_info(int(uid))
        except exceptions.BilibiliException as e:
            if e.code == -404:
                raise exceptions.BilibiliApiException(f"用户uid={uid}不存在")
            else:
                raise e
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
    images_info = []
    for path in images_path:
        i = utils.upload_image(path, verify)
        images_info.append(i)

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


def get_reposts_r(dynamic_id: int, verify: utils.Verify = None):
    """
    自动循环获取动态转发列表
    :param dynamic_id: 动态ID
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    offset = ""
    while True:
        data = get_reposts_raw(dynamic_id, offset, verify)
        if "items" not in data:
            break
        items = data["items"]
        for i in items:
            i["card"] = json.loads(i["card"])
            i["extend_json"] = json.loads(i["extend_json"])
            yield i
        if "offset" not in data:
            break
        offset = data["offset"]


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
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["dynamic"]["operate"]["like"]
    self_uid = user.get_self_info(verify)["mid"]
    data = {
        "dynamic_id": dynamic_id,
        "up": 1 if status else 2,
        "uid": self_uid,
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
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["dynamic"]["operate"]["delete"]
    data = {
        "dynamic_id": dynamic_id,
        "csrf": verify.csrf
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


TYPE_MAP = {
    2: "dynamic_draw",
    4: "dynamic_text"
}


def __get_type_and_rid(dynamic_id: int):
    dy_info = get_info(dynamic_id)
    type_ = TYPE_MAP.get(dy_info["desc"]["type"], TYPE_MAP[4])
    rid = dy_info["desc"]["rid"] if type_ == "dynamic_draw" else dynamic_id
    return type_, rid

# 评论相关


def get_comments_g(dynamic_id: int, order: str = "time", verify: utils.Verify = None):
    """
    获取评论
    :param dynamic_id:
    :param order:
    :param verify:
    :return:
    """
    type_, rid = __get_type_and_rid(dynamic_id)
    replies = bilibili_api.common.get_comments(rid, type_, order, verify)
    return replies


def get_sub_comments_g(dynamic_id: int, root: int, verify: utils.Verify = None):
    """
    获取评论下的评论
    :param dynamic_id: 动态ID
    :param root: 根评论ID
    :param verify:
    :return:
    """
    type_, rid = __get_type_and_rid(dynamic_id)
    return bilibili_api.common.get_sub_comments(rid, type_, root, verify=verify)


def send_comment(text: str, dynamic_id: int, root: int = None, parent: int = None,
                 verify: utils.Verify = None):
    """
    发送评论
    :param dynamic_id:
    :param parent: 回复谁的评论的rpid（若不填则对方无法收到回复消息提醒）
    :param root: 根评论rpid，即在哪个评论下面回复
    :param text: 评论内容，为回复评论时不会自动使用`回复 @%用户名%：%回复内容%`这种格式，目前没有发现根据rpid获取评论信息的API
    :param verify:
    :return:
    """
    type_, rid = __get_type_and_rid(dynamic_id)
    resp = bilibili_api.common.send_comment(text, rid, type_, root, parent, verify=verify)
    return resp


def set_like_comment(rpid: int, dynamic_id: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论点赞状态
    :param dynamic_id:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    type_, rid = __get_type_and_rid(dynamic_id)
    resp = bilibili_api.common.operate_comment("like", rid, type_, rpid, status, verify=verify)
    return resp


def set_hate_comment(rpid: int, dynamic_id: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论点踩状态
    :param dynamic_id:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    type_, rid = __get_type_and_rid(dynamic_id)
    resp = bilibili_api.common.operate_comment("hate", rid, type_, rpid, status, verify=verify)
    return resp


def set_top_comment(rpid: int, dynamic_id: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论置顶状态
    :param dynamic_id:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    type_, rid = __get_type_and_rid(dynamic_id)
    resp = bilibili_api.common.operate_comment("top", rid, type_, rpid, status, verify=verify)
    return resp


def del_comment(rpid: int, dynamic_id: int, verify: utils.Verify = None):
    """
    删除评论
    :param dynamic_id:
    :param rpid:
    :param verify:
    :return:
    """
    type_, rid = __get_type_and_rid(dynamic_id)
    resp = bilibili_api.common.operate_comment("del", rid, type_, rpid, verify=verify)
    return resp


# 评论相关结束


"""
希望の花、繋いだ絆を　♪
ーー「フリージア」
ₘₙⁿ
▏n
█▏　､⺍
█▏ ⺰ʷʷｨ
█◣▄██◣
◥██████▋
　◥████ █▎
　　███▉ █▎
　◢████◣⌠ₘ℩
　　██◥█◣\≫
　　██　◥█◣
　　█▉　　█▊
　　█▊　　█▊
　　█▊　　█▋
　　 █▏　　█▙
　　 █
在代码里也停不下来的团长是鉴（确信）
"""