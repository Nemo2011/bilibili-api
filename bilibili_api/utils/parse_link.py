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
from ..note import Note, NoteType
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
    + NOTE: 笔记
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
    NOTE = "note"
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
    Tuple[Note, Literal[ResourceType.NOTE]],
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
    credential = credential if credential else Credential()
    try:
        obj = None

        # 排除 bvxxxxxxxxxx 等缩写
        sobj = await check_short_name(url, credential)
        if sobj != -1:
            sobj[0].credential = credential
            return sobj # type: ignore

        # 删去首尾部空格
        url = url.strip()
        # 添加 https: 协议头
        if url.lstrip("https:") == url:
            url = "https:" + url

        # 转换为 yarl
        url = URL(url) # type: ignore

        # 排除小黑屋
        black_room = parse_black_room(url, credential) # type: ignore
        if not black_room == -1:
            obj = (black_room, ResourceType.BLACK_ROOM)
            return obj # type: ignore

        # 过滤 https://space.bilibili.com/
        if url.host == "space.bilibili.com" and url.path == "/" or url.path == "": # type: ignore
            try:
                info = await get_self_info(credential)
            except Exception as e:
                return (-1, ResourceType.FAILED)
            else:
                return (User(info["mid"], credential=credential), ResourceType.USER)

        channel = parse_season_series(url, credential) # 不需要 real_url，提前处理 # type: ignore
        if channel != -1:
            return (channel, ResourceType.CHANNEL_SERIES) # type: ignore

        url = await get_real_url(str(url)) # type: ignore
        url = URL(url) # type: ignore

        fl_space = parse_space_favorite_list(url, credential) # type: ignore
        if fl_space != -1:
            return fl_space # type: ignore
        game = parse_game(url, credential) # type: ignore
        if game != -1:
            game.credential = credential # type: ignore
            return (game, ResourceType.GAME) # type: ignore
        topic = parse_topic(url, credential) # type: ignore
        if topic != -1:
            topic.credential = credential # type: ignore
            return (topic, ResourceType.TOPIC) # type: ignore
        bnj_video = parse_bnj(url, credential) # type: ignore
        if bnj_video != -1:
            bnj_video.credential = credential # type: ignore
            return (bnj_video, ResourceType.VIDEO) # type: ignore
        note = parse_note(url, credential) # type: ignore
        if note != -1:
            return (note, ResourceType.NOTE) # type: ignore


        obj = None
        video = await parse_video(url, credential) # type: ignore
        if not video == -1:
            obj = video # auto_convert_video 会判断类型
        bangumi = parse_bangumi(url, credential) # type: ignore
        if not bangumi == -1:
            obj = (bangumi, ResourceType.BANGUMI)
        episode = parse_episode(url, credential) # type: ignore
        if not episode == -1:
            obj = (episode, ResourceType.EPISODE)
        favorite_list = parse_favorite_list(url, credential) # type: ignore
        if not favorite_list == -1:
            obj = (favorite_list, ResourceType.FAVORITE_LIST)
        cheese_video = await parse_cheese_video(url, credential) # type: ignore
        if not cheese_video == -1:
            obj = (cheese_video, ResourceType.CHEESE_VIDEO)
        audio = parse_audio(url, credential) # type: ignore
        if not audio == -1:
            obj = (audio, ResourceType.AUDIO)
        audio_list = parse_audio_list(url, credential) # type: ignore
        if not audio_list == -1:
            obj = (audio_list, ResourceType.AUDIO_LIST)
        article = parse_article(url, credential) # type: ignore
        if not article == -1:
            obj = (article, ResourceType.ARTICLE)
        article_list = parse_article_list(url, credential) # type: ignore
        if not article_list == -1:
            obj = (article_list, ResourceType.ARTICLE_LIST)
        user = parse_user(url, credential) # type: ignore
        if not user == -1:
            obj = (user, ResourceType.USER)
        live = parse_live(url, credential) # type: ignore
        if not live == -1:
            obj = (live, ResourceType.LIVE)
        dynamic = parse_dynamic(url, credential) # type: ignore
        if not dynamic == -1:
            obj = (dynamic, ResourceType.DYNAMIC)
        manga = parse_manga(url, credential) # type: ignore
        if not manga == -1:
            obj = (manga, ResourceType.MANGA)
        album = parse_album(url, credential) # type: ignore
        if not album == -1:
            obj = (album, ResourceType.ALBUM)

        if obj == None or obj[0] == None:
            return (-1, ResourceType.FAILED)
        else:
            obj[0].credential = credential # type: ignore
            return obj  # type: ignore
    except Exception as e:
        raise e
        return (-1, ResourceType.FAILED)


async def auto_convert_video(video: Video, credential: Union[Credential, None] = None) -> Tuple[Union[Video, Episode, InteractiveVideo], ResourceType]:
    # check interactive video
    video_info = await video.get_info()
    if video_info["rights"]["is_stein_gate"] == 1:
        return (InteractiveVideo(video.get_bvid(), credential=credential), ResourceType.INTERACTIVE_VIDEO)

    # check episode
    if "redirect_url" in video_info:
        reparse_link = await parse_link(await get_real_url(video_info["redirect_url"]), credential=credential) # type: ignore
        return reparse_link # type: ignore

    # return video
    return (video, ResourceType.VIDEO)

async def check_short_name(
    name: str,
    credential: Credential
) -> Union[
    Tuple[Video, Literal[ResourceType.VIDEO]],
    Tuple[Episode, Literal[ResourceType.EPISODE]],
    Tuple[CheeseVideo, Literal[ResourceType.CHEESE_VIDEO]],
    Tuple[FavoriteList, Literal[ResourceType.FAVORITE_LIST]],
    Tuple[User, Literal[ResourceType.USER]],
    Tuple[Article, Literal[ResourceType.ARTICLE]],
    Tuple[Audio, Literal[ResourceType.AUDIO]],
    Tuple[AudioList, Literal[ResourceType.AUDIO_LIST]],
    Tuple[ArticleList, Literal[ResourceType.ARTICLE_LIST]],
    Literal[-1]
]:
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
        v = Video(aid=int(name[2:]), credential=credential)
        return await auto_convert_video(v, credential=credential) # type: ignore
    elif name[:2].upper() == "BV":
        v = Video(bvid=name, credential=credential)
        return await auto_convert_video(v, credential=credential) # type: ignore
    elif name[:2].upper() == "ML":
        return (
            FavoriteList(FavoriteListType.VIDEO, int(name[2:]), credential=credential),
            ResourceType.FAVORITE_LIST,
        )
    elif name[:3].upper() == "UID":
        return (User(int(name[3:]), credential=credential), ResourceType.USER)
    elif name[:2].upper() == "CV":
        return (Article(int(name[2:]), credential=credential), ResourceType.ARTICLE)
    elif name[:2].upper() == "AU":
        return (Audio(int(name[2:]), credential=credential), ResourceType.AUDIO)
    elif name[:2].upper() == "AM":
        return (AudioList(int(name[2:]), credential=credential), ResourceType.AUDIO_LIST)
    elif name[:2].upper() == "RL":
        return (ArticleList(int(name[2:]), credential=credential), ResourceType.ARTICLE_LIST)
    else:
        return -1


async def parse_video(url: URL, credential: Credential) -> Union[Tuple[Union[Video, Episode, InteractiveVideo], ResourceType], Literal[-1]]:
    """
    解析视频,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[1] == "video":
        raw_video_id = url.parts[2]
        if raw_video_id[:2].upper() == "AV":
            aid = int(raw_video_id[2:])
            v = Video(aid=aid, credential=credential)
        elif raw_video_id[:2].upper() == "BV":
            v = Video(bvid=raw_video_id, credential=credential)
        else:
            return -1
        return await auto_convert_video(v, credential=credential)
    else:
        return -1


def parse_bangumi(url: URL, credential: Credential) -> Union[Bangumi, int]:
    """
    解析番剧,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and len(url.parts) >= 4:
        if url.parts[:3] == ("/", "bangumi", "media"):
            media_id = int(url.parts[3][2:])
            return Bangumi(media_id=media_id, credential=credential)
    return -1


def parse_episode(url: URL, credential: Credential) -> Union[Episode, int]:
    """
    解析番剧剧集,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and len(url.parts) >= 3:
        if url.parts[1] == "bangumi" and url.parts[2] == "play":
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
                        return Episode(epid=epid, credential=credential)
    return -1


def parse_favorite_list(url: URL, credential: Credential) -> Union[FavoriteList, int]:
    """
    解析收藏夹,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and len(url.parts) >= 4:
        if url.parts[:3] == ("/", "medialist", "detail"):
            media_id = int(url.parts[3][2:])
            return FavoriteList(media_id=media_id, credential=credential)
    return -1


async def parse_cheese_video(url: URL, credential: Credential) -> Union[CheeseVideo, int]:
    """
    解析课程视频,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and len(url.parts) >=4:
        if url.parts[1] == "cheese" and url.parts[2] == "play":
            if url.parts[3][:2].upper() == "EP":
                epid = int(url.parts[3][2:])
                return CheeseVideo(epid=epid, credential=credential)
            elif url.parts[3][:2].upper() == "SS":
                clid = int(url.parts[3][2:])
                cl = CheeseList(season_id=clid, credential=credential)
                return CheeseVideo(
                    epid=(await cl.get_list_raw())["items"][0]["id"], credential=credential
            )
    return -1


def parse_audio(url: URL, credential: Credential) -> Union[Audio, int]:
    """
    解析音频,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[1] == "audio":
        if url.parts[2][:2].upper() == "AU":
            auid = int(url.parts[2][2:])
            return Audio(auid=auid, credential=credential)
    return -1


def parse_audio_list(url: URL, credential: Credential) -> Union[AudioList, int]:
    """
    解析歌单,如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and url.parts[1] == "audio":
        if url.parts[2][:2].upper() == "AM":
            amid = int(url.parts[2][2:])
            return AudioList(amid=amid, credential=credential)
    return -1


def parse_article(url: URL, credential: Credential) -> Union[Article, int]:
    """
    解析专栏，如果不是返回 -1，否则返回对应类
    """
    if url.host == "www.bilibili.com" and len(url.parts) >= 3:
        if url.parts[1] == "read" and url.parts[2][:2].upper() == "CV":
            cvid = int(url.parts[2][2:])
            return Article(cvid=cvid, credential=credential)
    return -1


def parse_user(url: URL, credential: Credential) -> Union[User, int]:
    if url.host == "space.bilibili.com":
        if len(url.parts) >= 2:
            uid = url.parts[1]
            return User(uid=int(uid), credential=credential)
    return -1


def parse_live(url: URL, credential: Credential) -> Union[LiveRoom, int]:
    if url.host == "live.bilibili.com":
        if len(url.parts) >= 2:
            room_display_id = int(url.parts[1])
            return LiveRoom(room_display_id=room_display_id, credential=credential)
    return -1


def parse_season_series(url: URL, credential: Credential) -> Union[ChannelSeries, int]:
    if url.host == "space.bilibili.com":
        if len(url.parts) >= 2:  # path 存在 uid
            try:
                uid = int(url.parts[1])
            except:
                pass  # uid 无效
            else:
                if len(url.parts) >= 4:  # path 存在 collectiondetail 或者 seriesdetail
                    if url.parts[3] == "collectiondetail":
                        # https://space.bilibili.com/51537052/channel/collectiondetail?sid=22780&ctype=0
                        if url.query.get("sid") is not None:
                            sid = int(url.query["sid"])
                            return ChannelSeries(uid, ChannelSeriesType.SEASON, id_=sid, credential=credential)
                    elif url.parts[3] == "seriesdetail":
                        # https://space.bilibili.com/558830935/channel/seriesdetail?sid=2972810&ctype=0
                        if url.query.get("sid") is not None:
                            sid = int(url.query["sid"])
                            return ChannelSeries(uid, ChannelSeriesType.SERIES, id_=sid, credential=credential)
    elif url.host == "www.bilibili.com":
        if url.parts[1] == "list":
            # https://www.bilibili.com/list/660303135?sid=2908236 旧版合集，不需要 real_url
            if len(url.parts) >= 3:
                uid = int(url.parts[2])
                if "sid" in url.query:
                    sid = int(url.query["sid"])
                    return ChannelSeries(uid, ChannelSeriesType.SERIES, id_=sid, credential=credential)
        # https://www.bilibili.com/medialist/play/660303135?business=space 新版合集
        elif url.parts[1] == "medialist" and url.parts[2] == "play":
            if len(url.parts) >= 4:
                uid = int(url.parts[3])
                if "business_id" in url.query:
                    sid = int(url.query["business_id"])
                    return ChannelSeries(uid, ChannelSeriesType.SERIES, id_=sid, credential=credential)
    return -1


def parse_space_favorite_list(url: URL, credential: Credential) -> Union[Tuple[FavoriteList, ResourceType], Tuple[ChannelSeries, ResourceType], Literal[-1]]:
    if url.host == "space.bilibili.com":
        uid = url.parts[1]  # 获取 uid
        if len(url.parts) >= 3:  # path 存在 favlist
            if url.parts[2] == "favlist":
                if len(url.parts) == 3 and url.query.get("fid") == None:  # query 中不存在 fid 则返回默认收藏夹
                    api = get_api("favorite-list")["info"]["list_list"]
                    params = {"up_mid": uid, "type": 2}
                    favorite_lists = httpx.get(
                        api["url"], params=params, cookies=credential.get_cookies()
                    ).json()["data"]

                    if favorite_lists == None:
                        return -1
                    else:
                        default_favorite_id = int(favorite_lists["list"][0]["id"])
                        return (FavoriteList(media_id=default_favorite_id, credential=credential), ResourceType.FAVORITE_LIST)

                elif len(url.query) != 0:
                    fid = url.query.get("fid")  # 未知数据类型
                    ctype = url.query.get("ctype")
                    try:  # 尝试转换为 int 类型并设置 fid_is_int
                        fid = int(fid) # type: ignore
                        fid_is_int = True
                    except:
                        fid_is_int = False
                    if ctype is None and fid_is_int:
                        # 我的视频收藏夹
                        fid = int(fid) # type: ignore
                        return (FavoriteList(media_id=fid), ResourceType.FAVORITE_LIST)
                    elif fid_is_int:
                        if int(ctype) == 11: # type: ignore
                            fid = int(fid)  # 转换为 int 类型 # type: ignore
                            fid_is_int = True
                            return (
                                FavoriteList(media_id=fid, credential=credential),
                                ResourceType.FAVORITE_LIST,
                            )
                        elif int(ctype) == 21: # type: ignore
                            fid = int(fid) # type: ignore
                            fid_is_int = True
                            return (
                                ChannelSeries(id_=fid, type_=ChannelSeriesType.SEASON, credential=credential),
                                ResourceType.CHANNEL_SERIES
                            )
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


def parse_article_list(url: URL, credential: Credential) -> Union[ArticleList, int]:
    if url.host == "www.bilibili.com" and len(url.parts) >= 3:
        if url.parts[:3] == ("/", "read", "readlist"):
            rlid = int(url.parts[3][2:])
            return ArticleList(rlid=rlid, credential=credential)
    return -1


def parse_dynamic(url: URL, credential: Credential) -> Union[Dynamic, int]:
    if url.host == "t.bilibili.com":
        if len(url.parts) >= 2:
            dynamic_id = int(url.parts[1])
            return Dynamic(dynamic_id, credential=credential)
    return -1


def parse_black_room(url: URL, credential: Credential) -> Union[BlackRoom, int]:
    if len(url.parts) >= 3:
        if url.parts[:3] == ("/", "blackroom", "ban"):
            if len(url.parts) >= 4:  # 存在 id
                return BlackRoom(int(url.parts[3]), credential=credential)
    return -1


def parse_game(url: URL, credential: Credential) -> Union[Game, int]:
    if url.host == "www.biligame.com" and url.parts[1] == "detail" and url.query.get("id") is not None:
        return Game(int(url.query["id"]), credential=credential)
    return -1


def parse_topic(url: URL, credential: Credential) -> Union[Topic, int]:
    if url.host == "www.bilibili.com" and len(url.parts) >= 4:
        if url.parts[:4] == ("/", "v", "topic", "detail") and url.query.get("topic_id") is not None:

            return Topic(
                int(url.query["topic_id"]), credential=credential
            )
    return -1


def parse_manga(url: URL, credential: Credential) -> Union[Manga, int]:
    if url.host == "manga.bilibili.com" and url.parts[1] == "detail":
        return Manga(
            int(url.parts[2][2:]), credential=credential
        )
    return -1


def parse_album(url: URL, credential: Credential) -> Union[Album, int]:
    if url.host == "h.bilibili.com":
        return Album(int(url.parts[1]), credential=credential)
    return -1


def parse_bnj(url: URL, credential: Credential) -> Union[Video, int]:
    # https://www.bilibili.com/festival/2023bnj?bvid=BV1ZY4y1f79x&spm_id_from=333.999.0.0
    bvid = url.query.get("bvid")
    if bvid is not None:
        return Video(bvid, credential=credential)
    return -1


def parse_note(url: URL, credential: Credential) -> Union[Note, int]:
    # https://www.bilibili.com/h5/note-app/view?cvid=21385583
    if url.host == "www.bilibili.com" and url.parts[1:4] == ("h5", "note-app", "view"):
        if url.query.get("cvid") == None:
            return -1
        return Note(cvid=int(url.query.get("cvid")), note_type=NoteType.PUBLIC, credential=credential) # type: ignore
    return -1
