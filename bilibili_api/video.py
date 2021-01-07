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
import os
import base64
import aiohttp
import math
import asyncio
import logging
import websockets
import struct

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


def get_download_url(bvid: str = None, aid: int = None, page: int = 0,
                     verify: utils.Verify = None):
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
            data = json.loads(text)
            if data['code'] != 0:
                raise exceptions.BilibiliException(data['code'], data['messsage'])
            playurl = data['data']
        else:
            page_id = video_info["pages"][page]["cid"]
            url = API["video"]["info"]["playurl"]["url"]
            params = {
                "bvid": bvid,
                "avid": aid,
                "qn": 120,
                "cid": page_id,
                "otype": 'json',
                "fnval": 16
            }
            playurl = utils.get(url=url, params=params, cookies=verify.get_cookies())
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

# 弹幕相关


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
    api = API["video"]["danmaku"]["get_danmaku"] if date is None else API["video"]["danmaku"]["get_history_danmaku"]
    info = get_video_info(aid=aid, bvid=bvid, verify=verify)
    page_id = info["pages"][page]["cid"]
    params = {
        "oid": page_id,
        "type": 1,
        "segment_index": 1
    }
    if date is not None:
        params["date"] = date.strftime("%Y-%m-%d")
        params["type"] = 1
    req = requests.get(api["url"], params=params, headers=utils.DEFAULT_HEADERS, cookies=verify.get_cookies())
    if req.ok:
        content_type = req.headers['content-type']
        if content_type == 'application/json':
            con = req.json()
            if con['code'] != 0:
                raise exceptions.BilibiliException(con['code'], con['message'])
            else:
                return con
        elif content_type == 'application/octet-stream':
            # 解析二进制流数据
            con = req.content
            data = con
            danmakus = []
            offset = 0
            if data == b'\x10\x01':
                raise exceptions.BilibiliApiException(bvid + '视频弹幕已关闭')
            while offset < len(data):
                if data[offset] == 0x0a:
                    dm = utils.Danmaku('')
                    danmakus.append(dm)
                    offset += 1
                    dm_data_length, l = utils.read_varint(data[offset:])
                    offset += l
                    real_data = data[offset:offset+dm_data_length]
                    dm_data_offset = 0

                    while dm_data_offset < dm_data_length:
                        data_type = real_data[dm_data_offset] >> 3
                        dm_data_offset += 1
                        if data_type == 1:
                            d, l = utils.read_varint(real_data[dm_data_offset:])
                            dm_data_offset += l
                            dm.id = d
                        elif data_type == 2:
                            d, l = utils.read_varint(real_data[dm_data_offset:])
                            dm_data_offset += l
                            dm.dm_time = datetime.timedelta(seconds=d / 1000)
                        elif data_type == 3:
                            d, l = utils.read_varint(real_data[dm_data_offset:])
                            dm_data_offset += l
                            dm.mode = d
                        elif data_type == 4:
                            d, l = utils.read_varint(real_data[dm_data_offset:])
                            dm_data_offset += l
                            dm.font_size = d
                        elif data_type == 5:
                            d, l = utils.read_varint(real_data[dm_data_offset:])
                            dm_data_offset += l
                            dm.color = utils.Color()
                            dm.color.set_dec_color(d)
                        elif data_type == 6:
                            str_len = real_data[dm_data_offset]
                            dm_data_offset += 1
                            d = real_data[dm_data_offset:dm_data_offset + str_len]
                            dm_data_offset += str_len
                            dm.crc32_id = d.decode()
                        elif data_type == 7:
                            str_len = real_data[dm_data_offset]
                            dm_data_offset += 1
                            d = real_data[dm_data_offset:dm_data_offset + str_len]
                            dm_data_offset += str_len
                            dm.text = d.decode(errors='ignore')
                        elif data_type == 8:
                            d, l = utils.read_varint(real_data[dm_data_offset:])
                            dm_data_offset += l
                            dm.send_time = datetime.datetime.fromtimestamp(d)
                        elif data_type == 9:
                            d, l = utils.read_varint(real_data[dm_data_offset:])
                            dm_data_offset += l
                            dm.weight = d
                        elif data_type == 10:
                            d, l = utils.read_varint(real_data[dm_data_offset:])
                            dm_data_offset += l
                            dm.action = d
                        elif data_type == 11:
                            d, l = utils.read_varint(real_data[dm_data_offset:])
                            dm_data_offset += l
                            dm.pool = d
                        elif data_type == 12:
                            str_len = real_data[dm_data_offset]
                            dm_data_offset += 1
                            d = real_data[dm_data_offset:dm_data_offset + str_len]
                            dm_data_offset += str_len
                            dm.id_str = d.decode()
                        elif data_type == 13:
                            d, l = utils.read_varint(real_data[dm_data_offset:])
                            dm_data_offset += l
                            dm.attr = d
                        else:
                            break
                    offset += dm_data_length
            return danmakus
        elif content_type == 'text/xml':
            # 解析XML数据
            con = req.content.decode("utf-8")
            xml = parseString(con)
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
    api = API["video"]["danmaku"]["get_history_danmaku_index"]
    params = {
        "oid": page_id,
        "month": date.strftime("%Y-%m"),
        "type": 1
    }
    get = utils.get(url=api["url"], params=params, cookies=verify.get_cookies())
    return get


def like_danmaku(dmid: int, oid: int, is_like: bool = True, verify: utils.Verify = None):
    """
    点赞弹幕
    :param dmid: 弹幕ID
    :param oid: 分P id，又称cid
    :param is_like: 点赞/取消点赞
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])
    if not verify.has_csrf():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_csrf"])

    api = API['video']['danmaku']['like_danmaku']
    payload = {
        "dmid": dmid,
        "oid": oid,
        "op": 1 if is_like else 2,
        "platform": "web_player",
        "csrf": verify.csrf
    }
    resp = utils.post(api["url"], cookies=verify.get_cookies(), data=payload)
    return resp


def has_liked_danmaku(dmid, oid: int, verify: utils.Verify = None):
    """
    是否已点赞弹幕
    :param dmid: 弹幕id，为list时同时查询多个弹幕，为int时只查询一条弹幕
    :param oid: 分P id，又称cid
    :param verify:
    :return:
    """
    if verify is None:
        verify = utils.Verify()
    if not verify.has_sess():
        raise exceptions.NoPermissionException(utils.MESSAGES["no_sess"])

    api = API['video']['danmaku']['has_liked_danmaku']
    params = {
        "ids": dmid if type(dmid) == int else ",".join(list(map(lambda id_: str(id_), dmid))) if type(dmid) == list else None,
        "oid": oid,
    }
    if params['ids'] is None:
        raise exceptions.BilibiliApiException("参数错误")
    resp = utils.get(api["url"], cookies=verify.get_cookies(), params=params)
    return resp


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
    api = API["video"]["danmaku"]["send_danmaku"]
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


# 评论相关


def get_comments_g(bvid: str = None, aid: int = None, order: str = "time", verify: utils.Verify = None):
    """
    获取评论
    :param order:
    :param aid:
    :param bvid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)

    replies = common.get_comments(aid, "video", order, verify)
    return replies


def get_sub_comments_g(root: int, bvid: str = None, aid: int = None, verify: utils.Verify = None):
    """
    获取评论下的评论
    :param root: 根评论ID
    :param bvid:
    :param aid:
    :param verify:
    :return:
    """
    if not (aid or bvid):
        raise exceptions.NoIdException
    if aid is None:
        aid = utils.bvid2aid(bvid)
    return common.get_sub_comments(aid, "video", root, verify=verify)


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


# 视频上传三步

def video_upload(path: str, verify: utils.Verify, on_progress=None):
    """
    上传视频
    :param on_progress: 进度回调，数据格式：{"event": "事件名", "ok": "是否成功", "data": "附加数据"}
                        事件名：PRE_UPLOAD，GET_UPLOAD_ID，UPLOAD_CHUNK，VERIFY
    :param path: 视频路径
    :param verify:
    :return: 该视频的filename，用于后续提交投稿用
    """
    if on_progress is not None and not callable(on_progress):
        raise exceptions.BilibiliApiException("on_progress 参数必须是个方法")
    session = requests.session()
    session.headers = utils.DEFAULT_HEADERS
    requests.utils.add_dict_to_cookiejar(session.cookies, verify.get_cookies())
    if not os.path.exists(path):
        raise exceptions.UploadException("视频路径不存在")
    total_size = os.stat(path).st_size
    # 上传设置
    params = {
        'name': os.path.basename(path),
        'size': total_size,
        'r': 'upos',
        'profile': 'ugcupos/bup'
    }
    try:
        resp = session.get('https://member.bilibili.com/preupload', params=params)
        settings = resp.json()
        upload_url = 'https:' + settings['endpoint'] + '/' + settings['upos_uri'].replace('upos://', '')
        headers = {
            'X-Upos-Auth': settings['auth']
        }
        if on_progress:
            on_progress({"event": "PRE_UPLOAD", "ok": True, "data": None})
    except Exception as e:
        if on_progress:
            on_progress({"event": "PRE_UPLOAD", "ok": False, "data": e})
        raise e
    try:
        resp = session.post(upload_url + "?uploads&output=json", headers=headers)
        settings['upload_id'] = resp.json()['upload_id']
        filename = os.path.splitext(resp.json()['key'].lstrip('/'))[0]
        if on_progress:
            on_progress({"event": "GET_UPLOAD_ID", "ok": True, "data": None})
    except Exception as e:
        if on_progress:
            on_progress({"event": "GET_UPLOAD_ID", "ok": False, "data": e})
        raise e
    # 分配任务
    chunks_settings = []
    i = 0
    total_chunks = math.ceil(total_size / settings['chunk_size'])
    offset = 0
    remain = total_size
    while True:
        s = {
            'partNumber': i + 1,
            'uploadId': settings['upload_id'],
            'chunk': i,
            'chunks': total_chunks,
            'start': offset,
            'end': offset + settings['chunk_size'] if remain >= settings['chunk_size'] else total_size,
            'total': total_size
        }
        s['size'] = s['end'] - s['start']
        chunks_settings.append(s)
        i += 1
        offset = s['end']
        remain -= settings['chunk_size']
        if remain <= 0:
            break

    async def upload(chunks, sess):
        failed_chunks = []
        with open(path, 'rb') as f:
            for chunk in chunks:
                f.seek(chunk['start'], 0)
                async with sess.put(upload_url, params=chunk, data=f.read(chunk['size']), headers=utils.DEFAULT_HEADERS) as r:
                    if r.status != 200:
                        if on_progress:
                            on_progress({"event": "UPLOAD_CHUNK", "ok": False, "data": chunk})
                        failed_chunks.append(chunk)
                    else:
                        if on_progress:
                            on_progress({"event": "UPLOAD_CHUNK", "ok": True, "data": chunk})
        return failed_chunks

    async def main():
        chunks_per_thread = len(chunks_settings) // settings['threads']
        remain = len(chunks_settings) % settings['threads']
        task_chunks = []
        for i in range(settings['threads']):
            this_task_chunks = chunks_settings[i*chunks_per_thread:(i+1)*chunks_per_thread]
            task_chunks.append(this_task_chunks)
        task_chunks[-1] += (chunks_settings[-remain:])

        async with aiohttp.ClientSession(headers={'X-Upos-Auth': settings['auth']}, cookies=verify.get_cookies()) as sess:
            while True:
                # 循环上传
                coroutines = []
                chs = task_chunks
                for chunks in chs:
                    coroutines.append(upload(chunks, sess))
                results = await asyncio.gather(*coroutines)
                failed_chunks = []
                for result in results:
                    failed_chunks += result
                chs = failed_chunks
                if len(chs) == 0:
                    break
            # 验证是否上传成功
            params = {
                'output': 'json',
                'name': os.path.basename(path),
                'profile': 'ugcupos/bup',
                'uploadId': settings['upload_id'],
                'biz_id': settings['biz_id']
            }
            payload = {
                'parts': []
            }
            for chunk in chunks_settings:
                payload['parts'].append({
                    'eTag': 'eTag',
                    'partNumber': chunk['partNumber']
                })
            async with sess.post(upload_url, params=params, data=payload) as resp:
                result = await resp.read()
                result = json.loads(result)
                ok = result.get('OK', 0)
                if ok == 1:
                    if on_progress:
                        on_progress({"event": "VERIFY", "ok": True, "data": None})
                    return filename
                else:
                    if on_progress:
                        on_progress({"event": "VERIFY", "ok": False, "data": None})
                    raise exceptions.UploadException('视频上传失败')

    r = asyncio.get_event_loop().run_until_complete(main())
    return r


def video_cover_upload(path, verify: utils.Verify):
    """
    封面上传
    :param path:
    :param verify:
    :return: 封面URL，用于提交投稿信息用
    """
    if not os.path.exists(path):
        raise exceptions.UploadException('封面路径不存在')
    with open(path, 'rb') as f:
        filename = os.path.basename(path)
        if filename.endswith('.jpg') or filename.endswith('.jpeg'):
            mime = 'image/jpeg'
        elif filename.endswith('.png'):
            mime = 'image/png'
        elif filename.endswith('.gif'):
            mime = 'image/gif'
        data_url = f'data:{mime};base64,{base64.b64encode(f.read()).decode()}'
        payload = {
            'cover': data_url,
            'csrf': verify.csrf
        }
        resp = utils.post('https://member.bilibili.com/x/vu/web/cover/up', data=payload,
                          cookies=verify.get_cookies())
        cover_url = resp['url']
    return cover_url


def video_submit(data: dict, verify: utils.Verify):
    """
    提交投稿信息
    :param data: 投稿信息
    {
        "copyright": 1自制2转载,
        "source": "类型为转载时注明来源",
        "cover": "封面URL",
        "desc": "简介",
        "desc_format_id": 0,
        "dynamic": "动态信息",
        "interactive": 0,
        "no_reprint": 1为显示禁止转载,
        "subtitles": {
            // 字幕格式，请自行研究
            "lan": "语言",
            "open": 0
        },
        "tag": "标签1,标签2,标签3（英文半角逗号分隔）",
        "tid": 分区ID,
        "title": "标题",
        "videos": [
            {
                "desc": "描述",
                "filename": "video_upload(返回值)",
                "title": "分P标题"
            }
        ]
    }
    :param verify:
    :return:
    """
    url = "https://member.bilibili.com/x/vu/web/add"
    params = {
        "csrf": verify.csrf
    }
    payload = json.dumps(data, ensure_ascii=False).encode()
    resp = utils.post(url, params=params, data=payload, data_type="json", cookies=verify.get_cookies())
    return resp


def connect_all_VideoOnlineMonitor(*args):
    async def main():
        coroutines = []
        for a in args:
            coroutines.append(a.connect(True))
        await asyncio.gather(*coroutines)
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()


# 实时监控在线人数/在线弹幕
class VideoOnlineMonitor:
    DATAPACK_CLIENT_VERIFY = 0x7
    DATAPACK_SERVER_VERIFY = 0x8
    DATAPACK_CLIENT_HEARTBEAT = 0x2
    DATAPACK_SERVER_HEARTBEAT = 0x3
    DATAPACK_DANMAKU = 0x3e8

    def __init__(self, bvid: str = None, aid: int = None, page: int = 0, event_handler=None, debug: bool = False,
                 should_reconnect: bool = True):
        self.event_handler = event_handler
        """
        事件type：
        ONLINE： 在线人数更新
        DANMAKU： 收到实时弹幕
        DISCONNECT： 断开连接（传入连接状态码参数）
        """
        if bvid is not None:
            self.bvid = bvid
            self.aid = utils.bvid2aid(bvid)
        elif aid is not None:
            self.bvid = utils.aid2bvid(aid)
            self.aid = aid
        else:
            raise exceptions.BilibiliApiException('bvid和aid必须提供其中之一')
        # logger初始化
        self.logger = logging.getLogger(f'VideoOnlineMonitor_{bvid}')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[" + str(bvid) + "][%(asctime)s][%(levelname)s] %(message)s"))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO if not debug else logging.DEBUG)
        self.page = page
        self.__next_number = 1
        self.__connected_status = 0
        self.__heart_beat_task = None
        self.should_reconnect = should_reconnect
        self.__is_single_room = False

    def connect(self, return_coroutine: bool = False):
        if return_coroutine:
            self.__is_single_room = False
            return self.__main()
        else:
            self.__is_single_room = True
            asyncio.get_event_loop().run_until_complete(self.__main())
            asyncio.get_event_loop().run_forever()

    def disconnect(self):
        self.__connected_status = 2
        asyncio.create_task(self.__ws.close())

    def get_connect_status(self):
        return self.__connected_status

    async def __main(self):
        # 获取分P id
        pages = get_pages(self.bvid)
        if self.page >= len(pages):
            raise exceptions.BilibiliApiException("分P不存在")
        self.cid = pages[self.page]['cid']

        self.logger.debug(f'准备连接：{self.bvid}')
        self.logger.debug(f'获取服务器信息中')
        resp = utils.get('https://api.bilibili.com/x/web-interface/broadcast/servers?platform=pc')
        uri = f"wss://{resp['domain']}:{resp['wss_port']}/sub"
        self.__heartbeat_interval = resp['heartbeat']
        self.logger.debug(f'服务器信息获取成功，URI：{uri}')

        self.logger.debug('准备连接服务器')
        async with websockets.connect(uri) as ws:
            self.__ws = ws
            self.logger.debug('服务器连接成功，准备发送认证信息')
            verify_info = {
                'room_id': f'video://{self.aid}/{self.cid}',
                'platform': 'web',
                'accepts': [1000, 1015]
            }
            verify_info = json.dumps(verify_info, separators=(',', ':'))
            await ws.send(self.__pack(self.DATAPACK_CLIENT_VERIFY, 1, verify_info.encode()))
            while True:
                try:
                    recv = await ws.recv()
                except websockets.ConnectionClosed:
                    if self.__connected_status != 2:
                        self.logger.warning('连接被异常断开')
                        self.__connected_status = -1
                        if self.should_reconnect:
                            self.logger.info('准备重连')
                            asyncio.create_task(self.connect(True))
                    else:
                        self.logger.info('连接正常断开')
                        if self.__is_single_room:
                            asyncio.get_event_loop().stop()
                    if callable(self.event_handler):
                        self.event_handler({'type': 'DISCONNECT', 'bvid': self.bvid, 'aid': self.aid, 'data': self.__connected_status})
                    if self.__heart_beat_task is not None:
                        self.__heart_beat_task.cancel()
                    break
                data = self.__unpack(recv)
                self.logger.debug(f'收到消息：{data}')
                for d in data:
                    if d['type'] == self.DATAPACK_SERVER_VERIFY:
                        if d['data']['code'] == 0:
                            self.logger.info('连接服务器并验证成功')
                            self.__connected_status = 1
                            self.__heart_beat_task = asyncio.create_task(self.__heartbeat())
                    elif d['type'] == self.DATAPACK_SERVER_HEARTBEAT:
                        self.logger.debug(f'收到服务器心跳包反馈，编号：{d["number"]}')
                        self.logger.info(f'实时观看人数：{d["data"]["data"]["room"]["online"]}')
                        if callable(self.event_handler):
                            self.event_handler({'type': 'ONLINE', 'bvid': self.bvid, 'aid': self.aid, 'data': d['data']['data']})
                    elif d['type'] == self.DATAPACK_DANMAKU:
                        info = d['data'][0].split(",")
                        text = d['data'][1]
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
                        self.logger.info(f'收到实时弹幕：{dm.text}')
                        if callable(self.event_handler):
                            self.event_handler({'type': 'DANMAKU', 'bvid': self.bvid, 'aid': self.aid, 'data': dm})
                    else:
                        self.logger.warning('收到未知的数据包类型，无法解析')

    async def __heartbeat(self):
        while self.__connected_status == 1:
            self.logger.debug(f'发送心跳包，编号：{self.__next_number}')
            try:
                await self.__ws.send(self.__pack(self.DATAPACK_CLIENT_HEARTBEAT, self.__next_number, b'[object Object]'))
            except:
                break
            self.__next_number += 1
            await asyncio.sleep(self.__heartbeat_interval)

    @staticmethod
    def __pack(data_type: int, number: int, data: bytes):
        """
        数据包格式：
        offset(bytes) length(bytes) type data
        0  4  I 数据包长度
        4  4  I 固定0x00120001
        8  4  I 数据包类型
        12 4  I 递增数据包编号
        16 2  H 固定0x0000
        之后是有效载荷
        数据包类型表：
        0x7  客户端发送认证信息
        0x8  服务端回应认证结果
        0x2  客户端发送心跳包，有效载荷：'[object Object]'
        0x3  服务端回应心跳包，会带上在线人数等信息，返回JSON
        0x3e8  实时弹幕更新，返回列表，[0]弹幕信息，[1]弹幕文本
        """
        packed_data = bytearray()
        packed_data += struct.pack('>I', 0x00120001)
        packed_data += struct.pack('>I', data_type)
        packed_data += struct.pack('>I', number)
        packed_data += struct.pack('>H', 0)
        packed_data += data
        packed_data = struct.pack('>I', len(packed_data) + 4) + packed_data
        return bytes(packed_data)

    @staticmethod
    def __unpack(data: bytes):
        offset = 0
        real_data = []
        while offset < len(data):
            region_header = struct.unpack('>IIII', data[:16])
            region_data = data[offset:offset+region_header[0]]
            real_data.append({
                'type': region_header[2],
                'number': region_header[3],
                'data': json.loads(region_data[offset+18:offset+18+(region_header[0]-16)])
            })
            offset += region_header[0]
        return real_data




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
