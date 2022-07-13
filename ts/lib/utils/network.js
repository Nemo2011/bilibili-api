"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getAxiosInstance = exports.cookieJar = void 0;
const tough_cookie_1 = require("tough-cookie");
const crypto_1 = __importDefault(require("crypto"));
const axios_1 = __importDefault(require("axios"));
const axios_cookiejar_support_1 = require("axios-cookiejar-support");
const Credential_1 = require("../models/Credential");
exports.cookieJar = new tough_cookie_1.CookieJar();
async function getAxiosInstance(credential = new Credential_1.CookiesCredential(), proxy = null) {
    if (credential.sessdata !== null) {
        exports.cookieJar.setCookieSync(`sessdata=${credential.sessdata}; Domain=.bilibili.com`, 'https://www.bilibili.com');
    }
    if (credential.bili_jct !== null) {
        exports.cookieJar.setCookieSync(`bili_jct=${credential.bili_jct}; Domain=.bilibili.com`, 'https://www.bilibili.com');
    }
    if (credential.dedeuserid !== null) {
        exports.cookieJar.setCookieSync(`DedeUserID=${credential.dedeuserid}; Domain=.bilibili.com`, 'https://www.bilibili.com');
    }
    exports.cookieJar.setCookieSync(`buvid3=${crypto_1.default.randomUUID()}; Domain=.bilibili.com`, 'https://www.bilibili.com/');
    return (0, axios_cookiejar_support_1.wrapper)(axios_1.default.create({
        headers: {
            'user-agent': 'Mozilla/5.0',
            referer: 'https://www.bilibili.com/',
        },
        jar: exports.cookieJar,
        responseType: 'json',
        proxy: proxy
            ? {
                host: proxy.hostname,
                port: parseInt(proxy.port),
                auth: proxy.username && proxy.password
                    ? {
                        username: proxy.username,
                        password: proxy.password,
                    }
                    : undefined,
            }
            : false,
    }));
}
exports.getAxiosInstance = getAxiosInstance;
;
