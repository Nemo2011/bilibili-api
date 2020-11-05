r"""
模块： audio
功能： 音频区的各种操作
项目GitHub地址：https://github.com/Passkou/bilibili_api
项目主页：https://passkou.com/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""

from . import utils, exceptions, common, user

API = utils.get_api()


"""
音频区域
"""


def get_info(auid: int = None, verify: utils.Verify = None):
    """
    获取音频信息
    :param auid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["audio"]["audio_info"]["info"]
    params = {
        "sid": auid
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_tags(auid: int = None, verify: utils.Verify = None):
    """
    获取音频tags
    :param auid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["audio"]["audio_info"]["tag"]
    params = {
        "sid": auid
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_user_info(uid: int = None, verify: utils.Verify = None):
    """
    获取用户数据（收听数，粉丝数等）
    :param uid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["audio"]["audio_info"]["user"]
    params = {
        "uid": uid
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_download_url(auid: int = None, verify: utils.Verify = None):
    """
    获取音频下载链接
    :param auid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["audio"]["audio_info"]["download_url"]
    params = {
        "sid": auid,
        "privilege": 2,
        "quality": 2
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_favorite_list(auid: int, verify: utils.Verify = None):
    """
    获取收藏夹列表供收藏操作用
    :param auid:
    :param verify:
    :return:
    """
    resp = common.get_favorite_list(rid=auid, type_="audio", verify=verify)
    return resp


# 音频操作


def add_coins(auid: int = None, num: int = 2, verify: utils.Verify = None):
    """
    投币
    :param num: 投币数量，最多2
    :param auid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])
    if num not in (1, 2):
        raise exceptions.BilibiliApiException("投币数量只能是1个或2个")

    api = API["audio"]["audio_operate"]["coin"]
    data = {
        "sid": auid,
        "multiply": num,
        "csrf": verify.csrf
    }
    self_info = user.get_self_info(verify)
    cookies = verify.get_cookies()
    cookies["DedeUserID"] = str(self_info["mid"])
    resp = utils.post(url=api["url"], data=data, cookies=cookies)
    return resp


def operate_favorite(auid: int, add_media_ids: list = None,
                     del_media_ids: list = None, verify: utils.Verify = None):
    """
    操作音频收藏夹
    :param auid:
    :param add_media_ids:
    :param del_media_ids:
    :param verify:
    :return:
    """
    resp = common.operate_favorite(auid, "audio", add_media_ids, del_media_ids, verify)
    return resp


def share_to_dynamic(auid: int, content: str, verify: utils.Verify):
    """
    分享歌曲到动态
    :param amid:
    :param content:
    :param verify:
    :return:
    """
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    resp = common.dynamic_share(rid=auid, type_="audio", content=content, verify=verify)
    return resp

# 评论相关


def get_comments_g(auid: int, order: str = "time", verify: utils.Verify = None):
    """
    获取评论
    :param auid: 音频ID
    :param order:
    :param verify:
    :return:
    """
    replies = common.get_comments(auid, "audio", order, verify)
    return replies


def get_sub_comments_g(auid: int, root: int, verify: utils.Verify = None):
    """
    获取评论下的评论
    :param auid:
    :param root: 根评论ID
    :param verify:
    :return:
    """
    return common.get_sub_comments(auid, "audio", root, verify=verify)


def send_comment(text: str, auid: int,  root: int = None, parent: int = None,
                 verify: utils.Verify = None):
    """
    发送评论
    :param auid:
    :param parent: 回复谁的评论的rpid（若不填则对方无法收到回复消息提醒）
    :param root: 根评论rpid，即在哪个评论下面回复
    :param text: 评论内容，为回复评论时不会自动使用`回复 @%用户名%：%回复内容%`这种格式，目前没有发现根据rpid获取评论信息的API
    :param verify:
    :return:
    """
    resp = common.send_comment(text, auid, "audio", root, parent, verify=verify)
    return resp


def set_like_comment(rpid: int, auid: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论点赞状态
    :param auid:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    resp = common.operate_comment("like", auid, "audio", rpid, status, verify=verify)
    return resp


def set_hate_comment(rpid: int, auid: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论点踩状态
    :param auid:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    resp = common.operate_comment("hate", auid, "audio", rpid, status, verify=verify)
    return resp


def set_top_comment(rpid: int, auid: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论置顶状态
    :param auid:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    resp = common.operate_comment("top", auid, "audio", rpid, status, verify=verify)
    return resp


def del_comment(rpid: int, auid: int, verify: utils.Verify = None):
    """
    删除评论
    :param auid:
    :param rpid:
    :param verify:
    :return:
    """
    resp = common.operate_comment("del", auid, "audio", rpid, verify=verify)
    return resp


# 评论相关结束


"""
歌单区域
"""


# 评论相关


def list_get_comments_g(amid: int, order: str = "time", verify: utils.Verify = None):
    """
    获取评论
    :param amid: 歌单ID
    :param order:
    :param verify:
    :return:
    """
    replies = common.get_comments(amid, "audio_list", order, verify)
    return replies


def list_get_sub_comments_g(amid: int, root: int, verify: utils.Verify = None):
    """
    获取评论下的评论
    :param amid: 歌单ID
    :param root: 根评论ID
    :param verify:
    :return:
    """
    return common.get_sub_comments(amid, "audio_list", root, verify=verify)


def list_send_comment(text: str, amid: int,  root: int = None, parent: int = None,
                 verify: utils.Verify = None):
    """
    发送评论
    :param amid:
    :param parent: 回复谁的评论的rpid（若不填则对方无法收到回复消息提醒）
    :param root: 根评论rpid，即在哪个评论下面回复
    :param text: 评论内容，为回复评论时不会自动使用`回复 @%用户名%：%回复内容%`这种格式，目前没有发现根据rpid获取评论信息的API
    :param verify:
    :return:
    """
    resp = common.send_comment(text, amid, "audio_list", root, parent, verify=verify)
    return resp


def list_set_like_comment(rpid: int, amid: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论点赞状态
    :param amid:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    resp = common.operate_comment("like", amid, "audio_list", rpid, status, verify=verify)
    return resp


def list_set_hate_comment(rpid: int, amid: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论点踩状态
    :param amid:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    resp = common.operate_comment("hate", amid, "audio_list", rpid, status, verify=verify)
    return resp


def list_set_top_comment(rpid: int, amid: int, status: bool = True, verify: utils.Verify = None):
    """
    设置评论置顶状态
    :param amid:
    :param rpid:
    :param status: 状态
    :param verify:
    :return:
    """
    resp = common.operate_comment("top", amid, "audio_list", rpid, status, verify=verify)
    return resp


def list_del_comment(rpid: int, amid: int, verify: utils.Verify = None):
    """
    删除评论
    :param amid:
    :param rpid:
    :param verify:
    :return:
    """
    resp = common.operate_comment("del", amid, "audio_list", rpid, verify=verify)
    return resp

# 评论相关结束


def list_get_info(amid: int = None, verify: utils.Verify = None):
    """
    获取歌单信息
    :param amid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["audio"]["list_info"]["info"]
    params = {
        "sid": amid
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def list_get_tags(amid: int = None, verify: utils.Verify = None):
    """
    获取歌单tags
    :param amid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["audio"]["list_info"]["tag"]
    params = {
        "sid": amid
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def list_get_song_list_raw(amid: int = None, pn: int = 1, ps: int = 100, verify: utils.Verify = None):
    """
    低层级API获取歌单歌曲列表
    :param ps: 每页数量默认100
    :param pn: 页码
    :param amid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()

    api = API["audio"]["list_info"]["song_list"]
    params = {
        "sid": amid,
        "pn": pn,
        "ps": ps
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def list_get_song_list_g(amid: int = None, verify: utils.Verify = None):
    """
    循环获取歌单歌曲列表
    :param amid:
    :param verify:
    :return:
    """
    page = 1

    while True:
        resp = list_get_song_list_raw(amid, page, 100, verify)
        if resp is None:
            break
        for r in resp["data"]:
            yield r
        page += 1


def list_set_favorite(amid: int, status=True, verify: utils.Verify = None):
    """
    删除评论
    :param status:
    :param amid:
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])
    self_info = user.get_self_info(verify)
    cookies = verify.get_cookies()
    cookies["DedeUserID"] = str(self_info["mid"])
    if status:
        api = API["audio"]["list_operate"]["set_favorite"]
        data = {
            "sid": amid,
            "csrf": verify.csrf
        }
        resp = utils.post(url=api["url"], data=data, cookies=cookies)
    else:
        api = API["audio"]["list_operate"]["del_favorite"]
        data = {
            "csrf": verify.csrf
        }
        params = {
            "sid": amid
        }
        resp = utils.delete(url=api["url"], params=params, data=data, cookies=cookies)
    return resp


def list_share_to_dynamic(amid: int, content: str, verify: utils.Verify):
    """
    分享歌单到动态
    :param amid:
    :param content:
    :param verify:
    :return:
    """
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    info = list_get_info(amid, verify)
    resp = common.dynamic_share(rid=amid, type_="custom", title=info["title"], cover_url=info["cover"],
                                target_url=f"https://www.bilibili.com/audio/am{amid}", content=content, verify=verify)
    return resp