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
        while (_) try {
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
exports.setProxy = exports.request = void 0;
var tough_cookie_1 = require("tough-cookie");
var crypto = require("crypto");
var axios_1 = require("axios");
var axios_cookiejar_support_1 = require("axios-cookiejar-support");
var Credential_1 = require("../models/Credential");
var cookieJar = new tough_cookie_1.CookieJar();
var sess = null;
var user_proxy = null;
function getAxiosInstance(credential, proxy) {
    if (credential === void 0) { credential = new Credential_1.Credential(); }
    if (proxy === void 0) { proxy = null; }
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            if (credential.sessdata !== null) {
                cookieJar.setCookieSync("SESSDATA=".concat(credential.sessdata, "; Domain=.bilibili.com"), 'https://www.bilibili.com');
            }
            if (credential.bili_jct !== null) {
                cookieJar.setCookieSync("bili_jct=".concat(credential.bili_jct, " Domain=.bilibili.com"), 'https://www.bilibili.com');
            }
            if (credential.dedeuserid !== null) {
                cookieJar.setCookieSync("DedeUserID=".concat(credential.dedeuserid, "; Domain=.bilibili.com"), 'https://www.bilibili.com');
            }
            cookieJar.setCookieSync("buvid3=".concat(crypto.randomUUID(), "; Domain=.bilibili.com"), 'https://www.bilibili.com');
            // console.log(cookieJar.getCookieString("https://api.bilibili.com"));
            sess = (0, axios_cookiejar_support_1.wrapper)(axios_1["default"].create({
                headers: {
                    'user-agent': 'Mozilla/5.0',
                    referer: 'https://www.bilibili.com/'
                },
                // withCredentials: true, 
                jar: cookieJar,
                responseType: 'json',
                proxy: proxy
                    ? {
                        host: proxy.hostname,
                        port: parseInt(proxy.port),
                        auth: proxy.username && proxy.password
                            ? {
                                username: proxy.username,
                                password: proxy.password
                            }
                            : undefined
                    }
                    : false
            }));
            return [2 /*return*/, sess];
        });
    });
}
;
function setAxiosInstance(axios) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            sess = axios;
            return [2 /*return*/];
        });
    });
}
function request(request_config) {
    return __awaiter(this, void 0, void 0, function () {
        var method, url, params, data, credential, no_csrf, DEFAULT_HEADERS, headers, cookies, config, resp, has_content_type, resp_data, code, msg, real_data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    method = request_config.method;
                    url = request_config.url;
                    params = request_config.params;
                    data = request_config.data;
                    credential = request_config.credential;
                    no_csrf = request_config.no_csrf;
                    if (no_csrf === null || no_csrf === undefined) {
                        no_csrf = false;
                    }
                    if (credential === null || credential === undefined) {
                        credential = new Credential_1.Credential();
                    }
                    method = method.toUpperCase();
                    if (method !== "GET" && !no_csrf) {
                        credential.raise_for_no_bili_jct();
                    }
                    DEFAULT_HEADERS = {
                        "Referer": "https://www.bilibili.com",
                        "User-Agent": "Mozilla/5.0"
                    };
                    headers = DEFAULT_HEADERS;
                    if (!no_csrf && method in ["POST", "DELETE", "PATCH"]) {
                        if (data === null) {
                            data = {};
                        }
                        data["csrf"] = credential.bili_jct;
                        data["csrf_token"] = credential.bili_jct;
                    }
                    if (params === null) {
                        params = {};
                    }
                    if (params['jsonp'] !== undefined) {
                        params["callback"] = "callback";
                    }
                    cookies = credential.get_cookies();
                    config = {
                        "method": method,
                        "url": url,
                        "params": params,
                        "data": data,
                        "headers": headers,
                        "cookies": cookies
                    };
                    if (!(user_proxy !== null)) return [3 /*break*/, 2];
                    return [4 /*yield*/, getAxiosInstance(credential, user_proxy)];
                case 1:
                    _a.sent();
                    return [3 /*break*/, 4];
                case 2: return [4 /*yield*/, getAxiosInstance(credential)];
                case 3:
                    _a.sent();
                    _a.label = 4;
                case 4: return [4 /*yield*/, sess];
                case 5: return [4 /*yield*/, (_a.sent()).request(config)];
                case 6:
                    resp = _a.sent();
                    has_content_type = resp.headers['content-type'] ? true : false;
                    if (!has_content_type)
                        return [2 /*return*/];
                    if (resp.headers['content-type'].toLowerCase().indexOf("application/json") === -1) {
                        throw "响应不是 application/json 类型";
                    }
                    resp_data = resp['data'];
                    code = resp_data['code'];
                    if (code === null) {
                        throw "API 返回数据未含 code 字段";
                    }
                    if (code !== 0) {
                        msg = resp_data['message'];
                        if (msg === undefined) {
                            msg = "接口未返回错误信息";
                        }
                        throw msg;
                    }
                    real_data = resp_data['data'];
                    if (real_data === undefined) {
                        real_data = resp_data['result'];
                    }
                    return [2 /*return*/, real_data];
            }
        });
    });
}
exports.request = request;
function setProxy(proxy) {
    user_proxy = proxy;
}
exports.setProxy = setProxy;
