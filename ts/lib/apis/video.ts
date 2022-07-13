export var VideoData = {
  "info": {
    "stat": {
      "url": "https://api.bilibili.com/x/web-interface/archive/stat",
      "method": "GET",
      "verify": false,
      "params": {
        "aid": "int: av 号"
      },
      "comment": "视频数据"
    },
    "detail": {
      "url": "https://api.bilibili.com/x/web-interface/view",
      "method": "GET",
      "verify": false,
      "params": {
        "aid": "int: av 号"
      },
      "comment": "视频详细信息"
    },
    "tags": {
      "url": "https://api.bilibili.com/x/tag/archive/tags",
      "method": "GET",
      "verify": true,
      "params": {
        "aid": "int: av 号"
      },
      "comment": "视频标签信息"
    },
    "chargers": {
      "url": "https://api.bilibili.com/x/web-interface/elec/show", 
      "method": "GET",
      "verify": false,
      "params": {
        "aid": "int: av 号",
        "mid": "int: 用户 UID"
      },
      "comment": "视频充电信息"
    },
    "pages": {
      "url": "https://api.bilibili.com/x/player/pagelist",
      "method": "GET",
      "verify": false,
      "params": {
        "aid": "int: av 号"
      },
      "comment": "分 P 列表"
    },
    "playurl": {
      "url": "https://api.bilibili.com/x/player/playurl",
      "method": "GET",
      "verify": false,
      "params": {
        "avid": "int: av 号",
        "cid": "int: 分 P 编号",
        "qn": "int: 视频质量编号，最高 127",
        "otype": "const str: json",
        "fnval": "const int: 4048", 
        "platform": "int: 平台"
      },
      "comment": "视频下载的信息，下载链接需要提供 headers 伪装浏览器请求（Referer 和 User-Agent）"
    }
  }
}