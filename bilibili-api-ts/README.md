<div align="center">

![bilibili-api logo](https://raw.githubusercontent.com/Nemo2011/bilibili_api/main/design/logo-small.png)

# bilibili-api **typescript** 分部

![LICENSE](https://img.shields.io/badge/LICENSE-GPLv3-red)
![STARS](https://img.shields.io/github/stars/Nemo2011/bilibili_api?color=yellow&label=Github%20Stars)

python 版：<https://github.com/Nemo2011/bilibili_api/blob/main/README.md>

</div>

# 简介

这里是 Python 模块 bilibili-api 的 Typescript 克隆，适用于 JS/TS

**注意：本仓库全都是异步操作，而且是 `ajax`，就是那种代码跑完了结果你的结果才刚刚出来的那种，不 `await` 后果自负。**

# 快速上手

首先，使用以下命令安装：

```
$ npm install bilibili-api-ts
```

或者在 `package.json` 中添加依赖。

接下来让我们获取视频播放量等信息：

``` typescript
import { Video } from "bilibili-api-ts/video";

// 实例化 Video 类
var v = new Video("BV1uv411q7Mv");
// get_info 是 async 函数
v.get_info().then(
    function (value) {
        // value 即为结果
        console.log(value);
    }
)
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

# FA♂Q

**Q: 为什么会提示 412 Precondition Failed ？**

A: 你的请求速度太快了。造成请求速度过快的原因可能是你写了高并发的代码。

这种情况下，你的 IP 会暂时被封禁而无法使用，你可以设置代理绕过。

```typescript
import { setProxy, Proxy } from "bilibili-api-ts"
setProxy(new Proxy("代理网址", "代理端口", "用户名（可选）", "密码（可选)"))
```

**Q: 怎么没有我想要的功能？**

A: 你可以发 Issue 来提交你的需求，但是，最好的办法是自己写（懒）

<span id="contribute">**Q: 我有一个大胆的想法，如何给代码库贡献？**</span>

A: 请先 clone 本仓库一份，然后从 main 分支新建一个分支，在该分支上工作。
如果你觉得已经可以了，请向项目仓库的 develop 分支发起 Pull request。
如果你不明白这些操作的话，可以百度。完整指南：[CONTRIBUTING.md](https://github.com/Nemo2011/bilibili_api/blob/javascript/.github/JAVASCRIPT.md)

**Q: 稳定性怎么样？**

A: 由于该模块比较特殊，是爬虫模块，如果 b 站的接口变更，可能会马上失效。因此请始终保证是最新版本。如果发现问题可以提 [Issues][issues-new]。
