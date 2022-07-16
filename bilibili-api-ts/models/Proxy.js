"use strict";
exports.__esModule = true;
exports.Proxy = void 0;
var Proxy = /** @class */ (function () {
    function Proxy(config) {
        var host = config.host;
        var port = config.port;
        var username = config.username;
        var password = config.password;
        this.hostname = host;
        this.port = port;
        this.username = username;
        this.password = password;
    }
    return Proxy;
}());
exports.Proxy = Proxy;
