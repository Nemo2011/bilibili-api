# Module article_category.py


bilibili_api.article_category

专栏分类相关


``` python
from bilibili_api import article_category
```

- [class ArticleOrder()](#class-ArticleOrder)
- [def get\_categories\_list()](#def-get\_categories\_list)
- [def get\_categories\_list\_sub()](#def-get\_categories\_list\_sub)
- [def get\_category\_info\_by\_id()](#def-get\_category\_info\_by\_id)
- [def get\_category\_info\_by\_name()](#def-get\_category\_info\_by\_name)
- [async def get\_category\_recommend\_articles()](#async-def-get\_category\_recommend\_articles)

---

## class ArticleOrder()

> Extend: `enum.Enum`

专栏排序方式.

+ DEFAULT: 默认
+ TIME: 投稿时间排序
+ LIKE: 点赞数最多
+ COMMENTS: 评论数最多
+ FAVORITES: 收藏数最多




---

## def get_categories_list()

获取所有的分类的数据



**Returns:** `list[dict]`:  所有分区的数据




---

## def get_categories_list_sub()

获取所有分区的数据

含父子关系（即一层次只有主分区）



**Returns:** `list[dict]`:  所有分区的数据




---

## def get_category_info_by_id()

获取专栏分类信息


| name | type | description |
| - | - | - |
| `id` | `int` | id |

**Returns:** `tuple[dict | None, dict | None]`:  第一个是主分区，第二个是字分区。没有找到则为 (None, None)




---

## def get_category_info_by_name()

获取专栏分类信息


| name | type | description |
| - | - | - |
| `name` | `str` | 分类名 |

**Returns:** `tuple[dict | None, dict | None]`:  第一个是主分区，第二个是字分区。没有找到则为 (None, None)




---

## async def get_category_recommend_articles()

获取指定分区的推荐文章


| name | type | description |
| - | - | - |
| `category_id` | `int, optional` | 专栏分类的 id, 0 为全部. Defaults to 0. |
| `order` | `ArticleOrder, optional` | 排序方式. Defaults to ArticleOrder.DEFAULT. |
| `page_num` | `int, optional` | 页码. Defaults to 1. |
| `page_size` | `int, optional` | 每一页数据大小. Defaults to 20. |

**Returns:** `dict`:  调用 API 返回的结果




