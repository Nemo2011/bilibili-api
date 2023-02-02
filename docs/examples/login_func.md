# 示例：新建验证码窗口 (PyQt5)

``` python

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from bilibili_api import login_func


# 验证窗口类
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

# 示例：二维码登陆窗口 (PyQt5)

``` python
import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from bilibili_api import login_func, user, sync


# 二维码登录窗口类
class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.setFixedSize(180, 210)
        icon = QtGui.QIcon()
        Login.setWindowIcon(icon)
        self.label_5 = QtWidgets.QLabel(Login)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 161, 161))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(Login)
        self.label_2.setGeometry(QtCore.QRect(35, 10, 85, 21))
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(Login)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 0, 50, 40))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Login)

        qrcode_data = login_func.get_qrcode()
        self.pixmap = QtGui.QPixmap()
        self.pixmap.loadFromData(qrcode_data[0].content, qrcode_data[0].imageType)
        self.label_5.setPixmap(self.pixmap)
        self.label_5.setScaledContents(True)
        self.qrcode_sec = qrcode_data[1]

        self.pushButton_2.setIcon(QtGui.QIcon(QtGui.QPixmap("update.jpg")))

        def update_qrcode():
            qrcode_data = login_func.get_qrcode()
            self.label_5.setPixmap(QtGui.QPixmap(qrcode_data[0]))
            self.label_5.setScaledContents(True)
            self.label_5.update()
            self.qrcode_sec = qrcode_data[1]
        self.pushButton_2.clicked.connect(update_qrcode)

        Login.startTimer(1000)
        def timerEvent(*args, **kwargs):
            _translate = QtCore.QCoreApplication.translate
            try:
                events = login_func.check_qrcode_events(self.qrcode_sec)
            except:
                self.label_2.setText(_translate("Login", "⚫️二维码登录"))
                return
            else:
                if events == None: return
                if events[0] == login_func.QrCodeLoginEvents.SCAN:
                    self.label_2.setText(_translate("Login", "🔴二维码登录"))
                elif events[0] == login_func.QrCodeLoginEvents.CONF:
                    self.label_2.setText(_translate("Login", "🟡二维码登录"))
                elif events[0] == login_func.QrCodeLoginEvents.DONE:
                    self.label_2.setText(_translate("Login", "🟢二维码登录"))
                    credential = events[1]
                    self_info = sync(user.get_self_info(credential)) # type: ignore
                    reply = QtWidgets.QMessageBox.information(
                        Login,
                        "已成功登录到你的帐号",
                        "欢迎：" + self_info['name'],
                        QtWidgets.QMessageBox.Ok
                    )
                    Login.close()
        Login.timerEvent = timerEvent

        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "登录"))
        self.label_2.setText(_translate("Login", "🔴二维码登录"))
```
