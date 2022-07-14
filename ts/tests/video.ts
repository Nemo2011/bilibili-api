import { Video } from "../video";

export function test_video() {
    var v = new Video(null, 2);
    v.get_info().then(function ( value) {
        console.log(value);
    })
}
