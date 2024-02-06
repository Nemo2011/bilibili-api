# 示例：保存私信收到的图片，并对文字私信做出回复

```python
from bilibili_api import Credential, sync
from bilibili_api.session import Session, Event, EventType
from bilibili_api.utils.picture import Picture

session = Session(Credential(...))

@session.on(EventType.PICTURE)
async def pic(event: Event):
    img: Picture = event.content
    img.download("./")

@session.on(EventType.TEXT)
async def reply(event: Event):
    if event.content == "/close":
        session.close()
    elif event.content == "来张涩图":
        img = await Picture.from_file("test.png").upload_file(session.credential)
        await session.reply(event, img)
    else:
        await session.reply(event, "你好李鑫")

sync(session.start())
```