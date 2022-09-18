"""
bilibili_api.user

用户相关
"""

from enum import Enum
import json
from json.decoder import JSONDecodeError
import time

from .exceptions import ResponseCodeException

from .utils.sync import sync

from .utils.network_httpx import get_session, request
from .utils.utils import get_api, join
from .utils.Credential import Credential
from typing import List
import httpx

API = get_api("user")


class VideoOrder(Enum):
    """
    视频排序顺序。

    + PUBDATE : 上传日期倒序。
    + FAVORITE: 收藏量倒序。
    + VIEW    : 播放量倒序。
    """

    PUBDATE = "pubdate"
    FAVORITE = "stow"
    VIEW = "click"


class ChannelOrder(Enum):
    """
    合集视频排序顺序。
    + DEFAULT: 默认排序
    + CHANGE : 升序排序
    """

    DEFAULT = "false"
    CHANGE = "true"


class AudioOrder(Enum):
    """
    音频排序顺序。

    + PUBDATE : 上传日期倒序。
    + FAVORITE: 收藏量倒序。
    + VIEW    : 播放量倒序。
    """

    PUBDATE = 1
    VIEW = 2
    FAVORITE = 3


class AlbumType(Enum):
    """
    相册类型

    + ALL : 全部。
    + DRAW: 绘画。
    + PHOTO    : 摄影。
    + DAILY    : 日常。
    """

    ALL = "all"
    DRAW = "draw"
    PHOTO = "photo"
    DAILY = "daily"


class ArticleOrder(Enum):
    """
    专栏排序顺序。

    + PUBDATE : 发布日期倒序。
    + FAVORITE: 收藏量倒序。
    + VIEW    : 阅读量倒序。
    """

    PUBDATE = "publish_time"
    FAVORITE = "fav"
    VIEW = "view"


class ArticleListOrder(Enum):
    """
    文集排序顺序。

    + LATEST: 最近更新倒序。
    + VIEW  : 总阅读量倒序。
    """

    LATEST = 0
    VIEW = 1


class BangumiType(Enum):
    """
    番剧类型。

    + BANGUMI: 番剧。
    + DRAMA  : 电视剧/纪录片等。
    """

    BANGUMI = 1
    DRAMA = 2


class RelationType(Enum):
    """
    用户关系操作类型。

    + SUBSCRIBE         : 关注。
    + UNSUBSCRIBE       : 取关。
    + SUBSCRIBE_SECRETLY: 悄悄关注。
    + BLOCK             : 拉黑。
    + UNBLOCK           : 取消拉黑。
    + REMOVE_FANS       : 移除粉丝。
    """

    SUBSCRIBE = 1
    UNSUBSCRIBE = 2
    SUBSCRIBE_SECRETLY = 3
    BLOCK = 5
    UNBLOCK = 6
    REMOVE_FANS = 7


class User:
    """
    用户相关
    """

    def __init__(self, uid: int, credential: Credential = None):
        """
        Args:
            uid        (int)                 : 用户 UID
            credential (Credential, optional): 凭据. Defaults to None.
        """
        self.__uid = uid

        if credential is None:
            credential = Credential()
        self.credential = credential
        self.__self_info = None

    async def get_user_info(self):
        """
        获取用户信息（昵称，性别，生日，签名，头像 URL，空间横幅 URL 等）

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["info"]
        params = {"mid": self.__uid}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def __get_self_info(self):
        """
        获取自己的信息。如果存在缓存则使用缓存。

        Returns:
            dict: 调用接口返回的内容。
        """
        if self.__self_info is not None:
            return self.__self_info

        self.__self_info = await get_self_info(credential=self.credential)
        return self.__self_info

    def get_uid(self):
        """
        获取用户 uid

        Returns:
            用户 uid
        """
        return self.__uid

    async def get_user_fav_tag(self):
        """
        获取用户关注的 Tag 信息，如果用户设为隐私，则返回 获取登录数据失败

        Returns:
            dict: 调用接口返回的内容。
        """

        # (未打包至 utils 的) 获取被 ajax 重定向后的接口数据
        api = API["info"]["user_tag"]
        params = {"mid": self.__uid}
        if self.credential is None:
            cookies = Credential().get_cookies()
        else:
            cookies = self.credential.get_cookies()
        # cookies["buvid3"] = str(uuid.uuid1())
        cookies["Domain"] = ".bilibili.com"
        sess = get_session()
        resp = await sess.request(
            "GET",
            url=api["url"],
            params=params,
            follow_redirects=True,
            cookies=cookies,
            # credential=self.credential
        )
        try:
            r_json = json.loads(resp.text)
        except JSONDecodeError:
            r_json = {'status': False, 'data': f'解析接口返回的 Json 数据失败:{resp.status_code}'}
        return r_json

    async def get_space_notice(self):
        """
        获取用户空间公告

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["space_notice"]
        params = {"mid": self.__uid}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def set_space_notice(self, content: str = ""):
        """
        修改用户空间公告

        Args:
            content(str): 需要修改的内容

        Returns:
            dict: 调用接口返回的内容。
        """

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["set_space_notice"]
        data = {"notice": content}
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def get_relation_info(self):
        """
        获取用户关系信息（关注数，粉丝数，悄悄关注，黑名单数）

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["relation"]
        params = {"vmid": self.__uid}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_up_stat(self):
        """
        获取 UP 主数据信息（视频总播放量，文章总阅读量，总点赞数）

        Returns:
            dict: 调用接口返回的内容。
        """
        self.credential.raise_for_no_bili_jct()

        api = API["info"]["upstat"]
        params = {"mid": self.__uid}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_live_info(self):
        """
        获取用户直播间信息。

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["live"]
        params = {"mid": self.__uid}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_videos(
        self,
        tid: int = 0,
        pn: int = 1,
        ps: int = 30,
        keyword: str = "",
        order: VideoOrder = VideoOrder.PUBDATE,
    ):
        """
        获取用户投稿视频信息。

        Args:
            tid     (int, optional)       : 分区 ID. Defaults to 0（全部）.
            pn      (int, optional)       : 页码，从 1 开始. Defaults to 1.
            ps      (int, optional)       : 每一页的视频数. Defaults to 30.
            keyword (str, optional)       : 搜索关键词. Defaults to "".
            order   (VideoOrder, optional): 排序方式. Defaults to VideoOrder.PUBDATE

        Returns:
            dict.
        """
        api = API["info"]["video"]
        params = {
            "mid": self.__uid,
            "ps": ps,
            "tid": tid,
            "pn": pn,
            "keyword": keyword,
            "order": order.value,
        }
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_audios(
        self, order: AudioOrder = AudioOrder.PUBDATE, pn: int = 1, ps: int = 30
    ):
        """
        获取用户投稿音频。

        Args:
            order (AudioOrder, optional): 排序方式. Defaults to AudioOrder.PUBDATE.
            pn    (int, optional)       : 页码数，从 1 开始。 Defaults to 1.
            ps      (int, optional)       : 每一页的视频数. Defaults to 30.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["audio"]
        params = {"uid": self.__uid, "ps": ps, "pn": pn, "order": order.value}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_album(
        self, biz: AlbumType = AlbumType.ALL,
        page_num: int = 1,
        page_size: int = 30
    ):
        """
        获取用户投稿音频。

        Args:
            biz (AlbumType, optional): 排序方式. Defaults to AlbumType.ALL.
            page_num      (int, optional)       : 页码数，从 1 开始。 Defaults to 1.
            page_size    (int)       : 每一页的相簿条目. Defaults to 30.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["album"]
        params = {"uid": self.__uid, "page_num": page_num, "page_size": page_size, "biz": biz.value}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_articles(
        self, pn: int = 1, order: ArticleOrder = ArticleOrder.PUBDATE, ps: int = 30
    ):
        """
        获取用户投稿专栏。

        Args:
            order (ArticleOrder, optional): 排序方式. Defaults to ArticleOrder.PUBDATE.
            pn    (int, optional)         : 页码数，从 1 开始。 Defaults to 1.
            ps      (int, optional)       : 每一页的视频数. Defaults to 30.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["article"]
        params = {"mid": self.__uid, "ps": ps, "pn": pn, "sort": order.value}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_article_list(self, order: ArticleListOrder = ArticleListOrder.LATEST):
        """
        获取用户专栏文集。

        Args:
            order (ArticleListOrder, optional): 排序方式. Defaults to ArticleListOrder.LATEST

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["article_lists"]
        params = {"mid": self.__uid, "sort": order.value}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_dynamics(self, offset: int = 0, need_top: bool = False):
        """
        获取用户动态。

        Args:
            offset (str, optional):     该值为第一次调用本方法时，数据中会有个 next_offset 字段，
                                        指向下一动态列表第一条动态（类似单向链表）。
                                        根据上一次获取结果中的 next_offset 字段值，
                                        循环填充该值即可获取到全部动态。
                                        0 为从头开始。
                                        Defaults to 0.
            need_top (bool, optional):  显示置顶动态. Defaults to False.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["dynamic"]
        params = {
            "host_uid": self.__uid,
            "offset_dynamic_id": offset,
            "need_top": 1 if need_top else 0,
        }
        data = await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )
        # card 字段自动转换成 JSON。
        if "cards" in data:
            for card in data["cards"]:
                card["card"] = json.loads(card["card"])
                card["extend_json"] = json.loads(card["extend_json"])
        return data

    async def get_subscribed_bangumi(
        self, pn: int = 1, type_: BangumiType = BangumiType.BANGUMI
    ):
        """
        获取用户追番/追剧列表。

        Args:
            pn    (int, optional)         : 页码数，从 1 开始。 Defaults to 1.
            type_ (BangumiType, optional): 资源类型. Defaults to BangumiType.BANGUMI

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["bangumi"]
        params = {"vmid": self.__uid, "pn": pn, "ps": 15, "type": type_.value}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_followings(self, pn: int = 1, desc: bool = True):
        """
        获取用户关注列表（不是自己只能访问前 5 页）

        Args:
            pn   (int, optional) : 页码，从 1 开始. Defaults to 1.
            desc (bool, optional): 倒序排序. Defaults to True.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["followings"]
        params = {
            "vmid": self.__uid,
            "ps": 20,
            "pn": pn,
            "order": "desc" if desc else "asc",
        }
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_all_followings(self):
        """
        获取所有的关注列表。（如果用户设置保密会没有任何数据）

        Returns:
            list: 关注列表
        """
        api = API["info"]["all_followings"]
        params = {"mid": self.__uid}
        sess = get_session()
        data = json.loads(
            (
                await sess.get(
                    url=api["url"], params=params, cookies=self.credential.get_cookies()
                )
            ).text
        )
        return data["card"]["attentions"]

    async def get_followers(self, pn: int = 1, desc: bool = True):
        """
        获取用户粉丝列表（不是自己只能访问前 5 页，是自己也不能获取全部的样子）

        Args:
            pn   (int, optional) : 页码，从 1 开始. Defaults to 1.
            desc (bool, optional): 倒序排序. Defaults to True.

        Returns:
            dict: 调用接口返回的内容。
        """

        api = API["info"]["followers"]
        params = {
            "vmid": self.__uid,
            "ps": 20,
            "pn": pn,
            "order": "desc" if desc else "asc",
        }
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def top_followers(self, since=None):
        """
        获取用户粉丝排行
        Args:
            since   (int, optional) : 开始时间(msec)

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["top_followers"]
        params = {}
        if since:
            params["t"] = int(since)
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    async def get_overview_stat(self):
        """
        获取用户的简易订阅和投稿信息。

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["overview"]
        params = {"mid": self.__uid, "jsonp": "jsonp"}
        return await request(
            "GET", url=api["url"], params=params, credential=self.credential
        )

    # 操作用户

    async def modify_relation(self, relation: RelationType):
        """
        修改和用户的关系，比如拉黑、关注、取关等。

        Args:
            relation (RelationType): 用户关系。

        Returns:
            dict: 调用接口返回的内容。
        """

        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_bili_jct()

        api = API["operate"]["modify"]
        data = {"fid": self.__uid, "act": relation.value, "re_src": 11}
        return await request(
            "POST", url=api["url"], data=data, credential=self.credential
        )

    async def get_channel_videos_series(self, sid: int, pn: int = 1, ps: int = 100):
        """
        查看频道内所有视频。仅供 series_list。

        Args:
            sid(int): 频道的 series_id
            pn(int) : 页数，默认为 1
            ps(int) : 每一页显示的视频数量

        Returns:
            dict: 调用接口返回的内容
        """
        api = API["info"]["channel_video_series"]
        param = {"mid": self.__uid, "series_id": sid, "pn": pn, "ps": ps}
        return await request(
            "GET", url=api["url"], params=param, credential=self.credential
        )

    async def get_channel_videos_season(
        self,
        sid: int,
        sort: ChannelOrder = ChannelOrder.DEFAULT,
        pn: int = 1,
        ps: int = 100,
    ):
        """
        查看频道内所有视频。仅供 season_list。

        Args:
            sid(int)          : 频道的 season_id
            sort(ChannelOrder): 排序方式
            pn(int)           : 页数，默认为 1
            ps(int)           : 每一页显示的视频数量

        Returns:
            dict: 调用接口返回的内容
        """
        api = API["info"]["channel_video_season"]
        param = {
            "mid": self.__uid,
            "season_id": sid,
            "sort_reverse": sort.value,
            "page_num": pn,
            "page_size": ps,
        }
        return await request(
            "GET", url=api["url"], params=param, credential=self.credential
        )

    async def get_channel_list(self):
        """
        查看用户所有的频道（包括新版）和部分视频。
        适用于获取列表。
        未处理数据。不推荐。

        Returns:
            dict: 调用接口返回的结果
        """
        api = API["info"]["channel_list"]
        param = {"mid": self.__uid, "page_num": 1, "page_size": 1}
        res = await request(
            "GET", url=api["url"], params=param, credential=self.credential
        )
        items = res["items_lists"]["page"]["total"]
        time.sleep(0.5)
        if items == 0:
            items = 1
        param["page_size"] = items
        return await request(
            "GET", url=api["url"], params=param, credential=self.credential
        )

    async def get_channels(self):
        """
        获取用户所有合集

        Returns:
            List[ChannelSeries]: 合集与列表类的列表
        """
        channel_data = await self.get_channel_list()
        channels = []
        for item in channel_data["items_lists"]["seasons_list"]:
            id_ = item["meta"]["season_id"]
            meta = item["meta"]
            channels.append(
                ChannelSeries(
                    self.__uid,
                    ChannelSeriesType.SEASON,
                    id_,
                    self.credential,
                    meta=meta,
                )
            )
        for item in channel_data["items_lists"]["series_list"]:
            id_ = item["meta"]["series_id"]
            meta = item["meta"]
            channels.append(
                ChannelSeries(
                    self.__uid,
                    ChannelSeriesType.SERIES,
                    id_,
                    self.credential,
                    meta=meta,
                )
            )
        return channels

    async def get_cheese(self):
        """
        查看用户的所有课程

        Returns:
            dict: 调用接口返回的结果
        """
        api = API["info"]["pugv"]
        params = {"mid": self.__uid}
        return await request("GET", api["url"], params=params)


class ChannelSeriesType(Enum):
    """
    合集与列表类型

    + SERIES: 旧版
    + SEASON: 新版

    **新版合集名字为`合集·XXX`，请注意区别**
    """

    SERIES = 0
    SEASON = 1


class ChannelSeries:
    """
    合集与列表类
    """

    def __init__(
        self,
        uid: int,
        type_: ChannelSeriesType = ChannelSeriesType.SEASON,
        id_: int = 0,
        credential: Credential = None,
        meta=None,
    ):
        """
        uid(int)                : 用户 uid
        type_(ChannelSeriesType): 合集与列表类型
        id_(int)                : season_id 或 series_id
        credential(Credential)  : 凭证
        """
        self.__uid = uid
        self.is_new = type_.value
        self.id_ = id_
        self.owner = User(self.__uid, credential=credential)
        self.credential = credential
        self.meta = None
        if self.is_new:
            look_type = "seasons"
        else:
            look_type = "series"
        if meta is None:
            credential = self.credential if self.credential else Credential()
            api = API["info"]["channel_list"]
            param = {"mid": self.__uid, "page_num": 1, "page_size": 1}
            res = httpx.request(
                "GET", url=api["url"], params=param, cookies=credential.get_cookies()
            )
            items = json.loads(res.text)["data"]["items_lists"]["page"]["total"]
            time.sleep(0.5)
            if items == 0:
                items = 1
            param["page_size"] = items
            channel_list = json.loads(
                httpx.request(
                    "GET",
                    url=api["url"],
                    params=param,
                    cookies=credential.get_cookies(),
                ).text
            )["data"]
            for channel in channel_list["items_lists"][look_type + "_list"]:
                type_id = channel["meta"]["season_id" if self.is_new else "series_id"]
                if type_id == self.id_:
                    self.meta = channel["meta"]
            if self.meta is None:
                raise ValueError("未找到频道信息。")
        else:
            self.meta = meta

    def get_meta(self):
        """
        获取元数据

        Returns:
            调用 API 返回的结果
        """
        return self.meta

    async def get_videos(
        self, sort: ChannelOrder = ChannelOrder.DEFAULT, pn: int = 1, ps: int = 100
    ):
        """
        获取合集视频
        Args:
            sort(ChannelOrder): 排序方式，在旧版列表此参数不起效果。
            pn(int)           : 页数，默认为 1
            ps(int)           : 每一页显示的视频数量

        Returns:
            调用 API 返回的结果
        """
        if self.is_new:
            return await self.owner.get_channel_videos_season(self.id_, sort, pn, ps)
        else:
            return await self.owner.get_channel_videos_series(self.id_, pn, ps)


async def get_self_info(credential: Credential):
    """
    获取自己的信息

    Args:
        credential (Credential): Credential
    """
    api = API["info"]["my_info"]
    credential.raise_for_no_sessdata()

    return await request("GET", api["url"], credential=credential)


async def create_subscribe_group(name: str, credential: Credential):
    """
    创建用户关注分组

    Args:
        name       (str)       : 分组名
        credential (Credential): Credential

    Returns:
        API 调用返回结果。
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    api = API["operate"]["create_subscribe_group"]
    data = {"tag": name}

    return await request("POST", api["url"], data=data, credential=credential)


async def delete_subscribe_group(group_id: int, credential: Credential):
    """
    删除用户关注分组

    Args:
        group_id   (int)       : 分组 ID
        credential (Credential): Credential

    Returns:
        调用 API 返回结果
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    api = API["operate"]["del_subscribe_group"]
    data = {"tagid": group_id}

    return await request("POST", api["url"], data=data, credential=credential)


async def rename_subscribe_group(group_id: int, new_name: str, credential: Credential):
    """
    重命名关注分组

    Args:
        group_id   (int)       : 分组 ID
        new_name   (str)       : 新的分组名
        credential (Credential): Credential

    Returns:
        调用 API 返回结果
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    api = API["operate"]["rename_subscribe_group"]
    data = {"tagid": group_id, "name": new_name}

    return await request("POST", api["url"], data=data, credential=credential)


async def set_subscribe_group(
    uids: List[int], group_ids: List[int], credential: Credential
):
    """
    设置用户关注分组

    Args:
        uids       (List[int]) : 要设置的用户 UID 列表，必须已关注。
        group_ids  (List[int]) : 要复制到的分组列表
        credential (Credential): Credential

    Returns:
        API 调用结果
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    api = API["operate"]["set_user_subscribe_group"]
    data = {"fids": join(",", uids), "tagids": join(",", group_ids)}

    return await request("POST", api["url"], data=data, credential=credential)


async def get_self_history(
    page_num: int = 1, per_page_item: int = 100, credential: Credential = None
):
    """
    获取用户浏览历史记录

    Args:
        page_num (int): 页码数
        per_page_item (int): 每页多少条历史记录
        credential (Credential): Credential

    Returns:
        list(dict): 返回当前页的指定历史记录列表
    """
    if not credential:
        credential = Credential()

    credential.raise_for_no_sessdata()

    api = API["info"]["history"]
    params = {"pn": page_num, "ps": per_page_item}

    return await request("GET", url=api["url"], params=params, credential=credential)


async def get_self_coins(credential: Credential = None):
    """
    获取自己的硬币数量。
    如果接口返回错误代码则为身份校验失败

    Returns:
        int: 硬币数量
    """
    if credential is None:
        credential = Credential()
    credential.raise_for_no_sessdata()
    credential.raise_for_no_dedeuserid()
    api = API["info"]["get_coins"]
    return (await request("GET", url=api["url"], credential=credential))["money"]


async def get_toview_list(credential: Credential = Credential()):
    """
    获取稍后再看列表

    Args:
        credential(Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = get_api("toview")["info"]["list"]
    credential.raise_for_no_sessdata()
    return await request("GET", api["url"], credential=credential)


async def clear_toview_list(credential: Credential = Credential()):
    """
    清空稍后再看列表

    Args:
        credential(Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = get_api("toview")["operate"]["clear"]
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    return await request("POST", api["url"], credential=credential)


async def delete_viewed_videos_from_toview(credential: None):
    """
    删除稍后再看列表已经看过的视频

    Args:
        credential(Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = get_api("toview")["operate"]["del"]
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()
    datas = {"viewed": "true"}
    return await request("POST", api["url"], credential=credential, data=datas)


async def check_nickname(nick_name: str = None):
    """
    检验昵称是否可用

    Args:
        nick_name(str): 昵称

    Returns:
        List[bool, str]: 昵称是否可用 + 不可用原因
    """
    api = get_api("common")["nickname"]["check_nickname"]
    params = {"nickName": nick_name}
    try:
        resp = await request("GET", api["url"], params=params)
    except ResponseCodeException as e:
        return False, str(e)
    else:
        return True, ""


async def get_self_events(ts: int = 0, credential: Credential = None):
    """
    获取自己入站后每一刻的事件

    Args:
        ts(int, optional)               : 时间戳. Defaults to 0.
        credential(Credential, optional): 凭据. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    api = API["info"]["events"]
    params = {"ts": ts}
    return await request("GET", api["url"], params=params, credential=credential)
