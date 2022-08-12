# 示例：查询分区 tid

``` javascript
const channel = require("bilibili-api-ts/channel");

console.log(channel.get_channel_info_by_name({name: "动物圈"})[0].tid)
```
