<div>

# MPlayer - A Bilibili Interactive Video Player

</div>

<strong>⚠️⚠️⚠️FBI Warning: 💩 code⚠️⚠️⚠️</strong>

这个播放器只不过是为了播放 bilibili_api 下载下来的 IVI 互动视频文件而写的，因此更注重于互动视频的逻辑，而不是播放器基础功能，更不会整什么花里胡哨的外观。

## 功能介绍

通过 MPlayer，你能在离线状态下通过 `ivi` 文件来玩互动视频。`MPlayer` 支持互动视频的跳转、变量、跳转概率等概念，能完全还原互动视频体验 (除了 `进度回馈` 做得有点 shit)。在基础的视频播放上面，`MPlayer` 还原了进度条、音量控制，如你所见，甚至连倍速都没有加。至于发送弹幕功能（不都说了是离线播放器吗，弹幕是离线状态能发的东西吗）。

## 原理介绍

本项目基于 PyQt**6** 开发，许多地方与 PyQt**5** 不兼容，因此你需要另外安装 PyQt**6**，虚拟环境及第三方包管理工具是 **Poetry**，用的是 `pyproject.toml`，因此不能用 `setup.py`。

## Download & Run

本项目可以在 `pypi` 中安装。当然，你也可以使用编译好的文件（我只编译了 windows，因为其他平台编译都失败了。如果有大佬能帮忙编译好那是最好。）

运行请使用 `python3 -m mplayer` 运行。
