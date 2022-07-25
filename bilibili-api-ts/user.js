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
exports.User = exports.VideoOrder = void 0;
var Credential_1 = require("./models/Credential");
var network_1 = require("./utils/network");
var user_1 = require("./apis/user");
var API = user_1.UserAPIData;
/**
 * 视频排序顺序。
 *
 * + PUBDATE : 上传日期倒序。
 *
 * + FAVORITE: 收藏量倒序。
 *
 * + VIEW    : 播放量倒序。
 */
var VideoOrder;
(function (VideoOrder) {
    VideoOrder["PUBDATE"] = "pubdate";
    VideoOrder["FAVORITE"] = "stow";
    VideoOrder["VIEW"] = "click";
})(VideoOrder = exports.VideoOrder || (exports.VideoOrder = {}));
/**
 * 用户相关
 */
var User = /** @class */ (function () {
    /**
     * uid(number)           : 用户 uid
     *
     * credential(Credential): 凭据类
     */
    function User(_a) {
        var uid = _a.uid, _b = _a.credential, credential = _b === void 0 ? new Credential_1.Credential({}) : _b;
        this.credential = new Credential_1.Credential({});
        this.__self_info = null;
        this.uid = uid;
        if (credential === null || credential === undefined) {
            credential = new Credential_1.Credential({});
        }
        this.credential = credential;
        this.__self_info = null;
    }
    /**
     * 获取用户信息（昵称，性别，生日，签名，头像 URL，空间横幅 URL 等）
     *
     * @returns {Object} 调用 API 返回的结果
     */
    User.prototype.get_user_info = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            var api, params;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        api = API.info.info;
                        params = {
                            mid: this.uid
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api.url,
                                params: params,
                                credential: this.credential
                            })];
                    case 1: return [2 /*return*/, _b.sent()];
                }
            });
        });
    };
    /**
     * 获取用户 uid
     *
     * @returns {number} 用户 uid
     */
    User.prototype.get_uid = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_b) {
                return [2 /*return*/, this.uid];
            });
        });
    };
    return User;
}());
exports.User = User;
