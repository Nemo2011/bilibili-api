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
room = live.LiveRoom(22544798, credential=credential)

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


# 示例：直播间礼物统计

参考：<https://github.com/Nemo2011/bilibili-api/issues/43>

``` python

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bilibili_api import live, sync


class Gift(TypedDict):
    '''用户赠送礼物列表
    username: 用户名
    last_gift_time: 最后一次赠送礼物时时间戳
    gift_list: 赠送的礼物字典，格式 礼物名: 数量'''
    username: str
    last_gift_time: int
    gift_list: Dict[str, int]

user_list: Dict[int, Gift] = dict()
room = live.LiveDanmaku(21452505)
sched = AsyncIOScheduler(timezone="Asia/Shanghai")  # 定时任务框架

@room.on('SEND_GIFT')
async def on_gift(event):
    '记录礼物'
    info = event['data']['data']
    uid = info['uid']
    user = user_list.get(uid)
    if user:
        # 如果用户列表中有该用户 则更新他的礼物字典以及礼物时间戳
        num = user['gift_list'].get(info['giftName'], 0)
        user['gift_list'][info['giftName']] = num + info['num']
        user['last_gift_time'] = int(time.time())
    else:
        # 不存在则以现在时间及礼物新建 Gift 对象
        user_list[uid] = Gift(
            username=info['uname'],
            last_gift_time=int(time.time()),
            gift_list={info['giftName']: info['num']}
        )
        # 开启一个监控
        sched.add_job(check, 'interval', seconds=1, args=[uid], id=str(uid))

async def check(uid: int):
    '判断是否超过阈值并输出'
    user = user_list.get(uid)
    if user:
        if int(time.time()) - user.get('last_gift_time', 0) > 5:  # 此处的 5 即需求中的 n 表示秒数
            sched.remove_job(str(uid))  # 移除该监控任务
            print(user_list.pop(uid))  # 将该用户从列表中弹出并打印

if __name__ == '__main__':
    sched.start()  # 启动定时任务
    sync(room.connect())  # 连接直播间
```

# 示例：直播间自动回复弹幕

```python
from bilibili_api import Credential, Danmaku, sync
from bilibili_api.live import LiveDanmaku, LiveRoom

# 自己直播间号
ROOMID = 123
# 凭证 根据回复弹幕的账号填写
credential = Credential(
    sessdata="",
    bili_jct=""
)
# 监听直播间弹幕
monitor = LiveDanmaku(ROOMID, credential=credential)
# 用来发送弹幕
sender = LiveRoom(ROOMID, credential=credential)
# 自己的UID 可以手动填写也可以根据直播间号获取
UID = sync(sender.get_room_info())["room_info"]["uid"]


@monitor.on("DANMU_MSG")
async def recv(event):
    # 发送者UID
    uid = event["data"]["info"][2][0]
    # 排除自己发送的弹幕
    if uid == UID:
        return
    # 弹幕文本
    msg = event["data"]["info"][1]
    if msg == "你好":
        # 发送弹幕
        await sender.send_danmaku(Danmaku("你好！"))


# 启动监听
sync(monitor.connect())
```

参考：[自动回复直播间弹幕](https://github.com/Nemo2011/bilibili-api/issues/240#issuecomment-1475619484)
