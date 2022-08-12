"use strict";
exports.__esModule = true;
exports.ChannelData = void 0;
exports.ChannelData = {
    "ranking": {
        "get_top10": {
            "url": "https://api.bilibili.com/x/web-interface/ranking/region",
            "method": "GET",
            "verify": false,
            "params": {
                "rid": "int: tid，分区 id",
                "day": "int: 3，7"
            },
            "comment": "获取分区前十排行榜"
        }
    }
};
