# 示例：下载相簿所有图片

``` python
from bilibili_api import album
import asyncio

async def main() -> None:
    # 初始化相簿类
    al = album.Album(123348276)
    # 获取图片
    pictures = await al.get_pictures()
    # 下载所有图片
    cnt = 0
    for pic in pictures:
        await pic.download(f"{cnt}.png")
        cnt += 1

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```
