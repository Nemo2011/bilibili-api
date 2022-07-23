"use strict";
exports.__esModule = true;
exports.BytesReader = void 0;
var float_1 = require("@protobufjs/float");
var varint_1 = require("../utils/varint");
var BytesReader = /** @class */ (function () {
    function BytesReader(_a) {
        var stream = _a.stream;
        this.__stream = stream;
        this.__offset = 0;
    }
    BytesReader.prototype.has_end = function () {
        return this.__offset >= this.__stream.length;
    };
    BytesReader.prototype.double = function (LE) {
        if (LE === void 0) { LE = false; }
        var data = this.__stream.subarray(this.__offset, this.__offset + 8);
        if (LE === false) {
            var result = (0, float_1.readDoubleBE)(data, 0);
        }
        else {
            var result = (0, float_1.readDoubleLE)(data, 0);
        }
        this.__offset += 8;
        return result;
    };
    BytesReader.prototype.float = function (LE) {
        if (LE === void 0) { LE = false; }
        var data = this.__stream.subarray(this.__offset, this.__offset + 4);
        if (LE === false) {
            var result = (0, float_1.readFloatBE)(data, 0);
        }
        else {
            var result = (0, float_1.readFloatLE)(data, 0);
        }
        this.__offset += 4;
        return result;
    };
    BytesReader.prototype.varint = function () {
        var _a = (0, varint_1.read_varint)({ stream: this.__stream.subarray(this.__offset, this.__stream.length) }), d = _a[0], l = _a[1];
        this.__offset += l;
        return d;
    };
    BytesReader.prototype.byte = function () {
        var data = this.__stream.subarray(this.__offset);
        this.__offset += 1;
        return data;
    };
    BytesReader.prototype.string = function () {
        var length = this.varint();
        var data = this.__stream.subarray(this.__offset, this.__offset + length);
        this.__offset == length;
        return data.toString('utf-8');
    };
    BytesReader.prototype.bool = function () {
        var data = this.__stream[this.__offset];
        this.__offset += 1;
        return data === 1;
    };
    BytesReader.prototype.bytes_string = function () {
        var length = this.varint();
        var data = this.__stream.subarray(this.__offset, this.__offset + length);
        this.__offset += length;
        return data;
    };
    BytesReader.prototype.set_pos = function (pos) {
        if (pos < 0) {
            throw "读取位置不能小于 0";
        }
        if (pos >= this.__stream.length) {
            throw "读取位置超过字节流长度";
        }
        this.__offset = pos;
    };
    BytesReader.prototype.get_pos = function () {
        return this.__offset;
    };
    return BytesReader;
}());
exports.BytesReader = BytesReader;
