"""
bilibili_api.utils.varint

变长数字字节相关。
"""


def read_varint(stream: bytes):
    """
    读取 varint。

    Args:
        stream (bytes): 字节流。

    Returns:
        tuple[int, int]，真实值和占用长度。
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
