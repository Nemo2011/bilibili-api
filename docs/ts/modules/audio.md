# Module audio.ts(audio.js)

```typescript
import {} from "bilibili-api-ts/audio"
```

音频相关

## class Audio

音频类。

### Functions

#### constructor

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| auid       | int                  | 音频 AU 号             |
| credential | Credential, optional | 凭据. Defaults to None |

#### function get_auid()

获取 auid

**Returns:** auid

#### async function get_info()

获取音频信息

**Returns:** API 调用返回结果

#### async function get_tags()

获取音频 tags

**Returns:** API 调用返回结果

#### async function get_download_url()

获取音频下载链接

**Returns:** API 调用返回结果
