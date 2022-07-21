import { readDoubleLE, readDoubleBE, readFloatBE, readFloatLE } from "@protobufjs/float";
import { read_varint } from "../utils/varint";

export class BytesReader {
    __stream: Buffer
    __offset: number

    constructor({stream}: {stream: Buffer}) {
        this.__stream = stream;
        this.__offset = 0;
    }

    has_end() {
        return this.__offset >= this.__stream.length
    }

    double(LE: boolean=false) {
        var data = this.__stream.subarray(this.__offset, this.__offset + 8);
        if (LE === false) {
            var result = readDoubleBE(data, 0);
        }
        else {
            var result = readDoubleLE(data, 0)
        }
        this.__offset += 8;
        return result;
    }

    float(LE: boolean=false) {
        var data = this.__stream.subarray(this.__offset, this.__offset + 4);
        if (LE === false) {
            var result = readFloatBE(data, 0);
        }
        else {
            var result = readFloatLE(data, 0);
        }
        this.__offset += 4;
        return result;
    }

    varint() {
        var [d, l] = read_varint({stream: this.__stream.subarray(this.__offset, this.__stream.length)});
        console.log(d, l);
        this.__offset += l;
        return d;
    }

    byte() {
        var data = this.__stream.subarray(this.__offset);
        this.__offset += 1;
        return data;
    }

    string() {
        var length = this.varint();
        var data = this.__stream.subarray(this.__offset, this.__offset + length);
        this.__offset == length;
        return data.toString('utf-8');
    }

    bool() {
        var data = this.__stream[this.__offset];
        this.__offset += 1;
        return data === 1;
    }

    bytes_string() {
        var length = this.varint();
        var data = this.__stream.subarray(this.__offset, this.__offset + length);
        this.__offset += length;
        return data;
    }

    set_pos(pos: number) {
        if (pos < 0) {
            throw "读取位置不能小于 0"
        }
        if (pos >= this.__stream.length) {
            throw "读取位置超过字节流长度"
        }
        this.__offset = pos;
    }

    get_pos() {
        return this.__offset;
    }
}