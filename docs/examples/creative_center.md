# 示例：获取投稿视频数据

``` python
from bilibili_api import creative_center, Credential, sync


async def main():
    print(await creative_center.get_video_playanalysis(credential=Credential(
        sessdata="",
        bili_jct=""
    )))


sync(main())
```
