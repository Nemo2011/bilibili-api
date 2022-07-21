<div align="center">

![bilibili-api logo](./logo-small.png)

# bilibili-api **typescript** 分部

<img src="https://cdn.iconscout.com/icon/free/png-512/typescript-1174965.png" height=50 width=50><img src="https://logos-download.com/wp-content/uploads/2019/01/JavaScript_Logo.png" height=50 width=50><img src="https://tse4-mm.cn.bing.net/th/id/OIP-C.bodQFDX6bpdw0aj11XxjrAHaCi?pid=ImgDet&rs=1" height=50>

![LICENSE](https://img.shields.io/badge/LICENSE-GPLv3-red)
![STARS](https://img.shields.io/github/stars/nemo2011/bilibili-api?color=yellow&label=Github%20Stars)

python 版：<https://github.com/nemo2011/bilibili-api/blob/main/README.md>

</div>

# 简介

这里是 Python 模块 bilibili-api 的 Typescript 克隆，适用于 JS/TS

**注意：本仓库全都是异步操作，而且是 `ajax`，就是那种代码跑完了结果你的结果才刚刚出来的那种，不 `await` 后果自负。**

如果您是新手，请务必看完这个 `readme`，里面有许多重要的信息。

## 特色

- 可使用代理，绕过 b 站风控策略。
- 全面支持 BV 号（bvid），同时也兼容 AV 号（aid）。
- 调用简便，函数命名易懂，代码注释详细。
- 依赖少，无需第三方命令行工具，装完即用，无需其他配置。
- 更多的 API 敬请期待！

# 快速上手

首先，使用以下命令安装：

```
$ npm install bilibili-api-ts
```

或者在 `package.json` 中添加依赖。

接下来让我们获取视频播放量等信息：

``` typescript
// TS
import { Video } from "bilibili-api-ts/video";

// 实例化 Video 类
var v = new Video({
    bvid: "BV1uv411q7Mv"
});
// get_info 是 async 函数
v.get_info({}).then(
    function (value) {
        // value 即为结果
        console.log(value);
    }
)
```

``` javascript
// JS
const video = require("bilibili-api-ts/video.js");

// 实例化 Video 类
var v = new video.Video({
    bvid: "BV1uv411q7Mv"
});
// get_info 是 async 函数
v.get_info({}).then(
    function (value) {
        // value 即为结果
        console.log(value);
    }
)
```

>鉴于 js 与 ts 没什么大区别，所以后面所有的代码示例会只保留 `typescript` 代码。

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


**Q: 关于 API 调用的正确姿势是什么？**

A: 所有 API 调用，请使用 **指名方式** 传参，例子：

```typescript
// 参数：{bvid}: {bvid: string}
/** 
 * 所有的参数传入请传入一个字典，这样子可以换传参顺序、指名传参。
 * 请不要直接传参数，参数需要放在字典里，而且需要表明好键，不能不标键。
 */ 
// ----------
// 推荐
video.get_info({bvid:"BV1uv411q7Mv"})

// 当然也可以这样
video.get_info({"bvid":"BV1uv411q7Mv"})

// 不可以！
video.get_info({"BV1uv411q7Mv"}) // 没有标明键(bvid)

// 自己看 IntelliCode 的提示吧。
video.get_info("BV1uv411q7Mv") // 传入字典啊！
```

**Q: 为什么会提示 412 Precondition Failed ？**

A: 你的请求速度太快了。造成请求速度过快的原因可能是你写了高并发的代码。

这种情况下，你的 IP 会暂时被封禁而无法使用，你可以设置代理绕过。

```typescript
import { setProxy, Proxy } from "bilibili-api-ts"
setProxy(new Proxy({
    host: "代理网址", 
    port: "代理端口", 
    username: "用户名（可选）", 
    password: "密码（可选)"
}))
```

**Q: 怎么没有我想要的功能？**

A: 你可以发 Issue 来提交你的需求，但是，最好的办法是自己写（懒）

<span id="contribute">**Q: 我有一个大胆的想法，如何给代码库贡献？**</span>

A: 请先 clone 本仓库一份，然后从 main 分支新建一个分支，在该分支上工作。
如果你觉得已经可以了，请向项目仓库的 develop 分支发起 Pull request。
如果你不明白这些操作的话，可以百度。完整指南：[CONTRIBUTING.md](https://github.com/nemo2011/bilibili-api/blob/javascript/.github/JAVASCRIPT.md)

**Q: 稳定性怎么样？**

A: 由于该模块比较特殊，是爬虫模块，如果 b 站的接口变更，可能会马上失效。因此请始终保证是最新版本。如果发现问题可以提 [Issues][issues-new]。
