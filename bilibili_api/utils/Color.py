"""
bilibili_api.utils.Color

颜色类。
"""


class Color:
    """
    颜色帮助类。
    """
    def __init__(self, hex_: str = "FFFFFF"):
        self.__color = 0
        self.set_hex_color(hex_)

    def set_hex_color(self, hex_color: str):
        """
        设置十六进制RGB颜色。

        Args:
            hex_color (str):  十六进制颜色字符串（如 "66ccff"）。
        """
        if len(hex_color) == 3:
            hex_color = "".join([x + "0" for x in hex_color])
        dec = int(hex_color, 16)
        self.__color = dec

    def set_rgb_color(self, r: int, g: int, b: int):
        """
        根据 RGB 三个分量设置颜色。

        Args:
            r (int): 红色通道分量。
            g (int): 绿色通道分量。
            b (int): 蓝色通道分量
        """
        if not all([0 <= r < 256, 0 <= g < 256, 0 <= b < 256]):
            raise ValueError("值范围0~255")
        self.__color = (r << 8*2) + (g << 8) + b

    def set_dec_color(self, color: int):
        """
        设置十进制颜色。

        Args:
            color (int): 十进制颜色。
        """
        if 0 <= int(color) <= 16777215:
            self.__color = color
        else:
            raise ValueError("范围0~16777215")

    def get_hex_color(self):
        """
        获取十六进制颜色。

        Returns:
            str, 十六进制颜色字符串，如 "66ccff"
        """

        # 补零
        h = hex(int(self.__color)).lstrip("0x")
        h = "0" * (6 - len(h)) + h
        return h

    def get_rgb_color(self):
        """
        获取 RGB 三个分量颜色。

        Returns:
            tuple[int, int, int], 分别为 R, G, B 的十进制数值。
        """
        b = self.__color & 0x0000ff
        g = (self.__color & 0x00ff00) >> 8
        r = (self.__color & 0xff0000) >> 16
        return r, g, b

    def get_dec_color(self):
        """
        获取十进制颜色。

        Returns:
            int, 十进制颜色。
        """
        return self.__color

    def __str__(self):
        return self.get_hex_color()
