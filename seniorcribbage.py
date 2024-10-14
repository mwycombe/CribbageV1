#seniorcribbage.py
#
#################################################
#                                               #
#   Track scores each week for senior cribbage  #
#   Lead in for GRT club tracking               #
#                                               #
#   All screen and tab creation promot to here  #
#                                               #
#   Follw PEP8 naming conventions               #
#################################################
#
#   Index of modules used
#
#   seniorsconfig.py as cfg     globals
#   seniorstartup.py            kicks everything else off
#
#   Struct modules
#   
#   club.py                     sqlobject for Club record
#   tourney.py                  sqlobject for Tourney record
#   player.py                   sqlobject for Player record
#   scorecard.py                sqlobject for ScoreCard record
#   game.py                     sqlobject for Game record
#
#   Mem struct modules          used for fast results checking
#
#   memplayer.py                In-memory players
#   memscorecard.py             In-memory scorecards
#   memgame.py                  In-memory games
#
#   Screen builders      Dict Key       
#
#   <>                      root        app root level window
#   seniorstartup           senior      top level container
#   masterscreen.py         master      container frame
#                           notebook    notebook frame for all tabs
#   playerstab.py           ptab        for add/change/del players
#   tourneystab.py          ttab        for add/change/del tourneys
#   tourneyplayerstab.py    tptab       add/change/del tourney players

### seatingtab no longer in use ########
#   seatingtab.py           stab        capture games & score cards
########################################

### renamed resultstab.py ##############
#   scoringtab.py           sctab       capture score cards and games
########################################

#   resultstab.py           rsltab      captures score cards for tourney

### validatetab no longer in use #######
#   validatetab.py          vtab        validate/correct recorded scores
########################################

#   reportstab.py           rtab        select/print reports
#   finishtab.py            ftab        wrap up - update db as required
#
#   Action modules
#
#   Because most actions are associated with Variable() object closely
#   associated with the tkinter widgets, the actions will mostly be
#   contained along with the screen defintion modules.
#
#   Variabless in memory that need to be shared across modules will be promoted up
#   to the seniorsconfit module.
#
#   Arrays of sqlobjects are sorted and kept in memory as required.
#   When they are updated in memory, the corresponding dbms row is updated.
#    
#   Any new sqlobjects created also create a new row in the dbms.
#
################################################################################


# System imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg
import sys as sys
import os as os
from sqlobject import *

# Personal imports
### prefix shows modules no longer in use

# dbms imports
from accessPlayers import AccessPlayers
from accessTourneys import AccessTourneys
from accessResults import AccessResults

import seniorsconfig as cfg
from seniorstartup      import CribbageStartup
from masterscreen       import MasterScreen
from playerstab         import PlayersTab
from tourneystab        import TourneysTab
### from tourneyplayerstab  import TourneyPlayersTab
### from seatingtab         import SeatingTab
### from scoringtab         import ScoringTab
from resultstab         import ResultsTab
### from validationtab      import ValidationTab
from reportstab         import ReportsTab
from finishtab          import FinishTab
from helptab            import HelpTab


class SeniorCribbage (ttk.Frame):
	#************************************************************
	#   high level GUI
	#
	def __init__ (self, parent, title):
		super().__init__(parent)
		self.grid()
		self.parent = parent
		# self.parent.grid()
		self.parent.title(title)
		##        self.rowconfigure(0,weight=1)
		##        self.columnconfigure(0,weight=1)
		cfg.screenDict['senior'] = self # register this frame
		print ('Start SeniorCribbage')
		self.openAccessModules()
		self.buildPanels(self)          # pass in this panel
		# set up access<sqlobjects> into the cfg module

	#************************************************************
	#
	#   call all the modules that build panels for the app
	#   Each screen will also register itself in cfg
	#
	def buildPanels (self, parent=None):
		# build master inside senior panel
		# master will also build it's subordinate panels and register them
		MasterScreen(parent)

		# build out the tabs into notebook and self register themselves
		# when done, postion in first tab

		PlayersTab(cfg.screenDict['notebook'])
		TourneysTab(cfg.screenDict['notebook'])
		# SeatingTab(cfg.screenDict['notebook']) NO LONGER USED
		ResultsTab(cfg.screenDict['notebook'])
		# ValidationTab(cfg.screenDict['notebook']) NO LONGER USED
		ReportsTab(cfg.screenDict['notebook'])
		FinishTab(cfg.screenDict['notebook'])
		HelpTab(cfg.screenDict['notebook'])

		self.setEventCapture()

	def openAccessModules(self):
		# create and instance of each access module in cfg
		cfg.ap = AccessPlayers()
		cfg.at = AccessTourneys()
		cfg.ar = AccessResults()
	#************************************************************
	#   capture notebook tab events one place
	#
	def setEventCapture(self):
		print ('generic notebook tab event capture')
		cfg.screenDict['notebook'].bind('<<NotebookTabChanged>>',self.tabChange)


	#************************************************************
	#   route captured tab event
	#
	def tabChange (self,event):
		# ttk.Notebook tabs are zero origin indexed
		# nb.select() returns the tcl window id of the form p.n.s.r....and it's index
		# which converts it to the tab index number
		tabIndex = cfg.screenDict['notebook'].index(cfg.screenDict['notebook'].select())
		print('Tab Index:=',tabIndex)
		if tabIndex == 0:
			cfg.screenDict['ptab'].tabChange(event)
		if tabIndex == 1:
			# pass
			cfg.screenDict['ttab'].tabChange(event)
		elif tabIndex == 2:
			cfg.screenDict['rsltab'].tabChange(event)
		elif tabIndex == 3:
			cfg.screenDict['rtab'].tabChange(event)
		elif tabIndex == 4:
			cfg.screenDict['ftab'].tabChange(event)
		elif tabIndex == 5:
			cfg.screenDict['htab'].tabChange(event)


if __name__ == '__main__':

	# call clase level init method

	CribbageStartup.initDbms()

	# put root frame object into config module dictionary

	if 'root' not in cfg.screenDict:
		root = tk.Tk()
		cfg.screenDict['root'] = root
	print ('In seniorcribbage ... screenDict:= ', cfg.screenDict)
	# make resizeable
	cfg.screenDict['root'].rowconfigure(0, weight=1)
	cfg.screenDict['root'].columnconfigure(0, weight=1)


	cfg.appTitle = 'Senior Cribbage'
	app = SeniorCribbage(cfg.screenDict['root'],cfg.appTitle)

	print ('Populated screenDict at end of seniorcribbage startup...')
	for k in cfg.screenDict:
		print (k)

	app.mainloop()

    

