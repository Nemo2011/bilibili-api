# 自定义请求库

bilibili_api 作为一个爬虫库，自然依靠底层的网络请求库得以实现。具体地，bilibili_api 会在每次运行中使用可持久化的会话对象（`session`），相较于直接一次次地发起请求，这么做可以复用 `TCP` 连接，提高整体性能。

bilibili_api 默认使用 `curl_cffi` 作为底层的第三方请求库，但是第三方请求库可能面临着在具体项目中被更换/替代的需求，例如原来项目就一直用 `aiohttp`，现在又来了一个 `curl_cffi`，二者创建会话不同，`session` 的存在貌似没有了意义，这时候将二者的会话统一至关重要。也有一种可能，bilibili_api 使用的请求库在某些方面不如另一个请求库，而且会对实际造成部分影响，这对你来说很重要，你希望 bilibili_api 能使用那个更好的请求库。（例如 `aiohttp` 容易 `ServerDisconnected`，而 `httpx` 基本不会出现这种问题）因此模块也同时兼容其他的第三方请求库作为底层请求库，在此前提下可以更改模块使用的 `session`（具体如何支持见下文）。

众所周知，但是每个网络请求模块实现的逻辑可能不同，api 也可能不同，调用时针对不同的请求库需要使用不同的传参方式和不同的回调方式，乃至是不同的函数和不同的流程。那么模块是怎么做到兼容其他第三方请求库的？事实上，这中间存在另一个中间层，`client`。`client` 相关代码需要用户自己编写，其需要满足对第三方请求库的 `session` 的封装，对外暴露模块规定的 api，这样子只需要用户在外部重写 `client` 而非重写模块的代码即可实现对请求库的替代。

下文 `client` 均表示 **bilibili_api 在请求中连接 `Api` 类和第三方请求库（诸如 `curl_cffi`, `aiohttp`）的中间层**，`session` 均表示 **第三方请求库（诸如 `curl_cffi`, `aiohttp`）在模块每次运行中使用可持久化的会话对象**。

## 1、bilibili_api 是如何发起请求的？

我们以 `user.User().get_user_info()` 为例。此处选择的 `User` 实例为站长（`uid=1`）。我们大致简化这个过程，以解释 bilibili_api 发起请求的全过程。

首先，一般地，你所调用的所有函数都会创建一个类的实例，`Api`，可以把它当作请求的载体。这个例子中 `Api` 对象长这样：

- `method`: GET
- `url`: <https://api.bilibili.com/x/space/wbi/acc/info>
- `params`:
    - `mid`: 2
- `wbi`: true
- `wbi2`: true

这里有两个字段，`wbi` 和 `wbi2`，正常网络请求里面怎么可能会有？其实这是 bilibili 的一种风控方式，通过在请求中使用一整套名为 `wbi` 的加密方法达到反爬虫的目的。这套加密方法是通用的，所以无需具体到每一个函数上都执行一遍，于是安排到了 `Api` 类中具体进行加密过程。

接下来让我们看 `Api` 类发起请求的几行代码：

``` python
config = await self._prepare_request()
client = get_client()
resp = await client.request(**config)
```

第一行中，`_prepare_request` 方法就会对诸如 `wbi` 这类的反爬虫加密方式进行处理，操作完后我们可以得到一个 `config` 字典。`config` 字典长这样：

- `method`: GET
- `url`: <https://api.bilibili.com/x/space/wbi/acc/info>
- `params`:
    - `mid`: 2
    - `w_webid`: eyJhbGciOi...
    - `dm_img_list`: []
    - `dm_img_str`: JC
    - `dm_cover_img_str`: AC
    - `dm_img_inter`: {"ds":[],"wh":[0,0,0],"of":[0,0,0]}
    - `wts`: 1737376069
    - `web_location`: 1550101
    - `w_rid`: bfe6d5df5f...

这就是你正常情况下，为了访问这个接口，需要往 `httpx.get`, `aiohttp.get`, `curl_cffi.requests.get` 等第三方库中传入的参数。你在浏览器控制台抓取到的真实请求也应该长这样子。

第二行，我们调用 `get_client`，这个函数会返回一个 `client`。接着在第三行调用这个 `client` 的函数，`client` 会将参数传递到 `session`。

这个例子中，`config` 直接传入 `session` 也是可行的，但是不妨多考虑一下，我们现在还需要获得 `session` 的响应文本。`httpx` 只需要 `resp.text`，而 `aiohttp` 需要 `await resp.text()`，此处已经不能统一处理了。

我们再假设，现在需要上传一个文件（`multipart/form-data`），request-like api 中文件会放入 `files` 参数，而 aiohttp api 中文件需要使用 `FormData` 和其他字段结合后传入 `data`。这里该如何统一处理？

这就是 `client` 的作用：作为中间层，**它为模块提供了固定的 api，从而做到只要更换 `client` 就能更换请求库，而不是更换代码**，至于模块的 api 和第三方请求库的 api 的交接，就是 `client` 内部的事了。

## 2、如何编写 `client`？

**首先需要知道，`client` 本质就是封装 `session`，或者说是把第三方库的 `session` 变成模块认识的 `session`。**

不妨先了解一下 `get_client`。由上一句话，`get_client` 可类比为一个 `get_session` 函数，会话在全局中当然得是同一个，因此理论上 `get_client` 返回的 `client` 是在第一次创建后便一直保留下来的。

但有一点，**不同事件循环中的会话对象不一样。** 因此模块有一个 `client pool`，针对每个事件循环保留 `client`。

模块创建 `client` 时会传入几个 `request_settings` 中的设置，`proxy`, `timeout`, `verify_ssl`, `trust_env`，这些为用户设置的全局设置，`client` 初始化时需要将它们传入到封装 `session` 中。同时上文提到，可以更改模块使用的 `session`，这个操作基于对 `client` 的另一种初始化方式：只传入需要被封装的 `session`，而不是用用户设置的全局设置新建一个 `session`。如果传入了指定的 `session`，则前面的几个全局设置应予以被忽略。上文提到了 `client` 初始化，也是在暗示 `client` 实际上就是类，准确来说是一个抽象类：`bilibili_api.utils.network.BiliAPIClient`。

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
```

我们继续 `client` 其他功能的设计。`client` 发起 http 请求的函数还算好写，或者说还算好封装，希望吧。考虑到 `files` 参数传参方式五花八门，于是模块用了一个 dataclass 对其进行了统一规定（`BiliAPIFile`）。返回结果的 `response` 也有不同，模块也用了一个 dataclass 对其进行了规定（`BiliAPIResponse`）。

``` python
    ...
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
        allow_redirects: bool = False,
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
            allow_redirects (bool, optional): 是否允许重定向. Defaults to False.

        Returns:
            BiliAPIResponse: 响应对象

        Note: 无需实现 data 为 str 且 files 不为空的情况。
        """
        raise NotImplementedError
```

最后来到了 WebSocket 部分模块规定的 Api。众所周知目前偏向主流的是 aiohttp api，即先 `ws_connect` 获取一个 WebSocket 对象，再对这个对象进行操作。至于后续 WebSocket 对象的上下文模式，考虑到编码复杂度，于是模块放弃了上下文模式，同时也放弃了 aiohttp 迭代器式的收取信息的模式，采用了这样的方案：实现一个收取信息的函数，正常连接时堵塞式返回完整信息，连接关闭时自动退出（包括用户关闭），反正相信大家使用的请求库针对 websocket 都有不堵塞的基本的 `recv` 功能。~~httpx 这部分编写时就 `raise NotImplementedError` 好了，不纳入考虑范围~~

``` python
    ...
    @abstractmethod
    async def ws_create(
        self, url: str = "", params: dict = {}, headers: dict = {}, cookies: dict = {}
    ) -> int:
        """
        创建 WebSocket 连接

        Args:
            url (str, optional): WebSocket 地址. Defaults to "".
            params (dict, optional): WebSocket 参数. Defaults to {}.
            headers (dict, optional): WebSocket 头. Defaults to {}.
            cookies (dict, optional): WebSocket Cookies. Defaults to {}.

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
```

同时为了防止同一个 `client` 需要同时操控多个 WebSocket 的情况，`client` 应该用数组保留所有创建的 WebSocket 对象，为防止节外生枝，再搞一个 WebSocket 抽象类出来（也是放弃上下文模式的一个原因），`ws_connect` 结束后应返回一个 `int` 作为对应的 WebSocket 对象的“代号”，而不是直接把第三方请求库的 WebSocket 对象返回。之后涉及 WebSocket 的操作均需要传入 `ws_connect` 时候拿到的“代号”，否则 `client` 无法做到辨认具体是哪个 WebSocket 对象。

还有一些杂七杂八的函数需要实现，详情见接下来会提供的 [抽象类完整代码](#附录、抽象类完整代码)。

## 3、写完了我怎么才能真正地用上？

假设现在有人实现了 `AioHTTPClient` 的抽象类，首先你需要把你写完的成果注册到模块中：

``` python
register_client("aiohttp", AioHTTPClient)
```

第一参就是随便取个名字，注意传第二参的时候传入的是类，不是实例。

然后用函数选择你需要的请求客户端，传入你所取的名字。

``` python
select_client("aiohttp")
```

当然也可以取消注册：

``` python
unregister_client("aiohttp")
```

前面提到一种需求，即统一 bilibili_api 和外部程序的会话，即让 bilibili_api 去用外部程序的一个 `curl_cffi.requests.AsyncSession`，这时候便能通过 `set_session` 设置。

``` python
set_session(curl_cffi.requests.AsyncSession()) # your specific session
```

或者也可以让外部程序使用 bilibili_api 的会话，这时候调用 `get_session` 即可。

``` python
sess: curl_cffi.requests.AsyncSession = get_session()
```

注意：1、不同事件循环下会话不同，因此 `get_session` 和 `set_session` 都**仅限于当前事件循环。**2、因为第三方请求库已经可以自定义，所以 `get_session` 和 `set_session` 类型注释均使用了 `object`，属于自定义请求库的一种体现。~~此事在 changelog 中亦有记载。~~

**模块默认使用 `bilibili_api.clients.CurlCFFIClient.CurlCFFIClient`，注册时使用的名字为 `curl_cffi`。**

在 `README` 中有提到，如果没有安装 curl_cffi 库，但安装了 aiohttp 或 httpx 的话，模块大多也能正常使用，只是部分接口会受限。此处是这么实现的：以 `httpx`, `aiohttp`, `curl_cffi` 的顺序逐个尝试，如果能正常导入第三方请求库，就会注册相应的 `client`，并切换至相应 `client`。因此选择 `client` 的优先级便是 `curl_cffi` -> `aiohttp` -> `httpx`。

## 4、`aiohttp` 实战

现在让我们写一个自己写一个十分简单的 `AioHTTPClient`。

> 此处演示并不代表最佳实现，也可能存在问题，仅作举例参考，实际项目中请自己动手丰衣足食。

首先是初始化和设置，初始化不用说，`proxy` 和 `timeout` 设置可以每次请求都采用最新设置值来进行，因此我们在 `__init__` 中就先保存下来，在 `set_proxy` 和 `set_timeout` 函数中更新保存的值就可以了，`verify_ssl` 和 `trust_env` 就得考虑将原来的 `ClientSession` 替换了，因为 `set_xxx` 均为同步函数，所以更换 `ClientSession` 此处直接放在了 `request` 这个异步函数中。

``` python
class AioHTTPClient(BiliAPIClient):
    def __init__(
        self,
        proxy="",
        timeout=0,
        verify_ssl=True,
        trust_env=True,
        session: aiohttp.ClientSession = None,
    ):
        self.__args = {
            "proxy": proxy,
            "timeout": timeout,
            "verify_ssl": verify_ssl,
            "trust_env": trust_env,
        }
        self.__use_args = True
        self.__need_update_session = False
        if session:
            self.__use_args = False
            self.__session = session
        else:
            self.__session = aiohttp.ClientSession(
                trust_env=self.__args["trust_env"],
                connector=aiohttp.TCPConnector(verify_ssl=self.__args["verify_ssl"]),
            )
        self.__wss = {}
        self.__ws_cnt = 0

    def get_wrapped_session(self):
        return self.__session

    def set_proxy(self, proxy=""):
        self.__use_args = True
        self.__args["proxy"] = proxy

    def set_timeout(self, timeout=0):
        self.__use_args = True
        self.__args["timeout"] = timeout

    def set_verify_ssl(self, verify_ssl=True):
        self.__use_args = True
        self.__args["verify_ssl"] = verify_ssl
        self.__need_update_session = True

    def set_trust_env(self, trust_env=True):
        self.__use_args = True
        self.__args["trust_env"] = trust_env
        self.__need_update_session = True
    
    async def close(self):
        await self.__session.close()
```

上面的类中有一个属性：`__use_args`，因为当用户自己传入 `ClientSession` 时便不需要自己新建一个进行请求，而当请求前有调用 `request_settings` 的模块设置后又会变成需要 `client` 自行创建 `ClientSession` 请求，所以使用这个属性对是否需要用模块中的设置请求，还是用用户提供的 `ClientSession` 请求进行维护。接下来便是 `request` 函数。

``` python
class AioHTTPClient(BiliAPIClient):
    ...
    async def request(
        self,
        method: str = "",
        url: str = "",
        params: dict = {},
        data: Union[dict, str, bytes] = {},
        files: Dict[str, BiliAPIFile] = {},
        headers: dict = {},
        cookies: dict = {},
        allow_redirects: bool = False,
    ) -> BiliAPIResponse:
        if self.__need_update_session:
            await self.__session.close()
            self.__session = aiohttp.ClientSession(
                trust_env=self.__args["trust_env"],
                connector=aiohttp.TCPConnector(verify_ssl=self.__args["verify_ssl"]),
            )
            self.__need_update_session = False
        if files:
            form = aiohttp.FormData()
            if isinstance(data, str):
                raise NotImplementedError  # 无需实现
            for key, value in data.items():
                form.add_field(name=key, value=value)
            for key, value in files.items():
                form.add_field(
                    name=key,
                    value=open(value.path, "rb").read(),
                    content_type=value.mime_type,
                    filename=value.path.split("/")[-1],
                )
            data = form
        if self.__use_args:
            resp = await self.__session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                cookies=cookies,
                allow_redirects=allow_redirects,
                # 这是模块设置
                proxy=self.__args["proxy"],
                timeout=aiohttp.ClientTimeout(self.__args["timeout"]),
            )
        else:
            resp = await self.__session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                cookies=cookies,
                allow_redirects=allow_redirects,
                # 不需要管模块设置
            )
        resp_code = resp.status
        resp_headers = {}
        for key, item in resp.headers.items():
            resp_headers[key] = item
        resp_cookies = {}
        for key, item in resp.cookies.items():
            resp_cookies[key] = item.value
        return BiliAPIResponse(
            code=resp_code,
            headers=resp_headers,
            cookies=resp_cookies,
            raw=await resp.read(),
            url=str(resp.url),
        )
```

此处还好，注意 `files` 需要通过 `FormData` 与 `data` 合并。

最后则是 WebSocket 部分。因为模块规定的 api 基本是 aiohttp WebSocket api 的一部分改编，因此实现起来很容易。

``` python
class AioHTTPClient(BiliAPIClient):
    ...
    async def ws_create(self, url="", params=..., headers=...):
        # 这里也可能碰上更改设置，需要顺便更换一下 session
        if self.__need_update_session:
            await self.__session.close()
            self.__session = aiohttp.ClientSession(
                trust_env=self.__args["trust_env"],
                connector=aiohttp.TCPConnector(verify_ssl=self.__args["verify_ssl"]),
            )
            self.__need_update_session = False
        self.__ws_cnt += 1
        self.__wss[self.__ws_cnt] = await self.__session.ws_connect(
            url=url, params=params, headers=headers
        )
        return self.__ws_cnt

    async def ws_recv(self, cnt):
       msg = await self.__wss[cnt].receive()
       return msg.data, BiliWsMsgType(msg.type.value)

    async def ws_send(self, cnt, data):
        return await self.__wss[cnt].send_bytes(data)

    async def ws_close(self, cnt):
        return await self.__wss[cnt].close()
```

于是，`AioHTTPClient` 就大功告成了。经过测试可以正常处理 http 请求（GET，文件上传）和 WebSocket 连接（直播弹幕）。

## 5、注意事项

目前 bilibili 有许多接口需要通过浏览器指纹才能访问，这种指纹目前阶段仅基于 `curl-impersonate` 的请求库可以伪造，故目前其他流行的请求库，诸如 `aiohttp`, `httpx`，面对部分接口就是无法访问的状态。其中就有获取 `buvid` 的接口。模块在进行网络请求时，如果提供的 `Credential` 没有 `buvid3` 字段，则会从接口中获取、利用接口自行激活，打开请求日志就能看到这一过程。所以如果你**并未使用基于 `curl-impersonate` 的请求库**，也**不携带存在 `buvid3` 字段的 `Credential`**，那么**无论调用什么函数都无法返回结果**，因为模块在获取 `buvid` 阶段就会出现“网络问题”。解决也很简单：浏览器打开 bilibili，复制 cookies 中的 `buvid3` 字段，传入 `Credential`，传入模块的函数/类，即可。

当然并不是说启用了浏览器指纹限制的接口只有获取 `buvid` 的接口一个，其他接口**如果遇到无法获得结果/被风控问题，请先切换回 `curl_cffi` 再次尝试，如果仍有问题再提出 `issues`**。

## 附录、抽象类完整代码

``` python
@dataclass
class BiliAPIResponse:
    """
    响应对象类。
    """

    code: int
    headers: dict
    cookies: dict
    raw: bytes
    url: str

    def utf8_text(self):
        return self.raw.decode("utf-8")

    def json(self):
        return json.loads(self.utf8_text())


class BiliWsMsgType(Enum):
    """
    WebSocket 状态枚举
    """

    CONTINUATION = 0x0
    TEXT = 0x1
    BINARY = 0x2
    PING = 0x9
    PONG = 0xA
    CLOSE = 0x8
    CLOSING = 0x100
    CLOSED = 0x101


@dataclass
class BiliAPIFile:
    """
    上传文件类。
    """

    path: str
    mime_type: str


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
        allow_redirects: bool = False,
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
            allow_redirects (bool, optional): 是否允许重定向. Defaults to False.

        Returns:
            BiliAPIResponse: 响应对象

        Note: 无需实现 data 为 str 且 files 不为空的情况。
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
