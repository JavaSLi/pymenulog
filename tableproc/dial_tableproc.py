from tkinter import *
from menulogbase import MenulogApp

import model_tableproc
from model_tableproc import DataSet

import tkinter as tkinter
import tkinter.font
import menulogbase

TITLE = 'menulog-table-process'
USER_MENU_FILE = 'dial_tableproc.txt'

CMD_CHECK_MATCH = 'checkMatch'
CMD_EXAMPLE_1 = 'exampleCheckMatch1'
CMD_EXAMPLE_2 = 'exampleCheckMatch2'


class Dial(tkinter.Frame):
    def __init__(self, parent_menulog):
        super().__init__(parent_menulog.dial_frame)
        self.menulog = parent_menulog

        self.txtInputA = None
        self.txtInputB = None
        self.txtOutputA = None
        self.txtOutputB = None

        self.setup_ui()

    def setup_ui(self):
        # ------------------------------------------------------
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
        self.txtOutputA = tkinter.Text(self, width=12, wrap='none')
        self.txtOutputA.grid(row=1, column=1, pady=1, sticky=tkinter.NSEW)

        tkinter.Label(self, text='InputB').grid(row=0, column=2, pady=2)
        self.txtInputB = tkinter.Text(self, width=12, wrap='none')
        self.txtInputB.grid(row=1, column=2, pady=1, sticky=tkinter.NSEW)

        tkinter.Label(self, text='OutputB').grid(row=0, column=3, pady=2)
        self.txtOutputB = tkinter.Text(self, width=12, wrap='none')
        self.txtOutputB.grid(row=1, column=3, pady=1, sticky=tkinter.NSEW)

    def get_data_model(self) -> DataSet:
        data_set = DataSet()
        data_set.lst_input_a = model_tableproc.to_list(self.txtInputA.get(0.0, END))
        data_set.lst_input_b = model_tableproc.to_list(self.txtInputB.get(0.0, END))
        data_set.lst_output_a = model_tableproc.to_list(self.txtOutputA.get(0.0, END))
        data_set.lst_output_b = model_tableproc.to_list(self.txtOutputB.get(0.0, END))
        return data_set

    def update_data(self, data_set: DataSet):
        self.txtInputA.delete(0.0, END)
        self.txtInputA.insert(END, model_tableproc.to_text(data_set.lst_input_a))
        self.txtInputB.delete(0.0, END)
        self.txtInputB.insert(END, model_tableproc.to_text(data_set.lst_input_b))
        self.txtOutputA.delete(0.0, END)
        self.txtOutputA.insert(END, model_tableproc.to_text(data_set.lst_output_a))
        self.txtOutputB.delete(0.0, END)
        self.txtOutputB.insert(END, model_tableproc.to_text(data_set.lst_output_b))

    def record_cmd(self, cmd_line):
        self.menulog.add_log('')
        self.menulog.add_log(cmd_line)
        return

    def run(self, cmd_line) -> bool:
        data_set = self.get_data_model()
        if cmd_line == 'checkMatch':
            self.record_cmd(cmd_line)
            model_tableproc.check_match(data_set, self.menulog)
            self.update_data(data_set)
            return True
        elif cmd_line == 'exampleCheckMatch1':
            self.record_cmd(cmd_line)
            model_tableproc.example_check_match_1(data_set)
            self.update_data(data_set)
            return True
        elif cmd_line == 'exampleCheckMatch2':
            self.record_cmd(cmd_line)
            model_tableproc.example_check_match_2(data_set)
            self.update_data(data_set)
            return True
        else:
            return False


def get_lst_help():
    lst_help = [
        "Help",
        "帮助",
        "",
        "功能：检查表格的对应关系",
        "",
        "先把两列数据（从EXCEL）分别拷贝粘贴到<InputA>列和<InputB>列",
        "运行命令 " + CMD_CHECK_MATCH,
        "",
        "首先，算法分别检查<InputA>列和<InputB>列中有无重复项",
        "如果有重复项，暂停进一步的检查，分别在<OutputA>列和<OutputB>列中指出重复位置。",
        "数据行数较多时，需要把数据拷贝到对应的EXCEL表中进行比对。",
        "在重复检查中，所有空格被忽略。",
        "",
        "然后，如果没有重复项，算法检查<InputA>列和<InputB>列中有无对应不上的项",
        "如果有对应不上的项，分别在<OutputA>列和<OutputB>列中指出位置。",
        "数据行数较多时，需要把数据拷贝到对应的EXCEL表中进行比对。",
        "在对应检查中，所有空格被忽略。",
        "",
        "例子1（有重复项的情况）",
        "运行命令 " + CMD_EXAMPLE_1,
        "",
        "例子2（有对应不上的项的情况，没有重复项）",
        "运行命令 " + CMD_EXAMPLE_2,
        "",
        "Support Chinese 汉字, Korean 조선어, Japanese にほんご",
        ""
    ]
    lst_help = lst_help + menulogbase.get_common_help_list()
    return lst_help


def prepare_factory_menu():
    lst_menu = [
        "",
        "功能：表格处理 Table data process",
        "",
        CMD_CHECK_MATCH + "//检查表格对应",
        "",
        "例子1（有重复项的情况）",
        CMD_EXAMPLE_1 + "//表格对应_EXAMPLE_1",
        "",
        "例子2（有对应不上的项的情况，没有重复项）",
        CMD_EXAMPLE_2 + "//表格对应_EXAMPLE_2",
        "",
        ""
    ]
    lst_menu = lst_menu + menulogbase.get_common_factory_menu()
    return lst_menu


if __name__ == '__main__':
    menulog = MenulogApp(TITLE, USER_MENU_FILE, prepare_factory_menu(), get_lst_help())
    menulog.set_dial(Dial(menulog))

    menulog.mainloop()
