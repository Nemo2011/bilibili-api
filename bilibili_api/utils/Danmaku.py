"""
bilibili_api.utils.Danmaku

弹幕类。
"""

import time
from enum import Enum

from .utils import crack_uid


class FontSize(Enum):
    """
    字体大小枚举。
    """
    EXTREME_SMALL = 12
    SUPER_SMALL = 16
    SMALL = 18
    NORMAL = 25
    BIG = 36
    SUPER_BIG = 45
    EXTREME_BIG = 64


class Mode(Enum):
    """
    弹幕模式枚举。
    """
    FLY = 1
    TOP = 5
    BOTTOM = 4
    REVERSE = 6

class Danmaku:
    """
    弹幕类。
    """
    def __init__(self,
                 text: str,
                 dm_time: float = 0.0,
                 send_time: float = time.time(),
                 crc32_id: str = None,
                 color: str = 'ffffff',
                 weight: int = -1,
                 id_: int = -1,
                 id_str: str = "",
                 action: str = "",
                 mode: Mode = Mode.FLY,
                 font_size: FontSize = FontSize.NORMAL,
                 is_sub: bool = False,
                 pool: int = 0,
                 attr: int = -1):
        """
        Args:
            text      (str)               : 弹幕文本。
            dm_time   (float, optional)   : 弹幕在视频中的位置，单位为秒。Defaults to 0.0.
            send_time (float, optional)   : 弹幕发送的时间。Defaults to time.time().
            crc32_id  (str, optional)     : 弹幕发送者 UID 经 CRC32 算法取摘要后的值。Defaults to None.
            color     (str, optional)     : 弹幕十六进制颜色。Defaults to "ffffff".
            weight    (int, optional)     : 弹幕在弹幕列表显示的权重。Defaults to -1.
            id_       (int, optional)     : 弹幕 ID。Defaults to -1.
            id_str    (str, optional)     : 弹幕字符串 ID。Defaults to "".
            action    (str, optional)     : 暂不清楚。Defaults to "".
            mode      (Mode, optional)    : 弹幕模式。Defaults to Mode.FLY.
            font_size (FontSize, optional): 弹幕字体大小。Defaults to FontSize.NORMAL.
            is_sub    (bool, optional)    : 是否为字幕弹幕。Defaults to False.
            pool      (int, optional)     : 池。Defaults to 0.
            attr      (int, optional)     : 暂不清楚。 Defaults to -1.
        """
        self.text = text
        self.dm_time = dm_time
        self.send_time = send_time
        self.crc32_id = crc32_id
        self.color = color
        self.weight = weight
        self.id = id_
        self.id_str = id_str
        self.action = action
        self.mode = mode
        self.font_size = font_size
        self.is_sub = is_sub
        self.pool = pool
        self.attr = attr

        self.uid = None

    def __str__(self):
        ret = "%s, %s, %s" % (self.send_time, self.dm_time, self.text)
        return ret

    def __len__(self):
        return len(self.text)

    def crack_uid(self):
        """
        暴力破解 UID，可能存在误差，请慎重使用。

        Returns:
            int: 真实 UID。
        """
        self.uid = int(crack_uid(self.crc32_id))
        return self.uid

    def to_xml(self):
        string = f'<d p="{self.dm_time},{self.mode},{self.font_size},{int(self.color, 16)},{self.send_time},{self.pool},{self.crc32_id},{self.id},11">{self.text}</d>'
        return string
