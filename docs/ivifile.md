# 有关 `.ivi` 文件的说明

- 1. `.ivi` 文件是在 bilibili-api `v14.0.0.a3` 时发布的新功能，提供了一种互动视频离线保存的格式。
- 2. `.ivi` 文件不能直接用音视频播放器打开，但是你可以把文件后缀改成 `.zip` 并解压查看里面的内容。这里不解释里面的文件名、文件内容、内容含义。
- 3. `.ivi` 文件可以用 [MPlayer](#有关-mplayer-的说明) 打开。
- 4. `.ivi` 文件不能保证可以完全还原互动视频的体验。

# 有关 MPlayer 的说明

- 1. `MPlayer` 是为了播放 `.ivi` 文件而编写的播放器，基于 `PyQt6`
- 2. 因为技术方面的原因，使用 `MPlayer` 播放互动视频文件不能百分之百还原互动视频的体验。
- 3. `MPlayer` 不会在安装 `bilibili_api` 时自动安装。运行请戳 `MPlayer.py`。(运行需要 Python >= 3.10 环境及以下依赖)

        - `PyQt6`
        - `bilibili-api-python>=14.0.0.a3`

    下载信息：

        - commit: `181a588b4df012260fac6ba97342ccc438b7d51e`
        - url: `https://transfer.sh/nodxYp/MPlayer.zip` [(JUMP TO IT)](https://transfer.sh/nodxYp/MPlayer.zip)
        - date: `2022-12-14`


- 4. 可执行文件编译在做。
- 5. 更多有关信息，请查看 [README](https://github.com/Nemo2011/bilibili-api/tree/dev/MPlayer)

**Windows 用户如果打开 MPlayer 后播放视频呈现黑屏，请试着安装 `K-Lite Codec Pack`**

# MacOS 用户打开 MPlayer 注意

**请务必在打开 `MPlayer` 之前按照以下步骤进行操作，否则你可能会遇到下面的情况**

![](/mplayer-tip-pictures/2.png)

---

1. 在访达中找到 `ffmpeg` 的 `MacOS` 可执行文件。

![](/mplayer-tip-pictures/1.png)

2. 双击打开，如果出现如下情况。点击右上角的 `?` 按钮。(如果没有出现其他情况，则可以跳过后面所有步骤。)

![](/mplayer-tip-pictures/2.png)

3. 之后进入 `MacOS 帮助手册` 页面，点击：`为我打开隐私与安全性设置`。

![](/mplayer-tip-pictures/3.png)

4. 进入 `设置` 的 `隐私与安全性设置` 页面后找到 `已阻止使用“ffmpeg“，因为来自身份不明的开发者` 这里，点击：`仍然允许`。

![](/mplayer-tip-pictures/4.png)

5. 随后输入密码以解锁，再次弹出一个确认框，点 `确认` 之后将打开文件。

![](/mplayer-tip-pictures/5.png)

6. 如果一切正常，终端会显示以下信息：

```
ffmpeg version 5.0.1 Copyright (c) 2000-2022 the FFmpeg developers
...
Hyper fast Audio and Video encoder
usage: ffmpeg [options] [[infile options] -i infile]... {[outfile options] outfile}...

Use -h to get full help or, even better, run 'man ffmpeg'
```

---

**打开 `MPlayer` 时遇到其他问题？请提出 [Issues][issues-new] 以便解决。**
