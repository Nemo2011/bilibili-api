bilibili_api
=

# V2版本正在开发中，开发进度 <https://github.com/Passkou/bilibili_api/projects/1>
本项目地址：

<https://github.com/Passkou/bilibili_api>

本模块可调用 [哔哩哔哩](https://www.bilibili.com) （下称b站）的API，使用这些API可对视频、动态等进行一系列的操作，详细功能请见帮助文档。

我的个人网站：[喵帕斯小窝](https://passkou.com)

API列表 [点我](https://github.com/Passkou/bilibili_api/blob/master/bilibili_api/src/api.json)

开发文档及所有功能请见 [Wiki](https://github.com/Passkou/bilibili_api/wiki)

安装方法
-
本模块用到的第三方库： 

+ requests

仅支持 **Python3**，使用以下代码安装本模块  

```cmd
pip install bilibili_api
```

然后，使用以下代码导入本模块

```python
import bilibili_api
```
    
快速开始
-
以获取视频 [av40473736](https://www.bilibili.com/av40473736) 信息为例

首先，我们要导入 `video` 模块和 [Verify](https://github.com/Passkou/bilibili_api/wiki/Verify%E7%B1%BB) 验证类：

```python
from bilibili_api import video, Verify
```

该模块有三个类，分别是 [VideoInfo](https://github.com/Passkou/bilibili_api/wiki/VideoInfo%E7%B1%BB) 和
[VideoOperate](https://github.com/Passkou/bilibili_api/wiki/VideoOperate%E7%B1%BB)，前者用于获取视频信息，后者用于操作视频（点赞、投币等）。
还有一个 [Danmaku](https://github.com/Passkou/bilibili_api/wiki/Danmaku%E7%B1%BB) 类，用于获取弹幕和发送弹幕。

然后我们使用以下代码初始化这个类：

```python
verify = Verify(sessdata="your sessdata", csrf="your csrf")
my_video = video.VideoInfo(aid="40473736", verify=verify)
```

对于 [Verify](https://github.com/Passkou/bilibili_api/wiki/Verify%E7%B1%BB) 类，可用可不用。

但是，部分视频信息需要登录（即需要 SESSDATA ）后才能使用（如历史弹幕获取）。

对视频进行点赞、投币等用户操作则需要 SESSDATA 和 csrf 。

关于 SESSDATA 和 csrf 获取的详细方法，[点我](https://github.com/Passkou/bilibili_api/wiki/SESSDATA%E5%92%8CCSRF%E8%8E%B7%E5%8F%96%E6%96%B9%E6%B3%95%EF%BC%88Chrome%E4%B8%BA%E4%BE%8B%EF%BC%89)

接下来我们获取视频的详细信息：

```python
video_info = my_video.get_video_info()
print(video_info)
```
    
完整代码：

```python
from bilibili_api import video, Verify
import json

# 设置验证
verify = Verify(sessdata="your sessdata", csrf="your csrf")

# 初始化VideoInfo类
my_video = video.VideoInfo(aid="40473736", verify=verify)

# 获取视频信息
video_info = my_video.get_video_info()

# 转换成格式化JSON并打印
print(json.dumps(video_info, indent=4, ensure_ascii=False))
```

会得到类似下面的返回值（返回的是Python对象，为方便阅读已转换为JSON）：

```json
{
	"bvid": "",
	"aid": 40473736,
	"videos": 2,
	"tid": 22,
	"tname": "鬼畜调教",
	"copyright": 1,
	"pic": "http://i1.hdslb.com/bfs/archive/0d2c12f55f6e54bb0e7bcb2e093d000208bca860.jpg",
	"title": "轮到日向给你洗脑啦！（天使降临到我身边）",
	"pubdate": 1547204664,
	"ctime": 1547204664,
	"desc": "番剧名：天使降临到我身边\nBGM：天国と地獄\nみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやねみやね\n一集都给你做成鬼畜233",
	"state": 0,
	"attribute": 16512,
	"duration": 222,
	"rights": {
		"bp": 0,
		"elec": 0,
		"download": 1,
		"movie": 0,
		"pay": 0,
		"hd5": 0,
		"no_reprint": 1,
		"autoplay": 1,
		"ugc_pay": 0,
		"is_cooperation": 0,
		"ugc_pay_preview": 0,
		"no_background": 0
	},
	"owner": {
		"mid": 12440199,
		"name": "Passkou",
		"face": "http://i2.hdslb.com/bfs/face/0ad5abd97cb8f4575fbdfca847211f7df0f49cdb.jpg"
	},
	"stat": {
		"aid": 40473736,
		"view": 155513,
		"danmaku": 345,
		"reply": 439,
		"favorite": 3872,
		"coin": 2611,
		"share": 549,
		"now_rank": 0,
		"his_rank": 0,
		"like": 4550,
		"dislike": 0,
		"evaluation": ""
	},
	"dynamic": "#洗脑循环##天使降临到我身边##丧心病狂#",
	"cid": 71085394,
	"dimension": {
		"width": 1920,
		"height": 1080,
		"rotate": 0
	},
	"no_cache": false,
	"pages": [
		{
			"cid": 71085394,
			"page": 1,
			"from": "vupload",
			"part": "轮到日向给你洗脑啦！",
			"duration": 109,
			"vid": "",
			"weblink": "",
			"dimension": {
				"width": 1920,
				"height": 1080,
				"rotate": 0
			}
		},
		{
			"cid": 71206420,
			"page": 2,
			"from": "vupload",
			"part": "FL工程",
			"duration": 113,
			"vid": "",
			"weblink": "",
			"dimension": {
				"width": 1920,
				"height": 1080,
				"rotate": 0
			}
		}
	],
	"subtitle": {
		"allow_submit": false,
		"list": []
	}
}
```
    
接下来，就可以根据自己的实际需求对数据进行处理了。~~懒得写了.jpg~~
 
更详细的教程请见 [Wiki](https://github.com/Passkou/bilibili_api/wiki)

[更新日志](https://github.com/Passkou/bilibili_api/blob/master/changelog.md)
