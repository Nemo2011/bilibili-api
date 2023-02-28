# Module interactive_video.py

```python
from bilibili_api import interactive_video
```

## class InteractiveVideo

**Extends: bilibili_api.video.Video**

互动视频类

### Attributes

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |

### Functions

**这里仅列出新增的或重写过的函数，Video 类的其他函数都可使用**

#### async def up_submit_story_tree()
| name       | type                 | description                                       |
| ---------- | -------------------- | ------------------------------------------------- |
| story_tree | str                  | 情节树的描述。参考 bilibili_storytree.StoryGraph  |
| credential | Credential           | Credential 类。up 主需要拥有交互视频              |

提交情节树。up 主需要拥有交互视频。

**Returns:** dict: 调用 API 返回的结果

#### async def up_get_ivideo_pages()
| name       | type                 | description                           |
| ---------- | -------------------- | ------------------------------------- |
| bvid       | str                  | BV 号。                               |
| credential | Credential           | Credential 类。up 主需要拥有交互视频  |

获取交互视频分 P。up 主需要拥有交互视频。

**Returns:** dict: 调用 API 返回的结果

#### async def get_graph_version()

| name       | type                 | description             |
| ---------- | -------------------- | ----------------------- |
| bvid       | str                  | BV 号。                 |
| credential | Credential, optional | 凭据. Defaults to None. |

 获取剧情图版本号，仅供 `get_edge_info()` 使用。

**Returns:** int: 剧情图版本号

#### async def get_edge_info()

| name       | type                 | description                                          |
| ---------- | -------------------- | ---------------------------------------------------- |
| bvid       | str                  | BV 号。                                              |
| edge_id    | int \| None, optional        | 节点 ID，为 None 时获取根节点信息. Defaults to None. |
| credential | Credential, optional | 凭据. Defaults to None.                              |

获取剧情树节点信息。

**Returns:** dict: 调用 API 返回的结果

#### async def mark_score()

| name | type | description |
| ---- | ---- | ----------- |
| score | int | 互动视频分数. Defaults to 5. |

为互动视频打分

**Returns:** dict: 调用 API 返回的结果

#### async def get_graph()

获取视频对应情节树。

**Returns:** InteractiveGraph: 情节树

---

## class InteractiveVideoDownloaderMode

**Extends: enum.Enum**

互动视频下载模式

- IVI: 下载可播放的 ivi 文件
- NODE_VIDEOS: 下载所有节点的所有视频并存放在某个文件夹，每一个节点的视频命名为 `{节点 id} {节点标题 (自动去除敏感字符)}.mp4`
- DOT_GRAPH: 下载 dot 格式的情节树图表
- NO_PACKAGING: 前面按照 ivi 文件下载步骤进行下载，但是最终不会打包成为 ivi 文件，所有文件将存放于一个文件夹中。互动视频数据将存放在一个文件夹中，里面的文件命名/含义与拆包后的 ivi 文件完全相同。

---

## class InteractiveVideoDownloaderEvents

**Extends: enum.Enum**

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

## class InteractiveVideoDownloader

**Extends: AsyncEvent**

互动视频下载类

### Functions

#### def \_\_init\_\_()

| name               | type             | description                 |
| ------------------ | ---------------- | --------------------------- |
| video              | InteractiveVideo | 互动视频类                   |
| out                | str              | 输出文件地址                  |
| self_download_func | Coroutine \| None        | 自定义下载函数（需 async 函数） |
| downloader_mode | InteractiveVideoDownloaderMode | 下载模式 |

`self_download_func` 函数应接受两个参数（第一个是下载 URL，第二个是输出地址（精确至文件名））

#### async def start()

开始下载

#### async def abort()

中断下载

---

## class InteractiveButtonAlign

**Extends: enum.Enum**

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

## class InteractiveNodeJumpingType

**Extends: enum.Enum**

对下一节点的跳转的方式

- ASK    : 选择
- DEFAULT: 跳转到默认节点
- READY  : 选择(只有一个选择)

---

## class InteractiveVariable

互动节点的变量

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| name | str | 变量名 |
| var_id | str | 变量 id |
| var_value | int | 变量的值 |
| show | bool | 是否显示 |
| random | bool | 是否随机值(1-100) |

#### def get_id()

获取变量 id

**Returns:** int: 变量 id

#### def refresh_value()

刷新变量数值

**Returns:** None

#### def get_value()

获取变量数值

**Returns:** int: 变量数值

#### def is_show()

变量是否显示

**Returns:** bool: 变量是否显示

#### def is_random()

是否随机数值

**Returns:** bool: 变量是否随机数值

#### def get_name()

获取变量名

**Returns:** str: 变量名

---

## class InteractiveButton

互动视频节点按钮类

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| text | str | 文字 |
| x | int | X 轴 |
| y | int | Y 轴 |
| align | int \| InteractiveButtonAlign | 按钮的文字在按钮中的位置 |

#### def get_text()

获取文字

**Returns:** str: 按钮文字

#### def get_align()

获取按钮的文字在按钮中的位置

**Returns:** 按钮的文字在按钮中的位置

#### def get_pos()

获取按钮的位置

**Returns:** 按钮的位置

---

## class InteractiveJumpingCondition

节点跳转的公式，只有公式成立才会跳转

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| var | List[InteractiveVariable] | 所有变量 |
| condition | str | 公式 |

#### def get_result()

计算公式获得结果

**Returns:** bool: 是否成立

---

## class InteractiveJumpingCommand

节点跳转对变量的操作

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| var | List[InteractiveVariable] | 所有变量 |
| condition | str | 公式 |

---

## class InteractiveNode

互动视频节点类

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| video | InteractiveVideo | 视频类 |
| node_id | int | 节点 id |
| cid | int | CID |
| vars | List[InteractiveVariable] | 变量 |
| button | InteractiveButton \| None | 对应的按钮 |
| condition | InteractiveJumpingCondition | 跳转公式 |
| native_command | InteractiveJumpingCommand | 跳转时变量的操作 |
| is_default | bool | 是不是默认的跳转的节点 |

#### async def get_vars()

获取节点的所有变量

**Returns:** List[InteractiveVariable]: 节点的所有变量

#### async def get_children()

获取节点的所有子节点

**Returns:** List[InteractiveNode]: 所有子节点

#### def is_default()

是不是默认节点

**Returns:** bool: 是否默认节点

#### async def get_jumping_type()

获取子节点跳转方式 (参考 InteractiveNodeJumpingType)

**Returns:** int: 子节点跳转方式

#### def get_node_id()

获取节点 id

**Returns:** int: 节点 id

#### def get_cid()

获取节点 cid

**Returns:** int: 节点 cid

#### def get_self_button()

获取节点对应的按钮

**Returns:** InteractiveButton: 节点对应按钮

#### def get_jumping_condition()

获取节点跳转的公式

**Returns:** InteractiveJumpingCondition: 节点跳转公式

#### def get_video()

获取节点对应的视频

**Returns:** 节点对应视频

#### async def get_info()

获取节点的简介

**Returns:** dict: 调用 API 返回的结果

---

## class InteractiveGraph

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| video | InteractiveVideo | 互动视频类 |
| skin | dict | 样式 |
| root_cid | int | 根节点 CID |

#### def get_video()

获取情节树对应视频

**Returns:** 对应视频

#### def get_skin()

获取样式

**Returns:** 样式

#### async def get_root_node()

获取根节点

**Returns:** InteractiveNode: 根节点

#### async def get_children()

获取子节点

**Returns:** List[InteractiveNode]: 子节点

---

## def get_ivi_file_info()

| name | type | description |
| - | - | - |
| path | str | ivi 文件地址 |

获取 ivi 文件的信息

**Returns:** dict: ivi 文件信息
