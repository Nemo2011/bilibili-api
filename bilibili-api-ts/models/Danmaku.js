"use strict";
exports.__esModule = true;
exports.DmMode = exports.DmFontSize = exports.Danmaku = void 0;
var Danmaku = /** @class */ (function () {
    function Danmaku(_a) {
        var text = _a.text, _b = _a.dm_time, dm_time = _b === void 0 ? 0 : _b, _c = _a.send_time, send_time = _c === void 0 ? 0 : _c, _d = _a.crc32_id, crc32_id = _d === void 0 ? "" : _d, _e = _a.color, color = _e === void 0 ? "ffffff" : _e, _f = _a.weight, weight = _f === void 0 ? -1 : _f, _g = _a.id, id = _g === void 0 ? -1 : _g, _h = _a.id_str, id_str = _h === void 0 ? "" : _h, _j = _a.action, action = _j === void 0 ? -1 : _j, _k = _a.mode, mode = _k === void 0 ? DmMode.FLY : _k, _l = _a.font_size, font_size = _l === void 0 ? DmFontSize.NORMAL : _l, _m = _a.is_sub, is_sub = _m === void 0 ? false : _m, _o = _a.pool, pool = _o === void 0 ? 0 : _o, _p = _a.attr, attr = _p === void 0 ? -1 : _p;
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
