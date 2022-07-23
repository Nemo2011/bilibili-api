"use strict";
exports.__esModule = true;
exports.Proxy = void 0;
var Proxy = /** @class */ (function () {
    function Proxy(_a) {
        var host = _a.host, port = _a.port, username = _a.username, password = _a.password;
        this.hostname = host;
        this.port = port;
        this.username = username;
        this.password = password;
    }
    return Proxy;
}());
exports.Proxy = Proxy;
