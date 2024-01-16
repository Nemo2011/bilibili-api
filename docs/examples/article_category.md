# 示例：获取动漫分区推荐文章 (点赞数排序)

``` python
from bilibili_api import article_category, sync

cat, father_cat = article_category.get_category_info_by_name("动画")  # 函数返回分区信息以及其父分区的信息

# print(father_cat) -> None 动画分区本身就是主分区之一，不存在父分区

category_id = cat["id"]

cat_recommand_articles = sync(
    article_category.get_category_recommend_articles(
        category_id=category_id, order=article_category.ArticleOrder.LIKE
    )
)

# article_category.ArticleOrder.LIKE 代表点赞数排序

print(cat_recommand_articles)

```
