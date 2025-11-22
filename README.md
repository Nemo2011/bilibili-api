![bilibili-api logo](https://raw.githubusercontent.com/Nemo2011/bilibili-api/main/design/logo.png)

<div align="center">

# bilibili-api

</div>

此处为 `dev-dyn-fp` 分支。

## 这个分支是怎么出现的

分支与 `dev` 的主要区别在底层请求功能上的代码，有许多新的特性出现，最早成型于 #973，后在 `feat-browser-fingerprint-integration` 分支中逐步完善，最后这个分支与当时的 `dev` 分支合并形成了这里的 `dev-dyn-fp` 分支。

将来的此分支代码也将跟进 `dev` 分支的更改。

## 有什么新的特性 / 不同之处

- `fpgen` 支持 (from #973)
- `buvid` `bili_ticket` 的维护由全局转移到每个凭据类中维护 (from #973)
- `sid` 加入凭据类、登录功能
- 在上一条基础上提供了保留原来模式的设置
- 请求过滤器支持，可在请求函数前后添加自定义代码
- `BiliAPIClient` 中添加 `download_close`
- 线程安全优化

## 为什么要独立出来

因此分支代码改动过大，不能保证测试充分到位、无重大问题。因此此处建此分支作为体验使用，欢迎所有人对分支代码进行测试。将来此分支代码也将合并至 `dev` 分支。

## TODO(docs)

因特性过多，已考虑在文档中添加特别栏目，逐一介绍部分特性，同时对原来的文档进行加工。
