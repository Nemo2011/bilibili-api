# 获取 Credential 类所需信息

Credential 类实例化代码如下：

```python
from bilibili_api import Credential

credential = Credential(sessdata="你的 SESSDATA", bili_jct="你的 bili_jct", buvid3="你的 buvid3", dedeuserid="你的 DedeUserID", ac_time_value="你的 ac_time_value")
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

---

`ac_time_value` 相对特殊，仅用于刷新 Cookies，可以选择不获取，在 localStorage 中的ac_time_value 字段。

只需要打开 B 站，打开开发者工具，进入控制台，输入`window.localStorage.ac_time_value`即可获取值。

# Cookies 值简介

常见的凭据 (`Credential`) 信息有 Cookie 值

+ `SESSDATA`
+ `bili_jct`
+ `buvid3` / `buvid4`
+ `dedeuserid`

以及 Local Storage 中的

+ `ac_time_value`

下列一一介绍

## `SESSDATA`

`SESSDATA` 用于一般在获取对应用户信息时提供，通常是 `GET` 操作下提供，此类操作一般不会进行操作，仅读取信息

如获取个人简介、获取个人空间信息等情况下需要提供

## `bili_jct`

`bili_jct` 用于进行操作用户数据时提供，通常是 `POST` 操作下提供，此类操作会修改用户数据

如发送评论、点赞三连、上传视频等等情况下需要提供

## `buvid3` / `buvid4`

`buvid3` / `buvid4` 是 [设备验证码](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/device_identity.md#%E8%AE%BE%E5%A4%87%E5%94%AF%E4%B8%80%E6%A0%87%E8%AF%86-buvid)
  
通常不需要提供，但如放映室内部分接口需要提供，同时与风控有关

## `dedeuserid`

`dedeuserid` 通常为用户 `UID` ，几乎不需要提供

## `ac_time_value`

`ac_time_value` 在登录时获取，登录状态过期后用于刷新 `Cookies`，没有此值则只能重新登录，如不需要凭据刷新则不需要提供