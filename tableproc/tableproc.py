from tkinter import *
from menulogbase import MyApp
from menulogbase import TopLevelPausedLog

import tkinter as tkinter
import tkinter.font


class Dial(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent.dialframe)
        self.parent = parent
        self.hasBlockError = False

        self.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        tkinter.Label(self, text='InputA').grid(row=0, column=0, pady=2)
        self.txtInputA = tkinter.Text(self, width=12, wrap='none')
        self.txtInputA.grid(row=1, column=0, pady=1, sticky=tkinter.NSEW)

        tkinter.Label(self, text='OutputA').grid(row=0, column=1, pady=2)
        self.txtOutputA = tkinter.Text(self, width=12)
        self.txtOutputA.grid(row=1, column=1, pady=1, sticky=tkinter.NSEW)

        tkinter.Label(self, text='InputB').grid(row=0, column=2, pady=2)
        self.txtInputB = tkinter.Text(self, width=12)
        self.txtInputB.grid(row=1, column=2, pady=1, sticky=tkinter.NSEW)

        tkinter.Label(self, text='OutputB').grid(row=0, column=3, pady=2)
        self.txtOutputB = tkinter.Text(self, width=12)
        self.txtOutputB.grid(row=1, column=3, pady=1, sticky=tkinter.NSEW)

    def run(self, cmdln):
        cmdln = cmdln.strip()
        if cmdln == 'checkMatch':
            self.checkMatch(cmdln)
        elif cmdln == 'exampleCheckMatch1':
            self.exampleCheckMatch1(cmdln)
        elif cmdln == 'exampleCheckMatch2':
            self.exampleCheckMatch2(cmdln)
        else:
            self.parent.addLog('')
            self.parent.addLog("Error! Illegal Command : " + cmdln)
        return

    def checkMatch(self, cmdln):
        self.parent.addLog('')
        self.parent.addLog(cmdln)

        self.txtOutputA.delete(0.0, END)
        self.txtOutputB.delete(0.0, END)
        lstInputA = self.toList(self.txtInputA.get(0.0, END))
        lstInputB = self.toList(self.txtInputB.get(0.0, END))

        if len(lstInputA) == 1 and lstInputA[0].strip() == '':
            self.parent.addLog('Error! No data in InputA')
            return
        if len(lstInputB) == 1 and lstInputB[0].strip() == '':
            self.parent.addLog('Error! No data in InputB')
            return

        lstOutputA = []
        for item in lstInputA:
            lstOutputA.append('')
        lstOutputB = []
        for item in lstInputB:
            lstOutputB.append('')

        self.hasBlockError = False
        self.check_repeat('InputA', lstInputA, lstOutputA)
        self.check_repeat('InputB', lstInputB, lstOutputB)

        if self.hasBlockError == False:
            self.check_match_no_repeat('InputA', lstInputA, lstInputB, lstOutputA)
            self.check_match_no_repeat('InputB', lstInputB, lstInputA, lstOutputB)

        self.txtOutputA.insert(END, self.toText(lstOutputA))
        self.txtOutputB.insert(END, self.toText(lstOutputB))

        if self.hasBlockError == False:
            self.parent.addLog('')
            self.parent.addLog('OK! Success in check.')
        else:
            self.parent.addLog('!!!!!!!!!!!!!!!!')
            self.parent.addLog('Warning! Found some problems in data.')

        return

    def check_repeat(self, lstname, lst, lstResult):
        for i in range(0, len(lst)):
            for j in range(i+1, len(lst)):
                if lst[i] == lst[j]:
                    lstResult[i:i+1] = ['repeat']
                    lstResult[j:j+1] = ['repeat']
                    self.parent.addLog('Repeat in ' + lstname + ' : ' + str(i) + ',' + str(j))
                    self.hasBlockError = True
        return
    def check_match_no_repeat(self, lst1name, lst1, lst2, lstResult):
        for i1 in range(0, len(lst1)):
            bHasMatch = False
            for i2 in range(0, len(lst2)):
                if lst1[i1] == lst2[i2]:
                    bHasMatch = True
                    break
            if bHasMatch == False:
                lstResult[i1:i1 + 1] = ['No Match']
                self.parent.addLog('No match in ' + lst1name + ' : ' + str(i1))
                self.hasBlockError = True
        return
    def clear_text_boxes(self):
        self.txtInputA.delete(0.0, END)
        self.txtInputB.delete(0.0, END)
        self.txtOutputA.delete(0.0, END)
        self.txtOutputB.delete(0.0, END)
        return
    def exampleCheckMatch1(self, cmdln):
        self.parent.addLog('')
        self.parent.addLog(cmdln)
        self.clear_text_boxes()
        lstInputA = [
            "dog",
            "donkey",
            "horse",
            "lion",
            "tiger",
            "dog",
            "deer",
            "wolf"
            ]
        lstInputB = [
            "dog",
            "donkey",
            "horse",
            "lion",
            "tiger",
            "deer",
            "lion",
            "wolf"
            ]
        self.txtInputA.insert(END, self.toText(lstInputA))
        self.txtInputB.insert(END, self.toText(lstInputB))

        return
    def exampleCheckMatch2(self, cmdln):
        self.parent.addLog('')
        self.parent.addLog(cmdln)
        self.clear_text_boxes()

        lstInputA = [
            "dog",
            "donkey",
            "horse",
            "lion",
            "tiger",
            "deer",
            "wolf"
            ]
        lstInputB = [
            "dog",
            "donkey",
            "horse",
            "lion",
            "tiger1",
            "deer",
            "wolf"
            ]
        self.txtInputA.insert(END, self.toText(lstInputA))
        self.txtInputB.insert(END, self.toText(lstInputB))

        return

    def toList(self, sText):
        return sText.strip().split('\n')

    def toText(self, lst_text):
        str_text = ''
        for item in lst_text:
            str_text = str_text + item + "\n"
        return str_text

def factoryMenu():
    lstMenu = [
        "Table data process",
        "HELP",
        "  检查表格对应",
        "  帮助",
        "   先把两列数据（从EXCEL）分别拷贝粘贴到<InputA>列和<InputB>列",
        "   运行",
        "   checkMatch//检查表格对应",
        "   首先，检查<InputA>列和<InputB>列中有无重复项",
        "   如果有重复项，暂停，分别在<OutputA>列和<OutputB>列中指出重复项位置。",
        "   数据多时，需要拷贝到对应EXCEL表中进行比对。",
        "   然后，如果没有重复项，检查<InputA>列和<InputB>列中有无对应不上的项",
        "   如果有对应不上的项，分别在<OutputA>列和<OutputB>列中指出对应不上的项的位置。",
        "   数据多时，需要拷贝到对应EXCEL表中进行比对。",
        "   例子1（有重复项的情况）",
        "   exampleCheckMatch1//表格对应_EXAMPLE_1",
        "   例子2（有对应不上的项的情况，没有重复项）",
        "   exampleCheckMatch2//表格对应_EXAMPLE_2",
        "  Support Chinese 汉字, Korean 조선어, Japanese にほんご",
        "   "
    ]
    return lstMenu

if __name__ == '__main__':
    app = MyApp('menulog-table-process', 'dial_tableproc.txt', factoryMenu())
    app.setDial(Dial(app))

    app.mainloop()
