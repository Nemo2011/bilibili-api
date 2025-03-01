![bilibili-api logo](https://raw.githubusercontent.com/Nemo2011/bilibili-api/main/design/logo.png)

<div align="center">

# bilibili-api

[![API 数量](https://img.shields.io/badge/API%20数量-400+-blue)][api.json]
[![LICENSE](https://img.shields.io/badge/LICENSE-GPLv3+-red)][LICENSE]
[![Python](https://img.shields.io/badge/python-3.13|3.12|3.11|3.10|3.9-blue)](https://www.python.org)
[![Stable Version](https://img.shields.io/pypi/v/bilibili-api-python?label=stable)][pypi]
[![Pre-release Version](https://img.shields.io/github/v/release/Nemo2011/bilibili-api?label=pre-release&include_prereleases&sort=semver)][pypi-dev]
[![STARS](https://img.shields.io/github/stars/nemo2011/bilibili-api?color=yellow&label=Github%20Stars)][stargazers]
[![Testing](https://github.com/Nemo2011/bilibili-api/actions/workflows/testing.yml/badge.svg?branch=dev)](https://github.com/Nemo2011/bilibili-api/actions/workflows/testing.yml)

**:warning: 接口可能改动，请及时更新最新版 [![Stable Version](https://img.shields.io/pypi/v/bilibili-api-python?label=stable)][pypi]**

</div>

**注意事项：使用此模块时请仅用于学习和测试，禁止用于非法用途及其他恶劣的社区行为如：恶意刷屏、辱骂黄暴、各种形式的滥用等，违规此模块许可证 `GNU General Public License Version 3` 及此条注意事项而产生的任何后果自负，模块的所有贡献者不负任何责任。**

开发文档: [bilibili_api 开发文档][docs] ([GitHub][docs-github]) <!-- ([Gitee][docs-gitee]) -->

原仓库地址：[https://github.com/MoyuScript/bilibili-api](https://github.com/MoyuScript/bilibili-api)

Github 仓库：[https://github.com/nemo2011/bilibili-api](https://github.com/nemo2011/bilibili-api)

<!-- Gitee 仓库：[https://gitee.com/nemo2011/bilibili-api](https://gitee.com/nemo2011/bilibili-api) 长期未同步... -->

> 此仓库是对原仓库 `bilibili-api` 的继续的维护。更多相关的信息请前往原仓库地址进行查看。

# 简介

这是一个用 Python 写的调用 [Bilibili](https://www.bilibili.com) 各种 API 的库，
范围涵盖视频、音频、直播、动态、专栏、用户、番剧等[[1]](#脚注)。

## 特色

- 范围涵盖广，基本覆盖常用的爬虫，操作。
- 可使用代理，绕过 b 站风控策略。
- 全面支持 BV 号（bvid），同时也兼容 AV 号（aid）。
- 调用简便，函数命名易懂，代码注释详细。
- 不仅仅是官方提供的 API！还附加：AV 号与 BV 号互转[[2]](#脚注)、连接直播弹幕 Websocket 服务器、视频弹幕反查、下载弹幕、字幕文件[[3]](#脚注)、专栏内容爬取、cookies 刷新等[[4]](#脚注)。
- 支持采用各种手段避免触发反爬虫风控[[5]](#脚注)。
- **全部是异步操作**。
- 默认支持 `aiohttp` / `httpx` / `curl_cffi`。

# 快速上手

首先使用以下指令安装本模块：

```
# 主版本
$ pip3 install bilibili-api-python

# 开发版本
$ pip3 install bilibili-api-dev

# 最新修改会在 dev 分支
$ pip3 install git+https://github.com/Nemo2011/bilibili-api.git@dev
```

然后需要**自行安装**一个支持异步的第三方请求库，如 `aiohttp` / `httpx` / `curl_cffi`。

```
# aiohttp
$ pip3 install aiohttp

# httpx
$ pip3 install httpx

# curl_cffi
$ pip3 install "curl_cffi"
```

接下来我们来获取视频的播放量等信息：

```python
import asyncio
from bilibili_api import video


async def main() -> None:
    # 实例化 Video 类
    v = video.Video(bvid="BV1uv411q7Mv")
    # 获取信息
    info = await v.get_info()
    # 打印信息
    print(info)


if __name__ == "__main__":
    asyncio.run(main())

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

async def main() -> None:
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 Video 类
    v = video.Video(bvid="BVxxxxxxxx", credential=credential)
    info = await v.get_info()
    print(info)
    # 给视频点赞
    await v.like(True)

if __name__ == '__main__':
    asyncio.run(main())
```

如果没有报错，就代表调用 API 成功，你可以到视频页面确认是不是调用成功了。

> **Warning** 注意，请不要泄露这两个值给他人，否则你的账号将可能遭受盗号的风险！

# 异步迁移

由于从 v5 版本开始，基本全部改为异步，如果你不会异步，可以参考 [asyncio](https://docs.python.org/zh-cn/3/library/asyncio.html)

异步可以进行并发请求，性能更高，不过如果请求过快仍然会导致被屏蔽。

总的来说，异步比同步更有优势，所以不会的话可以去学一下，会发现新天地（误

如果你仍然想继续使用同步代码，请参考 [同步执行异步代码](https://nemo2011.github.io/bilibili-api/#/sync-executor)

# 模块使用的请求库

模块在允许的条件下，按照 `curl_cffi` `aiohttp` `httpx` 的优先级选择第三方请求库。

如果想要指定请求库，可以利用 `select_client` 进行切换。

``` python
from bilibili_api import select_client

select_client("curl_cffi") # 选择 curl_cffi，支持伪装浏览器的 TLS / JA3 / Fingerprint
select_client("aiohttp") # 选择 aiohttp
select_client("httpx") # 选择 httpx，不支持 WebSocket
```

curl_cffi 支持伪装浏览器的 TLS / JA3 / Fingerprint，但需要手动设置。

``` python
from bilibili_api import request_settings

request_settings.set("impersonate", "chrome131") # 第二参数数值参考 curl_cffi 文档
# https://curl-cffi.readthedocs.io/en/latest/impersonate.html
```

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
from bilibili_api import request_settings

request_settings.set_proxy("http://your-proxy.com") # 里头填写你的代理地址

request_settings.set_proxy("http://username:password@your-proxy.com") # 如果需要用户名、密码
```

**Q: 我想在项目中使用这个模块，但是我的项目使用其他请求库进行网络请求（如 `pycurl`），想要模块也同时使用它（们），可以吗？**

A: 可以，但是你可能要自己动手实现模块和具体请求库的适配。详见 [自定义请求库](https://nemo2011.github.io/bilibili-api/#/request_client)

**Q: 怎么没有我想要的功能？**

A: 你可以发 Issue 来提交你的需求，但是，最好的办法是自己写（懒）

<span id="contribute">**Q: 我有一个大胆的想法，如何给代码库贡献？**</span>

A: 请先 clone 本仓库一份，然后从 main 分支新建一个分支，在该分支上工作。
如果你觉得已经可以了，请向项目仓库的 develop 分支发起 Pull request。
如果你不明白这些操作的话，可以百度。完整指南：[CONTRIBUTING.md](https://github.com/nemo2011/bilibili-api/blob/main/.github/CONTRIBUTING.md)

**Q: 稳定性怎么样？**

A: 由于该模块比较特殊，是爬虫模块，如果 b 站的接口变更，可能会马上失效。因此请始终保证是最新版本。如果发现问题可以提 [Issues][issues-new]。

# 脚注

- \[1\] 这里只列出一部分，请以实际 API 为准。
- \[2\] 代码来源：<https://www.zhihu.com/question/381784377/answer/1099438784> (WTFPL)
- \[3\] 部分代码来源：<https://github.com/m13253/danmaku2ass> (GPLv3) <https://github.com/ewwink/python-srt2ass>
- \[4\] 思路来源：<https://socialsisteryi.github.io/bilibili-API-collect/docs/login/cookie_refresh.html> (CC-BY-NC 4.0)
- \[5\] 大量思路来源 <https://socialsisteryi.github.io/bilibili-API-collect> 中相关讨论。

[docs]: https://nemo2011.github.io/bilibili-api
[docs-github]: https://github.com/nemo2011/bilibili-api/tree/main/docs
[docs-gitee]: https://gitee.com/nemo2011/bilibili-api/tree/main/docs
[api.json]: https://github.com/nemo2011/bilibili-api/tree/main/bilibili_api/data/api/
[license]: https://github.com/nemo2011/bilibili-api/tree/main/LICENSE
[stargazers]: https://github.com/nemo2011/bilibili-api/stargazers
[issues-new]: https://github.com/Nemo2011/bilibili-api/issues/new/choose
[get-credential]: https://nemo2011.github.io/bilibili-api/#/get-credential
[pypi]: https://pypi.org/project/bilibili-api-python
[pypi-dev]: https://pypi.org/project/bilibili-api-dev

# Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Nemo2011/bilibili-api&type=Date)](https://star-history.com/#Nemo2011/bilibili-api&Date)
