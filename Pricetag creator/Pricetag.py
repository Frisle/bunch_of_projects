from openpyxl import load_workbook
import os
import subprocess
import threading
import webbrowser
from tkinter import *
from tkinter import Frame, messagebox
from tkinter.ttk import *
import pyperclip
from refresh_module import quickWriteRefreshBox, textBoxRefresh, makeChangeInLits
from tooltip import Toplevel, CreateToolTip
import keyboard

helpText = """ 
Работа программы основана на использовании таблиц Excell и взаимодействию
с браузером для отрисовок ценников.

Основная функция заключается в копировании строк из таблиц для дальнейшей автоматической
обработки программой.

Работа с вводом данных для автоматической обработки

1. По открытию программы нажать Ввод из буфера (активируется 60 секундное окно для ввода)
2. Открыть таблицы Excell и скопировать требуемое количество строк и нажать CTRL + 
C или копировать через контекстное меню.
3. На этом этапе в окне в правой стороне программы появятся скопированные строки. Для вывода строк в виде ценников, сперва необходимо запустить локальный сервер.
Для этого нужно открыть низпадающее Меню в левом углу программы и выбрать Локальный сервер.
4.Следующий шаг - создать ценники. На этом этапе программа проверяет правильность ввода (есть возможность проверить их вручную). Для создания ценников нужно нажать
кнопку Создать этикетки в нижней части правой стороны программы. И следом нажать Вывод этикеток (если все ценники оформлены правильно)
"""

# строка указывает скрипту работать с файлом в нужной директории
cards_filepath = os.path.join(os.getcwd(), 'assets/cardsFile.txt')
path_To_Server = os.path.join(os.getcwd(), 'assets/launch.exe')
filepath_List = os.path.join(os.getcwd(), 'assets/list.txt')
read_Me_File = os.path.join(os.getcwd(), 'assets/README.txt')
auto_List_File = os.path.join(os.getcwd(), 'assets/auto_list.txt')
CSV_File_Path = os.path.join(os.getcwd(), "assets/testCsvFile.csv")
temp_xlsx = os.path.join(os.getcwd(), "assets/temp.xlsx")

try:
    f = open(cards_filepath, "r")
    f1 = open(filepath_List, "r")
    f2 = open(auto_List_File, "r")
    f3 = open(temp_xlsx, "r")
except FileNotFoundError:
    f = open(cards_filepath, "w")
    f.close()
    f1 = open(filepath_List, "w")
    f1.close()
    f2 = open(auto_List_File, "w")
    f2.close()
    f3 = open(temp_xlsx, "w")
    f3.close()
else:
    pass


class FilteredString:

    def clean(self, line):
        self.filtered = " "
        for sym in line:
            if sym != "'" and sym != "[" and sym != "]":
                self.filtered += sym

        return self.filtered


instance_filtered_class = FilteredString()


def main():  # ведущая функция содержащая весь основной код

    def browser():  # запускает браузер по-умолчанию для отрисовки карточек
        webbrowser.open('http://127.0.0.1:8000/assets/cardspage.html')

    def server():  # запускает локальный сервер для выгрузки страницы
        subprocess.Popen(path_To_Server)

    def button_swap():
        if chk_state.get() == True:
            new_state = "Очистить"
            write_in_file.configure(text=new_state)
        else:
            write_in_file.configure(text="Записать")

    def rewrite_files():
        file_list = open(filepath_List, "r+", encoding="utf-8")
        file_list.truncate(0)
        file_list.close()
        textBoxRefresh(filepath_List, e_list_display_box)
        combo_box_mod()
        file_cards = open(cards_filepath, "r+", encoding="utf-8")
        file_cards.truncate(0)
        file_cards.close()

    def cards_view():
        edit_window = Toplevel()
        edit_window.title("Обувной учет. Версия 1.0")
        edit_window.geometry('500x500+400+100')
        edit_window.iconbitmap('assets/tag_icon.ico')
        edit_window.resizable(False, False)
        edit_text_box = Text(edit_window, width=65, wrap=WORD, font='Arial 10', height=26)
        edit_text_box.place(x=15, y=10)
        with open(cards_filepath, "r", encoding="utf-8") as FileRead:
            text = FileRead.readlines()
            text1 = "".join(text)
            edit_text_box.insert(1.0, text1)

    # блок захвата буфера обмена и записи данных из таблиц Excell
    def write_from_clipboard():
        # блок перезаписи листа и инициализации буфера обмена
        b_clipboard_button.configure(text="Ввод активен")
        try:
            file = open(filepath_List, "a", encoding="utf-8")
            spam = pyperclip.waitForNewPaste(20)  # получение данных из буфера и хранение
            pyperclip.copy('')  # очистка буфера после сохранения данных в spam
            temp_string = " ".join(spam.split("\t"))  # превращение списка в строку с разделением пробелом
            file.write("{}".format(temp_string))
            file.close()
            textBoxRefresh(filepath_List, e_list_display_box)
            e_list_display_box.see([0])
        except Exception:
            messagebox.showinfo("INFO", "Ввод из буфера завершен")
            b_clipboard_button.configure(text="Буфер обмена")
            return

    print_tag_b = """
<p class=\"box\">Бренд: {}
_________________________
Арт.: {} / №: <b>{}</b> 
Мат.: {}
Цена: 


<b>Размеры</b>: {}</p>\n"""

    print_tag_m = """
<div class=\"box\">{}
___________
Арт.: {} 
№: <b class=\"bold\">{}</b> 
Мат.: {}
Цена: 



<p>{}</p></div>"""

    empty_tag = """
<p class=\"box\">Бренд: {}
_________________________
Арт.: {} / №: <b>{}</b> 
Мат.: {}
Цена: 



<b>"____, ____, ____, ____, ____, 
____, ____, ____, ____, ____"</b></p>"""

    def cards_format():

        # очистка готовых ценников перед записью
        file_cards = open(cards_filepath, "r+", encoding="utf-8")
        file_cards.truncate(0)
        file_cards.close()
        with open(filepath_List, "r", encoding="utf-8") as listFile:  # аргумент encoding кодирует текст в utf8
            data_massive = []
            for line in listFile:  # блок извлекающий информацию из файла
                data_massive.append(line.rsplit())  # метод делит целую строку на отдельные через запятую
                filtered_list = list(
                    filter(None, data_massive))  # фильтрует список от пробелов и создает лист с листами

            for x in filtered_list:  # основной блок извлекающий и сортирующий информацию из листа
                name = x[0]
                article = x[1]
                number = x[2]
                shoeType = x[3]
                price = x[4]
                material = x[5]
                collor = x[6]
                features = x[7]
                marker = x[8]
                sizes = x[9:]

                # логический блок конструирует карточки
                if len(sizes) >= 6:
                    print_sizes = "{}\n{}".format(str(x[9:14]), str(x[14:]))

                    clean_sizes = instance_filtered_class.clean(print_sizes)
                elif len(sizes) >= 8:
                    print_sizes = "{}\n{}\n{}".format(str(x[9:14]), str(x[14:20]), str(x[20:]))
                    clean_sizes = instance_filtered_class.clean(print_sizes)
                elif len(sizes) == 1:
                    print_sizes = "{}".format(str(x[9:]))
                    clean_sizes = instance_filtered_class.clean(print_sizes)
                else:
                    print_sizes = "{}".format(str(x[9:]))
                    clean_sizes = instance_filtered_class.clean(print_sizes)
                if number == "нет":
                    print_number = "{}".format(collor)
                else:
                    print_number = "{}".format(number)

                if name == "нет":
                    print_name = "{}".format(features.capitalize())
                else:
                    print_name = "{}".format(name)
                    clean_name = print_name.replace(".", " ")

                if len(name) > 6:
                    print_material = "{}".format(material)
                else:
                    print_material = "{}".format(material)

                if article == "нет":
                    print_articul = "{}".format(features)
                else:
                    print_articul = "{}".format(article)

                file = open(cards_filepath, "a", encoding="utf-8")  # блок записи в файл

                if marker == "М":  # маленькие карточки
                    print_tag = str(print_tag_m).format(clean_name, print_articul, print_number, print_material,
                                                        clean_sizes)
                    file.write(print_tag)

                    combo_box_mod()
                elif marker == "Б":
                    print_tag = str(print_tag_b).format(clean_name, print_articul, print_number, print_material,
                                                        clean_sizes)
                    file.write(print_tag)
                    file.close()
                    combo_box_mod()

    """except Exception:
    
    messagebox.showerror("Ошибка ввода", "Список пуст или данные введены неверно")
    return"""

    def empty_tags():
        i = 0
        while i < 20:
            file = open(cards_filepath, "a", encoding="utf-8")
            print_tag = str(empty_tag).format("_______", "___________", "_____", "_________")
            file.write(print_tag)
            i += 1
        browser()

    # блок ручного ввода
    def manual_input():
        input_data_mark = ""
        list_of_data = []
        input_data_name = str(e_manual_input_name.get())
        input_data_art = str(e_manual_input_art.get())
        input_data_num = str(e_manual_input_num.get())
        input_data_type = str(e_manual_input_type.get())
        input_data_price = str(e_manual_input_price.get())
        input_data_mat = str(e_manual_input_mat.get())
        input_data_col = str(e_manual_input_col.get())
        input_data_feat = str(e_manual_input_feat.get())
        input_data_size = str(e_manual_input_size.get()).split()
        proccesed_sizes = " ".join(sorted(input_data_size))
        if tag_size_var.get() == 1:
            input_data_mark = "Б"
        elif tag_size_var.get() == 2:
            input_data_mark = "М"
        try:
            if len(input_data_name) == 0:
                raise IndexError
            elif len(input_data_art) == 0:
                raise IndexError
            elif len(input_data_num) == 0:
                raise IndexError
            elif len(input_data_type) == 0:
                raise IndexError
            elif len(input_data_price) == 0:
                raise IndexError
            elif len(input_data_mat) == 0:
                raise IndexError
            elif len(input_data_col) == 0:
                raise IndexError
            elif len(input_data_feat) == 0:
                raise IndexError
            elif len(input_data_mark) == 0:
                raise UnboundLocalError
            elif len(input_data_size) == 0:
                raise IndexError
        except IndexError:
            messagebox.showerror("Ошибка ввода", "В одном из полей отсутствуют данные")
        except UnboundLocalError:
            messagebox.showerror("Ошибка ввода", "Выберите размер ценника")
            return
        mod_input_data = "{} {} {} {} {} {} {} {} {} {} \n".format(input_data_name, input_data_art, input_data_num,
                                                                   input_data_type, input_data_price,
                                                                   input_data_mat, input_data_col, input_data_feat,
                                                                   input_data_mark, proccesed_sizes)
        list_of_data.append(mod_input_data)  # лист для записи введенных данных с заменой пробелов на запятые
        with open(filepath_List, "a", encoding="utf-8") as FileRead:
            FileRead.write(mod_input_data)
        wb = load_workbook(temp_xlsx)
        sheet = wb.active
        new_dict = {"A": input_data_name, "B": input_data_art, "C": input_data_num,
                   "D": input_data_type, "E": input_data_price, "F": input_data_mat,
                   "G": input_data_col, "H": input_data_feat, "I": input_data_mark, "K": proccesed_sizes}
        sheet.append(new_dict)
        wb.save(temp_xlsx)
        wb.close()
        combo_box_mod()
        textBoxRefresh(filepath_List, e_list_display_box)
        e_list_display_box.see("end")

    # блок записи с автоматическим поиском и заменой строк
    def search_write_and_replace():
        write_input_num.focus_set()
        # если чек бокс = True функция меняет назначение на удаление данных из auto_list
        if chk_state.get() == True:
            file = open(auto_List_File, "w", encoding="utf-8")
            file.close()
            e_display_text_file.delete(1.0, END)
            return
        else:
            quickWriteRefreshBox(auto_List_File, e_display_text_file)
        temp_list = []
        saved_values = []
        input_name = write_input_name.get()
        input_art = write_input_art.get()
        input_num = write_input_num.get()
        input_size = write_input_size.get()
        input_name_len = len(input_name)
        input_art_len = len(input_art)
        input_num_len = len(input_num)
        input_size_len = len(input_size)
        try:
            if input_name_len == 0:
                raise IndexError
            elif input_art_len == 0:
                raise IndexError
            elif input_num_len == 0:
                raise IndexError
            elif input_size_len == 0:
                raise IndexError
        except IndexError:
            messagebox.showerror("Ошибка ввода", "В одном из полей отсутствуют данные")
            return
        with open(auto_List_File, "r", encoding="utf-8") as listFile:
            temp_list = listFile.readlines()
            count = 0
            for line in temp_list:
                split_lines = line.split()
                name = split_lines[0]
                art = split_lines[1]
                number = split_lines[2]
                if input_name in name and input_name_len == len(name) and input_art in art and input_art_len == len(
                        art) and input_num_len == len(number) and input_num in number:
                    ind = temp_list.index(line)
                    count = count + 1
        if count == 0:
            with open(auto_List_File, "a", encoding="utf-8") as listFile:
                listFile.write("{} {} {} {}\n".format(input_name, input_art, input_num, input_size))
            combo_box_mod()
            quickWriteRefreshBox(auto_List_File, e_display_text_file)
        elif count >= 1:
            file = open(auto_List_File, "r", encoding="utf-8")
            lines = file.readlines()
            file.close()
            saved_values.append(temp_list[ind].replace("\n", " "))
            saved_values.append(input_size + "\n")
            rewrite_values = "".join(saved_values)
            del lines[ind]
            with open(auto_List_File, "w+", encoding="utf-8") as newFile:
                for line in lines:
                    newFile.write(line)
                newFile.write(rewrite_values)
            quickWriteRefreshBox(auto_List_File, e_display_text_file)
            combo_box_mod()
        write_input_art.delete(0, END)
        write_input_size.delete(0, END)
        write_input_num.delete(0, END)

    def change_quick_write():
        with open(auto_List_File, "w", encoding="utf-8") as ReadFile:
            change = e_display_text_file.get(1.0, END)
            ReadFile.write(change)

    def form_list_from_auto():
        marker = ""
        if tag_size_var1.get() == 1:
            marker = "Б"
        elif tag_size_var1.get() == 2:
            marker = "М"
        try:
            if len(marker) == 0:
                raise UnboundLocalError
        except UnboundLocalError:
            messagebox.showerror("Ошибка ввода", "В одном из полей отсутствуют данные")
        temp_list = []
        with open(auto_List_File, "r", encoding="utf-8") as readFile:
            for line in readFile:
                temp_list.append(line.rsplit())
                temp_list.sort()
            for x in temp_list:
                name = x[0]
                art = x[1]
                number = x[2]
                sizes = x[3:]
                sizes1 = " ".join(sorted(sizes))
                with open(filepath_List, "a", encoding="utf-8") as sortFile:
                    name = "{} {} {} нет 0 нет нет нет {} {}\n".format(name, art, number, marker, sizes1)
                    sortFile.write(name)
                textBoxRefresh(filepath_List, e_list_display_box)

    def help_window():
        help_window_readme = Toplevel()
        help_window_readme.title("Справка")
        help_window_readme.geometry('1100x500+200+100')
        help_window_readme.iconbitmap('assets/tag_icon.ico')
        help_window_readme.resizable(False, False)
        l_label_for_help = Label(help_window_readme, text=helpText, font='Arial 10')
        l_label_for_help.place(x=10, y=10)

    '''функции трединга'''

    def cards_thread_function():
        thread = threading.Thread(target=write_from_clipboard)
        thread.start()

    def server_thread_functon():
        thread1 = threading.Thread(target=server)
        thread1.start()

    def manual_thread_function():
        thread2 = threading.Thread(target=manual_input)
        thread2.start()

    def search_and_write():
        thread3 = threading.Thread(target=search_write_and_replace)
        thread3.start()

    '''Секция размещения виджетов/кнопок интерфейса'''

    window = Tk()
    window.title("Обувной учет. Версия 1.0")
    window.geometry('1010x460+200+200')
    window.iconbitmap('assets/tag_icon.ico')
    window.resizable(False, False)

    """ фреймы """

    frame1 = Frame(window, relief="groove", borderwidth=10, width=490, height=420)
    frame1.place(x=4, y=10)

    """ меню """

    main_menu = Menu(window)
    window.config(menu=main_menu)

    file_menu = Menu(main_menu, tearoff=0)
    file_menu.add_command(label="Просмотр файла", command=cards_view)
    file_menu.add_command(label="Перезапись", command=rewrite_files)
    file_menu.add_command(label="Локальный сервер", command=server_thread_functon)

    # file_menu.add_command(label="Выход")

    help_menu = Menu(main_menu, tearoff=0)
    help_menu.add_command(label="Документация", command=help_window)

    main_menu.add_cascade(label="Меню",
                          menu=file_menu)
    main_menu.add_cascade(label="Справка",
                          menu=help_menu)

    '''файловый менеджмент'''
    icon_for_create = PhotoImage(file="assets/create_tag.png")

    b_auto_list_change = Button(frame1, text="Сохранить", cursor="hand2", command=change_quick_write)
    b_auto_list_change.place(x=1, y=380)

    b_creat_tags = Button(window, text="Создать этикетки", cursor="hand2", command=cards_format)
    b_creat_tags.place(x=500, y=400)
    b_creat_tags.config(image=icon_for_create)
    CreateToolTip(b_creat_tags, text="Создать этикетки")

    b_stop_buffer = Button(window, text="test")
    b_stop_buffer.bind()

    '''команды редактору'''
    add_button_icon = PhotoImage(file="assets/adding_line.png")
    clipboard_button_icon = PhotoImage(file="assets/clipboard_button.png")

    b_clipboard_button = Button(window, text="Буфер обмена", cursor="hand2", command=cards_thread_function)
    b_clipboard_button.place(x=600, y=400)
    b_clipboard_button.config(image=clipboard_button_icon)

    icon_for_output_tag = PhotoImage(file="assets/output_tag.png")
    b_open_browser = Button(window, text="Вывод этикеток", cursor="hand2", command=browser)
    b_open_browser.place(x=550, y=400)
    b_open_browser.config(image=icon_for_output_tag)
    CreateToolTip(b_open_browser, text="Вывод этикеток")

    b_manual_input = Button(window, text="Запись новой позиции", cursor="hand2", command=manual_thread_function)
    b_manual_input.place(x=700, y=400)
    b_manual_input.config(image=add_button_icon)

    write_in_file = Button(frame1, text="Записать", cursor="hand2", command=search_and_write)
    write_in_file.place(x=1, y=45, width=105)

    b_form_list_entry = Button(frame1, text="Сформировать", cursor="hand2", command=form_list_from_auto)
    b_form_list_entry.place(x=90, y=380, width=105)

    b_button_excell_sheet_w = Button(window, text="Экспорт в Excell", cursor="hand2", command=0)
    # b_button_excell_sheet_w.place(x=720, y=400, width=105)

    # радио кнопки выбора размера ценников
    tag_size_var = IntVar()
    r_tag_button1 = Radiobutton(window, text="Б", variable=tag_size_var, value=1)
    r_tag_button2 = Radiobutton(window, text="М", variable=tag_size_var, value=2)
    r_tag_button1.place(x=930, y=20)
    r_tag_button2.place(x=960, y=20)

    tag_size_var1 = IntVar()
    r_tag_button3 = Radiobutton(window, text="Б", variable=tag_size_var1, value=1)
    r_tag_button4 = Radiobutton(window, text="М", variable=tag_size_var1, value=2)
    r_tag_button3.place(x=390, y=65)
    r_tag_button4.place(x=430, y=65)

    # чек кнопка выбора действия стереть/записать
    chk_state = IntVar()
    chk_state.set(-1)
    check = Checkbutton(frame1, text="Начать запись заново", variable=chk_state, onvalue=1, offvalue=0,
                        command=button_swap)
    check.place(x=1, y=90)

    '''ввод'''

    # функция привязки клавиши Enter к вводу новых строк в список
    def focus():
        if len(e_manual_input_size.get()) > 0:
            manual_thread_function()
        else:
            pass

    keyboard.add_hotkey("Enter", focus)

    # секция кнопок ручного ввода
    icon = PhotoImage(file="assets/output-onlinepngtools.png")
    edit_button_icon = PhotoImage(file="assets/edit_button.png")
    empty_button_icon = PhotoImage(file="assets/empty_tag.png")

    # кнопка ввода наименования
    e_manual_input_name = Entry(window, width=15)
    b_button_for_name = Button(window, command=lambda: e_manual_input_name.delete(0, END))
    keyboard.add_hotkey("ctrl+1", lambda: e_manual_input_name.delete(0, END))
    keyboard.add_hotkey("F1", lambda: e_manual_input_name.focus_set())
    b_button_for_name.place(x=610, y=20)
    b_button_for_name.config(image=icon)
    label_name1 = Label(window, text="1.Наименование")
    label_name1.place(x=495, y=1)

    # кнопка ввода артикула
    e_manual_input_art = Entry(window, width=15)
    b_button_for_art = Button(window, command=lambda: e_manual_input_art.delete(0, END))
    keyboard.add_hotkey("ctrl+2", lambda: e_manual_input_art.delete(0, END))
    keyboard.add_hotkey("F2", lambda: e_manual_input_art.focus_set())
    b_button_for_art.place(x=610, y=65)
    b_button_for_art.config(image=icon)
    label_name2 = Label(window, text="2.Арт.")
    label_name2.place(x=495, y=45)

    # кнопка ввода номера
    e_manual_input_num = Entry(window, width=15)
    b_button_for_num = Button(window, command=lambda: e_manual_input_num.delete(0, END))
    keyboard.add_hotkey("ctrl+3", lambda: e_manual_input_num.delete(0, END))
    keyboard.add_hotkey("F3", lambda: e_manual_input_num.focus_set())
    b_button_for_num.place(x=610, y=110)
    b_button_for_num.config(image=icon)
    label_name3 = Label(window, text="3.Номер", font="Arial 9")
    label_name3.place(x=495, y=90)

    # кнопка ввода типа модели
    e_manual_input_type = Entry(window, width=15)
    b_button_for_type = Button(window, command=lambda: e_manual_input_type.delete(0, END))
    keyboard.add_hotkey("ctrl+4", lambda: e_manual_input_type.delete(0, END))
    keyboard.add_hotkey("F4", lambda: e_manual_input_type.focus_set())
    b_button_for_type.place(x=750, y=20)
    b_button_for_type.config(image=icon)
    label_name4 = Label(window, text="4.Тип")
    label_name4.place(x=635, y=1)

    # кнопка ввода цены
    e_manual_input_price = Entry(window, width=15)
    b_button_for_price = Button(window, command=lambda: e_manual_input_price.delete(0, END))
    keyboard.add_hotkey("ctrl+5", lambda: e_manual_input_price.delete(0, END))
    keyboard.add_hotkey("F5", lambda: e_manual_input_price.focus_set())
    b_button_for_price.place(x=750, y=65)
    b_button_for_price.config(image=icon)
    label_name5 = Label(window, text="5.Цена")
    label_name5.place(x=635, y=45)

    # кнопка ввода материала иделия
    e_manual_input_mat = Entry(window, width=15)
    b_button_for_mat = Button(window, command=lambda: e_manual_input_mat.delete(0, END))
    keyboard.add_hotkey("ctrl+6", lambda: e_manual_input_mat.delete(0, END))
    keyboard.add_hotkey("F6", lambda: e_manual_input_mat.focus_set())
    b_button_for_mat.place(x=750, y=110)
    b_button_for_mat.config(image=icon)
    label_name6 = Label(window, text="6.Материал")
    label_name6.place(x=635, y=90)

    # кнопка ввода цвета изделия
    e_manual_input_col = Entry(window, width=15)
    b_button_for_col = Button(window, command=lambda: e_manual_input_col.delete(0, END))
    keyboard.add_hotkey("ctrl+7", lambda: e_manual_input_col.delete(0, END))
    keyboard.add_hotkey("F7", lambda: e_manual_input_col.focus_set())
    b_button_for_col.place(x=900, y=20)
    b_button_for_col.config(image=icon)
    label_name7 = Label(window, text="7.Цвет")
    label_name7.place(x=785, y=1)

    # кнопка ввода отличительных свойств изделия
    e_manual_input_feat = Entry(window, width=25)
    b_button_for_feat = Button(window, command=lambda: e_manual_input_feat.delete(0, END))
    keyboard.add_hotkey("ctrl+8", lambda: e_manual_input_feat.delete(0, END))
    keyboard.add_hotkey("F8", lambda: e_manual_input_feat.focus_set())
    b_button_for_feat.place(x=960, y=65)
    b_button_for_feat.config(image=icon)
    label_name8 = Label(window, text="8.Признаки")
    label_name8.place(x=785, y=45)

    # кнопка ввода размеров
    e_manual_input_size = Entry(window, width=25)
    b_button_for_size = Button(window, command=lambda: e_manual_input_size.delete(0, END))
    keyboard.add_hotkey("ctrl+9", lambda: e_manual_input_size.delete(0, END))
    keyboard.add_hotkey("F9", lambda: e_manual_input_size.focus_set())
    b_button_for_size.place(x=960, y=110)
    b_button_for_size.config(image=icon)
    label_name9 = Label(window, text="9.Размеры")
    label_name9.place(x=785, y=90)

    # кнопка для активации функции пустых ценников
    b_button_for_empty = Button(window, text="Пустые ценники", command=empty_tags)
    b_button_for_empty.place(x=650, y=400)
    b_button_for_empty.config(image=empty_button_icon)

    # блок вызова класса подписей элементов ToolTip
    e_manual_input_name.place(x=510, y=20)
    CreateToolTip(e_manual_input_name, text="Наименование")
    e_manual_input_art.place(x=510, y=65)
    CreateToolTip(e_manual_input_art, text="Артикул")
    e_manual_input_num.place(x=510, y=110)
    CreateToolTip(e_manual_input_num, text="Номер")
    e_manual_input_type.place(x=650, y=20)
    CreateToolTip(e_manual_input_type, text="Тип")
    e_manual_input_price.place(x=650, y=65)
    CreateToolTip(e_manual_input_price, text="Цена")
    e_manual_input_mat.place(x=650, y=110)
    CreateToolTip(e_manual_input_mat, text="Материал")
    e_manual_input_col.place(x=800, y=20)
    CreateToolTip(e_manual_input_col, text="Цвет")
    e_manual_input_feat.place(x=800, y=65)
    CreateToolTip(e_manual_input_feat, text="Признак")
    CreateToolTip(r_tag_button1, text="Размер ценника")
    CreateToolTip(r_tag_button2, text="Размер ценника")
    e_manual_input_size.place(x=800, y=110)
    CreateToolTip(e_manual_input_size, text="Размеры")

    """секция для ввода автопоиска"""
    write_input_num = Entry(frame1, width=15)
    write_input_num.place(x=110, y=70)
    b_button_for_num = Button(frame1, command=lambda: write_input_num.delete(0, END))
    b_button_for_num.place(x=210, y=69)
    b_button_for_num.config(image=icon)
    CreateToolTip(write_input_num, text="Номер")

    write_input_size = Entry(frame1, width=15)
    write_input_size.place(x=240, y=70)
    b_button_for_size = Button(frame1, command=lambda: write_input_size.delete(0, END))
    b_button_for_size.place(x=340, y=69)
    b_button_for_size.config(image=icon)
    CreateToolTip(write_input_size, text="Один размер")

    write_input_art = Entry(frame1, width=15)
    write_input_art.place(x=240, y=47)
    b_button_for_size = Button(frame1, command=lambda: write_input_art.delete(0, END))
    b_button_for_size.place(x=340, y=46)
    b_button_for_size.config(image=icon)
    CreateToolTip(write_input_art, text="Артикул")

    write_input_name = Entry(frame1, width=15)
    write_input_name.place(x=110, y=47)
    b_button_for_size = Button(frame1, command=lambda: write_input_name.delete(0, END))
    b_button_for_size.place(x=210, y=46)
    b_button_for_size.config(image=icon)
    CreateToolTip(write_input_name, text="Наименование")

    # окошко вывода авто поиска
    e_display_text_file = Text(frame1, width=66, wrap=WORD, font='Arial 10', height=15)
    e_display_text_file.place(x=1, y=120)

    # функция выполняет поиск по вводу из write_input_num и вставляет данные в write_input_art
    # если ввод из write_input_num уже есть
    def insert_text_widget(e):
        with open(auto_List_File, "r", encoding="utf-8") as listFile:
            data = write_input_num.get()
            temp_list = listFile.readlines()
            for item in temp_list:
                data_to_input = item.split()
                if data in data_to_input[2]:
                    if len(data) == len(data_to_input[2]) and data in item:
                        print(data, data_to_input[2])
                        write_input_art.insert(1, data_to_input[1])
                        write_input_size.focus_set()
                    else:
                        write_input_art.focus_set()
                    break
                elif data not in data_to_input[2]:
                    write_input_art.focus_set()

    write_input_num.bind("<Return>", insert_text_widget)

    c_combo_for_list = Combobox(window, width=77)
    c_combo_for_list.place(x=500, y=170)

    def combo_box_mod():
        with open(filepath_List, "r", encoding="utf-8") as fileRead:
            price_tag_quantity_count = 0
            list_file = fileRead.readlines()
            temp_list = []
            for x in list_file:
                price_tag_quantity_count += 1
                temp_list.append(x)
                c_combo_for_list['values'] = temp_list
        return price_tag_quantity_count

    combo_box_mod()

    price_tag_quantity_count = combo_box_mod()
    l_label_for_display_quont = Label(window, font="Arial 10", text="№: {}".format(price_tag_quantity_count))
    l_label_for_display_quont.place(x=889, y=140)

    def list_modifier():
        count = 0
        with open(filepath_List, encoding='utf-8') as listForMod:
            string_list = listForMod.readlines()
            string_get = c_combo_for_list.get()
            for line in string_list:
                if string_get == line:
                    ind = string_list.index(line)
                    temp_container = string_list[ind]
                    count = count = + 1
                    print(temp_container)

            def destroy_w(event):
                modifier_window.destroy()

            modifier_window = Toplevel()
            modifier_window.title("Редактор")
            modifier_window.geometry("600x90+200+100")
            modifier_window.iconbitmap('assets/tag_icon.ico')
            modifier_window.resizable(False, False)
            frame_1 = Frame(modifier_window, relief="groove", borderwidth=10, width=80, height=90)
            frame_1.place(x=4, y=10)
            modifier_window.bind("<Escape>", destroy_w)
            try:
                e_for_modification = Text(frame_1, font="Arial 10", width=80, height=2)
                e_for_modification.pack()
                e_for_modification.insert(0.0, temp_container.strip())
            except UnboundLocalError:
                modifier_window.destroy()
                messagebox.showerror("Ошибка", "Данные в строке выбор отсутствуют в списке или были изменены")
        if count == 1:
            def inside_func():

                b_test_button = Button(modifier_window, text="Изменение", command=inside_func)
                b_test_button.place(x=400, y=60)
                new_line = e_for_modification.get(1.0, END)
                modified_list = open(filepath_List, "w", encoding='utf-8')
                string_list[ind] = new_line
                new_file_contents = "".join(string_list)
                modified_list.write(new_file_contents)
                modified_list.close()

                textBoxRefresh(filepath_List, e_list_display_box)
                combo_box_mod()

            inside_func()

        else:
            pass

    b_test_button = Button(window, text="Фиксация", command=list_modifier)
    b_test_button.place(x=750, y=400)
    b_test_button.config(image=edit_button_icon)

    e_list_display_box = Text(window, width=70, wrap=WORD, font='Arial 10', height=12)
    e_list_display_box.place(x=500, y=200)

    scroll = Scrollbar(command=e_list_display_box.yview)
    scroll.place(x=990, y=200, height=200)
    e_list_display_box.config(yscrollcommand=scroll.set)

    # функция читает list и обновляет текст бокс
    quickWriteRefreshBox(auto_List_File, e_display_text_file)
    textBoxRefresh(filepath_List, e_list_display_box)

    def instance_make_change():
        makeChangeInLits(filepath_List, e_list_display_box)

    b_refresh_text_box = Button(window, text="Сохранить", cursor="hand2", command=instance_make_change)
    b_refresh_text_box.place(x=920, y=400)
    '''labels'''

    l_label_for_manual_mode = Label(frame1, font="Arial 9", text="Система для несортированных предметов")
    l_label_for_manual_mode.place(x=100, y=2)

    # --standalone --mingw64 --windows-disable-console --windows-icon-from-ico=tag_icon.ico --plugin-enable=tk-inter

    """def csvExport():
        temp_list = []
        with open(filepathList, "r", encoding="utf-8") as readFile:
            for line in readFile:
                temp_list.append(line.rsplit())
                filtered_list = list(filter(None, temp_list))
            for x in filtered_list:
                art = x[1]; name = x[0]; number = x[2]; type = x[3]; price = x[4];
                material = x[5]; features = x[6]; collor = x[7]; marker = x[8]; sizes = x[9:]
                sizes = " ".join(sizes)
                with open(CSVFilePath, "a", encoding="utf-8") as toWrite:
                    writer = csv.writer(toWrite)
                    writer.writerow([name, art, number, type, price, material, collor, features, marker, sizes])
    """

    window.mainloop()


main()

# --standalone --onefile --mingw64 --windows-disable-console --windows-icon-from-ico=assets\tag_icon.ico --plugin-enable=tk-inter --include-data-dir=C:\Users\wda61\Dropbox\Python_projects\Pricetag\assets=assets
