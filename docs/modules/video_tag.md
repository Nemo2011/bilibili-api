# Module video_tag.py


bilibili_api.video_tag

视频标签相关，部分的标签的 id 与同名的频道的 id 一模一样。


``` python
from bilibili_api import video_tag
```

--

## class Tag()

标签类




### async def get_history_cards()

获取标签下，指定dynamic_id的视频的后一个视频/动态作为起始的视频/动态



**Returns:** dict: 调用 API 返回的结果




### async def get_similar_tags()

获取相关的标签



**Returns:** dict: 调用 API 返回的结果




### def get_tag_id()

获取标签 id



**Returns:** int: 标签 id




### async def get_tag_info()

获取标签信息。



**Returns:** dict: 调用 API 返回的结果




### async def subscribe_tag()

关注标签。



**Returns:** dict: 调用 API 返回的结果。




### async def unsubscribe_tag()

取关标签。



**Returns:** dict: 调用 API 返回的结果。




