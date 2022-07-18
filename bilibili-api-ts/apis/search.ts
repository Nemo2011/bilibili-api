export const SearchData = {
  "search": {
    "web_search": {
      "url": "https://api.bilibili.com/x/web-interface/search/all/v2",
      "method": "GET",
      "verify": false,
      "params": {
        "keyword": "str: 搜索用的关键字", 
        "page": "int: 页码"
      },
      "comment": "在首页以关键字搜索，只指定关键字，其他参数不指定"
    },
    "web_search_by_type": {
      "url": "https://api.bilibili.com/x/web-interface/search/type",
      "method": "GET",
      "verify": false,
      "params": {
        "keyword": "str: 搜索用的关键字",
        "search_type": "str: 搜索时限定类型：视频(video)、番剧(media_bangumi)、影视(media_ft)、直播(live)、专栏(article)、话题(topic)、用户(bili_user)",
        "page": "int: 页码"
      },
      "comment": "搜索关键字时限定类型"
    }, 
    "default_search_keyword": {
      "url": "https://api.bilibili.com/x/web-interface/search/default", 
      "method": "GET", 
      "verify": false, 
      "comment": "获取默认的搜索内容"
    }, 
    "hot_search_keywords": {
      "url": "https://s.search.bilibili.com/main/hotword", 
      "method": "GET", 
      "verify": false, 
      "comment": "获取热搜"
    }
  }
}