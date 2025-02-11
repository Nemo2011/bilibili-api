# Module interactive_video.py


bilibili_api.interactive_video

互动视频相关操作


``` python
from bilibili_api import interactive_video
```

- [class InteractiveButton()](#class-InteractiveButton)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def get\_align()](#def-get\_align)
  - [def get\_pos()](#def-get\_pos)
  - [def get\_text()](#def-get\_text)
- [class InteractiveButtonAlign()](#class-InteractiveButtonAlign)
- [class InteractiveGraph()](#class-InteractiveGraph)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_children()](#async-def-get\_children)
  - [async def get\_root\_node()](#async-def-get\_root\_node)
  - [def get\_skin()](#def-get\_skin)
  - [def get\_video()](#def-get\_video)
- [class InteractiveJumpingCommand()](#class-InteractiveJumpingCommand)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def get\_command()](#def-get\_command)
  - [def get\_vars()](#def-get\_vars)
  - [def run\_command()](#def-run\_command)
- [class InteractiveJumpingCondition()](#class-InteractiveJumpingCondition)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def get\_condition()](#def-get\_condition)
  - [def get\_result()](#def-get\_result)
  - [def get\_vars()](#def-get\_vars)
- [class InteractiveNode()](#class-InteractiveNode)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_children()](#async-def-get\_children)
  - [def get\_cid()](#def-get\_cid)
  - [async def get\_info()](#async-def-get\_info)
  - [def get\_jumping\_command()](#def-get\_jumping\_command)
  - [def get\_jumping\_condition()](#def-get\_jumping\_condition)
  - [async def get\_jumping\_type()](#async-def-get\_jumping\_type)
  - [def get\_node\_id()](#def-get\_node\_id)
  - [def get\_self\_button()](#def-get\_self\_button)
  - [def get\_vars()](#def-get\_vars)
  - [def get\_video()](#def-get\_video)
  - [def is\_default()](#def-is\_default)
- [class InteractiveNodeJumpingType()](#class-InteractiveNodeJumpingType)
- [class InteractiveVariable()](#class-InteractiveVariable)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def get\_id()](#def-get\_id)
  - [def get\_name()](#def-get\_name)
  - [def get\_value()](#def-get\_value)
  - [def is\_random()](#def-is\_random)
  - [def is\_show()](#def-is\_show)
  - [def refresh\_value()](#def-refresh\_value)
- [class InteractiveVideo()](#class-InteractiveVideo)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_cid()](#async-def-get\_cid)
  - [async def get\_edge\_info()](#async-def-get\_edge\_info)
  - [async def get\_graph()](#async-def-get\_graph)
  - [async def get\_graph\_version()](#async-def-get\_graph\_version)
  - [async def mark\_score()](#async-def-mark\_score)
  - [async def up\_get\_ivideo\_pages()](#async-def-up\_get\_ivideo\_pages)
  - [async def up\_submit\_story\_tree()](#async-def-up\_submit\_story\_tree)
- [class InteractiveVideoDownloader()](#class-InteractiveVideoDownloader)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def abort()](#async-def-abort)
  - [async def start()](#async-def-start)
- [class InteractiveVideoDownloaderEvents()](#class-InteractiveVideoDownloaderEvents)
- [class InteractiveVideoDownloaderMode()](#class-InteractiveVideoDownloaderMode)
- [def get\_ivi\_file\_meta()](#def-get\_ivi\_file\_meta)

---

## class InteractiveButton()

互动视频节点按钮类




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `text` | `str` | 文字 |
| `x` | `int` | x 轴 |
| `y` | `int` | y 轴 |
| `align` | `InteractiveButtonAlign \| int` | 按钮的文字在按钮中的位置 |


### def get_align()

获取按钮文字布局



**Returns:** `int`:  按钮文字布局




### def get_pos()

获取按钮位置



**Returns:** `Tuple[int, int]`:  按钮位置




### def get_text()

获取按钮文字



**Returns:** `str`:  按钮文字




---

## class InteractiveButtonAlign()

**Extend: enum.Enum**

按钮的文字在按钮中的位置


``` text
-----
|xxx|----o (TEXT_LEFT)
-----

 -----
o----|xxx| (TEXT_RIGHT)
 -----

----------
|XXXXXXXX| (DEFAULT)
----------
```

- DEFAULT
- TEXT_UP
- TEXT_RIGHT
- TEXT_DOWN
- TEXT_LEFT




---

## class InteractiveGraph()

情节树类




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `video` | `InteractiveVideo` | 互动视频类 |
| `skin` | `Dict` | 样式 |
| `root_cid` | `int` | 根节点 CID |


### async def get_children()

获取子节点



**Returns:** `List[InteractiveNode]`:  子节点




### async def get_root_node()

获取根节点



**Returns:** `InteractiveNode`:  根节点




### def get_skin()

获取按钮样式



**Returns:** `dict`:  按钮样式




### def get_video()

获取视频



**Returns:** `InteractiveVideo`:  视频




---

## class InteractiveJumpingCommand()

节点跳转对变量的操作




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `var` | `List[InteractiveVariable]` | 所有变量 |
| `command` | `str` | 公式 |


### def get_command()

获取表达式



**Returns:** `str`:  表达式




### def get_vars()

获取公式中的变量



**Returns:** `List[InteractiveVariable]`:  变量




### def run_command()

执行操作



**Returns:** `List[InteractiveVariable]`:  所有变量的最终值




---

## class InteractiveJumpingCondition()

节点跳转的公式，只有公式成立才会跳转




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `var` | `List[InteractiveVariable]` | 所有变量 |
| `condition` | `str` | 公式 |


### def get_condition()

获取表达式



**Returns:** `str`:  表达式




### def get_result()

计算公式获得结果



**Returns:** `bool`:  是否成立




### def get_vars()

获取公式中的变量



**Returns:** `List[InteractiveVariable]`:  变量




---

## class InteractiveNode()

互动视频节点类




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `video` | `InteractiveVideo` | 视频类 |
| `node_id` | `int` | 节点 id |
| `cid` | `int` | CID |
| `vars` | `List[InteractiveVariable]` | 变量 |
| `button` | `InteractiveButton` | 对应的按钮 |
| `condition` | `InteractiveJumpingCondition` | 跳转公式 |
| `native_command` | `InteractiveJumpingCommand` | 跳转时变量操作 |
| `is_default` | `bool` | 是不是默认的跳转的节点 |


### async def get_children()

获取节点的所有子节点



**Returns:** `List[InteractiveNode]`:  所有子节点




### def get_cid()

获取节点 cid



**Returns:** `int`:  节点 cid




### async def get_info()

获取节点的简介



**Returns:** `dict`:  调用 API 返回的结果




### def get_jumping_command()

获取跳转时执行的语句，已自动执行，无需手动调用



**Returns:** `InteractiveJumpingCommand`:  执行的语句




### def get_jumping_condition()

获取跳转条件



**Returns:** `InteractiveJumpingCondition`:  跳转条件




### async def get_jumping_type()

获取子节点跳转方式 (参考 InteractiveNodeJumpingType)






### def get_node_id()

获取节点 id



**Returns:** `int`:  节点 id




### def get_self_button()

获取该节点所对应的按钮



**Returns:** `InteractiveButton`:  所对应的按钮




### def get_vars()

获取节点的所有变量



**Returns:** `List[InteractiveVariable]`:  节点的所有变量




### def get_video()

获取节点对应视频



**Returns:** `InteractiveVideo`:  对应视频




### def is_default()

节点是否为跳转中默认节点



**Returns:** `bool`:  是否为跳转中默认节点




---

## class InteractiveNodeJumpingType()

**Extend: enum.Enum**

对下一节点的跳转的方式

- ASK: 选择
- DEFAULT: 跳转到默认节点
- READY  : 选择(只有一个选择)




---

## class InteractiveVariable()

互动节点的变量




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `name` | `str` | 变量名 |
| `var_id` | `str` | 变量 id |
| `var_value` | `int` | 变量的值 |
| `show` | `bool` | 是否显示 |
| `random` | `bool` | 是否为随机值(1-100) |


### def get_id()

获取变量 id



**Returns:** `str`:  变量 id




### def get_name()

获取变量的名字



**Returns:** `str`:  变量的名字




### def get_value()

获取变量对应的值



**Returns:** `int`:  变量对应的值




### def is_random()

变量是否随机生成



**Returns:** `bool`:  变量是否随机生成




### def is_show()

变量是否显示



**Returns:** `bool`:  变量是否显示




### def refresh_value()

刷新变量数值






---

## class InteractiveVideo()

**Extend: bilibili_api.video.Video**

互动视频类




### def \_\_init\_\_()





### async def get_cid()

获取稿件 cid






### async def get_edge_info()

获取剧情图节点信息


| name | type | description |
| - | - | - |
| `edge_id` | `int, optional` | 节点 ID，为 None 时获取根节点信息. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_graph()

获取稿件情节树



**Returns:** `InteractiveGraph`:  情节树




### async def get_graph_version()

获取剧情图版本号，仅供 `get_edge_info()` 使用。



**Returns:** `int`:  剧情图版本号




### async def mark_score()

为互动视频打分


| name | type | description |
| - | - | - |
| `score` | `int` | 互动视频分数. Defaults to 5. |

**Returns:** `dict`:  调用 API 返回的结果




### async def up_get_ivideo_pages()

获取交互视频的分 P 信息。up 主需要拥有视频所有权。



**Returns:** `dict`:  调用 API 返回的结果




### async def up_submit_story_tree()

上传交互视频的情节树。up 主需要拥有视频所有权。


| name | type | description |
| - | - | - |
| `story_tree` | `str` | 情节树的描述，参考 bilibili_storytree.StoryGraph, 需要 Serialize 这个结构 |

**Returns:** `dict`:  调用 API 返回的结果




---

## class InteractiveVideoDownloader()

**Extend: bilibili_api.utils.AsyncEvent.AsyncEvent**

互动视频下载类




### def \_\_init\_\_()

`self_download_func` 函数应接受两个参数（第一个是下载 URL，第二个是输出地址（精确至文件名））

为保证视频能被成功下载，请在自定义下载函数请求的时候加入 `bilibili_api.HEADERS` 头部。


| name | type | description |
| - | - | - |
| `video` | `InteractiveVideo` | 互动视频类 |
| `out` | `str` | 输出文件地址 (如果模式为 NODE_VIDEOS/NO_PACKAGING 则此参数表示所有节点视频的存放目录) |
| `self_download_func` | `Coroutine` | 自定义下载函数（需 async 函数）. Defaults to None. |
| `downloader_mode` | `InteractiveVideoDownloaderMode` | 下载模式 |
| `stream_detecting_params` | `Dict` | `VideoDownloadURLDataDetecter` 提取最佳流时传入的参数，可控制视频及音频品质 |
| `fetching_nodes_retry_times` | `int` | 获取节点时的最大重试次数 |


### async def abort()

中断下载






### async def start()

开始下载






---

## class InteractiveVideoDownloaderEvents()

**Extend: enum.Enum**

互动视频下载器事件枚举

| event | meaning | IVI mode | NODE_VIDEOS mode | DOT_GRAPH mode | NO_PACKAGING mode | Is Built-In downloader event |
| ----- | ------- | -------- | ---------------- | -------------- | ----------------- | ------------------------- |
| START | 开始下载 | [x] | [x] | [x] | [x] | [ ] |
| GET | 获取到节点信息 | [x] | [x] | [x] | [x] | [ ] |
| PREPARE_DOWNLOAD | 准备下载单个节点 | [x] | [x] | [ ] | [x] | [ ] |
| DOWNLOAD_START | 开始下载单个文件 | Unknown | Unknown | [ ] | Unknown | [x] |
| DOWNLOAD_PART | 文件分块部分完成 | Unknown | Unknown | [ ] | Unknown | [x] |
| DOWNLOAD_SUCCESS | 完成下载 | Unknown | Unknown | [ ] | Unknown | [x] |
| PACKAGING | 正在打包 | [x] | [ ] | [ ] | [ ] | [ ] |
| SUCCESS | 下载成功 | [x] | [x] | [x] | [x] | [ ] |
| ABORTED | 用户暂停 | [x] | [x] | [x] | [x] | [ ] |
| FAILED | 下载失败 | [x] | [x] | [x] | [x] | [ ] |




---

## class InteractiveVideoDownloaderMode()

**Extend: enum.Enum**

互动视频下载模式

- IVI: 下载可播放的 ivi 文件
- NODE_VIDEOS: 下载所有节点的所有视频并存放在某个文件夹，每一个节点的视频命名为 `{节点 id} {节点标题 (自动去除敏感字符)}.mp4`
- DOT_GRAPH: 下载 dot 格式的情节树图表
- NO_PACKAGING: 前面按照 ivi 文件下载步骤进行下载，但是最终不会打包成为 ivi 文件，所有文件将存放于一个文件夹中。互动视频数据将存放在一个文件夹中，里面的文件命名/含义与拆包后的 ivi 文件完全相同。




---

## def get_ivi_file_meta()

获取 ivi 文件信息


| name | type | description |
| - | - | - |
| `path` | `str` | 文件地址 |

**Returns:** `dict`:  文件信息




