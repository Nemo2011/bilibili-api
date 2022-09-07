![bilibili-api logo](https://raw.githubusercontent.com/nemo2011/bilibili-api/main/design/logo.png)

<div align="center">

# bilibili-api

[![API 数量](https://img.shields.io/badge/API%20数量-200+-blue)][api.json]
[![LICENSE](https://img.shields.io/badge/LICENSE-GPLv3-red)][license]
[![STARS](https://img.shields.io/github/stars/nemo2011/bilibili-api?color=yellow&label=Github%20Stars)][stargazers]
![Python](https://img.shields.io/badge/Python-3.10|3.9|3.8-blue)

</div>

开发文档: [bilibili_api 开发文档][docs] ([GitHub][docs-github])([Gitee][docs-gitee])

原项目地址：[https://github.com/MoyuScript/bilibili-api](https://github.com/MoyuScript/bilibili-api)

Github 仓库：[https://github.com/nemo2011/bilibili-api](https://github.com/nemo2011/bilibili-api)

Gitee 仓库：[https://gitee.com/nemo2011/bilibili-api](https://gitee.com/nemo2011/bilibili-api)

# 简介

这是一个用 Python 写的调用 [Bilibili](https://www.bilibili.com) 各种 API 的库，
范围涵盖视频、音频、直播、动态、专栏、用户、番剧等[[1]](#脚注)。

## 特色

- 范围涵盖广，基本覆盖常用的爬虫，操作。
- 可使用代理，绕过 b 站风控策略。
- 全面支持 BV 号（bvid），同时也兼容 AV 号（aid）。
- 调用简便，函数命名易懂，代码注释详细。
- 依赖少，无需第三方命令行工具，装完即用，无需其他配置。
- 不仅仅是官方提供的 API！还附加：AV 号与 BV 号互转[[2]](#脚注)、连接直播弹幕 Websocket 服务器、视频弹幕反查、下载弹幕、字幕文件、专栏内容爬取等。
- **支持自动登录!**
- **全部是异步操作**。

# 快速上手

首先使用以下指令安装本模块：

```
$ pip3 install bilibili-api-python
```

接下来我们来获取视频的播放量等信息：

```python
import asyncio
from bilibili_api import video

async def main():
    # 实例化 Video 类
    v = video.Video(bvid="BV1uv411q7Mv")
    # 获取信息
    info = await v.get_info()
    # 打印信息
    print(info)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```

输出（已格式化，已省略部分）：

```json
{
    "bvid": "BV1uv411q7Mv",
    "aid": 243922477,
    "videos": 1,
    "tid": 17,
    "tname": "单机游戏",
    "copyright": 1,
    "pic": "http://i2.hdslb.com/bfs/archive/82e52df9d0221836c260c82f2890e3761a46716b.jpg",
    "title": "爆肝９８小时！在 MC 中还原糖调小镇",
    "pubdate": 1595203214,
    "ctime": 1595168654,
    ...and more
}
```

如何给这个视频点赞？我们需要登录自己的账号。

这里设计是传入一个 Credential 类，获取所需的信息参照：[获取 Credential 类所需信息][get-credential]

下面的代码将会给视频点赞

```python
import asyncio
from bilibili_api import video, Credential

async def main():
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 Video 类
    v = video.Video(bvid="BVxxxxxxxx", credential=credential)
    info = await v.get_info()
    print(info)
    # 给视频点赞
    await v.like(True)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```

如果没有报错，就代表调用 API 成功，你可以到视频页面确认是不是调用成功了。

!> 注意，请不要泄露这两个值给他人，否则你的账号将可能遭受盗号的风险！

# 异步迁移

由于从 v5 版本开始，全部改为异步，如果你不会异步，可以参考 [asyncio](https://docs.python.org/zh-cn/3/library/asyncio.html)

异步可以进行并发请求，性能更高，不过如果请求过快仍然会导致被屏蔽。

总的来说，异步比同步更有优势，所以不会的话可以去学一下，会发现新天地（误

如果你仍然想继续使用同步代码，请参考 [同步执行异步代码](https://nemo2011.github.io/bilibili-api/#/sync-executor)

# FA♂Q

**Q: 关于 API 调用的正确姿势是什么？**

A: 所有 API 调用，请尽量使用 **指名方式** 传参，
因为 API 较多，可能不同函数的传参顺序不一样，例子：

```python
# 推荐
video.get_info(bvid="BV1uv411q7Mv")

# 当然也可以这样
kwargs = {
    "bvid": "BV1uv411q7Mv"
}
video.get_info(**kwargs)

# 不推荐
video.get_info("BV1uv411q7Mv")
```

**Q: 为什么会提示 412 Precondition Failed ？**

A: 你的请求速度太快了。造成请求速度过快的原因可能是你写了高并发的代码。

这种情况下，你的 IP 会暂时被封禁而无法使用，你可以设置代理绕过。

```python
from bilibili_api import settings

settings.proxy = "http://your-proxy.com" # 里头填写你的代理地址

settings.proxy = "http://username:password@your-proxy.com" # 如果需要用户名、密码
```

**Q: 怎么没有我想要的功能？**

A: 你可以发 Issue 来提交你的需求，但是，最好的办法是自己写（懒）

<span id="contribute">**Q: 我有一个大胆的想法，如何给代码库贡献？**</span>

A: 请先 clone 本仓库一份，然后从 main 分支新建一个分支，在该分支上工作。
如果你觉得已经可以了，请向项目仓库的 develop 分支发起 Pull request。
如果你不明白这些操作的话，可以百度。完整指南：[CONTRIBUTING.md](https://github.com/nemo2011/bilibili-api/blob/main/.github/CONTRIBUTING.md)

**Q: 稳定性怎么样？**

A: 由于该模块比较特殊，是爬虫模块，如果 b 站的接口变更，可能会马上失效。因此请始终保证是最新版本。如果发现问题可以提 [Issues][issues-new]。

# 脚注

+ \[1\] 这里只列出一部分，请以实际 API 为准。
+ \[2\] 代码来源：<https://www.zhihu.com/question/381784377/answer/1099438784>


[docs]: https://nemo2011.github.io/bilibili-api
[docs-github]: https://github.com/nemo2011/bilibili-api/tree/main/docs
[docs-gitee]: https://gitee.com/nemo2011/bilibili-api/tree/main/docs
[api.json]: https://github.com/nemo2011/bilibili-api/tree/main/bilibili_api/data/api/
[license]: https://github.com/nemo2011/bilibili-api/tree/main/LICENSE.md
[stargazers]: https://github.com/nemo2011/bilibili-api/stargazers
[issues-new]: https://github.com/nemo2011/bilibili-api/issues/new
[get-credential]: https://nemo2011.github.io/bilibili-api/#/get-credential
