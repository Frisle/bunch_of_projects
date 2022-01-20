from typing import Counter
import pyperclip
import xlsxwriter
import os
import webbrowser
import subprocess
import threading
from tkinter import *
from tkinter import messagebox, Frame
from tkinter.ttk import *
import time 


#строка указывает скрипту работать с файлом в той же директории
cardsfilepath = os.path.join(os.getcwd(), 'cardsFile.txt')
pathToServer  = os.path.join(os.getcwd(), 'launch.exe')
filepathList = os.path.join(os.getcwd(), 'list.txt')
readMeFile = os.path.join(os.getcwd(), 'README')
autoListFile = os.path.join(os.getcwd(), 'auto_list.txt')



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
	textBoxRefresh()
	fileCards = open(cardsfilepath, "r+", encoding="utf-8")
	fileCards.truncate(0)
	fileCards.close()

def openCardsFile():#открывает текстовый файл с записанными карточками
	editWindow = Toplevel()
	editWindow.title("Обувной учет. Версия 1.0")
	editWindow.geometry('500x500+400+100')
	editWindow.iconbitmap('tag_icon.ico')
	editWindow.resizable(False, False)

	editTextBox = Text(editWindow, width=65, wrap=WORD, font='Arial 10', height=26)
	editTextBox.place(x=15, y=10)

	with open(cardsfilepath, "r", encoding="utf-8") as FileRead:
			text = FileRead.readlines()
			text1 = "".join(text)
			editTextBox.insert(1.0, text1)
	def writeChange():
		with open(cardsfilepath, "w", encoding="utf-8") as FileRead:
			changed = editTextBox.get(1.0, END)
			FileRead.write(changed)
	bSaveChanges = Button(editWindow, text="Сохранить", cursor='hand2', command=writeChange)
	bSaveChanges.place(x=15, y=470)


	def howManyTagsAreThere():
		with open(filepathList, "r", encoding="utf-8") as f:
			count = 0
			list1 = []
			for line in f:
				list1.append(line.split())
				filteredList = list(filter(None, list1))
				x = len(filteredList)
				print(x)
				if x == None:
					lLabelForDisplayQuont = Label(editWindow, text=" Число ценников 0")
					lLabelForDisplayQuont.place(x=110, y=470)
				else:
					lLabelForDisplayQuont = Label(editWindow, text="Число ценников " + str(x))
					lLabelForDisplayQuont.place(x=110, y=470)
		
	howManyTagsAreThere()

def openReadmeFile():
	pathToNotepad = 'C:\\Windows\\System32\\notepad.exe'
	subprocess.call([pathToNotepad, readMeFile])
	
def Browser():#запускает браузер по умолчанию для отрисовки карточек
	webbrowser.open('http://127.0.0.1:8000//cardspage.html')

def Server():
	subprocess.Popen(pathToServer)


#блок захвата буфера обмена и записи данных из таблиц Excell
def writeFromClipboard():#блок перезаписи листа и инициализации буфера обмена
	lLabelForTimer.configure(text="Ввод активен")
	try:
		file = open(filepathList, "a", encoding="utf-8")
		spam = pyperclip.waitForNewPaste(60)#получение днных из буфера и хранение
		pyperclip.copy('')#очистка буфера после сохранения данных в spam
		tempString = " ".join(spam.split("\t"))#превращение списка в строку с разделением пробелом
		file.write("{}".format(tempString))
		file.close()
		textBoxRefresh()
	except Exception:
		messagebox.showinfo("INFO","Ввод из буфера завершен")
		lLabelForTimer.configure(text="Ввод неактивен")
		return
	writeFromClipboard()

def cardsFormat():	
	try:
		with open (filepathList, "r", encoding="utf-8") as listFile:#аргумент encoding кодирует текст в utf8
			dataMassive = []		
			for line in listFile:#блок извлекающий информацию из файла
				dataMassive.append(line.rsplit())#метод делит целую строку на отдельные через запятую
				filteredList = list(filter(None, dataMassive))#фильтрует список от пробелов и создает лист с листами
			for x in filteredList:#основной блок извлекающий и сортирующий информацию из листа
					name = x[0]; article = x[1]; number = x[2]; shoeType = x[3]; price = x[4]; 
					material = x[5]; collor = x[6]; features = x[7]; marker = x[8]; sizes = x[9:]
					#логический блок конструирует карточки
					if len(sizes) > 5 and len(sizes) < 11:
						printSizesPrice = " \nЦена: \n\n\nРазмеры: {}\n{}</p>\n\n".format(str(x[9:14]), str(x[14:]))
					elif len(sizes) > 8:
						printSizesPrice = " \nЦена: \n\n\nРазмеры: {}\n{}\n{}</p>\n\n".format(str(x[9:14]), str(x[14:20]), str(x[20:]))
					elif len(sizes) == 1:
						printSizesPrice = " \nЦена: \n\n\nРазмеры: {}</p>\n\n".format(str(x[9:])) 		
					else:
						printSizesPrice = " \nЦена: \n\n\nРазмеры: {}</p>\n\n".format(str(x[9:]))
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

					if article == "нет":
						printArticul = "Арт.: {}".format(features)
					else:
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
	except Exception:
		messagebox.showerror("Ошибка ввода", "Список пуст или данные введены неверно")
		return

def manualInput():#блок ручного ввода
	listOfData = []
	tempList = []
	inputData = str(eManualInput.get()).rsplit()
	tempList.append(inputData)
	for x in tempList:
		try:
			str1 = x[0]; str2 = x[1]; str3 = x[2]; str4 = x[3]; str5 = x[4]; str6 = x[5]
			str7 = x[6:]
			str7 = " ".join(str7)
		except IndexError:
			messagebox.showerror("Ошибка ввода", "Введите данные")
			return
		mod_InputData = "{} {} {} нет 0 {} {} нет {} {} \n".format(str1, str2, str3, str4, str5, str6, str7)
	listOfData.append(mod_InputData)#лист для записи введеных данных с заменой пробелов на запятые
	with open(filepathList, "a", encoding="utf-8") as FileRead:
		FileRead.write(mod_InputData)
	textBoxRefresh()
	
#блок записи с автоматическим поиском и заменой строк
def searchWriteAndReplace():
	#если чек бокс = True функция меняет назначение на удаление данных из auto_list
	if chk_state.get() == True:
		file = open(autoListFile, "w", encoding="utf-8")
		file.close()
		eDisplayTextFile.delete(1.0, END)
		return
	else:
		quickWriteRefreshBox() 
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
	with open(autoListFile, "r", encoding="utf-8") as listFile:
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
			with open(autoListFile, "a", encoding="utf-8") as listFile:
				listFile.write("{} {} {} {}\n".format(nameInput, inputNewArt, inputNewNumber, sizeString))
			quickWriteRefreshBox()
	elif count >= 1:
		file = open(autoListFile, "r", encoding="utf-8")
		lines = file.readlines()
		file.close()
		savedValues.append(tempList[ind].replace("\n", " "))
		savedValues.append(sizeString+"\n")
		rewriteValues = "".join(savedValues)
		del lines[ind]
		with open(autoListFile, "w+", encoding="utf-8") as newFile:
			for line in lines:
					newFile.write(line)
			newFile.write(rewriteValues)
		quickWriteRefreshBox()

def changeQuickWrite():
	with open(autoListFile, "w", encoding="utf-8") as ReadFile:
		change = eDisplayTextFile.get(1.0, END)
		ReadFile.write(change)
	

def formListFromAuto():
	marker = eMarkerEntry.get()
	tempList = []
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
				name = "{} {} {} нет 0 нет нет нет {} {}\n".format(name, art, number, marker, sizes1)
				sortFile.write(name.replace("/", " "))		
			textBoxRefresh()

#блок записи в excell
def excellWrite():
	workbook = xlsxwriter.Workbook('temp.xlsx')
	worksheet = workbook.add_worksheet()

	tempList = []
	row = 0
	col = 0
	sizes1 =[]
	with open(filepathList, "r", encoding="utf-8") as readFile:
		for line in readFile:
			tempList.append(line.rsplit())
		for x in tempList:
			art = x[1]; name = x[0]; number = x[2]; type = x[3]; price = x[4];
			material = x[5]; features = x[6]; collor = x[7]; marker = x[8]; sizes = x[9:]
			sizes1.append(sizes)
			worksheet.write(row, col, name); worksheet.write(row, col+1, art); 
			worksheet.write(row, col+2, number); worksheet.write(row, col+3, type); 
			worksheet.write(row, col+4, price); worksheet.write(row, col+5, material)
			worksheet.write(row, col+6, features); worksheet.write(row, col+7, collor)
			worksheet.write(row, col+8, marker); worksheet.write_row(row, 9, sizes)
			row+=1
	workbook.close()



'''функции вызова трединга'''

def CardsthreadFunction():
	thread = threading.Thread(target=writeFromClipboard)
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
window.geometry('1000x450+200+200')
window.iconbitmap('tag_icon.ico')
window.resizable(False, False)

""" фреймы """

frame1 = Frame(window, relief="groove", borderwidth=10, width=490, height=420)
frame1.place(x=4, y=10) 

""" меню """

mainmenu = Menu(window)
window.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Просмотр файла", command=openCardsFile)
filemenu.add_command(label="Перезапись", command=revriteFiles)
filemenu.add_command(label="Локальный сервер", command=ServerThreadFuncton)
#filemenu.add_command(label="Выход")
 
helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Документация", command=openReadmeFile)
 
mainmenu.add_cascade(label="Меню",
					 menu=filemenu)
mainmenu.add_cascade(label="Справка",
					 menu=helpmenu)

'''файловый менеджмет'''


bAutoListChange = Button(frame1, text="Сохранить", cursor="hand2", command=changeQuickWrite)
bAutoListChange.place(x=1, y=380)

bCreatTags = Button(window, text="Создать этикетки", cursor="hand2", command=cardsFormat)
bCreatTags.place(x=500, y=400, width=105)

bStopBuffer = Button(window, text="test")
bStopBuffer.bind()


'''команды редактору'''

bExcelConst = Button(window, text="Ввод из буфера", cursor="hand2", command=CardsthreadFunction)
bExcelConst.place(x=500, y=110, width=105)

bOpenBrowser = Button(window, text="Вывод этикеток", cursor="hand2", command=Browser)
bOpenBrowser.place(x=610, y=400, width=105)

bManualInput = Button(window, text="Ручной ввод", cursor="hand2", command=ManualThreadFunction)
bManualInput.place(x=500, y=75, width=105)

writeInFile = Button(frame1, text="Записать", cursor="hand2", command=searchAndWrite)
writeInFile.place(x=1, y=45, width=105)

bFormListEntry = Button(frame1, text="Сформировать", cursor="hand2", command=formListFromAuto)
bFormListEntry.place(x=90, y=380, width=105)

bButtonExcellSheetW = Button(window, text="Экспорт в Excell", cursor="hand2", command=excellWrite)
bButtonExcellSheetW.place(x=720, y=400, width=105)


chk_state = IntVar()  
chk_state.set(-1)
check = Checkbutton(frame1, text="Начать запись заново", variable=chk_state, onvalue=1, offvalue=0, command=buttonSwap)
check.place(x=1, y=90)

'''ввод'''

eManualInput = Entry(window, width=60)
eManualInput.place(x=620, y=75)

WriteInput_art = Entry(frame1, width=20)
WriteInput_art.place(x=240, y=47)

writeInput_name = Entry(frame1, width=20)
writeInput_name.place(x=110, y=47)

eDisplayTextFile = Text(frame1, width=66, wrap=WORD, font='Arial 10', height=15)
eDisplayTextFile.place(x=1, y=120)

eMarkerEntry = Entry(frame1, width=2)
eMarkerEntry.place(x=370, y=47)

#функция читает лист auto_file и обновляет текст бокс
def quickWriteRefreshBox():
	with open(autoListFile, "r", encoding="utf-8") as Fileread:
		eDisplayTextFile.delete(1.0, END)
		try:
			temp = Fileread.readlines()
			text = "".join(temp)
			eDisplayTextFile.insert(1.0, text)
		except Exception:
			None
quickWriteRefreshBox()


eListDisplayBox = Text(window, width=70, wrap=WORD, font='Arial 10', height=15)
eListDisplayBox.place(x=500, y=140)


#функция читает list и обновляет текст бокс
def textBoxRefresh():
	with open(filepathList, "r", encoding="utf-8") as ReadFile:
		eListDisplayBox.delete(1.0, END)
		temp = ReadFile.readlines()
		listText = "".join(temp)
		eListDisplayBox.insert(1.0, listText)
		def makeChangeInLits():
			with open(filepathList, "w", encoding="utf-8") as Filelist:
				tempList = eListDisplayBox.get(1.0, END)
				Filelist.write(tempList)
	bRefreshTextBox = Button(window, text="Сохранить", cursor="hand2", command=makeChangeInLits)
	bRefreshTextBox.place(x=920, y=400)
textBoxRefresh()


'''labels'''
lLabelForManual = Label(window, font='Arial 9', text="Имя    Артикль    Номер    Материал    Цвет    Маркер    Размеры")
lLabelForManual.place(x=619, y=96)

llabelForName = Label(frame1, text="Наименование")
llabelForName.place(x=115, y=70)

lLabelForWrite = Label(frame1, font="Arial 8", text="Артикул Номер Размер")
lLabelForWrite.place(x=237, y=70)

lLabelForMarker = Label(frame1, font="Arial 10", text="Маркер")
lLabelForMarker.place(x=400, y=47)

lLabelForTimer = Label(window, font="Arial 9", text="Ввод неактивен")
lLabelForTimer.place(x=610, y=115)

lLabelForManualMode = Label(frame1, font="Arial 9", text="Система для несортированных предметов")
lLabelForManualMode.place(x=100, y=2)

lLabelForAutoMode = Label(window, font="Arial 9", text="Система для сортированных предметов")
lLabelForAutoMode.place(x=640, y=20)


window.mainloop()