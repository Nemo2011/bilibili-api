"use strict";
exports.__esModule = true;
exports.DmMode = exports.DmFontSize = exports.Danmaku = void 0;
var Danmaku = /** @class */ (function () {
    function Danmaku(config) {
        var text = config.text, dm_time = config.dm_time ? config.dm_time : 0, send_time = config.send_time ? config.send_time : 0, crc32_id = config.crc32_id ? config.crc32_id : "", color = config.color ? config.color : "", weight = config.weight ? config.weight : -1, id = config.id_ ? config.id_ : -1, id_str = config.id_str ? config.id_str : "", action = config.action ? config.action : "", mode = config.mode ? config.mode : DmMode.FLY, font_size = config.font_size ? config.font_size : DmFontSize.NORMAL, is_sub = config.is_sub ? config.is_sub : false, pool = config.pool ? config.pool : 0, attr = config.attr ? config.attr : -1;
        this.text = text;
        this.dm_time = dm_time;
        this.send_time = send_time;
        this.crc32_id = crc32_id;
        this.color = color;
        this.weight = weight;
        this.id = id;
        this.id_str = id_str;
        this.action = action;
        this.mode = mode;
        this.font_size = font_size;
        this.is_sub = is_sub;
        this.pool = pool;
        this.attr = attr;
    }
    return Danmaku;
}());
exports.Danmaku = Danmaku;
var DmFontSize;
(function (DmFontSize) {
    DmFontSize[DmFontSize["EXTREME_SMAL"] = 12] = "EXTREME_SMAL";
    DmFontSize[DmFontSize["SUPER_SMALL"] = 16] = "SUPER_SMALL";
    DmFontSize[DmFontSize["SMALL"] = 18] = "SMALL";
    DmFontSize[DmFontSize["NORMAL"] = 25] = "NORMAL";
    DmFontSize[DmFontSize["BIG"] = 36] = "BIG";
    DmFontSize[DmFontSize["SUPER_BIG"] = 45] = "SUPER_BIG";
    DmFontSize[DmFontSize["EXTREME_BIG"] = 64] = "EXTREME_BIG";
})(DmFontSize = exports.DmFontSize || (exports.DmFontSize = {}));
var DmMode;
(function (DmMode) {
    DmMode[DmMode["FLY"] = 1] = "FLY";
    DmMode[DmMode["TOP"] = 5] = "TOP";
    DmMode[DmMode["BOTTOM"] = 4] = "BOTTOM";
    DmMode[DmMode["REVERSE"] = 6] = "REVERSE";
})(DmMode = exports.DmMode || (exports.DmMode = {}));
