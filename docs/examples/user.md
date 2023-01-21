# 示例：获取用户粉丝数

```python
from bilibili_api import user, sync

u = user.User(660303135)

print(sync(u.get_relation_info())["follower"])
```

# 示例：康康站长认识哪些我喜欢的 up

``` python
from bilibili_api import user, Credential
import asyncio

async def main() -> None:
    CREDENTIAL = Credential(
        sessdata="xxxxxxxxxx"
    )
    bishi = user.User(uid=2, credential=CREDENTIAL)
    lists = await bishi.get_self_same_followers()
    for up in lists["list"]:
        print(up["uname"], end=" ")

if __name__ == '__main__':
    asyncio.run(main())
```

# 示例：获取用户所有动态

```python
import json
from bilibili_api import user, sync

# 实例化
u = user.User(660303135)

async def main():
  	# 用于记录下一次起点
    offset = 0
    
    # 用于存储所有动态
    dynamics = []

    # 无限循环，直到 has_more != 1
    while True:
      	# 获取该页动态
        page = await u.get_dynamics(offset)
        
        if 'cards' in page:
          	# 若存在 cards 字段（即动态数据），则将该字段列表扩展到 dynamics
            dynamics.extend(page['cards'])
		
        if page['has_more'] != 1:
        		# 如果没有更多动态，跳出循环
            break
				
        # 设置 offset，用于下一轮循环
        offset = page['next_offset']

    # 打印动态数量
    print(f"共有 {len(dynamics)} 条动态")

# 入口
sync(main())
```

# 示例：移除所有粉丝
```python
from bilibili_api import Credential, user, sync
from bilibili_api.user import RelationType

credential = Credential(sessdata="", bili_jct="")
my_user = user.User(uid=UID, credential=credential)

async def main():
    follower_counts = 0
    page = 1
    
    total_followers = (await my_user.get_relation_info())["follower"]
    
    # 因为请求一次 get_followers 只能获取 20 个粉丝，所以要做一个检查
    while follower_counts < total_followers:
    	# 获取当前页数的粉丝列表
        followers = await my_user.get_followers(pn=page)
	
	      # 循环当前页数的粉丝列表
        for i in followers["list"]:
          follower_counts += 1
	    
          uid = int(i["mid"])
	        name = i["uname"]
          u = user.User(uid=uid, credential=credential)
	    
	        # 移除粉丝
	        print(f"Removing {name}, uid:{uid}. Count: {follower_counts}")
          await u.modify_relation(relation=RelationType.REMOVE_FANS)
	    
	        # 防止触发 412 错误
          await asyncio.sleep(1)
	    
	# 下一页
        page += 1
	
sync(main())
```
