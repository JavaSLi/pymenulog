from tkinter import *

import tkinter as tkinter
import tkinter.font
import os
import codecs
import subprocess

MAX_LOG = 1000

CMD_HELP = 'help'
CMD_PRINT_MENU = 'menu'
CMD_OPEN_MENU_DIRECTORY = 'openMenuDir'
CMD_OPEN_MENU_FILE = 'openMenuFile'
CMD_REFRESH_MENU = 'refreshMenu'


def get_common_help_list():
    return [
        "*******************************",
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


def get_common_factory_menu():
    return [
        "*******************************",
        "",
        CMD_OPEN_MENU_FILE + "//打开用户菜单文件",
        "",
        CMD_REFRESH_MENU + "//刷新菜单",
        "",
        CMD_OPEN_MENU_DIRECTORY + "//打开目录",
        "",
        CMD_PRINT_MENU + "//打印菜单",
        "",
        CMD_HELP + "//帮助",
        ""
    ]


def open_dir_file(filename, menulog):
    try:
        os.startfile(filename)
    except Exception as e:
        menulog.add_log(e)
        subprocess.Popen(['xdg-open', filename])


class MenulogApp(tkinter.Tk):
    def __init__(self, title, menu_file_name, factory_menu, lst_help):
        super().__init__()

        self.title(title)
        self.menu_file_name = menu_file_name
        self.factory_menu = factory_menu
        self.user_factory_menu = []
        self.lst_help = lst_help

        self.cli = tkinter.StringVar()
        self.mouse_click_count = 0
        self.list_menu = None
        self.list_log = None
        self.entry_cli = None
        self.dial_frame = None

        self.dial = None

        self.setup_ui()

    def setup_ui(self):
        # ------------------------------------------------------
        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=2)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=2)
        # ------------------------------------------------------
        menu_area = tkinter.Frame(self.frame)
        menu_area.grid(row=0, column=0, rowspan=3, sticky=tkinter.NSEW, padx=2, pady=2)
        menu_area.config(bd=1, relief=tkinter.SOLID)
        self.setup_ui_menu_area(menu_area)
        # ------------------------------------------------------
        log_area = tkinter.Frame(self.frame)
        log_area.grid(row=0, column=1, sticky=tkinter.NSEW, padx=2, pady=2)
        log_area.config(bd=1, relief=tkinter.SOLID)
        self.setup_ui_log_area(log_area)
        # ------------------------------------------------------
        row_cli = tkinter.Frame(self.frame)
        row_cli.grid(row=1, column=1, sticky=tkinter.EW, padx=10, pady=2)

        tkinter.Label(row_cli, text='Command：', width=9).pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.entry_cli = tkinter.Entry(row_cli, textvariable=self.cli, width=50, bg='#606060', fg='white')
        self.entry_cli.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.entry_cli.bind("<Return>", self.run_cli)
        # ------------------------------------------------------
        dial_area = tkinter.Frame(self.frame)
        dial_area.grid(row=2, column=1, sticky=tkinter.NSEW, padx=2, pady=2)
        dial_area.config(bd=4, relief=tkinter.SOLID)

        tkinter.Label(dial_area, text='DIAL board', bg='#000080', fg='white', width=20).pack(side=tkinter.TOP,
                                                                                             fill=tkinter.X)
        self.dial_frame = tkinter.Frame(dial_area)
        self.dial_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        # ------------------------------------------------------

        self.geometry('1200x800')
        return

    def setup_ui_menu_area(self, frame):
        font_menu = tkinter.font.Font(self, size=11, weight='normal', underline=False)

        self.list_menu = Listbox(frame, width=40, selectmode=SINGLE, bg='#E0E0E0', font=font_menu)

        self.refresh_menu_list()

        # scrollbar_y = Scrollbar(frame, width=20)
        scrollbar_y = Scrollbar(frame)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        scrollbar_x = Scrollbar(frame, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        scrollbar_y.config(command=self.list_menu.yview)
        scrollbar_x.config(command=self.list_menu.xview)

        self.list_menu.config(yscrollcommand=scrollbar_y.set)
        self.list_menu.config(xscrollcommand=scrollbar_x.set)
        self.list_menu.pack(expand=YES, fill=BOTH)  # put this line under scrollbar_.pack()

        self.list_menu.bind('<ButtonRelease-1>', self.mouse_release_menu)
        self.list_menu.bind('<Button-1>', self.mouse_click)
        self.list_menu.bind('<Double-Button-1>', self.mouse_double_click)

    def setup_ui_log_area(self, frame):
        self.list_log = Listbox(frame, width=40, selectmode=SINGLE, bg='#606060', fg='white')
        self.list_log.insert(0, 'Log ----------------')

        # scrollbar_y = Scrollbar(frame, width=20)
        scrollbar_y = Scrollbar(frame)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        scrollbar_x = Scrollbar(frame, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        scrollbar_y.config(command=self.list_log.yview)
        scrollbar_x.config(command=self.list_log.xview)

        self.list_log.config(yscrollcommand=scrollbar_y.set)
        self.list_log.config(xscrollcommand=scrollbar_x.set)
        self.list_log.pack(expand=YES, fill=BOTH)  # put this line under scrollbar_.pack()

        self.list_log.bind('<Double-Button-1>', self.popup_paused_log)

    def set_dial(self, dial):
        self.dial = dial

    def add_log(self, msg):
        self.list_log.insert(END, msg)
        # msg = msg.strip()
        while self.list_log.size() > MAX_LOG:
            self.list_log.delete(0)
        # if len(msg) > 0:
        #     self.listLog.insert(END, msg)
        self.list_log.yview_moveto(1)
        return

    def run(self, cmd_line):
        cmd_line = cmd_line.strip()
        if len(cmd_line) == 0:
            return

        if cmd_line == CMD_HELP:
            self.add_log_help()
            self.dial.record_cmd(cmd_line)
        elif cmd_line == CMD_PRINT_MENU:
            self.add_log_menu()
            self.dial.record_cmd(cmd_line)
        elif cmd_line == CMD_OPEN_MENU_FILE:
            open_dir_file('.\\' + self.menu_file_name, self)
            self.dial.record_cmd(cmd_line)
        elif cmd_line == CMD_OPEN_MENU_DIRECTORY:
            open_dir_file('.', self)
            self.dial.record_cmd(cmd_line)
        elif cmd_line == CMD_REFRESH_MENU:
            self.refresh_menu_list()
            self.dial.record_cmd(cmd_line)
        elif self.dial.run(cmd_line):
            pass
        else:
            self.add_log_unknown_cmd(cmd_line)
        return

    def run_cli(self, _):
        self.run(self.cli.get())
        self.cli.set("")
        return

    def get_selected_menu_item(self):
        tup1 = self.list_menu.curselection()
        if len(tup1) > 0:
            return self.user_factory_menu[tup1[0]].strip()
        else:
            return ""

    def mouse_click(self, _):
        self.mouse_click_count = 1
        return

    def mouse_double_click(self, _):
        self.mouse_click_count = 2
        return

    def mouse_release_menu(self, _):
        if self.mouse_click_count == 1:
            self.cli.set(self.get_selected_menu_item())
            self.entry_cli.focus_set()
        elif self.mouse_click_count == 2:
            self.run(MenulogApp.to_cmd_line(self.get_selected_menu_item()))
            self.cli.set("")
            self.entry_cli.focus_set()
        self.mouse_click_count = 0
        return

    def popup_paused_log(self, _):
        paused_log_list = []
        for i in range(0, self.list_log.size()):
            paused_log_list.append(self.list_log.get(i))
        top_level_popup = TopLevelPausedLog(self, paused_log_list)
        top_level_popup.grab_set()  # switch to modal window
        #     self.wait_window(pw) # This line is very important ! ! !
        return

    def refresh_menu_list(self):
        self.user_factory_menu = ['****** user menu ****** (file:' + self.menu_file_name + ')']

        user_menu = []
        if os.path.isfile(self.menu_file_name):
            f_user_menu = codecs.open(self.menu_file_name, 'r', 'utf-8')
            user_menu = f_user_menu.readlines()
            for item in user_menu:
                self.user_factory_menu.append(item)
            f_user_menu.close()
        else:
            f_user_menu = codecs.open(self.menu_file_name, 'w', 'utf-8')
            f_user_menu.close()

        if len(user_menu) == 0:
            self.user_factory_menu.append('<EMPTY>')

        self.user_factory_menu.append('****** factory menu ******')
        for item in self.factory_menu:
            self.user_factory_menu.append(item)

        self.list_menu.delete(0, tkinter.END)
        for item in self.user_factory_menu:
            self.list_menu.insert(END, self.to_view(item))

    @staticmethod
    def to_view(line):
        # m = re.search(PATTERN, line, re.DOTALL)
        m = re.search("(\\s?)(.+)//(.+)", line, flags=0)
        if m:
            return m.group(1) + "【" + m.group(3) + "】" + m.group(2)
        else:
            return line

        # arr_arg = line.strip().split('//', 1)
        # if len(arr_arg) > 1:
        #     return "【" + arr_arg[1] + "】"
        # else:
        #     return line

    @staticmethod
    def to_cmd_line(line):
        m = re.search("(.+)//(.+)", line.strip(), flags=0)
        if m:
            return m.group(1)
        else:
            return ''

    def add_log_unknown_cmd(self, cmd_line):
        self.menulog.add_log('')
        self.menulog.add_log("Error! Unknown Command : " + cmd_line)
        return

    def add_log_help(self):
        for item in self.lst_help:
            self.add_log(item)
        return

    def add_log_menu(self):
        for item in self.user_factory_menu:
            self.add_log(item)
        return


class TopLevelPausedLog(tkinter.Toplevel):
    def __init__(self, parent, paused_log_list):
        super().__init__()
        self.title('Paused Log')
        self.parent = parent

        scrollbar_y = Scrollbar(self)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        scrollbar_x = Scrollbar(self, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        txt_log = Text(self, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set, width=80, height=60,
                       bg='#D0D0D0',
                       fg='black', wrap='none')

        txt_log.pack(expand=YES, fill=BOTH)
        for item in paused_log_list:
            txt_log.insert(END, item)
            txt_log.insert(END, "\n")

        scrollbar_y.config(command=txt_log.yview)
        scrollbar_x.config(command=txt_log.xview)

        txt_log.yview_moveto(1)

        self.geometry('1200x600')
        self.geometry('+200+200')
