from tkinter import *

import tkinter as tkinter
import tkinter.font
import os
import codecs


class MenulogApp(tkinter.Tk):
    def __init__(self, title, menu_file_name, factory_menu):
        super().__init__()

        self.title(title)
        self.MAX_LOG = 1000

        self.cli = tkinter.StringVar()
        self.mouse_click_count = 0
        self.list_menu = None
        self.list_log = None
        self.entry_cli = None
        self.dial_frame = None

        self.dial = None

        self.user_factory_menu = self.read_menu_file(menu_file_name, factory_menu)

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

        for item in self.user_factory_menu:
            self.list_menu.insert(END, self.to_view(item))

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
        while self.list_log.size() > self.MAX_LOG:
            self.list_log.delete(0)
        # if len(msg) > 0:
        #     self.listLog.insert(END, msg)
        self.list_log.yview_moveto(1)
        return

    def run_cli(self, _):
        self.dial.run(self.cli.get())
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
            self.dial.run(MenulogApp.to_cmd_line(self.get_selected_menu_item()))
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
    def read_menu_file(filename, factory_menu):
        user_factory_menu = ['****** user menu ****** (file:' + filename + ')']
        # if not os.path.isfile(filename):
        #     fo = codecs.open(filename, 'w', 'utf-8')
        #     # for item in factory_menu:
        #     #     fo.write(item + "\n")
        #     fo.close()

        user_menu = []
        if os.path.isfile(filename):
            f_user_menu = codecs.open(filename, 'r', 'utf-8')
            user_menu = f_user_menu.readlines()
            for item in user_menu:
                user_factory_menu.append(item)
            f_user_menu.close()
        else:
            f_user_menu = codecs.open(filename, 'w', 'utf-8')
            f_user_menu.close()

        if len(user_menu) == 0:
            user_factory_menu.append('<EMPTY>')

        user_factory_menu.append('****** factory menu ******')
        for item in factory_menu:
            user_factory_menu.append(item)

        return user_factory_menu

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
        # arr_arg = line.strip().split('//', 1)
        # if len(arr_arg) > 1:
        #     return arr_arg[0]
        # else:
        #     return ''


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
