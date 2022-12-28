"""
ivitools.player

IVI 文件播放器
"""
import copy
import random
from typing import List
from bilibili_api.interactive_video import (
    InteractiveVariable, 
    InteractiveJumpingCommand, 
    InteractiveJumpingCondition, 
    InteractiveNodeJumpingType, 
    get_ivi_file_meta
)
import wx
import wx.html2
import wx.grid
import tempfile
import zipfile
import os
import time
import shutil
import json
from .ffmpeg import freeze_ffmpeg
from moviepy.editor import VideoFileClip
import threading

FFMPEG_PATH = freeze_ffmpeg()

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


class ButtonLabel(wx.StaticText):
    def __init__(self, parent: wx.Frame = None):
        super().__init__(parent, -1, 
            style = wx.ALIGN_CENTRE_HORIZONTAL | wx.ALIGN_CENTRE_VERTICAL
        )

    def prep_text(self, text: str, x: int, y: int):
        if len(text) > 14:
            text = text[:14] + '\n' + text[14:]
        self.background = wx.StaticText(self.Parent, -1)
        self.background.Lower()
        self.background.SetSize(wx.Rect(x, y, 200, 57))
        self.background.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.SetLabelText(text)
        self.SetSize(x + 5, y + 5, 190, 47)
        self.SetBackgroundColour(wx.Colour(50, 50, 50))
        self.SetForegroundColour(wx.Colour(255, 255, 255))

    def show(self):
        self.background.Show()
        self.Show()
        self.background.Lower()
    
    def hide(self):
        self.background.Hide()
        self.Hide()

class IVIPlayer(wx.Frame):
    def __init__(self):
        super().__init__(None, -1, "IVITools Built-in Player")
        self.SetMaxSize((850, 600))
        self.SetMinSize((850, 600))
        self.SetSize(wx.Rect(100, 100, 850, 600))
        self.video_player = wx.html2.WebView.New(
            self, style = wx.ALIGN_TOP
        )
        self.video_player.SetSize(wx.Rect(0, 40, 850, 475))
        self.title = wx.StaticText(self, label = "(NO ANY VIDEOS YET)", style = wx.ALIGN_CENTER_HORIZONTAL)
        self.title.SetRect(wx.Rect(50, 0, 800, 20))
        self.title.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.variables_bar = wx.StaticText(self, label = "", style = wx.ALIGN_CENTER_HORIZONTAL)
        self.variables_bar.SetRect(wx.Rect(0, 20, 850, 20))
        self.show_buttons_toogle_button = wx.Button(self, label = "<")
        self.show_buttons_toogle_button.SetSize(wx.Rect(800, 520, 50, 50))
        self.show_buttons_toogle_button.Bind(wx.EVT_BUTTON, self.toogle_show_buttons)
        self.back_node_btn = wx.Button(self, label = "<-")
        self.back_node_btn.SetSize(wx.Rect(0, 0, 50, 20))
        self.back_node_btn.Bind(wx.EVT_BUTTON, self.back_to_previous)
        self.back_node_btn.Raise()
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        self.timer = wx.Timer(self)
        self.timer.Start(100)
        self.Bind(wx.EVT_TIMER, self.draw_choice_buttons)
        self.Bind(wx.EVT_LEFT_DOWN, self.check_buttons)
        self.choice_buttons: List[Button] = []
        self.choice_labels: List[ButtonLabel] = []
        self.tmp_dir = ""
        self.current_node = 0
        self.state_log = []
        self.variables = []
        self.show_buttons = False
        self.auto_show_buttons_thread = None

    def set_video_source(self, node_id: int):
        for lbl in self.choice_labels:
            lbl.hide()
        self.choice_buttons = []
        self.choice_labels = []
        self.show_buttons = False
        self.show_buttons_toogle_button.SetLabelText("<")
        self.current_node = node_id
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
                self.choice_buttons = [
                    Button(
                        -1, 
                        [0, 515], 
                        "Continue ->", 
                        "", 
                        ""
                    )
                ]
            else:
                # 进行选择
                def get_info(node_id: int):
                    return self.graph[str(node_id)]

                cnt = 0
                for idx, child in enumerate(children):
                    pos_x = cnt * 200
                    pos_y = 515
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
                    if idx != 0:
                        previous_info = get_info(children[idx - 1])
                        curpos, previouspos = (
                            cur_info["button"]["pos"],
                            previous_info["button"]["pos"],
                        )
                        if cur_info["button"]["pos"][0] != None:
                            if (abs(curpos[0] - previouspos[0]) <= 5) and (
                                abs(curpos[1] - previouspos[1]) <= 5
                            ):
                                # 可确定与上一个按钮同一个位置（即概率按钮）
                                # 不再生成单独的 label
                                self.choice_buttons[-1].pos[0] -= 200
                        elif cur_info["button"]["text"][2:] == previous_info["button"]["text"][2:]:
                            # 可确定与上一个按钮同一个位置（即概率按钮）
                            # 不再生成单独的 label
                            self.choice_buttons[-1].pos[0] -= 200
                        else:
                            cnt += 1
                    else:
                        cnt += 1
        if node_id != 1:
            self.title.Hide()
            self.title = wx.StaticText(
                self, 
                label = self.graph[str(node_id)]["title"], 
                style = wx.ALIGN_CENTER_HORIZONTAL
            )
            self.title.SetBackgroundColour(wx.Colour(255, 255, 255))
            self.title.SetSize(wx.Rect(50, 0, 800, 20))
        cid = self.graph[str(node_id)]["cid"]
        self.state_log.append({"cid": cid, "vars": copy.deepcopy(self.variables)})
        video_path = os.path.join(
            self.tmp_dir, 
            str(cid) + ".video.mp4"
        )
        audio_path = os.path.join(
            self.tmp_dir, 
            str(cid) + ".audio.mp4"
        )
        dest = os.path.join(
            self.tmp_dir, 
            str(cid) + ".mp4"
        )
        var_text = ""
        for var in self.variables:
            if var.is_show():
                var_text += f"{var.get_name()}: {int(var.get_value())} - "
        var_text = var_text.rstrip("- ")
        self.variables_bar.Hide()
        self.variables_bar = wx.StaticText(self, label = var_text, style = wx.ALIGN_CENTER_HORIZONTAL)
        self.variables_bar.SetSize(0, 20, 850, 20)
        if not os.path.exists(audio_path):
            self.video_player.LoadURL(
                "file://" + video_path
            )
        else:
            os.system(
                f'{FFMPEG_PATH}\
                -y -i "{video_path}" -i "{audio_path}"\
                 -strict -2 -acodec copy -vcodec copy \
                -f mp4 "{dest}"'
            )
            self.video_player.LoadURL(
                "file://" + dest
            )

    def open_ivi(self, ivi_path: str):
        self.tmp_dir = os.path.join(
            tempfile.gettempdir(), 
            "ivitools-player-extract", 
            str(time.time())
        )
        zipfile.ZipFile(ivi_path).extractall(self.tmp_dir)
        self.graph = json.load(open(os.path.join(self.tmp_dir, "ivideo.json")))
        variables = self.graph["1"]["vars"]
        for var in variables:
            self.variables.append(
                InteractiveVariable(
                    var["name"], var["id"], var["value"], var["show"], var["random"]
                )
            )
        self.title.Hide()
        self.title = wx.StaticText(
            self, 
            label = get_ivi_file_meta(ivi_path)["title"], 
            style = wx.ALIGN_CENTER_HORIZONTAL)
        self.title.SetRect(wx.Rect(50, 0, 800, 20))
        self.title.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.set_video_source(1)

    def on_exit(self, event):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
        self.Destroy()
    
    def draw_choice_buttons(self, event):
        if self.show_buttons == False:
            for lbl in self.choice_labels:
                lbl.hide()
            self.choice_labels = []
        else:
            if len(self.choice_labels) == 0:
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
                        lbl = ButtonLabel(self)
                        lbl.prep_text(
                            "Continue ->", 0, 515
                        )
                        self.choice_labels.append(lbl)
                        lbl.show()
                    else:
                        # 进行选择
                        def get_info(node_id: int):
                            return self.graph[str(node_id)]

                        cnt = 0
                        for idx, child in enumerate(children):
                            pos_x = cnt * 200
                            pos_y = 515
                            cur_info = get_info(child)
                            previous_info = get_info(children[idx - 1])
                            if cur_info["button"]["text"][2:] == previous_info["button"]["text"][2:]:
                                # 可确定与上一个按钮同一个位置（即概率按钮）
                                # 不再生成单独的 label
                                pass
                            # 生成 ButtonLabel 对象
                            if cur_info["button"]["pos"][0] == None:
                                cnt += 1
                                lbl = ButtonLabel(self)
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
                                    pass
                                else:
                                    # 生成 label
                                    cnt += 1
                                    lbl = ButtonLabel(self)
                                    lbl.prep_text(
                                        cur_info["button"]["text"], pos_x, pos_y
                                    )
                                    lbl.show()
                                    self.choice_labels.append(lbl)
                            else:
                                # 生成 label
                                cnt += 1
                                lbl = ButtonLabel(self)
                                lbl.prep_text(
                                    cur_info["button"]["text"], pos_x, pos_y
                                )
                                lbl.show()
                                self.choice_labels.append(lbl)
                                pass
            else:
                for btn in self.choice_labels:
                    btn.show()
    
    def toogle_show_buttons(self, event):
        if self.show_buttons:
            self.show_buttons = False
            self.show_buttons_toogle_button.SetLabelText("<")
        else:
            self.show_buttons = True
            self.show_buttons_toogle_button.SetLabelText(">")

    def check_buttons(self, event):
        if not self.show_buttons:
            return
        pos = event.Position
        pos = [pos.x, pos.y]
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
                if btn.node_id == -1:
                    # 直接跳转
                    for node_id in self.graph[str(self.current_node)]["sub"]:
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
                            self.set_video_source(btn.node_id)
                            break
                condition = InteractiveJumpingCondition(
                    self.variables, btn.condition
                )
                if condition.get_result():
                    # 可以跳转
                    native_command = InteractiveJumpingCommand(
                        self.variables, btn.command
                    )
                    self.variables = native_command.run_command()
                    self.set_video_source(btn.node_id)
                    break
    
    def back_to_previous(self, event):
        if len(self.state_log) < 2:
            return
        new_cid = copy.deepcopy(self.state_log[-2]["cid"])
        new_vars = copy.deepcopy(self.state_log[-2]["vars"])
        self.state_log.pop()
        for key in self.graph.keys():
            if self.graph[key]["cid"] == new_cid:
                new_node_id = int(key)
                self.current_node = new_node_id
                self.variables = new_vars
                self.set_video_source(new_node_id)
                self.state_log.pop()
                return
