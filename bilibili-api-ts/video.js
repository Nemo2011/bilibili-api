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
exports.Video = void 0;
var Credential_1 = require("./models/Credential");
var aid2bvid_1 = require("./utils/aid2bvid");
var network_1 = require("./utils/network");
var video_1 = require("./apis/video");
var API = video_1.VideoData;
var Video = /** @class */ (function () {
    /**
     * param bvid(int)              Bvid(可选)
     *
     * param aid(int)               Aid(可选)
     *
     * param credential(Credential) 凭据类(可选)
     */
    function Video(_a) {
        var _b = _a.bvid, bvid = _b === void 0 ? null : _b, _c = _a.aid, aid = _c === void 0 ? null : _c, _d = _a.credential, credential = _d === void 0 ? new Credential_1.Credential({}) : _d;
        this.__info = null;
        this.__bvid = "";
        this.__aid = 0;
        this.credential = new Credential_1.Credential({});
        if (credential === null && credential === undefined) {
            credential = new Credential_1.Credential({});
        }
        if (bvid !== null && bvid !== undefined) {
            this.set_bvid({ bvid: bvid });
        }
        else if (aid !== null && aid !== undefined) {
            this.set_aid({ aid: aid });
        }
        else {
            throw "请至少提供 bvid 和 aid 中的其中一个参数。";
        }
        this.credential = credential;
    }
    /**
     * 设置 bvid
     *
     * param bvid(string) Bvid
     */
    Video.prototype.set_bvid = function (_a) {
        var bvid = _a.bvid;
        if (bvid.length !== 12) {
            throw "bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。";
        }
        if (bvid.indexOf("BV") !== 0) {
            throw "bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。";
        }
        this.__bvid = bvid;
        this.__aid = (0, aid2bvid_1.bvid2aid)({ bvid: bvid });
    };
    /**
     * 获取 bvid
     *
     * @returns Bvid
     */
    Video.prototype.get_bvid = function (_a) {
        return this.__bvid;
    };
    /**
     * 设置 aid
     *
     * param aid(number) Aid
     */
    Video.prototype.set_aid = function (_a) {
        var aid = _a.aid;
        if (aid <= 0) {
            throw "aid 不能小于或等于 0。";
        }
        this.__aid = aid;
        this.__bvid = (0, aid2bvid_1.aid2bvid)({ aid: aid });
    };
    /**
     * 获取 aid
     *
     * @returns aid
     */
    Video.prototype.get_aid = function (_a) {
        return this.__aid;
    };
    /**
     * 获取视频详细信息
     *
     * @returns 调用 API 返回的结果
     */
    Video.prototype.get_info = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            var api, params, resp;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        api = API["info"]["detail"];
                        params = {
                            "bvid": this.get_bvid({}),
                            "aid": this.get_aid({})
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api['url'],
                                params: params,
                                credential: this.credential
                            })];
                    case 1:
                        resp = _b.sent();
                        this.__info = resp;
                        return [2 /*return*/, resp];
                }
            });
        });
    };
    /**
     * 获取视频详细信息的内存中的缓存数据
     *
     * @returns 调用 API 返回的结果
     */
    Video.prototype.__get_info_cached = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (!(this.__info === null)) return [3 /*break*/, 2];
                        return [4 /*yield*/, this.get_info({})];
                    case 1: return [2 /*return*/, _b.sent()];
                    case 2: return [2 /*return*/, this.__info];
                }
            });
        });
    };
    /**
     * 获取视频统计数据
     *
     * @returns 调用 API 返回的结果
     */
    Video.prototype.get_stat = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            var api, params;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        api = API['info']['stat'];
                        params = {
                            "bvid": this.get_bvid({}),
                            "aid": this.get_aid({})
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api['url'],
                                params: params,
                                credential: this.credential
                            })];
                    case 1: return [2 /*return*/, _b.sent()];
                }
            });
        });
    };
    /**
     * 获取视频标签
     *
     * @returns 调用 API 返回的结果
     */
    Video.prototype.get_tags = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            var api, params;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        api = API['info']['tags'];
                        params = {
                            "bvid": this.get_bvid({}),
                            "aid": this.get_aid({})
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api['url'],
                                params: params,
                                credential: this.credential
                            })];
                    case 1: return [2 /*return*/, _b.sent()];
                }
            });
        });
    };
    /**
     * 获取视频充电信息
     *
     * @returns 调用 API 返回的结果
     */
    Video.prototype.get_chargers = function () {
        return __awaiter(this, void 0, void 0, function () {
            var info, mid, api, params;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.__get_info_cached({})];
                    case 1:
                        info = _a.sent();
                        mid = info['owner']['mid'];
                        api = API['info']['chargers'];
                        params = {
                            "aid": this.get_aid({}),
                            "bvid": this.get_bvid({}),
                            "mid": mid
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api['url'],
                                params: params,
                                credential: this.credential
                            })];
                    case 2: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    /**
     * 获取视频分 P 信息
     *
     * @returns 调用 API 返回的结果
     */
    Video.prototype.get_pages = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            var api, params;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        api = API["info"]["pages"];
                        params = {
                            "aid": this.get_aid({}),
                            "bvid": this.get_bvid({})
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api['url'],
                                params: params,
                                credential: this.credential
                            })];
                    case 1: return [2 /*return*/, _b.sent()];
                }
            });
        });
    };
    /**
     * 获取分 P 对应的 cid
     *
     * param page_index(int) 分 P 序号
     *
     * @returns number: cid
     */
    Video.prototype.__get_page_id_by_index = function (page_index) {
        return __awaiter(this, void 0, void 0, function () {
            var info, pages, page, cid;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (page_index < 0) {
                            throw "分 p 号必须大于或等于 0。";
                        }
                        return [4 /*yield*/, this.__get_info_cached({})];
                    case 1:
                        info = _a.sent();
                        pages = info['pages'];
                        if (pages.length <= 0) {
                            throw "不存在该分 p。";
                        }
                        page = pages[page_index];
                        cid = page['cid'];
                        return [2 /*return*/, cid];
                }
            });
        });
    };
    /**
     * 获取分 P 对应的 cid
     *
     * param page_index(number) 分 P 序号
     *
     * @returns number: cid
     */
    Video.prototype.get_cid = function (_a) {
        var page_index = _a.page_index;
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (page_index === null || page_index === undefined) {
                            page_index = 0;
                        }
                        return [4 /*yield*/, this.__get_page_id_by_index(page_index)];
                    case 1: return [2 /*return*/, _b.sent()];
                }
            });
        });
    };
    /**
     * 获取视频播放流（下载地址）
     *
     * param page_index(number) 分 P 序号(可选)
     *
     * param cid(number)        分 P 编号(可选)
     *
     * param html5(boolean)     是否以 html5 端获取（这样子可以直接在网页中显示，但是视频源单一）(可选)
     *
     * page_index 和 cid 请务必提供一个。
     *
     * @returns 调用 API 返回的结果
     */
    Video.prototype.get_download_url = function (_a) {
        var _b = _a.page_index, page_index = _b === void 0 ? null : _b, _c = _a.cid, cid = _c === void 0 ? null : _c, _d = _a.html5, html5 = _d === void 0 ? false : _d;
        return __awaiter(this, void 0, void 0, function () {
            var api, params;
            return __generator(this, function (_e) {
                switch (_e.label) {
                    case 0:
                        if (!(cid === null || cid === undefined)) return [3 /*break*/, 3];
                        if (!(page_index === null || page_index === undefined)) return [3 /*break*/, 1];
                        throw "page_index 和 cid 至少提供一个。";
                    case 1: return [4 /*yield*/, this.__get_page_id_by_index(page_index)];
                    case 2:
                        cid = _e.sent();
                        _e.label = 3;
                    case 3:
                        api = API['info']['playurl'];
                        params = {
                            "avid": this.get_aid({}),
                            "cid": cid,
                            "qn": "127",
                            "otype": "json",
                            "fnval": 4048,
                            "fourk": 1
                        };
                        if (html5 === true) {
                            params['platform'] = 'html5';
                        }
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api['url'],
                                params: params,
                                credential: this.credential
                            })];
                    case 4: return [2 /*return*/, _e.sent()];
                }
            });
        });
    };
    /**
     * 获取相关视频信息
     *
     * @returns {Object} 调用 API 返回的结果
     */
    Video.prototype.get_related = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            var api, params;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        api = API.info.related;
                        params = {
                            aid: this.get_aid({}),
                            bvid: this.get_bvid({})
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api["url"],
                                params: params,
                                credential: this.credential
                            })];
                    case 1: return [2 /*return*/, _b.sent()];
                }
            });
        });
    };
    /**
     * 视频是否点赞过
     *
     * @returns {bool} 视频是否点赞过
     */
    Video.prototype.has_liked = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            var api, params;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.credential.raise_for_no_sessdata({});
                        api = API.info.has_liked;
                        params = {
                            bvid: this.get_bvid({}),
                            aid: this.get_aid({})
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api.url,
                                params: params,
                                credential: this.credential
                            })];
                    case 1: return [2 /*return*/, (_b.sent()) === 1];
                }
            });
        });
    };
    /**
     * 获取视频已投币数量
     *
     * @returns {number} 视频已投币数量
     */
    Video.prototype.get_pay_coins = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            var api, params;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.credential.raise_for_no_sessdata({});
                        api = API.info.get_pay_coins;
                        params = {
                            bvid: this.get_bvid({}),
                            aid: this.get_aid({})
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api.url,
                                params: params,
                                credential: this.credential
                            })];
                    case 1: return [2 /*return*/, (_b.sent())['multiply']];
                }
            });
        });
    };
    /**
     * 是否已收藏
     *
     * @returns {bool} 视频是否已收藏
     */
    Video.prototype.has_favoured = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            var api, params;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.credential.raise_for_no_sessdata({});
                        api = API.info.has_favoured;
                        params = {
                            bvid: this.get_bvid({}),
                            aid: this.get_aid({})
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api.url,
                                params: params,
                                credential: this.credential
                            })];
                    case 1: return [2 /*return*/, (_b.sent())['favoured']];
                }
            });
        });
    };
    /**
     * 获取收藏夹列表信息，用于收藏操作，含各收藏夹对该视频的收藏状态。
     *
     * @returns {Object} 调用 API 返回的结果
     */
    Video.prototype.get_media_list = function (_a) {
        return __awaiter(this, void 0, void 0, function () {
            var info, api, params;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.credential.raise_for_no_sessdata({});
                        return [4 /*yield*/, this.__get_info_cached({})];
                    case 1:
                        info = _b.sent();
                        api = API.info.media_list;
                        params = {
                            type: 2,
                            rid: this.get_aid({}),
                            up_mid: info.owner.mid
                        };
                        return [4 /*yield*/, (0, network_1.request)({
                                method: "GET",
                                url: api.url,
                                params: params,
                                credential: this.credential
                            })];
                    case 2: return [2 /*return*/, _b.sent()];
                }
            });
        });
    };
    /**
     * 获取高能进度条
     *
     * param page_index(number) 分 P 序号(可选)
     *
     * param cid(number)        分 P 编号(可选)
     *
     * @returns {Object} 调用 API 返回的结果
     */
    Video.prototype.get_pbp = function (_a) {
        var _b = _a.page_index, page_index = _b === void 0 ? null : _b, _c = _a.cid, cid = _c === void 0 ? null : _c;
        return __awaiter(this, void 0, void 0, function () {
            var api, params, sess;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        if (!(cid === null || cid === undefined)) return [3 /*break*/, 3];
                        if (!(page_index === null || page_index === undefined)) return [3 /*break*/, 1];
                        throw "page_index 和 cid 至少提供一个。";
                    case 1: return [4 /*yield*/, this.__get_page_id_by_index(page_index)];
                    case 2:
                        cid = _d.sent();
                        _d.label = 3;
                    case 3:
                        api = API.info.pbp;
                        params = {
                            cid: cid
                        };
                        return [4 /*yield*/, (0, network_1.get_session)({ credential: this.credential })];
                    case 4:
                        sess = _d.sent();
                        return [4 /*yield*/, sess];
                    case 5: return [4 /*yield*/, (_d.sent()).request({
                            url: api.url,
                            method: "GET",
                            params: params
                        })];
                    case 6: return [2 /*return*/, (_d.sent()).data];
                }
            });
        });
    };
    return Video;
}());
exports.Video = Video;
