import random
import time
import os
import pyperclip
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from shutil import copyfile
import getpass

window = Tk()
window.title("Генератор паролей. Версия 1.0")
window.geometry('510x400+500+300')
window.iconbitmap('ico.ico')
window.resizable(False, False)

filepath = os.path.join(os.getcwd(), 'password.pas')
#file_path_copy = os.path.join(os.getcwd(), 'password(copy).pas')

try:
	f = open(filepath, "r", encoding="utf-8")
except FileNotFoundError:
	f = open(filepath, "w", encoding="utf-8")
	f.close()
else:
	None

try:
	os.mkdir("C:\\Users\\vika8\\AppData\\Roaming\\Get_pass")
except FileExistsError:
	None

class ToolTip(object):

	def __init__(self, widget):
		self.widget = widget
		self.tipwindow = None
		self.id = None
		self.x = self.y = 0

	def showtip(self, text):
		self.text = text
		if self.tipwindow or not self.text:
			return
		x, y, cx, cy = self.widget.bbox("insert")
		x = x + self.widget.winfo_rootx() + 57
		y = y + cy + self.widget.winfo_rooty() +10
		self.tipwindow = tw = Toplevel(self.widget)
		tw.wm_overrideredirect(1)
		tw.wm_geometry("+%d+%d" % (x, y))
		label = Label(tw, text=self.text, justify=LEFT,
					  background="#ffffe0", relief=SOLID, borderwidth=1,
					  font=("tahoma", "8", "normal"))
		label.pack(ipadx=1)

	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()

def CreateToolTip(widget, text):
	toolTip = ToolTip(widget)
	def enter(event):
		toolTip.showtip(text)
	def leave(event):
		toolTip.hidetip()
	widget.bind('<Enter>', enter)
	widget.bind('<Leave>', leave)

icon = PhotoImage(file="button_resize.png")


eDisplayTextFile = Text(window, width=70, wrap=WORD, font='Arial 10', height=10)
eDisplayTextFile.place(x=1, y=200)

scroll = Scrollbar( command=eDisplayTextFile.yview)
scroll.place(x = 490, y = 200, height = 165)
eDisplayTextFile.config(yscrollcommand=scroll.set)

eEntryLogin = Entry(window)
eEntryLogin.place(x=290, y=11, width=80)
CreateToolTip(eEntryLogin, text="Поле для логина (без пробелов)")

comboSymbolsQuont = Combobox(window)
comboSymbolsQuont['values'] = (4,5,6,7,8,9,10,11,12,14,16,18,20)
comboSymbolsQuont.current(8)
comboSymbolsQuont.place(x=240, y=11, width=40)
CreateToolTip(comboSymbolsQuont, text="Желаемое количество символов\n"
										"(Рекомендуется не менee 12)")

frame1 = Frame(window, relief="groove", borderwidth=10, width=500, height=35)
frame1.pack(padx=30, pady=150)
lLabelForSearched = Label(frame1, text="Ищите пароль? Наберите название сервиса в поиске и он будет в буфере!", font="Arial 9")
lLabelForSearched.pack()


def main():
    
	

	def randomEngine():	
		timeAddition = time.localtime() #добавление временной метки
		timeString = time.strftime("%m/%d/%Y, %H:%M:%S", timeAddition)
		listNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
		listLiteral = ["a", "b","c", "d", "e", "f", "g", "h", "i", "j", "k", 
						"l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z"]
		listOfCapitals = ["A", "B","C", "D", "E", "F", "G", "H", "I", "J", "K",
							"L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W",
							"X", "Y", "Z"]
		listSymbols = ["?", "@", "&", "!", "%", "#", "*", "$", "№", "<", ">", "(", ")", "-", "+", "="]
		listOfPasswords = []
		try:
			userInput = str(eEntryServiceName.get()).capitalize()
			loginInput = str(eEntryLogin.get())
			if userInput == "" or loginInput == "":
				raise KeyError
		except KeyError:
			messagebox.showerror("Ошибка ввода", "Введите название сервиса и логин")
			return
		n = int(comboSymbolsQuont.get())
		result = ""
		for x in range(n): #генерация рандомного пароля
			x = random.choice(listNumbers)
			y = random.choice(listLiteral)
			z = random.choice(listOfCapitals)
			a = random.choice(listSymbols)
			result += str(x) + str(y) + str(z) + str(a)
		listOfPasswords = "{} | {} | {} | {}\n".format(userInput, result[:n], loginInput, timeString)
		pyperclip.copy(result[:n]) #метод копирования текста в буфер обмена
		spam = pyperclip.paste
		def writeInFile():
			count = 0
			with open (filepath, encoding='utf-8') as passwordFile:		
				stringList = passwordFile.readlines()
				for line in stringList:
					if userInput in line:
						count += 1
						ind = stringList.index(line) #хранит индекс элемента строки выбранного пользователем
			if count == 1:
				def insideFunc():#функция заменяет требуемую строку на новую
					#открытие текстового файла
					passwordFile = open(filepath,"w", encoding='utf-8')
					#привязка индекса к новой строке
					stringList[ind] = listOfPasswords
					#включение новой строки в лист с остальными записями
					newFileContents = "".join(stringList)
					passwordFile.write(newFileContents)
					passwordFile.close()
					refreshBox()
				insideFunc()
			else:
				def writeOneFile():
					with open(filepath, "a", encoding="utf-8") as passwordFile: 
						newFile = "".join(listOfPasswords)
						for line in newFile:
							passwordFile.write(line)
					refreshBox()
				writeOneFile()
		writeInFile()
		main()
	bButtonPassGeneration = Button(window, text="Генерация", cursor="hand2", command=randomEngine)
	bButtonPassGeneration.place(x=1, y=10, width=105)
	

	cPassList = Combobox(window)
	cPassList.current()
	cPassList.place(x=150, y=40)
	CreateToolTip(cPassList, text="Поле для поиска/удаления")

	eEntryServiceName = Combobox(window)
	eEntryServiceName.current()
	eEntryServiceName.place(x=150, y=11, width=86)
	CreateToolTip(eEntryServiceName, text="Поле для ввода названия сервиса (без пробелов)")

	
	serviceList = []
	with open(filepath, 'r', encoding="utf-8") as passwordFile:
			tempList = []
			for x in passwordFile:
				tempList.append(x.split())
			for y in tempList:
				password = y[0]
				serviceList.append(password)
				serviceList.sort()
				eEntryServiceName['values'] = (serviceList)
				cPassList['values'] = (serviceList)
	
	
	def searchThrough():
		tempList = []
		try:
			userInput1 = cPassList.get().capitalize()
			if userInput1 == "":
				raise KeyError
		except KeyError:
			messagebox.showerror("Ошибка ввода", "Введите название сервиса")
			return
		with open (filepath, "r", encoding="utf-8") as searchFile:
			for line in searchFile:
				if userInput1 in line:
					tempList.append(line.split())
				for x in tempList:
					lLabelForSearched.configure(text= "Пароль: ({}) для Логина: ({})".format(x[2], x[4]))
					pyperclip.copy(x[2])
					spam = pyperclip.paste
	bButtonSearch = Button(window, text="Поиск", cursor="hand2", command=searchThrough)
	bButtonSearch.place(x=1, y=40, width=105)
	def deleteOneLine():
		warning = messagebox.askyesno(title="Предупреждение", message="Это действие удалит выбранный пароль. Продолжать?")
		if warning:
			userInputDel = cPassList.get().capitalize()
			with open (filepath, "r", encoding="utf-8") as passwordFile:		
				stringList = passwordFile.readlines()
				for line in stringList:
					if userInputDel in line:
						ind = stringList.index(line)
			passwordFile = open(filepath, "r", encoding="utf-8")
			lines = passwordFile.readlines()
			passwordFile.close()
			del lines[ind]
			newPasswordFile = open(filepath, "w+", encoding="utf-8")
			for line in lines:
				newPasswordFile.write(line)
			newPasswordFile.close()
			lLabelForSearched.configure(text="Ищите пароль? Наберите название сервиса в поиске и он будет в буфере!")
			refreshBox()
			main()
	bButtonForDelete = Button(window, text="Удалить", cursor="hand2", command=deleteOneLine)
	bButtonForDelete.place(x=1, y=70, width=105)

	def truncateFile():
		warning = messagebox.askyesno(title="Предупреждение", message="Это действие удалит все пароли. Продолжать?")
		if warning:
			file = open(filepath, "r+", encoding="utf-8")
			file.truncate(0)
			file.close()
			refreshBox()
			main()
	bButtonForCompliteDel = Button(window, text="Удалить ВСЕ", cursor="hand2", command=truncateFile)
	bButtonForCompliteDel.place(x=1, y=370)

	def helpWindow():
		helpWindow = Toplevel()
		helpWindow.geometry("500x400+550+300")
		helpWindow.title("Справка")
		helpWindow.iconbitmap("ico.ico")
		helpWindow.resizable(False, False)
		lLabelForHelp = Label(helpWindow, font='Arial 10', text=helpText)
		lLabelForHelp.pack()
	bHelp = Button(window, cursor="hand2", command=helpWindow)
	bHelp.place(x=460, y=10)
	bHelp.config(image=icon)


def refreshBox():
	with open(filepath, "r", encoding="utf-8") as Fileread:
		eDisplayTextFile.delete(1.0, END)
		try:
			for line in Fileread:
				eDisplayTextFile.insert(1.0, line)
		except Exception:
			None
refreshBox()

#дополнительная копия метода отображает время изменения при запуске
try:
	fileStatsObj = os.stat("C:\\Users\\vika8\\AppData\\Roaming\\password(copy).pas").st_mtime
	modificationTime = time.ctime(fileStatsObj) 
except Exception:
	None

#функция создает бекап файла с паролями и считывает время последней его модификации 
try:
	def backing_up():
		name = getpass.getuser()
		print(name)
		warning = messagebox.askyesno("Предупреждение", "Это действие создаст копию текущих паролей"
							" и тем самым перезапишет актуальную копию. Продолжать?")
		if warning:
			copyfile(filepath, "C:\\Users\\%s\\AppData\\Roaming\\Get_pass\\password(copy).pas" %name)
			#метод смотрит время последней модификации и возвращает его в секундах
			fileStatsObj = os.stat("C:\\Users\\%s\\AppData\\Roaming\\Get_pass\\password(copy).pas" %name).st_mtime
			#метод переводит секунды в читаемый формат времени
			modificationTime = time.ctime(fileStatsObj)
			lLableForModTime.configure( text = "Последний бекап был: " +  str(modificationTime))
except Exception:
	None

bButtonForBackUp = Button(window, text = "Бэкап", width=15, command=backing_up)
bButtonForBackUp.place(x = 410, y = 70)

lLableForModTime = Label(window, text=" ", font= "arial 8")
lLableForModTime.place(x = 250, y = 130)
try:
	lLableForModTime.configure( text = "Последний бекап был: " +  str(modificationTime))
except Exception:
	None


def restore_from_backup():
	name = getpass.getuser()
	print(name)
	try:
		warning = messagebox.askyesno("Предупреждение", "Это действие восстановит список паролей из последнего бекапа"
							" и тем самым перезапишет действующую базу. Продолжать?")
		if warning:
			copyfile("C:\\Users\\%s\\AppData\\Roaming\\Get_pass\\password(copy).pas" %name, filepath)
			refreshBox()
	except Exception:
		None

bButtonForRestore = Button(window, text = "Восcтановить", width= 15, command=restore_from_backup)
bButtonForRestore.place(x = 410, y = 100)


helpText = """Для генерации нового пароля:\nВведите название сервиса и логина в соответствующих полях
После генерации, новый пароль автоматически\nкопируется в буфер обмена.\n
Для обновления пароля: повторно введите название сервиса и логин.
И сгенерируйте новый пароль.
(при необходимости ввести новый логин)\n
Для поиска пароля: введите соответствующий сервис в строке поиска.
После чего пароль будет скопирован в буфер обмена.\n
Для удаления ненужного пароля:
Выберите/Введите название сервиса в поиске и нажмите \"Удалить\"
Для удаление всех существующих паролей, нажмите \"Удалить ВСЕ\"\n
Кнопка \"Бэкап\" создает копию актуальной базы паролей и
хранит ее в рабочей директории
Кнопка \"Восстановить\" замещает актуальную (или удаленную)
базу данных ранее сохраненной"""


main()




window.mainloop()	