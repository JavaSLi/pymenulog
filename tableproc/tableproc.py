from tkinter import *
from menulogbase import MenulogApp

import tkinter as tkinter
import tkinter.font


def to_text(lst_text):
    str_text = ''
    for item in lst_text:
        str_text = str_text + item + "\n"
    return str_text


def to_list(s_text):
    return s_text.strip().split('\n')


class Dial(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent.dial_frame)
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

    def run(self, cmd_line):
        cmd_line = cmd_line.strip()
        if cmd_line == 'checkMatch':
            self.check_match(cmd_line)
        elif cmd_line == 'exampleCheckMatch1':
            self.example_check_match_1(cmd_line)
        elif cmd_line == 'exampleCheckMatch2':
            self.example_check_match_2(cmd_line)
        else:
            self.parent.add_log('')
            self.parent.add_log("Error! Illegal Command : " + cmd_line)
        return

    def check_match(self, cmd_line):
        self.parent.add_log('')
        self.parent.add_log(cmd_line)

        self.txtOutputA.delete(0.0, END)
        self.txtOutputB.delete(0.0, END)
        lst_input_a = to_list(self.txtInputA.get(0.0, END))
        lst_input_b = to_list(self.txtInputB.get(0.0, END))

        if len(lst_input_a) == 1 and lst_input_a[0].strip() == '':
            self.parent.add_log('Error! No data in InputA')
            return
        if len(lst_input_b) == 1 and lst_input_b[0].strip() == '':
            self.parent.add_log('Error! No data in InputB')
            return

        lst_output_a = [''] * len(lst_input_a)
        lst_output_b = [''] * len(lst_input_b)

        self.hasBlockError = False
        self.check_repeat('InputA', lst_input_a, lst_output_a)
        self.check_repeat('InputB', lst_input_b, lst_output_b)

        if not self.hasBlockError:
            self.check_match_no_repeat('InputA', lst_input_a, lst_input_b, lst_output_a)
            self.check_match_no_repeat('InputB', lst_input_b, lst_input_a, lst_output_b)

        self.txtOutputA.insert(END, to_text(lst_output_a))
        self.txtOutputB.insert(END, to_text(lst_output_b))

        if not self.hasBlockError:
            self.parent.add_log('')
            self.parent.add_log('OK! Success in check.')
        else:
            self.parent.add_log('!!!!!!!!!!!!!!!!')
            self.parent.add_log('Warning! Found some problems in data.')

        return

    def check_repeat(self, lst_name, lst, lst_result):
        for i in range(0, len(lst)):
            for j in range(i + 1, len(lst)):
                if lst[i] == lst[j]:
                    lst_result[i:i + 1] = ['repeat']
                    lst_result[j:j + 1] = ['repeat']
                    self.parent.add_log('Repeat in ' + lst_name + ' : ' + str(i) + ',' + str(j))
                    self.hasBlockError = True
        return

    def check_match_no_repeat(self, lst1name, lst1, lst2, lst_result):
        for i1 in range(0, len(lst1)):
            b_has_match = False
            for i2 in range(0, len(lst2)):
                if lst1[i1] == lst2[i2]:
                    b_has_match = True
                    break
            if not b_has_match:
                lst_result[i1:i1 + 1] = ['No Match']
                self.parent.add_log('No match in ' + lst1name + ' : ' + str(i1))
                self.hasBlockError = True
        return

    def clear_text_boxes(self):
        self.txtInputA.delete(0.0, END)
        self.txtInputB.delete(0.0, END)
        self.txtOutputA.delete(0.0, END)
        self.txtOutputB.delete(0.0, END)
        return

    def example_check_match_1(self, cmd_line):
        self.parent.add_log('')
        self.parent.add_log(cmd_line)
        self.clear_text_boxes()
        lst_input_a = [
            "dog",
            "donkey",
            "horse",
            "lion",
            "tiger",
            "dog",
            "deer",
            "wolf"
        ]
        lst_input_b = [
            "dog",
            "donkey",
            "horse",
            "lion",
            "tiger",
            "deer",
            "lion",
            "wolf"
        ]
        self.txtInputA.insert(END, to_text(lst_input_a))
        self.txtInputB.insert(END, to_text(lst_input_b))

        return

    def example_check_match_2(self, cmd_line):
        self.parent.add_log('')
        self.parent.add_log(cmd_line)
        self.clear_text_boxes()

        lst_input_a = [
            "dog",
            "donkey",
            "horse",
            "lion",
            "tiger",
            "deer",
            "wolf"
        ]
        lst_input_b = [
            "dog",
            "donkey",
            "horse",
            "lion",
            "tiger1",
            "deer",
            "wolf"
        ]
        self.txtInputA.insert(END, to_text(lst_input_a))
        self.txtInputB.insert(END, to_text(lst_input_b))

        return


def prepare_factory_menu():
    lst_menu = [
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
    return lst_menu


if __name__ == '__main__':
    app = MenulogApp('menulog-table-process', 'dial_tableproc.txt', prepare_factory_menu())
    app.set_dial(Dial(app))

    app.mainloop()
