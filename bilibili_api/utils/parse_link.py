"""
bilibili_api.utils.parse_link

链接资源解析。
"""

from enum import Enum

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
    + CHANNEL_SERIES: 用户合集与列表
    """
    VIDEO = "video"
    BANGUMI = "bangumi"
    EPISODE = "episode"
    FAVORITE_LIST = "favorite_list"
    CHEESE = "cheese"
    CHEESE_VIDEO = "cheese_video"
    AUDIO = "audio"
    AUDIO_LIST = "audio_list"
    ARTICLE = "article"
    CHANNEL_SERIES = "channel_series"
