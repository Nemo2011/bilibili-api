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

# 示例：简易录播

```python
from bilibili_api import live, sync
import aiohttp


async def main():
    # 初始化
    room = live.LiveRoom(3)
    # 获取直播流链接
    stream_info = await room.get_room_play_url()
    url = stream_info['durl'][0]['url']

    async with aiohttp.ClientSession() as sess:
        # 设置 UA 和 Referer 头以绕过验证
        async with sess.get(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com/"}) as resp:
            # 以二进制追加方式打开文件以存储直播流
            with open('live.flv', 'ab') as f:
                for chunk in resp.iter_bytes(1024):
                    if not chunk:
                        # 无更多数据，退出循环
                        print('无更多数据')
                        break
                    print(f'接收到数据 {len(chunk)}B')
                    # 写入数据
                    f.write(chunk)

sync(main())
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

