from tkinter import *
import os
import tkinter as tkinter
import tkinter.font

from menulogbase import MenulogApp

TITLE = 'Menulog Example-1'
USER_MENU_FILE = 'dial_example1.txt'


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

    def record_cmd(self, cmd_line):
        self.last_cmd.set(cmd_line)
        self.cmd_counter.set(self.cmd_counter.get() + 1)

        self.menulog.add_log('')
        self.menulog.add_log(cmd_line)
        return

    @staticmethod
    # def run(self, cmd_line) -> bool:
    def run(_) -> bool:
        # if cmd_line == CMD_HELP:
        #     pass
        #     return True
        # else:
        #     pass
        #     return False
        return False

    @staticmethod
    def get_lst_help():
        return [
            "Help",
            "帮助",
            "",
            ""
        ]

    @staticmethod
    def get_factory_menu():
        return [
            "",
            "UNDER CONSTRUCTION",
            "",
            "UNDER CONSTRUCTION",
            "",
            "UNDER CONSTRUCTION",
            "",
            ""
        ]


if __name__ == '__main__':
    menulog = MenulogApp(TITLE, os.path.join(os.path.dirname(__file__), USER_MENU_FILE))
    menulog.set_dial(Dial(menulog))

    menulog.mainloop()
