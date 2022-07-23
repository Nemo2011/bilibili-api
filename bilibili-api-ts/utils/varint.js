"use strict";
exports.__esModule = true;
exports.read_varint = void 0;
function read_varint(_a) {
    var stream = _a.stream;
    var value = 0;
    var position = 0;
    var shift = 0;
    while (true) {
        if (position >= stream.length) {
            break;
        }
        var byte = stream[position];
        value += (byte & 127) << shift;
        if ((byte & 128) === 0) {
            break;
        }
        position += 1;
        shift += 7;
    }
    return [value, position + 1];
}
exports.read_varint = read_varint;
