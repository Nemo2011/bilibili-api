# 示例：新建验证码窗口 (pyqt5)

``` python

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from bilibili_api import login_func

# Ui 类
class Ui_Geetest(object):
    def setupUi(self, Geetest):
        Geetest.setObjectName("Geetest")
        Geetest.resize(600, 500)
        Geetest.setFixedSize(Geetest.width(), Geetest.height())
        print("正在开启极验验证码服务：")
        server_thread = login_func.start_geetest_server()
        self.webview = QtWebEngineWidgets.QWebEngineView(Geetest)
        self.webview.setObjectName("webview")
        self.webview.setGeometry(QtCore.QRect(0, 0, 600, 500))
        self.webview.setUrl(QtCore.QUrl(server_thread.url))

        self.retranslateUi(Geetest)
        QtCore.QMetaObject.connectSlotsByName(Geetest)

        def onclose(self):
            login_func.close_geetest_server()
        Geetest.closeEvent = onclose

    def retranslateUi(self, Geetest):
        _translate = QtCore.QCoreApplication.translate
        Geetest.setWindowTitle(_translate("Geetest", "极验验证"))
```

# 示例：展示登录二维码

``` python
from PIL import Image
from bilibili_api import login_func
qrcode_result = login_func.get_qrcode()
img = Image.open(qrcode_result[0])
img.show()
# token = qrcode_result[1]
# login_func.check_qrcode_events(token)
```
