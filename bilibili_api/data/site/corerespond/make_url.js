"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
exports.defaultFunc = exports.encrypt = void 0;
var fs = require("fs");
var path_1 = require("path");
var util_1 = require("util");
var e;
var n = [];
function o(e) {
    return n[e];
}
var i = 0, a;
function getA() {
    if (!a) {
        a = new Uint8Array(e.memory.buffer);
    }
    return a;
}
var f = new util_1.TextEncoder();
function u(e, n) {
    var a = f.encodeInto(e, n);
    return a;
}
function l(e, malloc, realloc) {
    if (!realloc) {
        var t = f.encode(e), r_1 = malloc(t.length);
        i = t.length;
        return r_1;
    }
    var r = e.length, o = malloc(r);
    var a = getA();
    var l = 0;
    for (; l < r; l++) {
        var n_1 = e.charCodeAt(l);
        if (n_1 > 127)
            break;
        a[o + l] = n_1;
    }
    if (l !== r) {
        if (l !== 0) {
            e = e.slice(l);
            var temp_r = l + 3 * e.length;
            o = realloc(o, r, temp_r);
            r = temp_r;
        }
        var n_2 = getA().subarray(o + l, o + r);
        l += u(e, n_2).written;
    }
    i = l;
    return o;
}
var s;
function getS() {
    if (!s || s.buffer !== e.memory.buffer) {
        s = new Int32Array(e.memory.buffer);
    }
    return s;
}
var b = n.length;
var d = new TextDecoder('utf-8');
function g(e, n) {
    return d.decode(getA().subarray(e, e + n));
}
function w(e) {
    b === n.length && n.push(n.length + 1);
    var t = b;
    b = n[t];
    n[t] = e;
    return t;
}
function encrypt(params) {
    try {
        var a_1 = w(params);
        e.encrypt(8, a_1);
        return g(getS()[2], getS()[3]);
    }
    finally {
        // e.__wbindgen_free(t1, wasmInit);
    }
}
exports.encrypt = encrypt;
function emptyFunc() {
    return;
}
function defaultFunc() {
    return __awaiter(this, void 0, void 0, function () {
        var importObject, instance;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    importObject = { wbg: {} };
                    importObject.wbg.__wbindgen_json_serialize = function (n, t) {
                        var a = l(JSON.stringify(o(t) || null), e.__wbindgen_malloc, e.__wbindgen_realloc);
                        getS()[n / 4 + 1] = i;
                        getS()[n / 4 + 0] = a;
                    };
                    importObject.wbg.__wbg_self_1b7a39e3a92c949c = emptyFunc;
                    importObject.wbg.__wbg_log_da30ae7b677263c7 = emptyFunc;
                    importObject.wbg.__wbindgen_object_drop_ref = emptyFunc;
                    importObject.wbg.__wbg_new_59cb74e423758ede = emptyFunc;
                    importObject.wbg.__wbg_stack_558ba5917b466edd = function (n, t) {
                        var r = l(o(t).stack, e.__wbindgen_malloc, e.__wbindgen_realloc), a = i;
                        getS()[n / 4 + 1] = a;
                        getS()[n / 4 + 0] = r;
                    };
                    importObject.wbg.__wbg_error_4bb6c2a97407129a = emptyFunc;
                    importObject.wbg.__wbg_randomFillSync_d5bd2d655fdf256a = emptyFunc;
                    importObject.wbg.__wbg_getRandomValues_f5e14ab7ac8e995d = emptyFunc;
                    importObject.wbg.__wbg_crypto_968f1772287e2df0 = emptyFunc;
                    importObject.wbg.__wbindgen_is_undefined = emptyFunc;
                    importObject.wbg.__wbg_getRandomValues_a3d34b4fee3c2869 = emptyFunc;
                    importObject.wbg.__wbg_require_604837428532a733 = emptyFunc;
                    return [4 /*yield*/, WebAssembly.instantiate(fs.readFileSync(path_1.resolve(__dirname, './encrypt.wasm')), importObject)];
                case 1:
                    instance = (_a.sent()).instance;
                    e = instance.exports;
                    return [2 /*return*/, e];
            }
        });
    });
}
exports.defaultFunc = defaultFunc;

async function get_url() {
    await defaultFunc();
    const correspondPath = encrypt({
        data: convertToHex(`refresh_${Date.now()}`),
        digest: 'SHA256',
    });

    const URL = 'https://www.bilibili.com/correspond/1/' + correspondPath;

    function convertToHex(str) {
        return str.split('').reduce((i, t) => i + t.charCodeAt(0).toString(16), '');
    }
    return URL;
}

exports.get_url = get_url
