"use strict";
exports.__esModule = true;
exports.Credential = void 0;
var Credential = /** @class */ (function () {
    function Credential(config) {
        if (config === void 0) { config = null; }
        this.sessdata = null;
        this.bili_jct = null;
        this.dedeuserid = null;
        if (config !== null) {
            var sessdata = config.sessdata;
            var bili_jct = config.bili_jct;
            var dedeuserid = config.dedeuserid;
            this.sessdata = sessdata;
            this.bili_jct = bili_jct;
            this.dedeuserid = dedeuserid;
        }
    }
    Credential.prototype.raise_for_no_sessdata = function () {
        if (this.sessdata === "")
            throw "Credential 类需要 sessdata";
    };
    Credential.prototype.raise_for_no_bili_jct = function () {
        if (this.bili_jct === "")
            throw "Credential 类需要 bili_jct";
    };
    Credential.prototype.raise_for_no_dedeuserid = function () {
        if (this.dedeuserid === "")
            throw "Credential 类需要 dedeuserid";
    };
    Credential.prototype.get_cookies = function () {
        return {
            "SESSDATA": this.sessdata,
            "bili_jct": this.bili_jct,
            "DedeUserID": this.dedeuserid
        };
    };
    return Credential;
}());
exports.Credential = Credential;
