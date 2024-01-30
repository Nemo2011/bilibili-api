# 示例：获取视频标签下的视频

```python
from bilibili_api import video_tag, sync
tag = video_tag.Tag(tag_name="空难")
print(sync(tag.get_cards()))
```

```python
# 获取从第二个视频开始的视频/动态
from bilibili_api import video_tag, sync
tag = video_tag.Tag(tag_name="空难")

cards = sync(tag.get_cards())["cards"]

first_di = cards[0]["desc"]["dynamic_id"]
second_di = cards[1]["desc"]["dynamic_id"]

# tag.get_history_cards 得到的是以指定dynamic_id的视频/动态的*后一个视频/动态*作为起始的cards
history_cards = sync(tag.get_history_cards(first_di))["cards"]

raise_for_statement(second_di == history_cards[0]["desc"]["dynamic_id"]
```
