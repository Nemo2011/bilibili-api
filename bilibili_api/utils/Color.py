"""
bilibili_api.utils.Color

颜色类
"""


class Color(object):
    def __init__(self, hex_: str = "FFFFFF"):
        self.__color = 0
        self.set_hex_color(hex_)

    def set_hex_color(self, hex_color: str):
        """
        设置十六进制RGB颜色
        :param hex_color:
        :return:
        """
        if len(hex_color) == 3:
            hex_color = "".join([x + "0" for x in hex_color])
        dec = int(hex_color, 16)
        self.__color = dec

    def set_rgb_color(self, r: int, g: int, b: int):
        """
        根据RGB三个分量设置颜色
        :param r: 红色分量
        :param g: 绿色分量
        :param b: 蓝色分量
        :return:
        """
        if not all([0 <= r < 256, 0 <= g < 256, 0 <= b < 256]):
            raise ValueError("值范围0~255")
        self.__color = (r << 8*2) + (g << 8) + b

    def set_dec_color(self, color: int):
        """
        设置十进制颜色
        :param color:
        :return:
        """
        if 0 <= int(color) <= 16777215:
            self.__color = color
        else:
            raise ValueError("范围0~16777215")

    def get_hex_color(self):
        """
        获取十六进制颜色
        :return:
        """
        # 补零
        h = hex(int(self.__color)).lstrip("0x")
        h = "0" * (6 - len(h)) + h
        return h

    def get_rgb_color(self):
        """
        获取RGB三个分量颜色
        :return:
        """
        h = hex(int(self.__color)).lstrip("0x")
        # 补零
        h = "0" * (6 - len(h)) + h
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        return r, g, b

    def get_dec_color(self):
        """
        获取十进制颜色
        :return:
        """
        return self.__color

    def __str__(self):
        return self.get_hex_color()
