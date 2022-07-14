import { Video } from "../video";
import { Proxy } from "../models/Proxy";
import { set_proxy } from "../utils/network";

export function test_video() {
    var p = new Proxy("177.136.84.134", "999");
    set_proxy(p);
    var v = new Video(null, 2);
    v.get_info().then(function ( value) {
        console.log(value);
    })
}
