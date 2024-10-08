# `Opus`, `Article`, `Dynamic`

~~不得不说阿 b 真会整活~~

为防止许多人对这三个类之间的关系、定义不理解，下文将作出详细解释。

## 1. 定义

- `Opus`: 图文。跳转后链接为 `https://www.bilibili.com/opus/***`。
- `Article`: 专栏。可用于访问链接为 `https://www.bilibili.com/read/cv***`。
- `Dynamic`: 动态。可用于访问链接为 `https://t.bilibili.com/***`。

例如崩坏星穹铁道的版本更新说明，可以用以下两个链接访问：

- `https://www.bilibili.com/opus/863994527716737095`
- `https://www.bilibili.com/read/cv27705422/`

所以这个版本更新说明既是专栏，又是图文。

而原神4.4版本更新说明，可以用以下两个链接访问：

- `https://www.bilibili.com/opus/892568086139371664?spm_id_from=333.1365.0.0`
- `https://www.bilibili.com/read/cv30460236/?spm_id_from=333.1365.0.0`

但是第一个 `opus` 链接会重定向至第二个链接，需要跳转，所以其不是图文，但是是专栏。

## 2. 分类

接下来我们对各个类之间的关系进行一个梳理：

![](./opus.png)

## 3. 解析

1. 部分专栏和动态发布时，会自动转成图文，但是他们还是属于动专栏和动态。
2. 在创建图文之后，也会对专栏创建对应动态。大概率是因为图文的 `API` 部分是直接照抄动态的来用的。因此所有的图文全部属于动态。
3. 剩下不是图文的专栏或者动态，即为普通专栏和普通动态。
4. 公开笔记会以专栏的形式存在。

## 4. 不同类存在的不同 api

对于所有三个类，都可以点赞、收藏；对于 `Dynamic` 和 `Opus`，可以查询“点赞与转发”；对于 `Article` 和 `Opus`，可以投币。

注：`Dynamic` 中所有的 API 为旧版动态页面的 API；`Article` 中所有的 API 为旧版专栏页面的 API；`Opus` 中所有的 API 则是新版图文页面的 API。

## 5. 模块提供的类之间的转换

- `Article` -> `Opus`
- `Dynamic` -> `Opus`
- `Opus` -> `Article`
- `Opus` -> `Dynamic`
