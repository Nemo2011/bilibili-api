r"""
模块：异常库
功能：定义一些常见错误
项目GitHub地址：https://github.com/Passkou/bilibili_api
  _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/
"""


class BilibiliApiException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class NoPermissionException(BilibiliApiException):
    def __init__(self, msg="无操作权限"):
        self.msg = msg


class BilibiliException(BilibiliApiException):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return "错误代码：%s, 信息：%s" % (self.code, self.msg)


class NetworkException(BilibiliApiException):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "网络错误。状态码：%s" % self.code


class NoIdException(BilibiliApiException):
    def __init__(self):
        self.msg = "aid和bvid请至少提供一个"


class LiveException(BilibiliApiException):
    def __init__(self, msg: str):
        super().__init__(msg)

class UploadException(BilibiliApiException):
    def __init__(self, msg: str):
        super().__init__(msg)

"""
奇怪的异常增加了！
"""