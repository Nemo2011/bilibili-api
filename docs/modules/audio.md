# Module audio.py

```python
from bilibili_api import audio
```

音频相关

---

## async def get_homepage_recommend()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

获取音频首页推荐

**Returns:** dict: 调用 API 返回的结果

---


## class Audio

音频类。

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

### Functions

#### def \_\_init\_\_()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| auid       | int                  | 音频 AU 号             |
| credential | Credential \| None, optional | 凭据. Defaults to None |

#### def get_auid()

获取 auid

**Returns:** auid

#### async def get_info()

获取音频信息

**Returns:** 调用 API 返回的结果

#### async def get_tags()

获取音频 tags

**Returns:** 调用 API 返回的结果

#### async def get_download_url()

获取音频下载链接

**Returns:** 调用 API 返回的结果

#### async def add_coins()

| name | type          | description              |
| ---- | ------------- | ------------------------ |
| num  | int, optional | 投币数量。Defaults to 2. |

投币

**Returns:** 调用 API 返回的结果

---

## class AudioList

歌单

### Functions

#### def \_\_init\_\_()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| amid       | int                  | 歌单 ID                |
| credential | Credential \| None, optional | 凭据. Defaults to None |

#### def get_amid()

获取歌单 amid

**Returns:** amid

#### async def get_info()

获取歌单信息

**Returns:** 调用 API 返回的结果

#### async def get_tags()

获取歌单 tags

**Returns:** 调用 API 返回的结果

#### async def get_song_list()

| name | type          | description         |
| ---- | ------------- | ------------------- |
| pn   | int, optional | 页码。Defaults to 1 |

获取歌单歌曲列表

**Returns:** 调用 API 返回的结果

---

## async def get_user_stat()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| uid        | int                  | 用户 UID               |
| credential | Credential \| None, optional | 凭据. Defaults to None |

获取用户数据（收听数，粉丝数等）

**Returns:** 调用 API 返回的结果

---

## class TagsAudio

音频搜索可以用的标签，有语言和类型两种标签，每种标签选一个

- Lang: 语言标签枚举类
- Genre: 类型标签枚举类

### SubClasses

#### class Lang

**Extends: enum.Enum**

音频搜索语言标签枚举

- ALL: 全部
- CHINESE: 华语
- EUROPE_AMERICA: 欧美
- JAPAN: 日语
- KOREA: 韩语
- OTHER: 其他

#### Class Genre

**Extends: enum.Enum**

音频搜索类型标签枚举

- ALL: 全部
- POPULAR: 流行
- ROCK: 摇滚
- ELECTRONIC: 电子音乐
- COUNTRYSIDE: 乡村
- FOLK: 民谣
- LIVE: 轻音乐
- CLASSICAL: 古典
- NEW_CENTURY: 新世纪
- REGGAE: 雷鬼
- BLUES: 布鲁斯
- RHYTHM_BLUES: 节奏与布鲁斯
- ORIGINAL: 原声
- WORLD: 世界音乐
- CHILDREN: 儿童音乐
- LATIN: 拉丁
- PUNK: 朋克
- MEDAL: 金属
- JAZZ: 爵士乐
- HIP_HOP: 嘻哈
- SINGER_SONGWRITER: 唱作人
- AMUSEMENT: 娱乐/舞台
- OTHER: 其他
        
---

## async def get_homepage_music_video_list()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| keyword   | str |             关键词. Defaults to None. | 
| lang      | TagsAudio.Lang|   音频语言. Defaults to TagsAudio.Lang.ALL | 
| genre     | TagsAudio.Genre|  音频类型. Defaults to TagsAudio.Genre.ALL | 
| order     | OrderAudio|       音频排序方式. Defaults to OrderAudio.NEW | 
| page_num  | int|              页码. Defaults to 1. | 
| page_size | int |             每页的数据大小. Defaults to 10. | 

**Returns:** dict: 调用 API 返回的结果
