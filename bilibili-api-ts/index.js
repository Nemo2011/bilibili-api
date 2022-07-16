"use strict";
exports.__esModule = true;
exports.help = exports.HEADERS = exports.Credential = exports.Proxy = exports.bvid2aid = exports.aid2bvid = exports.setProxy = void 0;
var network_1 = require("./utils/network");
exports.setProxy = network_1.setProxy;
var aid2bvid_1 = require("./utils/aid2bvid");
exports.aid2bvid = aid2bvid_1.aid2bvid;
exports.bvid2aid = aid2bvid_1.bvid2aid;
var Proxy_1 = require("./models/Proxy");
exports.Proxy = Proxy_1.Proxy;
var Credential_1 = require("./models/Credential");
exports.Credential = Credential_1.Credential;
var HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com"
};
exports.HEADERS = HEADERS;
function help() {
    var config = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        config[_i] = arguments[_i];
    }
    console.log("欢迎来到 bilibili-api-ts，这个模块是 Python bilibili-api 的 Typescript 克隆，适用于 JS/TS。\n文档请前往 https://nemo2011.github.io/bilibili_api/#/README-ts 查看。");
}
exports.help = help;
