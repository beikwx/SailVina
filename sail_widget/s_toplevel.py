from tkinter import Toplevel


class STopLevel(object):

    def __init__(self, root, win_x, win_y, title):
        self.root = root
        self.toplevel = Toplevel(self.root)
        self._center(self.toplevel, win_x, win_y, title)

    def _center(self, top, win_x, win_y, title):
        # 居中显示
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (win_x / 2)
        y = (screen_height / 2) - (win_y / 2)
        top.geometry('%dx%d+%d+%d' % (win_x, win_y, x, y))
        top.resizable(width=False, height=False)
        top.title(title)
        top.focus()
        top.grab_set()
        top.lift()
