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
    def setup(self, Form):
        # UI
        Form.setObjectName("Form")
        Form.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
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
        self.slider.setValue(100)
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

        # Slot & String
        self.win: QtWidgets.QWidget = Form
        self.pp.setEnabled(False)
        self.pushButton.setEnabled(False)
        self.retranslateUi(Form)
        self.win.closeEvent = self.on_close_check
        self.pushButton_2.clicked.connect(self.open_ivi)
        self.pushButton_3.clicked.connect(self.close_ivi)
        self.pushButton_4.clicked.connect(self.sound_on_off_event)
        self.pp.clicked.connect(self.pp_button)
        self.horizontalSlider.valueChanged.connect(self.volume_change_event)
        self.slider.sliderReleased.connect(self.position_change_event)
        self.slider.sliderPressed.connect(self.position_start_change_event)

        # InteractiveVariables
        self.current_node = 0
        self.variables = []
        self.state_log = []

        # Video Play Variables & Functions
        self.is_draging_slider = False
        self.is_stoping = False
        self.win.startTimer(5)
        self.has_end = False
        self.final_position = -1

        # Timer & Refresh
        def timerEvent(*args, **kwargs):
            if self.is_draging_slider:
                return
            if self.mediaplayer.duration() == 0:
                self.slider.setValue(100)
                self.label.setText("--:--/--:--")
                return
            if (
                (self.mediaplayer.duration() // 1000)
                == ((self.mediaplayer.position() // 1000))
            ) and (not self.has_end):
                self.has_end = True
                self.final_position = self.mediaplayer.position()
                self.slider.setValue(100)
                duration = self.mediaplayer.duration() // 1000
                duration_sec = duration % 60
                duration_min = duration // 60
                if duration_sec < 10:
                    duration_sec = "0" + str(duration_sec)
                if duration_min < 10:
                    duration_min = "0" + str(duration_min)
                self.label.setText(f'{duration_min}:{duration_sec}/{duration_min}:{duration_sec}')
                return
            elif self.has_end:
                self.has_end = True
                self.slider.setValue(100)
                self.mediaplayer.setPosition(self.final_position)
                self.mediaplayer.setAudioOutput(
                    QtMultimedia.QAudioOutput().setVolume(0)
                )
                duration = self.mediaplayer.duration() // 1000
                duration_sec = duration % 60
                duration_min = duration // 60
                if duration_sec < 10:
                    duration_sec = "0" + str(duration_sec)
                if duration_min < 10:
                    duration_min = "0" + str(duration_min)
                self.label.setText(f'{duration_min}:{duration_sec}/{duration_min}:{duration_sec}')
                return
            else:
                self.has_end = False
            self.last_position = self.mediaplayer.position()
            self.slider.setValue(
                int(self.mediaplayer.position() / self.mediaplayer.duration() * 100)
            )
            duration = self.mediaplayer.duration() // 1000
            position = self.mediaplayer.position() // 1000
            duration_sec = duration % 60
            duration_min = duration // 60
            position_sec = position % 60
            position_min = position // 60
            if duration_sec < 10:
                duration_sec = "0" + str(duration_sec)
            if duration_min < 10:
                duration_min = "0" + str(duration_min)
            if position_sec < 10:
                position_sec = "0" + str(position_sec)
            if position_min < 10:
                position_min = "0" + str(position_min)
            self.label.setText(f'{position_min}:{position_sec}/{duration_min}:{duration_sec}')
        self.win.timerEvent = timerEvent

    def start_playing(self):
        self.mediaplayer.play()
        self.is_stoping = False

    def stop_playing(self):
        self.mediaplayer.stop()
        self.is_stoping = True

    def pause_playing(self):
        self.mediaplayer.pause()
        self.is_stoping = True

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.pp.setText(_translate("Form", "Pause"))
        self.pushButton.setText(_translate("Form", "<- Previous"))
        self.node.setText(_translate("Form", "(当前节点: 无)"))
        self.info.setText(_translate("Form", "视频标题(BVID)"))
        self.pushButton_2.setText(_translate("Form", "Open"))
        self.pushButton_3.setText(_translate("Form", "Close"))
        self.pushButton_4.setText(_translate("Form", "Sound: Off"))
        self.label.setText(_translate("Form", "--:--/--:--"))
        self.label_2.setText(_translate("Form", "0"))

    def set_source(self, cid: int):
        self.has_end = False
        self.mediaplayer.setAudioOutput(
            QtMultimedia.QAudioOutput().setVolume(self.horizontalSlider.value() / 100)
        )
        self.stop_playing()
        path1 = ".mplayer/" + str(cid) + ".video.mp4"
        path2 = ".mplayer/" + str(cid) + ".audio.mp4"
        dest = ".mplayer/" + str(cid) + ".mp4"
        if not os.path.exists(path2):
            self.mediaplayer.setSource(
                QtCore.QUrl(".mplayer/" + str(cid) + ".video.mp4")
            )
            self.mediaplayer.setPosition(0)
            self.start_playing()
            return
        os.system(
            f'{get_ffmpeg_path()}\
            -y -i "{path1}" -i "{path2}" -strict -2 -acodec copy -vcodec copy -f mp4 "{dest}"'
        )
        self.mediaplayer.setSource(QtCore.QUrl(".mplayer/" + str(cid) + ".mp4"))
        self.mediaplayer.setPosition(0)
        self.start_playing()

    def extract_ivi(self, path: str):
        if os.path.exists(".mplayer"):
            shutil.rmtree(".mplayer")
        ivi = zipfile.ZipFile(path)
        ivi.extractall(".mplayer/")
        bilivideo_parser = json.JSONDecoder()
        self.node.setText("(当前节点: 视频主节点)")
        self.info.setText(
            bilivideo_parser.decode(open(".mplayer/bilivideo.json", "r").read())[
                "title"
            ]
            + "("
            + bilivideo_parser.decode(open(".mplayer/bilivideo.json", "r").read())[
                "bvid"
            ]
            + ")"
        )
        self.graph = json.load(open(".mplayer/ivideo.json", "r"))
        self.current_node = 1
        self.set_source(self.graph["1"]["cid"])

    def close_ivi(self):
        self.current_node = 0
        self.variables = []
        self.state_log = []
        self.stop_playing()
        self.pp.setText("Pause")
        self.has_end = False
        self.mediaplayer = QtMultimedia.QMediaPlayer()  # Clear the multimedia source
        self.mediaplayer.setVideoOutput(self.player)
        self.mediaplayer.setAudioOutput(QtMultimedia.QAudioOutput())
        if os.path.exists(".mplayer"):
            shutil.rmtree(".mplayer")
        self.node.setText("(当前节点: 无)")
        self.info.setText("视频标题(BVID)")
        self.win.setWindowTitle("MPlayer")
        self.lineEdit.setText("")
        self.pp.setEnabled(False)
        self.pushButton.setEnabled(False)

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
                    filter="All Files (*);;Bilibili Interactive Video (*.ivi)",
                )
                self.extract_ivi(filename)
                self.win.setWindowTitle("MPlayer - " + filename)
                self.lineEdit.setText(filename)
            self.pp.setEnabled(True)
            self.pushButton.setEnabled(True)
        except Exception as e:
            warning = QtWidgets.QMessageBox()
            warning.warning(self.win, "Oops...", str(e))

    def volume_change_event(self):
        if self.horizontalSlider.value() == 0:
            self.pushButton_4.setText("Sound: Off")
        else:
            self.pushButton_4.setText("Sound: On")
        if (not self.has_end) or (not self.is_stoping):
            pass
        else:
            self.pause_playing()
        volume = self.horizontalSlider.value()
        self.label_2.setText(str(volume))
        self.audio_output.setVolume(float(volume / 100))
        self.mediaplayer.setAudioOutput(self.audio_output)
        if (not self.has_end) or (not self.is_stoping):
            pass
        else:
            self.start_playing()

    def position_start_change_event(self):
        self.mediaplayer.pause()
        self.is_draging_slider = True

    def position_change_event(self):
        volume = self.slider.value()
        if volume != 100 and self.has_end:
            self.has_end = False
            self.mediaplayer.setAudioOutput(
                QtMultimedia.QAudioOutput().setVolume(
                    self.horizontalSlider.value() / 100
                )
            )
            self.volume_change_event()
        self.mediaplayer.setPosition(int(self.mediaplayer.duration() * volume / 100))
        if not self.is_stoping:
            self.start_playing()
        self.is_draging_slider = False

    def sound_on_off_event(self):
        if "on" in self.pushButton_4.text().lower():
            self.pushButton_4.setText("Sound: Off")
            curpos = self.mediaplayer.position()
            self.stop_playing()
            volume = self.horizontalSlider.value()
            self.label_2.setText(str(volume))
            self.audio_output = QtMultimedia.QAudioOutput()
            self.audio_output.setVolume(0.0)
            self.mediaplayer.setAudioOutput(self.audio_output)
            self.mediaplayer.setPosition(curpos)
            self.start_playing()
            self.horizontalSlider.setSliderPosition(0)
        else:
            self.pushButton_4.setText("Sound: On")
            curpos = self.mediaplayer.position()
            self.stop_playing()
            volume = self.horizontalSlider.value()
            self.label_2.setText(str(volume))
            self.audio_output = QtMultimedia.QAudioOutput()
            self.audio_output.setVolume(1.0)
            self.mediaplayer.setAudioOutput(self.audio_output)
            self.mediaplayer.setPosition(curpos)
            self.start_playing()
            self.horizontalSlider.setSliderPosition(100)

    def pp_button(self):
        if self.is_stoping:
            self.start_playing()
            self.pp.setText("Pause")
        else:
            self.pause_playing()
            self.pp.setText("Play")

    def on_close_check(self, event):
        if self.current_node != 0:
            reply = QtWidgets.QMessageBox.question(self.win, "WARNING", "IVI file is playing. Are you sure to exit? ",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self.close_ivi()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = MPlayer()
    ui.setup(win)
    win.show()
    sys.exit(app.exec())
