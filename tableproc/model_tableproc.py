from menulogbase import MenulogApp


class DataSet:
    def __init__(self):
        self.lst_input_a = None
        self.lst_input_b = None
        self.lst_output_a = None
        self.lst_output_b = None
        self.hasBlockError = False

    def clear(self):
        self.lst_input_a = []
        self.lst_input_b = []
        self.lst_output_a = []
        self.lst_output_b = []
        self.hasBlockError = False
        return


def to_text(lst_text):
    str_text = ''
    for item in lst_text:
        str_text = str_text + item + "\n"
    return str_text


def to_list(s_text):
    return s_text.strip().split('\n')


def check_match(data_set: DataSet, menulog: MenulogApp):
    data_set.hasBlockError = False
    if len(data_set.lst_input_a) == 1 and data_set.lst_input_a[0].strip() == '':
        menulog.add_log('Error! No data in InputA')
        return
    if len(data_set.lst_input_b) == 1 and data_set.lst_input_b[0].strip() == '':
        menulog.add_log('Error! No data in InputB')
        return

    data_set.lst_output_a = [''] * len(data_set.lst_input_a)
    data_set.lst_output_b = [''] * len(data_set.lst_input_b)

    data_set.hasBlockError = False
    check_repeat('InputA', data_set.lst_input_a, data_set.lst_output_a, data_set, menulog)
    check_repeat('InputB', data_set.lst_input_b, data_set.lst_output_b, data_set, menulog)

    if not data_set.hasBlockError:
        check_match_no_repeat('InputA', data_set.lst_input_a, data_set.lst_input_b,
                              data_set.lst_output_a, data_set, menulog)
        check_match_no_repeat('InputB', data_set.lst_input_b, data_set.lst_input_a,
                              data_set.lst_output_b, data_set, menulog)

    if not data_set.hasBlockError:
        menulog.add_log('')
        menulog.add_log('OK! Success in check.')
    else:
        menulog.add_log('!!!!!!!!!!!!!!!!')
        menulog.add_log('Warning! Found some problems in data.')

    return


def check_repeat(lst_name, lst, lst_result, data_set: DataSet, menulog: MenulogApp):
    for i in range(0, len(lst)):
        if len(lst[i]) > 0:
            for j in range(i + 1, len(lst)):
                if lst[i] == lst[j]:
                    lst_result[i:i + 1] = ['repeat']
                    lst_result[j:j + 1] = ['repeat']
                    menulog.add_log('Repeat in ' + lst_name + ' : ' + str(i) + ',' + str(j))
                    data_set.hasBlockError = True
    return


def check_match_no_repeat(lst1name, lst1, lst2, lst_result, data_set: DataSet, menulog: MenulogApp):
    for i1 in range(0, len(lst1)):
        if len(lst1[i1]) > 0:
            b_has_match = False

            for i2 in range(0, len(lst2)):
                if lst1[i1] == lst2[i2]:
                    b_has_match = True
                    break

            if not b_has_match:
                lst_result[i1:i1 + 1] = ['No Match']
                menulog.add_log('No match in ' + lst1name + ' : ' + str(i1))
                data_set.hasBlockError = True
    return


def example_check_match_1(data_set: DataSet):
    data_set.clear()
    data_set.lst_input_a = [
        "dog",
        "donkey",
        "horse",
        "lion",
        "tiger",
        "",
        "dog",
        "deer",
        "",
        "",
        "wolf"
    ]
    data_set.lst_input_b = [
        "dog",
        "",
        "donkey",
        "",
        "horse",
        "lion",
        "tiger",
        "deer",
        "lion",
        "wolf"
    ]
    return


def example_check_match_2(data_set: DataSet):
    data_set.clear()

    data_set.lst_input_a = [
        "dog",
        "donkey",
        "horse",
        "",
        "lion",
        "tiger",
        "deer",
        "wolf"
    ]
    data_set.lst_input_b = [
        "dog",
        "donkey",
        "",
        "horse",
        "lion",
        "deer",
        "",
        "wolf",
        "cat",
        ""
    ]
    return
