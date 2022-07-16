"use strict";
exports.__esModule = true;
exports.aid2bvid = exports.bvid2aid = void 0;
var table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF", tr = {};
for (var i = 0; i < 58; i++) {
    tr[table[i]] = i;
}
var s = [11, 10, 3, 8, 4, 6], xor = 177451812, add = 8728348608;
function bvid2aid(config) {
    var bvid = config.bvid;
    var r = 0;
    for (var i = 0; i < 6; i++) {
        r += tr[bvid[s[i]]] * Math.pow(58, i);
    }
    return ((r - add) ^ xor);
}
exports.bvid2aid = bvid2aid;
function aid2bvid(config) {
    var aid = config.aid;
    aid = (aid ^ xor) + add;
    var r = "BV1  4 1 7  ".split("");
    for (var i = 0; i < 6; i++) {
        r[s[i]] = table[Math.floor(aid / Math.pow(58, i)) % 58];
    }
    return r.join("");
}
exports.aid2bvid = aid2bvid;
