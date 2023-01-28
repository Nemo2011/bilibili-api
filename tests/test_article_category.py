# bilibili_api.article_category

from bilibili_api import article_category


async def test_a_get_category_info_by_id():
    return article_category.get_category_info_by_id(3)


async def test_b_get_category_info_by_name():
    return article_category.get_category_info_by_name("轻小说")


async def test_c_get_category_list():
    return article_category.get_categories_list()


async def test_d_get_category_list_sub():
    return article_category.get_categories_list_sub()


async def test_e_get_category_recommend_articles():
    return await article_category.get_category_recommend_articles(
        category_id=3,
        order=article_category.ArticleOrder.FAVORITES,
        page_num=11,
        page_size=4514
    )
