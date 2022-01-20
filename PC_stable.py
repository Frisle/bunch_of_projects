import pyperclip
import os
import webbrowser
import subprocess
import threading
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from pathlib import Path


pathToServer  = os.path.join(os.getcwd(), 'launch.exe')
cardsfilepath = os.path.join(os.getcwd(), 'cardsFile.txt')#строка указывает скрипту работать с файлом в той же директории
filepathList = os.path.join(os.getcwd(), 'list.txt')
readMeFile = os.path.join(os.getcwd(), 'README')
listForArticles = os.path.join(os.getcwd(), 'auto_list.txt')



def creatingWorkAssets():
	try:
		f = open("cardsFile.txt", "r")
		f1 = open("list.txt", "r")
		f2 = open("auto_list.txt", "r")
	except FileNotFoundError:
		f = open("cardsFile.txt", "w")
		f.close()
		f1 = open("list.txt", "w")
		f1.close()
		f2 = open("auto_list.txt", "w")
		f2.close()
	else:
		None
creatingWorkAssets()



def buttonSwap():
	if chk_state.get() == True:
		newState = "Очистить"
		writeInFile.configure(text=newState)
	else:
		writeInFile.configure(text="Записать")

def revriteFiles():
	fileList = open(filepathList, "r+", encoding="utf-8")
	fileList.truncate(0)
	fileList.close()
	fileCards = open(cardsfilepath, "r+", encoding="utf-8")
	fileCards.truncate(0)
	fileCards.close()

def openCardsFile():#открывает текстовый файл с записанными карточками
	editWindow = Toplevel()
	editWindow.title("Обувной учет. Версия 1.0")
	editWindow.geometry('500x500+300+300')
	editWindow.iconbitmap('tag_icon.ico')
	
	editTextBox = Text(editWindow, width=65, wrap=WORD, font='Arial 10', height=20)
	editTextBox.place(x=15, y=10)
	
	with open(cardsfilepath, "r", encoding="utf-8") as FileRead:
		for line in FileRead:
			text = line
			editTextBox.insert(1.0, text)
	def writeChange():
		with open(cardsfilepath, "w", encoding="utf-8") as FileRead:
			changed = editTextBox.get(1.0, END)
			FileRead.write(changed)
	
	bSaveChanges = Button(editWindow, text="Сохранить", cursor='hand2', command=writeChange)
	bSaveChanges.place(x=15, y=350)


def openReadmeFile():
	pathToNotepad = 'C:\\Windows\\System32\\notepad.exe'
	subprocess.call([pathToNotepad, readMeFile])
	
def Browser():#запускает браузер по умолчанию для отрисовки карточек
	webbrowser.open('http://127.0.0.1:8000//cardspage.html')

def Server():
	subprocess.Popen(pathToServer)


#блок захвата буфера обмена и записи данных из таблиц Excell
def cardsConstruct():
	def writeFromClipboard():#блок перезаписи листа и инициализации буфера обмена
		file = open(filepathList, "w", encoding="utf-8")
		spam = pyperclip.waitForNewPaste()#получение данных из буфера и хранение
		pyperclip.copy('')#очистка буфера после сохранения данных в spam
		file.write(str(spam)+"\n")
		file.close()
	writeFromClipboard()
	with open (filepathList, "r", encoding="utf-8") as listFile:#аргумент encode кодирует текст в utf8
		#x = str(input("Ручной ввод(1). Авто(2) "))
		dataMassive = []
		for line in listFile:#блок извлекающий информацию из файла
			dataMassive.append(line.rsplit())#метод удаляет лишние знаки если есть
			filteredList = list(filter(None, dataMassive))#фильтрует список от пробелов
		for x in filteredList:#основной блок извлекающий и сортирующий информацию из листа
			try:
				name = x[0]
				article = x[1]
				number = x[2]
				sizes = x[9:]
				material = x[5]
				collor = x[6]
				shoeType = x[3]
				price = x[4]
				features = x[7]
				marker = x[8]
			except IndexError:
				messagebox.showerror("Ошибка ввода", "Скопированные данные не соответствуют требованию")
				return
			def cardsFormat():	
				if len(sizes) > 5:#логический блок конструирует карточки
					printSizesPrice = " \nЦена: \n\n\nРазмеры: {}\n{}</p>\n\n".format(str(x[9:13]), str(x[13:]))
				elif len(sizes) == 1:
					printSizesPrice = " \nЦена: \n\n\nРазмеры: {}</p>\n\n\n".format(str(x[9:]))
				else:
					printSizesPrice = " \nЦена: \n\n\nРазмеры: {}</p>\n\n\n".format(str(x[9:]))  		
				if number == "нет":
					printNumber = " / Цвет: {}".format(collor)
				else:
					printNumber = " / Номер: <b>{}</b>".format(number)
				if name == "нет":
					printName ="<p class=\"box\">{}".format(features.capitalize())
				else:
					printName = "<p class=\"box\">Бренд: {}".format(name)
				if len(name) > 6:
					printMaterial = " / Мат.: {}\n".format(material)
				else:
					printMaterial = " / Материал: {}\n".format(material)
				printArticul = "Арт.: {}".format(article)
				file = open(cardsfilepath, "a", encoding="utf-8")#блок записи в файл
				if marker == "М": #маленькие карточки
					file.write(printName.replace("Бренд: ", "") + "\n")
					file.write(printArticul)
					file.write(printNumber.replace("Номер: ", "№: ") + "\n")
					file.write(printSizesPrice.replace("Размеры: ", ""))
					file.close()
				elif marker == "Б":#большие карточки
					file.write(printName)
					file.write(printMaterial)
					file.write(printArticul)
					file.write(printNumber)
					file.write(printSizesPrice)
					file.close()
				elif marker == "У":
					file.write(printArticul)
					file.write(printNumber)
					file.write(printSizesPrice)
					file.close()
			cardsFormat()
	cardsConstruct()

def manualInput():#блок ручного ввода
	listOfData = []
	inputData = str(eManualInput.get())
	listOfData.append(inputData.rsplit())#лист для записи введеных данных с заменой пробелов на запятые
	for x in listOfData:
		try:
			name = x[0].capitalize()
			article = x[1]
			number = x[2]
			material = x[3]
			collor = x[4]
			marker = x[5]
			sizes = x[6:]
		except IndexError:
			messagebox.showerror("Ошибка ввода", "Введите данные")
			return
		def cardsFormat():	
			if len(sizes) > 5:#логический блок конструирует карточки
				printSizesPrice = " \nЦена: \n\nРазмеры: {}\n{}</p>\n\n".format(str(x[6:11]), str(x[11:]))
			elif len(sizes) == 1:
				printSizesPrice = " \nЦена: \n\nРазмеры: {}</p>\n\n\n".format(str(x[6:]))
			else:
				printSizesPrice = " \nЦена: \n\nРазмеры: {}</p>\n\n\n".format(str(x[6:])) 
			if number == "нет":
				printNumber = " / Цвет: {}".format(collor)
			else:
				printNumber = " / Номер: <b>{}</b>".format(number)
			if len(name) > 6:
				printMaterial = " / Мат.: {}\n".format(material)
			else:
				printMaterial = " / Материал: {}\n".format(material)
			printName = "<p class=\"box\">Бренд: {}".format(name)
			printArticul = "Арт.: {}".format(article)
			file = open(cardsfilepath, "a", encoding="utf-8")#блок записи в файл
			if marker == "М": #маленькие карточки
				file.write(printName.replace("Бренд: ", "") + "\n")
				file.write(printArticul)
				file.write(printNumber.replace("Номер: ", "№: ") + "\n")
				file.write(printSizesPrice.replace("Размеры: ", ""))
				file.close()
			elif marker == "Б":#большие карточки
				file.write(printName)
				file.write(printMaterial)
				file.write(printArticul)
				file.write(printNumber)
				file.write(printSizesPrice)
				file.close()
			elif marker == "У":
				file.write(printArticul)
				file.write(printNumber)
				file.write(printSizesPrice)
				file.close()
		cardsFormat()

#блок записи с автоматическим поиском и заменой строк
def searchWriteAndReplace():
	if chk_state.get() == True:
		file = open(listForArticles, "w", encoding="utf-8")
		file.close()
		eDisplayTextFile.delete(1.0, END)
		return
	else:
		with open(listForArticles, "r", encoding="utf-8") as Fileread:
			eDisplayTextFile.delete(1.0, END)
			try:
				for line in Fileread:
					text = line
					eDisplayTextFile.insert(1.0, text)
			except Exception:
				None
	input_list = []
	tempList = []
	savedValues = []
	mane_input = str(WriteInput_art.get()).split()
	nameInput = str(writeInput_name.get())
	lenghtOfname = len(nameInput)	
	input_list.append(mane_input)
	for line in input_list:
		try:
			inputNewArt = str(line[0])
			inputNewNumber = line[1]
			numberLen = len(inputNewNumber)
			inputNewSize = line[2:]
			sizeString = "".join(inputNewSize)
			stringSize = len(inputNewArt)
		except IndexError:
			messagebox.showerror("Ошибка ввода", "Введите данные")
			return
	with open(listForArticles, "r", encoding="utf-8") as listFile:
		tempList = listFile.readlines()
		count = 0
		for line in tempList:
			splitLines = line.split()
			name = splitLines[0]
			art = splitLines[1]
			number = splitLines[2]
			if nameInput in name and lenghtOfname == len(name) and inputNewArt in art and stringSize == len(art) and numberLen == len(number) and inputNewNumber in number:
				ind = tempList.index(line)
				count = count + 1
	if count == 0:
			with open(listForArticles, "a", encoding="utf-8") as listFile:
				listFile.write("{} {} {} {}\n".format(nameInput, inputNewArt, inputNewNumber, sizeString))
			with open(listForArticles, "r", encoding="utf-8") as Fileread:
				eDisplayTextFile.delete(1.0, END)
				for line in Fileread:
					text = line
					eDisplayTextFile.insert(1.0, text)
	elif count >= 1:
		file = open(listForArticles, "r", encoding="utf-8")
		lines = file.readlines()
		file.close()
		savedValues.append(tempList[ind].replace("\n", " "))
		savedValues.append(sizeString+"\n")
		rewriteValues = "".join(savedValues)
		del lines[ind]
		with open(listForArticles, "w+", encoding="utf-8") as newFile:
			for line in lines:
    				newFile.write(line)
			newFile.write(rewriteValues)
		with open(listForArticles, "r", encoding="utf-8") as Fileread:
			eDisplayTextFile.delete(1.0, END)
			for line in Fileread:
				text = line
				eDisplayTextFile.insert(1.0, text)

def formListProduct():
	sortEditWindow = Toplevel()
	sortEditWindow.geometry('200x200+300+300')
	sortEditWindow.title("Обувной учет. Версия 1.0")

	tempList = []
	sortList = ""
	with open("auto_list.txt", "r", encoding="utf-8") as readFile:
		for line in readFile:
			tempList.append(line.rsplit())
			tempList.sort()
		for x in tempList:
			name = x[0]
			art = x[1]
			number = x[2]
			sizes = x[3:]
			sizes.sort()
			sizes1 = " ".join(sizes)

			with open(filepathList, "a", encoding="utf-8") as sortFile:
				name = "{} {} {} туф 0 эко-кожа нет нет М {}\n".format(name, art, number, sizes1)
				sortFile.write(name.replace("/", " "))		

'''функции вызова трединга'''

def CardsthreadFunction():
	thread = threading.Thread(target=cardsConstruct)
	thread.start()
	
    	
def ServerThreadFuncton():
	thread1 = threading.Thread(target=Server)
	thread1.start()
	
def ManualThreadFunction():
	thread2 = threading.Thread(target=manualInput)
	thread2.start()

def searchAndWrite():
	thread3 = threading.Thread(target=searchWriteAndReplace)
	thread3.start()

'''Секция размещения виджетов/кнопок интерфейса'''

window = Tk()
window.title("Обувной учет. Версия 1.0")
window.geometry('500x400+300+300')
window.iconbitmap('tag_icon.ico')

'''файловый менеджмет'''

bRevriteFiles = Button(window, text="Перезапись", cursor="hand2", command=revriteFiles)
bRevriteFiles.place(x=300, y=10, width=114)

bSeverStart = Button(window, text="Локальный сервер", cursor="hand2", command=ServerThreadFuncton)
bSeverStart.place(x=300, y=40, width=114)

bReadmeFile = Button(window, text="Readme", width=10, cursor="hand2", command=openReadmeFile)
bReadmeFile.place(x=415, y=10)



'''команды редактору'''

bExcelConst = Button(window, text="Ввод из Excell", cursor="hand2", command=CardsthreadFunction)
bExcelConst.place(x=1, y=10, width=105)

bFileOpen = Button(window, text="Просмотр файла", cursor="hand2", command=openCardsFile)
bFileOpen.place(x=1, y=40, width=105)

bOpenBrowser = Button(window, text="Вывод этикеток", cursor="hand2", command=Browser)
bOpenBrowser.place(x=1, y=70, width=105)

bManualInput = Button(window, text="Ручной ввод", cursor="hand2", command=ManualThreadFunction)
bManualInput.place(x=1, y=100, width=105)

writeInFile = Button(window, text="Записать", cursor="hand2", command=searchAndWrite)
writeInFile.place(x=1, y=130, width=105)


chk_state = IntVar()  
chk_state.set(-1)
check = Checkbutton(window, text="Начать запись заново", variable=chk_state, onvalue=1, offvalue=0, command=buttonSwap)
check.place(x=350, y=370)

'''ввод'''

eManualInput = Entry(window, width=60)
eManualInput.place(x=120, y=100)

WriteInput_art = Entry(window, width=20)
WriteInput_art.place(x=250, y=130)

writeInput_name = Entry(window, width=20)
writeInput_name.place(x=120, y=130)

eDisplayTextFile = Text(window, width=60, wrap=WORD, font='Arial 10', height=10)
eDisplayTextFile.place(x=35, y=200)

with open(listForArticles, "r", encoding="utf-8") as Fileread:
	eDisplayTextFile.delete(1.0, END)
	try:
		for line in Fileread:
			text = line
			eDisplayTextFile.insert(1.0, text)
	except Exception:
		None
	

'''labels'''
lLabelForManual = Label(window, font='Arial 9', text="Имя    Артикль    Номер    Материал    Цвет    Маркер    Размеры")
lLabelForManual.place(x=120, y=75)

lLabelForExcel = Label(window, text="")
lLabelForExcel.place(x=200, y=7)

llabelForName = Label(window, text="Наименование")
llabelForName.place(x=120, y=153)

lLabelForWrite = Label(window, font="Arial 8", text="Артикул Номер Размер")
lLabelForWrite.place(x=250, y=153)




window.mainloop()