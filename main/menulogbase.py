from tkinter import *

import tkinter as tkinter
import tkinter.font
import os
import codecs
import subprocess

MAX_LOG = 1000

SPLITTER_CMD_ARG = ' '
SPLITTER_COMMENT = '//'

CMD_HELP = 'help'
CMD_PRINT_MENU = 'menu'
CMD_OPEN_DIRECTORY = 'openDir'
CMD_OPEN_FILE = 'openFile'
CMD_REFRESH_MENU = 'refreshMenu'


class MenulogApp(tkinter.Tk):
    def __init__(self, title, path_menu_file):
        super().__init__()

        self.title(title)
        self.path_menu_file = path_menu_file
        self.path_menu_dir = os.path.abspath(os.path.dirname(self.path_menu_file))

        self.user_factory_menu = []
        self.lst_help = []

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
        self.prepare_help()
        self.refresh_menu_list()
        return

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

        if self.dial.run(cmd_line):
            pass
        elif cmd_line == CMD_HELP:
            self.add_log_help()
            self.dial.record_cmd(cmd_line)
        elif cmd_line == CMD_PRINT_MENU:
            self.add_log_menu()
            self.dial.record_cmd(cmd_line)
        elif cmd_line == CMD_REFRESH_MENU:
            self.refresh_menu_list()
            self.dial.record_cmd(cmd_line)
        elif self.try_open_dir(cmd_line):
            self.dial.record_cmd(cmd_line)
        elif self.try_open_file(cmd_line):
            self.dial.record_cmd(cmd_line)
        else:
            self.add_log_unknown_cmd(cmd_line)
        return

    def run_cli(self, _):
        self.run(self.cli.get())
        self.cli.set("")
        return

    @staticmethod
    def to_lst_cmd_args(line):
        m = re.search("(.+)//(.+)", line.strip(), flags=0)
        if m:
            return m.group(1).split(SPLITTER_CMD_ARG)
        else:
            return line.split(SPLITTER_CMD_ARG)

    def try_open_dir(self, cmd_line) -> bool:
        lst_cmd_arg = self.to_lst_cmd_args(cmd_line)
        if len(lst_cmd_arg) == 2 and lst_cmd_arg[0] == CMD_OPEN_DIRECTORY:
            self.open_dir_file(lst_cmd_arg[1])
            return True
        return False

    def try_open_file(self, cmd_line) -> bool:
        lst_cmd_arg = self.to_lst_cmd_args(cmd_line)
        if len(lst_cmd_arg) == 2 and lst_cmd_arg[0] == CMD_OPEN_FILE:
            self.open_dir_file(lst_cmd_arg[1])
            return True
        return False

    def open_dir_file(self, path_file):
        try:
            os.startfile(path_file)
        except Exception as e:
            self.add_log(e)
            subprocess.Popen(['xdg-open', path_file])

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
        self.add_log('')
        self.add_log("Error! Unknown Command : " + cmd_line)
        return

    def add_log_help(self):
        for item in self.lst_help:
            self.add_log(item)
        return

    def add_log_menu(self):
        for item in self.user_factory_menu:
            self.add_log(item)
        return

    def refresh_menu_list(self):
        user_menu_file = []
        if os.path.isfile(self.path_menu_file):
            f_user_menu = codecs.open(self.path_menu_file, 'r', 'utf-8')
            user_menu_file = f_user_menu.readlines()
            f_user_menu.close()
        else:
            f_user_menu = codecs.open(self.path_menu_file, 'w', 'utf-8')
            f_user_menu.close()

        if len(user_menu_file) == 0:
            user_menu_file = ['<EMPTY>']

        #################################################
        lst_common_factory_menu = [
            "*******************************",
            "",
            CMD_OPEN_FILE + SPLITTER_CMD_ARG + self.path_menu_file + SPLITTER_COMMENT + "打开用户菜单文件",
            "",
            CMD_REFRESH_MENU + SPLITTER_COMMENT + "刷新菜单",
            "",
            CMD_OPEN_DIRECTORY + SPLITTER_CMD_ARG + self.path_menu_dir + SPLITTER_COMMENT + "打开目录",
            "",
            CMD_PRINT_MENU + SPLITTER_COMMENT + "打印菜单",
            "",
            CMD_HELP + SPLITTER_COMMENT + "帮助",
            ""
        ]
        self.user_factory_menu = ['****** user menu ****** (file:' + self.path_menu_file + ')'] \
            + user_menu_file \
            + ['****** factory menu ******'] + self.dial.get_factory_menu() \
            + lst_common_factory_menu
        #################################################
        self.list_menu.delete(0, tkinter.END)
        for item in self.user_factory_menu:
            self.list_menu.insert(END, self.to_view(item))

    def prepare_help(self):
        lst_common_help = [
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
            "请试一试命令(" + CMD_OPEN_DIRECTORY + ")打开菜单目录，编辑菜单文件。",
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
        self.lst_help = self.dial.get_lst_help() + lst_common_help
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
