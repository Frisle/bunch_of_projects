import csv
import os
import subprocess
import threading
import webbrowser
from tkinter import *
from tkinter import Frame, messagebox
from tkinter.ttk import *
import pyperclip
import xlsxwriter

helpText = """ 
Работа программы основана на использовании таблиц Excell и взаимодействию
с браузером для отрисовок ценников.

Основная функция заключается в копировании строк из таблиц для дальнейшей автоматической
обработки программой.

Работа с вводом данных для автоматической обработки

1. По открытию программы нажать Ввод из буфера (активируется 60 секундное окно для ввода)
2. Открыть таблицы Excell и скопировать требуемое количество строк и нажать CTRL + C или копировать через контекстное меню.
3. На этом этапе в окне в правой стороне программы появятся скопированные строки. Для вывода строк в виде ценников, сперва необходимо запустить локальный сервер.
Для этого нужно открыть низпадающее Меню в левом углу программы и выбрать Локальный сервер.
4.Следующий шаг - создать ценники. На этом этапе программа проверяет правильность ввода (есть возможность проверить их вручную). Для создания ценников нужно нажать
кнопку Создать этикетки в нижней части правой стороны программы. И следом нажать Вывод этикеток (если все ценники оформлены правильно)
"""


#строка указывает скрипту работать с файлом в нужной директории
cardsfilepath = os.path.join(os.getcwd(), 'assets/cardsFile.txt')
pathToServer  = os.path.join(os.getcwd(), 'assets/launch.exe')
filepathList = os.path.join(os.getcwd(), 'assets/list.txt')
readMeFile = os.path.join(os.getcwd(), 'assets/README')
autoListFile = os.path.join(os.getcwd(), 'assets/auto_list.txt')
CSVFilePath = os.path.join(os.getcwd(), "assets/testCsvFile.csv")

try:
	f = open(cardsfilepath, "r")
	f1 = open(filepathList, "r")
	f2 = open(autoListFile, "r")
	f3 = open("temp.xlsx", "r")
except FileNotFoundError:
	f = open(cardsfilepath, "w")
	f.close()
	f1 = open(filepathList, "w")
	f1.close()
	f2 = open(autoListFile, "w")
	f2.close()
	f3 = open("temp.xlsx", "w")
	f3.close()
else:
    	None





try:
	file = open(CSVFilePath, "r", encoding="utf-8")
	file.close()
except FileNotFoundError:
	file = open(CSVFilePath, "w", encoding="utf-8")
	writer = csv.writer(file)
	header = ["Бренд", "Артикул", "Номер", "Тип", "Цена", "Материал", "Признак", "Цвет", "Метка", "Размеры"]
	writer.writerow(header)
	file.close()
else:
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

def main():#ведущая функция содержащая весь основной код
		
	def Browser():#запускает браузер по умолчанию для отрисовки карточек
		webbrowser.open('http://127.0.0.1:8000/assets/cardspage.html')

	def Server():#запускает локальный сервер для выгрузки страницы
		subprocess.Popen(pathToServer)

	def CreateToolTip(widget, text):#функция вызова класса tooltip
		toolTip = ToolTip(widget)
		def enter(event):
				toolTip.showtip(text)
		def leave(event):
				toolTip.hidetip()
		widget.bind('<Enter>', enter)
		widget.bind('<Leave>', leave)

	

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
		editWindow.iconbitmap('assets/tag_icon.ico')
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


	
		with open(filepathList, "r", encoding="utf-8") as f:
			count = 0
			list1 = []
			for line in f:
				list1.append(line.split())
				filteredList = list(filter(None, list1))
				x = len(filteredList)
				if x == None:
					lLabelForDisplayQuont = Label(editWindow, text="Число ценников 0")
					lLabelForDisplayQuont.place(x=110, y=470)
				else:
					lLabelForDisplayQuont = Label(editWindow, text="Число ценников " + str(x))
					lLabelForDisplayQuont.place(x=110, y=470)
			
	
#блок захвата буфера обмена и записи данных из таблиц Excell
	def writeFromClipboard():#блок перезаписи листа и инициализации буфера обмена
		lLabelForTimer.configure(text="Ввод активен")
		try:
			file = open(filepathList, "a", encoding="utf-8")
			spam = pyperclip.waitForNewPaste(20)#получение днных из буфера и хранение
			pyperclip.copy('')#очистка буфера после сохранения данных в spam
			tempString = " ".join(spam.split("\t"))#превращение списка в строку с разделением пробелом
			file.write("{}".format(tempString))
			file.close()
			textBoxRefresh()
		except Exception:
			messagebox.showinfo("INFO","Ввод из буфера завершен")
			lLabelForTimer.configure(text="Ввод неактивен")
			return
			
		
		
		
		
	printTagB = """
<p class=\"box\">Бренд: {}
_________________________
Арт.: {} / №: <b>{}</b> 
Мат.: {}
Цена: 


<b>Размеры</b>: {}</p>"""

	printTagM = """
<p class=\"box\">Бренд: {}
_________________________
Арт.: {} / №: <b>{}</b> 
Мат.: {}
Цена: 


"   ", "   ", "   ",</p>\n"""






	def cardsFormat():	
		try:
			#очистка готовых ценников перед записью
			fileCards = open(cardsfilepath, "r+", encoding="utf-8")
			fileCards.truncate(0)
			fileCards.close() 
			with open (filepathList, "r", encoding="utf-8") as listFile:#аргумент encoding кодирует текст в utf8
				dataMassive = []		
				for line in listFile:#блок извлекающий информацию из файла
					dataMassive.append(line.rsplit())#метод делит целую строку на отдельные через запятую
					filteredList = list(filter(None, dataMassive))#фильтрует список от пробелов и создает лист с листами
				for x in filteredList:#основной блок извлекающий и сортирующий информацию из листа	
					name = x[0]; article = x[1]; number = x[2]; shoeType = x[3]; price = x[4]; 
					material = x[5]; collor = x[6]; features = x[7]; marker = x[8]; sizes = x[9:]
					#логический блок конструирует карточки
					if len(sizes) > 5 and len(sizes) < 8:
						printSizes = "{}\n{}".format(str(x[9:14]), str(x[14:]))
					elif len(sizes) > 12:
						printSizes = "{}\n{}\n{}".format(str(x[9:14]), str(x[14:20]), str(x[20:]))
					elif len(sizes) == 1:
						printSizes = "{}".format(str(x[9:])) 		
					else:
						printSizes = "{}".format(str(x[9:]))
					if number == "нет":
						printNumber = "{}".format(collor)
					else:
						printNumber = "{}".format(number)
					
					if name == "нет":
						printName ="{}".format(features.capitalize())
					else:
						printName = "{}".format(name)
					
					if len(name) > 6:
						printMaterial = "{}".format(material)
					else:
						printMaterial = "{}".format(material)

					if article == "нет":
						printArticul = "{}".format(features)
					else:
						printArticul = "{}".format(article)
			
					file = open(cardsfilepath, "a", encoding="utf-8")#блок записи в файл
					if marker == "М": #маленькие карточки
						printTag = str(printTagM).format(printName, printArticul, printNumber)
						file.write(printTag)
						file.close()
						comboBoxMod()
					elif marker == "Б":
						printTag = str(printTagB).format(printName, printArticul, printNumber, printMaterial, printSizes)
						file.write(printTag)
						file.close
						comboBoxMod()
		except Exception:
			messagebox.showerror("Ошибка ввода", "Список пуст или данные введены неверно")
			return
	

	def manualInput():#блок ручного ввода
		listOfData = []
		inputDataName = str(eManualInputName.get())
		inputDataArt = str(eManualInputArt.get())
		inputDataNum = str(eManualInputNum.get())
		inputDataType = str(eManualInputType.get())
		inputDataPrice = str(eManualInputPrice.get())
		inputDataMat = str(eManualInputMat.get())
		inputDataCol = str(eManualInputCol.get())
		inputDataFeat = str(eManualInputFeat.get())
		inputDataSize = str(eManualInputSize.get()).split()
		proccesedSizes = " ".join(sorted(inputDataSize))
		if tagSizeVar.get() == 1:
			inputDataMark = "Б"
		elif tagSizeVar.get() == 2:
			inputDataMark = "М"
		try:
			if len(inputDataName) == 0:
				raise IndexError
			elif len(inputDataArt) == 0:
				raise IndexError 
			elif len(inputDataNum) == 0:
				raise IndexError
			elif len(inputDataType) == 0:
				raise IndexError
			elif len(inputDataPrice) == 0:
				raise IndexError
			elif len(inputDataMat) == 0:
				raise IndexError
			elif len(inputDataCol) == 0:
				raise IndexError
			elif len(inputDataFeat) == 0:
				raise IndexError
			elif len(inputDataMark) == 0:
				raise UnboundLocalError
			elif len(inputDataSize) == 0:
				raise IndexError
		except IndexError:
			messagebox.showerror("Ошибка ввода", "В одном из полей отсутствуют данные")
		except UnboundLocalError:
			messagebox.showerror("Ошибка ввода", "Выберите размер ценника")
			return
		mod_InputData = "{} {} {} {} {} {} {} {} {} {} \n".format(inputDataName, inputDataArt, inputDataNum, inputDataType, inputDataPrice, 
																		inputDataMat, inputDataCol, inputDataFeat, inputDataMark, proccesedSizes)
		listOfData.append(mod_InputData)#лист для записи введеных данных с заменой пробелов на запятые
		with open(filepathList, "a", encoding="utf-8") as FileRead:
			FileRead.write(mod_InputData)
		comboBoxMod()
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
		tempList = []
		savedValues = []
		inputName = writeInput_name.get()
		inputArt = WriteInput_art.get()
		inputNum = writeInput_num.get()
		inputSize = writeInput_size.get()
		inputNameLen = len(inputName)
		inputArtLen = len(inputArt)
		inputNumLen = len(inputNum)
		inputSizeLen = len(inputSize)
		try:
			if inputNameLen == 0:
				raise IndexError
			elif inputArtLen == 0:
				raise IndexError
			elif inputNumLen == 0:
				raise IndexError
			elif inputSizeLen == 0:
				raise IndexError
		except IndexError:
			messagebox.showerror("Ошибка ввода", "В одном из полей отсутствуют данные")
			return
		with open(autoListFile, "r", encoding="utf-8") as listFile:
			tempList = listFile.readlines()
			count = 0
			for line in tempList:
				splitLines = line.split()
				name = splitLines[0]
				art = splitLines[1]
				number = splitLines[2]
				if inputName in name and inputNameLen == len(name) and inputArt in art and inputArtLen == len(art) and inputNumLen == len(number) and inputNum in number:
					ind = tempList.index(line)
					count = count + 1
		if count == 0:
				with open(autoListFile, "a", encoding="utf-8") as listFile:
					listFile.write("{} {} {} {}\n".format(inputName, inputArt, inputNum, inputSize))
				comboBoxMod()
				quickWriteRefreshBox()
		elif count >= 1:
			file = open(autoListFile, "r", encoding="utf-8")
			lines = file.readlines()
			file.close()
			savedValues.append(tempList[ind].replace("\n", " "))
			savedValues.append(inputSize+"\n")
			rewriteValues = "".join(savedValues)
			del lines[ind]
			with open(autoListFile, "w+", encoding="utf-8") as newFile:
				for line in lines:
						newFile.write(line)
				newFile.write(rewriteValues)
			quickWriteRefreshBox()
			comboBoxMod()

	def changeQuickWrite():
		with open(autoListFile, "w", encoding="utf-8") as ReadFile:
			change = eDisplayTextFile.get(1.0, END)
			ReadFile.write(change)
	

	def formListFromAuto():
		if tagSizeVar1.get() == 1:
			marker = "Б"
		elif tagSizeVar1.get() == 2:
			marker = "М"
		try:
			if len(marker) == 0:
				raise UnboundLocalError
		except UnboundLocalError:
			messagebox.showerror("Ошибка ввода", "В одном из полей отсутствуют данные")
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
				sizes1 = " ".join(sorted(sizes))
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

	def csvExport():
		tempList = []
		with open(filepathList, "r", encoding="utf-8") as readFile:
			for line in readFile:
				tempList.append(line.rsplit())
				filteredList = list(filter(None, tempList))
			for x in filteredList:
				art = x[1]; name = x[0]; number = x[2]; type = x[3]; price = x[4];
				material = x[5]; features = x[6]; collor = x[7]; marker = x[8]; sizes = x[9:]
				sizes = " ".join(sizes)
				with open(CSVFilePath, "a", encoding="utf-8") as toWrite:
					writer = csv.writer(toWrite)
					writer.writerow([name, art, number, type, price, material, collor, features, marker, sizes])

	
	def helpWindow():
		help = Toplevel()
		help.title("Справка")
		help.geometry('1100x500+200+100')
		help.iconbitmap('assets/tag_icon.ico')
		help.resizable(False, False)

		

		lLableForHelp = Label(help, text = helpText, font = 'Arial 10')
		lLableForHelp.place(x = 10, y = 10)
		

	def CSVBrowser():
		browser = Toplevel()
		browser.title("CSV Браузер")
		browser.geometry('1000x500+300+100')
		browser.iconbitmap('assets/tag_icon.ico')
		browser.resizable(False, False)

		eWindowForCSVview = Text(browser, width=120, wrap=WORD, font='Arial 10', height=30)
		eWindowForCSVview.pack()


	'''функции трединга'''

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
	window.geometry('1010x460+200+200')
	window.iconbitmap('assets/tag_icon.ico')
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
	filemenu.add_command(label="CSV Браузер", command=CSVBrowser)
	#filemenu.add_command(label="Выход")
	
	helpmenu = Menu(mainmenu, tearoff=0)
	helpmenu.add_command(label="Документация", command=helpWindow)
	
	mainmenu.add_cascade(label="Меню",
						menu=filemenu)
	mainmenu.add_cascade(label="Справка",
						menu=helpmenu)

	'''файловый менеджмет'''
	iconForCreate = PhotoImage(file="assets/createTag.png")


	bAutoListChange = Button(frame1, text="Сохранить", cursor="hand2", command=changeQuickWrite)
	bAutoListChange.place(x=1, y=380)

	bCreatTags = Button(window, text="Создать этикетки", cursor="hand2", command=cardsFormat)
	bCreatTags.place(x=500, y=400)
	bCreatTags.config(image=iconForCreate)
	CreateToolTip(bCreatTags, text="Создать этикетки")

	bStopBuffer = Button(window, text="test")
	bStopBuffer.bind()


	'''команды редактору'''
	bExcelConst = Button(window, text="Буфер обмена", cursor="hand2", command=CardsthreadFunction)
	bExcelConst.place(x=790, y=110, width=105)

	
	iconForOutputTag = PhotoImage(file="assets/outputTags.png")
	bOpenBrowser = Button(window, text="Вывод этикеток", cursor="hand2", command=Browser)
	bOpenBrowser.place(x=550, y=400)
	bOpenBrowser.config(image=iconForOutputTag)
	CreateToolTip(bOpenBrowser, text="Вывод этикеток")
	
	bManualInput = Button(window, text="Запись новой позиции", cursor="hand2", command=ManualThreadFunction)
	bManualInput.place(x=500, y=85)

	writeInFile = Button(frame1, text="Записать", cursor="hand2", command=searchAndWrite)
	writeInFile.place(x=1, y=45, width=105)

	bFormListEntry = Button(frame1, text="Сформировать", cursor="hand2", command=formListFromAuto)
	bFormListEntry.place(x=90, y=380, width=105)

	bButtonExcellSheetW = Button(window, text="Экспорт в Excell", cursor="hand2", command=excellWrite)
	bButtonExcellSheetW.place(x=720, y=400, width=105)

	bButonCsvWrite = Button(window, text="Экспорт в CSV", cursor="hand2", command=csvExport)
	#радио кнопки выбора размера ценников
	tagSizeVar = IntVar()
	rTagButton1 = Radiobutton(window, text = "Б", variable=tagSizeVar, value=1)
	rTagButton2 = Radiobutton(window, text = "М", variable=tagSizeVar, value=2)
	rTagButton1.place(x=930, y=20)
	rTagButton2.place(x=960, y=20)
	
	tagSizeVar1 = IntVar()
	rTagButton3 = Radiobutton(window, text = "Б", variable=tagSizeVar1, value=1)
	rTagButton4 = Radiobutton(window, text = "М", variable=tagSizeVar1, value=2)
	rTagButton3.place(x=390, y=65)
	rTagButton4.place(x=430, y=65)

	#чек кнопка выбора действия стереть/записать
	chk_state = IntVar()  
	chk_state.set(-1)
	check = Checkbutton(frame1, text="Начать запись заново", variable=chk_state, onvalue=1, offvalue=0, command=buttonSwap)
	check.place(x=1, y=90)

	'''ввод'''

	


	icon = PhotoImage(file="assets/output-onlinepngtools.png")	
	#секция кнопок ручного ввода
	eManualInputName = Entry(window, width=15)
	bButtonForName = Button(window, command= lambda: eManualInputName.delete(0, END))
	bButtonForName.place(x=600, y=9)
	bButtonForName.config(image=icon)
	eManualInputArt = Entry(window, width=15)
	bButtonForArt = Button(window, command= lambda: eManualInputArt.delete(0, END))
	bButtonForArt.place(x=600, y=34)
	bButtonForArt.config(image=icon)
	eManualInputNum = Entry(window, width=15)
	bButtonForNum = Button(window, command= lambda: eManualInputNum.delete(0, END))
	bButtonForNum.place(x=600, y=59)
	bButtonForNum.config(image=icon)
	eManualInputType = Entry(window, width=15)
	bButtonForType = Button(window, command= lambda: eManualInputType.delete(0, END))
	bButtonForType.place(x=750, y=9)
	bButtonForType.config(image=icon)
	eManualInputPrice = Entry(window, width=15)
	bButtonForPrice = Button(window, command= lambda: eManualInputPrice.delete(0, END))
	bButtonForPrice.place(x=750, y=34)
	bButtonForPrice.config(image=icon)
	eManualInputMat = Entry(window, width=15)
	bButtonForMat = Button(window, command= lambda: eManualInputMat.delete(0, END))
	bButtonForMat.place(x=750, y=59)
	bButtonForMat.config(image=icon)
	eManualInputCol = Entry(window, width=15)
	bButtonForCol = Button(window, command= lambda: eManualInputCol.delete(0, END))
	bButtonForCol.place(x=900, y=9)
	bButtonForCol.config(image=icon)
	eManualInputFeat = Entry(window, width=15)
	bButtonForFeat = Button(window, command= lambda: eManualInputFeat.delete(0, END))
	bButtonForFeat.place(x=900, y=34)
	bButtonForFeat.config(image=icon)
	eManualInputSize =Entry(window, width=25)
	bButtonForSize = Button(window, command= lambda: eManualInputSize.delete(0, END))
	bButtonForSize.place(x=970, y=59)
	bButtonForSize.config(image=icon)

	eManualInputName.place(x=500, y=10)
	CreateToolTip(eManualInputName, text="Наименование")
	eManualInputArt.place(x=500, y=35)
	CreateToolTip(eManualInputArt, text="Артикул")
	eManualInputNum.place(x=500, y=60)
	CreateToolTip(eManualInputNum, text="Номер")
	eManualInputType.place(x=650, y=10)
	CreateToolTip(eManualInputType, text="Тип")
	eManualInputPrice.place(x=650, y=35)
	CreateToolTip(eManualInputPrice, text="Цена")
	eManualInputMat.place(x=650, y=60)
	CreateToolTip(eManualInputMat, text="Материал")
	eManualInputCol.place(x=800, y=10)
	CreateToolTip(eManualInputCol, text="Цвет")
	eManualInputFeat.place(x=800, y=35)
	CreateToolTip(eManualInputFeat, text="Признак")
	CreateToolTip(rTagButton1, text="Размер ценника")
	CreateToolTip(rTagButton2, text="Размер ценника")
	eManualInputSize.place(x=800, y=60)
	CreateToolTip(eManualInputSize, text="Размеры")

	"""секция для ввода автопоиска"""
	writeInput_num = Entry(frame1, width=15)
	writeInput_num.place(x=110, y=70)
	bButtonFor_num = Button(frame1, command= lambda: writeInput_num.delete(0, END))
	bButtonFor_num.place(x=210, y=69)
	bButtonFor_num.config(image=icon)
	CreateToolTip(writeInput_num, text="Номер")

	writeInput_size = Entry(frame1, width=15)
	writeInput_size.place(x=240, y=70)
	bButtonFor_size = Button(frame1, command= lambda: writeInput_size.delete(0, END))
	bButtonFor_size.place(x=340, y=69)
	bButtonFor_size.config(image=icon)
	CreateToolTip(writeInput_size, text="Один размер")

	WriteInput_art = Entry(frame1, width=15)
	WriteInput_art.place(x=240, y=47)
	bButtonFor_size = Button(frame1, command= lambda: WriteInput_art.delete(0, END))
	bButtonFor_size.place(x=340, y=46)
	bButtonFor_size.config(image=icon)
	CreateToolTip(WriteInput_art, text="Артикул")

	writeInput_name = Entry(frame1, width=15)
	writeInput_name.place(x=110, y=47)
	bButtonFor_size = Button(frame1, command= lambda: writeInput_name.delete(0, END))
	bButtonFor_size.place(x=210, y=46)
	bButtonFor_size.config(image=icon)
	CreateToolTip(writeInput_name, text="Наименование")

	#окошко вывода автопоиска
	eDisplayTextFile = Text(frame1, width=66, wrap=WORD, font='Arial 10', height=15)
	eDisplayTextFile.place(x=1, y=120)



	#функция читает лист auto_file и обновляет текст бокс автопоиска
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




	cComboForList = Combobox(window, width=77)
	cComboForList.place(x=500, y=150)
	
	def comboBoxMod():
		with open(filepathList, "r", encoding="utf-8") as fileRead:
			listFile = fileRead.readlines()
			tempList = []
			for x in listFile:
				tempList.append(x)
				cComboForList['values'] = (tempList)
	comboBoxMod()

	
	
	def listModifier():
		count = 0
		with open (filepathList, encoding='utf-8') as listForMod:		
			stringList = listForMod.readlines()
			stringGet = cComboForList.get()	
			for line in stringList:
				if stringGet == line:
					ind = stringList.index(line)
					tempContainer = stringList[ind]
					count = count =+ 1
					print(tempContainer)
			def destroyW(event):
				modifierWindow.destroy()
			modifierWindow = Toplevel()
			modifierWindow.title("Редактор")
			modifierWindow.geometry("600x90+200+100")
			modifierWindow.iconbitmap('assets/tag_icon.ico')
			modifierWindow.resizable(False, False)
			frame1 = Frame(modifierWindow, relief="groove", borderwidth=10, width=80, height=90)
			frame1.place(x=4, y=10)
			modifierWindow.bind("<Escape>", destroyW)
			try:
				eForModification = Text(frame1, font="Arial 10", width=80, height=2)
				eForModification.pack()
				eForModification.insert(0.0, tempContainer.strip())
			except UnboundLocalError:
				modifierWindow.destroy()
				messagebox.showerror("Ошибка", "Данные в строке выбор отстутствуют в списке или были изменены")
		if count == 1:
			def insideFunc():
				
				bTestButton = Button(modifierWindow, text="Изменение", command=insideFunc)
				bTestButton.place(x=400, y=60)
				newLine = eForModification.get(1.0, END)
				modifiedList = open(filepathList,"w", encoding='utf-8')
				stringList[ind] = newLine
				newFileContents = "".join(stringList)
				modifiedList.write(newFileContents)
				modifiedList.close()
				
				print(newLine)
				textBoxRefresh()
				comboBoxMod()
				
			insideFunc()
		
		else:
			return
		
			


	bTestButton = Button(window, text="Фиксация", command=listModifier)
	bTestButton.place(x=500, y=120)

	

	
	
	eListDisplayBox = Text(window, width=70, wrap=WORD, font='Arial 10', height=12)
	eListDisplayBox.place(x=500, y=200)

	scroll = Scrollbar( command=eListDisplayBox.yview)
	scroll.place(x = 990, y = 200, height = 200)
	eListDisplayBox.config(yscrollcommand=scroll.set)

	


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

	lLabelForTimer = Label(window, font="Arial 9", text="Ввод неактивен")
	lLabelForTimer.place(x=900, y=115)

	lLabelForManualMode = Label(frame1, font="Arial 9", text="Система для несортированных предметов")
	lLabelForManualMode.place(x=100, y=2)


	#--standalone --mingw64 --windows-disable-console --windows-icon-from-ico=tag_icon.ico --plugin-enable=tk-inter

	window.mainloop()
main()