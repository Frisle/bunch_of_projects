from tkinter import Button, END

def quickWriteRefreshBox(file, module):
		with open(file, "r", encoding="utf-8") as Fileread:
			module.delete(1.0, END)
			try:
				temp = Fileread.readlines()
				text = "".join(temp)
				module.insert(1.0, text)
			except Exception:
				pass
	

def textBoxRefresh(file, module):
		with open(file, "r", encoding="utf-8") as ReadFile:
			module.delete(1.0, END)
			temp = ReadFile.readlines()
			listText = "".join(temp)
			module.insert(1.0, listText)
			
def makeChangeInLits(file, module):
		with open(file, "w", encoding="utf-8") as Filelist:
			tempList = module.get(1.0, END)
			Filelist.write(tempList)

	