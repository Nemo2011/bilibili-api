# 示例：抓取活动页面评论

```python
from bilibili_api import comment, activity, sync, Credential


async def main() -> int:
    url = "https://www.bilibili.com/blackboard/topic/index_10years_web.html"
    aid = await activity.get_activity_aid(url)

    comments = []
    page = 1
    count = 0
    while True:
        c = await comment.get_comments(
            aid,
            comment.CommentResourceType.ACTIVITY,
            page,
            credential=Credential(sessdata="xxx"),
        )

        replies = c["replies"]
        if replies is None:
            break
        comments.extend(replies)
        count += c["page"]["size"]
        page += 1
        if count >= c["page"]["count"] or count >= 10:
            break

    for cmt in comments:
        print(f"{cmt['member']['uname']}: {cmt['content']['message']}")
    print(f"\n\n共有 {count} 条评论（不含子评论）")


sync(main())
```