# 示例：获取动漫分区推荐文章 (点赞数排序)

``` python
from bilibili_api import article_category, sync

category_id = article_category.get_category_info_by_name("动画")[0]["id"]

print(sync(article_category.get_category_recommend_articles(
    category_id=category_id,
    order=article_category.ArticleOrder.LIKE
)))
```
