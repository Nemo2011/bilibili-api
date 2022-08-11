"use strict";
exports.__esModule = true;
exports.get_channel_info_by_name = exports.get_channel_info_by_tid = void 0;
var channel_1 = require("./data/channel");
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
