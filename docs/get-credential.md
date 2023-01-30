# 获取 Credential 类所需信息

Credential 类实例化代码如下：

```python
from bilibili_api import Credential

credential = Credential(sessdata="你的 SESSDATA", bili_jct="你的 bili_jct", buvid3="你的 buvid3", dedeuserid="你的 DedeUserID")
```

`sessdata` `bili_jct` `buvid3` 和 `dedeuserid` 这四个参数的值均在浏览器的 Cookies 里头，下面说明获取方法。

## 火狐浏览器（Firefox）

1. 按 **F12** 打开开发者工具。

![](https://pic.imgdb.cn/item/6038d30b5f4313ce2533b6d1.jpg)

2. 在工具窗口上方找到 **存储** 选项卡。

![](https://pic.imgdb.cn/item/6038d31d5f4313ce2533c1bd.jpg)

3. 展开左边的 **Cookie** 列表，选中任一b站域名。在右侧找到对应三项即可。

![](https://pic.imgdb.cn/item/6038d3df5f4313ce25344c6a.jpg)

## 谷歌浏览器（Chrome）

1. 按 **F12** 打开开发者工具。

![](https://pic.imgdb.cn/item/6038d4065f4313ce25346335.jpg)

2. 在工具窗口上方找到 **Application** 选项卡。

![](https://pic.imgdb.cn/item/6038d4425f4313ce253484e4.jpg)

3. 在左侧找到 **Storage/Cookies**，并选中任一b站域名，在右侧找到对应三项即可。

![](https://pic.imgdb.cn/item/6038d4ce5f4313ce2534ecb3.jpg)

## 微软 Edge

1. 按 **F12** 打开开发者工具。

![](https://pic.imgdb.cn/item/6038d5125f4313ce25353318.jpg)

2. 在工具窗口上方找到 **应用程序** 选项卡 。

![](https://pic.imgdb.cn/item/6038d5395f4313ce25354c15.jpg)

3. 在左侧找到 **存储/Cookies**，并选中任一b站域名，在右侧找到对应三项即可。

![](https://pic.imgdb.cn/item/6038d5755f4313ce253571bb.jpg)
