# Module opus.py


bilibili_api.opus

图文相关


``` python
from bilibili_api import opus
```

- [class Opus()](#class-Opus)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_info()](#async-def-get\_info)
  - [def get\_opus\_id()](#def-get\_opus\_id)
  - [async def is\_article()](#async-def-is\_article)
  - [async def markdown()](#async-def-markdown)
  - [async def turn\_to\_article()](#async-def-turn\_to\_article)
  - [def turn\_to\_dynamic()](#def-turn\_to\_dynamic)

---

## class Opus()

图文类。


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |


### def \_\_init\_\_()





### async def get_info()

获取图文基本信息



**Returns:** dict: 调用 API 返回的结果




### def get_opus_id()

获取图文 id



**Returns:** int: 图文 idd




### async def is_article()

获取图文是否同时为专栏

如果是，则专栏/图文/动态数据共享，可以投币



**Returns:** bool: 是否同时为专栏




### async def markdown()

将图文转为 markdown



**Returns:** str: markdown 内容




### async def turn_to_article()

对专栏图文，转换为专栏（评论、点赞等数据专栏/动态/图文共享）

如图文无对应专栏将报错。



**Returns:** article.Article: 专栏类




### def turn_to_dynamic()

转为动态

图文完全包含于动态，且图文与专栏 id 数值上一致，因此此函数绝对成功。



**Returns:** dynamic.Dynamic: 对应的动态类




