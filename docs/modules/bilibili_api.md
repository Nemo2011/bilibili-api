# Module bilibili_api


bilibili_api

哔哩哔哩的各种 API 调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。

 (默认已导入所有子模块，例如 `bilibili_api.video`, `bilibili_api.user`)


``` python
from bilibili_api import ...
```

- [class ApiException()](#class-ApiException)
- [class ArgsException()](#class-ArgsException)
- [class AsyncEvent()](#class-AsyncEvent)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def add\_event\_listener()](#def-add\_event\_listener)
  - [def dispatch()](#def-dispatch)
  - [def ignore\_event()](#def-ignore\_event)
  - [def on()](#def-on)
  - [def remove\_all\_event\_listener()](#def-remove\_all\_event\_listener)
  - [def remove\_event\_listener()](#def-remove\_event\_listener)
  - [def remove\_ignore\_events()](#def-remove\_ignore\_events)
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
  - [async def get\_buvid\_cookies()](#async-def-get\_buvid\_cookies)
  - [def get\_cookies()](#def-get\_cookies)
  - [def has\_ac\_time\_value()](#def-has\_ac\_time\_value)
  - [def has\_bili\_jct()](#def-has\_bili\_jct)
  - [def has\_buvid3()](#def-has\_buvid3)
  - [def has\_buvid4()](#def-has\_buvid4)
  - [def has\_dedeuserid()](#def-has\_dedeuserid)
  - [def has\_sessdata()](#def-has\_sessdata)
  - [def raise\_for\_no\_ac\_time\_value()](#def-raise\_for\_no\_ac\_time\_value)
  - [def raise\_for\_no\_bili\_jct()](#def-raise\_for\_no\_bili\_jct)
  - [def raise\_for\_no\_buvid3()](#def-raise\_for\_no\_buvid3)
  - [def raise\_for\_no\_buvid4()](#def-raise\_for\_no\_buvid4)
  - [def raise\_for\_no\_dedeuserid()](#def-raise\_for\_no\_dedeuserid)
  - [def raise\_for\_no\_sessdata()](#def-raise\_for\_no\_sessdata)
  - [async def refresh()](#async-def-refresh)
- [class CredentialNoAcTimeValueException()](#class-CredentialNoAcTimeValueException)
- [class CredentialNoBiliJctException()](#class-CredentialNoBiliJctException)
- [class CredentialNoBuvid3Exception()](#class-CredentialNoBuvid3Exception)
- [class CredentialNoBuvid4Exception()](#class-CredentialNoBuvid4Exception)
- [class CredentialNoDedeUserIDException()](#class-CredentialNoDedeUserIDException)
- [class CredentialNoSessdataException()](#class-CredentialNoSessdataException)
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
  - [def get\_test\_type()](#def-get\_test\_type)
  - [def has\_done()](#def-has\_done)
  - [def start\_geetest\_server()](#def-start\_geetest\_server)
  - [def test\_generated()](#def-test\_generated)
- [class GeetestException()](#class-GeetestException)
- [class GeetestMeta()](#class-GeetestMeta)
- [class GeetestType()](#class-GeetestType)
- [var HEADERS](#var-HEADERS)
- [class LiveException()](#class-LiveException)
- [class LoginError()](#class-LoginError)
- [class NetworkException()](#class-NetworkException)
- [class Picture()](#class-Picture)
  - [def convert\_format()](#def-convert\_format)
  - [def from\_content()](#def-from\_content)
  - [def from\_file()](#def-from\_file)
  - [async def load\_url()](#async-def-load\_url)
  - [def resize()](#def-resize)
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
- [async def bili\_simple\_download()](#async-def-bili\_simple\_download)
- [def bvid2aid()](#def-bvid2aid)
- [def get\_available\_settings()](#def-get\_available\_settings)
- [def get\_client()](#def-get\_client)
- [async def get\_real\_url()](#async-def-get\_real\_url)
- [def get\_registered\_available\_settings()](#def-get\_registered\_available\_settings)
- [def get\_registered\_clients()](#def-get\_registered\_clients)
- [def get\_selected\_client()](#def-get\_selected\_client)
- [def get\_session()](#def-get\_session)
- [async def parse\_link()](#async-def-parse\_link)
- [def recalculate\_wbi()](#def-recalculate\_wbi)
- [def refresh\_bili\_ticket()](#def-refresh\_bili\_ticket)
- [def refresh\_buvid()](#def-refresh\_buvid)
- [def register\_client()](#def-register\_client)
- [var request\_log](#var-request\_log)
  - [def get\_ignore\_events()](#def-get\_ignore\_events)
  - [def get\_on\_events()](#def-get\_on\_events)
  - [def is\_on()](#def-is\_on)
  - [def set\_ignore\_events()](#def-set\_ignore\_events)
  - [def set\_on()](#def-set\_on)
  - [def set\_on\_events()](#def-set\_on\_events)
- [var request\_settings](#var-request\_settings)
  - [def get()](#def-get)
  - [def get\_all()](#def-get\_all)
  - [def get\_enable\_auto\_buvid()](#def-get\_enable\_auto\_buvid)
  - [def get\_enable\_bili\_ticket()](#def-get\_enable\_bili\_ticket)
  - [def get\_proxy()](#def-get\_proxy)
  - [def get\_timeout()](#def-get\_timeout)
  - [def get\_trust\_env()](#def-get\_trust\_env)
  - [def get\_verify\_ssl()](#def-get\_verify\_ssl)
  - [def get\_wbi\_retry\_times()](#def-get\_wbi\_retry\_times)
  - [def set()](#def-set)
  - [def set\_enable\_auto\_buvid()](#def-set\_enable\_auto\_buvid)
  - [def set\_enable\_bili\_ticket()](#def-set\_enable\_bili\_ticket)
  - [def set\_proxy()](#def-set\_proxy)
  - [def set\_timeout()](#def-set\_timeout)
  - [def set\_trust\_env()](#def-set\_trust\_env)
  - [def set\_verify\_ssl()](#def-set\_verify\_ssl)
  - [def set\_wbi\_retry\_times()](#def-set\_wbi\_retry\_times)
- [def select\_client()](#def-select\_client)
- [def set\_session()](#def-set\_session)
- [def sync()](#def-sync)
- [def unregister\_client()](#def-unregister\_client)

---

## class ApiException()

**Extend: builtins.Exception**

API 基类异常。




---

## class ArgsException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

参数错误。




---

## class AsyncEvent()

发布-订阅模式异步事件类支持。

特殊事件：__ALL__ 所有事件均触发




### def \_\_init\_\_()





### def add_event_listener()

注册事件监听器。


| name | type | description |
| - | - | - |
| `name` | `str` | 事件名。 |
| `handler` | `Union[Callable, Coroutine]` | 回调函数。 |




### def dispatch()

异步发布事件。


| name | type | description |
| - | - | - |
| `name` | `str` | 事件名。 |
| `*args, **kwargs` | `Any` | 要传递给函数的参数。 |




### def ignore_event()

忽略指定事件


| name | type | description |
| - | - | - |
| `name` | `str` | 事件名。 |




### def on()

装饰器注册事件监听器。


| name | type | description |
| - | - | - |
| `event_name` | `str` | 事件名。 |




### def remove_all_event_listener()

移除所有事件监听函数






### def remove_event_listener()

移除事件监听函数。


| name | type | description |
| - | - | - |
| `name` | `str` | 事件名。 |
| `handler` | `Union[Callable, Coroutine]` | 要移除的函数。 |

**Returns:** `bool`:  是否移除成功。




### def remove_ignore_events()

移除所有忽略事件






---

## class BiliAPIClient()

**Extend: abc.ABC**


请求客户端抽象类。通过对第三方模块请求客户端的封装令模块可对其进行调用。

``` python
class BiliAPIClient(ABC):
    """
    请求客户端抽象类。通过对第三方模块请求客户端的封装令模块可对其进行调用。
    """

    @abstractmethod
    def __init__(
        self,
        proxy: str = "",
        timeout: float = 0.0,
        verify_ssl: bool = True,
        trust_env: bool = True,
        session: Optional[object] = None,
    ) -> None:
        """
        Args:
            proxy (str, optional): 代理地址. Defaults to "".
            timeout (float, optional): 请求超时时间. Defaults to 0.0.
            verify_ssl (bool, optional): 是否验证 SSL. Defaults to True.
            trust_env (bool, optional): `trust_env`. Defaults to True.
            session (object, optional): 会话对象. Defaults to None.

        Note: 仅当用户只提供 `session` 参数且用户中途未调用 `set_xxx` 函数才使用用户提供的 `session`。
        """
        raise NotImplementedError

    @abstractmethod
    def get_wrapped_session(self) -> object:
        """
        获取封装的第三方会话对象

        Returns:
            object: 第三方会话对象
        """
        raise NotImplementedError

    @abstractmethod
    def set_timeout(self, timeout: float = 0.0) -> None:
        """
        设置请求超时时间

        Args:
            timeout (float, optional): 请求超时时间. Defaults to 0.0.
        """
        raise NotImplementedError

    @abstractmethod
    def set_proxy(self, proxy: str = "") -> None:
        """
        设置代理地址

        Args:
            proxy (str, optional): 代理地址. Defaults to "".
        """
        raise NotImplementedError

    @abstractmethod
    def set_verify_ssl(self, verify_ssl: bool = True) -> None:
        """
        设置是否验证 SSL

        Args:
            verify_ssl (bool, optional): 是否验证 SSL. Defaults to True.
        """
        raise NotImplementedError

    @abstractmethod
    def set_trust_env(self, trust_env: bool = True) -> None:
        """
        设置 `trust_env`

        Args:
            trust_env (bool, optional): `trust_env`. Defaults to True.
        """
        raise NotImplementedError

    @abstractmethod
    async def request(
        self,
        method: str = "",
        url: str = "",
        params: dict = {},
        data: Union[dict, str, bytes] = {},
        files: Dict[str, BiliAPIFile] = {},
        headers: dict = {},
        cookies: dict = {},
        allow_redirects: bool = True,
    ) -> BiliAPIResponse:
        """
        进行 HTTP 请求

        Args:
            method (str, optional): 请求方法. Defaults to "".
            url (str, optional): 请求地址. Defaults to "".
            params (dict, optional): 请求参数. Defaults to {}.
            data (Union[dict, str, bytes], optional): 请求数据. Defaults to {}.
            files (Dict[str, BiliAPIFile], optional): 请求文件. Defaults to {}.
            headers (dict, optional): 请求头. Defaults to {}.
            cookies (dict, optional): 请求 Cookies. Defaults to {}.
            allow_redirects (bool, optional): 是否允许重定向. Defaults to True.

        Returns:
            BiliAPIResponse: 响应对象

        Note: 无需实现 data 为 str 且 files 不为空的情况。
        """
        raise NotImplementedError

    @abstractmethod
    async def download_create(
        self,
        url: str = "",
        headers: dict = {},
    ) -> int:
        """
        开始下载文件

        Args:
            url     (str, optional) : 请求地址. Defaults to "".
            headers (dict, optional): 请求头. Defaults to {}.

        Returns:
            int: 下载编号，用于后续操作。
        """
        raise NotImplementedError

    @abstractmethod
    async def download_chunk(self, cnt: int) -> bytes:
        """
        下载部分文件

        Args:
            cnt    (int): 下载编号

        Returns:
            bytes: 字节
        """
        raise NotImplementedError

    @abstractmethod
    def download_content_length(self, cnt: int) -> int:
        """
        获取下载总字节数

        Args:
            cnt    (int): 下载编号

        Returns:
            int: 下载总字节数
        """
        raise NotImplementedError

    @abstractmethod
    async def ws_create(
        self, url: str = "", params: dict = {}, headers: dict = {}
    ) -> int:
        """
        创建 WebSocket 连接

        Args:
            url (str, optional): WebSocket 地址. Defaults to "".
            params (dict, optional): WebSocket 参数. Defaults to {}.
            headers (dict, optional): WebSocket 头. Defaults to {}.

        Returns:
            int: WebSocket 连接编号，用于后续操作。
        """
        raise NotImplementedError

    @abstractmethod
    async def ws_send(self, cnt: int, data: bytes) -> None:
        """
        发送 WebSocket 数据

        Args:
            cnt (int): WebSocket 连接编号
            data (bytes): WebSocket 数据
        """
        raise NotImplementedError

    @abstractmethod
    async def ws_recv(self, cnt: int) -> Tuple[bytes, BiliWsMsgType]:
        """
        接受 WebSocket 数据

        Args:
            cnt (int): WebSocket 连接编号

        Returns:
            Tuple[bytes, BiliWsMsgType]: WebSocket 数据和状态

        Note: 建议实现此函数时支持其他线程关闭不阻塞，除基础状态同时实现 CLOSING, CLOSED。
        """
        raise NotImplementedError

    @abstractmethod
    async def ws_close(self, cnt: int) -> None:
        """
        关闭 WebSocket 连接

        Args:
            cnt (int): WebSocket 连接编号
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        """
        关闭请求客户端，即关闭封装的第三方会话对象
        """
        raise NotImplementedError
```



---

**@dataclasses.dataclass** 

## class BiliAPIFile()

上传文件类。


| name | type | description |
| - | - | - |
| `path` | `str` | 文件地址 |
| `mime_type` | `str` | 文件类型 |


---

**@dataclasses.dataclass** 

## class BiliAPIResponse()

响应对象类。


| name | type | description |
| - | - | - |
| `code` | `int` | 响应码 |
| `headers` | `Dict` | 响应头 |
| `cookies` | `Dict` | 当前状态的 cookies |
| `raw` | `bytes` | 响应数据 |
| `url` | `str` | 当前 url |


### def json()

解析 json



**Returns:** `object`:  解析后的 json




### def utf8_text()

转为 utf8 文字



**Returns:** `str`:  utf8 文字




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
| `sessdata` | `str \| None, optional` | 浏览器 Cookies 中的 SESSDATA 字段值. Defaults to None. |
| `bili_jct` | `str \| None, optional` | 浏览器 Cookies 中的 bili_jct 字段值. Defaults to None. |
| `buvid3` | `str \| None, optional` | 浏览器 Cookies 中的 BUVID3 字段值. Defaults to None. |
| `buvid4` | `str \| None, optional` | 浏览器 Cookies 中的 BUVID4 字段值. Defaults to None. |
| `dedeuserid` | `str \| None, optional` | 浏览器 Cookies 中的 DedeUserID 字段值. Defaults to None. |
| `ac_time_value` | `str \| None, optional` | 浏览器 Cookies 中的 ac_time_value 字段值. Defaults to None. |


### async def check_refresh()

检查是否需要刷新 cookies



**Returns:** `bool`:  cookies 是否需要刷新




### async def check_valid()

检查 cookies 是否有效



**Returns:** `bool`:  cookies 是否有效




**@staticmethod** 

### def from_cookies()

从 cookies 新建 Credential


| name | type | description |
| - | - | - |
| `cookies` | `Dict, optional` | Cookies. Defaults to {}. |

**Returns:** `Credential`:  凭据类




### async def get_buvid_cookies()

获取请求 Cookies 字典，自动补充 buvid 字段



**Returns:** `dict`:  请求 Cookies 字典




### def get_cookies()

获取请求 Cookies 字典



**Returns:** `dict`:  请求 Cookies 字典




### def has_ac_time_value()

是否提供 ac_time_value



**Returns:** `bool`:  是否提供 ac_time_value




### def has_bili_jct()

是否提供 bili_jct。



**Returns:** `bool`:  是否提供 bili_jct。




### def has_buvid3()

是否提供 buvid3



**Returns:** `bool`:  是否提供 buvid3




### def has_buvid4()

是否提供 buvid4



**Returns:** `bool`:  是否提供 buvid4




### def has_dedeuserid()

是否提供 dedeuserid。



**Returns:** `bool`:  是否提供 dedeuserid。




### def has_sessdata()

是否提供 sessdata。



**Returns:** `bool`:  是否提供 sessdata。




### def raise_for_no_ac_time_value()

没有提供 ac_time_value 时抛出异常。






### def raise_for_no_bili_jct()

没有提供 bili_jct 则抛出异常。






### def raise_for_no_buvid3()

没有提供 buvid3 时抛出异常。






### def raise_for_no_buvid4()

没有提供 buvid3 时抛出异常。






### def raise_for_no_dedeuserid()

没有提供 DedeUserID 时抛出异常。






### def raise_for_no_sessdata()

没有提供 sessdata 则抛出异常。






### async def refresh()

刷新 cookies






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

Credential 类未提供 buvid3 时的异常。




---

## class CredentialNoBuvid4Exception()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

Credential 类未提供 buvid4 时的异常。




---

## class CredentialNoDedeUserIDException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

Credential 类未提供 DedeUserID 时的异常。




---

## class CredentialNoSessdataException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

Credential 类未提供 sessdata 时的异常。




---

## class Danmaku()

弹幕类。




### def \_\_init\_\_()

大会员专属颜色文字填充：http://i0.hdslb.com/bfs/dm/9dcd329e617035b45d2041ac889c49cb5edd3e44.png

大会员专属颜色背景填充：http://i0.hdslb.com/bfs/dm/ba8e32ae03a0a3f70f4e51975a965a9ddce39d50.png


| name | type | description |
| - | - | - |
| `text` | `str` | 弹幕文本。 |
| `dm_time` | `float, optional` | 弹幕在视频中的位置，单位为秒。Defaults to 0.0. |
| `send_time` | `float, optional` | 弹幕发送的时间。Defaults to time.time(). |
| `crc32_id` | `str, optional` | 弹幕发送者 UID 经 CRC32 算法取摘要后的值。Defaults to "". |
| `color` | `str, optional` | 弹幕十六进制颜色。Defaults to "ffffff" (如果为大会员专属的颜色则为"special"). |
| `weight` | `int, optional` | 弹幕在弹幕列表显示的权重。Defaults to -1. |
| `id_` | `int, optional` | 弹幕 ID。Defaults to -1. |
| `id_str` | `str, optional` | 弹幕字符串 ID。Defaults to "". |
| `action` | `str, optional` | 暂不清楚。Defaults to "". |
| `mode` | `Union[DmMode, int], optional` | 弹幕模式。Defaults to Mode.FLY. |
| `font_size` | `Union[DmFontSize, int], optional` | 弹幕字体大小。Defaults to FontSize.NORMAL. |
| `is_sub` | `bool, optional` | 是否为字幕弹幕。Defaults to False. |
| `pool` | `int, optional` | 池。Defaults to 0. |
| `attr` | `int, optional` | 暂不清楚。 Defaults to -1. |
| `uid` | `int, optional` | 弹幕发送者 UID。Defaults to -1. |


**@staticmethod** 

### def crack_uid()

(@staticmethod)

暴力破解 UID，可能存在误差，请慎重使用。

精确至 UID 小于 10000000 的破解。


| name | type | description |
| - | - | - |
| `crc32_id` | `str` | crc32 id |

**Returns:** `int`:  真实 UID。




### def to_xml()

将弹幕转换为 xml 格式弹幕



**Returns:** `str`:  xml




---

## class DanmakuClosedException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

视频弹幕被关闭错误。




---

## class DmFontSize()

**Extend: enum.Enum**

字体大小枚举。

- EXTREME_SMALL
- SUPER_SMALL
- SMALL
- NORMAL
- BIG
- SUPER_BIG
- EXTREME_BIG




---

## class DmMode()

**Extend: enum.Enum**

弹幕模式枚举。

- FLY: 飞行弹幕
- TOP: 置顶弹幕
- BOTTOM: 底部弹幕
- REVERSE: 反向弹幕
- ADVANCE: 高级弹幕
- CODE: 代码弹幕 (基于 flash 实现)
- SPECIAL: BAS 弹幕




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






### def complete_test()

作答测试


| name | type | description |
| - | - | - |
| `validate` | `str` | 作答结果的 validate |
| `seccode` | `str` | 作答结果的 seccode |




### async def generate_test()

创建验证码


| name | type | description |
| - | - | - |
| `type_` | `GeetestType` | 极验验证码类型。登录为 LOGIN，登录验证为 VERIFY. Defaults to GeetestType.LOGIN. |




### def get_geetest_server_url()

获取本地极验验证码服务链接



**Returns:** `str`:  链接




### def get_info()

获取验证码信息



**Returns:** `GeetestMeta`:  验证码信息




### def get_result()

获取结果



**Returns:** `GeetestMeta`:  验证结果




### def get_test_type()

获取测试类型



**Returns:** `GeetestType`:  测试类型




### def has_done()

是否完成



**Returns:** `bool`:  是否完成




### def start_geetest_server()

开启本地极验验证码服务






### def test_generated()

当前是否有创建的测试



**Returns:** `bool`:  是否有创建的测试




---

## class GeetestException()

**Extend: bilibili_api.exceptions.ApiException.ApiException**

未找到验证码服务器




---

**@dataclasses.dataclass** 

## class GeetestMeta()

极验验证码完成信息

NOTE: `gt`, `challenge`, `token` 为验证码基本字段。`seccode`, `validate` 为完成验证码后可得字段。




---

## class GeetestType()

**Extend: enum.Enum**

极验验证码类型

- LOGIN: 登录
- VERIFY: 登录验证




---

## var HEADERS

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

可以不实例化，用 `load_url`, `from_content` 或 `from_file` 加载图片。


| name | type | description |
| - | - | - |
| `height` | `int` | 高度 |
| `imageType` | `str` | 格式，例如 |
| `size` | `Any` | 大小。单位 KB |
| `url` | `str` | 图片链接 |
| `width` | `int` | 宽度 |
| `content` | `bytes` | 图片内容 |


### def convert_format()

将图片转换为另一种格式。


| name | type | description |
| - | - | - |
| `new_format` | `str` | 新的格式。例：`png`, `ico`, `webp`. |

**Returns:** `Picture`:  `self`




**@staticmethod** 

### def from_content()

加载字节数据


| name | type | description |
| - | - | - |
| `content` | `str` | 图片内容 |
| `format` | `str` | 图片后缀名，如 `webp`, `jpg`, `ico` |

**Returns:** `Picture`:  加载后的图片对象




**@staticmethod** 

### def from_file()

加载本地图片。


| name | type | description |
| - | - | - |
| `path` | `str` | 图片地址 |

**Returns:** `Picture`:  加载后的图片对象




**@staticmethod** 

### async def load_url()

加载网络图片。(async 方法)


| name | type | description |
| - | - | - |
| `url` | `str` | 图片链接 |

**Returns:** `Picture`:  加载后的图片对象




### def resize()

调整大小


| name | type | description |
| - | - | - |
| `width` | `int` | 宽度 |
| `height` | `int` | 高度 |

**Returns:** `Picture`:  `self`




### def to_file()

下载图片至本地。


| name | type | description |
| - | - | - |
| `path` | `str` | 下载地址。 |

**Returns:** `Picture`:  `self`




### async def upload()

上传图片至 B 站。


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类。 |

**Returns:** `Picture`:  `self`




### async def upload_by_note()

通过笔记接口上传图片至 B 站。


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类。 |

**Returns:** `Picture`:  `self`




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
+ OPUS: 图文
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
| `content` | `str` | 弹幕内容 |
| `id_` | `int` | 弹幕 id. Defaults to -1. |
| `id_str` | `str` | 弹幕 id (string 类型). Defaults to "". |
| `mode` | `Union[DmMode, int]` | 弹幕类型. Defaults to DmMode.SPECIAL. |
| `pool` | `int` | 弹幕池. Defaults to 2. |


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
| `aid` | `int` | AV 号。 |

**Returns:** `str`:  BV 号。




---

## async def bili_simple_download()

适用于下载 bilibili 链接的简易终端下载函数

默认会携带 HEADERS 访问链接，避免 403

用途举例：下载 video.get_download_url 返回结果中的链接


| name | type | description |
| - | - | - |
| `url` | `str` | 链接 |
| `out` | `str` | 输出地址 |
| `intro` | `str` | 下载简述 |




---

## def bvid2aid()

BV 号转 AV 号。

| name | type | description |
| - | - | - |
| `bvid` | `str` | BV 号。 |

**Returns:** `int`:  AV 号。




---

## def get_available_settings()

获取当前支持的设置项



**Returns:** `List[str]`:  支持的设置项名称




---

## def get_client()

在当前事件循环下获取模块正在使用的请求客户端



**Returns:** `BiliAPIClient`:  请求客户端




---

## async def get_real_url()

获取短链接跳转目标，以进行操作。


| name | type | description |
| - | - | - |
| `short_url` | `str` | 短链接。 |
| `credential` | `Credential \| None` | 凭据类。 |

**Returns:** `str`:  目标链接（如果不是有效的链接会报错）




---

## def get_registered_available_settings()

获取所有注册过的 BiliAPIClient 所支持的设置项



**Returns:** `Dict[str, List[str]]`:  所有注册过的 BiliAPIClient 所支持的设置项




---

## def get_registered_clients()

获取所有注册过的 BiliAPIClient



**Returns:** `Dict[str, Type[BiliAPIClient]]`:  注册过的 BiliAPIClient




---

## def get_selected_client()

获取用户选择的请求客户端名称和对应的类



**Returns:** `Tuple[str, Type[BiliAPIClient]]`:  第 0 项为客户端名称，第 1 项为对应的类




---

## def get_session()

在当前事件循环下获取请求客户端的会话对象。



**Returns:** `object`:  会话对象




---

## async def parse_link()

调用 yarl 解析 bilibili url 的函数。


| name | type | description |
| - | - | - |
| `url` | `str` | 链接 |
| `credential` | `Credential` | 凭据类 |

**Returns:** `Tuple[obj, ResourceType]`:  (对象，类型) 或 -1,-1 表示出错




---

## def recalculate_wbi()

重新计算 wbi 的参数






---

## def refresh_bili_ticket()

刷新 bili_ticket






---

## def refresh_buvid()

刷新模块自动生成的 buvid3 和 buvid4






---

## def register_client()

注册请求客户端并切换，可用于用户自定义请求客户端。


| name | type | description |
| - | - | - |
| `name` | `str` | 请求客户端类型名称，用户自定义命名。 |
| `cls` | `type` | 基于 BiliAPIClient 重写后的请求客户端类。 |
| `settings` | `Dict` | 请求客户端在基础设置外的其他设置，键为设置名称，值为设置默认值。Defaults to {}. |




---

## var request_log

**Extend: AsyncEvent**


请求日志支持，默认支持输出到指定 I/O 对象。

可以添加更多监听器达到更多效果。

Logger: request_log.logger

Extends: AsyncEvent

Events:

- (模块自带 BiliAPIClient)
- REQUEST:     HTTP 请求。
- RESPONSE:    HTTP 响应。
- WS_CREATE:   新建的 Websocket 请求。
- WS_RECV:     获得到 WebSocket 请求。
- WS_SEND:     发送了 WebSocket 请求。
- WS_CLOSE:    关闭 WebSocket 请求。
- DWN_CREATE:  新建下载。
- DWN_PART:    部分下载。
- (Api)
- API_REQUEST: Api 请求。
- API_RESPONSE: Api 响应。
- (反爬虫)
- ANTI_SPIDER: 反爬虫相关信息。

CallbackData: 描述 (str) 数据 (dict)

示例：

``` python
@request_log.on("REQUEST")
async def handle(desc: str, data: dict) -> None:
    print(desc, data)
```

默认启用 Api 和 Anti-Spider 相关信息。



### def get_ignore_events()

获取日志输出排除的事件类型



**Returns:** `List[str]`:  日志输出排除的事件类型




### def get_on_events()

获取日志输出支持的事件类型



**Returns:** `List[str]`:  日志输出支持的事件类型




### def is_on()

获取日志输出是否启用



**Returns:** `bool`:  是否启用




### def set_ignore_events()

设置日志输出排除的事件类型


| name | type | description |
| - | - | - |
| `events` | `List[str]` | 日志输出排除的事件类型 |




### def set_on()

设置日志输出是否启用


| name | type | description |
| - | - | - |
| `status` | `bool` | 是否启用 |




### def set_on_events()

设置日志输出支持的事件类型


| name | type | description |
| - | - | - |
| `events` | `List[str]` | 日志输出支持的事件类型 |




---

## var request_settings

请求参数设置



### def get()

获取某项设置

不可用于 `wbi_retry_times` `enable_auto_buvid` `enable_bili_ticket`

默认设置名称：`proxy` `timeout` `verify_ssl` `trust_env`


| name | type | description |
| - | - | - |
| `name` | `str` | 设置名称 |

**Returns:** `Any`:  设置的值




### def get_all()

获取目前所有的设置项

不可用于 `wbi_retry_times` `enable_auto_buvid` `enable_bili_ticket`



**Returns:** `dict`:  所有的设置项




### def get_enable_auto_buvid()

获取设置的是否自动生成 buvid



**Returns:** `bool`:  是否自动生成 buvid. Defaults to True.




### def get_enable_bili_ticket()

获取设置的是否使用 bili_ticket



**Returns:** `bool`:  是否使用 bili_ticket. Defaults to True.




### def get_proxy()

获取设置的代理



**Returns:** `str`:  代理地址. Defaults to "".




### def get_timeout()

获取设置的 web 请求超时时间



**Returns:** `float`:  超时时间. Defaults to 5.0.




### def get_trust_env()

获取设置的 `trust_env`



**Returns:** `bool`:  `trust_env`. Defaults to True.




### def get_verify_ssl()

获取设置的是否验证 SSL



**Returns:** `bool`:  是否验证 SSL. Defaults to True.




### def get_wbi_retry_times()

获取设置的 wbi 重试次数



**Returns:** `int`:  wbi 重试次数. Defaults to 3.




### def set()

设置某项设置

不可用于 `wbi_retry_times` `enable_auto_buvid` `enable_bili_ticket`

默认设置名称：`proxy` `timeout` `verify_ssl` `trust_env`


| name | type | description |
| - | - | - |
| `name` | `str` | 设置名称 |
| `value` | `str` | 设置的值 |




### def set_enable_auto_buvid()

设置是否自动生成 buvid


| name | type | description |
| - | - | - |
| `enable_auto_buvid` | `bool` | 是否自动生成 buvid. |




### def set_enable_bili_ticket()

设置是否使用 bili_ticket


| name | type | description |
| - | - | - |
| `enable_bili_ticket` | `bool` | 是否使用 bili_ticket. |




### def set_proxy()

修改设置的代理


| name | type | description |
| - | - | - |
| `proxy` | `str` | 代理地址 |




### def set_timeout()

修改设置的 web 请求超时时间


| name | type | description |
| - | - | - |
| `timeout` | `float` | 超时时间 |




### def set_trust_env()

修改设置的 `trust_env`


| name | type | description |
| - | - | - |
| `verify_ssl` | `bool` | `trust_env` |




### def set_verify_ssl()

修改设置的是否验证 SSL


| name | type | description |
| - | - | - |
| `verify_ssl` | `bool` | 是否验证 SSL |




### def set_wbi_retry_times()

修改设置的 wbi 重试次数


| name | type | description |
| - | - | - |
| `wbi_retry_times` | `int` | wbi 重试次数. |




---

## def select_client()

选择模块使用的注册过的请求客户端，可用于用户自定义请求客户端。


| name | type | description |
| - | - | - |
| `name` | `str` | 请求客户端类型名称，用户自定义命名。 |




---

## def set_session()

在当前事件循环下设置请求客户端的会话对象。


| name | type | description |
| - | - | - |
| `session` | `object` | 会话对象 |




---

## def sync()

同步执行异步函数，使用可参考 [同步执行异步代码](https://nemo2011.github.io/bilibili-api/#/sync-executor)


| name | type | description |
| - | - | - |
| `obj` | `Coroutine \| Future` | 异步函数 |

**Returns:** `Any`:  该异步函数的返回值




---

## def unregister_client()

取消注册请求客户端，可用于用户自定义请求客户端。


| name | type | description |
| - | - | - |
| `name` | `str` | 请求客户端类型名称，用户自定义命名。 |




