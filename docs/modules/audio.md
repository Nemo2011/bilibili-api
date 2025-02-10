# Module audio.py


bilibili_api.audio

音频相关


``` python
from bilibili_api import audio
```

- [class Audio()](#class-Audio)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def add\_coins()](#async-def-add\_coins)
  - [def get\_auid()](#def-get\_auid)
  - [async def get\_download\_url()](#async-def-get\_download\_url)
  - [async def get\_info()](#async-def-get\_info)
  - [async def get\_tags()](#async-def-get\_tags)
- [class AudioList()](#class-AudioList)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def get\_amid()](#def-get\_amid)
  - [async def get\_info()](#async-def-get\_info)
  - [async def get\_song\_list()](#async-def-get\_song\_list)
  - [async def get\_tags()](#async-def-get\_tags)
- [async def get\_hot\_song\_list()](#async-def-get\_hot\_song\_list)
- [async def get\_user\_stat()](#async-def-get\_user\_stat)

---

## class Audio()

音频


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `auid` | `int` | 音频 AU 号 |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None |


### async def add_coins()

投币


| name | type | description |
| - | - | - |
| `num` | `int, optional` | 投币数量。Defaults to 2. |

**Returns:** `dict`:  调用 API 返回的结果




### def get_auid()

获取 auid



**Returns:** `int`:  auid




### async def get_download_url()

获取音频下载链接



**Returns:** `dict`:  调用 API 返回的结果




### async def get_info()

获取音频信息



**Returns:** `dict`:  调用 API 返回的结果




### async def get_tags()

获取音频 tags



**Returns:** `dict`:  调用 API 返回的结果




---

## class AudioList()

歌单


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `amid` | `int` | 歌单 ID |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |


### def get_amid()

获取 amid



**Returns:** `int`:  amid




### async def get_info()

获取歌单信息



**Returns:** `dict`:  调用 API 返回的结果




### async def get_song_list()

获取歌单歌曲列表


| name | type | description |
| - | - | - |
| `pn` | `int, optional` | 页码. Defaults to 1 |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_tags()

获取歌单 tags



**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_hot_song_list()

获取热门歌单


| name | type | description |
| - | - | - |
| `pn` | `int, optional` | 页数. Defaults to 1 |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_user_stat()

获取用户数据（收听数，粉丝数等）


| name | type | description |
| - | - | - |
| `uid` | `int` | 用户 UID |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None |

**Returns:** `dict`:  调用 API 返回的结果




