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

> `wbi` 为 B 站对用户相关 API 采取的一个反爬虫措施，需要传入一些经过加密的参数，否则请求可能会被驳回。每次计算此参数的之后，这个值有失效可能，届时模块会自动重新计算这个参数新的值，进行重试。当重试次数超过一定次数 (`settings.wbi_retry_times`) 后，模块将发出报错。

```python
request_settings.set_wbi_retry_times(10) # defaults to 3
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
