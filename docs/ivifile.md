# 有关 `ivi` 文件的说明

> `ivi` 文件是在 bilibili-api `v14.0.0.a3` 时发布的新功能，提供了一种互动视频离线保存的格式。`.ivi` 文件不能保证可以完全还原互动视频的体验。

[文件详解](#ivi-文件详解)

# 有关 `ivitools` 的说明

`ivitools` 是管理 `ivi` 文件的工具，支持：拆开、播放、扫描 `ivi` 文件。`ivitools` 将在 `bilibili_api` 安装的时候自动安装完毕，可以直接用 `ivitools` 调用相关功能。

# `ivitools` 命令详解

1. `ivitools download [BVID] [OUT]` 下载互动视频至 `ivi` 格式
2. `ivitools extract [IVI] [OUT]` 拆开 `ivi` 文件至目标文件夹
3. `ivitools help` 帮助
4. `ivitools play [IVI]` 播放 `ivi` 文件
5. `ivitools scan [IVI]` 扫描 `ivi` 文件
6. `ivitools touch [IVI]` 获取 `ivi` 文件简介 (`JSON` 格式 )

# `ivi` 文件详解

解析 `ivi` 文件首先需要拆开它，可以用 `ivitools extract` 命令，当然，`ivi` 文件的打包格式就是 `zip`。

拆开后，我们可以看见许多的文件。文件树如下：

- test_ivi
  - bilivideo.json
  - ivideo.json
  - xxxxx.video.mp4
  - xxxxx.audio.mp4

其中，`bilivideo.json` 存放了视频的基本信息（`BVID` 和视频标题）。而 `ivideo.json` 则是剧情树。还有许多的 `mp4` 文件，这些都对应了一个个的节点，举个例子，`123.audio.mp4` 是 `cid` 为 `123` 的节点对应的视频的音频流。节点的 `cid` 可以在 `ivideo.json` 中找到。

`ivideo.json` 存放的是一个字典，字典的 `key` 对应了节点的 `id`，而内容则是节点的信息。无论哪个视频，初始的节点的 `id` 永远都是 `1`。以下为一个节点的信息的详解: 

- "1" (str: 节点 ID 转为字符串的结果)
  - `title` (str: 标题)
  - `cid` (int: CID)
  - `button` (dict: 跳转对应按钮的信息)
    - `text` (str: 按钮文字)
    - `align` (int: 按钮文字相对于定位的位置，有上左下右中五种，可以参考 `interactive_video.InteractiveButtonAlign`，里面有详细注释)
    - `pos` (list: 按钮位置信息 (如果所有按钮都照正常布局，那么此数据的值为 `[null, null]`))
      - `0`: X 坐标
      - `1`: Y 坐标
  - `condition` (str: 节点跳转必须符合的表达式，默认为 `""`。为 `javascript` 语言。主要作用为实现随机跳转。)
  - `jump_type` (int: 跳转方式，有直接跳转和选择跳转两种，可查看 `interactive_video.InteractiveJumpingType`)
  - `is_default` (bool: 是否为默认节点，如果是直接跳转则会跳转至默认节点，或者是定时选择后直接跳转至默认节点(定时选择后直接跳转目前不支持))
  - `command` (str: 跳转成功后需要对变量做的操作。为 `javascript` 语言。)
  - `sub` (list: 子节点列表)
  - `vars` (list: 初始化时的变量设置)
    - `每一项` (dict)
      - `name` (str: 变量名)
      - `id` (str: 变量 id，为变量在 `command` 和 `condition` 中出现时使用的变量名)
      - `value` (int: 变量数值)
      - `show` (bool: 变量是否展示，有的变量需要时刻展示给观看者，例如 `循环编号`, `分数` 等)
      - `random` (bool: 变量是否随机值。随机变量配上跳转公式是实现随机跳转的重要部分，这里说明：随机值取值范围为 `0-100`。)

这里列出文件详解，是为了其他大佬可以把 `ivi` 文件移植到其他语言上。如果对文件有疑惑，欢迎提 `issues`!
