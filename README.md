![LOGO](https://res.passkou.com/image/20200812011335.png)

# bilibili_api

[![API数量](https://img.shields.io/badge/API数量-100+-blue)](https://github.com/Passkou/bilibili_api/tree/master/bilibili_api/data/api.json) [![STARS](https://img.shields.io/github/stars/Passkou/bilibili_api?color=yellow&label=Github%20Stars)](https://github.com/Passkou/bilibili_api/stargazers) [![LICENSE](https://img.shields.io/badge/LICENSE-GPLv3-red)](https://github.com/Passkou/bilibili_api/tree/master/LICENSE.md) ![Python](https://img.shields.io/badge/Python-3.9|3.8-blue) [![](https://img.shields.io/badge/这个标签太好玩了-.py-orange)](https://shields.io/)


**开发文档**: [bilibili_api 开发文档][docs]

# 公告

**由于本人学业繁忙，如果有需求、非严重BUG等，请尽量自己实现，可以修改源代码然后发pull request给我，谢谢！**

# 介绍

这是一个用Python写的调用 [Bilibili](https://www.bilibili.com) 各种API的库，范围涵盖视频、音频、直播、动态、专栏、用户、番剧等[[1]](#脚注)。你可以使用很简短的代码去调用API，而不需要自己去寻找API，指定各种参数。

用到的第三方库：

- requests
- beautifulsoup4
- aiohttp
- websockets
- cssutils

# 特色

- 范围涵盖广，基本覆盖常用的爬虫，操作。
- 可使用代理，绕过b站风控策略。
- 全面支持BV号（bvid），同时也兼容AV号（aid）。
- 调用简便，函数命名易懂，代码注释详细。
- 不仅仅是官方提供的API！还附加：AV号与BV号互转[[2]](#脚注)、连接直播弹幕Websocket服务器、视频弹幕反查[[3]](#脚注)、专栏内容爬取等。
- 更多功能请参照 [开发文档][docs]。

# 快速开始

首先使用以下指令安装本模块：

```
$ pip install bilibili_api
```

接下来我们来获取视频的播放量等信息：

```python
from bilibili_api import video

v = video.get_video_info(bvid="BV1uv411q7Mv")
print(v)
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
    "title": "爆肝９８小时！在MC中还原糖调小镇",
    "pubdate": 1595203214,
    "ctime": 1595168654,
    ...
}
```

就这么简单。

如何给这个视频点赞？我们需要登录自己的账号。

几乎所有函数都支持传入一个本API自定义的类 `bilibili_api.Verify` ，用于验证登录。

为了调用API方便，我们一次性获取全部需要用到的值。

## 获取 SESSDATA 和 CSRF

这里以 **谷歌浏览器** 为例。

首先我们可以在链接栏左侧看到一个小锁，如果你没有使用HTTPS，那么可能会显示 `不安全` 的字样，点击以后，下面有个Cookies。

![](https://res.passkou.com/image/20200812000443.png)

点开后，我们在下面找到以下两个键对应的值，分别是 **SESSDATA** 和 **bili_jct**，这里注意一下，**bili_jct 就是 CSRF **。

![](https://res.passkou.com/image/20200812000554.png)

接下来，我们实例化 `bilibili_api.Verify` 类，之后用于传入各种API函数。

```python
from bilibili_api import Verify

verify = Verify(sessdata="你的SESSDATA值", csrf="你的bili_jct值")
```

接下来我们给这个视频进行点赞操作，完整代码如下：

```python
from bilibili_api import video, Verify

verify = Verify("你的SESSDATA值", "你的bili_jct值")
video.set_like(bvid="BV1uv411q7Mv", status=True, verify=verify)
```

如果没有报错，就代表调用API成功，你可以到视频页面确认是不是调用成功了。

**注意，请不要泄露这两个值给他人，否则你的账号将可能遭受盗号的风险！**

**注意，请不要泄露这两个值给他人，否则你的账号将可能遭受盗号的风险！**

**注意，请不要泄露这两个值给他人，否则你的账号将可能遭受盗号的风险！**

# 一些注意事项

这里是一些常见的注意事项，基本只要遵守了这些注意事项调用API就不会出太大问题~~（除非有BUG）~~

## 关于API调用

所有API调用，请尽量使用 **指名方式** 传参，因为API较多，我写的时候可能不同函数的传参顺序不一样，例子：

```python
# 建议方式
video.set_like(bvid="BV1uv411q7Mv", status=True, verify=verify)

# 当然也可以这样
kwargs = {
    "bvid": "BV1uv411q7Mv",
    "status": True,
    "verify": verify
}
video.set_like(**kwargs)

# ！！！不建议方式
video.set_like("BV1uv411q7Mv", True, verify)
```

这样不管顺序是怎么样都不用怕了（余裕）

## 关于b站风控策略

请求速度不要过快，自己测试简单的线性请求（如单线程使用循环结构）请求是不会触发风控策略的，当然这是大部分API，以实际情况为准。

如果你使用多线程、多进程或者并发等在同一时间点请求多次的方法，可能会触发b站风控策略，返回的状态码是412，导致无法继续使用爬虫。

当然如果你已经触发风控策略，可以通过设置代理来绕过。设置方法如下：

```python
import bilibili_api

bilibili_api.request_settings["proxies"] = {} # 里头填写你的代理
```

如何设置请参照 [requests 设置代理](https://requests.readthedocs.io/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)，传入和说明相同的值就可以了。

# Issue 提交规范

为了能高效回答大家的问题，在这里简单讲一下提交Issue的规范，这么做对你我都方便\_(:з」∠)_。

目前Issue的Tag暂时分为以下几类：

1. **建议**，给这个API的建言献策。
2. **提问**，在使用过程中遇到的疑问。
3. **漏洞**，API出现了BUG。
4. **需求**，API尚未收录的功能但是你有需求。

这个Tag只能我标记，希望你们在提交Issue的时候尽量使用以下格式：

---

类型：上述提到的Tag

版本：你当前使用的API版本

（这里就可以写正文了）

---

**举个栗子**

---

类型：漏洞

版本：2.0.0

你这是什么API啊，害人不浅啊。你已经是个成熟的API了，怎么还不会帮我自动爬虫？我看你就是个逊啦。

---

## 在提交 Issue 前

如果是遇到漏洞，建议你先检查自己API的版本是不是最新的，可能更新到最新版本就解决了问题。如果已经是最新的仍然存在漏洞，就可以提交 Issue 来骂我 ~~（并不）~~ 。

提问前请先仔细阅读 [开发文档][docs] ！！！！里面写的很全面，如果实在不懂再发 Issue 来问。

# PR规范 ~~（不是舔）~~

PR: Pull request

首先非常欢迎你对代码做出贡献~~（这样我就可以偷懒了）~~

在提交PR前，请务必遵守以下的规则，方便你的代码通过审核：

1. 如果你要增加新的API，请先在 `data/api.json` 中对应分类增加API的详细说明，具体格式可以参照现有的内容。另外，请对增加的API代码注释进行详尽的说明，每个参数除非含义十分明显（如bvid），都进行说明，具体格式可以参照现有代码。
2. 希望你能在肝代码前，看看现有的代码风格，尽量模仿，方便日♂后维护。[这里有一份代码风格规范文档可以参考](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/)，实际上如果你使用的IDE是PyCharm，也会对你的代码进行指导。当然，如果你执意不遵守的话............那我就会累死了QAQ。
3. **所有PR请向develop分支发起**

**计划写一份面向开发者的开发文档 ~~(咕咕咕)~~**

# 支持这个项目

这个项目目前只由我（Passkou）一个人在维护。

如果你想支持一下这个项目，可以做以下几点：

1. GitHub上给个小星星（star）~
2. 如果你的项目中用到了这个库，可以在说明文档中标注一下这个项目的Github地址。
3. 如果你用了这个项目进行爬虫，制作了数据统计视频并发到b站或其他视频平台，你也可以在简介中注明一下用到了这个模块，这就够了。
4. 当然，你也可以参与维护这个项目，提交PR即可。

# 脚注

\[1]: 这里只列出一部分，请以实际API为准。


\[2]: 代码来源：<https://www.zhihu.com/question/381784377/answer/1099438784>


\[3]: 代码翻译自：<https://github.com/esterTion/BiliBili_crc2mid>



[docs]: /docs
