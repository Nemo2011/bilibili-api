# 短链接支持

bilibili_api 从 10.0 开始支持短链接了（说白了就是支持查看短链目标了）

``` python
from bilibili_api import get_real_url, sync
print(sync(get_real_url("https://b23.tv/mx00St"))) # https://www.bilibili.com/video/BV1YQ4y127Rd?p=1&share_medium=android&share_plat=android&share_session_id=d6c56bd5-db84-4cc8-9bb7-8f91cd8edfe0&share_source=COPY&share_tag=s_i&timestamp=1629155789&unique_k=mx00St
```
