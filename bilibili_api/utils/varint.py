"""
bilibili_api.utils.varint

变长数字字节相关
"""


def read_varint(stream: bytes):
    """
    读取varint
    :param stream:
    :return: value（真实值）, length（varint长度）
    """
    value = 0
    position = 0
    shift = 0
    while True:
        if position >= len(stream):
            break
        byte = stream[position]
        value += (byte & 0b01111111) << shift
        if byte & 0b10000000 == 0:
            break
        position += 1
        shift += 7
    return value, position + 1
