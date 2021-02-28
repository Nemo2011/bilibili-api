"""
bilibili_api.utils.Danmaku

弹幕类
"""

import datetime
from .Color import Color
from .utils import crack_uid

class Danmaku:
    FONT_SIZE_EXTREME_SMALL = 12
    FONT_SIZE_SUPER_SMALL = 16
    FONT_SIZE_SMALL = 18
    FONT_SIZE_NORMAL = 25
    FONT_SIZE_BIG = 36
    FONT_SIZE_SUPER_BIG = 45
    FONT_SIZE_EXTREME_BIG = 64
    MODE_FLY = 1
    MODE_TOP = 5
    MODE_BOTTOM = 4
    MODE_REVERSE = 6
    TYPE_NORMAL = 0
    TYPE_SUBTITLE = 1

    def __init__(self, text: str, dm_time: float = 0.0, send_time: float = time.time(), crc32_id: str = None
                 , color: Color = None, weight: int = -1, id_: int = -1, id_str: str = "", action: str = '',
                 mode: int = MODE_FLY, font_size: int = FONT_SIZE_NORMAL, is_sub: bool = False, pool: int = -1,
                 attr: int = -1):
        self.dm_time = datetime.timedelta(seconds=dm_time)
        self.send_time = datetime.datetime.fromtimestamp(send_time)
        self.crc32_id = crc32_id
        self.uid = None

        self.color = color if color else Color()

        self.mode = mode
        self.font_size = font_size
        self.is_sub = is_sub
        self.text = text

        self.weight = weight
        self.id = id_
        self.id_str = id_str
        self.action = action
        self.pool = pool
        self.attr = attr

    def __str__(self):
        ret = "%s, %s, %s" % (self.send_time, self.dm_time, self.text)
        return ret

    def __len__(self):
        return len(self.text)

    def crack_uid(self):
        """
        暴力破解UID，可能存在误差，请慎重使用
        :return: 真实 UID
        """
        self.uid = int(crack_uid(self.crc32_id))
        return self.uid