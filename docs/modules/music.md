# Module music.py

```python
from bilibili_api import music
```


音乐相关 API

注意: 目前 B 站的音频并不和 B 站的音乐相关信息互通。这里的 Music 类的数据来源于视频下面的 bgm 标签和全站音乐榜中的每一个 bgm/音乐。get_homepage_recommend 和 get_music_index_info 来源于 https://www.bilibili.com/v/musicplus/

## async def get_homepage_recommend()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

获取音频首页推荐

**Returns:** dict: 调用 API 返回的结果

---


## class MusicIndexTags

音乐索引信息查找可以用的标签，有语言和类型两种标签，每种标签选一个

- Lang: 语言标签枚举类
- Genre: 类型标签枚举类

### SubClasses

#### class Lang

**Extends: enum.Enum**

- ALL: 全部
- CHINESE: 华语
- EUROPE_AMERICA: 欧美
- JAPAN: 日语
- KOREA: 韩语
- OTHER: 其他

#### Class Genre

**Extends: enum.Enum**

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

## class MusicOrder()

**Extends: enum.Enum**

音乐排序类型

+ NEW: 最新
+ HOT: 最热

---

## async def get_music_index_info()

| name       | type                 | description            |
| ---------- |----------------------| ---------------------- |
| keyword   | str                  |             关键词. Defaults to None. | 
| lang      | MusicIndexTags.Lang  |   语言. Defaults to MusicIndexTags.Lang.ALL | 
| genre     | MusicIndexTags.Genre |  类型. Defaults to MusicIndexTags.Genre.ALL | 
| order     | MusicOrder           |       排序方式. Defaults to OrderAudio.NEW | 
| page_num  | int                  |              页码. Defaults to 1. | 
| page_size | int                  |             每页的数据大小. Defaults to 10. | 

**Returns:** dict: 调用 API 返回的结果

---

## class Music


音乐类。

此处的“音乐”定义：部分视频的标签中有里面出现过的音乐的标签, 可以点击音乐标签查看音乐信息。此类将提供查询音乐信息的接口。

其中音乐的 ID 为 `video.get_tags` 返回值数据中的 `music_id` 键值

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| music_id | str | 音乐 id，例如 MA436038343856245020 |

#### async def get_info()

获取音乐信息

**Returns:** dict: 调用 API 返回的结果

#### async def get_music_videos()

获取音乐的音乐视频

**Returns:** dict: 调用 API 返回的结果
