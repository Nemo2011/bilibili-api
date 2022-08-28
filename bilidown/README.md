<div align="center">

```
                                         _____
________   ___   ___        ___          |   |
|\   __  \ |\  \ |\  \      |\  \        |   |
\ \  \|\ /_\ \  \\ \  \     \ \  \       |   |
   \ \   __  \\ \  \\ \  \     \ \  \    --     --
    \ \  \|\  \\ \  \\ \  \____ \ \  \   \       /
    \ \_______\\ \__\\ \_______\\ \__\   \     /
    \|_______| \|__| \|_______| \|__|    \   /
                                         \_/
```

# **BiliDown**

**专业级 Bilibili 命令行下载器**

**Powered by [Bilibili API](https://github.com/Nemo2011/bilibili-api)**

</div>

***

- **支持几乎所有视频下载**
- **支持弹幕(ass)下载**
- **支持 FLV 视频**
- **支持 cookies(`sessdata`) 登录**
- **支持扫码登录**
- **支持番剧全集下载**
- **支持课程全课时下载**
- **支持 FFmpeg**
- **支持选择分辨率、音质、编码**
- **支持 av1 编码**
- **支持 4K, 8K, 杜比视界**
- **支持音频下载**
- **支持歌单所有音频下载**
- **支持专栏下载(`markdown`, `json`)**
- **支持直播间录播**
- **支持自定义输出文件名**
- **支持自定义输出文件夹**
- **外部程序调用方便**

目前 `BiliDown` 支持下载: 
  - 视频
  - 音频
  - 专栏
  - 番剧
  - 课程
  - 歌单
  - 弹幕
  - 直播间流
  - 用户空间内容

## Install

```
pip install bilidown
```

## Requires

- Python **>= 3.8.0**
- FFmpeg **(可选)**

>`BiliDown` 支持不使用 `FFmpeg`, 如果选择不使用 `FFmpeg` 可以加上 `--ffmpeg "#none"` 参数

## Usage

下载 `字幕君交流场所`(`BV1xx411c7mD` & `av2`): 

```
bilidown av2
```

<details>
<summary> 输出:  </summary>

```
                                         _____
________   ___   ___        ___          |   |
|\   __  \ |\  \ |\  \      |\  \        |   |
\ \  \|\ /_\ \  \\ \  \     \ \  \       |   |
 \ \   __  \\ \  \\ \  \     \ \  \    --     --
  \ \  \|\  \\ \  \\ \  \____ \ \  \   \       /
   \ \_______\\ \__\\ \_______\\ \__\   \     /
    \|_______| \|__| \|_______| \|__|    \   /
                                          \_/

BiliDown: 哔哩哔哩命令行下载器
Powered by Bilibili API
By Nemo2011<yimoxia@outlook.com>
使用 -h 获取帮助。

----------开始下载----------

INF: 链接 -> av2
INF: 正在获取链接信息
INF: 解析结果：视频

INF: 视频 AID:  2
INF: 视频分 P 数:  1
INF: 正在获取下载地址(P1)
INF: 视频清晰度：|  32: 清晰 480P   |  16: 流畅 360P   |
NUM: 请选择清晰度对应数字(默认为最大清晰度): [Enter]
INF: 视频编码：|  avc: AVC(H.264)   |  hev: HEVC(H.265)   |  av01: AV1   |
STR: 请选择视频编码对应的号码(默认为 "avc"): [Enter]
INF: 音频音质：|  30216: 低品质   |  30232: 中等品质   |
NUM: 请选择音质对应数字(默认为最好音质): [Enter]
INF: 选择的视频清晰度 清晰 480P | (32)
INF: 选择的视频编码 AVC(H.264) | (avc)
INF: 选择的音频音质 中等品质 | (30232)

INF: 开始下载视频(P1)
DWN: 开始下载 字幕君交流场所 - BV1xx411c7mD(P1) - 视频 至 ./video_temp.m4s
DWN: 1s. Done 39093 parts. All 39093 parts. (1 part = 1024 bytes)
DWN: 完成下载
INF: 开始下载音频(P1)
DWN: 开始下载 字幕君交流场所 - BV1xx411c7mD(P1) - 音频 至 ./audio_temp.m4s
DWN: 0s. Done 33800 parts. All 33800 parts. (1 part = 1024 bytes)
DWN: 完成下载
INF: 下载视频完成 开始混流


ffmpeg version 5.0.1 Copyright (c) 2000-2022 the FFmpeg developers
  built with Apple clang version 13.1.6 (clang-1316.0.21.2.5)
  configuration: --prefix=/opt/homebrew/Cellar/ffmpeg/5.0.1_3 --enable-shared --enable-pthreads --enable-version3 --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libbluray --enable-libdav1d --enable-libmp3lame --enable-libopus --enable-librav1e --enable-librist --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvmaf --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libspeex --enable-libsoxr --enable-libzmq --enable-libzimg --disable-libjack --disable-indev=jack --enable-videotoolbox --enable-neon
  libavutil      57. 17.100 / 57. 17.100
  libavcodec     59. 18.100 / 59. 18.100
  libavformat    59. 16.100 / 59. 16.100
  libavdevice    59.  4.100 / 59.  4.100
  libavfilter     8. 24.100 /  8. 24.100
  libswscale      6.  4.100 /  6.  4.100
  libswresample   4.  3.100 /  4.  3.100
  libpostproc    56.  3.100 / 56.  3.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from './video_temp.m4s':
  Metadata:
    major_brand     : iso5
    minor_version   : 1
    compatible_brands: avc1iso5dsmsmsixdash
    encoder         : Lavf57.71.100
    description     : Packed by Bilibili XCoder v2.0.2
  Duration: 00:34:15.34, start: 0.067000, bitrate: 155 kb/s
  Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 512x384 [SAR 1:1 DAR 4:3], 0 kb/s, 15 fps, 15 tbr, 16k tbn (default)
    Metadata:
      handler_name    : VideoHandler
      vendor_id       : [0][0][0][0]
Input #1, mov,mp4,m4a,3gp,3g2,mj2, from './audio_temp.m4s':
  Metadata:
    major_brand     : iso5
    minor_version   : 1
    compatible_brands: avc1iso5dsmsmsixdash
    encoder         : Lavf57.71.100
    description     : Packed by Bilibili XCoder v2.0.2
  Duration: 00:34:15.64, start: 0.000000, bitrate: 134 kb/s
  Stream #1:0[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 0 kb/s (default)
    Metadata:
      handler_name    : SoundHandler
      vendor_id       : [0][0][0][0]
Output #0, mp4, to './字幕君交流场所 - BV1xx411c7mD(P1).mp4':
  Metadata:
    major_brand     : iso5
    minor_version   : 1
    compatible_brands: avc1iso5dsmsmsixdash
    description     : Packed by Bilibili XCoder v2.0.2
    encoder         : Lavf59.16.100
  Stream #0:0(und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 512x384 [SAR 1:1 DAR 4:3], q=2-31, 0 kb/s, 15 fps, 15 tbr, 16k tbn (default)
    Metadata:
      handler_name    : VideoHandler
      vendor_id       : [0][0][0][0]
  Stream #0:1(und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 0 kb/s (default)
    Metadata:
      handler_name    : SoundHandler
      vendor_id       : [0][0][0][0]
Stream mapping:
  Stream #0:0 -> #0:0 (copy)
  Stream #1:0 -> #0:1 (copy)
Press [q] to stop, [?] for help
frame=    1 fps=0.0 q=-1.0 size=       0kB time=00:00:00.00 bitrate=N/A speed=  frame=30829 fps=0.0 q=-1.0 Lsize=   73116kB time=00:34:15.63 bitrate= 291.4kbits/s speed=1.25e+04x    
video:38686kB audio:33148kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 1.784769%
INF: 混流完成(或用户手动取消)
INF: ---完成分 P---
Y/N: 此资源支持下载弹幕, 是否下载: [Enter]
INF: 开始下载弹幕(P1) 字幕君交流场所
INF: 下载弹幕完成
----------完成下载----------


BiliDown 下载完成
共 1 项, 成功 1 项, 失败 0 项, 不支持 0 项
./字幕君交流场所 - BV1xx411c7mD(P1).mp4
./字幕君交流场所 - BV1xx411c7mD(P1).ass
```

</details>

---

当你想要抓取番剧所有的视频弹幕的时候，可以这么做: 

```
bilidown "https://www.bilibili.com/bangumi/play/ss33626" --danmakus-settings only --download-list --dic danmakus
```

`--danmakus-settings only` 可以只抓取弹幕，跳过视频的下载

`--download-list` 可以下载番剧全部剧集(或课程全部课时 & 视频所有分 P)

`--dic danmakus` 可以将所有输出放在 `danmakus` 文件夹中以便整理

<details>
<summary> 输出: </summary>

```

                                         _____
________   ___   ___        ___          |   |
|\   __  \ |\  \ |\  \      |\  \        |   |
\ \  \|\ /_\ \  \\ \  \     \ \  \       |   |
 \ \   __  \\ \  \\ \  \     \ \  \    --     --
  \ \  \|\  \\ \  \\ \  \____ \ \  \   \       /
   \ \_______\\ \__\\ \_______\\ \__\   \     /
    \|_______| \|__| \|_______| \|__|    \   /
                                          \_/

BiliDown: 哔哩哔哩命令行下载器
Powered by Bilibili API
By Nemo2011<yimoxia@outlook.com>
使用 -h 获取帮助。

INF: 已开启下载全部列表的模式
INF: 识别到弹幕下载设置为 only
INF: 识别到文件输出地址为  danmakus
----------开始下载----------

INF: 链接 -> https://www.bilibili.com/bangumi/play/ss33626
INF: 正在获取链接信息
INF: 解析结果：番剧剧集

----------完成下载----------
INF: 番剧 media_id 28229055
INF: 番剧共 84 集

INF: 开始下载弹幕 三国演义：第1集 桃园三结义
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第2集 十常侍乱政
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第3集 董卓霸京师
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第4集 孟德献刀
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第5集 三英战吕布
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第6集 连环计
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第7集 凤仪亭
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第8集 三让徐州
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第9集 孙策立业
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第10集 辕门射戟
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第11集 宛城之战
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第12集 白门楼（上）
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第13集 白门楼（下）
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第14集 煮酒论英雄
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第15集 袁曹起兵
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第16集 关羽约三事
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第17集 挂印封金
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第18集 千里走单骑
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第19集 古城相会
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第20集 孙策之死
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第21集 官渡之战（上）
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第22集 官渡之战（下）
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第23集 大破袁绍
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第24集 跃马檀溪
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第25集 刘备求贤
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第26集 回马荐诸葛
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第27集 三顾茅庐
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第28集 火烧博望坡
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第29集 携民渡江
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第30集 舌战群儒
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第31集 智激周瑜
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第32集 周瑜空设计
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第33集 群英会
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第34集 草船借箭
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第35集 苦肉计
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第36集 庞统献连环
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第37集 横槊赋诗
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第38集 诸葛祭风
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第39集 火烧赤壁
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第40集 智取南郡
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第41集 力夺四郡
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第42集 美人计
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第43集 甘露寺
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第44集 回荆州
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第45集 三气周瑜
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第46集 卧龙吊孝
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第47集 割须弃袍
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第48集 张松献图
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第49集 刘备入川
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第50集 凤雏落坡
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第51集 义释严颜
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第52集 夺占西川
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第53集 单刀赴会
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第54集 合肥会战
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第55集 立嗣之争
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第56集 定军山
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第57集 巧取汉中
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第58集 水淹七军
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第59集 走麦城
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第60集 曹操之死
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第61集 曹丕篡汉
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第62集 兴兵伐吴
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第63集 火烧连营
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第64集 安居平五路
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第65集 兵渡泸水
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第66集 绝路问津
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第67集 七擒孟获
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第68集 出师北伐
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第69集 收姜维
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第70集 司马复出
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第71集 空城退敌
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第72集 司马取印
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第73集 祁山斗智
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第74集 诸葛妆神
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第75集 六出祁山
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第76集 火熄上方谷
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第77集 秋风五丈原
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第78集 诈病赚曹爽
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第79集 吴宫干戈
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第80集 兵困铁笼山
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第81集 司马昭弑君
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第82集 九伐中原
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第83集 偷渡阴平
INF: 下载弹幕完成

INF: 开始下载弹幕 三国演义：第84集 三分归晋
INF: 下载弹幕完成

----------完成下载----------


BiliDown 下载完成
共 1 项, 成功 1 项, 失败 0 项, 不支持 0 项
danmakus/三国演义：第1集 桃园三结义 - 番剧 EP327584(三国演义).ass
danmakus/三国演义：第2集 十常侍乱政 - 番剧 EP327585(三国演义).ass
danmakus/三国演义：第3集 董卓霸京师 - 番剧 EP327586(三国演义).ass
danmakus/三国演义：第4集 孟德献刀 - 番剧 EP327587(三国演义).ass
danmakus/三国演义：第5集 三英战吕布 - 番剧 EP327588(三国演义).ass
danmakus/三国演义：第6集 连环计 - 番剧 EP327589(三国演义).ass
danmakus/三国演义：第7集 凤仪亭 - 番剧 EP327590(三国演义).ass
danmakus/三国演义：第8集 三让徐州 - 番剧 EP327591(三国演义).ass
danmakus/三国演义：第9集 孙策立业 - 番剧 EP327592(三国演义).ass
danmakus/三国演义：第10集 辕门射戟 - 番剧 EP327593(三国演义).ass
danmakus/三国演义：第11集 宛城之战 - 番剧 EP327597(三国演义).ass
danmakus/三国演义：第12集 白门楼（上） - 番剧 EP327598(三国演义).ass
danmakus/三国演义：第13集 白门楼（下） - 番剧 EP327599(三国演义).ass
danmakus/三国演义：第14集 煮酒论英雄 - 番剧 EP327600(三国演义).ass
danmakus/三国演义：第15集 袁曹起兵 - 番剧 EP327601(三国演义).ass
danmakus/三国演义：第16集 关羽约三事 - 番剧 EP327602(三国演义).ass
danmakus/三国演义：第17集 挂印封金 - 番剧 EP327603(三国演义).ass
danmakus/三国演义：第18集 千里走单骑 - 番剧 EP327607(三国演义).ass
danmakus/三国演义：第19集 古城相会 - 番剧 EP327610(三国演义).ass
danmakus/三国演义：第20集 孙策之死 - 番剧 EP327612(三国演义).ass
danmakus/三国演义：第21集 官渡之战（上） - 番剧 EP327624(三国演义).ass
danmakus/三国演义：第22集 官渡之战（下） - 番剧 EP327625(三国演义).ass
danmakus/三国演义：第23集 大破袁绍 - 番剧 EP327627(三国演义).ass
danmakus/三国演义：第24集 跃马檀溪 - 番剧 EP327628(三国演义).ass
danmakus/三国演义：第25集 刘备求贤 - 番剧 EP327629(三国演义).ass
danmakus/三国演义：第26集 回马荐诸葛 - 番剧 EP327630(三国演义).ass
danmakus/三国演义：第27集 三顾茅庐 - 番剧 EP327631(三国演义).ass
danmakus/三国演义：第28集 火烧博望坡 - 番剧 EP327633(三国演义).ass
danmakus/三国演义：第29集 携民渡江 - 番剧 EP327637(三国演义).ass
danmakus/三国演义：第30集 舌战群儒 - 番剧 EP327638(三国演义).ass
danmakus/三国演义：第31集 智激周瑜 - 番剧 EP327639(三国演义).ass
danmakus/三国演义：第32集 周瑜空设计 - 番剧 EP327640(三国演义).ass
danmakus/三国演义：第33集 群英会 - 番剧 EP327641(三国演义).ass
danmakus/三国演义：第34集 草船借箭 - 番剧 EP327642(三国演义).ass
danmakus/三国演义：第35集 苦肉计 - 番剧 EP327643(三国演义).ass
danmakus/三国演义：第36集 庞统献连环 - 番剧 EP327644(三国演义).ass
danmakus/三国演义：第37集 横槊赋诗 - 番剧 EP327645(三国演义).ass
danmakus/三国演义：第38集 诸葛祭风 - 番剧 EP327646(三国演义).ass
danmakus/三国演义：第39集 火烧赤壁 - 番剧 EP327647(三国演义).ass
danmakus/三国演义：第40集 智取南郡 - 番剧 EP327648(三国演义).ass
danmakus/三国演义：第41集 力夺四郡 - 番剧 EP327649(三国演义).ass
danmakus/三国演义：第42集 美人计 - 番剧 EP327650(三国演义).ass
danmakus/三国演义：第43集 甘露寺 - 番剧 EP327658(三国演义).ass
danmakus/三国演义：第44集 回荆州 - 番剧 EP327659(三国演义).ass
danmakus/三国演义：第45集 三气周瑜 - 番剧 EP327671(三国演义).ass
danmakus/三国演义：第46集 卧龙吊孝 - 番剧 EP327672(三国演义).ass
danmakus/三国演义：第47集 割须弃袍 - 番剧 EP327673(三国演义).ass
danmakus/三国演义：第48集 张松献图 - 番剧 EP327675(三国演义).ass
danmakus/三国演义：第49集 刘备入川 - 番剧 EP327677(三国演义).ass
danmakus/三国演义：第50集 凤雏落坡 - 番剧 EP327679(三国演义).ass
danmakus/三国演义：第51集 义释严颜 - 番剧 EP327680(三国演义).ass
danmakus/三国演义：第52集 夺占西川 - 番剧 EP327681(三国演义).ass
danmakus/三国演义：第53集 单刀赴会 - 番剧 EP327688(三国演义).ass
danmakus/三国演义：第54集 合肥会战 - 番剧 EP327690(三国演义).ass
danmakus/三国演义：第55集 立嗣之争 - 番剧 EP327691(三国演义).ass
danmakus/三国演义：第56集 定军山 - 番剧 EP327692(三国演义).ass
danmakus/三国演义：第57集 巧取汉中 - 番剧 EP327747(三国演义).ass
danmakus/三国演义：第58集 水淹七军 - 番剧 EP327748(三国演义).ass
danmakus/三国演义：第59集 走麦城 - 番剧 EP327749(三国演义).ass
danmakus/三国演义：第60集 曹操之死 - 番剧 EP327750(三国演义).ass
danmakus/三国演义：第61集 曹丕篡汉 - 番剧 EP327751(三国演义).ass
danmakus/三国演义：第62集 兴兵伐吴 - 番剧 EP327752(三国演义).ass
danmakus/三国演义：第63集 火烧连营 - 番剧 EP327753(三国演义).ass
danmakus/三国演义：第64集 安居平五路 - 番剧 EP327754(三国演义).ass
danmakus/三国演义：第65集 兵渡泸水 - 番剧 EP327755(三国演义).ass
danmakus/三国演义：第66集 绝路问津 - 番剧 EP327757(三国演义).ass
danmakus/三国演义：第67集 七擒孟获 - 番剧 EP327758(三国演义).ass
danmakus/三国演义：第68集 出师北伐 - 番剧 EP327761(三国演义).ass
danmakus/三国演义：第69集 收姜维 - 番剧 EP327765(三国演义).ass
danmakus/三国演义：第70集 司马复出 - 番剧 EP327768(三国演义).ass
danmakus/三国演义：第71集 空城退敌 - 番剧 EP327769(三国演义).ass
danmakus/三国演义：第72集 司马取印 - 番剧 EP327770(三国演义).ass
danmakus/三国演义：第73集 祁山斗智 - 番剧 EP327771(三国演义).ass
danmakus/三国演义：第74集 诸葛妆神 - 番剧 EP327772(三国演义).ass
danmakus/三国演义：第75集 六出祁山 - 番剧 EP327773(三国演义).ass
danmakus/三国演义：第76集 火熄上方谷 - 番剧 EP327774(三国演义).ass
danmakus/三国演义：第77集 秋风五丈原 - 番剧 EP327775(三国演义).ass
danmakus/三国演义：第78集 诈病赚曹爽 - 番剧 EP327776(三国演义).ass
danmakus/三国演义：第79集 吴宫干戈 - 番剧 EP327777(三国演义).ass
danmakus/三国演义：第80集 兵困铁笼山 - 番剧 EP327779(三国演义).ass
danmakus/三国演义：第81集 司马昭弑君 - 番剧 EP327780(三国演义).ass
danmakus/三国演义：第82集 九伐中原 - 番剧 EP327781(三国演义).ass
danmakus/三国演义：第83集 偷渡阴平 - 番剧 EP327782(三国演义).ass
danmakus/三国演义：第84集 三分归晋 - 番剧 EP327783(三国演义).ass
```

</details>


---


没事下载直播...

```
bilidown "https://live.bilibili.com/24075835" --out "直播 {live_id}.mp4"
```

**MacOS & Linux 建议加上 `sudo` 运行**

`--out "直播 {live_id}.mp4"` 提供了文件输出名, 这里的 `{live_id}` 为转义块, `BiliDown` 会自动把 `{live_id}` 替换成直播间房号(`24075835`)

<details>
<summary> 输出: </summary>

```

                                         _____
________   ___   ___        ___          |   |
|\   __  \ |\  \ |\  \      |\  \        |   |
\ \  \|\ /_\ \  \\ \  \     \ \  \       |   |
 \ \   __  \\ \  \\ \  \     \ \  \    --     --
  \ \  \|\  \\ \  \\ \  \____ \ \  \   \       /
   \ \_______\\ \__\\ \_______\\ \__\   \     /
    \|_______| \|__| \|_______| \|__|    \   /
                                          \_/

BiliDown: 哔哩哔哩命令行下载器
Powered by Bilibili API
By Nemo2011<yimoxia@outlook.com>
使用 -h 获取帮助。

INF: 识别到文件名为  直播 {live_id}.mp4
----------开始下载----------

INF: 链接 -> https://live.bilibili.com/24075835
INF: 正在获取链接信息
INF: 解析结果：直播间

直播间房号: 24075835
如果想要停止下载请长按 ESC 键
^[DWN: 35s. 接收到数据 12255232B
WRN: 用户手动停止
INF: 正在转换格式
ffmpeg version 5.0.1 Copyright (c) 2000-2022 the FFmpeg developers
  built with Apple clang version 13.1.6 (clang-1316.0.21.2.5)
  configuration: --prefix=/opt/homebrew/Cellar/ffmpeg/5.0.1_3 --enable-shared --enable-pthreads --enable-version3 --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libbluray --enable-libdav1d --enable-libmp3lame --enable-libopus --enable-librav1e --enable-librist --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvmaf --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libspeex --enable-libsoxr --enable-libzmq --enable-libzimg --disable-libjack --disable-indev=jack --enable-videotoolbox --enable-neon
  libavutil      57. 17.100 / 57. 17.100
  libavcodec     59. 18.100 / 59. 18.100
  libavformat    59. 16.100 / 59. 16.100
  libavdevice    59.  4.100 / 59.  4.100
  libavfilter     8. 24.100 /  8. 24.100
  libswscale      6.  4.100 /  6.  4.100
  libswresample   4.  3.100 /  4.  3.100
  libpostproc    56.  3.100 / 56.  3.100
[flv @ 0x127f04280] Estimating duration from bitrate, this may be inaccurate
Input #0, flv, from './直播 24075835.flv':
  Metadata:
    Rawdata         : 
    displayWidth    : 1920
    displayHeight   : 1080
    fps             : 30
    profile         : 
    level           : 
    encoder         : obs-output module (libobs version 27.2.1)
    server          : BSRS/1.4.4(Sco)
    server_version  : 1.4.4
  Duration: 00:01:07.22, start: 0.022000, bitrate: 2721 kb/s
  Stream #0:0: Video: h264 (High), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], 2560 kb/s, 30 fps, 30 tbr, 1k tbn
  Stream #0:1: Audio: aac (LC), 48000 Hz, stereo, fltp, 163 kb/s
Stream mapping:
  Stream #0:0 -> #0:0 (h264 (native) -> h264 (libx264))
  Stream #0:1 -> #0:1 (aac (native) -> aac (native))
Press [q] to stop, [?] for help
[libx264 @ 0x107f04b40] using SAR=1/1
[libx264 @ 0x107f04b40] using cpu capabilities: ARMv8 NEON
[libx264 @ 0x107f04b40] profile High, level 4.0, 4:2:0, 8-bit
[libx264 @ 0x107f04b40] 264 - core 164 r3095 baee400 - H.264/MPEG-4 AVC codec - Copyleft 2003-2022 - http://www.videolan.org/x264.html - options: cabac=1 ref=3 deblock=1:0:0 analyse=0x3:0x113 me=hex subme=7 psy=1 psy_rd=1.00:0.00 mixed_ref=1 me_range=16 chroma_me=1 trellis=1 8x8dct=1 cqm=0 deadzone=21,11 fast_pskip=1 chroma_qp_offset=-2 threads=12 lookahead_threads=2 sliced_threads=0 nr=0 decimate=1 interlaced=0 bluray_compat=0 constrained_intra=0 bframes=3 b_pyramid=2 b_adapt=1 b_bias=0 direct=1 weightb=1 open_gop=0 weightp=2 keyint=250 keyint_min=25 scenecut=40 intra_refresh=0 rc_lookahead=40 rc=crf mbtree=1 crf=23.0 qcomp=0.60 qpmin=0 qpmax=69 qpstep=4 ip_ratio=1.40 aq=1:1.00
Output #0, mp4, to './直播 24075835.mp4':
  Metadata:
    Rawdata         : 
    displayWidth    : 1920
    displayHeight   : 1080
    fps             : 30
    profile         : 
    level           : 
    server_version  : 1.4.4
    server          : BSRS/1.4.4(Sco)
    encoder         : Lavf59.16.100
  Stream #0:0: Video: h264 (avc1 / 0x31637661), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], q=2-31, 30 fps, 15360 tbn
    Metadata:
      encoder         : Lavc59.18.100 libx264
    Side data:
      cpb: bitrate max/min/avg: 0/0/0 buffer size: 0 vbv_delay: N/A
  Stream #0:1: Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 128 kb/s
    Metadata:
      encoder         : Lavc59.18.100 aac
[flv @ 0x127f04280] Packet mismatch -2068792204 18115 10614002trate=2529.1kbits/s dup=2 drop=0 speed=4.43x    
[flv @ 0x127f04280] Concatenated FLV detected, might fail to demux, decode and seek 31830
[flv @ 0x127f04280] Packet corrupt (stream = 0, dts = 68405).itrate=2335.7kbits/s dup=2 drop=0 speed=4.63x    
[NULL @ 0x127f048e0] Invalid NAL unit size (20766 > 19534).
[NULL @ 0x127f048e0] missing picture in access unit with size 19550
./直播 24075835.flv: corrupt input packet in stream 0
[h264 @ 0x127e06460] Invalid NAL unit size (20766 > 19534).
[h264 @ 0x127e06460] Error splitting the input into NAL units.
Error while decoding stream #0:0: Invalid data found when processing input
frame= 2054 fps=136 q=-1.0 Lsize=   20308kB time=00:01:08.38 bitrate=2432.7kbits/s dup=2 drop=0 speed=4.54x    
video:19121kB audio:1090kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.484419%
[libx264 @ 0x107f04b40] frame I:9     Avg QP:15.81  size:212624
[libx264 @ 0x107f04b40] frame P:656   Avg QP:22.47  size: 18295
[libx264 @ 0x107f04b40] frame B:1389  Avg QP:32.49  size:  4078
[libx264 @ 0x107f04b40] consecutive B-frames:  1.2% 12.2% 41.5% 45.2%
[libx264 @ 0x107f04b40] mb I  I16..4: 24.1% 30.9% 45.0%
[libx264 @ 0x107f04b40] mb P  I16..4:  0.3%  0.4%  0.4%  P16..4:  9.3%  4.6%  3.5%  0.0%  0.0%    skip:81.4%
[libx264 @ 0x107f04b40] mb B  I16..4:  0.0%  0.0%  0.0%  B16..8:  8.3%  2.3%  1.0%  direct: 0.5%  skip:87.9%  L0:41.1% L1:49.6% BI: 9.3%
[libx264 @ 0x107f04b40] 8x8 transform intra:33.6% inter:39.7%
[libx264 @ 0x107f04b40] coded y,uvDC,uvAC intra: 47.5% 67.4% 52.9% inter: 3.1% 3.1% 1.4%
[libx264 @ 0x107f04b40] i16 v,h,dc,p: 41% 41% 10%  8%
[libx264 @ 0x107f04b40] i8 v,h,dc,ddl,ddr,vr,hd,vl,hu: 17% 20% 37%  4%  4%  3%  5%  3%  6%
[libx264 @ 0x107f04b40] i4 v,h,dc,ddl,ddr,vr,hd,vl,hu: 21% 26% 18%  5%  7%  6%  6%  6%  6%
[libx264 @ 0x107f04b40] i8c dc,h,v,p: 44% 33% 17%  6%
[libx264 @ 0x107f04b40] Weighted P-Frames: Y:0.0% UV:0.0%
[libx264 @ 0x107f04b40] ref P L0: 68.7% 10.8% 14.8%  5.7%
[libx264 @ 0x107f04b40] ref B L0: 81.1% 16.8%  2.1%
[libx264 @ 0x107f04b40] ref B L1: 96.1%  3.9%
[libx264 @ 0x107f04b40] kb/s:2287.72
[aac @ 0x107f060f0] Qavg: 525.499
----------完成下载----------


BiliDown 下载完成
共 1 项, 成功 1 项, 失败 0 项, 不支持 0 项
./直播 24075835.mp4
```

</details>

最后的输出文件名是: `./直播 24075835.mp4`

有关其他的转义块，请使用 `bilidown -h` 查看详情

---

如果外部程序想要调用 `BiliDown` 怎么办？最主要的问题就是 `BiliDown` 许多的选择需要用户自己输入, 所以 `BiliDown` 提供了 `--default-settings` 参数

使用 `--default-settings` 参数后, `BiliDown` 会使用用户的设置进行下载

还是 `字幕君交流场所`, 我们来试一下加上 `--default-settings` 参数: 

```
bilidown av2 --default-settings "16|hev|30216"
```

这里我们设置了下载使用的设置: `16 | hev | 30216`

他们分别对应 `视频分辨率 | 视频编码 | 音频音质`, 这里使用了一种编码, 编码对应的实际含义请使用 `bilidown -h` 查看详情

其实这里没有填完整设置, 完整设置为 `视频分辨率 | 视频编码 | 音频音质 | 专栏下载格式 | 用户空间下载资源类型`

## License

GNU General Public License version 3.0
