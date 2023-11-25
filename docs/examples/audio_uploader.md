# 示例：上传单个音频

```python
import asyncio
from bilibili_api import audio_uploader, sync
from bilibili_api.credential import Credential

c = Credential(
    sessdata="...",
    bili_jct="...",
)


async def main()
    meta = audio_uploader.SongMeta(
        title="test",
        desc="test",
        song_type=audio_uploader.SongCategories.SongType.PURE_MUSIC,
        content_type=audio_uploader.SongCategories.ContentType.MUSIC,
        cover=r"path to image",
        creation_type=audio_uploader.SongCategories.CreationType.COVER,
        tags=["2333"],
        language=audio_uploader.SongCategories.Language.CHINESE,
        style=audio_uploader.SongCategories.Style.ELECTRONIC,
        theme=audio_uploader.SongCategories.Theme.GAME,
    )
    uploader = audio_uploader.AudioUploader(
        path=r"path to audio", credential=c, meta=meta
    )
    song_id = await uploader.start()
    print(song_id)

sync(main())
```
