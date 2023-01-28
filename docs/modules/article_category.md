# Module article_category.md

``` python
from bilibili_api import article_category
```

专栏分类相关

## class ArticleOrder

专栏排序方式.

+ DEFAULT: 默认
+ TIME: 投稿时间排序
+ LIKE: 点赞数最多
+ COMMENTS: 评论数最多
+ FAVORITES: 收藏数最多

---

## def get_category_info_by_id()

| name | type | description |
| ---- | ---- | ----------- |
| id   | int  | id          |

获取专栏分类信息

**Returns:** Tuple[dict | None, dict | None]: 第一个是主分区，第二个是字分区。没有找到则为 (None, None)

---

## def get_category_info_by_name()

| name | type | description |
| ---- | ---- | ----------- |
| name | int  | 分类名       |

获取专栏分类信息

**Returns:** Tuple[dict | None, dict | None]: 第一个是主分区，第二个是字分区。没有找到则为 (None, None)

---

## def get_categories_list()

获取所有的分类的数据

**Returns:** List[dict]: 所有分区的数据

---

## def get_categories_list_sub()

获取所有分区的数据

含父子关系（即一层次只有主分区）

**Returns:** dict: 所有分区的数据

---

## async def get_category_recommend_articles()

| name | type | description |
| ---- | ---- | ----------- |
| category_id | int | 专栏分类的 id, 0 为全部. Defaults to 0. |
| order | ArticleOrder | 排序方式. Defaults to ArticleOrder.DEFAULT. |
| page_num | int | 页码. Defaults to 1. |
| page_size | int | 每一页数据大小. Defaults to 20. |

获取指定分区的推荐文章

**Returns:** dict: 调用 API 返回的结果
