export function read_varint(stream:Uint8Array) {
    var value = 0;
    var position = 0;
    var shift = 0;
    while (true) {
        if (position >= stream.length) {
            break;
        }
        var byte = stream[position];
        value += (byte & 0b01111111) << shift;
        if ((byte & 0b10000000) === 0) {
            break;
        }
        position += 1;
        shift += 7;
    }
    return [value, position + 1];
}