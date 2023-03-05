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

## class JuryVoteOpinion

仲裁投票类型枚举，选择对应案件类型的观点

    单条评论（弹幕）
    - SUITABLE: 合适
    - AVERAGE: 一般
    - UNSUITABLE: 不合适
    - UNKNOW: 无法判断

    评论（弹幕）氛围
    - ENV_GREAT: 评论环境好
    - ENV_AVERAGE: 评论环境一般
    - ENV_BAD: 评论环境差
    - ENV_UNKNOW: 无法判断评论环境

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

**Returns:** dict: 调用 API 返回的结果

## async def get_reason()

获取小黑屋违规原因

**Returns:** dict: 调用 API 返回的结果

---

## class JuryCase

### Attributes

| name | type | description |
| - | - | - |
| case_id | int | 案件 id |
| credential | Credential \| None | 凭据类 ｜

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| case_id | int | 案件 id |
| credential | Credential | 凭据类 |

#### async def get_details()

获取案件详细信息

**Returns:** dict: 调用 API 返回的结果

#### async def get_opinions()

获取案件观点列表

**Returns:** dict: 调用 API 返回的结果

#### async def vote()

| name | type | description |
| - | - | - |
| opinion | JuryVoteOpinion | 仲裁投票类型枚举，选择对应案件类型的观点 |
| is_insider | bool | 是否观看此类视频 |
| is_anonymous | bool | 是否匿名投票 |
| reason | str, optional | 投票理由. Defaults to None. |

进行仲裁投票

**Returns:** dict: 调用 API 返回的结果

---

## async def get_next_jury_case()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据 |

获取下一个仲裁案件

**Returns:** JuryCase: JuryCase 类

---

## async def get_jury_case_list()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据 |

获取仲裁案件列表

**Returns:** list: JuryCase 类列表