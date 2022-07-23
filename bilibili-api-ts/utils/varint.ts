export function read_varint({stream}: {stream:Uint8Array}) {
    var value = 0;
    var position = 0;
    var shift = 0;
    while (true) {
        if (position >= stream.length) {
            break;
        }
        var byte = stream.at(position);
        value += (byte & 127) << shift;
        if ((byte & 128) === 0) {
            break;
        }
        position += 1;
        shift += 7;
    }
    return [value, position + 1];
}