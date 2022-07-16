const video = require("./video");

var v = new video.Video({
    aid: 2
});

v.get_info().then(
    function (value) {
        console.log(value);
    }
)