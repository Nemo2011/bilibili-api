# 示例：保存私信收到的图片，并对文字私信做出回复

```python
from bilibili_api import Credential, sync
from bilibili_api.session import Session, Event

session = Session(Credential(...))

@session.on(Event.PICTURE)
async def pic(event: Event):
    await event.content.download()

@session.on(Event.TEXT)
async def reply(event: Event):
    if event.content == '/close':
        session.close()
    else:
        await session.reply(event, '你好李鑫')

sync(session.start())
```