# 示例：获取视频所有评论

**建议登录后操作**

## 旧接口

```python
from bilibili_api import comment, sync


async def main():
    # 存储评论
    comments = []
    # 页码
    page = 1
    # 当前已获取数量
    count = 0
    while True:
        # 获取评论
        c = await comment.get_comments(418788911, comment.CommentResourceType.VIDEO, page)

        replies = c['replies']
        if replies is None:
            # 未登陆时只能获取到前20条评论
            # 此时增加页码会导致c为空字典
            break

        # 存储评论
        comments.extend(replies)
        # 增加已获取数量
        count += c['page']['size']
        # 增加页码
        page += 1

        if count >= c['page']['count']:
            # 当前已获取数量已达到评论总数，跳出循环
            break

    # 打印评论
    for cmt in comments:
        print(f"{cmt['member']['uname']}: {cmt['content']['message']}")

    # 打印评论总数
    print(f"\n\n共有 {count} 条评论（不含子评论）")


sync(main())
```

## 新接口

``` python
from bilibili_api import comment, sync


async def main():
    # 存储评论
    comments = []
    # 刷新次数（约等于页码）
    page = 1
    # 每次提供的 offset (pagination_str)
    pag = ""

    while True:
        # 获取评论
        c = await comment.get_comments_lazy(418788911, comment.CommentResourceType.VIDEO, offset=pag)

        pag = c["cursor"]["pagination_reply"]["next_offset"]
        replies = c['replies']
        if replies is None:
            # 未登陆时只能获取到前20条评论
            # 此时增加页码会导致c为空字典
            break

        # 存储评论
        comments.extend(replies)
        # 增加页码
        page += 1

        # 只刷新 5 次（约等于 5 页）
        if page > 5:
            break

    # 打印评论
    for cmt in comments:
        print(f"{cmt["member"]['uname']}: {cmt['content']['message']}")

    # 打印评论总数
    print(f"\n\n共有 {len(comments)} 条评论（不含子评论）")


sync(main())
```
