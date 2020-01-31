class NoPermissionException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class BiliException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return "返回code不为0。错误代码：%s, 信息：%s" % (self.code, self.msg)


class NetworkException(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "连接错误。错误代码：%s" % self.code
