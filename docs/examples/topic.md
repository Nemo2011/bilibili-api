# 示例：获取话题下的内容

``` python
from bilibili_api import topic, sync
t = topic.Topic(topic_id = 66573)
print(sync(t.get_cards(10)))
```
