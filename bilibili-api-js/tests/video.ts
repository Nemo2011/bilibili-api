import { Video } from "../video";

export function test_video() {
    var v = new Video(null, 2);
    v.get_info().then(function (value) {
        console.log("get_info()");
    })
    v.get_stat().then(function (value) {
        console.log("get_stat()");
    })
    v.get_tags().then(function (value) {
        console.log("get_tags()");
    })
    // v.get_chargers().then(function (value) {
    //     console.log("get_chargers()");
    //     console.log(value);
    // })
    v.get_pages().then(function (value) {
        console.log("get_pages()");
    })
    v.get_download_url(0).then(function (value) {
        console.log("get_download_url()");
    })
}
