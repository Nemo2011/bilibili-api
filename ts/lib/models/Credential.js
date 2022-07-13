"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CookiesCredential = void 0;
class CookiesCredential {
    sessdata;
    bili_jct;
    dedeuserid;
    constructor(sessdata = "", bili_jct = "", dedeuserid = "") {
        this.sessdata = sessdata;
        this.bili_jct = bili_jct;
        this.dedeuserid = dedeuserid;
    }
    raise_for_no_sessdata() {
        if (this.sessdata === "")
            throw "Credential 类需要 sessdata";
    }
    raise_for_no_bili_jct() {
        if (this.bili_jct === "")
            throw "Credential 类需要 bili_jct";
    }
    raise_for_no_dedeuserid() {
        if (this.dedeuserid === "")
            throw "Credential 类需要 dedeuserid";
    }
}
exports.CookiesCredential = CookiesCredential;
