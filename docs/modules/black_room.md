# Module bilibili_api.black_room

```
from bilibili_api import black_room
```

## class BlackReasonType

**Extends: enum.Enum**

违规类型代码

违规原因类型枚举 (英语翻译错误请忽略/提 issue/发起 PR) 

- ALL: 全部
- FLOOD_SCREEN: 刷屏
- SOFA: 抢沙发
- PRON_VULGAR: 色情低俗内容
- GAMBLED_SCAMS: 赌博诈骗内容
- ILLEGAL: 违禁信息
- ADS: 垃圾广告信息
- PERSONAL_ATTACK: 人身攻击
- INVASION_OF_PRIVACY: 侵犯隐私
- LEAD_WAR: 引战
- SPOILER: 剧透
- ADD_MALICIOUS_TAG: 恶意为他人添加标签
- DEL_OTHERS_TAG: 恶意删除他人标签
- PRON: 色情
- VULGAR: 低俗
- VIOLENT: 暴力血腥内容
- MALICIOUS_ARCHIVES: 恶意投稿行为
- ILLEGAL_STATION: 发布非法网站信息
- SEND_UNREAL_EVENT: 发布不实信息
- ABETMENT: 发布教唆怂恿信息
- MALICIOUS_SPAMMING: 恶意刷屏
- ILLEGAL_ACCOUNT: 账号违规
- PLAGIARISM: 抄袭
- PRETEND_ORIGINAL: 冒充官号
- BAD_FOR_YOUNGS: 青少年不宜
- BREAK_INTERNET_SECURITY: 破坏网络安全
- SEND_UNREAL_MISLEADING_EVENT: 发布不实舞蹈信息
- VIOLATE_SITE_OPERATING_RULES: 违规网站运营规则
- MALICIOUS_TOPICS: 恶意创建话题
- CREATE_ILLEGAL_LUCKY_DRAW: 发布违规抽奖
- PRETEND_OTHER: 冒充他人

---

## class BlackType

违规类型枚举

- ALL: 全部
- COMMENT: 评论
- DANMAKU: 弹幕
- PRIVATE_MESSAGE: 私信
- TAG: 标签
- PERSONAL_INFORMATION: 个人信息
- VIDEO: 视频
- ARTICLE: 专栏
- DYNAMIC: 动态
- ALBUM: 相簿

---

## class BlackFrom

**Extends: enum.Enum**

违规来源

- SYSTEM: 系统封禁
- ADMIN: 风纪仲裁
- ALL: 全部

---

## async def get_blocked_list()

获取小黑屋名单

| name | type | description |
| - | - | - |
| from_ | BlackFrom | 违规来源. Defaults to BlackFrom.ALL. |
| type_ | int | 违规类型. 查看 black_room.BLACK_TYPE。Defaults to 0 (ALL). |
| pn | int | 页数. Defaults to 1. |
| credential | Credential \| None | 凭据, Defaults to None. |

---

## class BlackRoom()

### Attributes

| name | type | description |
| - | - | - |
| credential | Credential \| None | 凭据类 ｜

### Functions

## def \_\_init\_\_()

| name | type | description |
| - | - | - |
| black_room_id | int | 小黑屋 id |
| credential | Credential \| None | 凭据类. Defaults to None. |

## async def get_details()

获取小黑屋详细信息
