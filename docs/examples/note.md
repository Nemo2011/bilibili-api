# 示例：获取公开笔记信息

```python
import asyncio
from bilibili_api import note

async def main():
    # 实例化 Note 类
    n = note.Note(cvid="21046701")
    # 获取笔记信息
    info = await n.get_info()
    # 打印笔记信息
    print(info)

if __name__ == '__main__':
    # 主入口
    asyncio.get_event_loop().run_until_complete(main())
```