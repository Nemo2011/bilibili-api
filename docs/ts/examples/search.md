# 示例：获取搜索结果

``` typescript
const search = requier("bilibili-api-ts/search");
search.search({keyword: "奥利给"}).then(value => console.log(value));
```
