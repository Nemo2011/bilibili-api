# 模块请求库相关

此部分主要是函数 / 用法介绍，将部分用途较多的函数拎出来提一提。这些函数的相关信息文档中均可找到。

[TOC]

## 1、默认支持的第三方请求库

### 1、总表

|           | 优先级 | request | stream | WebSocket | 额外网络请求设置                                                           |
| --------- | ------ | ------- | ------ | --------- | -------------------------------------------------------------------------- |
| curl_cffi | 3      | ✅      | ✅     | ✅        | - `impersonate` defaults to ` ` <br> - `http2` defaults to `False` |
| aiohttp   | 2      | ✅      | ✅     | ✅        |                                                                            |
| httpx     | 1      | ✅      | ✅     | ❌        | `http2` defaults to `False`                                                |

名为 `impersonate` 的设置决定了 curl_cffi 模仿哪个浏览器的指纹，名为 `http2` 的设置决定了 curl_cffi / httpx 是否启用 HTTP2。[这些设置如何启用？](https://nemo2011.github.io/bilibili-api/#/configuration)

### 2、切换请求库

```python
select_client("curl_cffi") # 选择 curl_cffi
select_client("aiohttp") # 选择 aiohttp
select_client("httpx") # 选择 httpx，不支持 WebSocket

print(get_selected_client()) # httpx
```

### 3、把模块的会话拿出来用

```python
select_client("httpx") # 使用 httpx
sess: httpx.AsyncClient = get_session() # 此函数获取的会话仅限于当前事件循环
```

### 4、把自己的会话传给模块

```python
sess: httpx.AsyncClient = httpx.AsyncClient(
    .........
    .........
    .........
)
set_session(sess) # 同样仅限于当前事件循环
```

## 2、模块使用第三方库底层逻辑简析

bilibili_api 支持不同网络请求库的功能基于一个抽象类：`BiliAPIClient`。通过对这个抽象类的改写，可以实现**统一接口样式**的、**基于不同第三方请求库**的不同类，例如模块自带的 `bilibili_api.clients.AioHTTPClient.AioHTTPClient`, `bilibili_api.clients.CurlCFFIClient.CurlCFFIClient`, `bilibili_api.clients.HTTPXClient.HTTPXClient`，这些类会像第三方请求库的会话一样工作，但是它们是**统一接口样式**的。换种说法，这是对第三方请求库的会话对象**进行封装**。

现规定 `session` 表示 **第三方请求库（诸如 `curl_cffi`, `aiohttp`）在模块每次运行中使用可持久化的会话对象**，`client` 表示继承 `BiliAPIClient` 的类。

### 1、模块如何发起请求

我们以 `user.User().get_user_info()` 为例。此处选择的 `User` 实例为站长（`uid=1`）。我们大致简化这个过程，以解释 bilibili_api 发起请求的全过程。

首先，一般地，调用的所有函数会创建一个类的实例，`Api`，可以把它当作请求的载体。这个例子中 `Api` 对象长这样：

- `method`: GET
- `url`: <https://api.bilibili.com/x/space/wbi/acc/info>
- `params`:
  - `mid`: 2
- `wbi`: true
- `wbi2`: true

这里有两个字段，`wbi` 和 `wbi2`，正常网络请求里面没有。其实这是 bilibili 的一种风控方式，通过在请求中使用一整套名为 `wbi` 的加密方法达到反爬虫的目的。这套加密方法是通用的，所以无需在每一个需要使用 `wbi` 的函数中执行一遍，这些工作被安排到了 `Api` 类中。

接下来让我们看 `Api` 类发起请求的几行代码：

```python
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

这就是正常情况下，为了访问这个接口，需要往 `httpx.get`, `aiohttp.get`, `curl_cffi.requests.get` 等第三方库中传入的参数。在浏览器控制台抓取到的真实请求也应该长这样子。

第二行，调用 `get_client`，这个函数会返回一个 `client` 实例。接着在第三行调用这个 `client` 的函数，`client` 会将参数传递到 `session`。

这个例子中，`config` 直接传入 `session` 也是可行的，因为字段够简单，但是不妨多考虑一下，我们现在还需要获得 `session` 的响应文本。`httpx` 只需要 `resp.text`，而 `aiohttp` 需要 `await resp.text()`，此处已经不能统一处理了。

我们再假设，现在需要上传一个文件（`multipart/form-data`），request-like api 中文件会放入 `files` 参数，而 aiohttp api 中文件需要使用 `FormData` 和其他字段结合后传入 `data`。这里该如何统一处理？

这就是 `client` 的作用：作为中间层，**它为模块提供了固定的 api，从而做到只要更换 `client` 就能更换请求库，而不是更换代码**。例如在响应上，它用 `BiliAPIResponse` 统一了各个第三方请求库，在上传文件传参上，它用 `BiliAPIFile` 统一了各个第三方请求库。

### 2、模块如何处理 `client` 类

前面提到模块底层基于 `client` 类，那么是如何用到这个类的？

首先需要把 `client` 的类注册到模块中，以供模块使用。后文将详细描述。

然后是有了这个类之后具体调用方式，首先创建实例，此过程在 `get_client` 中进行。创建实例是有说法的，模块默认有一套设置，它们会在创建实例的过程中给到每一个 `client`，然后 `client` 会将这些设置应用到第三方请求库会话上。也有种情况用户自己要提供会话，即 `set_session`，这时候 `client` 初始化只接受用户提供的会话，模块设置应当被忽略。创建完实例后即可调用。

### 3、如何使用 `client`

前文提到，模块通过 `client` 统一后的接口发送网络请求。事实上，通过 `get_client` 函数就能获取到模块正在使用的 `BiliAPIClient`。因为 `BiliAPIClient` 接口统一，故直接使用 `BiliAPIClient` 相关函数即使更换第三方请求库结果上也不会有影响（理论）。

例如下载文件的功能，在模块提供的示例中有出现，就是基于 `BiliAPIClient` 相关函数实现的。

```python
async def download(url: str, out: str, intro: str):
    dwn_id = await get_client().download_create(url, HEADERS) # 创建下载任务（本质上是建立起连接）
    bts = 0
    tot = get_client().download_content_length(dwn_id) # 获取文件长度
    with open(out, "wb") as file:
        while True:
            bts += file.write(await get_client().download_chunk(dwn_id)) # 每次下载部分
            print(f"{intro} - {out} [{bts} / {tot}]", end="\r")
            if bts == tot:
                break
    print()
# 此函数在 aiohttp / httpx / curl_cffi 下都能正常运行。
```

接下来对 `BiliAPIClient` 内部函数进行介绍。

#### \_\_init\_\_

提供两种传参方式：1、传入所有的设置，字段名称为设置的名字，提供默认值。2、传入一个第三方请求库的会话对象。

```python
def __init__(
    self,
    proxy: str = "",
    timeout: float = 0.0,
    verify_ssl: bool = True,
    trust_env: bool = True,
    session: Optional[object] = None,
) -> None: ...
```

#### set_xxx

当模块设置被修改时会执行的函数

```python
def set_timeout(self, timeout: float = 0.0) -> None: ...
def set_proxy(self, proxy: str = "") -> None: ...
def set_verify_ssl(self, verify_ssl: bool = True) -> None: ...
def set_trust_env(self, trust_env: bool = True) -> None: ...
```

#### get_wrapped_session

获取 `client` 中被包装的 `session`

```python
def get_wrapped_session(self) -> object: ...
```

> `get_session() = get_client().get_wrapped_session()`

#### request

非常正常的 request。

```python
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
) -> BiliAPIResponse: ...
```

`BiliAPIResponse` 和 `BiliAPIFile` 相关可在文档中查阅。

#### WebSocket

WebSocket 为持续连接，然而 `BiliAPIClient` 未提供上下文 api。在创建了 WebSocket 连接后，函数会返回一个整数，表示连接编号，这个连接会以编号的形式保留着。之后相关操作需要传入编号进行。

```python
async def ws_create(
    self, url: str = "", params: dict = {}, headers: dict = {}
) -> int: ...
async def ws_send(self, cnt: int, data: bytes) -> None: ...
async def ws_recv(self, cnt: int) -> Tuple[bytes, BiliWsMsgType]: ...
async def ws_close(self, cnt: int) -> None: ...
```

#### 下载

此处下载为流式下载，设计上和 WebSocket 类似（返回编号表示连接，其他函数传入编号）。

```python
async def download_create(
    self,
    url: str = "",
    headers: dict = {},
) -> int: ...
async def download_chunk(self, cnt: int) -> bytes: ...
def download_content_length(self, cnt: int) -> int: ...
```

## 3、将其他第三方请求库与模块进行适配

### 1、基础

整体思路是新建一个类，继承 `BiliAPIClient`，然后对前文提到的函数进行实现。

此处实现可以参考模块自带的 `client`。见 <https://github.com/nemo2011/bilibili-api/tree/main/bilibili_api/clients>

> 函数中可以调用 `request_log.dispatch` 函数实现日志功能。

### 2、进阶

有时会在自己编写的 `client` 类中添加设置，例如 `curl_cffi` 的 `impersonate` 参数便应当为设置项。如何实现这个功能？

以此处的 `impersonate` 参数为例子，先在 `__init__` 中加上 `xxx` 参数（在 `__init__` 中加上 `impersonate` 参数），然后在 `client` 类中实现 `set_xxx` (在 `CurlCFFIClient` 中实现 `set_impersonate`) 即可。

### 3、注册

前文提到 `client` 使用前需要注册，模块默认携带的 `AioHTTPClient` `CurlCFFIClient` `HTTPXClient` 也有注册的过程。

注册的函数为 `register_client`，第一项参数传入你喜欢的 `client` 的名字，第二项参数传入 `client` 的类，第三项参数需要传入 `client` 中额外使用到的设置项。以 `impersonate` 为例子，首先需要一个字典，然后将字典的 `impersonate` 项设置为你喜欢的 `impersonate` 设置项的默认值，最后将这个字典传入。

```python
class CurlCFFIClient(BiliAPIClient):
    ...

register_client("curl_cffi", CurlCFFIClient, {"impersonate": "chrome131"})
```

注册后会自动切换到注册的 `client`。然后便能使用 `client`。

同时，注册也可以取消。

```python
unregister_client("curl_cffi")
```
