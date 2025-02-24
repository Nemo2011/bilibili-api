# 配置

```python
from bilibili_api import request_settings, request_log
```

## 代理

```python
request_settings.set_proxy("http://example.com")
```

## web 请求超时设置

```python
request_settings.set_timeout(1.0)
```

## 设置是否验证 ssl / 使用环境变量

```python
request_settings.set_verify_ssl(False)
request_settings.set_trust_env(True)
```

## 打印请求日志

```python
request_log.set_on(True)
```

request_log 本质为 `AsyncEvent`，即发布-订阅模式异步事件类，日志输出先经过 `AsyncEvent` ，再会到 `logging.Logger`，因此模块支持对不同事件类型的过滤。

``` python
request_log.set_on_events(["REQUEST"]) # 仅当有 http 请求时打印日志
request_log.set_ignore_events(["API_REQUEST", "API_RESPONSE"]) # 去除 Api 类相关的信息
```

request_log 默认只打印以下类型信息：

- API_REQUEST
- API_RESPONSE
- ANTI_SPIDER
- WS_CONNECT
- WS_RECV
- WS_SEND
- WS_CLOSE

## 设置 `wbi` 请求重试次数上限

> `wbi` 为 B 站对用户相关 API 采取的一个反爬虫措施，需要传入一些经过加密的参数，否则请求可能会被驳回。每次计算此参数的之后，这个值有失效可能，届时模块会 **自动重新计算** 这个参数新的值，进行重试。当重试次数超过一定次数 (`settings.wbi_retry_times`) 后，模块将发出报错。

> 手动重新计算可用 `recalculate_wbi` 

```python
request_settings.set_wbi_retry_times(10) # defaults to 3

from bilibili_api import recalculate_wbi
recalculate_wbi() # 重新计算 wbi 参数
```

## 设置 `buvid` 自动生成

> `buvid` 是访问 B 站时可能需要提供的 cookie 系列，分为 `buvid3` 和 `buvid4` 字段。如果不提供部分接口可能受限。模块在用户未提供 credential 或 credential 中无 `buvid3` 或 `buvid4` 字段时，会自动生成一组 `buvid`，但过程中需要进行网络请求，此功能可通过这项设置关闭。

> 自动生成的 `buvid` 若有必要，**需要用户手动刷新**，使用 `refresh_buvid`

```python
request_settings.set_enable_auto_buvid(False)

from bilibili_api import refresh_buvid
refresh_buvid() # 刷新 buvid
```

## 设置 `bili_ticket` 自动生成

> `bili_ticket` 是访问 B 站时可能需要提供的 cookie 系列，分为 `bili_ticket` 和 `bili_ticket_expires` 字段。提供 `bili_ticket` 有时可以达到一些玄学效果。默认不启用，可以通过此项设置启用。

> `bili_ticket` 过期后模块会 **自动重新计算**。手动重新计算可用 `refresh_bili_ticket`

```python
request_settings.set_enable_bili_ticket(True)

from bilibili_api import refresh_bili_ticket
refresh_bili_ticket() # 刷新 bili_ticket
```

## 额外设置

针对不同的第三方请求库，模块会有各不相同的额外设置。相关信息见 [模块请求库相关](https://nemo2011.github.io/bilibili-api/#/request_client)。

为了对这些字段进行处理，`request_settings` 提供 `set` 函数。

``` python
request_settings.set("impersonate", "edge99") # 设置名为 impersonate 的设置为 edge99
```

`set` 函数同样支持上面出现过的 `proxy` `timeout`。

``` python
# 等价
request_settings.set_proxy("http://example.com")
request_settings.set("proxy", "http://example.com")
```

## 获取设置

``` python
# 获取 proxy
proxy = request_settings.get_proxy()
proxy = request_settings.get("proxy")
proxy = request_settings.get_all()["proxy"]
# 获取所有设置
all_settings = request_settings.get_all()
```
