import copy
import enum
import json
import os
import random
import shutil
import sys
import time
import zipfile
from typing import List, Union, Tuple

from PyQt6 import QtCore, QtGui, QtMultimedia, QtMultimediaWidgets, QtWidgets


class InteractiveVariable:
    """
    互动节点的变量
    """

    def __init__(
        self,
        name: str,
        var_id: str,
        var_value: int,
        show: bool = False,
        random: bool = False,
    ):
        """
        Args:
            name      (str)  : 变量名
            var_id    (str)  : 变量 id
            var_value (int)  : 变量的值
            show      (bool) : 是否显示
            random    (bool) : 是否为随机值(1-100)
        """
        self.__var_id = var_id
        self.__var_value = var_value
        self.__name = name
        self.__is_show = show
        self.__random = random

    def get_id(self) -> str:
        return self.__var_id

    def refresh_value(self) -> None:
        """
        刷新变量数值
        """
        if self.is_random():
            self.__var_value = int(rand(0, 100))

    def get_value(self) -> int:
        return self.__var_value

    def is_show(self) -> bool:
        return self.__is_show

    def is_random(self) -> bool:
        return self.__random

    def get_name(self) -> str:
        return self.__name

    def __str__(self):
        return f"{self.__name} {self.__var_value}"


class InteractiveButtonAlign(enum.Enum):
    """
    按钮的文字在按钮中的位置


    ``` text
    -----
    |xxx|----o (TEXT_LEFT)
    -----

         -----
    o----|xxx| (TEXT_RIGHT)
         -----

    ----------
    |XXXXXXXX| (DEFAULT)
    ----------
    ```

    - DEFAULT
    - TEXT_UP
    - TEXT_RIGHT
    - TEXT_DOWN
    - TEXT_LEFT
    """

    DEFAULT = 0
    TEXT_UP = 1
    TEXT_RIGHT = 2
    TEXT_DOWN = 3
    TEXT_LEFT = 4


class InteractiveButton:
    """
    互动视频节点按钮类
    """

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        align: Union[InteractiveButtonAlign, int] = InteractiveButtonAlign.DEFAULT,
    ):
        """
        Args:
            text  (str)                         : 文字
            x     (int)                         : x 轴
            y     (int)                         : y 轴
            align (InteractiveButtonAlign | int): 按钮的文字在按钮中的位置
        """
        self.__text = text
        self.__pos = (x, y)
        if isinstance(align, InteractiveButtonAlign):
            align = align.value
        self.__align = align

    def get_text(self) -> str:
        return self.__text

    def get_align(self) -> int:
        return self.__align  # type: ignore

    def get_pos(self) -> Tuple[int, int]:
        return self.__pos

    def __str__(self):
        return f"{self.__text} {self.__pos}"


class InteractiveJumpingCondition:
    """
    节点跳转的公式，只有公式成立才会跳转
    """

    def __init__(self, var: List[InteractiveVariable] = [], condition: str = "True"):
        """
        Args:
            var       (List[InteractiveVariable]): 所有变量
            condition (str)                      : 公式
        """
        self.__vars = var
        self.__command = condition

    def get_result(self) -> bool:
        """
        计算公式获得结果

        Returns:
            bool: 是否成立
        """
        if self.__command == "":
            return True
        command = copy.copy(self.__command)
        for var in self.__vars:
            var_name = var.get_id()
            var_value = var.get_value()
            command = command.replace(var_name, str(var_value))
        command = command.replace("&&", " and ")
        command = command.replace("||", " or ")
        command = command.replace("!", " not ")
        command = command.replace("===", "==")
        command = command.replace("!==", "!=")
        command = command.replace("true", "True")
        command = command.replace("false", "False")
        return eval(command)

    def __str__(self):
        return f"{self.__command}"


class InteractiveJumpingCommand:
    """
    节点跳转对变量的操作
    """

    def __init__(self, var: List[InteractiveVariable] = [], command: str = ""):
        """
        Args:
            var       (List[InteractiveVariable]): 所有变量
            condition (str)                      : 公式
        """
        self.__vars = var
        self.__command = command

    def run_command(self) -> List["InteractiveVariable"]:
        """
        执行操作

        Returns:
            List[InteractiveVariable]
        """
        if self.__command == "":
            return self.__vars
        for code in self.__command.split(";"):
            var_name_ = code.split("=")[0]
            var_new_value = code.split("=")[1]
            for var in self.__vars:
                var_name = var.get_id()
                var_value = var.get_value()
                var_new_value = var_new_value.replace(var_name, str(var_value))
            var_new_value_calc = eval(var_new_value)
            for var in self.__vars:
                if var.get_id() == var_name_:
                    var._InteractiveVariable__var_value = var_new_value_calc  # type: ignore
        return self.__vars


class InteractiveNodeJumpingType(enum.Enum):
    """
    对下一节点的跳转的方式

    - ASK    : 选择
    - DEFAULT: 跳转到默认节点
    - READY  : 选择(只有一个选择)
    """

    READY = 1
    DEFAULT = 0
    ASK = 2


class Button:
    def __init__(self, id_, pos, text, condition, command):
        # A class that provides the button model.
        self.node_id = id_
        self.pos = pos
        self.text = text
        self.condition = condition
        self.command = command
        # 什么？别问我为什么不用 TypedDict / dataclass

    def __str__(self) -> str:
        return f"{self.pos} {self.text} {self.condition} {self.command}"


class ButtonLabel(QtWidgets.QLabel):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent=parent)
        self.setObjectName(str(time.time()))

    def prep_text(self, text: str, x: int, y: int):
        self.setText(text)
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.setFont(font)
        rect = QtCore.QRect(x, y, 200, 50)
        self.setGeometry(rect)
        self.setStyleSheet(
            "border-width: 5px;\
             border-style: solid;\
             border-color: rgb(100, 100, 100);\
             background-color: rgb(50, 50, 50);\
             color: rgb(255, 255, 255);"
        )
        self.raise_()
        return self


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
        Form.setMinimumSize(QtCore.QSize(800, 650))
        Form.setMaximumSize(QtCore.QSize(800, 650))
        Form.setBaseSize(QtCore.QSize(800, 650))
        Form.setWindowTitle("MPlayer")
        self.win: QtWidgets.QWidget = Form
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
        self.info.setGeometry(QtCore.QRect(320, 520, 471, 36))
        self.info.setWordWrap(True)
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
        self.lineEdit.setPlaceholderText("Type in the path to your ivi file. ")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(690, 560, 108, 32))
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
        self.pushButton.clicked.connect(self.back_to_previous)

        # InteractiveVariables
        self.current_node = 0
        self.variables: List[InteractiveVariable] = []
        self.state_log = []
        self.graph = None
        self.choice_buttons: List[Button] = []
        self.choice_labels: List[ButtonLabel] = []

        # Video Play Variables & Functions
        self.temp_dir = ""
        self.is_draging_slider = False
        self.is_stoping = False
        self.win.startTimer(100)
        self.has_end = False
        self.final_position = -1

        # Timer & Refresh
        def timerEvent(*args, **kwargs):
            # 创建要跳转的节点
            if self.has_end:
                if len(self.choice_labels) != 0:
                    for lbl in self.choice_labels:
                        lbl.raise_()
                    self.player.lower()
                else:
                    children = self.graph[str(self.current_node)]["sub"]
                    if len(children) == 0:
                        # 已结束
                        pass
                    else:
                        # 跳转类型
                        if (
                            self.graph[str(children[0])]["jump_type"]
                            == InteractiveNodeJumpingType.DEFAULT.value
                        ):
                            # 直接跳转
                            for node_id in children:
                                btn = Button(
                                    node_id,
                                    [0, 0],
                                    "",
                                    self.graph[str(node_id)]["condition"],
                                    self.graph[str(node_id)]["command"],
                                )
                                condition = InteractiveJumpingCondition(
                                    self.variables, btn.condition
                                )
                                if condition.get_result():
                                    # 可以跳转
                                    native_command = InteractiveJumpingCommand(
                                        self.variables, btn.command
                                    )
                                    self.variables = native_command.run_command()
                                    btn_id = btn.node_id
                                    self.set_source(self.graph[str(btn_id)]["cid"])
                                    self.current_node = btn.node_id
                                    self.volume_change_event()
                                    title = self.graph[str(node_id)]["title"]
                                    self.node.setText(f"(当前节点: {title})")
                                    break
                        else:
                            # 进行选择
                            def get_info(node_id: int):
                                return self.graph[str(node_id)]

                            cnt = 0
                            for idx, child in enumerate(children):
                                pos_x = cnt * 200
                                pos_y = 600
                                cur_info = get_info(child)
                                # 生成 Button 对象
                                self.choice_buttons.append(
                                    Button(
                                        child,
                                        [pos_x, pos_y],
                                        cur_info["button"]["text"],
                                        cur_info["condition"],
                                        cur_info["command"],
                                    )
                                )
                                # 生成 ButtonLabel 对象
                                if cur_info["button"]["pos"][0] == None:
                                    if idx != 0:
                                        previous_info = get_info(children[idx - 1])
                                        curtext, previoustext = (
                                            cur_info["button"]["text"],
                                            previous_info["button"]["text"],
                                        )
                                        if curtext[2:] == previoustext[2:]:
                                            # 可确定与上一个按钮同一个位置（即概率按钮）
                                            # 不再生成单独的 label
                                            self.choice_buttons[-1].pos[0] -= 200
                                            continue
                                    cnt += 1
                                    lbl = ButtonLabel(self.win)
                                    lbl.prep_text(
                                        cur_info["button"]["text"], pos_x, pos_y
                                    )
                                    lbl.show()
                                    self.choice_labels.append(lbl)
                                    continue
                                if idx != 0:
                                    previous_info = get_info(children[idx - 1])
                                    curpos, previouspos = (
                                        cur_info["button"]["pos"],
                                        previous_info["button"]["pos"],
                                    )
                                    if (abs(curpos[0] - previouspos[0]) <= 5) and (
                                        abs(curpos[1] - previouspos[1]) <= 5
                                    ):
                                        # 可确定与上一个按钮同一个位置（即概率按钮）
                                        # 不再生成单独的 label
                                        self.choice_buttons[-1].pos[0] -= 200
                                    else:
                                        # 生成 label
                                        cnt += 1
                                        lbl = ButtonLabel(self.win)
                                        lbl.prep_text(
                                            cur_info["button"]["text"], pos_x, pos_y
                                        )
                                        lbl.show()
                                        self.choice_labels.append(lbl)
                                else:
                                    # 生成 label
                                    cnt += 1
                                    lbl = ButtonLabel(self.win)
                                    lbl.prep_text(
                                        cur_info["button"]["text"], pos_x, pos_y
                                    )
                                    lbl.show()
                                    self.choice_labels.append(lbl)
                                    pass
                            add_space = int((800 - cnt * 200) / 2)
                            for idx, lbl in enumerate(self.choice_labels):
                                lbl.setGeometry(
                                    QtCore.QRect(
                                        lbl.geometry().left() + add_space,
                                        lbl.geometry().top(),
                                        lbl.geometry().width(),
                                        lbl.geometry().height(),
                                    )
                                )
                            for btn in self.choice_buttons:
                                btn.pos[0] += add_space
            # 处理进度条
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
                self.mediaplayer.pause()
                self.final_position = self.mediaplayer.position()
                self.mediaplayer.setAudioOutput(
                    QtMultimedia.QAudioOutput().setVolume(0)
                )
                self.slider.setValue(100)
                duration = self.mediaplayer.duration() // 1000
                duration_sec = duration % 60
                duration_min = duration // 60
                if duration_sec < 10:
                    duration_sec = "0" + str(duration_sec)
                if duration_min < 10:
                    duration_min = "0" + str(duration_min)
                self.label.setText(
                    f"{duration_min}:{duration_sec}/{duration_min}:{duration_sec}"
                )
                self.player.lower()
                for lbl in self.choice_labels:
                    lbl.raise_()
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
                self.label.setText(
                    f"{duration_min}:{duration_sec}/{duration_min}:{duration_sec}"
                )
                self.player.lower()
                for lbl in self.choice_labels:
                    lbl.raise_()
                return
            else:
                self.has_end = False
                self.choice_buttons = []
                for lbl in self.choice_labels:
                    lbl.hide()
                self.choice_labels = []
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
            self.label.setText(
                f"{position_min}:{position_sec}/{duration_min}:{duration_sec}"
            )
            # 将选择的按钮置于最上层
            for lbl in self.choice_labels:
                lbl.raise_()

        self.win.timerEvent = timerEvent

        # Click & Jump
        def mouseReleaseEvent(event: QtGui.QMouseEvent):
            pos = event.position()
            pos = [pos.x(), pos.y()]
            for var in self.variables:
                if var.is_random():
                    var._InteractiveVariable__var_value = random.random() * 100
            for btn in self.choice_buttons:
                if (
                    (pos[0] - btn.pos[0] <= 200)
                    and (pos[0] - btn.pos[0] >= 0)
                    and (pos[1] - btn.pos[1] <= 50)
                    and (pos[1] - btn.pos[1] >= 0)
                ):
                    condition = InteractiveJumpingCondition(
                        self.variables, btn.condition
                    )
                    if condition.get_result():
                        # 可以跳转
                        native_command = InteractiveJumpingCommand(
                            self.variables, btn.command
                        )
                        self.variables = native_command.run_command()
                        btn_id = btn.node_id
                        self.set_source(self.graph[str(btn_id)]["cid"])
                        self.current_node = btn.node_id
                        self.volume_change_event()
                        title = self.graph[str(btn.node_id)]["title"]
                        self.node.setText(f"(当前节点: {title})")
                        break

        self.win.mouseReleaseEvent = mouseReleaseEvent

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
        wintitle = "MPlayer"
        for var in self.variables:
            if var.is_show():
                wintitle += f" - {var.get_name()}: {int(var.get_value())}"
        for lbl in self.choice_labels:
            lbl.hide()
        self.choice_labels = []
        self.choice_buttons = []
        self.win.setWindowTitle(wintitle)
        self.state_log.append({"cid": cid, "vars": copy.deepcopy(self.variables)})
        self.has_end = False
        self.mediaplayer.setAudioOutput(
            QtMultimedia.QAudioOutput().setVolume(self.horizontalSlider.value() / 100)
        )
        self.stop_playing()
        self.pp.setText("Pause")
        dest = self.temp_dir + str(cid) + ".mp4"
        self.mediaplayer.setSource(QtCore.QUrl(dest))
        self.mediaplayer.setPosition(0)
        if self.mediaplayer.duration() <= 7:
            self.mediaplayer.setPosition(self.mediaplayer.duration())
        self.start_playing()

    def extract_ivi(self, path: str):
        curtime = str(time.time())
        try:
            os.mkdir(".mplayer")
        except:
            pass
        os.mkdir(".mplayer/" + curtime)
        self.temp_dir = ".mplayer/" + curtime + "/"
        ivi = zipfile.ZipFile(path)
        ivi.extractall(self.temp_dir)
        bilivideo_parser = json.JSONDecoder()
        self.node.setText("(当前节点: 视频主节点)")
        self.info.setText(
            bilivideo_parser.decode(
                open(self.temp_dir + "bilivideo.json", "r", encoding="utf-8").read()
            )["title"]
            + "("
            + bilivideo_parser.decode(
                open(self.temp_dir + "bilivideo.json", "r", encoding="utf-8").read()
            )["bvid"]
            + ")"
        )
        self.graph = json.load(
            open(self.temp_dir + "ivideo.json", "r", encoding="utf-8")
        )
        self.current_node = 1
        variables = self.graph["1"]["vars"]
        for var in variables:
            self.variables.append(
                InteractiveVariable(
                    var["name"], var["id"], var["value"], var["show"], var["random"]
                )
            )
        self.set_source(self.graph["1"]["cid"])
        self.volume_change_event()

    def close_ivi(self):
        self.player.hide()
        self.player = QtMultimediaWidgets.QVideoWidget(self.win)
        self.player.setGeometry(QtCore.QRect(0, 0, 800, 450))
        self.player.setObjectName("player")
        self.player.show()
        self.current_node = 0
        self.variables = []
        self.state_log = []
        self.choice_buttons = []
        for lbl in self.choice_labels:
            lbl.hide()
        self.choice_labels = []
        self.graph = None
        self.stop_playing()
        self.pp.setText("Pause")
        self.has_end = False
        self.mediaplayer = QtMultimedia.QMediaPlayer()  # Clear the multimedia source
        self.mediaplayer.setVideoOutput(self.player)
        self.mediaplayer.setAudioOutput(QtMultimedia.QAudioOutput())
        self.volume_change_event()
        shutil.rmtree(self.temp_dir)
        while True:
            if not os.path.exists(self.temp_dir):
                break
        try:
            os.rmdir(".mplayer")
        except:
            # Not empty
            pass
        self.temp_dir = ""
        self.node.setText("(当前节点: 无)")
        self.info.setText("视频标题(BVID)")
        self.win.setWindowTitle("MPlayer")
        self.lineEdit.setText("")
        self.pp.setEnabled(False)
        self.pushButton.setEnabled(False)

    def open_ivi(self):
        if self.current_node != 0:
            return
        try:
            if self.lineEdit.text() != "":
                self.extract_ivi(self.lineEdit.text())
            else:
                dialog = QtWidgets.QFileDialog()
                filename, _ = dialog.getOpenFileName(
                    self.win,
                    "Choose an 'ivi' file to open. ",
                    filter="Bilibili Interactive Video (*.ivi)",
                )
                self.extract_ivi(filename)
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
        position = self.mediaplayer.position()
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
            self.mediaplayer.setPosition(position)
            self.start_playing()

    def position_start_change_event(self):
        self.mediaplayer.pause()
        self.is_draging_slider = True

    def position_change_event(self):
        volume = self.slider.value()
        if volume != 100 and self.has_end:
            self.slider.setValue(100)
            return
        self.mediaplayer.setPosition(int(self.mediaplayer.duration() * volume / 100))
        if not self.is_stoping:
            self.start_playing()
        self.is_draging_slider = False

    def sound_on_off_event(self):
        if "on" in self.pushButton_4.text().lower():
            self.pushButton_4.setText("Sound: Off")
            curpos = self.mediaplayer.position()
            self.mediaplayer.pause()
            volume = self.horizontalSlider.value()
            self.label_2.setText(str(volume))
            self.audio_output = QtMultimedia.QAudioOutput()
            self.audio_output.setVolume(0.0)
            self.mediaplayer.setAudioOutput(self.audio_output)
            self.mediaplayer.setPosition(curpos)
            if not self.is_stoping:
                self.start_playing()
            self.horizontalSlider.setSliderPosition(0)
        else:
            self.pushButton_4.setText("Sound: On")
            curpos = self.mediaplayer.position()
            self.mediaplayer.pause()
            volume = self.horizontalSlider.value()
            self.label_2.setText(str(volume))
            self.audio_output = QtMultimedia.QAudioOutput()
            self.audio_output.setVolume(1.0)
            self.mediaplayer.setAudioOutput(self.audio_output)
            self.mediaplayer.setPosition(curpos)
            if not self.is_stoping:
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
            reply = QtWidgets.QMessageBox.question(
                self.win,
                "WARNING",
                "IVI file is playing. Are you sure want to exit? ",
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No,
            )
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self.close_ivi()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def back_to_previous(self):
        if len(self.state_log) < 2:
            QtWidgets.QMessageBox.warning(
                self.win,
                "WTF???",
                "MPlayer can't find the previous node. \nMaybe there's not any node or only one node?",
            )
            return
        new_cid = copy.deepcopy(self.state_log[-2]["cid"])
        new_vars = copy.deepcopy(self.state_log[-2]["vars"])
        self.state_log.pop()
        for key in self.graph.keys():
            if self.graph[key]["cid"] == new_cid:
                new_node_id = int(key)
                self.current_node = new_node_id
                self.variables = new_vars
                self.set_source(new_cid)
                self.state_log.pop()
                title = self.graph[str(new_node_id)]["title"]
                self.node.setText(f"(当前节点: {title})")
                self.volume_change_event()
                return


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = MPlayer()
    ui.setup(win)
    win.show()
    sys.exit(app.exec())


def prepopen(path: str):
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = MPlayer()
    ui.setup(win)
    ui.lineEdit.setText(path)
    ui.open_ivi()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
