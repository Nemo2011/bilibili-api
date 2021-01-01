# article 模块

专栏相关。

## 通用名词解释

cv：cv号，标识专栏的唯一ID。

**如无特殊说明，下列所有方法均需要传入cv号，不再赘述。**

## 方法

### 评论相关

参见 [评论信息和操作](/docs/通用解释.md#评论信息和操作)，传入cv。

### get_info

获取专栏信息。

### set_like

专栏点赞

| 参数名 | 类型 | 必须提供 | 默认 | 释义 |
| ------ | ---- | -------- | ---- | ---- |
| status | bool | False    | True | 状态 |

### add_coins

专栏投币

| 参数名 | 类型 | 必须提供 | 默认 | 释义                         |
| ------ | ---- | -------- | ---- | ---------------------------- |
| num    | int  | False    | 1    | 投币数量，现在貌似只能是一个 |

### share_to_dynamic

分享到动态。

| 参数名  | 类型 | 必须提供 | 默认 | 释义     |
| ------- | ---- | -------- | ---- | -------- |
| content | str  | True     | -    | 动态内容 |

### get_content

自己写的专栏内容爬虫并转换成markdown，按照以下格式写就可以了。

```python
from bilibili_api import article
# 这是一篇全格式的测试文章
ar = article.get_content(cid=7099047)
# 打印出来预览
print(ar)
# 转换成markdown
ar.save_as_markdown(path="保存目录路径")
```

说的很简单，实际上转换过程麻烦的要死QAQ，感兴趣的可以去看看源代码。

