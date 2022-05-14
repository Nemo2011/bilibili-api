from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException
from bilibili_api import article
from .common import get_credential

ar = article.Article(7099047, get_credential())

async def test_a_get_content():
    await ar.fetch_content()

    md = ar.markdown()

    js = ar.json()

    return js

async def test_b_set_like():
    return await ar.set_like()

async def test_c_set_favorite():
    return await ar.set_favorite()

async def test_d_add_coins():
    try:
        return await ar.add_coins()
    except ResponseCodeException as e:
        if e.code != 34005:
            raise e

        return e

async def test_e_get_info():
    return await ar.get_info()

async def test_f_get_article_list():
    return await article.get_article_list(10)

async def after_all():
    await ar.set_like(False)
    await ar.set_favorite(False)
