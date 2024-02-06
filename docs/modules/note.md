# Module note.py

```python
from bilibili_api import note
```

笔记相关操作

?> 注意，笔记分为私有笔记和公开笔记...公开笔记实质为专栏
?> 公有笔记不限数量，私有笔记每稿件只能写一篇

## const dict NoteType

笔记类型枚举

## class Note

笔记类，各种对笔记的操作都在里面

### Attributes

| name | type | description|
| ---- | ---- | ---------- |
| credential | Credential | 凭据 |

### Funcitions

#### def \_\_init\_\_()
| name | type | description|
| ---- | ---- | ---------- |
| type | str | 笔记类型 |
| oid | int | 稿件 id |
| oid_type | int | 稿件 id 类型 |
| note_id | int | 笔记 id |
| credential | Credential \| None, optional | Credential 类 |

---

#### def set_oid()

| name | type | description |
| ---- | ---- | ----------- |
| oid | int  | av 号。     |

设置 oid。

**Returns:** None

---

#### def set_note_id()

| name | type | description |
| ---- | ---- | ----------- |
| note_id | int  | note_id。 |

设置 note_id。

**Returns:** None

---

#### def set_cvid()

| name | type | description |
| ---- | ---- | ----------- |
| cvid | int  | cvid 专栏号。 |

设置 cvid。

**Returns:** None

---

#### def get_oid()

获取 oid。

**Returns:** str: oid

---

#### def get_cvid()

获取 cvid。

**Returns:** str: cvid

---

#### def get_note_id()

获取 note_id。

**Returns:** str: note_id

---

#### def turn_to_article()

将笔记类转为专栏类。需要保证笔记是公开笔记。

**Returns:** Note: 专栏类

---

#### async def get_info()

获取笔记信息。

**Returns:** API 调用返回结果。

---

#### async def get_images_raw_info()

获取笔记所有图片原始信息。

**Returns:** API 调用返回结果。

---

#### async def get_images()

获取笔记所有图片并转为 Picture 类。

**Returns:** List[Picture]

---

#### async def get_all()

一次性获取专栏尽可能详细数据，包括原始内容、标签、发布时间、标题、相关专栏推荐等。

**Returns:** API 调用返回结果。

---

#### async def fetch_content()

加载专栏内容。该方法不会返回任何值，调用该方法后请再调用 `self.markdown()` 或 `self.json() `来获取你需要的值。

**Returns:** None

---

#### def markdown()

转换为 Markdown

请先调用 fetch_content()

**Returns:** str: Markdown 内容

---

#### def json()

转换为 JSON 数据

请先调用 fetch_content()

**Returns:** dict: JSON 数据

---

#### async def set_like()

| name   | type           | description                |
| ------ | -------------- | -------------------------- |
| status | bool, optional | 点赞状态. Defaults to True |

设置专栏点赞状态

**Returns:** API 调用返回结果。

---

#### async def set_favorite()

| name   | type           | description                |
| ------ | -------------- | -------------------------- |
| status | bool, optional | 收藏状态. Defaults to True |

设置专栏收藏状态

**Returns:** API 调用返回结果。

---

#### async def add_coins()

给专栏投币，目前只能投一个

**Returns:** API 调用返回结果。
