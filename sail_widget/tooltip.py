import tkinter as tk
from tkinter import ttk


class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tip_windows = None

    def show_tip(self, tip_text):
        # 在提示窗口中显示文字
        # 如果没有定义窗口或者文字则不显示提示
        if self.tip_windows or not tip_text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")  # 获取控件的大小
        x = x + self.widget.winfo_rootx() + 25  # 计算提示框的大小
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tip_windows = tw = tk.Toplevel(self.widget)  # 创建新的提示窗口
        tw.wm_overrideredirect(True)  # 去掉所有的窗口管理(Windows Manager, wm)修饰器
        tw.lift()
        tw.wm_geometry("+%d+%d" % (x, y))  # 创建窗口的大小

        label = ttk.Label(tw, text=tip_text, justify=tk.LEFT,
                          background="#ffffe0", relief=tk.SOLID,
                          borderwidth=1, font=("微软雅黑", "9", "normal"), wraplength=150)
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tip_windows
        self.tip_windows = None
        if tw:
            tw.destroy()


def create_tooltip(widget, text):
    tooltip = ToolTip(widget)

    def enter(event):
        tooltip.show_tip(text)

    def leave(event):
        tooltip.hide_tip()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
