# vocabulary_test_project
import random
import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import ttk
import win32api
import keyboard

# Это программа выполняет функцию языкового квиза. скрипт основывается на txt документе содержащем словарные позиции
# данный скрипт можно приспособить для вывода простых вопросов таким образом обращая его в вопрос-ответный квиз

# messagebox.showinfo("Good day pumpkin!", "First choose text file, then pick words range and hit Activate!")


def on_exit():
	print("exit")
	next_button_pressed.set("next button pressed")
	button_pressed.set("button pressed")
	window.destroy()


def main_window():
	window = Tk()
	window.title("Vocabulary quiz")
	window.geometry("800x350+400+200")
	window.config(bg='gray97')
	window.protocol('WM_DELETE_WINDOW', on_exit)
	return window


window = main_window()


s = ttk.Style()
s.theme_use("clam")
collor = "gray97"


english_words_quiz_path = os.path.join(os.getcwd(), 'assets/english_words.txt')
finnish_words_quiz_path = os.path.join(os.getcwd(), 'assets/finish_words.txt')           
deutch_words_quiz_path = os.path.join(os.getcwd(), 'assets/deutch_words.txt')           
configuration_file = os.path.join(os.getcwd(), "assets/configurate.txt")

with open(configuration_file, "w", encoding="utf - 8") as configure:
	write = configure.write("data_set_name: ")


data_base_list = ["English", "Finnish", "Deutch"]


def configurate():
	if cData_Base_choose.get() == "English":
		path = english_words_quiz_path
	elif cData_Base_choose.get() == "Finnish":
		path = finnish_words_quiz_path
	elif cData_Base_choose.get() == "Deutch":
		path = deutch_words_quiz_path
	
	with open(configuration_file, "w", encoding="utf - 8") as configure:
		try:
			configure.write("data_set_name: %s" % path)
		except UnboundLocalError:
			messagebox.showerror("There is an error :(", "Choose vocabulary set first pumpkin :)")

	with open(path, "r", encoding="utf - 8") as dictionary:
		read = dictionary.readlines()
		llable_for_quontity.configure(text="Amount of words in database: %s" % len(read))
		lst = [x for x in range(len(read)+2)]
		cWords_quontity_start["values"] = lst[0:-1:1]
		cWords_quontity_stop["values"] = lst[0:-1:1]
	b_Button_for_start_the_quiz.configure(state=ACTIVE)
	cWords_quontity_stop.configure(state=ACTIVE)
	cWords_quontity_start.configure(state=ACTIVE)
	interface_flush()
	return path


def interface_flush():
	llabel_for_annouce.configure(text="")
	lLabel_for_question.configure(text="")
	bButton_for_next.configure(text="Start")
	lLabel_for_question.configure(background="")
	eEntry_answer.delete(0, END)
	lLabel_for_indicate_start.configure(text="")
	

def sorting():
	# lLable_for_indicate_start.configure(text="")
	interface_flush()
	with open(configuration_file, "r", encoding="utf - 8") as configure:
		read = configure.readline()
		# Переменная path хранит путь до файла. До 14 индекса указана категория.
		path = read[14:].strip()
	lst_of_raw_strings = []
	output_clean_words = []
	sourse_clean_words = []
	# метод with open открывает документ для чтения базы слов, образования списков и замера количества слов в документе
	with open(path, "r", encoding="utf - 8") as dictionary:
		read = dictionary.readlines()
		
		# этот блок отвечает за ввод значений начала и конца списка
		try:
			start_count = int(cWords_quontity_start.get())
			stop_count = int(cWords_quontity_stop.get())
		except ValueError:
			messagebox.showerror("There is an error :(", "Choose words range first honey bunny :)")

		# loop очищает строки от новой строки, знака тире, и пробелов во второй части под-листа
		for line in read[start_count:stop_count]:
			striped_line = line.strip('\n')
			lst_of_raw_strings.append(striped_line.split("@"))
			# метод random.shuffle() перемешивает лист для рандомизации выдачи слов для квиза
			random.shuffle(lst_of_raw_strings)
		for string2 in lst_of_raw_strings:
			output_clean_words.append(string2[1].strip())
		for string1 in lst_of_raw_strings:
			sourse_clean_words.append(string1[0].strip())

	words_count = len(lst_of_raw_strings)

	two_component_list = [list(a) for a in zip(sourse_clean_words, output_clean_words)]
	if len(read[start_count:stop_count]) == 0:
		messagebox.showerror("Input error", "Start or stop numbers are bigger or smaller than requared honey :)")
		return
	# print("Words in this exercise: %s\n" %len(read[start_count:stop_count]))
	return two_component_list, sourse_clean_words, output_clean_words, words_count


def start_quiz():
	score = 0
	call = sorting()
	for i in call[0]:
		
		lLabel_for_indicate_start.configure(text="Press \"Start\" to begin")
		key_board_layout = int(win32api.GetKeyboardLayoutName())
		# метод рандом при каждой итерации генерирует произвольное число между 0 и 1
		random_number = random.randint(0, 1)

		# логический блок для направления перевода иностранный - русский
		eEntry_answer.delete(0, END)
		bButton_for_next.wait_variable(next_button_pressed)
		eEntry_answer.focus_set()
		bButton_for_next.configure(text="Next word")
		if random_number == 0:
			if key_board_layout == 409:  # english
				keyboard.press_and_release("alt+shift")
			else:
				pass
			lLabel_for_question.configure(background="")

			llabel_for_annouce.configure(text="")
			lLabel_for_question.configure(text="%s" % i[0].capitalize())
			fined_index = call[0].index(i)
			lLabel_for_indicate_start.configure(text="{} out of {}".format(fined_index + 1, call[3]))

			bButton_for_answer.wait_variable(button_pressed)
			
			if eEntry_answer.get().lower() in call[2][fined_index] and len(eEntry_answer.get()) > 1:
				lLabel_for_question.configure(background="green")
				llabel_for_annouce.configure(text="This is the right answer!\nGood job honey!")
				score += 1
			else:
				text = "Sorry sweet pie,""but it is false.""\nRight answer is: {}""\n""But your answer is {}"
				llabel_for_annouce.configure(text=text.format(call[2][fined_index], eEntry_answer.get()))
				lLabel_for_question.configure(background="red")

		# логический блок для направления перевода русский - иностранный
		elif random_number == 1:
			if key_board_layout == 419:  # russia
				keyboard.press_and_release("alt+shift")
			else:
				pass
			lLabel_for_question.configure(background="")

			lLabel_for_question.configure(text="%s" % i[1].capitalize())
			fined_index = call[0].index(i)
			lLabel_for_indicate_start.configure(text="{} out of {}".format(fined_index + 1, call[3]))
			bButton_for_answer.wait_variable(button_pressed)

			if eEntry_answer.get() in call[1][fined_index] and len(eEntry_answer.get()) > 1:
				llabel_for_annouce.configure(text="This is the right answer!\nGood job honey!")
				lLabel_for_question.configure(background="green")
				score += 1
			else:
				text = "Sorry sweet pie, but it is false.\nRight answer is: {}\nBut your answer is {}"
				llabel_for_annouce.configure(text=text.format(call[1][fined_index], eEntry_answer.get()))
				lLabel_for_question.configure(background="red")

	if score == call[3]:
		messagebox.showinfo("Result", "Result: {} out of {}! Great job my sweet pie!\n".format(score, call[3]))
	elif call[3] > score:
		messagebox.showinfo("Result", "Result: {} out of {}! Dont you worry my sweet pie, you will succeed just keep trying!\n".format(score, call[3]))
	elif call[3] - score == 1:
		messagebox.showinfo("Result", "Result: {} out of {}! Almost got it sweet pie! Keep on gooing!\n".format(score, call[3]))
	# lLable_for_indicate_start.configure(text="")

	interface_flush()


def open_a_words_file():
	path = configurate()
	os.popen(path)


def help_func():
	help_window = Toplevel()
	help_window.title("Справка")
	label = Label(help_window, text=help_text, font="Arial 10")
	label.pack()


main_menu = Menu(window)
window.config(menu=main_menu)

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label="Просмотр файла", command=open_a_words_file)
file_menu.add_command(label="Справка", command=help_func)
# file_menu.add_command(label="Выход")

help_menu = Menu(main_menu, tearoff=0)
help_menu.add_command(label="")

main_menu.add_cascade(label="Меню", menu=file_menu)


frame2 = Frame(window, width=300, height=400, relief="groove", borderwidth=10)
frame2.pack(side=LEFT, padx=50)

frame1 = Frame(window, width=500, height=600, relief="groove", borderwidth=10)
frame1.pack(side=RIGHT, padx=50, pady=10)


"""//////////Frame 1///////////"""


lLabel_for_indicate_start = Label(frame1, text="", font="Arial 10")
lLabel_for_indicate_start.pack(pady=5)

lLabel_for_question = Label(frame1, font="Arial 15")
lLabel_for_question.pack(side=TOP, padx=20)

llabel_for_annouce = Label(frame1, font="Arial 10")
llabel_for_annouce.pack(pady=7)

eEntry_answer = Entry(frame1, width=35)
eEntry_answer.pack(pady=30, padx=40)


button_pressed = StringVar()
bButton_for_answer = Button(frame1, text="Answer", command=lambda: button_pressed.set("button pressed"))
bButton_for_answer.pack(side=LEFT, padx=25, pady=20)


def enter_answer():
	button_pressed.set("button pressed")


def next_question():
	next_button_pressed.set("next button pressed")


window.bind("<Return>", lambda event: enter_answer())
window.bind("<Shift-Return>", lambda event: next_question())

next_button_pressed = StringVar()
bButton_for_next = Button(frame1, text="Start!", command=lambda: next_button_pressed.set("next button pressed"))
bButton_for_next.pack(side=RIGHT, padx=25, pady=20)


"""//////////Frame 2///////////"""


# комбобокс для выбора языкового пакета
cData_Base_choose = Combobox(frame2)
cData_Base_choose.current()
cData_Base_choose.pack(pady=5)
cData_Base_choose["values"] = data_base_list


llable_for_quontity = Label(frame2, text="", font="Arial 10")
llable_for_quontity.pack(pady=5)

bButton_for_choose_options = Button(frame2, text="Enable words set", command=configurate)
bButton_for_choose_options.pack(pady=5)


frame_in_frame2 = Frame(frame2)
frame_in_frame2.pack()

lLable_for_from_to = Label(frame_in_frame2, text="From       :       to")
lLable_for_from_to.pack()

cWords_quontity_start = Combobox(frame_in_frame2, width=3, state=DISABLED)
cWords_quontity_start.current()
cWords_quontity_start.pack(side=LEFT, padx=10, pady=8)


cWords_quontity_stop = Combobox(frame_in_frame2, width=3, state=DISABLED)
cWords_quontity_stop.current()
cWords_quontity_stop.pack(side=RIGHT, padx=10, pady=8)


b_Button_for_start_the_quiz = Button(frame2, text="Activate vocab set", width=30, state=DISABLED, command=start_quiz)
b_Button_for_start_the_quiz.pack(side=BOTTOM, pady=20)


help_text = """Справочное окно
Для того чтобы начать наш квиз сперва нужно выбрать языковую базу из предложенных.
Затем, выбрать диапазон слов которые вы хотите учить
После выбора диапазона нужно нажать "Activate vocab set" 
В левой стороне окна появится "Press Start to begin"
После чего жмите старт и квиз начался!
Ввод слова можно осуществлять кнопкой Enter 
Переход к следующему слову производится сочетанием клавиш Shif+Enter
"""


window.mainloop()


# --standalone --mingw64 --windows-disable-console --windows-icon-from-ico=quiz_icon.ico --plugin-enable=tk-inter
