"""
bilibili_api.audio_uploader

音频上传
"""

import asyncio
import os
import json
import time
from enum import Enum
from typing import List, Union, Optional
from dataclasses import dataclass, field

from . import user
from .utils.upos import UposFile, UposFileUploader
from .utils.utils import get_api
from .utils.picture import Picture
from .utils.AsyncEvent import AsyncEvent
from .utils.credential import Credential
from .exceptions.ApiException import ApiException
from .utils.network import Api, get_session, HEADERS
from .exceptions.NetworkException import NetworkException

from enum import Enum

_API = get_api("audio_uploader")


class SongCategories:
    class ContentType(Enum):  # cr_type
        """
        内容类型

        + MUSIC: 音乐
        + AUDIO_PROGRAM: 有声节目
        """

        MUSIC = 1
        AUDIO_PROGRAM = 2

    class CreationType(Enum):
        """
        创作类型

        + ORIGINAL: 原创
        + COVER: 翻唱/翻奏
        + REMIX: 改编/remix
        """

        ORIGINAL = 1
        COVER = 2
        REMIX = 48

    class SongType(Enum):
        """
        声音类型

        + HUMAN_SINGING: 人声演唱
        + VOCALOID: VOCALOID歌手
        + HUMAN_GHOST: 人力鬼畜
        + PURE_MUSIC: 纯音乐/演奏
        """

        HUMAN_SINGING = 3
        VOCALOID = 4
        HUMAN_GHOST = 5
        PURE_MUSIC = 6

    class Style(Enum):
        """
        音乐风格

        + POP: 流行
        + ANCIENT: 古风
        + ROCK: 摇滚
        + FOLK: 民谣
        + ELECTRONIC: 电子
        + DANCE: 舞曲
        + RAP: 说唱
        + LIGHT_MUSIC: 轻音乐
        + ACAPELLA: 阿卡贝拉
        + JAZZ: 爵士
        + COUNTRY: 乡村
        + RNB_SOUL: R&B/Soul
        + CLASSICAL: 古典
        + ETHNIC: 民族
        + BRITISH: 英伦
        + METAL: 金属
        + PUNK: 朋克
        + BLUES: 蓝调
        + REGGAE: 雷鬼
        + WORLD_MUSIC: 世界音乐
        + LATIN: 拉丁
        + ALTERNATIVE_INDEPENDENT: 另类/独立
        + NEW_AGE: New Age
        + POST_ROCK: 后摇
        + BOSSA_NOVA: Bossa Nova
        """

        POP = 7
        ANCIENT = 8
        ROCK = 9
        FOLK = 10
        ELECTRONIC = 11
        DANCE = 12
        RAP = 13
        LIGHT_MUSIC = 14
        ACAPELLA = 15
        JAZZ = 16
        COUNTRY = 17
        RNB_SOUL = 18
        CLASSICAL = 19
        ETHNIC = 20
        BRITISH = 21
        METAL = 22
        PUNK = 23
        BLUES = 24
        REGGAE = 25
        WORLD_MUSIC = 26
        LATIN = 27
        ALTERNATIVE_INDEPENDENT = 28
        NEW_AGE = 29
        POST_ROCK = 30
        BOSSA_NOVA = 31

    class Language(Enum):
        """
        语言

        + CHINESE: 华语
        + JAPANESE: 日语
        + ENGLISH: 英语
        + KOREAN: 韩语
        + CANTONESE: 粤语
        + OTHER_LANGUAGES: 其他语种
        """

        CHINESE = 32
        JAPANESE = 33
        ENGLISH = 34
        KOREAN = 35
        CANTONESE = 36
        OTHER_LANGUAGES = 37

    class Theme(Enum):
        """
        主题

        + ANIMATION: 动画
        + GAME: 游戏
        + FILM_AND_TELEVISION: 影视
        + INTERNET_SONG: 网络歌曲
        + SECOND_CREATION: 同人
        + IDOL: 偶像
        """

        ANIMATION = 38
        GAME = 39
        FILM_AND_TELEVISION = 40
        INTERNET_SONG = 41
        SECOND_CREATION = 42
        IDOL = 43

    class AudioType(Enum):
        """
        有声节目类型

        + RADIO_DRAMA: 广播剧
        + AUDIO_STORY: 有声故事
        + OTHER: 其他
        """

        RADIO_DRAMA = 44
        AUDIO_STORY = 45
        OTHER = 47


class CompilationCategories:
    class SongType(Enum):
        """
        声音类型

        + HUMAN_SINGING: 人声演唱
        + VOCALOID_SINGER: VOCALOID歌手
        + HUMAN_KICHUKU: 人力鬼畜
        + PURE_MUSIC: 纯音乐
        """

        HUMAN_SINGING = 102
        VOCALOID_SINGER = 103
        HUMAN_KICHUKU = 104
        PURE_MUSIC = 105

    class CreationType(Enum):
        """
        创作类型

        + ORIGINAL: 原创
        + COVER: 翻唱/翻奏
        + REMIX: 改编/remix
        """

        ORIGINAL = 106
        COVER = 107
        REMIX = 108

    class Language(Enum):
        """
        语种

        + CHINESE: 中文
        + JAPANESE: 日语
        + ENGLISH: 英语
        + KOREAN: 韩语
        + CANTONESE: 粤语
        + OTHER_LANGUAGES: 其他语种
        """

        CHINESE = 109
        JAPANESE = 110
        ENGLISH = 111
        KOREAN = 112
        CANTONESE = 113
        OTHER_LANGUAGES = 114

    class Theme(Enum):
        """
        主题来源

        + GAME: 游戏
        + ANIMATION: 动画
        + FILM_AND_TELEVISION: 影视
        + NETWORK_SONG: 网络歌曲
        + DERIVATIVE_WORK: 同人
        + IDOL: 偶像
        """

        ANIMATION = 115
        GAME = 116
        FILM_AND_TELEVISION = 117
        NETWORK_SONG = 118
        DERIVATIVE_WORK = 119
        IDOL = 120

    class Style(Enum):
        """
        风格

        + POP: 流行
        + ANCIENT_STYLE: 古风
        + ROCK: 摇滚
        + FOLK_SONG: 民谣
        + ELECTRONIC: 电子
        + DANCE_MUSIC: 舞曲
        + RAP: 说唱
        + LIGHT_MUSIC: 轻音乐
        + A_CAPPELLA: 阿卡贝拉
        + JAZZ: 爵士
        + COUNTRY_MUSIC: 乡村
        + R_AND_B: R&B/Soul
        + CLASSICAL: 古典
        + CLASSICAL: 古典
        + ETHNIC: 民族
        + BRITISH: 英伦
        + METAL: 金属
        + PUNK: 朋克
        + BLUES: 蓝调
        + REGGAE: 雷鬼
        + WORLD_MUSIC: 世界音乐
        + LATIN: 拉丁
        + ALTERNATIVE: 另类/独立
        + NEW_AGE: New Age
        + POST_ROCK: 后摇
        + BOSSA_NOVA: Bossa Nova
        """

        POP = 121
        ANCIENT_STYLE = 122
        ROCK = 123
        FOLK_SONG = 124
        ELECTRONIC = 125
        DANCE_MUSIC = 126
        RAP = 127
        LIGHT_MUSIC = 128
        A_CAPPELLA = 129
        JAZZ = 130
        COUNTRY_MUSIC = 131
        R_AND_B = 132
        CLASSICAL = 133
        ETHNIC = 134
        BRITISH = 135
        METAL = 136
        PUNK = 137
        BLUES = 138
        REGGAE = 139
        WORLD_MUSIC = 140
        LATIN = 141
        ALTERNATIVE = 142
        NEW_AGE = 143
        POST_ROCK = 144
        BOSSA_NOVA = 145

    class ContentType(Enum):
        """
        内容类型

        + MUSIC: 音乐
        + AUDIO_PROGRAM: 有声节目
        """

        MUSIC = 146
        AUDIO_PROGRAM = 147

    class AudioType(Enum):
        """
        声音类型

        + RADIO_DRAMA: 广播剧
        + AUDIO_STORY: 有声故事
        + ASMR: ASMR
        + OTHER: 其他
        """

        RADIO_DRAMA = 148
        AUDIO_STORY = 149
        ASMR = 150
        OTHER = 151


class AudioUploaderEvents(Enum):
    """
    上传事件枚举

    Events:
    + PREUPLOAD  获取上传信息
    + PREUPLOAD_FAILED  获取上传信息失败
    + PRE_CHUNK  上传分块前
    + AFTER_CHUNK  上传分块后
    + CHUNK_FAILED  区块上传失败
    + PRE_COVER  上传封面前
    + AFTER_COVER  上传封面后
    + COVER_FAILED  上传封面失败
    + PRE_SUBMIT  提交音频前
    + SUBMIT_FAILED  提交音频失败
    + AFTER_SUBMIT  提交音频后
    + COMPLETED  完成上传
    + ABORTED  用户中止
    + FAILED  上传失败
    """

    PREUPLOAD = "PREUPLOAD"
    PREUPLOAD_FAILED = "PREUPLOAD_FAILED"

    PRE_CHUNK = "PRE_CHUNK"
    AFTER_CHUNK = "AFTER_CHUNK"
    CHUNK_FAILED = "CHUNK_FAILED"

    PRE_COVER = "PRE_COVER"
    AFTER_COVER = "AFTER_COVER"
    COVER_FAILED = "COVER_FAILED"

    PRE_SUBMIT = "PRE_SUBMIT"
    SUBMIT_FAILED = "SUBMIT_FAILED"
    AFTER_SUBMIT = "AFTER_SUBMIT"

    COMPLETED = "COMPLETE"
    ABORTED = "ABORTED"
    FAILED = "FAILED"


@dataclass
class AuthorInfo:
    name: str
    uid: int = 0


@dataclass
class SongMeta:
    """
    content_type (SongCategories.ContentType): 内容类型

    song_type (Union[SongCategories.SongType, SongCategories.AudioType]): 歌曲类型

    creation_type (SongCategories.CreationType): 创作类型

    language (Optional[SongCategories.Language]): 语言类型

    theme (Optional[SongCategories.Theme]): 主题来源

    style (Optional[SongCategories.Style]): 风格类型

    singer (List[AuthorInfo]): 歌手

    player (Optional[List[AuthorInfo]]): 演奏

    sound_source (Optional[List[AuthorInfo]]): 音源

    tuning (Optional[List[AuthorInfo]]): 调音

    lyricist (Optional[List[AuthorInfo]]): 作词

    arranger (List[AuthorInfo]): 编曲

    composer (Optional[List[AuthorInfo]]): 作曲

    mixer (Optional[str]): 混音

    cover_maker (Optional[List[AuthorInfo]]): 封面制作者

    instrument (Optional[List[str]]): 乐器

    origin_url (Optional[str]): 原曲链接

    origin_title (Optional[str]): 原曲标题

    title (str): 标题

    cover (Optional[Picture]): 封面

    description (Optional[str]): 描述

    tags (Union[List[str], str]): 标签

    aid (Optional[int]): 视频 aid

    cid (Optional[int]): 视频 cid

    tid (Optional[int]): 视频 tid

    compilation_id (Optional[int]): 合辑 ID

    lrc (Optional[str]): 歌词
    """

    title: str
    desc: str
    tags: Union[List[str], str]
    content_type: SongCategories.ContentType
    song_type: Union[SongCategories.SongType, SongCategories.AudioType]
    creation_type: SongCategories.CreationType
    language: Optional[SongCategories.Language] = None
    theme: Optional[SongCategories.Theme] = None
    style: Optional[SongCategories.Style] = None
    singer: Optional[List[AuthorInfo]] = field(default_factory=list)
    player: Optional[List[AuthorInfo]] = field(default_factory=list)
    sound_source: Optional[List[AuthorInfo]] = field(default_factory=list)
    tuning: Optional[List[AuthorInfo]] = field(default_factory=list)
    lyricist: Optional[List[AuthorInfo]] = field(default_factory=list)
    arranger: Optional[List[AuthorInfo]] = field(default_factory=list)
    composer: Optional[List[AuthorInfo]] = field(default_factory=list)
    mixer: Optional[List[AuthorInfo]] = field(default_factory=list)
    cover_maker: Optional[List[AuthorInfo]] = field(default_factory=list)
    instrument: Optional[List[str]] = field(default_factory=list)
    origin_url: Optional[str] = None
    origin_title: Optional[str] = None
    cover: Optional[Picture] = None
    aid: Optional[int] = None
    cid: Optional[int] = None
    tid: Optional[int] = None
    lrc: Optional[str] = None
    compilation_id: Optional[int] = None
    is_bgm: bool = True


class AudioUploader(AsyncEvent):
    """
    音频上传
    """

    __song_id: int
    __upos_file: UposFile
    __task: asyncio.Task

    def _check_meta(self):
        assert self.meta.content_type is not None
        assert self.meta.song_type is not None
        assert self.meta.cover is not None and isinstance(self.meta.cover, str)
        if self.meta.content_type == SongCategories.ContentType.MUSIC:
            assert self.meta.creation_type is not None
            assert self.meta.song_type is not None
            assert self.meta.language is not None

            if self.meta.song_type == SongCategories.SongType.HUMAN_SINGING:
                assert self.meta.singer is not None
                assert self.meta.language is not None

            elif self.meta.song_type in [
                SongCategories.SongType.VOCALOID,
                SongCategories.SongType.HUMAN_GHOST,
            ]:
                assert self.meta.sound_source is not None
                assert self.meta.language is not None
                assert self.meta.tuning is not None

            elif self.meta.song_type == SongCategories.SongType.PURE_MUSIC:
                assert self.meta.player is not None

        if isinstance(self.meta.tags, str):
            self.meta.tags = self.meta.tags.split(",")
        assert len(self.meta.tags != 0)

        assert self.meta.title is not None
        assert self.meta.cover is not None
        assert self.meta.desc is not None

    def __init__(self, path: str, meta: SongMeta, credential: Credential):
        """
        初始化

        Args:
            path (str): 文件路径

            meta (AudioMeta): 元数据

            credential (Credential): 账号信息
        """
        super().__init__()
        self.path = path
        self.meta = meta
        self.credential = credential
        self.__upos_file = UposFile(path)

    async def _preupload(self) -> dict:
        """
        分 P 上传初始化

        Returns:
            dict: 初始化信息
        """
        self.dispatch(AudioUploaderEvents.PREUPLOAD.value, {"song": self.meta})
        api = _API["preupload"]

        # 首先获取音频文件预检信息
        session = get_session()

        resp = await session.get(
            api["url"],
            params={
                "profile": "uga/bup",
                "name": os.path.basename(self.path),
                "size": self.__upos_file.size,
                "r": "upos",
                "ssl": "0",
                "version": "2.6.0",
                "build": 2060400,
            },
            cookies=self.credential.get_cookies(),
            headers=HEADERS.copy(),
        )
        if resp.status_code >= 400:
            self.dispatch(
                AudioUploaderEvents.PREUPLOAD_FAILED.value, {"song": self.meta}
            )
            raise NetworkException(resp.status_code, resp.reason_phrase)

        preupload = resp.json()

        if preupload["OK"] != 1:
            self.dispatch(
                AudioUploaderEvents.PREUPLOAD_FAILED.value, {"song": self.meta}
            )
            raise ApiException(json.dumps(preupload))

        url = f'https:{preupload["endpoint"]}/{preupload["upos_uri"].removeprefix("upos://")}'
        headers = HEADERS.copy()
        headers["x-upos-auth"] = preupload["auth"]

        # 获取 upload_id
        resp = await session.post(
            url,
            headers=headers,
            params={
                "uploads": "",
                "output": "json",
                "profile": "uga/bup",
                "filesize": self.__upos_file.size,
                "partsize": preupload["chunk_size"],
                "biz_id": preupload["biz_id"],
            },
        )
        if resp.status_code >= 400:
            self.dispatch(
                AudioUploaderEvents.PREUPLOAD_FAILED.value, {"song": self.meta}
            )
            raise ApiException("获取 upload_id 错误")

        data = json.loads(resp.text)

        if data["OK"] != 1:
            self.dispatch(
                AudioUploaderEvents.PREUPLOAD_FAILED.value, {"song": self.meta}
            )
            raise ApiException("获取 upload_id 错误：" + json.dumps(data))

        preupload["upload_id"] = data["upload_id"]
        self.__song_id = preupload["biz_id"]
        return preupload

    async def _upload_cover(self, cover: str) -> str:
        return await upload_cover(cover, self.credential)

    async def _main(self):
        preupload = await self._preupload()
        await UposFileUploader(file=self.__upos_file, preupload=preupload).upload()
        if self.meta.lrc:
            lrc_url = await upload_lrc(
                song_id=self.__song_id, lrc=self.meta.lrc, credential=self.credential
            )
        else:
            lrc_url = ""
        self.dispatch(AudioUploaderEvents.PRE_COVER)
        if self.meta.cover:
            try:
                cover_url = await self._upload_cover(self.meta.cover)
            except Exception as e:
                self.dispatch(AudioUploaderEvents.COVER_FAILED, {"err": e})
                raise e
            self.dispatch(AudioUploaderEvents.AFTER_COVER.value, cover_url)
        self.dispatch(AudioUploaderEvents.PRE_SUBMIT.value)
        try:
            result = await self._submit(lrc_url=lrc_url, cover_url=cover_url)
        except Exception as e:
            self.dispatch(AudioUploaderEvents.SUBMIT_FAILED.value, {"err": e})
            raise e
        self.dispatch(AudioUploaderEvents.AFTER_SUBMIT.value, result)
        return result

    async def _submit(self, cover_url: str, lrc_url: str = "") -> int:
        uploader = await user.get_self_info(self.credential)
        data = {
            "lyric_url": lrc_url,
            "cover_url": cover_url,
            "song_id": self.__song_id,
            "mid": uploader["mid"],
            "cr_type": self.meta.content_type.value,
            "creation_type_id": self.meta.creation_type.value,
            "music_type_id": self.meta.song_type.value,
            "style_type_id": self.meta.style.value if self.meta.style else 0,
            "theme_type_id": self.meta.theme.value if self.meta.theme else 0,
            "language_type_id": self.meta.language.value if self.meta.language else 0,
            "origin_title": self.meta.origin_title if self.meta.origin_title else "",
            "origin_url": self.meta.origin_url if self.meta.origin_url else "",
            "avid": self.meta.aid if self.meta.aid else "",
            "tid": self.meta.tid if self.meta.tid else "",
            "cid": self.meta.cid if self.meta.cid else "",
            "compilation_id": self.meta.compilation_id
            if self.meta.compilation_id
            else "",
            "title": self.meta.title,
            "intro": self.meta.desc,
            "member_with_type": [
                {
                    "m_type": 1,  # 歌手
                    "members": [
                        {"name": singer.name, "mid": singer.uid}
                        for singer in self.meta.singer
                    ],
                },
                {
                    "m_type": 2,  # 作词
                    "members": [
                        {"name": lyricist.name, "mid": lyricist.uid}
                        for lyricist in self.meta.lyricist
                    ],
                },
                {
                    "m_type": 3,
                    "members": [
                        {"name": composer.name, "mid": composer.uid}
                        for composer in self.meta.composer
                    ],
                },  # 作曲
                {
                    "m_type": 4,
                    "members": [
                        {"name": arranger.name, "mid": arranger.uid}
                        for arranger in self.meta.arranger
                    ],
                },  # 编曲
                {
                    "m_type": 5,
                    "members": [
                        {"name": mixer.name, "mid": mixer.uid}
                        for mixer in self.meta.mixer
                    ],
                },  # 混音只能填一个人，你问我为什么我不知道
                {
                    "m_type": 6,
                    "members": [
                        {"name": cover_maker.name, "mid": cover_maker.uid}
                        for cover_maker in self.meta.cover_maker
                    ],
                },  # 本家作者
                {
                    "m_type": 7,
                    "members": [
                        {"name": cover_maker.name, "mid": cover_maker.uid}
                        for cover_maker in self.meta.cover_maker
                    ],
                },  # 封面
                {
                    "m_type": 8,
                    "members": [
                        {"name": sound_source.name, "mid": sound_source.uid}
                        for sound_source in self.meta.sound_source
                    ],
                },  # 音源
                {
                    "m_type": 9,
                    "members": [
                        {"name": tuning.name, "mid": tuning.uid}
                        for tuning in self.meta.tuning
                    ],
                },  # 调音
                {
                    "m_type": 10,
                    "members": [
                        {"name": player.name, "mid": player.uid}
                        for player in self.meta.player
                    ],
                },  # 演奏
                {
                    "m_type": 11,
                    "members": [
                        {"name": instrument} for instrument in self.meta.instrument
                    ],
                },  # 乐器
                {
                    "m_type": 127,
                    "members": [{"name": uploader["name"], "mid": uploader["mid"]}],
                },  # 上传者
            ],
            "song_tags": [{"tagName": tag_name} for tag_name in self.meta.tags],
            "create_time": "%.3f" % time.time(),
            "activity_id": 0,
            "is_bgm": 1 if self.meta.is_bgm else 0,
            "source": 0,
            "album_id": 0,
        }
        api = _API["submit_single_song"]
        return (
            await Api(**api, credential=self.credential, json_body=True, no_csrf=True)
            .update_data(**data)
            .result
        )

    async def start(self) -> dict:
        """
        开始上传
        """
        task = asyncio.create_task(self._main())
        self.__task = task

        try:
            result = await task
            self.__task = None
            return result
        except asyncio.CancelledError:
            # 忽略 task 取消异常
            pass
        except Exception as e:
            self.dispatch(AudioUploaderEvents.FAILED.value, {"err": e})
            raise e

    async def abort(self):
        """
        中断更改
        """
        if self.__task:
            self.__task.cancel("用户手动取消")

        self.dispatch(AudioUploaderEvents.ABORTED.value, None)


async def upload_lrc(lrc: str, song_id: int, credential: Credential) -> str:
    """
    上传 LRC 歌词

    Args:
        lrc (str): 歌词

        credential (Credential): 凭据
    """
    api = _API["lrc"]
    data = {"song_id": song_id, "lrc": lrc}
    return await Api(**api, credential=credential).update_data(**data).result


async def get_upinfo(param: Union[int, str], credential: Credential) -> List[dict]:
    """
    获取 UP 信息

    Args:
        param (Union[int, str]): UP 主 ID 或者用户名

        credential (Credential): 凭据
    """
    api = _API["upinfo"]
    data = {"param": param}
    return await Api(**api, credential=credential).update_data(**data).result


async def upload_cover(cover: Picture, credential: Credential) -> str:
    api = _API["image"]
    # 小于 3MB
    assert os.path.getsize(cover) < 1024 * 1024 * 3, "3MB size limit"
    # 宽高比 1:1
    assert cover.width == cover.height, "width == height, 600 * 600 recommanded"
    files = {"file": cover.content}
    return await Api(**api, credential=credential).update_files(**files).result
