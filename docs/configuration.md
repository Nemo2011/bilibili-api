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
