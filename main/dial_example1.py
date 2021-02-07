from tkinter import *
from menulogbase import MenulogApp

import tkinter as tkinter
import tkinter.font
import os
import subprocess

TITLE = 'Menulog Example-1'
USER_MENU_FILE = 'dial_example1.txt'

CMD_HELP = 'help'
CMD_PRINT_MENU = 'menu'
CMD_OPEN_MENU_DIRECTORY = 'openMenuDir'
CMD_OPEN_MENU_FILE = 'openMenuFile'


class Dial(tkinter.Frame):
    def __init__(self, parent_menulog):
        super().__init__(parent_menulog.dial_frame)
        self.menulog = parent_menulog

        self.last_cmd = tkinter.StringVar()
        self.cmd_counter = tkinter.IntVar()

        self.setup_ui()

    def setup_ui(self):
        # ------------------------------------------------------
        self.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        # self.config(bd=1, relief=tkinter.SOLID)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

        image01 = PhotoImage(file="01.gif")
        label_image1 = tkinter.Label(self, image=image01)
        label_image1.image = image01
        label_image1.grid(row=0, column=0, pady=5)

        label_image2 = tkinter.Label(self, image=image01)
        label_image2.image = image01
        label_image2.grid(row=0, column=1, pady=5)

        image02 = PhotoImage(file="02.gif")
        label_image3 = tkinter.Label(self, image=image02)
        label_image3.image = image02
        label_image3.grid(row=0, column=2, pady=5)

        label_image4 = tkinter.Label(self, image=image02)
        label_image4.image = image02
        label_image4.grid(row=0, column=3, pady=5)

        row1 = tkinter.Frame(self)
        row1.grid(row=1, column=0, columnspan=4, sticky=tkinter.NSEW, pady=5)
        label_last_cmd = tkinter.Label(row1, justify=LEFT, anchor=tkinter.E, width=24)
        label_last_cmd['text'] = 'Last Command:'
        label_last_cmd.pack(side=tkinter.LEFT, fill=tkinter.X, padx=10)
        tkinter.Entry(row1, textvariable=self.last_cmd, width=36).pack(side=tkinter.LEFT)

        row2 = tkinter.Frame(self)
        row2.grid(row=2, column=0, columnspan=4, sticky=tkinter.NSEW, pady=5)
        label_cmd_counter = tkinter.Label(row2, justify=LEFT, anchor=tkinter.E, width=24)
        label_cmd_counter['text'] = 'Executed Command Count:'
        label_cmd_counter.pack(side=tkinter.LEFT, fill=tkinter.X, padx=10)
        tkinter.Entry(row2, textvariable=self.cmd_counter, width=36).pack(side=tkinter.LEFT)

    def run(self, cmd_line):
        cmd_line = cmd_line.strip()
        if len(cmd_line) == 0:
            return

        if cmd_line == CMD_HELP:
            self.record_cmd(cmd_line)
            self.add_log_help()
        elif cmd_line == CMD_PRINT_MENU:
            self.record_cmd(cmd_line)
            self.add_log_menu()
        elif cmd_line == CMD_OPEN_MENU_FILE:
            self.record_cmd(cmd_line)
            self.open_dir_file('.\\' + USER_MENU_FILE)
        elif cmd_line == CMD_OPEN_MENU_DIRECTORY:
            self.record_cmd(cmd_line)
            self.open_dir_file('.')
        else:
            self.add_log_unknown_cmd(cmd_line)
        return

    def record_cmd(self, cmd_line):
        self.last_cmd.set(cmd_line)
        self.cmd_counter.set(self.cmd_counter.get() + 1)

        self.menulog.add_log('')
        self.menulog.add_log(cmd_line)
        return

    def add_log_unknown_cmd(self, cmd_line):
        self.menulog.add_log('')
        self.menulog.add_log("Error! Unknown Command : " + cmd_line)
        return

    def add_log_help(self):
        for item in get_lst_help():
            self.menulog.add_log(item)
        return

    def add_log_menu(self):
        for item in menulog.user_factory_menu:
            self.menulog.add_log(item)
        return

    def open_dir_file(self, filename):
        try:
            os.startfile(filename)
        except Exception as e:
            self.menulog.add_log(e)
            subprocess.Popen(['xdg-open', filename])


def get_lst_help():
    return [
        "Help",
        "帮助",
        "",
        "Menulog 包括三个区域：",
        "    菜单（Menu）区域"
        "    日志（Log）区域",
        "    表盘（Dial）区域",
        "另外，再加上一个命令行（CLI）输入框。",
        "",
        "菜单区域的内容由两部分组成：",
        "    程序本身自带的菜单（厂商菜单）",
        "    用户自己编辑的菜单文件部分",
        "菜单中有的命令行可以直接双击鼠标执行。",
        "命令行的格式：命令+两个斜杠/+注释说明。",
        "请试一试命令(" + CMD_OPEN_MENU_DIRECTORY + ")打开菜单目录，编辑菜单文件。",
        "",
        "日志区域的内容来自命令执行过程。",
        "双击鼠标将弹出停滞的日志内容，可以剪切粘贴内容。",
        "",
        "表盘区域的内容主要是参数和状态数据。",
        "",
        "用户自编辑的菜单文件支持多种文字：",
        "Chinese 汉字",
        "Japanese にほんご",
        "Korean 조선어",
        "",
        ""
    ]


def prepare_factory_menu():
    lst_menu = [
        "",
        "UNDER CONSTRUCTION",
        "",
        "UNDER CONSTRUCTION",
        "",
        "UNDER CONSTRUCTION",
        "",
        "",
        "*******************************",
        "",
        CMD_OPEN_MENU_FILE + "//打开用户菜单文件",
        "",
        CMD_OPEN_MENU_DIRECTORY + "//打开目录",
        "",
        CMD_PRINT_MENU + "//打印菜单",
        "",
        CMD_HELP + "//帮助",
        ""
    ]
    return lst_menu


if __name__ == '__main__':
    menulog = MenulogApp(TITLE, USER_MENU_FILE, prepare_factory_menu())
    menulog.set_dial(Dial(menulog))

    menulog.mainloop()
