from openpyxl import Workbook, load_workbook
import os
import subprocess
import threading
import webbrowser
from tkinter import *
from tkinter import Frame, messagebox
from tkinter.ttk import *
import pyperclip
#import xlsxwriter
import keyboard

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
readMeFile = os.path.join(os.getcwd(), 'assets/README.txt')
autoListFile = os.path.join(os.getcwd(), 'assets/auto_list.txt')
CSVFilePath = os.path.join(os.getcwd(), "assets/testCsvFile.csv")
tempxlsx = os.path.join(os.getcwd(), "assets/temp.xlsx")


try:
	f = open(cardsfilepath, "r")
	f1 = open(filepathList, "r")
	f2 = open(autoListFile, "r")
	f3 = open(tempxlsx, "r")
except FileNotFoundError:
	f = open(cardsfilepath, "w")
	f.close()
	f1 = open(filepathList, "w")
	f1.close()
	f2 = open(autoListFile, "w")
	f2.close()
	f3 = open(tempxlsx, "w")
	f3.close()
else:
    	None


class filteredString():

	def clean(self, str):
		self.filtered = " "
		for sym in str:
			if sym != "'" and sym != "[" and sym != "]":
				self.filtered += sym
				
		return self.filtered
	
		

v = filteredString()


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
		comboBoxMod()
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
		b_clipboard_button.configure(text="Ввод активен")
		try:
			file = open(filepathList, "a", encoding="utf-8")
			spam = pyperclip.waitForNewPaste(20)#получение днных из буфера и хранение
			pyperclip.copy('')#очистка буфера после сохранения данных в spam
			tempString = " ".join(spam.split("\t"))#превращение списка в строку с разделением пробелом
			file.write("{}".format(tempString))
			file.close()
			textBoxRefresh()
			eListDisplayBox.see([0])
		except Exception:
			messagebox.showinfo("INFO","Ввод из буфера завершен")
			b_clipboard_button.configure(text="Буфер обмена")
			return
			
		
		
		
		
	printTagB = """
<p class=\"box\">Бренд: {}
_________________________
Арт.: {} / №: <b>{}</b> 
Мат.: {}
Цена: 


<b>Размеры</b>: {}</p>\n"""

	printTagM = """
<div class=\"box\">{}
___________
Арт.: {} 
№: <b class=\"bold"\>{}</b> 
Мат.: {}
Цена: 



<p>{}</p></div>"""

	emptyTag = """
<p class=\"box\">Бренд: {}
_________________________
Арт.: {} / №: <b>{}</b> 
Мат.: {}
Цена: 



<b>"____, ____, ____, ____, ____, 
____, ____, ____, ____, ____"</b></p>"""


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
					if len(sizes) > 6:
						printSizes = "{}\n{}".format(str(x[9:14]), str(x[14:]))
						cleanSizes = v.clean(printSizes)
					elif len(sizes) > 8:
						printSizes = "{}\n{}\n{}".format(str(x[9:14]), str(x[14:20]), str(x[20:]))
						cleanSizes = v.clean(printSizes)
					elif len(sizes) == 1:
						printSizes = "{}".format(str(x[9:])) 
						cleanSizes = v.clean(printSizes)		
					else:
						printSizes = "{}".format(str(x[9:]))
						cleanSizes = v.clean(printSizes)
					if number == "нет":
						printNumber = "{}".format(collor)
					else:
						printNumber = "{}".format(number)
					
					if name == "нет":
						printName ="{}".format(features.capitalize())
					else:
						printName = "{}".format(name)
						cleanName = printName.replace(".", " ")
						
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
						printTag = str(printTagM).format(cleanName, printArticul, printNumber, printMaterial, cleanSizes)
						file.write(printTag)
						file.close()
						comboBoxMod()
					elif marker == "Б":
						printTag = str(printTagB).format(cleanName, printArticul, printNumber, printMaterial, cleanSizes)
						file.write(printTag)
						file.close
						comboBoxMod()
		except Exception:
			messagebox.showerror("Ошибка ввода", "Список пуст или данные введены неверно")
			return 
	

	

	def emptyTags():
		i = 0
		while i < 20:
			file = open(cardsfilepath, "a", encoding="utf-8")
			printTag = str(emptyTag).format("_______", "___________", "_____", "_________")
			file.write(printTag)
			i += 1
		Browser()
			


	#блок ручного ввода
	def manualInput():
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
		wb = load_workbook(tempxlsx)
		sheet = wb.active
		newDict = {"A" : inputDataName, "B" : inputDataArt, "C" : inputDataNum,
            "D": inputDataType, "E": inputDataPrice, "F": inputDataMat, 
            "G": inputDataCol, "H": inputDataFeat, "I": inputDataMark, "K": proccesedSizes}
		sheet.append(newDict)
		wb.save(tempxlsx)
		wb.close()
		comboBoxMod()
		textBoxRefresh()
		eListDisplayBox.see("end")

	#блок записи с автоматическим поиском и заменой строк
	def searchWriteAndReplace():
		writeInput_num.focus_set()
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
		WriteInput_art.delete(0, END)
		writeInput_size.delete(0, END)
		writeInput_num.delete(0, END)

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
		with open(autoListFile, "r", encoding="utf-8") as readFile:
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
					sortFile.write(name)
				textBoxRefresh()

	#блок записи в excell
	"""def excellWrite():
		workbook = xlsxwriter.Workbook(tempxlsx)
		worksheet = workbook.add_worksheet()

		tempList = []
		row = 0
		col = 0
		sizes1 =[]
		with open(filepathList, "r", encoding="utf-8") as readFile:
			for line in readFile:
				tempList.append(line.rsplit())
			for x in tempList:
				art = x[1]; name = x[0]; number = x[2]; type = x[3]; price = x[4]
				material = x[5]; features = x[6]; collor = x[7]; marker = x[8]; sizes = x[9:]
				sizes1.append(sizes)
				worksheet.write(row, col, name); worksheet.write(row, col+1, art); 
				worksheet.write(row, col+2, number); worksheet.write(row, col+3, type); 
				worksheet.write(row, col+4, price); worksheet.write(row, col+5, material)
				worksheet.write(row, col+6, features); worksheet.write(row, col+7, collor)
				worksheet.write(row, col+8, marker); worksheet.write_row(row, 9, sizes)
				row+=1
		workbook.close()
		path_to_excell = r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.exe"
		subprocess.call([path_to_excell, tempxlsx])
"""
	
	def helpWindow():
		help = Toplevel()
		help.title("Справка")
		help.geometry('1100x500+200+100')
		help.iconbitmap('assets/tag_icon.ico')
		help.resizable(False, False)

		

		lLableForHelp = Label(help, text = helpText, font = 'Arial 10')
		lLableForHelp.place(x = 10, y = 10)
		

	


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

	def excellExport():
		thread4 = threading.Thread(target=0)
		thread4.start()


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
	
	#filemenu.add_command(label="Выход")
	
	helpmenu = Menu(mainmenu, tearoff=0)
	helpmenu.add_command(label="Документация", command=helpWindow)
	
	mainmenu.add_cascade(label="Меню",
						menu=filemenu)
	mainmenu.add_cascade(label="Справка",
						menu=helpmenu)

	'''файловый менеджмет'''
	iconForCreate = PhotoImage(file="assets/create_tag.png")


	bAutoListChange = Button(frame1, text="Сохранить", cursor="hand2", command=changeQuickWrite)
	bAutoListChange.place(x=1, y=380)

	bCreatTags = Button(window, text="Создать этикетки", cursor="hand2", command=cardsFormat)
	bCreatTags.place(x=500, y=400)
	bCreatTags.config(image=iconForCreate)
	CreateToolTip(bCreatTags, text="Создать этикетки")

	bStopBuffer = Button(window, text="test")
	bStopBuffer.bind()


	'''команды редактору'''
	add_button_icon = PhotoImage(file = "assets/adding_line.png")
	clipboard_button_icon = PhotoImage(file = "assets/clipboard_button.png")

	b_clipboard_button = Button(window, text="Буфер обмена", cursor="hand2", command=CardsthreadFunction)
	b_clipboard_button.place(x=600, y=400)
	b_clipboard_button.config(image = clipboard_button_icon)
	

	
	iconForOutputTag = PhotoImage(file="assets/output_tag.png")
	bOpenBrowser = Button(window, text="Вывод этикеток", cursor="hand2", command=Browser)
	bOpenBrowser.place(x=550, y=400)
	bOpenBrowser.config(image=iconForOutputTag)
	CreateToolTip(bOpenBrowser, text="Вывод этикеток")
	
	bManualInput = Button(window, text="Запись новой позиции", cursor="hand2", command=ManualThreadFunction)
	bManualInput.place(x=700, y=400)
	bManualInput.config(image=add_button_icon)

	writeInFile = Button(frame1, text="Записать", cursor="hand2", command=searchAndWrite)
	writeInFile.place(x=1, y=45, width=105)

	bFormListEntry = Button(frame1, text="Сформировать", cursor="hand2", command=formListFromAuto)
	bFormListEntry.place(x=90, y=380, width=105)

	bButtonExcellSheetW = Button(window, text="Экспорт в Excell", cursor="hand2", command=0)
	#bButtonExcellSheetW.place(x=720, y=400, width=105)

	

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
	#функция привязки клавиши Enter к вводу новых строк в список
	def focus():
		if len(eManualInputSize.get()) > 0:
			ManualThreadFunction()
		else:
			None
	keyboard.add_hotkey("Enter", focus)

	
	#секция кнопок ручного ввода
	icon = PhotoImage(file="assets/output-onlinepngtools.png")	
	edit_button_icon = PhotoImage(file = "assets/edit_button.png")
	empty_button_icon = PhotoImage(file = "assets/empty_tag.png")
	
	#кнопка ввода наименования
	eManualInputName = Entry(window, width=15)
	bButtonForName = Button(window, command= lambda: eManualInputName.delete(0, END))
	keyboard.add_hotkey("ctrl+1", lambda: eManualInputName.delete(0, END))
	keyboard.add_hotkey("F1", lambda: eManualInputName.focus_set())
	bButtonForName.place(x=610, y=20)
	bButtonForName.config(image=icon)
	labelName1 = Label(window, text="1.Наименование")
	labelName1.place(x=495, y=1)

	#кнопка ввода артикула
	eManualInputArt = Entry(window, width=15)
	bButtonForArt = Button(window, command= lambda: eManualInputArt.delete(0, END))
	keyboard.add_hotkey("ctrl+2", lambda: eManualInputArt.delete(0, END))
	keyboard.add_hotkey("F2", lambda: eManualInputArt.focus_set())
	bButtonForArt.place(x=610, y=65)
	bButtonForArt.config(image=icon)
	labelName2 = Label(window, text="2.Арт.")
	labelName2.place(x=495, y=45)

	#кнопка ввода номера
	eManualInputNum = Entry(window, width=15)
	bButtonForNum = Button(window, command= lambda: eManualInputNum.delete(0, END))
	keyboard.add_hotkey("ctrl+3", lambda: eManualInputNum.delete(0, END))
	keyboard.add_hotkey("F3", lambda: eManualInputNum.focus_set())
	bButtonForNum.place(x=610, y=110)
	bButtonForNum.config(image=icon)
	labelName3= Label(window, text="3.Номер", font="Arial 9")
	labelName3.place(x=495, y=90)
	
	
	#кнопка ввода типа модели
	eManualInputType = Entry(window, width=15)
	bButtonForType = Button(window, command= lambda: eManualInputType.delete(0, END))
	keyboard.add_hotkey("ctrl+4", lambda: eManualInputType.delete(0, END))
	keyboard.add_hotkey("F4", lambda: eManualInputType.focus_set())
	bButtonForType.place(x=750, y=20)
	bButtonForType.config(image=icon)
	labelName4 = Label(window, text="4.Тип")
	labelName4.place(x=635, y=1)

	#кнопка ввода цены
	eManualInputPrice = Entry(window, width=15)
	bButtonForPrice = Button(window, command= lambda: eManualInputPrice.delete(0, END))
	keyboard.add_hotkey("ctrl+5", lambda: eManualInputPrice.delete(0, END))
	keyboard.add_hotkey("F5", lambda: eManualInputPrice.focus_set())
	bButtonForPrice.place(x=750, y=65)
	bButtonForPrice.config(image=icon)
	labelName5 = Label(window, text="5.Цена")
	labelName5.place(x=635, y=45)

	#кнопка ввода материала иделия
	eManualInputMat = Entry(window, width=15)
	bButtonForMat = Button(window, command= lambda: eManualInputMat.delete(0, END))
	keyboard.add_hotkey("ctrl+6", lambda: eManualInputMat.delete(0, END))
	keyboard.add_hotkey("F6", lambda: eManualInputMat.focus_set())
	bButtonForMat.place(x=750, y=110)
	bButtonForMat.config(image=icon)
	labelName6 = Label(window, text="6.Материал")
	labelName6.place(x=635, y=90)

	#кнопка ввода цвета изделия
	eManualInputCol = Entry(window, width=15)
	bButtonForCol = Button(window, command= lambda: eManualInputCol.delete(0, END))
	keyboard.add_hotkey("ctrl+7", lambda: eManualInputCol.delete(0, END))
	keyboard.add_hotkey("F7", lambda: eManualInputCol.focus_set())
	bButtonForCol.place(x=900, y=20)
	bButtonForCol.config(image=icon)
	labelName7 = Label(window, text="7.Цвет")
	labelName7.place(x=785, y=1)

	#кнопка ввода отличителных свойств изделия
	eManualInputFeat = Entry(window, width=25)
	bButtonForFeat = Button(window, command= lambda: eManualInputFeat.delete(0, END))
	keyboard.add_hotkey("ctrl+8", lambda: eManualInputFeat.delete(0, END))
	keyboard.add_hotkey("F8", lambda: eManualInputFeat.focus_set())
	bButtonForFeat.place(x=960, y=65)
	bButtonForFeat.config(image=icon)
	labelName8 = Label(window, text="8.Признаки")
	labelName8.place(x=785, y=45)

	#копка ввода размеров
	eManualInputSize =Entry(window, width=25)
	bButtonForSize = Button(window, command= lambda: eManualInputSize.delete(0, END))
	keyboard.add_hotkey("ctrl+9", lambda: eManualInputSize.delete(0, END))
	keyboard.add_hotkey("F9", lambda: eManualInputSize.focus_set())
	bButtonForSize.place(x=960, y=110)
	bButtonForSize.config(image=icon)
	labelName9 = Label(window, text="9.Размеры")
	labelName9.place(x=785, y=90)

	#кнопка для активации функции пустых ценников
	bButtonForEmpty = Button(window, text="Пустые ценники", command=emptyTags)
	bButtonForEmpty.place(x = 650, y = 400)
	bButtonForEmpty.config(image=empty_button_icon)

	#блок вызова класса подписей элементов ToolTip	
	eManualInputName.place(x=510, y=20)
	CreateToolTip(eManualInputName, text="Наименование")
	eManualInputArt.place(x=510, y=65)
	CreateToolTip(eManualInputArt, text="Артикул")
	eManualInputNum.place(x=510, y=110)
	CreateToolTip(eManualInputNum, text="Номер")
	eManualInputType.place(x=650, y=20)
	CreateToolTip(eManualInputType, text="Тип")
	eManualInputPrice.place(x=650, y=65)
	CreateToolTip(eManualInputPrice, text="Цена")
	eManualInputMat.place(x=650, y=110)
	CreateToolTip(eManualInputMat, text="Материал")
	eManualInputCol.place(x=800, y=20)
	CreateToolTip(eManualInputCol, text="Цвет")
	eManualInputFeat.place(x=800, y=65)
	CreateToolTip(eManualInputFeat, text="Признак")
	CreateToolTip(rTagButton1, text="Размер ценника")
	CreateToolTip(rTagButton2, text="Размер ценника")
	eManualInputSize.place(x=800, y=110)
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

	#функция выполняет поиск по вводу из writeInput_num и вставляет данные в WriteInput_art если ввод из writeInput_num уже есть  
	def insert_text_widget(e):
		with open(autoListFile, "r", encoding="utf-8") as listFile:
			data = writeInput_num.get()
			tempList = listFile.readlines()
			for item in tempList:
				data_to_input = item.split()
				if data in data_to_input[2]:
					if len(data) == len(data_to_input[2]) and data in item:
						print(data, data_to_input[2])	
						WriteInput_art.insert(1, data_to_input[1])
						writeInput_size.focus_set()
					else:
						print("its activates")
						WriteInput_art.focus_set()
					break
				elif data not in data_to_input[2]:
					print("its activates too")
					WriteInput_art.focus_set()
					

	writeInput_num.bind("<Return>", insert_text_widget)

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
	cComboForList.place(x=500, y=170)

	def comboBoxMod():
		with open(filepathList, "r", encoding="utf-8") as fileRead:
			count = 0
			listFile = fileRead.readlines()
			tempList = []
			for x in listFile:
				count += 1
				tempList.append(x)
				cComboForList['values'] = (tempList) 
		lLabelForDisplayQuont = Label(window, font = "Arial 10", text="№: {}".format(count))
		lLabelForDisplayQuont.place(x=889, y=140)
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
				
				textBoxRefresh()
				comboBoxMod()
				
			insideFunc()
		
		else:
			return
		
			


	
	bTestButton = Button(window, text="Фиксация", command=listModifier)
	bTestButton.place(x=750, y=400)
	bTestButton.config(image=edit_button_icon)

	

	
	
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

	

	
	

	lLabelForManualMode = Label(frame1, font="Arial 9", text="Система для несортированных предметов")
	lLabelForManualMode.place(x=100, y=2)


	#--standalone --mingw64 --windows-disable-console --windows-icon-from-ico=tag_icon.ico --plugin-enable=tk-inter


	"""def csvExport():
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
"""



	window.mainloop()
main()


	#--standalone --onefile --mingw64 --windows-disable-console --windows-icon-from-ico=assets\tag_icon.ico --plugin-enable=tk-inter --include-data-dir=C:\Users\wda61\Dropbox\Python_projects\Pricetag\assets=assets








