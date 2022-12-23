<div align="center">

# **MPlayer** - A Bilibili Interactive Video Player

**⚠️⚠️⚠️FBI Warning: **💩code**⚠️⚠️⚠️**

</div>

这个播放器只不过是为了播放 bilibili_api 下载下来的 IVI 互动视频文件而写的，因此更注重于互动视频的逻辑，而不是播放器基础功能，更不会整什么花里胡哨的外观。

## 功能介绍

通过 MPlayer，你能在离线状态下通过 `ivi` 文件来玩互动视频。`MPlayer` 支持互动视频的跳转、变量、跳转概率等概念，能~~完全~~还原互动视频体验。在基础的视频播放上面，`MPlayer` 还原了进度条、音量控制。

## 原理介绍

本项目使用 Python**3.11**(内含 python**3.10** `match-case` 最新语法)，基于 PyQt**6** 开发，许多地方与 PyQt**5** 不兼容，因此你需要另外安装 PyQt**6**。

## Download & Run

本项目可以在 `pypi` 中安装。当然，你也可以使用编译好的文件（我只编译了 windows，因为其他平台编译都失败了。如果有大佬能帮忙编译好那是最好。）

运行请使用 `python3 -m mplayer` 运行。
