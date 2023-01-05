"""
bilibili_api.BytesReader

读字节流助手。
"""
import struct

from .varint import read_varint


class BytesReader:
    """
    读字节流助手类。
    """

    def __init__(self, stream: bytes):
        """

        Args:
            stream (bytes): 字节流
        """
        self.__stream = stream
        self.__offset: int = 0

    def has_end(self) -> bool: # pylint: disable=used-before-assignment
        """
        是否已读到末尾

        Returns:
            bool。
        """
        return self.__offset >= len(self.__stream)

    def double(self, LE=False) -> float: # pylint: disable=used-before-assignment
        """
        读 double。

        Args:
            LE (bool): 为小端。

        Returns:
            float。
        """
        data = struct.unpack(
            "<d" if LE else ">d", self.__stream[self.__offset : self.__offset + 8]
        )
        self.__offset += 8
        return data[0]

    def float(self, LE=False) -> float:
        """
        读 float。

        Args:
            LE (bool): 为小端。

        Returns:
            float。
        """
        stream = self.__stream[self.__offset : self.__offset + 4]
        data = struct.unpack("<f" if LE else ">f", stream)
        self.__offset += 4
        return data[0]

    def varint(self) -> int:
        """
        读 varint。

        Returns:
            int。
        """
        d, l = read_varint(self.__stream[self.__offset :])
        self.__offset += l
        return d

    def byte(self) -> int:
        """
        读 byte。

        Returns：
            int。
        """
        data = self.__stream[self.__offset]
        self.__offset += 1
        return data

    def string(self, encoding="utf8") -> str:
        """
        读 string。

        Args:
            encoding (str):  编码方式。

        Returns:
            str。
        """
        str_len = self.varint()
        data = self.__stream[self.__offset : self.__offset + str_len]
        self.__offset += str_len
        return data.decode(encoding=encoding, errors="ignore")

    def bool(self) -> bool:
        """
        读 bool。

        Returns:
            bool。
        """
        data = self.__stream[self.__offset]
        self.__offset += 1
        return data == 1

    def bytes_string(self) -> bytes:
        """
        读原始字节流。

        Returns:
            bytes。
        """
        str_len = self.varint()
        data = self.__stream[self.__offset : self.__offset + str_len]
        self.__offset += str_len
        return data

    def fixed16(self, LE=False) -> int:
        """
        读 Fixed int16。

        Args:
            LE (bool): 为小端。

        Returns:
            int。
        """
        data = struct.unpack(
            "<h" if LE else ">h", self.__stream[self.__offset : self.__offset + 2]
        )
        self.__offset += 2
        return data[0]

    def fixed32(self, LE=False) -> int:
        """
        读 Fixed int32.

        Args:
            LE (bool): 为小端。

        Returns:
            int。
        """
        data = struct.unpack(
            "<i" if LE else ">i", self.__stream[self.__offset : self.__offset + 4]
        )
        self.__offset += 4
        return data[0]

    def fixed64(self, LE=False) -> int:
        """
        读 Fixed int64。

        Args:
            LE (bool): 为小端。

        Returns:
            int。
        """
        data = struct.unpack(
            "<q" if LE else ">q", self.__stream[self.__offset : self.__offset + 8]
        )
        self.__offset += 8
        return data[0]

    def ufixed16(self, LE=False) -> int:
        """
        读 Unsigned fixed Int16。

        Args:
            LE (bool): 为小端。

        Returns:
            int。
        """
        data = struct.unpack(
            "<H" if LE else ">H", self.__stream[self.__offset : self.__offset + 2]
        )
        self.__offset += 2
        return data[0]

    def ufixed32(self, LE=False) -> int:
        """
        读 Unsigned fixed Int32。

        Args:
            LE (bool): 为小端。

        Returns:
            int。
        """
        data = struct.unpack(
            "<I" if LE else ">I", self.__stream[self.__offset : self.__offset + 4]
        )
        self.__offset += 4
        return data[0]

    def ufixed64(self, LE=False) -> int:
        """
        读 Unsigned fixed Int64。

        Args:
            LE (bool): 为小端。

        Returns:
            int。
        """
        data = struct.unpack(
            "<Q" if LE else ">Q", self.__stream[self.__offset : self.__offset + 8]
        )
        self.__offset += 8
        return data[0]

    def set_pos(self, pos: int) -> None:
        """
        设置读取起始位置。

        Args:
            pos (int): 读取起始位置。
        """
        if pos < 0:
            raise Exception("读取位置不能小于 0")

        if pos >= len(self.__stream):
            raise Exception("读取位置超过字节流长度")

        self.__offset = pos

    def get_pos(self) -> int:
        """
        获取当前位置。

        Returns:
            int, 当前位置。
        """
        return self.__offset
