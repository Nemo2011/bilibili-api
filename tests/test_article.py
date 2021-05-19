from bilibili_api import article


async def test_a_get_content():
    ar = await article.get_article_content(7099047)

    md = ar.markdown()

    js = ar.json()

    return js
