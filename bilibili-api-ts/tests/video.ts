import { Video } from "../video";
import { Credential } from "../index";

export function test_video() {
    var v = new Video(
        {
            aid: 2, 
            credential: new Credential({
                sessdata: "49fe124a%2C1673004720%2C86384%2A71"
            })
        }
    );
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
    v.get_download_url({
        page_index: 0
    }).then(function (value) {
        console.log("get_download_url()");
        console.log(value);
    })
}
