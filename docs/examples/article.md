# 示例：获取专栏内容并转换为 Markdown

```python
from bilibili_api import article, sync


async def main():
    ar = article.Article(7099047)

    await ar.fetch_content()

    with open('article.md', 'w', encoding='utf8') as f:
        f.write(ar.markdown())


sync(main())
```

