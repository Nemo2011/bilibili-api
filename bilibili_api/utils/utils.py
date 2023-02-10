"""
bilibili_api.utils.utils

通用工具库。
"""

import json
import os
from typing import List, TypeVar


def get_api(field: str) -> dict:
    """
    获取 API。

    Args:
        field (str): API 所属分类，即 data/api 下的文件名（不含后缀名）

    Returns:
        dict, 该 API 的内容。
    """
    path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "data", "api", f"{field.lower()}.json"
        )
    )
    if os.path.exists(path):
        with open(path, encoding="utf8") as f:
            return json.loads(f.read())
    else:
        return {}


# def crack_uid(crc32: str):
#     """
#     弹幕中的 CRC32 ID 转换成用户 UID。
#
#     警告，破解后的 UID 不一定准确，有存在误差，仅供参考。
#
#     代码翻译自：https://github.com/esterTion/BiliBili_crc2mid。
#
#     Args:
#         crc32 (str):  crc32 计算摘要后的 UID。
#
#     Returns:
#         int, 真实用户 UID，不一定准确。
#     """
#     __CRCPOLYNOMIAL = 0xEDB88320
#     __crctable = [None] * 256
#     __index = [None] * 4
#
#     def __create_table():
#         for i in range(256):
#             crcreg = i
#             for j in range(8):
#                 if (crcreg & 1) != 0:
#                     crcreg = __CRCPOLYNOMIAL ^ (crcreg >> 1)
#                 else:
#                     crcreg >>= 1
#             __crctable[i] = crcreg
#
#     __create_table()
#
#     def __crc32(input_):
#         if type(input_) != str:
#             input_ = str(input_)
#         crcstart = 0xFFFFFFFF
#         len_ = len(input_)
#         for i in range(len_):
#             index = (crcstart ^ ord(input_[i])) & 0xFF
#             crcstart = (crcstart >> 8) ^ __crctable[index]
#         return crcstart
#
#     def __crc32lastindex(input_):
#         if type(input_) != str:
#             input_ = str(input_)
#         crcstart = 0xFFFFFFFF
#         len_ = len(input_)
#         index = None
#         for i in range(len_):
#             index = (crcstart ^ ord(input_[i])) & 0xFF
#             crcstart = (crcstart >> 8) ^ __crctable[index]
#         return index
#
#     def __getcrcindex(t):
#         for i in range(256):
#             if __crctable[i] >> 24 == t:
#                 return i
#         return -1
#
#     def __deepCheck(i, index):
#         tc = 0x00
#         str_ = ""
#         hash_ = __crc32(i)
#         tc = hash_ & 0xFF ^ index[2]
#         if not (57 >= tc >= 48):
#             return [0]
#         str_ += str(tc - 48)
#         hash_ = __crctable[index[2]] ^ (hash_ >> 8)
#
#         tc = hash_ & 0xFF ^ index[1]
#         if not (57 >= tc >= 48):
#             return [0]
#         str_ += str(tc - 48)
#         hash_ = __crctable[index[1]] ^ (hash_ >> 8)
#
#         tc = hash_ & 0xFF ^ index[0]
#         if not (57 >= tc >= 48):
#             return [0]
#         str_ += str(tc - 48)
#         hash_ = __crctable[index[0]] ^ (hash_ >> 8)
#
#         return [1, str_]
#
#     ht = int(crc32, 16) ^ 0xFFFFFFFF
#     i = 3
#     while i >= 0:
#         __index[3 - i] = __getcrcindex(ht >> (i * 8))
#         # pylint: disable=invalid-sequence-index
#         snum = __crctable[__index[3 - i]]
#         ht ^= snum >> ((3 - i) * 8)
#         i -= 1
#     for i in range(10000000):
#         lastindex = __crc32lastindex(i)
#         if lastindex == __index[3]:
#             deepCheckData = __deepCheck(i, __index)
#             if deepCheckData[0]:
#                 break
#     if i == 10000000:
#         return -1
#     return str(i) + deepCheckData[1]


def join(seperator: str, array: list):
    """
    用指定字符连接数组

    Args:
        seperator (str) : 分隔字符
        array     (list): 数组

    Returns:
        str: 连接结果
    """
    return seperator.join(map(lambda x: str(x), array))


ChunkT = TypeVar("ChunkT", List, List)


def chunk(arr: ChunkT, size: int) -> List[ChunkT]:
    if size <= 0:
        raise Exception('Parameter "size" must greater than 0')

    result = []
    temp = []

    for i in range(len(arr)):
        temp.append(arr[i])

        if i % size == size - 1:
            result.append(temp)
            temp = []

    if temp:
        result.append(temp)

    return result
