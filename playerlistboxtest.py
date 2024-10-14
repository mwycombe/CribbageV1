# test out keystroke navigation in a listbox a la basic
# system imports
# 9/28/2019 This is a test to see how we can handle keystroke navigation of a listbox oversized list
# 12/13/2019 Fixed the run-off problem with X in search from top
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg

from sqlobject import *

import sys as sys
import os as os

# Personal imports
from datetime import datetime

from testdatesdb import TestDatesDB
from player import Player

class ListBoxTest (ttk.Frame):

	def __init__ (self, parent, title):
		super().__init__(parent)
		self.grid()

		# instance 'globals'
		self.subPanelList = []     # will store the subpanels in here.
		self.subPanelCount = 18    # number of subpanels

		self.players = tk.StringVar()
		self.playerInfo = []

		self.existingPlayers = []
		self.pNames = []

		self.parent = parent
		self.parent.title(title)

		self.getPlayers()
		self.buildPanels(self.parent)

		# now set up to set focus and grab keystrokes over the listbox
		self.listOfPlayers.focus_set()
		self.activeIndex = 0
		self.listOfPlayers.activate(self.activeIndex)  # start with the first entry active
		self.listOfPlayers.selection_set(self.activeIndex)  # and selected

		print('Initial Line: ',self.listOfPlayers.get(tk.ACTIVE))

		self.listOfPlayers.bind('<KeyRelease>',self.keyStroke)


	def keyStroke(self,keyEvent):
		# show key stroke
		# Make sure we show 0 as selected
		print('Active Index: ',self.activeIndex)

		if keyEvent.keysym == 'Down':
			print('Down key')
			print('Line: ',self.listOfPlayers.get(tk.ACTIVE))
			self.activeIndex = self.listOfPlayers.curselection()[0]
			print('activeIndex after down: ',self.activeIndex)

		elif keyEvent.keysym == 'Up':
			print('Up key')
			print('Line: ',self.listOfPlayers.get(tk.ACTIVE))
			self.activeIndex = self.listOfPlayers.curselection()[0]
			print('activeIndex after up: ', self.activeIndex)
		else:
			print(keyEvent.char.upper(), ' key pressed')
			if self.activeIndex == self.listOfPlayers.size() - 1:   # already at the end
				self.searchFromTop(self.listOfPlayers,keyEvent.char.upper())
			elif self.listOfPlayers.get(self.activeIndex + 1)[0].upper() == keyEvent.char.upper():
				self.activeIndex += 1
				self.listOfPlayers.see(self.activeIndex)
				self.listOfPlayers.event_generate('<Down>')
				print('Next down active index: ',self.activeIndex)
				print('Next down active line: ',self.listOfPlayers.get(self.activeIndex))
			else:
				self.searchFromTop(self.listOfPlayers,keyEvent.char.upper())
	# DONE: guard against a non-matched key, like Enter, that runs off the end.
	def searchFromTop(self,lbox,init):
		# just go to top for now
		print('Search from top')
		lbox.selection_clear(lbox.curselection())
		lbox.activate(0)
		ix = 0
		while (lbox.get(ix)[0].upper() != init) :
			ix += 1
			if (ix == lbox.size()):
				# we have reached the end of the list
				# default to first entry
				lbox.activate(0)
				lbox.selection_set(0)
				lbox.see(0)
				ix = 0
				break
		lbox.activate(ix)   # activate the first line we found with the init
		lbox.selection_set(ix)
		self.activeIndex = ix
		lbox.see(ix)
		print('New active line',lbox.get(self.activeIndex))
		print('New activeIndex: ',self.activeIndex)

	def getPlayers(self):
		# fill the list with existing players
		self.existingPlayers = list(Player.select().orderBy('FirstName'))
		print ('Players list:= ', len(self.existingPlayers))

	def buildPanels (self, parent=None):
		#****************
		# set up the panels and fields for the test
		#

		self.mainPanel = ttk.LabelFrame(
						 parent,
						 text = 'ListBox Test Panel',
						 width='50mc',
						 height='75m',
						 borderwidth='4p',
						 relief='sunken'
						 )
		self.mainPanel.grid(row=0,
		                    column=0,
		                    sticky='nw')
		self.mainPanel.grid_propagate(0)
		# self.datetime1Field.grid(row=2, column=1)
		self.buildListBox(self.mainPanel,self.existingPlayers)

	def buildListBox(self, parent,existingPlayers):
		# stert by building a small list box with a scroll bar
		for p in self.existingPlayers:
			self.playerInfo.append(p.FirstName + ' ' + p.LastName)
		self.players.set(self.playerInfo)
		self.listOfPlayers = tk.Listbox(parent,
		                                listvariable=self.players)
		self.listOfPlayers.grid(row=0,column=0)
		self.addVSB(parent,self.listOfPlayers)

	def addVSB(self,parent,LBox):
		self.vsb = tk.Scrollbar(parent,orient=tk.VERTICAL)
		self.vsb.grid(row=0,column=1,sticky='ns')
		self.vsb['command'] = LBox.yview
		LBox['yscrollcommand'] = self.vsb.set

	def buttonCommand(self):
		self.buttonMsg = mbx.askokcancel('Button Pressed')

		print ('SubPanelList: ',self.subPanelList)
		print ('Children of mainPanel',self.mainPanel.winfo_children())
		print ('Existing players: ',self.existingPlayers)

		print ('All done. . .')




if __name__ == '__main__':
	appTitle = 'ListBox Test'
	root = tk.Tk()
	root.rowconfigure(0,weight=1)
	root.columnconfigure(0,weight=1)


	# open up dhte test1 database for testing dates.
	# there are two fields TestDate1 DATE
	#                       TestDate2 DATETIME
	# dbmsName = 'TPySeniors.sqlite3'
	dbmsName = 'PySeniors.sqlite3'
	dbmsDirectory = 'c:/Cribbage/Seniors/dbms/'
	connection_string = 'sqlite:' + dbmsDirectory + dbmsName
	print ('About to try and open: ',connection_string)
	try:
		conn = connectionForURI(connection_string)
		sqlhub.processConnection = conn
		print('Connected successfully')
	except:
		print ('Unable to open ',connection_string, '...terminating')
		os._exit(-1)

	app = ListBoxTest(root,appTitle)
	app.mainloop()

