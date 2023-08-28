** 注意，此类操作务必传入 `Credential` 并且要求传入 `buvid3` 否则可能无法鉴权 **

# 示例：操作放映室

``` python
import asyncio
from bilibili_api import credential, watchroom
from bilibili_api.watchroom import Message, MessageSegment

c = credential.Credential(sessdata=""
                          , bili_jct=""
                          , buvid3="")

async def main():
    room = await watchroom.create(113, 1678, False, c)
    await room.join()
    print(await room.get_info())
    await room.share()
    await room.send(Message("欢迎！") + MessageSegment("这里是测试放映室。"))

if __name__ == "__main__":
    asyncio.run(main())

```
