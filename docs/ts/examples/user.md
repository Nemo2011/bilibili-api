# 示例：获取站长账号简介(站长 uid 是 2，小号 uid 是 1, 这里用 uid 是 2)

```typescript
const bili_user = require("bilibili-api-ts/user");

var zhanzhang = new bili_user.User({
    uid: 2
});

zhanzhang.get_user_info().then(
    value => console.log(value)
);
```
