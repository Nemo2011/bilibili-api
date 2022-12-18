import sys
from PyQt6 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets


class MPlayer(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(800, 600))
        Form.setMaximumSize(QtCore.QSize(800, 600))
        Form.setBaseSize(QtCore.QSize(800, 600))
        self.player = QtMultimediaWidgets.QVideoWidget(Form)
        self.player.setGeometry(QtCore.QRect(0, 0, 800, 450))
        self.player.setObjectName("player")
        self.slider = QtWidgets.QSlider(Form)
        self.slider.setGeometry(QtCore.QRect(120, 455, 671, 22))
        self.slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider.setObjectName("slider")
        self.pp = QtWidgets.QPushButton(Form)
        self.pp.setGeometry(QtCore.QRect(0, 450, 113, 32))
        self.pp.setObjectName("pp")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(0, 480, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.node = QtWidgets.QLabel(Form)
        self.node.setGeometry(QtCore.QRect(120, 485, 191, 16))
        self.node.setObjectName("node")
        self.info = QtWidgets.QLabel(Form)
        self.info.setGeometry(QtCore.QRect(320, 485, 471, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info.setObjectName("info")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 510, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setGeometry(QtCore.QRect(120, 515, 561, 21))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(690, 510, 103, 32))
        self.pushButton_3.setObjectName("pushButton_3")

        self.win = Form

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pp.setText(_translate("Form", "Play/Pause"))
        self.pushButton.setText(_translate("Form", "<- Prevous"))
        self.node.setText(_translate("Form", "(当前节点: 无)"))
        self.info.setText(_translate("Form", "视频标题(BVID)"))
        self.pushButton_2.setText(_translate("Form", "Open"))
        self.pushButton_3.setText(_translate("Form", "Close"))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = MPlayer()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec())
