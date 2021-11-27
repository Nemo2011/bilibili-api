# 示例：创建视频收藏夹并收藏一个视频

```python
from bilibili_api import video, favorite_list, sync, Credential

cre = Credential('', '')

async def main():
    v = video.Video('BV1AV411x7Gs', credential=cre)
    resp = await favorite_list.create_video_favorite_list('TEST', credential=cre)
    media_id = resp['id']
    await v.set_favorite([media_id])

sync(main())
```

