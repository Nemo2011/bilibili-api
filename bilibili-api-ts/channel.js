"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
exports.get_channel_list_sub = exports.get_channel_list = exports.get_top10 = exports.get_channel_info_by_name = exports.get_channel_info_by_tid = void 0;
var channel_1 = require("./data/channel");
var channel_2 = require("./apis/channel");
var Credential_1 = require("./models/Credential");
var network_1 = require("./utils/network");
/**
 * 根据 tid 获取频道信息。
 *
 * param tid(number): 频道 tid
 *
 * @returns {Object[Object, Object]} 第一项是主分区，第二项是子分区，没有时返回 None。
 */
function get_channel_info_by_tid(_a) {
    var tid = _a.tid;
    for (var _i = 0, ChannelData_1 = channel_1.ChannelData; _i < ChannelData_1.length; _i++) {
        var channel = ChannelData_1[_i];
        if (channel.tid ? false : true) {
            continue;
        }
        if (tid === Number(channel.tid)) {
            return [channel, null];
        }
        for (var _b = 0, _c = channel.sub; _b < _c.length; _b++) {
            var sub_channel = _c[_b];
            if (sub_channel.tid ? false : true) {
                continue;
            }
            if (tid === Number(sub_channel.tid)) {
                return [channel, sub_channel];
            }
        }
    }
    return [null, null];
}
exports.get_channel_info_by_tid = get_channel_info_by_tid;
/**
 * 根据频道名称获取频道信息。
 *
 * param name(string): 频道的名称
 *
 * @returns {Object[Object, Object]} 第一项是主分区，第二项是子分区，没有时返回 None。
 */
function get_channel_info_by_name(_a) {
    var name = _a.name;
    for (var _i = 0, ChannelData_2 = channel_1.ChannelData; _i < ChannelData_2.length; _i++) {
        var main_ch = ChannelData_2[_i];
        if (main_ch.name.indexOf(name) !== -1) {
            return [main_ch, null];
        }
        for (var _b = 0, _c = main_ch.sub; _b < _c.length; _b++) {
            var sub_ch = _c[_b];
            if (sub_ch.name.indexOf(name) !== -1) {
                return [main_ch, sub_ch];
            }
        }
    }
}
exports.get_channel_info_by_name = get_channel_info_by_name;
/**
 * 获取分区前十排行榜。
 *
 * param tid(number)                     : 频道的 tid
 *
 * param day(number, optional)           : 3 天排行还是 7 天排行，defaults to 7
 *
 * param credential(Credential, optional): 凭据类
 * @returns
 */
function get_top10(_a) {
    var tid = _a.tid, day = _a.day, credential = _a.credential;
    return __awaiter(this, void 0, void 0, function () {
        var api, params;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    if (credential === null || credential === undefined) {
                        credential = new Credential_1.Credential({});
                    }
                    if (day === null || day === undefined) {
                        day = 7;
                    }
                    if (day !== 3 && day !== 7) {
                        throw "参数 day 只能是 3，7。";
                    }
                    api = channel_2.ChannelData.ranking.get_top10;
                    params = {
                        rid: tid,
                        day: day
                    };
                    return [4 /*yield*/, (0, network_1.request)({
                            method: "GET",
                            url: api.url,
                            params: params,
                            credential: credential
                        })];
                case 1: return [2 /*return*/, _b.sent()];
            }
        });
    });
}
exports.get_top10 = get_top10;
/**
 * 获取所有分区的数据
 *
 * @returns {any[]} 所有分区的数据
 */
function get_channel_list(_a) {
    var channel_list = [];
    for (var _i = 0, ChannelData_3 = channel_1.ChannelData; _i < ChannelData_3.length; _i++) {
        var channel_big = ChannelData_3[_i];
        var channel_big_copy = JSON.parse(JSON.stringify(channel_big));
        delete channel_big_copy['sub'];
        channel_list.push(channel_big_copy);
        for (var _b = 0, _c = channel_big.sub; _b < _c.length; _b++) {
            var channel_sub = _c[_b];
            var channel_sub_copy = JSON.parse(JSON.stringify(channel_sub));
            channel_sub_copy['father'] = channel_big_copy;
            channel_list.push(channel_sub_copy);
        }
    }
    return channel_list;
}
exports.get_channel_list = get_channel_list;
/**
 * 获取所有分区的数据
 * 含父子关系（即一层次只有主分区）
 *
 * @returns {Object} 所有主分区的数据
 */
function get_channel_list_sub(_a) {
    return channel_1.ChannelData;
}
exports.get_channel_list_sub = get_channel_list_sub;
