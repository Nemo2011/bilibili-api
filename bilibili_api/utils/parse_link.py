"""
bilibili_api.utils.parse_link

链接资源解析。
"""

from enum import Enum
import json
import httpx

from .utils import get_api
from ..article import Article
from ..audio import Audio, AudioList

from ..bangumi import Bangumi, Episode
from ..cheese import CheeseList, CheeseVideo
from ..live import LiveRoom
from ..user import User, ChannelSeriesType, ChannelSeries
from .Credential import Credential
from .sync import sync
from ..user import get_self_info
from .short import get_real_url
from ..video import Video
from ..favorite_list import FavoriteList, FavoriteListType, get_video_favorite_list

import re


class ResourceType(Enum):
    """
    链接类型类。

    + VIDEO: 视频
    + BANGUMI: 番剧
    + EPISODE: 番剧剧集
    + FAVORITE_LIST: 视频收藏夹
    + CHEESE: 课程
    + CHEESE_VIDEO: 课程视频
    + AUDIO: 音频
    + AUDIO_LIST: 歌单
    + ARTICLE: 专栏
    + USER: 用户
    + LIVE: 直播间
    + CHANNEL_SERIES: 合集与列表
    """

    VIDEO = "video"
    BANGUMI = "bangumi"
    EPISODE = "episode"
    FAVORITE_LIST = "favorite_list"
    CHEESE_VIDEO = "cheese_video"
    AUDIO = "audio"
    AUDIO_LIST = "audio_list"
    ARTICLE = "article"
    USER = "user"
    LIVE = "live"
    CHANNEL_SERIES = "channel_series"


async def parse_link(url, credential: Credential = Credential()):
    """
    解析 bilibili url 的函数。
    可以解析：
    - 视频
    - 番剧
    - 番剧剧集
    - 收藏夹
    - 课程视频
    - 音频
    - 歌单
    - 专栏
    - 用户

    Args:
        url(str)              : 链接
        credential(Credential): 凭据类

    Returns:
        Union[tuple, int]: (对象，类型) 或 -1,-1 表示出错
    """
    try:
        obj = check_short_name(url)
        if obj != -1:
            obj[0].credential = credential
            return obj

        url = await get_real_url(url)

        # 特殊处理，因为后面会过滤参数，这两项需要参数完成
        channel = parse_season_series(url)
        if channel != -1:
            return (channel, ResourceType.CHANNEL_SERIES)
        fl_space = parse_space_favorite_list(url, credential)
        if fl_space != -1:
            return fl_space

        # 过滤参数
        url = url.split("?")[0]
        if url == "https://space.bilibili.com":
            try:
                info = sync(get_self_info(credential))
            except:
                return -1
            else:
                return (User(info["mid"], credential=credential), ResourceType.USER)
        obj = None
        video = parse_video(url)
        if not video == -1:
            obj = (video, ResourceType.VIDEO)
        bangumi = parse_bangumi(url)
        if not bangumi == -1:
            obj = (bangumi, ResourceType.BANGUMI)
        episode = parse_episode(url)
        if not episode == -1:
            obj = (episode, ResourceType.EPISODE)
        favorite_list = parse_favorite_list(url)
        if not favorite_list == -1:
            obj = (favorite_list, ResourceType.FAVORITE_LIST)
        cheese_video = parse_cheese_video(url)
        if not cheese_video == -1:
            obj = (cheese_video, ResourceType.CHEESE_VIDEO)
        audio = parse_audio(url)
        if not audio == -1:
            obj = (audio, ResourceType.AUDIO)
        audio_list = parse_audio_list(url)
        if not audio_list == -1:
            obj = (audio_list, ResourceType.AUDIO_LIST)
        article = parse_article(url)
        if not article == -1:
            obj = (article, ResourceType.ARTICLE)
        user = parse_user(url)
        if not user == -1:
            obj = (user, ResourceType.USER)
        live = parse_live(url)
        if not live == -1:
            obj = (live, ResourceType.LIVE)

        if obj == None:
            return -1
        else:
            obj[0].credential = credential
            return obj
    except Exception as e:
        raise e
        return -1


def check_short_name(name: str):
    """
    解析:
      - avxxxxxxxxxx
      - bvxxxxxxxxxx
      - mlxxxxxxxxxx
      - uidxxxxxxxxx
      - cvxxxxxxxxxx
    """
    if name[:2].upper() == "AV":
        return (Video(aid=int(name[2:])), ResourceType.VIDEO)
    elif name[:2].upper() == "BV":
        return (Video(bvid=name), ResourceType.VIDEO)
    elif name[:2].upper() == "ML":
        return (FavoriteList(FavoriteListType.VIDEO, int(name[2:])), ResourceType.FAVORITE_LIST)
    elif name[:3].upper() == "UID":
        return (User(int(name[3:])), ResourceType.USER)
    elif name[:2].upper() == "CV":
        return (Article(int(name[2:])), ResourceType.ARTICLE)
    else:
        return -1


def parse_video(url):
    """
    解析视频,如果不是返回 -1，否则返回对应类
    """
    if url[:31] == "https://www.bilibili.com/video/":
        last_part = url[31:]
        if last_part[:2].upper() == "AV":
            aid = int(last_part[2:].replace("/", ""))
            return Video(aid=aid)
        elif last_part[:2].upper() == "BV":
            bvid = "BV" + last_part[2:].replace("/", "")
            return Video(bvid=bvid)
        else:
            return -1
    else:
        return -1


def parse_bangumi(url):
    """
    解析番剧,如果不是返回 -1，否则返回对应类
    """
    if url[:41] == "https://www.bilibili.com/bangumi/media/md":
        last_part = url[41:].replace("/", "")
        media_id = int(last_part)
        return Bangumi(media_id=media_id)
    else:
        return -1


def parse_episode(url):
    """
    解析番剧剧集,如果不是返回 -1，否则返回对应类
    """
    if url[:38] == "https://www.bilibili.com/bangumi/play/":
        last_part = url[38:]
        if last_part[:2].upper() == "SS":
            ssid = int(last_part[2:].replace("/", ""))
            b = Bangumi(ssid=ssid)
            first_episode_id = int(
                sync(b.get_episode_list())["main_section"]["episodes"][0]["share_url"][
                    40:
                ]
            )
            return Episode(epid=first_episode_id)
        elif last_part[:2].upper() == "EP":
            epid = int(last_part[2:].replace("/", ""))
            return Episode(epid=epid)
        else:
            return -1
    else:
        return -1


def parse_favorite_list(url):
    """
    解析收藏夹,如果不是返回 -1，否则返回对应类
    """
    if url[:44] == "https://www.bilibili.com/medialist/detail/ml":
        last_part = int(url[44:].replace("/", ""))
        return FavoriteList(media_id=last_part)
    else:
        return -1


def parse_cheese_video(url):
    """
    解析课程视频,如果不是返回 -1，否则返回对应类
    """
    if url[:37] == "https://www.bilibili.com/cheese/play/":
        if url[37:39].upper() == "EP":
            last_part = int(url[39:].replace("/", ""))
            return CheeseVideo(epid=last_part)
        elif url[37:39].upper() == "SS":
            cheese = CheeseList(season_id=int(url[39:].replace("/", "")))
            ep = sync(cheese.get_list())["items"][0]["id"]
            return CheeseVideo(epid=ep)
    else:
        return -1


def parse_audio(url):
    """
    解析音频,如果不是返回 -1，否则返回对应类
    """
    if url[:33] == "https://www.bilibili.com/audio/au":
        last_part = int(url[33:].replace("/", ""))
        return Audio(auid=last_part)
    else:
        return -1


def parse_audio_list(url):
    """
    解析歌单,如果不是返回 -1，否则返回对应类
    """
    if url[:33] == "https://www.bilibili.com/audio/am":
        last_part = int(url[33:].replace("/", ""))
        return AudioList(amid=last_part)
    else:
        return -1


def parse_article(url):
    """
    解析专栏,如果不是返回 -1，否则返回对应类
    """
    if url[:32] == "https://www.bilibili.com/read/cv":
        last_part = int(url[32:].replace("/", ""))
        return Article(cvid=last_part)
    else:
        return -1


def parse_user(url):
    if url[:27] == "https://space.bilibili.com/":
        num_re = re.compile(r"\d+")
        uid = num_re.findall(url)[0]
        return User(uid=uid)
    else:
        return -1


def parse_live(url):
    if url[:26] == "https://live.bilibili.com/":
        last_part = int(url[26:].replace("/", ""))
        return LiveRoom(room_display_id=last_part)
    else:
        return -1


def parse_season_series(url):
    if url[:27] == "https://space.bilibili.com/":
        uid = 0
        for i in url.split("/"):
            try:
                uid = int(i)
            except:
                pass
            if "collectiondetail" in i:
                sid = int(i[21:])
                return ChannelSeries(uid, ChannelSeriesType.SEASON, id_=sid)
            if "seriesdetail" in i:
                sid = int(i[17:])
                return ChannelSeries(uid, ChannelSeriesType.SERIES, id_=sid)
    elif url[:40] == "https://www.bilibili.com/medialist/play/":
        for i in url.split("/"):
            if "?" in i:
                uid = int(i.split("?")[0])
                params = i.split("?")[1].split("&")
                for param in params:
                    if "business_id" in param:
                        sid = int(param[12:])
                        return ChannelSeries(uid, ChannelSeriesType.SERIES, id_=sid)
    return -1


def parse_space_favorite_list(url, credential):
    if url[:27] == "https://space.bilibili.com/":
        uid = 0
        for i in url.split("/"):
            try:
                uid = int(i)
            except:
                pass
            if "favlist" in i:
                if len(i) == len("favlist"):
                    api = get_api("favorite-list")["info"]["list_list"]
                    params = {"up_mid": uid, "type": 2}

                    favorite_lists = json.loads(
                        httpx.get(
                            api["url"], params=params, cookies=credential.get_cookies()
                        ).text
                    )["data"]

                    if favorite_lists == None:
                        return -1
                    else:
                        default_favorite_list = favorite_lists["list"][0]
                        return (
                            FavoriteList(media_id=default_favorite_list["id"]),
                            ResourceType.FAVORITE_LIST,
                        )
                oid = ""
                type_ = ""
                for arg in i.split("&"):
                    if "?" in arg:
                        arg = arg.split("?")[1]
                    if "fid" in arg:
                        oid = arg[4:]
                    if "ctype" in arg:
                        type_ = int(arg[6:])
                oid_is_number = True
                try:
                    oid_int = int(oid)
                except:
                    oid_is_number = False
                if type_ == "" and oid_is_number:
                    # 我的视频收藏夹
                    oid_int = int(oid)
                    return (FavoriteList(media_id=oid_int), ResourceType.FAVORITE_LIST)
                elif type_ != "":
                    # 我的订阅
                    if type_ == 11:
                        # 收藏的收藏夹
                        oid_int = int(oid)
                        return (
                            FavoriteList(media_id=oid_int),
                            ResourceType.FAVORITE_LIST,
                        )
                    else:
                        return -1
                elif not oid_is_number:
                    # 其他类型的收藏夹
                    if oid == FavoriteListType.ARTICLE.value:
                        return (
                            FavoriteList(
                                FavoriteListType.ARTICLE, credential=credential
                            ),
                            ResourceType.FAVORITE_LIST,
                        )
                    elif oid == FavoriteListType.CHEESE.value:
                        return (
                            FavoriteList(
                                FavoriteListType.CHEESE, credential=credential
                            ),
                            ResourceType.FAVORITE_LIST,
                        )
                else:
                    return -1
            else:
                pass
    else:
        return -1
    return -1
