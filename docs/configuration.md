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

## 设置 `wbi` 请求重试次数上限

> `wbi` 为 B 站对用户相关 API 采取的一个反爬虫措施，需要传入一些经过加密的参数，否则请求可能会被驳回。每次计算此参数的之后，这个值有失效可能，届时模块会自动重新计算这个参数新的值，进行重试。当重试次数超过一定次数 (`settings.wbi_retry_times`) 后，模块将发出报错。

```python
request_settings.set_wbi_retry_times(10) # defaults to 3
```
