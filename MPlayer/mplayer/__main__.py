import json
from PyQt6 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
import sys, os, shutil, zipfile, platform

def get_ffmpeg_path():
    if "darwin" in platform.system().lower():
        # MacOS
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "bin",
            "ffmpeg",
            "macos",
            "all",
            "ffmpeg",
        )
    elif "nt" == os.name:
        # Windows
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "bin",
            "ffmpeg",
            "windows",
            "all",
            "ffmpeg.exe",
        )
    elif "linux" in platform.platform().lower():
        # Linux
        if "arm" in platform.platform().lower():
            # Linux arm
            return os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "bin",
                "ffmpeg",
                "linux",
                "arm64",
                "ffmpeg",
            )
        else:
            # Linux x64
            return os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "bin",
                "ffmpeg",
                "linux",
                "x64",
                "ffmpeg",
            )
    else:
        raise SystemError("您的系统不受支持：", platform.platform())

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
        Form.setWindowTitle("MPlayer")
        self.player = QtMultimediaWidgets.QVideoWidget(Form)
        self.player.setGeometry(QtCore.QRect(0, 0, 800, 450))
        self.player.setObjectName("player")
        self.mediaplayer = QtMultimedia.QMediaPlayer()
        self.mediaplayer.setVideoOutput(self.player)
        self.audio_output = QtMultimedia.QAudioOutput()
        self.audio_output.setVolume(0.0)
        self.mediaplayer.setAudioOutput(self.audio_output)
        self.slider = QtWidgets.QSlider(Form)
        self.slider.setGeometry(QtCore.QRect(120, 455, 571, 22))
        self.slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider.setObjectName("slider")
        self.pp = QtWidgets.QPushButton(Form)
        self.pp.setGeometry(QtCore.QRect(0, 450, 113, 32))
        self.pp.setObjectName("pp")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(0, 525, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.node = QtWidgets.QLabel(Form)
        self.node.setGeometry(QtCore.QRect(120, 530, 191, 16))
        self.node.setObjectName("node")
        self.info = QtWidgets.QLabel(Form)
        self.info.setGeometry(QtCore.QRect(320, 530, 471, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info.setObjectName("info")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 560, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setGeometry(QtCore.QRect(120, 565, 561, 21))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(680, 560, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 485, 113, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalSlider = QtWidgets.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(120, 490, 571, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(699, 449, 81, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(700, 490, 60, 16))
        self.label_2.setObjectName("label_2")

        self.win = Form
        self.retranslateUi(Form)
        self.pushButton_2.clicked.connect(self.open_ivi)
        self.pushButton_3.clicked.connect(self.close_ivi)
        self.horizontalSlider.valueChanged.connect(self.volume_change_event)
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
        self.pushButton_4.setText(_translate("Form", "Sound: On"))
        self.label.setText(_translate("Form", "--:--/--:--"))
        self.label_2.setText(_translate("Form", "0"))

    def extract_ivi(self, path: str):
        if os.path.exists(".mplayer"):
            shutil.rmtree(".mplayer")
        ivi = zipfile.ZipFile(path)
        ivi.extractall(".mplayer/")
        bilivideo_parser = json.JSONDecoder()
        self.node.setText("(当前节点: 视频主节点)")
        self.info.setText(
            bilivideo_parser.decode(open(".mplayer/bilivideo.json", "r").read())["title"]
            + "(" 
            + bilivideo_parser.decode(open(".mplayer/bilivideo.json", "r").read())["bvid"] 
            + ")"
        )
        self.graph = json.load(open(".mplayer/ivideo.json", "r"))
        # self.mediaplayer.play()

    def close_ivi(self):
        self.mediaplayer.stop()
        self.mediaplayer = QtMultimedia.QMediaPlayer() # Clear the multimedia source
        self.mediaplayer.setVideoOutput(self.player)
        self.mediaplayer.setAudioOutput(QtMultimedia.QAudioOutput())
        if os.path.exists(".mplayer"):
            shutil.rmtree(".mplayer")
        self.node.setText("(当前节点: 无)")
        self.info.setText("视频标题(BVID)")
        self.win.setWindowTitle("MPlayer")

    def open_ivi(self):
        try:
            if self.lineEdit.text() != "":
                self.extract_ivi(self.lineEdit.text())
                self.win.setWindowTitle("MPlayer - " + self.lineEdit.text())
            else:
                dialog = QtWidgets.QFileDialog()
                filename, _ = dialog.getOpenFileName(
                    self.win, 
                    "Choose an 'ivi' file to open. ", 
                    filter = "All Files (*);;Bilibili Interactive Video (*.ivi)"
                )
                self.extract_ivi(filename)
                self.win.setWindowTitle("MPlayer - " + filename)
                self.lineEdit.setText(filename)
        except Exception as e:
            warning = QtWidgets.QMessageBox()
            warning.warning(self.win, "Oops...", str(e))

    def volume_change_event(self):
        curpos = self.mediaplayer.position()
        self.mediaplayer.stop()
        volume = self.horizontalSlider.value()
        self.label_2.setText(str(volume))
        self.audio_output = QtMultimedia.QAudioOutput()
        self.audio_output.setVolume(float(volume / 100))
        self.mediaplayer.setAudioOutput(self.audio_output)
        self.mediaplayer.setPosition(curpos)
        self.mediaplayer.play()

    def set_source(self, cid: int):
        path1 = ".mplayer/" + str(cid) + ".video.mp4"
        path2 = ".mplayer/" + str(cid) + ".audio.mp4"
        dest = ".mplayer/" + str(cid) + ".mp4"
        os.system(
            f'{get_ffmpeg_path()}\
            -y -i "{path1}" -i "{path2}" -strict -2 -acodec copy -vcodec copy -f mp4 "{dest}"'
        )
        self.mediaplayer.setSource(QtCore.QUrl(".mplayer/" + str(cid) + ".mp4"))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = MPlayer()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec())
