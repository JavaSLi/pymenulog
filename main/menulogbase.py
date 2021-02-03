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

    self.listLog = Listbox(self, selectmode=SINGLE, width=80, height=60)
    
    for item in pausedloglist:
        self.listLog.insert(END, item)
    self.listLog.yview_moveto(1)
        
    sc = tkinter.Scrollbar(self)
    sc.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    sc['command']=self.listLog.yview #Same as sc.configure(command=self.listLog.yview)

    self.listLog.config(yscrollcommand=sc.set)
    self.listLog.pack(side=tkinter.LEFT,fill=tkinter.BOTH, expand=1)
    
    self.listLog.bind('<Double-Button-1>', self.copyLogCLI)

    self.geometry('1000x600')
    self.geometry('+800+200')
  def copyLogCLI(self,event):
    tup1=self.listLog.curselection()
    if len(tup1)>0:
      self.parent.cli.set(self.listLog.get(tup1[0]).strip())
      self.destroy()
    return

class MyApp(tkinter.Tk):
  def __init__(self, menuFilename, factoryMenu):
    super().__init__()
    self.title('Menulog')

    self.cli = tkinter.StringVar()
    fontemp = tkinter.font.Font(self, size=12, weight='bold', underline = False)
#------------------------------------------------------
    self.frame=Frame(self)
    self.frame.pack(fill=BOTH, expand=1)
    self.frame.columnconfigure(0,weight=1) 
    self.frame.columnconfigure(2,weight=1) 
    self.frame.rowconfigure(0,weight=1)
    self.frame.rowconfigure(2,weight=1)
    
    self.listMenu = Listbox(self.frame, width=48, selectmode=SINGLE, font=fontemp)

    userMenu = self.readMenuFile(menuFilename, factoryMenu)
    for item in userMenu:
        self.listMenu.insert(END, item)
     
    scrollMenu = tkinter.Scrollbar(self.frame,width=20)
    scrollMenu['command']=self.listMenu.yview #Same as scrollMenu.configure(command=self.listMenu.yview)
    scrollMenu.grid(row=0,column=1,rowspan=3,sticky=tkinter.E+tkinter.NS)
 
    self.listMenu.config(yscrollcommand=scrollMenu.set)
    self.listMenu.grid(row=0,column=0,rowspan=3,sticky=tkinter.NSEW)
    
    self.listMenu.bind('<ButtonRelease-1>', self.copyMenuCLI)
    self.listMenu.bind('<Double-Button-1>', self.runMenu)
#------------------------------------------------------
    self.listLog = Listbox(self.frame, selectmode=SINGLE)
    self.listLog.insert(0,'Log ----------------')
    
    scrollLog = tkinter.Scrollbar(self.frame,width=20)
    scrollLog['command']=self.listLog.yview #Same as scrollLog.configure(command=self.listLog.yview)
    scrollLog.grid(row=0,column=3,sticky=tkinter.E+tkinter.NS)

    self.listLog.config(yscrollcommand=scrollLog.set)
#     self.listLog.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
    self.listLog.grid(row=0,column=2,sticky=tkinter.NSEW)
    
#     self.listLog.bind('<Button-1>', self.setName)
    self.listLog.bind('<Double-Button-1>', self.popupPausedLog)
#------------------------------------------------------
    rowCLI = tkinter.Frame(self.frame)
    tkinter.Label(rowCLI, text='Command：', width=9).pack(side=tkinter.LEFT,fill=tkinter.BOTH)
    entryCLI = tkinter.Entry(rowCLI, textvariable=self.cli, width=40)
    entryCLI.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
    rowCLI.grid(row=1,column=2,columnspan=2,sticky=tkinter.EW,pady=10)
    entryCLI.bind("<Return>", self.runCLI)

    self.geometry('1200x800')        

#     self.setupUI()
  def packdDial(self, dial):
    self.dial = dial
#------------------------------------------------------
#     self.dial.grid(row=2,column=2,columnspan=3)
#     dial = Dial(self)
    self.dial.grid(row=2,column=2,columnspan=2,sticky=tkinter.NSEW,pady=5,padx=5)
#     tkinter.Label(self, text='DIAL', width=16).grid(row=2,column=2,columnspan=3)

  def addLog(self,msg):
      msg = msg.strip()
      while self.listLog.size()>20:
        self.listLog.delete(0)
      if len(msg)>0:
        self.listLog.insert(END, msg)
      self.listLog.yview_moveto(1)
      return
  def runCLI(self,event):
    self.dial.run(self.cli.get())
    return
  def runMenu(self,event):
    tup1=self.listMenu.curselection()
    if len(tup1)>0:
#       self.cli.set('run'+self.listMenu.get(tup1[0]))
      self.dial.run(self.listMenu.get(tup1[0]))
    return
  def copyMenuCLI(self,event):
    tup1=self.listMenu.curselection()
    if len(tup1)>0:
      self.cli.set(self.listMenu.get(tup1[0]).strip())
    return
  def popupPausedLog(self,event):
    pausedloglist = []
    for i in range(0, self.listLog.size()):
        pausedloglist.append(self.listLog.get(i))
    toplevel = TopLevelPausedLog(self,pausedloglist)
    toplevel.grab_set()  # switch to modal window
#     self.wait_window(pw) # This line is very important ! ! !
    return
  def readMenuFile(self, filename, factoryMenu):
    if os.path.isfile(filename) == False:
      fo = codecs.open(filename,'w','utf-8')        
      for item in factoryMenu:
        fo.write(item + "\n")
      fo.close()

    userMenu = []
    if os.path.isfile(filename) == True:
      fRead = codecs.open(filename,'r','utf-8')
      userMenu = fRead.readlines()
      fRead.close()
    
    return userMenu
# if __name__ == '__main__':
#   app = MyApp()
#   app.mainloop()
# class Dial(tkinter.Frame):
#   def __init__(self, parent):
#     super().__init__()
#     # 第一行（两列）
#     row1 = tkinter.Frame(self)
#     row1.pack(fill="x")
#     tkinter.Label(row1, text='姓名：', width=8).pack(side=tkinter.LEFT)
#     self.name = tkinter.StringVar()
#     tkinter.Entry(row1, textvariable=self.name, width=20).pack(side=tkinter.LEFT)
#     # 第二行
#     row2 = tkinter.Frame(self)
#     row2.pack(fill="x", ipadx=1, ipady=1)
#     tkinter.Label(row2, text='年龄：', width=8).pack(side=tkinter.LEFT)
#     self.age = tkinter.IntVar()
#     tkinter.Entry(row2, textvariable=self.age, width=20).pack(side=tkinter.LEFT)
# 
# if __name__ == '__main__':
# #   dial = Dial()
# #   app = MyApp(Dial())
#   app = MyApp()
#   dial = Dial(app)
#   app.setupUI(dial)
#   app.mainloop()