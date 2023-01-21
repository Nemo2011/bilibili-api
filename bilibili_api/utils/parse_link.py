"""
bilibili_api.utils.parse_link

链接资源解析。
"""

import json
import re
from enum import Enum
from typing import Literal, Tuple, Union

import httpx

from ..article import Article, ArticleList
from ..audio import Audio, AudioList
from ..bangumi import Bangumi, Episode
from ..black_room import BlackRoom
from ..cheese import CheeseVideo
from ..dynamic import Dynamic
from ..exceptions import *
from ..favorite_list import FavoriteList, FavoriteListType
from ..interactive_video import InteractiveVideo
from ..live import LiveRoom
from ..user import ChannelSeries, ChannelSeriesType, User, get_self_info
from ..video import Video
from ..game import Game
from .Credential import Credential
from .short import get_real_url
from .utils import get_api
from ..topic import Topic
from ..manga import Manga
from ..album import Album


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
    + BLACK_ROOM: 小黑屋
    + GAME: 游戏
    + TOPIC: 话题
    + MANGA: 漫画
    + ALBUM: 相簿
    + FAILED: 错误
    """

    VIDEO = "video"
    INTERACTIVE_VIDEO = "interactive_video"
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
    ARTICLE_LIST = "article_list"
    DYNAMIC = "dynamic"
    BLACK_ROOM = "black_room"
    GAME = "game"
    TOPIC = "topic"
    MANGA = "manga"
    ALBUM = "album"
    FAILED = "failed"


async def parse_link(
    url: str,
    credential: Union[Credential, None] = None
) -> Union[
    Tuple[Video, Literal[ResourceType.VIDEO]],
    Tuple[InteractiveVideo, Literal[ResourceType.INTERACTIVE_VIDEO]],
    Tuple[Bangumi, Literal[ResourceType.BANGUMI]],
    Tuple[Episode, Literal[ResourceType.EPISODE]],
    Tuple[FavoriteList, Literal[ResourceType.FAVORITE_LIST]],
    Tuple[CheeseVideo, Literal[ResourceType.CHEESE_VIDEO]],
    Tuple[Audio, Literal[ResourceType.AUDIO]],
    Tuple[AudioList, Literal[ResourceType.AUDIO_LIST]],
    Tuple[Article, Literal[ResourceType.ARTICLE]],
    Tuple[User, Literal[ResourceType.USER]],
    Tuple[LiveRoom, Literal[ResourceType.LIVE]],
    Tuple[ChannelSeries, Literal[ResourceType.CHANNEL_SERIES]],
    Tuple[ArticleList, Literal[ResourceType.ARTICLE_LIST]],
    Tuple[Dynamic, Literal[ResourceType.DYNAMIC]],
    Tuple[BlackRoom, Literal[ResourceType.BLACK_ROOM]],
    Tuple[Game, Literal[ResourceType.GAME]],
    Tuple[Topic, Literal[ResourceType.TOPIC]],
    Tuple[Manga, Literal[ResourceType.MANGA]],
    Tuple[Album, Literal[ResourceType.ALBUM]],
    Tuple[Literal[-1], Literal[ResourceType.FAILED]]
]:
    """
    解析 bilibili url 的函数。

    Args:
        url(str)              : 链接
        credential(Credential): 凭据类

    Returns:
        Tuple[obj, ResourceType]: (对象，类型) 或 -1,-1 表示出错
    """
    url = url.lstrip().rstrip()
    credential = credential if credential else Credential()
    try:
        obj = None

        sobj = check_short_name(url, credential)
        if sobj != -1:
            sobj[0].credential = credential
            return sobj

        if url.upper().startswith("BV") or url.upper().startswith("AV"):
            url = "https://www.bilibili.com/video/" + url
            # 视频缩写形式直接补充为完整形式，以便后面跳转链接解析

        black_room = parse_black_room(url)
        if not black_room == -1:
            obj = (black_room, ResourceType.BLACK_ROOM)
            return obj

        url = await get_real_url(url)

        # 特殊处理，因为后面会过滤参数，这几项需要参数完成
        channel = parse_season_series(url)
        if channel != -1:
            return (channel, ResourceType.CHANNEL_SERIES)
        fl_space = parse_space_favorite_list(url, credential)
        if fl_space != -1:
            return fl_space
        game = parse_game(url)
        if game != -1:
            game.credential = credential
            return (game, ResourceType.GAME)
        topic = parse_topic(url)
        if topic != -1:
            topic.credential = credential
            return (topic, ResourceType.TOPIC)
        bnj_video = parse_bnj(url)
        if bnj_video != -1:
            bnj_video.credential = credential
            return (bnj_video, ResourceType.VIDEO)

        # 过滤参数
        url = url.split("?")[0]
        if url == "https://space.bilibili.com":
            try:
                info = await get_self_info(credential)
            except:
                return (-1, ResourceType.FAILED)
            else:
                return (User(info["mid"], credential=credential), ResourceType.USER)
        obj = None
        video = parse_video(url, credential)
        if not video == -1:
            if isinstance(video, InteractiveVideo):
                obj = (video, ResourceType.INTERACTIVE_VIDEO)
            else:
                obj = (video, ResourceType.VIDEO)
        bangumi = parse_bangumi(url)
        if not bangumi == -1:
            obj = (bangumi, ResourceType.BANGUMI)
        episode = parse_episode(url, credential)
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
        article_list = parse_article_list(url)
        if not article_list == -1:
            obj = (article_list, ResourceType.ARTICLE_LIST)
        user = parse_user(url)
        if not user == -1:
            obj = (user, ResourceType.USER)
        live = parse_live(url)
        if not live == -1:
            obj = (live, ResourceType.LIVE)
        dynamic = parse_dynamic(url)
        if not dynamic == -1:
            obj = (dynamic, ResourceType.DYNAMIC)
        manga = parse_manga(url)
        if not manga == -1:
            obj = (manga, ResourceType.MANGA)
        album = parse_album(url)
        if not album == -1:
            obj = (album, ResourceType.ALBUM)

        if obj == None or obj[0] == None:
            return (-1, ResourceType.FAILED)
        else:
            obj[0].credential = credential
            return obj # type: ignore
    except Exception as e:
        return (-1, ResourceType.FAILED)


def check_short_name(name: str, credential: Credential):
    """
    解析:
      - mlxxxxxxxxxx
      - uidxxxxxxxxx
      - cvxxxxxxxxxx
      - auxxxxxxxxxx
      - amxxxxxxxxxx
      - rlxxxxxxxxxx
    """
    if name[:2].upper() == "ML":
        return (
            FavoriteList(FavoriteListType.VIDEO, int(name[2:])),
            ResourceType.FAVORITE_LIST,
        )
    elif name[:3].upper() == "UID":
        return (User(int(name[3:])), ResourceType.USER)
    elif name[:2].upper() == "CV":
        return (Article(int(name[2:])), ResourceType.ARTICLE)
    elif name[:2].upper() == "AU":
        return (Audio(int(name[2:])), ResourceType.AUDIO)
    elif name[:2].upper() == "AM":
        return (AudioList(int(name[2:])), ResourceType.AUDIO_LIST)
    elif name[:2].upper() == "RL":
        return (ArticleList(int(name[2:])), ResourceType.ARTICLE_LIST)
    else:
        return -1


def parse_video(url, credential: Credential):
    """
    解析视频,如果不是返回 -1，否则返回对应类
    """
    if url[:31] == "https://www.bilibili.com/video/":
        last_part = url[31:]
        if last_part[:2].upper() == "AV":
            aid = int(last_part[2:].replace("/", ""))
            v = Video(aid=aid)
        elif last_part[:2].upper() == "BV":
            bvid = "BV" + last_part[2:].replace("/", "")
            v = Video(bvid=bvid)
        else:
            return -1
        info = json.loads(
            httpx.get(
                "https://api.bilibili.com/x/web-interface/view",
                params={"bvid": v.get_bvid()},
                cookies=credential.get_cookies(),
            ).text
        )
        is_interactive = info["data"]["rights"]["is_stein_gate"]
        if is_interactive == 1:
            return InteractiveVideo(v.get_bvid())
        else:
            return v
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


def parse_episode(url, credential):
    """
    解析番剧剧集,如果不是返回 -1，否则返回对应类
    """
    if url[:38] == "https://www.bilibili.com/bangumi/play/":
        last_part = url[38:]
        if last_part[:2].upper() == "EP":
            epid = int(last_part[2:].replace("/", ""))
            return Episode(epid=epid)
        elif last_part[:2].upper() == "SS":
            try:
                resp = httpx.get(
                    url,
                    cookies=credential.get_cookies(),
                    headers={"User-Agent": "Mozilla/5.0"},
                )
            except Exception as e:
                raise ResponseException(str(e))
            else:
                content = resp.text

                pattern = re.compile(r"window.__INITIAL_STATE__=(\{.*?\});")
                match = re.search(pattern, content)
                if match is None:
                    raise ApiException("未找到番剧信息")
                try:
                    content = json.loads(match.group(1))
                except json.JSONDecodeError:
                    raise ApiException("信息解析错误")
                else:
                    epid = content["epInfo"]["id"]
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
                if (type_ == "" or type_ == 21) and oid_is_number:
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


def parse_article_list(url):
    if url[:41] == "https://www.bilibili.com/read/readlist/rl":
        last_part = int(url[41:].replace("/", ""))
        return ArticleList(last_part)
    else:
        return -1


def parse_dynamic(url):
    if url[:23] == "https://t.bilibili.com/":
        last_part = url[23:].replace("/", "")
        if last_part == "":
            return -1
        else:
            return Dynamic(int(last_part))
    else:
        return -1


def parse_black_room(url: str):
    if url.lstrip("https:") == url:
        url = "https:" + url
    if url[:39] == "https://www.bilibili.com/blackroom/ban/":
        last_part = url[39:].replace("/", "")
        if last_part == "":
            return -1
        else:
            return BlackRoom(int(last_part))
    else:
        return -1


def parse_game(url: str):
    if url[:36] == "https://www.biligame.com/detail/?id=":
        return Game(int(url[36:]))
    else:
        return -1


def parse_topic(url: str):
    if url[:50] == "https://www.bilibili.com/v/topic/detail/?topic_id=":
        return Topic(
            int(url[50:].split("&")[0])
        )
    else:
        return -1


def parse_manga(url: str):
    if url[:36] == "https://manga.bilibili.com/detail/mc":
        return Manga(
            int(url[36:].replace("/", ""))
        )
    else:
        return -1


def parse_album(url: str):
    if url[:23] == "https://h.bilibili.com/":
        return Album(
            int(url[23:].replace("/", ""))
        )
    else:
        return -1


def parse_bnj(url: str):
    # https://www.bilibili.com/festival/2023bnj?bvid=BV1ZY4y1f79x&spm_id_from=333.999.0.0
    try:
        args = url.split("?")[1].split("&")
        for arg in args:
            if "bvid=" in arg:
                return Video(
                    arg.split("=")[1]
                )
        return -1
    except:
        return -1
