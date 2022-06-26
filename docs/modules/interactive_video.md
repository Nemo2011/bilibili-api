# Module interactive_video.py

```python
from bilibili_api import interactive_video
```

## _async_ def up_submit_story_tree()
| name       | type                 | description                                       |
| ---------- | -------------------- | ------------------------------------------------- |
| story_tree | str                  | 情节树的描述。参考 bilibili_storytree.StoryGraph  |
| credential | Credential           | Credential 类。up 主需要拥有交互视频              |

提交情节树。up 主需要拥有交互视频。

**Returns:** API 调用返回结果。

---

## _async_ def up_get_ivideo_pages()
| name       | type                 | description                           |
| ---------- | -------------------- | ------------------------------------- |
| bvid       | str                  | BV 号。                               |
| credential | Credential           | Credential 类。up 主需要拥有交互视频  |

获取交互视频分 P。up 主需要拥有交互视频。

**Returns:** API 调用返回结果。

---

## _async_ def get_graph_version()

| name       | type                 | description             |
| ---------- | -------------------- | ----------------------- |
| bvid       | str                  | BV 号。                 |
| credential | Credential, optional | 凭据. Defaults to None. |

 获取剧情图版本号，仅供 `get_edge_info()` 使用。

**Returns:** API 调用返回结果

---

## _async_ def get_edge_info()

| name       | type                 | description                                          |
| ---------- | -------------------- | ---------------------------------------------------- |
| bvid       | str                  | BV 号。                                              |
| edge_id    | int, optional        | 节点 ID，为 None 时获取根节点信息. Defaults to None. |
| credential | Credential, optional | 凭据. Defaults to None.                              |

 获取剧情树节点信息。

**Returns:** API 调用返回结果

---
