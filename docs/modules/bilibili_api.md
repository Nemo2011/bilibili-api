# Module bilibili_api.py


bilibili_api

哔哩哔哩的各种 API 调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。

 (默认已导入所有子模块，例如 `bilibili_api.video`, `bilibili_api.user`)


``` python
from bilibili_api import bilibili_api
```

- [class Api()](#class-Api)
  - [async def request()](#async-def-request)
  - [def update\_data()](#def-update\_data)
  - [def update\_files()](#def-update\_files)
  - [def update\_headers()](#def-update\_headers)
  - [def update\_params()](#def-update\_params)
- [class ApiException()](#class-ApiException)
- [class ArgsException()](#class-ArgsException)
- [class BiliAPIClient()](#class-BiliAPIClient)
- [class BiliAPIFile()](#class-BiliAPIFile)
- [class BiliAPIResponse()](#class-BiliAPIResponse)
  - [def json()](#def-json)
  - [def utf8\_text()](#def-utf8\_text)
- [class BiliWsMsgType()](#class-BiliWsMsgType)
- [class CookiesRefreshException()](#class-CookiesRefreshException)
- [class Credential()](#class-Credential)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def check\_refresh()](#async-def-check\_refresh)
  - [async def check\_valid()](#async-def-check\_valid)
  - [def from\_cookies()](#def-from\_cookies)
  - [def get\_cookies()](#def-get\_cookies)
  - [def has\_ac\_time\_value()](#def-has\_ac\_time\_value)
  - [def has\_bili\_jct()](#def-has\_bili\_jct)
  - [def has\_buvid3()](#def-has\_buvid3)
  - [def has\_dedeuserid()](#def-has\_dedeuserid)
  - [def has\_sessdata()](#def-has\_sessdata)
  - [def raise\_for\_no\_ac\_time\_value()](#def-raise\_for\_no\_ac\_time\_value)
  - [def raise\_for\_no\_bili\_jct()](#def-raise\_for\_no\_bili\_jct)
  - [def raise\_for\_no\_buvid3()](#def-raise\_for\_no\_buvid3)
  - [def raise\_for\_no\_dedeuserid()](#def-raise\_for\_no\_dedeuserid)
  - [def raise\_for\_no\_sessdata()](#def-raise\_for\_no\_sessdata)
  - [async def refresh()](#async-def-refresh)
- [class CredentialNoAcTimeValueException()](#class-CredentialNoAcTimeValueException)
- [class CredentialNoBiliJctException()](#class-CredentialNoBiliJctException)
- [class CredentialNoBuvid3Exception()](#class-CredentialNoBuvid3Exception)
- [class CredentialNoDedeUserIDException()](#class-CredentialNoDedeUserIDException)
- [class CredentialNoSessdataException()](#class-CredentialNoSessdataException)
- [class CurlCFFIClient()](#class-CurlCFFIClient)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def close()](#async-def-close)
  - [def get\_wrapped\_session()](#def-get\_wrapped\_session)
  - [async def request()](#async-def-request)
  - [def set\_proxy()](#def-set\_proxy)
  - [def set\_timeout()](#def-set\_timeout)
  - [def set\_trust\_env()](#def-set\_trust\_env)
  - [def set\_verify\_ssl()](#def-set\_verify\_ssl)
  - [async def ws\_close()](#async-def-ws\_close)
  - [async def ws\_create()](#async-def-ws\_create)
  - [async def ws\_recv()](#async-def-ws\_recv)
  - [async def ws\_send()](#async-def-ws\_send)
- [class Danmaku()](#class-Danmaku)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def crack\_uid()](#def-crack\_uid)
  - [def to\_xml()](#def-to\_xml)
- [class DanmakuClosedException()](#class-DanmakuClosedException)
- [class DmFontSize()](#class-DmFontSize)
- [class DmMode()](#class-DmMode)
- [class DynamicExceedImagesException()](#class-DynamicExceedImagesException)
- [class ExClimbWuzhiException()](#class-ExClimbWuzhiException)
- [class Geetest()](#class-Geetest)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def close\_geetest\_server()](#def-close\_geetest\_server)
  - [def complete\_test()](#def-complete\_test)
  - [async def generate\_test()](#async-def-generate\_test)
  - [def get\_geetest\_server\_url()](#def-get\_geetest\_server\_url)
  - [def get\_info()](#def-get\_info)
  - [def get\_result()](#def-get\_result)
  - [def has\_done()](#def-has\_done)
  - [def start\_geetest\_server()](#def-start\_geetest\_server)
  - [def test\_generated()](#def-test\_generated)
- [class GeetestMeta()](#class-GeetestMeta)
- [class GeetestServerNotFoundException()](#class-GeetestServerNotFoundException)
- [class GeetestUndoneException()](#class-GeetestUndoneException)
- [class LiveException()](#class-LiveException)
- [class LoginError()](#class-LoginError)
- [class NetworkException()](#class-NetworkException)
- [class Picture()](#class-Picture)
  - [def convert\_format()](#def-convert\_format)
  - [def from\_content()](#def-from\_content)
  - [def from\_file()](#def-from\_file)
  - [async def load\_url()](#async-def-load\_url)
  - [def to\_file()](#def-to\_file)
  - [async def upload()](#async-def-upload)
  - [async def upload\_by\_note()](#async-def-upload\_by\_note)
- [class ResourceType()](#class-ResourceType)
- [class ResponseCodeException()](#class-ResponseCodeException)
- [class ResponseException()](#class-ResponseException)
- [class SpecialDanmaku()](#class-SpecialDanmaku)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
- [class StatementException()](#class-StatementException)
- [class VideoUploadException()](#class-VideoUploadException)
- [class WbiRetryTimesExceedException()](#class-WbiRetryTimesExceedException)
- [def aid2bvid()](#def-aid2bvid)
- [def bvid2aid()](#def-bvid2aid)
- [async def get\_bili\_ticket()](#async-def-get\_bili\_ticket)
- [async def get\_buvid()](#async-def-get\_buvid)
- [def get\_client()](#def-get\_client)
- [async def get\_real\_url()](#async-def-get\_real\_url)
- [def get\_selected\_client()](#def-get\_selected\_client)
- [def get\_session()](#def-get\_session)
- [async def get\_wbi\_mixin\_key()](#async-def-get\_wbi\_mixin\_key)
- [async def parse\_link()](#async-def-parse\_link)
- [def refresh\_bili\_ticket()](#def-refresh\_bili\_ticket)
- [def refresh\_buvid()](#def-refresh\_buvid)
- [def refresh\_wbi\_mixin\_key()](#def-refresh\_wbi\_mixin\_key)
- [def register\_client()](#def-register\_client)
- [def select\_client()](#def-select\_client)
- [def set\_session()](#def-set\_session)
- [def sync()](#def-sync)
- [def unregister\_client()](#def-unregister\_client)

---

**@dataclasses.dataclass** 

## class Api()

用于请求的 Api 类


| name | type | description |
| - | - | - |
| url | str | 请求地址 |
| method | str | 请求方法 |
| comment | Union[str, None] | 注释. Defaults to "". |
| wbi | Union[bool, None] | 是否使用 wbi 鉴权. Defaults to False. |
| wbi2 | Union[bool, None] | 是否使用参数进一步的 wbi 鉴权. Defaults to False. |
| bili_ticket | Union[bool, None] | 是否使用 bili_ticket. Defaults to False. |
| verify | Union[bool, None] | 是否验证凭据. Defaults to False. |
| no_csrf | Union[bool, None] | 是否不使用 csrf. Defaults to False. |
| json_body | Union[bool, None] | 是否使用 json 作为载荷. Defaults to False. |
| ignore_code | Union[bool, None] | 是否忽略返回值 code 的检验. Defaults to False. |
| data | Union[Dict, None] | 请求载荷. Defaults to {}. |
| params | Union[Dict, None] | 请求参数. Defaults to {}. |
| credential | Union[Credential, None] | 凭据. Defaults to Credential(). |


### async def request()

向接口发送请求。


| name | type | description |
| - | - | - |
| raw | bool | 是否不提取 data 或 result 字段。 Defaults to False. |
| byte | bool | 是否直接返回字节数据。 Defaults to False. |

**Returns:** 接口未返回数据时，返回 None，否则返回该接口提供的 data 或 result 字段的数据。




### def update_data()

更新 data



**Returns:** None



### def update_files()

更新 files



**Returns:** None



### def update_headers()

更新 headers



**Returns:** None



### def update_params()

更新 params



**Returns:** None



---

## class ApiException()

**Extend: builtins.Exception**

API 基类异常。




---

## class ArgsException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

参数错误。




---

## class BiliAPIClient()

**Extend: abc.ABC**

请求客户端抽象类。通过对第三方模块请求客户端的封装令模块可对其进行调用。




---

**@dataclasses.dataclass** 

## class BiliAPIFile()

上传文件类。


| name | type | description |
| - | - | - |
| path | str | 文件地址 |
| mime_type | str | 文件类型 |


---

**@dataclasses.dataclass** 

## class BiliAPIResponse()

响应对象类。


| name | type | description |
| - | - | - |
| code | int | 响应码 |
| headers | Dict | 响应头 |
| cookies | Dict | 当前状态的 cookies |
| raw | bytes | 响应数据 |
| url | str | 当前 url |


### def json()

解析 json



**Returns:** object: 解析后的 json




### def utf8_text()

转为 utf8 文字



**Returns:** str: utf8 文字




---

## class BiliWsMsgType()

**Extend: enum.Enum**

WebSocket 状态枚举

- CONTINUATION: 延续
- TEXT: 文字
- BINARY: 字节
- PING: ping
- PONG: pong
- CLOSE: 关闭

- CLOSING: 正在关闭
- CLOSED: 已关闭




---

## class CookiesRefreshException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

Cookies 刷新错误。




---

## class Credential()

凭据类，用于各种请求操作的验证。




### def \_\_init\_\_()

各字段获取方式查看：https://nemo2011.github.io/bilibili-api/#/get-credential.md


| name | type | description |
| - | - | - |
| sessdata | Union[str, None] | 浏览器 Cookies 中的 SESSDATA 字段值. Defaults to None. |
| bili_jct | Union[str, None] | 浏览器 Cookies 中的 bili_jct 字段值. Defaults to None. |
| buvid3 | Union[str, None] | 浏览器 Cookies 中的 BUVID3 字段值. Defaults to None. |
| dedeuserid | Union[str, None] | 浏览器 Cookies 中的 DedeUserID 字段值. Defaults to None. |
| ac_time_value | Union[str, None] | 浏览器 Cookies 中的 ac_time_value 字段值. Defaults to None. |


### async def check_refresh()

检查是否需要刷新 cookies



**Returns:** bool: cookies 是否需要刷新




### async def check_valid()

检查 cookies 是否有效



**Returns:** bool: cookies 是否有效




**@staticmethod** 

### def from_cookies()

从 cookies 新建 Credential


| name | type | description |
| - | - | - |
| cookies | Union[Dict, None] | Cookies. Defaults to {}. |

**Returns:** Credential: 凭据类




### def get_cookies()

获取请求 Cookies 字典



**Returns:** dict: 请求 Cookies 字典




### def has_ac_time_value()

是否提供 ac_time_value



**Returns:** bool.




### def has_bili_jct()

是否提供 bili_jct。



**Returns:** bool。




### def has_buvid3()

是否提供 buvid3



**Returns:** bool.




### def has_dedeuserid()

是否提供 dedeuserid。



**Returns:** bool。




### def has_sessdata()

是否提供 sessdata。



**Returns:** bool。




### def raise_for_no_ac_time_value()

没有提供 ac_time_value 时抛出异常。



**Returns:** None



### def raise_for_no_bili_jct()

没有提供 bili_jct 则抛出异常。



**Returns:** None



### def raise_for_no_buvid3()

没有提供 buvid3 时抛出异常。



**Returns:** None



### def raise_for_no_dedeuserid()

没有提供 DedeUserID 时抛出异常。



**Returns:** None



### def raise_for_no_sessdata()

没有提供 sessdata 则抛出异常。



**Returns:** None



### async def refresh()

刷新 cookies



**Returns:** None



---

## class CredentialNoAcTimeValueException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

Credential 类未提供 ac_time_value 时的异常。




---

## class CredentialNoBiliJctException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

Credential 类未提供 bili_jct 时的异常。




---

## class CredentialNoBuvid3Exception()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

Credential 类未提供 bili_jct 时的异常。




---

## class CredentialNoDedeUserIDException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

Credential 类未提供 DedeUserID 时的异常。




---

## class CredentialNoSessdataException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

Credential 类未提供 sessdata 时的异常。




---

## class CurlCFFIClient()

**Extend: bilibili_api.utils.network.BiliAPIClient**





### def \_\_init\_\_()





### async def close()




**Returns:** None



### def get_wrapped_session()




**Returns:** None



### async def request()




**Returns:** None



### def set_proxy()




**Returns:** None



### def set_timeout()




**Returns:** None



### def set_trust_env()




**Returns:** None



### def set_verify_ssl()




**Returns:** None



### async def ws_close()




**Returns:** None



### async def ws_create()




**Returns:** None



### async def ws_recv()




**Returns:** None



### async def ws_send()




**Returns:** None



---

## class Danmaku()

弹幕类。




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| text | str | 弹幕文本。 |
| dm_time | Union[float, None] | 弹幕在视频中的位置，单位为秒。Defaults to 0.0. |
| send_time | Union[float, None] | 弹幕发送的时间。Defaults to time.time(). |
| crc32_id | Union[str, None] | 弹幕发送者 UID 经 CRC32 算法取摘要后的值。Defaults to "". |
| color | Union[str, None] | 弹幕十六进制颜色。Defaults to "ffffff" (如果为大会员专属的颜色则为"special"). |
| weight | Union[int, None] | 弹幕在弹幕列表显示的权重。Defaults to -1. |
| id_ | Union[int, None] | 弹幕 ID。Defaults to -1. |
| id_str | Union[str, None] | 弹幕字符串 ID。Defaults to "". |
| action | Union[str, None] | 暂不清楚。Defaults to "". |
| mode | Union[Union[DmMode, None] | 弹幕模式。Defaults to Mode.FLY. |
| font_size | Union[Union[DmFontSize, None] | 弹幕字体大小。Defaults to FontSize.NORMAL. |
| is_sub | Union[bool, None] | 是否为字幕弹幕。Defaults to False. |
| pool | Union[int, None] | 池。Defaults to 0. |
| attr | Union[int, None] | 暂不清楚。 Defaults to -1. |
| uid | Union[int, None] | 弹幕发送者 UID。Defaults to -1. |
| 大会员专属颜色文字填充：http://i0.hdslb.com/bfs/dm/9dcd329e617035b45d2041ac889c49cb5edd3e44.png |  | //i0.hdslb.com/bfs/dm/9dcd329e617035b45d2041ac889c49cb5edd3e44.png |
| 大会员专属颜色背景填充：http://i0.hdslb.com/bfs/dm/ba8e32ae03a0a3f70f4e51975a965a9ddce39d50.png |  | //i0.hdslb.com/bfs/dm/ba8e32ae03a0a3f70f4e51975a965a9ddce39d50.png |


**@staticmethod** 

### def crack_uid()

(@staticmethod)

暴力破解 UID，可能存在误差，请慎重使用。

精确至 UID 小于 10000000 的破解。


| name | type | description |
| - | - | - |
| crc32_id | str | crc32 id |

**Returns:** int: 真实 UID。




### def to_xml()

将弹幕转换为 xml 格式弹幕



**Returns:** None



---

## class DanmakuClosedException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

视频弹幕被关闭错误。




---

## class DmFontSize()

**Extend: enum.Enum**

字体大小枚举。




---

## class DmMode()

**Extend: enum.Enum**

弹幕模式枚举。




---

## class DynamicExceedImagesException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

动态上传图片数量超过限制




---

## class ExClimbWuzhiException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

ExClimbWuzhi 失败异常




---

## class Geetest()

极验验证类




### def \_\_init\_\_()





### def close_geetest_server()

关闭本地极验验证码服务



**Returns:** None



### def complete_test()

作答测试


| name | type | description |
| - | - | - |
| validate | str | 作答结果的 validate |
| seccode | str | 作答结果的 seccode |

**Returns:** None



### async def generate_test()

创建验证码



**Returns:** None



### def get_geetest_server_url()

获取本地极验验证码服务链接



**Returns:** str: 链接




### def get_info()

获取验证码信息



**Returns:** GeetestMeta: 验证码信息




### def get_result()

获取结果



**Returns:** dict: 验证结果




### def has_done()

是否完成



**Returns:** bool: 是否完成




### def start_geetest_server()

开启本地极验验证码服务



**Returns:** None



### def test_generated()

当前是否有创建的测试



**Returns:** bool: 是否有创建的测试




---

**@dataclasses.dataclass** 

## class GeetestMeta()

极验验证码完成信息

NOTE: `gt`, `challenge`, `token` 为验证码基本字段。`seccode`, `validate` 为完成验证码后可得字段。




---

## class GeetestServerNotFoundException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

未找到验证码服务器




---

## class GeetestUndoneException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

验证码未完成




---

## class LiveException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**





---

## class LoginError()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

参数错误。




---

## class NetworkException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

网络错误。




---

**@dataclasses.dataclass** 

## class Picture()

(@dataclasses.dataclass)

图片类，包含图片链接、尺寸以及下载操作。

可以不实例化，用 `from_url`, `from_content` 或 `from_file` 加载图片。


| name | type | description |
| - | - | - |
| height | int | 高度 |
| imageType | str | 格式，例如 |
| size | Any | 尺寸 |
| url | str | 图片链接 |
| width | int | 宽度 |
| content | bytes | 图片内容 |


### def convert_format()

将图片转换为另一种格式。


| name | type | description |
| - | - | - |
| new_format | str | 新的格式。例：`png`, `ico`, `webp`. |

**Returns:** Picture: `self`




**@staticmethod** 

### def from_content()

加载字节数据


| name | type | description |
| - | - | - |
| content | str | 图片内容 |
| format | str | 图片后缀名，如 `webp`, `jpg`, `ico` |

**Returns:** Picture: 加载后的图片对象




**@staticmethod** 

### def from_file()

加载本地图片。


| name | type | description |
| - | - | - |
| path | str | 图片地址 |

**Returns:** Picture: 加载后的图片对象




**@staticmethod** 

### async def load_url()

加载网络图片。(async 方法)


| name | type | description |
| - | - | - |
| url | str | 图片链接 |

**Returns:** Picture: 加载后的图片对象




### def to_file()

下载图片至本地。


| name | type | description |
| - | - | - |
| path | str | 下载地址。 |

**Returns:** Picture: `self`




### async def upload()

上传图片至 B 站。


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类。 |

**Returns:** Picture: `self`




### async def upload_by_note()

通过笔记接口上传图片至 B 站。


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类。 |

**Returns:** Picture: `self`




---

## class ResourceType()

**Extend: enum.Enum**

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
+ NOTE: 笔记
+ FAILED: 错误




---

## class ResponseCodeException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

API 返回 code 错误。




---

## class ResponseException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

API 响应异常。




---

## class SpecialDanmaku()





### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| content | str | 弹幕内容 |
| id_ | int | 弹幕 id. Defaults to -1. |
| id_str | str | 弹幕 id (string 类型). Defaults to "". |
| mode | Union[DmMode, int] | 弹幕类型. Defaults to DmMode.SPECIAL. |
| pool | int | 弹幕池. Defaults to 2. |


---

## class StatementException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

条件异常。




---

## class VideoUploadException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

视频上传错误。




---

## class WbiRetryTimesExceedException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

Wbi 重试达到最大次数




---

## def aid2bvid()

AV 号转 BV 号。

| name | type | description |
| - | - | - |
| aid | int | AV 号。 |

**Returns:** str: BV 号。




---

## def bvid2aid()

BV 号转 AV 号。

| name | type | description |
| - | - | - |
| bvid | str | BV 号。 |

**Returns:** int: AV 号。




---

## async def get_bili_ticket()

获取 bili_ticket


| name | type | description |
| - | - | - |
| credential | Union[Credential, None] | 凭据. Defaults to None. |

**Returns:** str: bili_ticket




---

## async def get_buvid()

获取 buvid3 和 buvid4



**Returns:** Tuple[str, str]: 第 0 项为 buvid3，第 1 项为 buvid4。




---

## def get_client()

在当前事件循环下获取模块正在使用的请求客户端



**Returns:** BiliAPIClient: 请求客户端




---

## async def get_real_url()

获取短链接跳转目标，以进行操作。


| name | type | description |
| - | - | - |
| short_url | str | 短链接。 |
| credential | Credential \| None | 凭据类。 |

**Returns:** 目标链接（如果不是有效的链接会报错）


返回值为原 url 类型



---

## def get_selected_client()

获取用户选择的请求客户端名称和对应的类



**Returns:** Tuple[str, Type[BiliAPIClient]]: 第 0 项为客户端名称，第 1 项为对应的类

**Note**: 模块默认使用 `curl_cffi` 库作为请求客户端。



---

## def get_session()

在当前事件循环下获取请求客户端的会话对象。



**Returns:** object: 会话对象




---

## async def get_wbi_mixin_key()

获取 wbi mixin key


| name | type | description |
| - | - | - |
| credential | Union[Credential, None] | 凭据. Defaults to None. |

**Returns:** str: wbi mixin key




---

## async def parse_link()

调用 yarl 解析 bilibili url 的函数。


| name | type | description |
| - | - | - |
| url | str | 链接 |
| credential | Credential | 凭据类 |

**Returns:** Tuple[obj, ResourceType]: (对象，类型) 或 -1,-1 表示出错




---

## def refresh_bili_ticket()

刷新 bili_ticket



**Returns:** None



---

## def refresh_buvid()

刷新 buvid3 和 buvid4



**Returns:** None



---

## def refresh_wbi_mixin_key()

刷新 wbi mixin key



**Returns:** None



---

## def register_client()

注册请求客户端，可用于用户自定义请求客户端。


| name | type | description |
| - | - | - |
| name | str | 请求客户端类型名称，用户自定义命名。 |
| cls | type | 基于 BiliAPIClient 重写后的请求客户端类。 |
| **Note**: 模块默认使用 `curl_cffi` 库作为请求客户端。 |  | 模块默认使用 `curl_cffi` 库作为请求客户端。 |

**Returns:** None



---

## def select_client()

选择模块使用的注册过的请求客户端，可用于用户自定义请求客户端。


| name | type | description |
| - | - | - |
| name | str | 请求客户端类型名称，用户自定义命名。 |
| **Note**: 模块默认使用 `curl_cffi` 库作为请求客户端。 |  | 模块默认使用 `curl_cffi` 库作为请求客户端。 |

**Returns:** None



---

## def set_session()

在当前事件循环下设置请求客户端的会话对象。


| name | type | description |
| - | - | - |
| session | object | 会话对象 |

**Returns:** None



---

## def sync()

同步执行异步函数，使用可参考 [同步执行异步代码](https://nemo2011.github.io/bilibili-api/#/sync-executor)


| name | type | description |
| - | - | - |
| obj | Coroutine \| Future | 异步函数 |

**Returns:** 该异步函数的返回值




---

## def unregister_client()

取消注册请求客户端，可用于用户自定义请求客户端。


| name | type | description |
| - | - | - |
| name | str | 请求客户端类型名称，用户自定义命名。 |
| **Note**: 模块默认使用 `curl_cffi` 库作为请求客户端。 |  | 模块默认使用 `curl_cffi` 库作为请求客户端。 |

**Returns:** None



