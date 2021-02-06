from tkinter import *
from menulogbase import MenulogApp

import tkinter as tkinter
import tkinter.font


class Dial(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent.dial_frame)
        self.parent = parent
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
        tkinter.Label(row1, text='Parameter1:', width=10).pack(side=tkinter.LEFT)
        self.param1 = tkinter.StringVar()
        tkinter.Entry(row1, textvariable=self.param1, width=36).pack(side=tkinter.LEFT)

        row2 = tkinter.Frame(self)
        row2.grid(row=2, column=0, columnspan=4, sticky=tkinter.NSEW, pady=5)
        tkinter.Label(row2, text='Parameter2:', width=10).pack(side=tkinter.LEFT)
        self.param2 = tkinter.IntVar()
        tkinter.Entry(row2, textvariable=self.param2, width=36).pack(side=tkinter.LEFT)

    def run(self, cmd_line):
        cmd_line = cmd_line.strip()
        self.param1.set(cmd_line)
        self.parent.add_log(cmd_line)
        return


def prepare_factory_menu():
    lst_menu = [
        "Menu-example",
        "HELP",
        "  Menudialog consists of three parts, Menu-Area, Log-Area, and Dial-Area,",
        "    plus a command input-box.",
        "  Menu-Area has many lines of commands and comments.",
        "  Menu lines are often indented to show tree-structure",
        "  The command lines often use the format of 'command+/+/+comment',",
        "    and only comment part is shown in the Menu List",
        "  Log-Area lines are output from the running command,",
        "    and the new lines are often generated so quickly",
        "    that you can only glance over them rather than check them.",
        "  To check the detail of the Log,",
        "    you can double-click on Log-list,",
        "    then a sub-window with a paused log-list will popup.",
        "  To double-click on the paused log-list,",
        "    the popup sub-window will be closed,",
        "    and the selected line will be drop on the command input-box",
        "  Support Chinese 汉字, Korean 조선어, Japanese にほんご",
        "  "
    ]
    return lst_menu


if __name__ == '__main__':
    app = MenulogApp('menulog-example-1', 'dial_example1.txt', prepare_factory_menu())
    app.set_dial(Dial(app))

    app.mainloop()
