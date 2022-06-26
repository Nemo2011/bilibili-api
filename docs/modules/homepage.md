# Module homepage.py

```python
from bilibili_api import homepage
```

主页相关操作。

## _async_ def get_top_photo()

获取主页最上方的图像。
例如：b 站的风叶穿行，通过这个 API 获取的图片就是风叶穿行的图片。

**Returns:** 调用 API 返回的结果。


## _async_ def get_links()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |

获取主页左面的链接。
可能和个人喜好有关。

**Returns:** 调用 API 返回的结果

## _async_ def get_popularize()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |

获取推广的项目。
~~有视频有广告~~

**Returns:** 调用 API 返回的结果

## _async_ def get_videos()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |

获取首页推荐的视频。

**Returns:** 调用 API 返回的结果
