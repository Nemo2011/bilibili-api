# Module audio.py

```python
from bilibili_api import audio
```

音频相关

## class Audio

音频类。

### Functions

#### def \_\_init\_\_()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| auid       | int                  | 音频 AU 号             |
| credential | Credential, optional | 凭据. Defaults to None |

#### _async_ def get_auid()

获取 auid

**Returns:** auid

#### _async_ def get_info()

获取音频信息

**Returns:** API 调用返回结果

#### _async_ def get_tags()

获取音频 tags

**Returns:** API 调用返回结果

#### _async_ def get_download_url()

获取音频下载链接

**Returns:** API 调用返回结果

#### _async_ def add_coins()

| name | type          | description              |
| ---- | ------------- | ------------------------ |
| num  | int, optional | 投币数量。Defaults to 2. |

投币

**Returns:** API 调用返回结果

---

## class AudioList

歌单

### Functions

#### def \_\_init\_\_()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| amid       | int                  | 歌单 ID                |
| credential | Credential, optional | 凭据. Defaults to None |

#### _async_ def get_info()

获取歌单信息

**Returns:** API 调用返回结果

#### _async_ def get_tags()

获取歌单 tags

**Returns:** API 调用返回结果

#### _async_ def get_song_list()

| name | type          | description         |
| ---- | ------------- | ------------------- |
| pn   | int, optional | 页码。Defaults to 1 |

获取歌单歌曲列表

**Returns:** API 调用返回结果

---

## _async_ def get_user_stat()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| uid        | int                  | 用户 UID               |
| credential | Credential, optional | 凭据. Defaults to None |

获取用户数据（收听数，粉丝数等）

**Returns:** API 调用返回结果