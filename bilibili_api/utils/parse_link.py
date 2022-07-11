"""
bilibili_api.utils.parse_link

链接资源解析。
"""

from enum import Enum
from importlib.resources import Resource
from bilibili_api.article import Article
from bilibili_api.audio import Audio, AudioList

from bilibili_api.bangumi import Bangumi, Episode
from bilibili_api.cheese import CheeseList, CheeseVideo
from bilibili_api.favorite_list import VideoFavoriteList
from bilibili_api.user import User
from bilibili_api.utils.Credential import Credential
from bilibili_api.utils.sync import sync
from bilibili_api.user import get_self_info
from .short import get_real_url
from ..video import Video
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

async def parse_link(url, credential: Credential=None):
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
        url = await get_real_url(url)
        url = url.split("?")[0]
        if url == "https://space.bilibili.com":
            print(get_self_info(credential))
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
        
        if obj == None:
            return -1
        else:
            obj[0].credential = credential
            return obj
    except Exception as e:
        print(e)
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
    if url[:41] == 'https://www.bilibili.com/bangumi/media/md':
        last_part = url[41:].replace("/", "")
        media_id = int(last_part)
        return Bangumi(media_id=media_id)
    else:
        return -1

def parse_episode(url):
    """
    解析番剧剧集,如果不是返回 -1，否则返回对应类
    """
    if url[:38] == 'https://www.bilibili.com/bangumi/play/':
        last_part = url[38:]
        if last_part[:2].upper() == "SS":
            ssid = int(last_part[2:].replace("/", ""))
            b = Bangumi(ssid=ssid)
            first_episode_id = int(sync(b.get_episode_list())['main_section']['episodes'][0]['share_url'][40:])
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
    if url[:44] == 'https://www.bilibili.com/medialist/detail/ml':
        last_part = int(url[44:].replace("/", ""))
        return VideoFavoriteList(media_id=last_part)
    else:
        return -1

def parse_cheese_video(url):
    """
    解析课程视频,如果不是返回 -1，否则返回对应类
    """
    if url[:37] == 'https://www.bilibili.com/cheese/play/':
        if url[37:39].upper() == "EP":
            last_part = int(url[39:].replace("/", ""))
            return CheeseVideo(epid=last_part)
        elif url[37:39].upper() == "SS":
            cheese = CheeseList(season_id=int(url[39:].replace("/", "")))
            ep = sync(cheese.get_list())['items'][0]['id']
            return CheeseVideo(epid=ep)
    else:
        return -1

def parse_audio(url):
    """
    解析音频,如果不是返回 -1，否则返回对应类
    """
    if url[:33] == 'https://www.bilibili.com/audio/au':
        last_part = int(url[33:].replace("/", ""))
        return Audio(auid=last_part)
    else:
        return -1

def parse_audio_list(url):
    """
    解析歌单,如果不是返回 -1，否则返回对应类
    """
    if url[:33] == 'https://www.bilibili.com/audio/am':
        last_part = int(url[33:].replace("/", ""))
        return AudioList(amid=last_part)
    else:
        return -1

def parse_article(url):
    """
    解析专栏,如果不是返回 -1，否则返回对应类
    """
    if url[:32] == 'https://www.bilibili.com/read/cv':
        last_part = int(url[32:].replace("/", ""))
        return Article(cvid=last_part)
    else:
        return -1

def parse_user(url):
    if url[:27] == 'https://space.bilibili.com/':
        num_re = re.compile(r"\d+")
        uid = num_re.findall(url)[0]
        return User(uid=uid)
    else:
        return -1
