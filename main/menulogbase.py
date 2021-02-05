from tkinter import *

import tkinter as tkinter
import tkinter.font
import os
import codecs


class TopLevelPausedLog(tkinter.Toplevel):
    def __init__(self, parent, pausedloglist):
        super().__init__()
        self.title('Paused Log')
        self.parent = parent

        self.listLog = Listbox(self, selectmode=SINGLE, width=80, height=60, bg='#D0D0D0', fg='black')

        for item in pausedloglist:
            self.listLog.insert(END, item)
        self.listLog.yview_moveto(1)

        sc = tkinter.Scrollbar(self)
        sc.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        sc['command'] = self.listLog.yview  # Same as sc.configure(command=self.listLog.yview)

        self.listLog.config(yscrollcommand=sc.set)
        self.listLog.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.listLog.bind('<Double-Button-1>', self.copyLogCLI)

        self.geometry('1000x600')
        self.geometry('+200+200')

    def copyLogCLI(self, event):
        tup1 = self.listLog.curselection()
        if len(tup1) > 0:
            self.parent.cli.set(self.listLog.get(tup1[0]).strip())
            self.parent.entryCLI.focus_set()
            self.destroy()
        return

class MyApp(tkinter.Tk):
    def __init__(self, menuFilename, factoryMenu):
        super().__init__()
        self.title('Menulog')

        self.cli = tkinter.StringVar()
        fontemp = tkinter.font.Font(self, size=12, weight='bold', underline=False)
        # ------------------------------------------------------
        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(2, weight=2)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)

        # ------------------------------------------------------
        self.listMenu = Listbox(self.frame, width=40, selectmode=SINGLE, font=fontemp)

        self.userMenu = self.readMenuFile(menuFilename, factoryMenu)
        for item in self.userMenu:
            self.listMenu.insert(END, self.toView(item))

        scrollMenu = tkinter.Scrollbar(self.frame, width=20)
        scrollMenu['command'] = self.listMenu.yview  # Same as scrollMenu.configure(command=self.listMenu.yview)
        scrollMenu.grid(row=0, column=1, rowspan=3, sticky=tkinter.E + tkinter.NS)

        self.listMenu.config(yscrollcommand=scrollMenu.set)
        self.listMenu.grid(row=0, column=0, rowspan=3, sticky=tkinter.NSEW)

        # self.listMenu.bind('<ButtonRelease-1>', self.copyMenuCLI)
        self.listMenu.bind('<Button-1>', self.copyMenuCLI)
        self.listMenu.bind('<Double-Button-1>', self.runMenu)
        # ------------------------------------------------------
        self.listLog = Listbox(self.frame, width=48, selectmode=SINGLE, bg='#606060', fg='white')
        self.listLog.insert(0, 'Log ----------------')

        scrollLog = tkinter.Scrollbar(self.frame, width=20)
        # scrollLog['command']=self.listLog.yview #Same as scrollLog.configure(command=self.listLog.yview)
        scrollLog.configure(command=self.listLog.yview)
        scrollLog.grid(row=0, column=3, sticky=tkinter.E + tkinter.NS)

        self.listLog.config(yscrollcommand=scrollLog.set)
        #     self.listLog.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
        self.listLog.grid(row=0, column=2, sticky=tkinter.NSEW)

        #     self.listLog.bind('<Button-1>', self.setName)
        self.listLog.bind('<Double-Button-1>', self.popupPausedLog)
        # ------------------------------------------------------
        rowCLI = tkinter.Frame(self.frame)
        tkinter.Label(rowCLI, text='Command：', width=9).pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.entryCLI = tkinter.Entry(rowCLI, textvariable=self.cli, width=50, bg='#606060', fg='white')
        self.entryCLI.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        rowCLI.grid(row=1, column=2, columnspan=2, sticky=tkinter.EW, pady=10)
        self.entryCLI.bind("<Return>", self.runCLI)
        # ------------------------------------------------------
        dialArea = tkinter.Frame(self.frame)
        dialArea.grid(row=2, column=2, columnspan=2, sticky=tkinter.NSEW, pady=5, padx=5)
        dialArea.config(bd=3, relief=tkinter.SOLID)

        # dialArea.rowconfigure(0,weight=0)
        # dialArea.rowconfigure(1,weight=1)
        tkinter.Label(dialArea, text='DIAL board', bg='#000080', fg='white', width=20).pack(side=tkinter.TOP,
                                                                                            fill=tkinter.X)
        self.dialframe = tkinter.Frame(dialArea)
        self.dialframe.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.geometry('1200x800')

    #     self.setupUI()
    def toView(self, line):
        arrArg = line.strip().split('//', 1)
        if len(arrArg) > 1:
            return "【" + arrArg[1] + "】"
        else:
            return line

    def toCmdln(self, line):
        arrArg = line.strip().split('//', 1)
        if len(arrArg) > 1:
            return arrArg[0]
        else:
            return line.strip()

    def setDial(self, dial):
        self.dial = dial

    def addLog(self, msg):
        self.listLog.insert(END, msg)
        # msg = msg.strip()
        while self.listLog.size() > 20:
            self.listLog.delete(0)
        # if len(msg) > 0:
        #     self.listLog.insert(END, msg)
        self.listLog.yview_moveto(1)
        return

    def runCLI(self, event):
        self.dial.run(self.toCmdln(self.cli.get()))
        self.cli.set("")
        return

    def getSeletecMenuItem(self):
        tup1 = self.listMenu.curselection()
        if len(tup1) > 0:
            return self.userMenu[tup1[0]].strip()
        else:
            return ""

    def runMenu(self, event):
        self.dial.run(self.toCmdln(self.getSeletecMenuItem()))
        self.cli.set("")
        return

    def copyMenuCLI(self, event):
        self.cli.set(self.getSeletecMenuItem())
        self.entryCLI.focus_set()
        return

    def popupPausedLog(self, event):
        pausedloglist = []
        for i in range(0, self.listLog.size()):
            pausedloglist.append(self.listLog.get(i))
        toplevel = TopLevelPausedLog(self, pausedloglist)
        toplevel.grab_set()  # switch to modal window
        #     self.wait_window(pw) # This line is very important ! ! !
        return

    def readMenuFile(self, filename, factoryMenu):
        if os.path.isfile(filename) == False:
            fo = codecs.open(filename, 'w', 'utf-8')
            for item in factoryMenu:
                fo.write(item + "\n")
            fo.close()

        userMenu = []
        if os.path.isfile(filename) == True:
            fRead = codecs.open(filename, 'r', 'utf-8')
            userMenu = fRead.readlines()
            fRead.close()

        return userMenu