# 短链接支持

bilibili_api 从 10.0.0 开始支持短链接了（说白了就是支持查看短链目标了）

获取默认链接(长链接)的短链接
``` python
from bilibili_api import get_short_url, sync
print(sync(get_short_url(real_url="https://www.bilibili.com/video/BV18X4y1N7Yh/")))  # optionally pass in Credential
```

获取短链接的对应默认链接(长链接)
``` python
from bilibili_api import get_real_url, sync
print(sync(get_real_url(short_url="https://b23.tv/mx00St"))) # https://www.bilibili.com/video/BV1YQ4y127Rd?p=1&share_medium=android&share_plat=android&share_session_id=d6c56bd5-db84-4cc8-9bb7-8f91cd8edfe0&share_source=COPY&share_tag=s_i&timestamp=1629155789&unique_k=mx00St
```
