# Module audio.py


bilibili_api.audio

音频相关


``` python
from bilibili_api import audio
```

## class Audio

**Extend: builtins.object**

音频


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |


### async def add_coins()

投币


| name | type | description |
| - | - | - |
| num | Union[int, None] | 投币数量。Defaults to 2. |

**Returns:** dict: 调用 API 返回的结果




### def get_auid()

获取 auid



**Returns:** int: auid




### async def get_download_url()

获取音频下载链接



**Returns:** dict: 调用 API 返回的结果




### async def get_info()

获取音频信息



**Returns:** dict: 调用 API 返回的结果




### async def get_tags()

获取音频 tags



**Returns:** dict: 调用 API 返回的结果




## class AudioList

**Extend: builtins.object**

歌单


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |


### def get_amid()

获取 amid



**Returns:** int: amid




### async def get_info()

获取歌单信息



**Returns:** dict: 调用 API 返回的结果




### async def get_song_list()

获取歌单歌曲列表


| name | type | description |
| - | - | - |
| pn | Union[int, None] | 页码. Defaults to 1 |

**Returns:** dict: 调用 API 返回的结果




### async def get_tags()

获取歌单 tags



**Returns:** dict: 调用 API 返回的结果




## async def get_hot_song_list()

获取热门歌单


| name | type | description |
| - | - | - |
| pn | Union[int, None] | 页数. Defaults to 1 |
| credential | Union[Credential, None] | 凭据. Defaults to None |

**Returns:** dict: 调用 API 返回的结果




## async def get_user_stat()

获取用户数据（收听数，粉丝数等）


| name | type | description |
| - | - | - |
| uid | int | 用户 UID |
| credential | Union[Credential, None] | 凭据. Defaults to None |

**Returns:** dict: 调用 API 返回的结果




