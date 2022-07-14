import { Video } from "../video";
import { Proxy } from "../models/Proxy";
import { setProxy } from "../utils/network";

export function test_video() {
    var v = new Video(null, 2);
    v.get_info().then(function ( value) {
        console.log(value);
    })
}
