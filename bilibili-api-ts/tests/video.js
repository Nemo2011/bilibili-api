"use strict";
exports.__esModule = true;
exports.test_video = void 0;
var video_1 = require("../video");
var index_1 = require("../index");
function test_video() {
    var v = new video_1.Video({
        aid: 2,
        credential: new index_1.Credential({
            sessdata: "49fe124a%2C1673004720%2C86384%2A71"
        })
    });
    v.get_info().then(function (value) {
        console.log("get_info()");
    });
    v.get_stat().then(function (value) {
        console.log("get_stat()");
    });
    v.get_tags().then(function (value) {
        console.log("get_tags()");
    });
    // v.get_chargers().then(function (value) {
    //     console.log("get_chargers()");
    //     console.log(value);
    // })
    v.get_pages().then(function (value) {
        console.log("get_pages()");
    });
    v.get_download_url({
        page_index: 0
    }).then(function (value) {
        console.log("get_download_url()");
        console.log(value);
    });
}
exports.test_video = test_video;
