# 配置

```python
from bilibili_api import settings
```

## 代理

```python
settings.proxy = "" # 此处填写你的代理地址
```

## web 请求超时设置

```python
settings.timeout = 1.0
```

## 极验验证页面自动弹出

>验证码登录、密码登录需要完成极验验证，页面默认会自动弹出，但是可以通过设置关闭

```python
settings.geetest_auto_open = False
```

## 设置 **`http`** 请求客户端

```python
# 使用 aiohttp.ClientSession()
settings.http_client = settings.HTTPClient.AIOHTTP # default
# 使用 httpx.AsyncClient()
settings.http_client = settings.HTTPClient.HTTPX
```

## 打印 `Api` 类请求日志

```python
settings.request_log = True
```

## 设置 `wbi` 请求重试次数上限

> `wbi` 为 B 站对用户相关 API 采取的一个反爬虫措施，需要传入一些经过加密的参数，否则请求可能会被驳回。每次计算此参数的之后，这个值有失效可能，届时模块会自动重新计算这个参数新的值，进行重试。当重试次数超过一定次数 (`settings.wbi_retry_times`) 后，模块将发出报错。

```python
settings.wbi_retry_times = 10 # defaults to 3
```
