## 这是一个后端请求转发接口

```python
# 需要单独安装 fastapi 和 uvicorn

import uvicorn

from bilibili_api.tools.parser import get_fastapi

if __name__ == "__main__":
    uvicorn.run(get_fastapi(), host="0.0.0.0", port=9000)
```

以上代码可以用来开启一个 `uvicorn` 后端，配合同目录下 `Card.vue` 可实现一个简单的 bilibili 主播卡片。

<div align="center">

![card](https://user-images.githubusercontent.com/41439182/216977177-5575ebcf-2596-4053-84e9-19b1d44c3f33.png)

</div>

### 起因

很久很久之前，我刚来到这个仓库，当时有个 Issue [#31](https://github.com/Nemo2011/bilibili-api/issues/31) 说：

> 这个包可以在脚手架里用吗，我在vue-cli开发模式下启动直接提示跨域

解决办法是在后端写请求，例如使用 fastapi + uvicorn 开一个后端，自己写接口。

开始我不懂啥意思，直到后来我也写了点 vue ，用到了 bilibili 的接口发现跨域，我就打算按照那个方法写后端。

但是一个个重新写接口名再找对应函数确实很累，所以我写了这个解析函数。

### 用法

```python
from bilibili_api import user, sync

async def main():
    return await user.User(uid=2).get_user_info()

print(sync(main()))
```

上述代码现在只需要一个链接就能实现。

[http://localhost:9000/user.User(2).get_user_info()](http://localhost:9000/user.User(2).get_user_info())

你也可以使用指名参数。

[http://localhost:9000/user.User(uid=2).get_user_info()](http://localhost:9000/user.User(uid=2).get_user_info())

### FAQ

> Q1. 这个有什么用呢？

前端不直接访问原接口，而是通过这个后端进行请求转发，就不会跨域了。

> Q2. 为什么要解析函数，直接用 `eval()` 不好吗？

有安全隐患，用解析函数一步一步调用比较安全。

> Q3. 参数值除了可以使用数字，还支持什么呢？

常规值支持整数、浮点数 `None` `True` `False` 以及 `"` 或 `'` 开头并结尾的字符串。

[http://localhost:9000/video.Video(bvid="BV1ju411T7so").get_aid()](http://localhost:9000/video.Video(bvid="BV1ju411T7so").get_aid())

此外，你也可以使用一个可被解析的值作为参数值，例如：

[http://localhost:9000/channel_series.ChannelSeries(id_=1845727,uid=148524702,type_=channel_series.ChannelSeriesType.SEASON).get_meta()](http://localhost:9000/channel_series.ChannelSeries(id_=1845727,uid=148524702,type_=channel_series.ChannelSeriesType.SEASON).get_meta())

### 进阶用法

使用请求参数 `query` 储存值，接着在函数中使用 `type` 作为参数值。

[http://localhost:9000/comment.get_comments(708326075350908930,type,1)?type=comment.CommentResourceType.DYNAMIC](http://localhost:9000/comment.get_comments(708326075350908930,type,1)?type=comment.CommentResourceType.DYNAMIC)

使用 `.key` 的方式对获取的字典结果取值，获得更精细数据，节省带宽。使用 `.index` 的方式对列表结果取元素，例如：

[http://localhost:9000/user.User(2).get_user_info().elec.show_info.list.0.uname](http://localhost:9000/user.User(2).get_user_info().elec.show_info.list.0.uname)

使用 `?max_age=86400` 请求参数设置缓存，这里是 `86400` 秒。
