# cribbagesetup.py
# 3/9/2020
#
# allows user to set up the directories and names for where things are located on their system
#
# this is equivalent to settings in many other programs
#
# config file is now named Cribbage.cfg
# contents are:
#   clubNumber = xxx
#   season = 20xx-yy
#   dbmsDirectory = d:\dir\dir\
#   dbmsName = <name>.sqlite3
#
# items retrieved from Clubs table
#   clubName reporting directory  location director
#
# cribageSetUp.py is used from tab with currently config'd club and report directory
# Once this setup has changed things, need to rerun startup to reinitialize
# cribbageconfig.py
#



# TODO: After configs are changed, need to re-read cfg file & retrieve club params
# TODO: Always re-run set-up to re-initialize cribbageConfigy.py imported as cfg.


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg
import sys as sys
import os as os
from sqlobject import *

# Personal imports
# dbms imports
from accessPlayers      import AccessPlayers
from accessTourneys     import AccessTourneys
from accessResults      import AccessResults
from accessClubs        import AccessClubs


class CribbageSetUp (ttk.Frame):
	# start with the name and location of the cfg file
	# then move on to its contents
	def __init__(self, parent):
		print ('Start peggerssetup')

		# control variables
		self.homeDictVar = tk.StringVar()
		self.dbmsDirectoryVar = tk.StringVar()
		self.reportDirectoryVar = tk.StringVar()
		self.dbmsNameVar = tk.StringVar()
		self.clubNameVar = tk.StringVar()
		self.clubNumberVar = tk.StringVar()
		self.clubLocationVar = tk.StringVar()
		self.clubSeasonVar = tk.StringVar()

		self.homeDictVar.set(os.getcwd())






		super().__init__(parent)

		self.setupPanel = ttk.Labelframe(parent,
		                                 relief='flat',
		                                 borderwidth = '5',
		                                 width = '20c',
		                                 height = '20c',
		                                 text='Setup Panel')
		self.setupPanel.grid(row=0, column=0, sticky='nsew')
		self.configPanel = ttk.LabelFrame(self.setupPanel,
		                                  relief = 'sunken',
		                                  borderwidth = '15',
		                                  # pady='20',
		                                  padding='20',
		                                  width = '20c',
		                                  height = '5c',
		                                  text='Config Location')
		self.directoryPanel = ttk.LabelFrame(self.setupPanel,
		                                     relief = 'sunken',
		                                     borderwidth = '15',
		                                     # pady='20',
		                                     padding='20',
		                                     width = '20c',
		                                     height = '5c',
		                                     text='Directory Panel')
		self.clubPanel =ttk.LabelFrame(self.setupPanel,
		                                relief = 'sunken',
		                                borderwidth = '15',
		                                # pady='20',
		                                padding='20',
		                                width = '20c',
		                                height = '5c',
		                                text='Club Panel')
		self.configPanel.grid(column=0, sticky='nsew')
		self.directoryPanel.grid(column=0, sticky='nsew')
		self.clubPanel.grid(column=0, sticky='nsew')
		print ('Home dir:= ', os.getcwd())

		# start with config location

		self.homeDictLabel = tk.Label(self.configPanel,
		                              text='Current Home Directory',
		                              width=20)
		self.homeDictValue = tk.Entry(self.configPanel,
		                         textvariable=self.homeDictVar,
		                         width = 45)
		self.noCfgLabel = tk.Label(self.configPanel,
		                           text='Unable to locate cfg file in home directory',
		                           bg='pink',
		                           fg='blue',
									width=45)
		self.retryCfgButton = tk.Button(self.configPanel,
		                                text='Correct')
		self.retryCfgButton.bind('<Button-1>', self.retryCfg)

		self.homeDictLabel.grid(row=0, column=0, sticky='ew')
		self.homeDictValue.grid(row=0, column=1, sticky='ew')
		self.noCfgLabel.grid(column=0, sticky='ew')
		self.retryCfgButton.grid(column=0, sticky='ew')

		self.noCfgLabel.grid(row=0, column=0, sticky='ew')
		self.retryCfgButton.grid(row=0, column=1, sticky='ew')
		self.hideWidget(self.noCfgLabel)
		self.hideWidget((self.retryCfgButton))

		# Directory panel content
		# Location for dbms and reports
		self.dbmsDirectoryLabel = tk.Label(self.directoryPanel,
		                                   text='Dbms Directory',
		                                   width = 20)
		self.dbmsDirectoryValue = tk.Entry(self.directoryPanel,
		                              textvariable=self.dbmsDirectoryVar,
		                              width = 45)
		self.dbmsNameLabel = tk.Label(self.directoryPanel,
		                              text='Dbms Name     ',
		                              width = 20)
		self.dbmsNameValue = tk.Entry(self.directoryPanel,
		                         textvariable=self.dbmsNameVar,
		                         width=45)
		self.reportDirectoryLabel = tk.Label(self.directoryPanel,
		                                     text='Report Directory',
		                                     width=20)
		self.reportDirectoryValue = tk.Entry(self.directoryPanel,
		                                textvariable=self.reportDirectoryVar,
		                                width=45)
		self.dbmsDirectoryLabel.grid(row=0, column=0, sticky='w')
		self.dbmsDirectoryValue.grid(row=0, column=1, sticky='ew')
		self.dbmsNameLabel.grid(row=1, column=0, sticky='w')
		self.dbmsNameValue.grid(row=1, column=1, sticky='ew')
		self.reportDirectoryLabel.grid(row=2, column=0, sticky='w')
		self.reportDirectoryValue.grid(row=2, column=1, sticky='ew')

		# club information
		self.clubNameLabel = tk.Label(self.clubPanel,
		                              text='Club Name    ',
		                              width=20)
		self.clubNameValue = tk.Entry(self.clubPanel,
		                         textvariable=self.clubNameVar,
		                         width=30)
		self.clubNumberLabel = tk.Label(self.clubPanel,
		                                text='Club Number  ',
		                                width=20)
		self.clubNumberValue = tk.Entry(self.clubPanel,
		                           textvariable=self.clubNumberVar,
		                           width=30)
		self.clubLocationLabel = tk.Label(self.clubPanel,
		                                  text='Club Location  ',
		                                  width=20)
		self.clubLocationValue = tk.Entry(self.clubPanel,
		                             textvariable=self.clubLocationVar,
		                             width=30)
		self.clubSeasonLabel = tk.Label(self.clubPanel,
		                                text='Club Season    ',
		                                width=20)
		self.clubSeasonValue = tk.Entry(self.clubPanel,
		                                textvariable=self.clubSeasonVar,
		                                width=20)
		self.clubNameLabel.grid(row=0, column=0, sticky='w')
		self.clubNameValue.grid(row=0, column=1, sticky='w')
		self.clubNumberLabel.grid(row=1, column=0, sticky='w')
		self.clubNumberValue.grid(row=1, column=1, sticky='w')
		self.clubLocationLabel.grid(row=2, column=0, sticky='w')
		self.clubLocationValue.grid(row=2, column=1, sticky='w')
		self.clubSeasonLabel.grid(row=3, column=0, sticky='w')
		self.clubSeasonValue.grid(row=3, column=1, sticky='w')
		# initialize entry fields, where possible
		self.homeDictVar.set(os.getcwd())
		# open existing config file
		try:
			print ('At directory: ', self.homeDictVar.get())
			self.configFile = open('Peggers.cfg', 'r+')

			self.parseConfigFile()
			self.dbmsDirectoryVar.set(self.dbmsDirectory)
			self.dbmsNameVar.set(self.dbmsName)
			self.reportDirectoryVar.set(self.reportDirectory)
			self.clubSeasonVar.set(self.clubSeason)
			self.clubNameVar.set(self.clubName)
			self.clubNumberVar.set(self.clubNumber)
			self.clubLocationVar.set(self.clubLocation)
		except FileNotFoundError:
			print('Unable to locate Peggers.cfg')
			self.showCfgLocateError()
	def parseConfigFile(self):
		for line in self.configFile:
			print (line)
			eName=line.split(sep='=')[0].strip()
			eValue = line.split(sep='=')[1].strip()
			if eName == 'title':
				self.appTitle = eValue
			elif eName == 'dbmsDirectory':
				self.dbmsDirectory = eValue
			elif eName == 'dbms':
				self.dbmsName = eValue
			elif eName == 'season':
				self.clubSeason = eValue
			elif eName == 'reportDirectory':
				self.reportDirectory = eValue
			elif eName == 'clubname':
				self.clubName = eValue
			elif eName == 'clubnumber':
				self.clubNumber = eValue
			elif eName == 'clublocation':
				self.clubLocation = eValue
	def showCfgLocateError(self):
		self.showWidget(self.noCfgLabel)
		self.showWidget(self.retryCfgButton)
	def hideWidget(self, w):
		w.grid_remove()
	def showWidget(self, w):
		w.grid()
	def retryCfg(self, event):
		self.hideWidget(self.noCfgLabel)
		self.hideWidget(self.retryCfgButton)
		self.homeDict.focus_force()
if __name__ == '__main__':
	root = tk.Tk()
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	root.title('Peggers System Setup')
	setup = PeggersSetUp(root)
	setup.rowconfigure(0, weight=1)
	setup.columnconfigure(0, weight=1)
	root.mainloop()
