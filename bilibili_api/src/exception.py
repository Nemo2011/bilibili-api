class bilibiliApiException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class NoPermissionException(bilibiliApiException):
    def __init__(self, msg="无操作权限"):
        self.msg = msg


class BiliException(bilibiliApiException):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return "返回code不为0。错误代码：%s, 信息：%s" % (self.code, self.msg)


class NetworkException(bilibiliApiException):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "连接错误。错误代码：%s" % self.code
