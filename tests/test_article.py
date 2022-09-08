# bilibili_api.article
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException
from bilibili_api import article
from .common import get_credential

ar = article.Article(1, get_credential())
al = article.ArticleList(10, get_credential())

async def test_a_markdown_get_content():
    await ar.fetch_content()

    md = ar.markdown()

    return md

async def test_b_json_get_content():
    await ar.fetch_content()

    js = ar.json()

    return js

async def test_c_set_like():
    return await ar.set_like()

async def test_d_set_favorite():
    return await ar.set_favorite()

async def test_e_add_coins():
    try:
        return await ar.add_coins()
    except ResponseCodeException as e:
        if e.code != 34005:
            raise e

        return e

async def test_f_get_info():
    return await ar.get_info()

async def test_g_get_article_list():
    return await al.get_content()

async def after_all():
    await ar.set_like(False)
    await ar.set_favorite(False)
