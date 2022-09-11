# 示例：获取 IP 所在地区

``` python
from bilibili_api import client, sync

async def main():
    zone = await client.get_zone()
    print(zone)

sync(main())
```
