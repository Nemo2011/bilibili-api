"""
bilibili_api.utils.parse_link

链接资源解析。
"""

import json
import re
from enum import Enum
from typing import Literal, Tuple, Union

import httpx
from yarl import URL

from ..article import Article, ArticleList
from ..audio import Audio, AudioList
from ..bangumi import Bangumi, Episode
from ..black_room import BlackRoom
from ..cheese import CheeseVideo, CheeseList
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
    调用 yarl 解析 bilibili url 的函数。

    Args:
        url(str)              : 链接
        credential(Credential): 凭据类

    Returns:
        Tuple[obj, ResourceType]: (对象，类型) 或 -1,-1 表示出错
    """
    raw_url = url # 保留 yarl 解析前的原始链接 url
    credential = credential if credential else Credential()
    try:
        obj = None
        
        # 排除 bvxxxxxxxxxx 等缩写
        sobj = check_short_name(url, credential)
        if sobj != -1:
            sobj[0].credential = credential
            return sobj
            
        # 删去首尾部空格
        url = url.strip()
        # 添加 https: 协议头
        if url.lstrip("https:") == url:
            url = "https:" + url
        # 转换为 yarl
        url = URL(url)

        # 排除小黑屋
        black_room = parse_black_room(url)
        if not black_room == -1:
            obj = (black_room, ResourceType.BLACK_ROOM)
            return obj
            
        # 过滤 https://space.bilibili.com/
        if url.host == "space.bilibili.com" and url.path == "/" or url.path == "":
            try:
                info = await get_self_info(credential)
            except Exception as e:
                return (-1, ResourceType.FAILED)
            else:
                return (User(info["mid"], credential=credential), ResourceType.USER)
        
        channel = parse_season_series(url) # 不需要 real_url，提前处理
        if channel != -1:
            return (channel, ResourceType.CHANNEL_SERIES)

        # 不确定是否可以修改 short.py 的代码，所以先这样
        url = URL(await get_real_url(raw_url))

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
        cheese_video = await parse_cheese_video(url)
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
            return obj  # type: ignore
    except Exception as e:
        return (-1, ResourceType.FAILED)


def is_interactive_video(bvid: str, credential: Credential):
    info = httpx.get(
        "https://api.bilibili.com/x/web-interface/view",
        params={"bvid": bvid},
        cookies=credential.get_cookies()).json()
    return info["data"]["rights"]["is_stein_gate"] == 1


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
    if name[:2].upper() == "AV":
        v = Video(aid=int(name[2:]))
        bvid = v.get_bvid()
        if is_interactive_video(bvid, credential):
            return (InteractiveVideo(bvid), ResourceType.INTERACTIVE_VIDEO)
        else:
            return (v, ResourceType.VIDEO)
    elif name[:2].upper() == "BV":
        v = Video(bvid=name)
        bvid = v.get_bvid()
        if is_interactive_video(bvid, credential):
            return (InteractiveVideo(bvid), ResourceType.INTERACTIVE_VIDEO)
        else:
            return (v, ResourceType.VIDEO)
    elif name[:2].upper() == "ML":
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


def parse_video(url: URL, credential: Credential):
    """
    解析视频,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[1] == "video":
        raw_video_id = url.parts[2]
        if raw_video_id[:2].upper() == "AV":
            aid = int(raw_video_id[2:])
            v = Video(aid=aid)
            bvid = v.get_bvid()
        elif raw_video_id[:2].upper() == "BV":
            v = Video(bvid=raw_video_id)
            bvid = raw_video_id
        else:
            return -1
        if is_interactive_video(bvid=bvid, credential=credential) == 1:
            return InteractiveVideo(bvid)
        else:
            return v
    else:
        return -1


def parse_bangumi(url: URL) -> Union[Bangumi, int]:
    """
    解析番剧,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[:3] == ("/", "bangumi", "media"):
        media_id = int(url.parts[3][2:])
        return Bangumi(media_id=media_id)
    return -1


def parse_episode(url: URL, credential) -> Union[Episode, int]:
    """
    解析番剧剧集,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[1] == "bangumi" and url.parts[2] == "play":
        video_short_id = url.parts[3]

        if video_short_id[:2].upper() == "EP":
            epid = int(video_short_id[2:])
            return Episode(epid=epid)
        elif video_short_id[:2].upper() == "SS":
            try:
                resp = httpx.get(
                    str(url),
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
    return -1


def parse_favorite_list(url: URL) -> Union[FavoriteList, int]:
    """
    解析收藏夹,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[:3] == ("/", "medialist", "detail"):
        media_id = int(url.parts[3][2:])
        return FavoriteList(media_id=media_id)
    return -1


async def parse_cheese_video(url: URL) -> Union[CheeseVideo, int]:
    """
    解析课程视频,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[1] == "cheese" and url.parts[2] == "play":
        if url.parts[3][:2].upper() == "EP":
            epid = int(url.parts[3][2:])
            return CheeseVideo(epid=epid)
        elif url.parts[3][:2].upper() == "SS":
            clid = int(url.parts[3][2:])
            cl = CheeseList(season_id=clid)
            return CheeseVideo(
                epid=(await cl.get_list_raw())["items"][0]["id"]
            )
    return -1


def parse_audio(url: URL) -> Union[Audio, int]:
    """
    解析音频,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[1] == "audio":
        if url.parts[2][:2].upper() == "AU":
            auid = int(url.parts[2][2:])
            return Audio(auid=auid)
    return -1


def parse_audio_list(url: URL) -> Union[AudioList, int]:
    """
    解析歌单,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[1] == "audio":
        if url.parts[2][:2].upper() == "AM":
            amid = int(url.parts[2][2:])
            return AudioList(amid=amid)
    return -1


def parse_article(url: URL) -> Union[Article, int]:
    """
    解析专栏，如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[1] == "read" and url.parts[2][:2].upper() == "CV":
        cvid = int(url.parts[2][2:])
        return Article(cvid=cvid)
    return -1


def parse_user(url: URL) -> Union[User, int]:
    if url.host == "space.bilibili.com":
        if len(url.parts) >= 2:
            uid = url.parts[1]
            return User(uid=uid)
    return -1


def parse_live(url: URL) -> Union[LiveRoom, int]:
    if url.host == "live.bilibili.com":
        if len(url.parts) >= 2:
            room_display_id = url.parts[1]
            return LiveRoom(room_display_id=room_display_id)
    return -1


def parse_season_series(url: URL) -> Union[ChannelSeries, int]:
    if url.host == "space.bilibili.com":
        if len(url.parts) >= 2:  # path 存在 uid
            try:
                uid = int(url.parts[1])
            except:
                pass  # uid 无效
        if len(url.parts) >= 4:  # path 存在 collectiondetail 或者 seriesdetail
            if url.parts[3] == "collectiondetail":
                # https://space.bilibili.com/51537052/channel/collectiondetail?sid=22780&ctype=0
                if url.query.get("sid") is not None:
                    sid = int(url.query["sid"])
                    return ChannelSeries(uid, ChannelSeriesType.SEASON, id_=sid)
            elif url.parts[3] == "seriesdetail":
                # https://space.bilibili.com/558830935/channel/seriesdetail?sid=2972810&ctype=0 
                if url.query.get("sid") is not None:
                    sid = int(url.query["sid"])
                    return ChannelSeries(uid, ChannelSeriesType.SERIES, id_=sid)
    elif url.host == "www.bilibili.com":
        if url.parts[1] == "list": 
            # https://www.bilibili.com/list/660303135?sid=2908236 旧版合集，不需要 real_url
            if len(url.parts) >= 3 and url.query.get("sid") is not None:
                sid = int(url.query["sid"])
                uid = int(url.parts[2])
                return ChannelSeries(uid, ChannelSeriesType.SERIES, id_=sid)
        elif url.parts[1] == "medialist" and url.parts[2] == "play": # https://www.bilibili.com/medialist/play/660303135?business=space 新版合集
            if len(url.parts) >= 4:
                uid = int(url.parts[3])
            if url.query.get("business_id") is not None:
                sid = int(url.query.get("business_id"))
                return ChannelSeries(uid, ChannelSeriesType.SERIES, id_=sid)
    return -1


def parse_space_favorite_list(url: URL, credential) -> Union[FavoriteList, int]:
    if url.host == "space.bilibili.com":
        uid = url.parts[1]  # 获取 uid
        if len(url.parts) >= 3:  # path 存在 favlist
            if url.parts[2] == "favlist":
                if len(url.parts) == 3:  # query 中不存在 fid 则返回默认收藏夹
                    api = get_api("favorite-list")["info"]["list_list"]
                    params = {"up_mid": uid, "type": 2}
                    favorite_lists = httpx.get(
                        api["url"], params=params, cookies=credential.get_cookies()
                    ).json()["data"]

                    if favorite_lists == None:
                        return -1
                    else:
                        default_favorite_list = favorite_lists["list"][0]
                        return (FavoriteList(media_id=default_favorite_list["id"]), ResourceType.FAVORITE_LIST)
                elif len(url.query) != 0:
                    fid = url.query.get("fid")  # 未知数据类型
                    ctype = url.query.get("ctype")
                    try:  # 尝试转换为 int 类型并设置 fid_is_int
                        fid = int(fid)
                        fid_is_int = True
                    except:
                        fid_is_int = False

                    if ctype is None and fid_is_int:
                        # 我的视频收藏夹
                        fid = int(fid)
                        return (FavoriteList(media_id=fid), ResourceType.FAVORITE_LIST)
                    elif ctype is not None:  # 存在 ctype
                        ctype = int(url.query.get("ctype"))
                        if ctype == 11:
                            fid = int(fid)  # 转换为 int 类型
                            fid_is_int = True
                            return (
                                FavoriteList(media_id=fid),
                                ResourceType.FAVORITE_LIST,
                            )
                        else:
                            return -1  # 未知收藏夹类型
                    elif fid_is_int == False:
                        # ctype 不存在且 fid 非 int 类型
                        if fid == FavoriteListType.ARTICLE.value:
                            return (
                                FavoriteList(
                                    FavoriteListType.ARTICLE, credential=credential
                                ),
                                ResourceType.FAVORITE_LIST,
                            )
                        elif fid == FavoriteListType.CHEESE.value:
                            return (
                                FavoriteList(
                                    FavoriteListType.CHEESE, credential=credential
                                ),
                                ResourceType.FAVORITE_LIST,
                            )
    return -1


def parse_article_list(url: URL) -> Union[ArticleList, int]:
    if url.host == "www.bilibili.com" and url.parts[:3] == ("/", "read", "readlist"):
        rlid = int(url.parts[3][2:])
        return ArticleList(rlid=rlid)
    return -1


def parse_dynamic(url: URL) -> Union[Dynamic, int]:
    if url.host == "t.bilibili.com":
        if len(url.parts) >= 2:
            dynamic_id = int(url.parts[1])
            return Dynamic(dynamic_id)
    return -1


def parse_black_room(url: URL) -> Union[BlackRoom, int]:
    if len(url.parts) >= 3:
        if url.parts[:3] == ("/", "blackroom", "ban"):
            if len(url.parts) >= 4:  # 存在 id
                return BlackRoom(int(url.parts[3]))
    return -1


def parse_game(url: URL) -> Union[Game, int]:
    if url.host == "www.biligame.com" and url.parts[1] == "detail" and url.query.get("id") is not None:
        return Game(int(url.query["id"]))
    return -1


def parse_topic(url: URL) -> Union[Topic, int]:
    if url.host == "www.bilibili.com" and url.parts[:4] == ("/", "v", "topic", "detail") and url.query.get("topic_id") is not None:
        return Topic(
            int(url.query["topic_id"])
        )
    return -1


def parse_manga(url: URL) -> Union[Manga, int]:
    if url.host == "manga.bilibili.com" and url.parts[1] == "detail":
        return Manga(
            int(url.parts[2][2:])
        )
    return -1


def parse_album(url: URL) -> Union[Album, int]:
    if url.host == "h.bilibili.com":
        return Album(int(url.parts[1]))
    return -1


def parse_bnj(url: URL) -> Union[Video, int]:
    # https://www.bilibili.com/festival/2023bnj?bvid=BV1ZY4y1f79x&spm_id_from=333.999.0.0
    bvid = url.query.get("bvid")
    if bvid is not None:
        return Video(bvid)
    return -1