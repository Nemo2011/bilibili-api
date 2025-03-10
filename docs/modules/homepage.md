# Module homepage.py


bilibili_api.homepage

主页相关操作。


``` python
from bilibili_api import homepage
```

- [async def get\_favorite\_list\_and\_toview()](#async-def-get\_favorite\_list\_and\_toview)
- [async def get\_favorite\_list\_content()](#async-def-get\_favorite\_list\_content)
- [async def get\_links()](#async-def-get\_links)
- [async def get\_popularize()](#async-def-get\_popularize)
- [async def get\_top\_photo()](#async-def-get\_top\_photo)
- [async def get\_videos()](#async-def-get\_videos)

---

## async def get_favorite_list_and_toview()

获取首页右上角视频相关列表（收藏夹+稍后再看）

收藏夹具体内容在 `get_favorite_list_content` 接口


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_favorite_list_content()

获取首页右上角视频相关列表（收藏夹+稍后再看）的具体内容

稍后再看具体内容在 `get_favorite_list_and_toview` 接口


| name | type | description |
| - | - | - |
| `media_id` | `int` | 收藏夹 id |
| `credential` | `Credential` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_links()

获取主页左面的链接。
可能和个人喜好有关。


| name | type | description |
| - | - | - |
| `credential` | `Credential \| None` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_popularize()

获取推广的项目。
(有视频有广告)


| name | type | description |
| - | - | - |
| `credential` | `Credential \| None` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_top_photo()

获取主页最上方的图像。
例如：b 站的风叶穿行，通过这个 API 获取的图片就是风叶穿行的图片。



**Returns:** `dict`:  调用 API 返回的结果。




---

## async def get_videos()

获取首页推荐的视频。


| name | type | description |
| - | - | - |
| `credential` | `Credential \| None` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




