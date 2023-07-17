# bilibili_api.article
from bilibili_api import article
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException

from .common import get_credential

ar = article.Article(17973349, get_credential())
al = article.ArticleList(10, get_credential())


async def test_a_Article_markdown_get_content():
    await ar.fetch_content()

    md = ar.markdown()

    return md


async def test_b_Article_json_get_content():
    await ar.fetch_content()

    js = ar.json()

    return js


async def test_c_Article_set_like():
    await ar.set_like()
    return await ar.set_like(False)


async def test_d_Article_set_favorite():
    return await ar.set_favorite()


async def test_e_Article_add_coins():
    try:
        return await ar.add_coins()
    except ResponseCodeException as e:
        if e.code != 34005 and e.code != -104:
            raise e

        return e


async def test_f_Article_get_info():
    return await ar.get_info()


async def test_g_ArticleList_get_article_list():
    return await al.get_content()


async def test_h_get_article_rank():
    return await article.get_article_rank()
