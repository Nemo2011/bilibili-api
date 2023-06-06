# 示例：刷新 Credential

通过 `credential.refresh()` 方法刷新 Credential。

必须要有 `ac_time_value` 字段，否则无法刷新。

获取方法见 [获取 Credential 类所需信息](get-credential.md)。

```python
from bilibili_api import Credential

# 生成一个 Credential 对象
credential = Credential(sessdata="xxx", bili_jct="xxx", ac_time_value="xxx")

# 检查 Credential 是否需要刷新
print(credential.check_refresh())

# 刷新 Credential
credential.refresh()
```

不需要过于频繁地刷新。

如果需要长期使用此凭据则不应该在浏览器登录账户导致 Cookies 被刷新。