# Module opus.py


bilibili_api.opus

图文相关


``` python
from bilibili_api import opus
```

---

## class Opus()

图文类。


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |


### def __init__()





### async def get_info()

获取图文基本信息



**Returns:** dict: 调用 API 返回的结果




### def get_opus_id()

获取图文 id



**Returns:** int: 图文 idd




### def get_type()

获取图文类型(专栏/动态)



**Returns:** OpusType: 图文类型




### def is_note()

是否为笔记



**Returns:** None



### def markdown()

将图文转为 markdown



**Returns:** str: markdown 内容




### def turn_to_article()

对专栏图文，转换为专栏



**Returns:** None



### def turn_to_dynamic()

转为动态



**Returns:** None



### def turn_to_note()

转为笔记



**Returns:** None



---

## class OpusType()

**Extend: enum.Enum**

图文类型

+ ARTICLE: 专栏
+ DYNAMIC: 动态




