# 示例：获取直播间弹幕和礼物

```python
from bilibili_api import live, sync

room = live.LiveDanmaku(22544798)

@room.on('DANMU_MSG')
async def on_danmaku(event):
    # 收到弹幕
    print(event)

@room.on('SEND_GIFT')
async def on_gift(event):
    # 收到礼物
    print(event)

sync(room.connect())
```


# 示例：直播间赠送金瓜子礼物

```python
from bilibili_api import live, sync, Credential

SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""

# 自己的uid
self_uid = 0
# 实例化 Credential 类
credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
room = live.LiveRoom(22544798, credential)

# 获取礼物列表
gift_config = sync(live.get_gift_config())
for gift in gift_config['list']:
    if gift['name'] == "牛哇牛哇":
        # 赠送礼物 "牛哇牛哇" 1个
        res = sync(room.send_gift_gold(uid=self_uid, gift_id=gift['id'], gift_num=1, price=gift['price']))
        print(res)
        break
else:
    print('礼物 牛哇牛哇 不存在')

```

