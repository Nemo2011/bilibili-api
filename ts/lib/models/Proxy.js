"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Proxy = void 0;
class Proxy {
    hostname;
    port;
    username;
    password;
    constructor(host, port, username = null, password = null) {
        this.hostname = host;
        this.port = port;
        this.username = username;
        this.password = password;
    }
}
exports.Proxy = Proxy;
