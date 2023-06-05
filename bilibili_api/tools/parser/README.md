### 这是一个解析器

```python
# 需要单独安装 fastapi 和 uvicorn

from bilibili_api.tools.parser import get_fastapi

import uvicorn

if __name__ == "__main__":
    uvicorn.run(get_fastapi(), host="0.0.0.0", port=9000)
```

以上代码可以用来开启一个 `uvicorn` 后端，配合同目录下 `Card.vue` 可实现一个简单的 bilibili 主播卡片。

<div align="center">

![card](https://user-images.githubusercontent.com/41439182/216977177-5575ebcf-2596-4053-84e9-19b1d44c3f33.png)

</div>

---

### 起因

很久很久之前，我刚来到这个仓库，当时有个 Issue #31 他说：

> 这个包可以在脚手架里用吗，我在vue-cli开发模式下启动直接提示跨域

解决办法是在后端写请求，例如使用 fastapi + uvicorn 开一个后端，自己写接口。

开始我不懂啥意思，直到后来我也写了点 vue ，用到了 bilibili 的接口发现跨域，我就打算按照那个方法写后端。

但是一个个重新写接口名再找对应函数确实很累，所以我写了这个解析器

---

### 用法

这段代码我已经部署在阿里云的函数计算里了，域名：[https://aliyun.nana7mi.link](https://aliyun.nana7mi.link)

```python
from bilibili_api import user, sync

async def main():
    return await user.User(uid=2).get_user_info()

print(sync(main()))
```

上述代码现在只需要一个链接：[https://aliyun.nana7mi.link/user.User(2).get_user_info()](https://aliyun.nana7mi.link/user.User(2).get_user_info()) 就能实现。

属于是从接口来回接口去了。

类似的还有 [https://aliyun.nana7mi.link/live.LiveRoom(21452505).get_room_info()](https://aliyun.nana7mi.link/live.LiveRoom(21452505).get_room_info())

---

### FAQ

> Q1. 这个有什么用呢？

前端访问不跨域了。

> Q2. 为什么要解析器，直接用 eval() 不好吗？

有安全隐患，用解析器这样一步一步调用比较安全。

---

### 进阶用法

使用网址 params 请求参数储存值。

[https://aliyun.nana7mi.link/comment.get_comments(708326075350908930,type,1:int)?type=comment.CommentResourceType.DYNAMIC](https://aliyun.nana7mi.link/comment.get_comments(708326075350908930,type,1:int)?type=comment.CommentResourceType.DYNAMIC)

这个变量是另一个需要被解析的文本，为什么不直接放在网址里呢？因为放前面会被当做字符串传进去。

同时为了不让所有参数都以字符串传入，还加了类型标注，在变量后使用类似 `:int` 的方式来强制转换，目前支持 `:int` `:float` `:bool` `:parse`。

其中 `:parse` 较为特殊，它的作用是解析前面这个字符串，用前面这个网址举例

[https://aliyun.nana7mi.link/comment.get_comments(708326075350908930,comment.CommentResourceType.DYNAMIC:parse,1:int)](https://aliyun.nana7mi.link/comment.get_comments(708326075350908930,comment.CommentResourceType.DYNAMIC:parse,1:int))

---

### 再高级一点呢

使用 `?max_age=86400` 参数设置为期 86400 秒的缓存。

在获取的字典结果后再使用 `.key` 的方式获得更精细数据，节省带宽，例如：

[https://aliyun.nana7mi.link/user.User(2).get_user_info().face?max_age=86400](https://aliyun.nana7mi.link/user.User(2).get_user_info().face?max_age=86400)

对于列表结果可以使用 `.index` 的方式获取列表中对应元素，例如：

[https://aliyun.nana7mi.link/user.User(660303135).get_dynamics(0:int).cards.3.card](https://aliyun.nana7mi.link/user.User(660303135).get_dynamics(0:int).cards.3.card)

