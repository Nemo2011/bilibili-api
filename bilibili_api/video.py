r"""
模块：video
功能：获取视频各种信息以及操作视频
项目GitHub地址：https://github.com/Passkou/bilibili_api
项目主页：https://passkou.com/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""
from . import exceptions, utils, user, common
import requests
import json
from xml.dom.minidom import parseString
import re
import datetime
import time

API = utils.get_api()


def get_video_info(bvid: str = None, aid: int = None, is_simple: bool = False, verify: utils.Verify = None):
    """
    获取视频信息
    :param aid:
    :param bvid:
    :param is_simple: 简易信息（另一个API）
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()

    if is_simple:
        api = API["video"]["info"]["info_simple"]
    else:
        api = API["video"]["info"]["info_detail"]
    params = {
        "aid": aid,
        "bvid": bvid
    }
    info = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return info


def get_danmaku(bvid: str = None, aid: int = None, page: int = 0,
                verify: utils.Verify = None, date: datetime.date = None):
    """
    获取弹幕
    :param aid:
    :param bvid:
    :param page: 分p数
    :param verify: date不为None时需要SESSDATA验证
    :param date: 为None时获取最新弹幕，为datetime.date时获取历史弹幕
    """

    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()
    if date is not None:
        if not verify.has_sess():
            raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    api = API["video"]["info"]["danmaku"] if date is None else API["video"]["info"]["history_danmaku"]
    info = get_video_info(aid=aid, bvid=bvid, verify=verify)
    page_id = info["pages"][page]["cid"]
    params = {
        "oid": page_id
    }
    if date is not None:
        params["date"] = date.strftime("%Y-%m-%d")
        params["type"] = 1
    req = requests.get(api["url"], params=params, headers=utils.DEFAULT_HEADERS, cookies=verify.get_cookies())
    if req.ok:
        con = req.content.decode("utf-8")
        try:
            xml = parseString(con)
        except Exception:
            j = json.loads(con)
            raise exceptions.BilibiliException(j["code"], j["message"])
        danmaku = xml.getElementsByTagName("d")
        py_danmaku = []
        for d in danmaku:
            info = d.getAttribute("p").split(",")
            text = d.childNodes[0].data
            if info[5] == '0':
                is_sub = False
            else:
                is_sub = True
            dm = utils.Danmaku(
                dm_time=float(info[0]),
                send_time=int(info[4]),
                crc32_id=info[6],
                color=utils.Color(info[3]),
                mode=info[1],
                font_size=info[2],
                is_sub=is_sub,
                text=text
            )
            py_danmaku.append(dm)
        return py_danmaku
    else:
        raise exceptions.NetworkException(req.status_code)


def get_history_danmaku_index(bvid: str = None, aid: int = None, page: int = 0,
                              date: datetime.date = None, verify: utils.Verify = None):
    """
    获取历史弹幕索引
    :param aid:
    :param bvid:
    :param page:
    :param date: 默认为这个月
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()
    if date is None:
        date = datetime.date.fromtimestamp(time.time())
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    info = get_video_info(aid=aid, bvid=bvid, verify=verify)
    page_id = info["pages"][page]["cid"]
    api = API["video"]["info"]["history_danmaku_index"]
    params = {
        "oid": page_id,
        "month": date.strftime("%Y-%m"),
        "type": 1
    }
    get = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return get


def get_tags(bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    获取视频标签
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()

    api = API["video"]["info"]["tags"]
    params = {
        "aid": aid,
        "bvid": bvid
    }
    resp = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return resp


def get_chargers(bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    获取视频充电用户
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()

    api = API["video"]["info"]["charge"]
    info = get_video_info(aid=aid, bvid=bvid, verify=verify)
    mid = info["owner"]["mid"]
    params = {
        "aid": aid,
        "mid": mid,
        "bvid": bvid
    }
    get = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return get


def get_pages(bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    获取视频分P情况
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()

    api = API["video"]["info"]["pages"]
    params = {
        "aid": aid,
        "bvid": bvid
    }
    get = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return get


def get_download_url(bvid: str = None, aid: int = None, page: int = 0, verify: utils.Verify = None):
    """
    获取视频下载链接
    :param aid:
    :param bvid:
    :param page:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()

    video_info = get_video_info(aid=aid, bvid=bvid, verify=verify)
    if page + 1 > len(video_info["pages"]):
        raise exceptions.BilibiliApiException("不存在该分P（page）")
    if bvid is not None:
        url = "https://www.bilibili.com/video/%s" % bvid
    else:
        url = "https://www.bilibili.com/video/av%s" % aid
    req = requests.get(url, cookies=verify.get_cookies(), headers=utils.DEFAULT_HEADERS, params={"p": page + 1})
    if req.ok:
        match = re.search("<script>window.__playinfo__=(.*?)</script>", req.text)
        if match is not None:
            text = match.group(1)
            playurl = json.loads(text)
        elif match is None:
            page_id = video_info["pages"][page]["cid"]
            url = API["video"]["info"]["playurl"]["url"]
            params = {
                "bvid": bvid,
                "avid": aid,
                "qn": 112,
                "cid": page_id
            }
            playurl = utils.get(url=url, params=params, cookies=verify.get_cookies())
        else:
            raise exceptions.BilibiliApiException("无法获取playurl")
        return playurl
    else:
        raise exceptions.NetworkException(req.status_code)


def get_related(bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    获取该视频相关推荐
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()

    api = API["video"]["info"]["related"]
    params = {
        "aid": aid,
        "bvid": bvid
    }
    get = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return get


def get_added_coins(bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    投币数量
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["video"]["info"]["is_coins"]
    params = {
        "aid": aid,
        "bvid": bvid
    }
    get = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    value = get["multiply"]
    return value


def get_favorite_list(bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    获取收藏夹列表供收藏操作用
    :param bvid: 
    :param aid: 
    :param verify: 
    :return: 
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)
    resp = common.get_favorite_list(rid=aid, type_="video", verify=verify)
    return resp


def is_liked(bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    是否点赞视频
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["video"]["info"]["is_liked"]
    params = {
        "aid": aid,
        "bvid": bvid
    }
    get = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    if get == 1:
        return True
    else:
        return False


def is_favoured(bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    是否收藏过
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API["video"]["info"]["is_favoured"]
    if aid is None:
        aid = utils.bvid2aid(bvid)
    params = {
        "aid": aid,
        "bvid": bvid
    }
    get = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    value = get["favoured"]
    return value


# 操作视频


def set_like(status: bool = True, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    点赞
    :param status: True点赞False取消点赞
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API["video"]["operate"]["like"]
    data = {
        "aid": aid,
        "like": 0,
        "csrf": verify.csrf,
        "bvid": bvid
    }
    if status:
        data["like"] = 1
    else:
        data["like"] = 2
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def add_coins(num: int = 1, like: bool = True, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    投币
    :param num: 1或2个
    :param like: 是否同时点赞
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])
    if num not in (1, 2):
        raise exceptions.BilibiliApiException("硬币必须是1个或2个")

    api = API["video"]["operate"]["coin"]
    data = {
        "aid": aid,
        "multiply": num,
        "select_like": 1 if like else 0,
        "csrf": verify.csrf,
        "bvid": bvid
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def operate_favorite(bvid: str = None, aid: int = None, add_media_ids: list = None,
                     del_media_ids: list = None, verify: utils.Verify = None):
    """
    操作音频收藏夹
    :param aid:
    :param bvid:
    :param add_media_ids:
    :param del_media_ids:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)
    resp = common.operate_favorite(aid, "video", add_media_ids, del_media_ids, verify)
    return resp


# 评论相关


def get_comments(bvid: str = None, aid: int = None, order: str = "time", limit: int = 1919810,
                 callback=None, verify: utils.Verify = None):
    """
    获取评论
    :param order:
    :param callback: 回调函数
    :param aid:
    :param bvid:
    :param limit: 限制数量
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)

    replies = common.get_comments(aid, "video", order, limit, callback, verify)
    return replies


def send_comment(text: str, root: int = None, parent: int = None, bvid: str = None, aid: int = None,
                 verify: utils.Verify = None):
    """
    发送评论
    :param parent: 回复谁的评论的rpid（若不填则对方无法收到回复消息提醒）
    :param root: 根评论rpid，即在哪个评论下面回复
    :param text: 评论内容，为回复评论时不会自动使用`回复 @%用户名%：%回复内容%`这种格式，目前没有发现根据rpid获取评论信息的API
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)

    resp = common.send_comment(text, aid, "video", root, parent, verify=verify)
    return resp


def set_like_comment(rpid: int, status: bool = True, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    设置评论点赞状态
    :param rpid:
    :param status: 状态
    :param bvid:
    :param aid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)

    resp = common.operate_comment("like", aid, "video", rpid, status, verify=verify)
    return resp


def set_hate_comment(rpid: int, status: bool = True, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    设置评论点踩状态
    :param rpid:
    :param status: 状态
    :param bvid:
    :param aid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)

    resp = common.operate_comment("hate", aid, "video", rpid, status, verify=verify)
    return resp


def set_top_comment(rpid: int, status: bool = True, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    设置评论置顶状态
    :param rpid:
    :param status: 状态
    :param bvid:
    :param aid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)

    resp = common.operate_comment("top", aid, "video", rpid, status, verify=verify)
    return resp


def del_comment(rpid: int, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    删除评论
    :param rpid:
    :param bvid:
    :param aid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)

    resp = common.operate_comment("del", aid, "video", rpid, verify=verify)
    return resp


# 评论相关结束


def send_danmaku(danmaku: utils.Danmaku, page: int = 0, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    发送弹幕
    :param danmaku: Danmaku类
    :param page: 分p号
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    page_info = get_pages(bvid, aid, verify)
    oid = page_info[page]["cid"]
    api = API["video"]["operate"]["send_danmaku"]
    if danmaku.is_sub:
        pool = 1
    else:
        pool = 0
    data = {
        "type": 1,
        "oid": oid,
        "msg": danmaku.text,
        "aid": aid,
        "bvid": bvid,
        "progress": int(danmaku.dm_time.seconds * 1000),
        "color": danmaku.color.get_dec_color(),
        "fontsize": danmaku.font_size,
        "pool": pool,
        "mode": danmaku.mode,
        "plat": 1,
        "csrf": verify.csrf
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def add_tag(tag_name: str, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    添加标签
    :param tag_name: 标签名
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])
    if aid is None:
        aid = utils.bvid2aid(bvid)

    api = API["video"]["operate"]["add_tag"]
    data = {
        "aid": aid,
        "tag_name": tag_name,
        "csrf": verify.csrf,
        "bvid": bvid
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def del_tag(tag_id: int, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    if not (aid or bvid):
        raise exceptions.NoIdException
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])
    if aid is None:
        aid = utils.bvid2aid(bvid)

    api = API["video"]["operate"]["del_tag"]
    data = {
        "aid": aid,
        "tag_id": tag_id,
        "csrf": verify.csrf,
        "bvid": bvid
    }
    resp = utils.post(url=api["url"], data=data, cookies=verify.get_cookies())
    return resp


def share_to_dynamic(content: str, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    视频分享到动态
    :param aid:
    :param bvid:
    :param content:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)
    resp = common.dynamic_share("video", aid, content, verify=verify)
    return resp


r"""
哼哼哼，啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊

             ▃▆█▇▄▖
　　     　▟◤▖　　　 ◥█▎
　　　◢◤　   ▐　　　　  ▐▉
　▗◤　　　▂　▗▖　　  ▕ █▎
　◤　▗▅▖◥▄　▀◣　  　█▊
▐　▕▎◥▖◣◤　　　　 ◢██
█◣　◥▅█▀　　　　  ▐██◤
▐█▙▂　　　     ◢██◤
　◥██◣　　　　◢▄◤
　　　▀██▅▇▀
"""