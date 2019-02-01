#! python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
from datetime import datetime,timedelta
import shelve
import random


class wordCheck(Frame):

	class wordObj():
		
			def __init__(self,word,meaning):
			
				self.word = word.strip()
				self.meaning = meaning.strip()
				self.addDate = datetime.now().strftime("%Y%m%d")
				self.lastSuccess = "Unknown"
				self.lastFail = "Unknown"
				self.failCount = 0

	def __init__(self,root):
	
		Frame.__init__(self,root,pady = 10)
		self.grid(row = 0,column = 0)
		self.create_widgets()
		self.initDB()
		self.loadDB()
		self.tWordTest()
		
	def create_widgets(self):
	
		self.wordPanel = LabelFrame(self,text = 'Word Display', font = ("tahoma","10","bold"))
		self.wordPanel.pack(fill = 'both',padx=2)

		self.wordDisplay = Label(self.wordPanel, width = 48, height = 6, text = "sophisticated", font=("tahoma","14","bold"), foreground = 'blue')
		self.wordDisplay.grid(row = 0, rowspan = 2, column = 0, columnspan = 6, sticky = 'we')
		
		self.statusPanel = LabelFrame(self,text = 'Statistics', font = ("tahoma","10","bold"))
		self.statusPanel.pack(fill = 'both',padx=2)
		
		self.lastSuccessLabel = Label(self.statusPanel, width = 24, text = "Last Success", foreground = 'red')
		self.lastSuccessLabel.grid(row = 0, column = 0, sticky = 'we')
		
		self.lastFailLabel = Label(self.statusPanel, width = 24, text = "Last Failed", foreground = 'red')
		self.lastFailLabel.grid(row = 0, column = 1, sticky = 'we')
		
		self.failCountLabel = Label(self.statusPanel, width = 24, text = "Failed Count", foreground = 'red')
		self.failCountLabel.grid(row = 0, column = 2, sticky = 'we')
		
		self.lastSuccessStatus = Label(self.statusPanel, width = 24, foreground = 'black')
		self.lastSuccessStatus.grid(row = 1, column = 0, sticky = 'we')
		
		self.lastFailStatus = Label(self.statusPanel, width = 24, foreground = 'black')
		self.lastFailStatus.grid(row = 1, column = 1, sticky = 'we')
		
		self.failCountStatus = Label(self.statusPanel, width = 24, foreground = 'black')
		self.failCountStatus.grid(row = 1, column = 2, sticky = 'we')

		self.checkPanel = LabelFrame(self,text = 'Test Result', font = ("tahoma","10","bold"))
		self.checkPanel.pack(fill = 'both',padx=2)
		
		self.resultLabel = Label(self.checkPanel, width = 24, text = "Result:", foreground = 'red')
		self.resultLabel.grid(row = 0, column = 0, sticky = 'e')
		
		global checkResult 
		checkResult = StringVar()
		
		self.resultList = ttk.Combobox(self.checkPanel, width = 24, textvariable = checkResult, values = ("Success","Failed"))
		self.resultList.grid(row = 0, column = 1, pady = 3, sticky = 'w')
		
		self.updateButton = Button(self.checkPanel, width = 24, text = 'Update Statistics', command = self.updateStat)
		self.updateButton.grid(row = 0, column = 2 , padx = 6, pady = 3, sticky = 'e')
		
		self.nextButton = Button(self, width = 10, text = 'Next', font=("tahoma","10","bold"), command = self.tWordTest)
		self.nextButton.pack(padx = 8, pady = 18)
		
		self.reportButton = Button(self, width = 10, text = 'Report', font=("tahoma","10","bold"), command = self.report)
		self.reportButton.pack(padx = 8, pady = 10)
		
	def initDB(self):
			
		wordDataBase = shelve.open("wordDB",writeback = True)
		
		with open("tVolcabulary.txt","r") as wordFile:

			for line in wordFile:
	
				if line != "" or line != "\n":
				
					if line.strip().split(":")[0] not in wordDataBase:
					
						wordObtained = line.strip().split(":")[0]
						meaningObtained = line.strip().split(":")[1]
						
						wordElement = self.wordObj(wordObtained,meaningObtained)
						wordDataBase[wordElement.word] = wordElement
						
		wordDataBase.close()
		
	def loadDB(self):

		global wordObjList
		wordObjList = []
		
		global waitingQueue
		waitingQueue = []
		
		d = shelve.open("wordDB")
		
		for key in d:
		
			wordObjList.append(d[key])	
				
		d.close()

	def tWordTest(self):

		dbObj = shelve.open("wordDB")
		checkResult.set("")
			
		wordNumber = random.randint(0,len(wordObjList)-1)
		
		global randWord
		randWord = wordObjList[wordNumber].word
		
		textToDisplay = randWord + "\n\n" + wordObjList[wordNumber].meaning
		
		self.wordDisplay["text"] = textToDisplay
		self.lastSuccessStatus["text"] = dbObj[randWord].lastSuccess
		self.lastFailStatus["text"] = dbObj[randWord].lastFail
		self.failCountStatus["text"] = dbObj[randWord].failCount
		
		popWord = wordObjList.pop(wordNumber)
		
		print("="*50)
		print("popWord: ",popWord.word)
		print("="*50)
		print("wordobjList: ",str(len(wordObjList)))
		
		for i in wordObjList:
		
			print(i.word)
			
		print("="*50)
		
		waitingQueue.append(popWord)
		
		print("waitingQueue: ",str(len(waitingQueue)))
		
		for i in waitingQueue:	
		
			print(i.word)
			
		print("="*50)
		
		if len(waitingQueue) >= 0.75 * len(wordObjList):
		
			backWord = waitingQueue.pop(0)
			print("backWord",backWord.word)
			wordObjList.append(backWord)
			
		print("="*50)
		
	def updateStat(self):
	
		db = shelve.open("wordDB",writeback = True)
	
		if checkResult.get() == "Success":
		
			db[randWord].lastSuccess = datetime.now().strftime("%Y%m%d")
			self.lastSuccessStatus["text"] = db[randWord].lastSuccess
			messagebox.showwarning("Warning","Status Updated Successfully!")
			
		elif checkResult.get() == "Failed":
		
			db[randWord].lastFail = datetime.now().strftime("%Y%m%d")
			db[randWord].failCount = db[randWord].failCount + 1
			self.lastFailStatus["text"] = db[randWord].lastFail
			self.failCountStatus["text"] = db[randWord].failCount
			messagebox.showwarning("Warning","Status Updated Successfully!")
			
		else:
		
			messagebox.showwarning("Warning","Please Mark Success Or Failed!")	
			
		db.close()
			
	def report(self):
	
		d = shelve.open("wordDB")
		fullList = []
		
		for key in d:
		
			fullList.append(d[key])
			
		seqNum = 1
		result = ""
		reportList = sorted(fullList,key = lambda word : word.failCount, reverse = True)
		
		for wordObject in reportList:
			
			result = result + str(seqNum) + ". " + wordObject.word + "({})".format(wordObject.meaning) + " : " + str(wordObject.failCount) + "\n"
			seqNum = seqNum + 1
		
		reportWindow = Toplevel(self)
		reportWindow.title("Report Sorted By Failed Count")
		reportWindow.transient(self)
		
		reportResults = scrolledtext.ScrolledText(reportWindow,width = 40, wrap = WORD,state = "normal")
		reportResults.pack()

		reportResults.insert(END,result)
		reportResults.config(state = "disabled")
			
	def exit_program(self):
	
		root.quit()
		root.destroy()
		exit()

if __name__ == "__main__":

	root=Tk()
	root.title("gWordChecker v1.0")
	wordCheck(root)
	root.mainloop()