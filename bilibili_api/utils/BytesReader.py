"""
bilibili_api.BytesReader

读字节流助手
"""
import struct
from .varint import read_varint


class BytesReader:
    def __init__(self, stream: bytes):
        """

        :param stream: 字节流
        :type stream: bytes
        """
        self.__stream = stream
        self.__offset = 0

    def has_end(self):
        """
        是否已读到末尾

        :return: bool
        """
        return self.__offset == len(self.__stream)

    def double(self, LE=False):
        """
        读 double

        :param LE: 小端
        """
        data = struct.unpack("<d" if LE else ">d", self.__stream[self.__offset:self.__offset + 8])
        self.__offset += 8
        return data[0]

    def float(self, LE=False):
        """
        读 float

        :param LE: 小端
        """
        data = struct.unpack("<f" if LE else ">f", self.__stream[self.__offset:self.__offset + 4])
        self.__offset += 4
        return data[0]

    def varint(self):
        """
        读 varint
        """
        d, l = read_varint(self.__stream[self.__offset:])
        self.__offset += l
        return d

    def byte(self):
        """
        读 byte
        """
        data = self.__stream[self.__offset]
        self.__offset += 1
        return data

    def string(self, encoding="utf8"):
        """
        读 string

        :param encoding: 编码方式
        """
        str_len = self.varint()
        data = self.__stream[self.__offset:self.__offset + str_len]
        self.__offset += str_len
        return data.decode(encoding=encoding)
    
    def bool(self):
        """
        读 bool
        """
        data = self.__stream[self.__offset]
        self.__offset += 1
        return data == 1

    def bytes_string(self):
        """
        读原始字节流
        """
        str_len = self.varint()
        data = self.__stream[self.__offset:self.__offset + str_len]
        self.__offset += str_len
        return data

    def fixed16(self, LE=False):
        """
        读 Fixed int16

        :param LE: 小端
        """
        data = struct.unpack("<h" if LE else ">h", self.__stream[self.__offset:self.__offset + 2])
        self.__offset += 2
        return data[0]

    def fixed32(self, LE=False):
        """
        读 Fixed int32

        :param LE: 小端
        """
        data = struct.unpack("<i" if LE else ">i", self.__stream[self.__offset:self.__offset + 4])
        self.__offset += 4
        return data[0]

    def fixed64(self, LE=False):
        """
        读 Fixed int64

        :param LE: 小端
        """
        data = struct.unpack("<q" if LE else ">q", self.__stream[self.__offset:self.__offset + 8])
        self.__offset += 8
        return data[0]

    def ufixed16(self, LE=False):
        """
        读 Unsigned fixed Int16

        :param LE: 小端
        """
        data = struct.unpack("<H" if LE else ">H", self.__stream[self.__offset:self.__offset + 2])
        self.__offset += 2
        return data[0]

    def ufixed32(self, LE=False):
        """
        读 Unsigned fixed Int32

        :param LE: 小端
        """
        data = struct.unpack("<I" if LE else ">I", self.__stream[self.__offset:self.__offset + 4])
        self.__offset += 4
        return data[0]

    def ufixed64(self, LE=False):
        """
        读 Unsigned fixed Int64

        :param LE: 小端
        """
        data = struct.unpack("<Q" if LE else ">Q", self.__stream[self.__offset:self.__offset + 8])
        self.__offset += 8
        return data[0]

    def set_pos(self, pos: int):
        """
        设置读取起始位置

        :param pos: 读取起始位置
        """
        if pos < 0:
            raise Exception("读取位置不能小于 0")

        if pos >= len(self.__stream):
            raise Exception("读取位置超过字节流长度")

        self.__offset = pos

    def get_pos(self):
        """
        获取当前位置
        """
        return self.__offset
