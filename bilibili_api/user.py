"""
bilibili_api.user

用户相关
"""

import json
import time
from enum import Enum
from typing import List, Union, Tuple
from json.decoder import JSONDecodeError

from .utils.utils import get_api, join
from .utils.credential import Credential
from .exceptions import ResponseCodeException
from .utils.network import get_session, Api
from .channel_series import ChannelOrder, ChannelSeries, ChannelSeriesType

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


class MedialistOrder(Enum):
    """
    medialist排序顺序。

    + PUBDATE : 上传日期。
    + PLAY    : 播放量。
    + COLLECT : 收藏量。
    """

    PUBDATE = 1
    PLAY = 2
    COLLECT = 3


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


class BangumiFollowStatus(Enum):
    """
    番剧追番状态类型。

    + ALL        : 全部
    + WANT       : 想看
    + WATCHING   : 在看
    + WATCHED    : 已看
    """

    ALL = 0
    WANT = 1
    WATCHING = 2
    WATCHED = 3


class HistoryType(Enum):
    """
    历史记录分类

    + ALL      : 全部
    + archive  : 稿件
    + live     : 直播
    + article  : 专栏
    """

    ALL = "all"
    archive = "archive"
    live = "live"
    article = "article"


class HistoryBusinessType(Enum):
    """
    历史记录 Business 分类

    + archive：稿件
    + pgc：剧集（番剧 / 影视）
    + live：直播
    + article-list：文集
    + article：文章
    """

    archive = "archive"
    pgc = "pgc"
    live = "live"
    article_list = "article-list"
    article = "article"


class OrderType(Enum):
    """
    排序字段

    + desc：倒序
    + asc：正序
    """

    desc = "desc"
    asc = "asc"


async def name2uid_sync(names: Union[str, List[str]]):
    """
    将用户名转为 uid

    Args:
        names (str/List[str]): 用户名

    Returns:
        dict: 调用 API 返回的结果
    """
    if isinstance(names, str):
        n = names
    else:
        n = ",".join(names)
    params = {"names": n}
    return Api(**API["info"]["name_to_uid"]).update_params(**params).result_sync


async def name2uid(names: Union[str, List[str]]):
    """
    将用户名转为 uid

    Args:
        names (str/List[str]): 用户名

    Returns:
        dict: 调用 API 返回的结果
    """
    if isinstance(names, str):
        n = names
    else:
        n = ",".join(names)
    params = {"names": n}
    return await Api(**API["info"]["name_to_uid"]).update_params(**params).result


class User:
    """
    用户相关
    """

    def __init__(self, uid: int, credential: Union[Credential, None] = None):
        """
        Args:
            uid        (int)                        : 用户 UID

            credential (Credential | None, optional): 凭据. Defaults to None.
        """
        self.__uid = uid

        if credential is None:
            credential = Credential()
        self.credential = credential
        self.__self_info = None

    def get_user_info_sync(self) -> dict:
        """
        获取用户信息（昵称，性别，生日，签名，头像 URL，空间横幅 URL 等）

        Returns:
            dict: 调用接口返回的内容。

        [用户空间详细信息](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/user/info.md#%E7%94%A8%E6%88%B7%E7%A9%BA%E9%97%B4%E8%AF%A6%E7%BB%86%E4%BF%A1%E6%81%AF)
        """
        params = {
            "mid": self.__uid,
        }
        result = Api(**API["info"]["info"], credential=self.credential, params=params).result_sync
        return result

    async def get_user_info(self) -> dict:
        """
        获取用户信息（昵称，性别，生日，签名，头像 URL，空间横幅 URL 等）

        Returns:
            dict: 调用接口返回的内容。

        [用户空间详细信息](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/user/info.md#%E7%94%A8%E6%88%B7%E7%A9%BA%E9%97%B4%E8%AF%A6%E7%BB%86%E4%BF%A1%E6%81%AF)
        """
        params = {
            "mid": self.__uid,
        }
        return (
            await Api(**API["info"]["info"], credential=self.credential)
            .update_params(**params)
            .result
        )

    async def __get_self_info(self) -> dict:
        """
        获取自己的信息。如果存在缓存则使用缓存。

        Returns:
            dict: 调用接口返回的内容。
        """
        if self.__self_info is not None:
            return self.__self_info

        self.__self_info = await self.get_user_info()
        return self.__self_info

    def get_uid(self) -> int:
        """
        获取用户 UID

        Returns:
            int: 用户 UID
        """
        return self.__uid

    async def get_user_fav_tag(self, pn: int = 1, ps: int = 20) -> dict:
        """
        获取用户关注的 Tag 信息，如果用户设为隐私，则返回 获取登录数据失败

        Args:
            pn (int, optional): 页码，从 1 开始. Defaults to 1.
            ps (int, optional): 每页的数据量. Defaults to 20.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["user_tag"]
        params = {"vmid": self.__uid}  # , "pn": pn, "ps": ps}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_space_notice(self) -> dict:
        """
        获取用户空间公告

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["space_notice"]
        params = {"mid": self.__uid}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def set_space_notice(self, content: str = "") -> dict:
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
        return await Api(**api, credential=self.credential).update_data(**data).result

    async def get_relation_info(self) -> dict:
        """
        获取用户关系信息（关注数，粉丝数，悄悄关注，黑名单数）

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["relation_stat"]
        params = {"vmid": self.__uid}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_up_stat(self) -> dict:
        """
        获取 UP 主数据信息（视频总播放量，文章总阅读量，总点赞数）

        Returns:
            dict: 调用接口返回的内容。
        """
        self.credential.raise_for_no_bili_jct()

        api = API["info"]["upstat"]
        params = {"mid": self.__uid}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_top_videos(self) -> dict:
        """
        获取用户的指定视频（代表作）

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["user_top_videos"]
        params = {"vmid": self.get_uid()}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_masterpiece(self) -> list:
        """
        获取用户代表作

        Returns:
            list: 调用接口返回的内容。
        """
        api = API["info"]["masterpiece"]
        params = {"vmid": self.get_uid()}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_user_medal(self) -> dict:
        """
        读取用户粉丝牌详细列表，如果隐私则不可以

        Returns:
            dict: 调用接口返回的内容。
        """
        self.credential.raise_for_no_sessdata()
        # self.credential.raise_for_no_bili_jct()
        api = API["info"]["user_medal"]
        params = {"target_id": self.__uid}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_live_info(self) -> dict:
        """
        获取用户直播间信息。

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["live"]
        params = {"mid": self.__uid}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_videos(
        self,
        tid: int = 0,
        pn: int = 1,
        ps: int = 30,
        keyword: str = "",
        order: VideoOrder = VideoOrder.PUBDATE,
    ) -> dict:
        """
        获取用户投稿视频信息。

        Args:
            tid     (int, optional)       : 分区 ID. Defaults to 0（全部）.

            pn      (int, optional)       : 页码，从 1 开始. Defaults to 1.

            ps      (int, optional)       : 每一页的视频数. Defaults to 30.

            keyword (str, optional)       : 搜索关键词. Defaults to "".

            order   (VideoOrder, optional): 排序方式. Defaults to VideoOrder.PUBDATE

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["video"]
        params = {
            "mid": self.__uid,
            "ps": ps,
            "tid": tid,
            "pn": pn,
            "keyword": keyword,
            "order": order.value,
            # -352 https://github.com/Nemo2011/bilibili-api/issues/595
            "dm_img_list": "[]",  # 鼠标/键盘操作记录
            # WebGL 1.0 (OpenGL ES 2.0 Chromium)
            "dm_img_str": "V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
            # ANGLE (Intel, Intel(R) UHD Graphics 630 (0x00003E9B) Direct3D11 vs_5_0 ps_5_0, D3D11)Google Inc. (Intel
            "dm_cover_img_str": "QU5HTEUgKEludGVsLCBJbnRlbChSKSBVSEQgR3JhcGhpY3MgNjMwICgweDAwMDAzRTlCKSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChJbnRlbC",
        }
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_media_list(
        self,
        oid: int | None = None,
        ps: int = 20,
        direction: bool = False,
        desc: bool = True,
        sort_field: MedialistOrder = MedialistOrder.PUBDATE,
        tid: int = 0,
        with_current: bool = False
    ) -> dict:
        """
        以 medialist 形式获取用户投稿信息。

        Args:
            oid             (int, optional)         : 起始视频 aid， 默认为列表开头
            ps              (int, optional)         : 每一页的视频数. Defaults to 20. Max 100
            direction       (bool, optional)        : 相对于给定oid的查询方向 True 向列表末尾方向 False 向列表开头方向 Defaults to False.
            desc            (bool, optional)        : 倒序排序. Defaults to True.
            sort_field      (int, optional)         : 用于排序的栏  1 发布时间，2 播放量，3 收藏量
            tid             (int, optional)         : 分区 ID. Defaults to 0（全部）. 1 部分（未知）
            with_current    (bool, optional)        : 返回的列表中是否包含给定oid自身 Defaults to False.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["media_list"]
        params = {
            "mobi_app": 'web',
            "type": 1,
            "biz_id": self.__uid,
            "oid": oid,
            "otype": 2,
            "ps": ps,
            "direction": direction,
            "desc": desc,
            "sort_field": sort_field.value,
            "tid": tid,
            "with_current": with_current
        }
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_audios(
        self, order: AudioOrder = AudioOrder.PUBDATE, pn: int = 1, ps: int = 30
    ) -> dict:
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
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_album(
        self, biz: AlbumType = AlbumType.ALL, page_num: int = 1, page_size: int = 30
    ) -> dict:
        """
        获取用户投稿相簿。

        Args:
            biz (AlbumType, optional): 排序方式. Defaults to AlbumType.ALL.

            page_num      (int, optional)       : 页码数，从 1 开始。 Defaults to 1.

            page_size    (int)       : 每一页的相簿条目. Defaults to 30.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["album"]
        params = {
            "uid": self.__uid,
            "page_num": page_num,
            "page_size": page_size,
            "biz": biz.value,
        }
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_articles(
        self, pn: int = 1, order: ArticleOrder = ArticleOrder.PUBDATE, ps: int = 30
    ) -> dict:
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
        return (
            await Api(**api, credential=self.credential, wbi=True)
            .update_params(**params)
            .result
        )

    async def get_article_list(
        self, order: ArticleListOrder = ArticleListOrder.LATEST
    ) -> dict:
        """
        获取用户专栏文集。

        Args:
            order (ArticleListOrder, optional): 排序方式. Defaults to ArticleListOrder.LATEST

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["article_lists"]
        params = {"mid": self.__uid, "sort": order.value}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_dynamics(self, offset: int = 0, need_top: bool = False) -> dict:
        """
        获取用户动态。

        建议使用 user.get_dynamics_new() 新接口。
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
        data = (
            await Api(**api, credential=self.credential).update_params(**params).result
        )
        # card 字段自动转换成 JSON。
        if "cards" in data:
            for card in data["cards"]:
                card["card"] = json.loads(card["card"])
                card["extend_json"] = json.loads(card["extend_json"])
        return data

    async def get_dynamics_new(self, offset: int = "") -> dict:
        """
        获取用户动态。

        Args:
            offset (str, optional):     该值为第一次调用本方法时，数据中会有个 offset 字段，

                                        指向下一动态列表第一条动态（类似单向链表）。

                                        根据上一次获取结果中的 next_offset 字段值，

                                        循环填充该值即可获取到全部动态。

                                        空字符串为从头开始。
                                        Defaults to "".

        Returns:
            dict: 调用接口返回的内容。
        """
        self.credential.raise_for_no_sessdata()
        api = API["info"]["dynamic_new"]
        params = {
            "host_mid": self.__uid,
            "offset": offset,
            "features": "itemOpusStyle",
            "timezone_offset": -480,
        }
        data = (
            await Api(**api, credential=self.credential).update_params(**params).result
        )
        return data

    async def get_subscribed_bangumi(
        self,
        type_: BangumiType = BangumiType.BANGUMI,
        follow_status: BangumiFollowStatus = BangumiFollowStatus.ALL,
        pn: int = 1,
        ps: int = 15,
    ) -> dict:
        """
        获取用户追番/追剧列表。

        Args:
            pn    (int, optional)         : 页码数，从 1 开始。 Defaults to 1.

            ps      (int, optional)       : 每一页的番剧数. Defaults to 15.

            type_ (BangumiType, optional): 资源类型. Defaults to BangumiType.BANGUMI

            follow_status (BangumiFollowStatus, optional): 追番状态. Defaults to BangumiFollowStatus.ALL

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["bangumi"]
        params = {
            "vmid": self.__uid,
            "pn": pn,
            "ps": ps,
            "type": type_.value,
            "follow_status": follow_status.value,
        }
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_followings(
        self,
        pn: int = 1,
        ps: int = 100,
        attention: bool = False,
        order: OrderType = OrderType.desc,
    ) -> dict:
        """
        获取用户关注列表（不是自己只能访问前 5 页）

        Args:
            pn        (int, optional)  : 页码，从 1 开始. Defaults to 1.

            ps        (int, optional)  : 每页的数据量. Defaults to 100.

            attention (bool, optional) : 是否采用“最常访问”排序，否则为“关注顺序”排序. Defaults to False.

            order     (OrderType, optional) : 排序方式. Defaults to OrderType.desc.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["all_followings2"]
        params = {
            "vmid": self.__uid,
            "ps": ps,
            "pn": pn,
            "order_type": "attention" if attention else "",
            "order": order.value,
        }
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_all_followings(self) -> dict:
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

    async def get_followers(
        self, pn: int = 1, ps: int = 100, desc: bool = True
    ) -> dict:
        """
        获取用户粉丝列表（不是自己只能访问前 5 页，是自己也不能获取全部的样子）

        Args:
            pn   (int, optional) : 页码，从 1 开始. Defaults to 1.

            ps   (int, optional) : 每页的数据量. Defaults to 100.

            desc (bool, optional): 倒序排序. Defaults to True.

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["followers"]
        params = {
            "vmid": self.__uid,
            "ps": ps,
            "pn": pn,
            "order": "desc" if desc else "asc",
        }
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_self_same_followers(self, pn: int = 1, ps: int = 50) -> dict:
        """
        获取用户与自己共同关注的 up 主

        Args:
            pn (int): 页码. Defaults to 1.

            ps (int): 单页数据量. Defaults to 50.

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()
        api = API["info"]["get_same_followings"]
        params = {"vmid": self.get_uid(), "pn": pn, "ps": ps}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def top_followers(self, since=None) -> dict:
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
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_overview_stat(self) -> dict:
        """
        获取用户的简易订阅和投稿信息。

        Returns:
            dict: 调用接口返回的内容。
        """
        api = API["info"]["overview"]
        params = {"mid": self.__uid, "jsonp": "jsonp"}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_relation(self, uid: int) -> dict:
        """
        获取与某用户的关系

        Args:
            uid (int): 用户 UID

        Returns:
            dict: 调用接口返回的内容。
        """

        api = API["info"]["relation"]
        params = {"mid": uid}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    # 操作用户关系

    async def modify_relation(self, relation: RelationType) -> dict:
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
        return await Api(**api, credential=self.credential).update_data(**data).result

    # 有关合集与列表

    async def get_channel_videos_series(
        self,
        sid: int,
        sort: ChannelOrder = ChannelOrder.DEFAULT,
        pn: int = 1,
        ps: int = 100,
    ) -> dict:
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
        params = {
            "mid": self.__uid,
            "series_id": sid,
            "pn": pn,
            "ps": ps,
            "sort": "asc" if sort == ChannelOrder.CHANGE else "desc",
        }
        return (
            await Api(**api, wbi=True, credential=self.credential)
            .update_params(**params)
            .result
        )

    async def get_channel_videos_season(
        self,
        sid: int,
        sort: ChannelOrder = ChannelOrder.DEFAULT,
        pn: int = 1,
        ps: int = 100,
    ) -> dict:
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
        params = {
            "mid": self.__uid,
            "season_id": sid,
            "sort_reverse": sort.value,
            "page_num": pn,
            "page_size": ps,
        }
        return (
            await Api(**api, wbi=True, credential=self.credential)
            .update_params(**params)
            .result
        )

    async def get_channel_list(self) -> dict:
        """
        查看用户所有的频道（包括新版）和部分视频。

        适用于获取列表。

        未处理数据。不推荐。

        Returns:
            dict: 调用接口返回的结果
        """
        api = API["info"]["channel_list"]
        params = {"mid": self.__uid, "page_num": 1, "page_size": 1}
        res = (
            await Api(**api, wbi=True, credential=self.credential)
            .update_params(**params)
            .result
        )
        items = res["items_lists"]["page"]["total"]
        time.sleep(0.5)
        if items == 0:
            items = 1
        params["page_size"] = items
        return (
            await Api(**api, wbi=True, credential=self.credential)
            .update_params(**params)
            .result
        )

    async def get_channels(self) -> List["ChannelSeries"]:
        """
        获取用户所有合集

        Returns:
            List[ChannelSeries]: 合集与列表类的列表
        """
        from . import channel_series

        channel_data = await self.get_channel_list()
        channels = []
        for item in channel_data["items_lists"]["seasons_list"]:
            id_ = item["meta"]["season_id"]
            meta = item["meta"]
            channel_series.channel_meta_cache[
                str(ChannelSeriesType.SEASON.value) + "-" + str(id_)
                ] = meta
            channels.append(
                ChannelSeries(
                    self.__uid, ChannelSeriesType.SEASON, id_, self.credential
                )
            )
        for item in channel_data["items_lists"]["series_list"]:
            id_ = item["meta"]["series_id"]
            meta = item["meta"]
            channel_series.channel_meta_cache[
                str(ChannelSeriesType.SERIES.value) + "-" + str(id_)
                ] = meta
            channels.append(
                ChannelSeries(
                    self.__uid, ChannelSeriesType.SERIES, id_, self.credential
                )
            )
        return channels

    async def get_cheese(self) -> dict:
        """
        查看用户的所有课程

        Returns:
            dict: 调用接口返回的结果
        """
        api = API["info"]["pugv"]
        params = {"mid": self.__uid}
        return (
            await Api(**api, wbi=True, credential=self.credential)
            .update_params(**params)
            .result
        )

    async def get_reservation(self) -> dict:
        """
        获取用户空间预约

        Returns:
            dict: 调用接口返回的结果
        """
        api = API["info"]["reservation"]
        params = {"vmid": self.get_uid()}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_elec_user_monthly(self) -> dict:
        """
        获取空间充电公示信息

        Returns:
            dict: 调用接口返回的结果
        """
        api = API["info"]["elec_user_monthly"]
        params = {"up_mid": self.get_uid()}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    async def get_uplikeimg(self) -> dict:
        """
        视频三联特效

        Returns:
            dict: 调用 API 返回的结果。
        """
        api = API["info"]["uplikeimg"]
        params = {"vmid": self.get_uid()}
        return await Api(**api).update_params(**params).result


async def get_self_info(credential: Credential) -> dict:
    """
    获取自己的信息

    Args:
        credential (Credential): Credential
    """
    api = API["info"]["my_info"]
    credential.raise_for_no_sessdata()

    return await Api(**api, credential=credential).result


async def edit_self_info(
    birthday: str, sex: str, uname: str, usersign: str, credential: Credential
) -> dict:
    """
    修改自己的信息 (Web)

    Args:
        birthday (str)      : 生日 YYYY-MM-DD

        sex (str)           : 性别 男|女|保密

        uname (str)         : 用户名

        usersign (str)      : 个性签名

        credential (Credential): Credential
    """

    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    api = API["info"]["edit_my_info"]
    data = {"birthday": birthday, "sex": sex, "uname": uname, "usersign": usersign}

    return await Api(**api, credential=credential).update_data(**data).result


async def create_subscribe_group(name: str, credential: Credential) -> dict:
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

    return await Api(**api, credential=credential).update_data(**data).result


async def delete_subscribe_group(group_id: int, credential: Credential) -> dict:
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

    return await Api(**api, credential=credential).update_data(**data).result


async def rename_subscribe_group(
    group_id: int, new_name: str, credential: Credential
) -> dict:
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

    return await Api(**api, credential=credential).update_data(**data).result


async def set_subscribe_group(
    uids: List[int], group_ids: List[int], credential: Credential
) -> dict:
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

    return await Api(**api, credential=credential).update_data(**data).result


async def get_self_history(
    page_num: int = 1,
    per_page_item: int = 100,
    credential: Union[Credential, None] = None,
) -> dict:
    """
    获取用户浏览历史记录（旧版）

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

    return await Api(**api, credential=credential).update_params(**params).result


async def get_self_history_new(
    credential: Credential,
    _type: HistoryType = HistoryType.ALL,
    ps: int = 20,
    view_at: int = None,
    max: int = None,
    business: HistoryBusinessType = None,
) -> dict:
    """
    获取用户浏览历史记录（新版），与旧版不同有分类参数，但相对缺少视频信息

    max、business、view_at 参数用于历史记录列表的 IFS (无限滚动)，其用法类似链表的 next 指针

    将返回值某历史记录的 oid、business、view_at 作为上述参数传入，即可获取此 oid 之前的历史记录

    Args:
        credential (Credential) : Credential

        _type      (HistroyType): 历史记录分类, 默认为 HistroyType.ALL

        ps         (int)        : 每页多少条历史记录, 默认为 20

        view_at    (int)        : 时间戳，获取此时间戳之前的历史记录

        max        (int)        : 历史记录截止目标 oid

    Returns:
        dict: 调用 API 返回的结果
    """
    credential.raise_for_no_sessdata()
    api = API["info"]["history_new"]
    params = {
        "type": _type.value,
        "ps": ps,
        "view_at": view_at,
        "max": max,
        "business": business if business is None else business.value,
    }
    return await Api(**api, credential=credential).update_params(**params).result


async def get_self_coins(credential: Credential) -> int:
    """
    获取自己的硬币数量。

    Returns:
        int: 硬币数量
    """
    if credential is None:
        credential = Credential()
    credential.raise_for_no_sessdata()
    credential.raise_for_no_dedeuserid()
    api = API["info"]["get_coins"]
    return (await Api(**api, credential=credential).result)["money"]


async def get_self_special_followings(
    credential: Credential, pn: int = 1, ps: int = 50
) -> dict:
    """
    获取自己特殊关注的列表

    Args:
        credential (Credential)   : 凭据类

        pn         (int, optional): 页码. Defaults to 1.

        ps         (int, optional): 每页数据大小. Defaults to 50.
    """
    credential.raise_for_no_sessdata()
    api = API["info"]["get_special_followings"]
    params = {"pn": pn, "ps": ps}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_self_whisper_followings(
    credential: Credential, pn: int = 1, ps: int = 50
) -> dict:
    """
    获取自己悄悄关注的列表。

    Args:
        credential (Credential)   : 凭据类

        pn         (int, optional): 页码. Defaults to 1.

        ps         (int, optional): 每页数据大小. Defaults to 50.
    """
    credential.raise_for_no_sessdata()
    api = API["info"]["get_whisper_followings"]
    params = {"pn": pn, "ps": ps}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_self_friends(credential: Credential) -> dict:
    """
    获取与自己互粉的人

    Args:
        credential (Credential)   : 凭据类
    """
    credential.raise_for_no_sessdata()
    api = API["info"]["get_friends"]
    return await Api(**api, credential=credential).result


async def get_self_black_list(
    credential: Credential, pn: int = 1, ps: int = 50
) -> dict:
    """
    获取自己的黑名单信息

    Args:
        credential (Credential)   : 凭据类

        pn         (int, optional): 页码. Defaults to 1.

        ps         (int, optional): 每页数据大小. Defaults to 50.
    """
    credential.raise_for_no_sessdata()
    api = API["info"]["get_black_list"]
    params = {"pn": pn, "ps": ps}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_toview_list(credential: Credential):
    """
    获取稍后再看列表

    Args:
        credential (Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """
    api = get_api("toview")["info"]["list"]
    credential.raise_for_no_sessdata()
    return await Api(**api, credential=credential).result


async def clear_toview_list(credential: Credential):
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
    return await Api(**api, credential=credential).result


async def delete_viewed_videos_from_toview(credential: Credential):
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
    return await Api(**api, credential=credential).update_data(**datas).result


async def check_nickname(nick_name: str) -> Tuple[bool, str]:
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
        resp = await Api(**api).update_params(**params).result
    except ResponseCodeException as e:
        return False, str(e)
    else:
        return True, ""


async def get_self_events(ts: int = 0, credential: Union[Credential, None] = None):
    """
    获取自己入站后每一刻的事件

    Args:
        ts(int, optional)                      : 时间戳. Defaults to 0.

        credential(Credential | None, optional): 凭据. Defaults to None.

    Returns:
        dict: 调用 API 返回的结果
    """
    credential = credential if credential else Credential()
    api = API["info"]["events"]
    params = {"ts": ts}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_self_notes_info(
    page_num: int, page_size: int, credential: Credential
) -> dict:
    """
    获取自己的笔记列表

    Args:
        page_num: 页码

        page_size: 每页项数

        credential(Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """

    assert page_num > 0
    assert page_size > 0

    credential.raise_for_no_sessdata()

    api = API["info"]["all_notes"]
    params = {"pn": page_num, "ps": page_size}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_self_public_notes_info(
    page_num: int, page_size: int, credential: Credential
) -> dict:
    """
    获取自己的公开笔记列表

    Args:
        page_num: 页码

        page_size: 每页项数

        credential(Credential): 凭据类

    Returns:
        dict: 调用 API 返回的结果
    """

    assert page_num > 0
    assert page_size > 0

    credential.raise_for_no_sessdata()

    api = API["info"]["public_notes"]
    params = {"pn": page_num, "ps": page_size}
    return await Api(**api, credential=credential).update_params(**params).result


async def get_self_jury_info(credential: Credential) -> dict:
    """
    获取自己风纪委员信息
    """
    credential.raise_for_no_sessdata()
    api = API["info"]["jury"]
    return await Api(**api, credential=credential).result
