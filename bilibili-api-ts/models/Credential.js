"use strict";
exports.__esModule = true;
exports.Credential = void 0;
var Credential = /** @class */ (function () {
    function Credential(_a) {
        var _b = _a.sessdata, sessdata = _b === void 0 ? "" : _b, _c = _a.bili_jct, bili_jct = _c === void 0 ? "" : _c, _d = _a.dedeuserid, dedeuserid = _d === void 0 ? "" : _d;
        this.sessdata = null;
        this.bili_jct = null;
        this.dedeuserid = null;
        this.sessdata = sessdata;
        this.bili_jct = bili_jct;
        this.dedeuserid = dedeuserid;
    }
    Credential.prototype.raise_for_no_sessdata = function (_a) {
        if (this.sessdata === "")
            throw "Credential 类需要 sessdata";
    };
    Credential.prototype.raise_for_no_bili_jct = function (_a) {
        if (this.bili_jct === "")
            throw "Credential 类需要 bili_jct";
    };
    Credential.prototype.raise_for_no_dedeuserid = function (_a) {
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
