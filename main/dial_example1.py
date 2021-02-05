from tkinter import *
from menulogbase import MyApp
from menulogbase import TopLevelPausedLog

import tkinter as tkinter
import tkinter.font


class Dial(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent.dialframe)
        self.parent = parent
        self.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

        # self.config(bd=1, relief=tkinter.SOLID)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        tkinter.Label(self, text='DIAL board', width=20).grid(row=0, column=0, columnspan=4, sticky=tkinter.NSEW,
                                                              pady=5)

        image01 = PhotoImage(file="01.gif")
        labelImage1 = tkinter.Label(self, image=image01)
        labelImage1.image = image01
        labelImage1.grid(row=1, column=0, pady=5)

        labelImage2 = tkinter.Label(self, image=image01)
        labelImage2.image = image01
        labelImage2.grid(row=1, column=1, pady=5)

        image02 = PhotoImage(file="02.gif")
        labelImage3 = tkinter.Label(self, image=image02)
        labelImage3.image = image02
        labelImage3.grid(row=1, column=2, pady=5)

        labelImage4 = tkinter.Label(self, image=image02)
        labelImage4.image = image02
        labelImage4.grid(row=1, column=3, pady=5)

        row1 = tkinter.Frame(self)
        row1.grid(row=2, column=0, columnspan=4, sticky=tkinter.NSEW, pady=5)
        tkinter.Label(row1, text='Parameter1:', width=10).pack(side=tkinter.LEFT)
        self.param1 = tkinter.StringVar()
        tkinter.Entry(row1, textvariable=self.param1, width=36).pack(side=tkinter.LEFT)

        row2 = tkinter.Frame(self)
        row2.grid(row=3, column=0, columnspan=4, sticky=tkinter.NSEW, pady=5)
        tkinter.Label(row2, text='Parameter2:', width=10).pack(side=tkinter.LEFT)
        self.param2 = tkinter.IntVar()
        tkinter.Entry(row2, textvariable=self.param2, width=36).pack(side=tkinter.LEFT)

    def run(self, cmdln):
        cmdln = cmdln.strip()
        self.param1.set(cmdln)
        self.parent.addLog(cmdln)
        return


def factoryMenu():
    lstMenu = [
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
    return lstMenu


if __name__ == '__main__':
    app = MyApp('dial_example1.txt', factoryMenu())
    app.setDial(Dial(app))

    app.mainloop()
