#peggers.py
#
#################################################
#                                               #
#   Track scores each week for Peggers cribbage #
#   Lead in for GRT club tracking               #
#                                               #
#   All screen and tab creation point to here   #
#                                               #
#   Follow PEP8 naming conventions              #
#################################################
#
#   Index of modules used
#
#   oeggersconfig.py as cfg     globals
#   peggersstartup.py           kicks everything else off
#
#   Struct modules
#   
#   club.py                     sqlobject for Club record
#   tourney.py                  sqlobject for Tourney record
#   player.py                   sqlobject for Player record
#   scorecard.py                sqlobject for ScoreCard record
######### obsolete game record
#   game.py                     sqlobject for Game record
#########
#
#   Mem struct modules          used for fast results checking
######### mem structs are now obsolete
#
#   lists of sqlobjects for the records serve the same purpose
#
#   memplayer.py                In-memory players
#   memscorecard.py             In-memory scorecards
#   memgame.py                  In-memory games
#
#   peggersconfig.py            global inter-tab variables
#
#   Screen builders      Dict Key
#
#   <>                      root        app root level window
#   peggerstartup           peggers     top level container
#   masterscreen.py         master      container frame
#                           notebook    notebook frame for all tabs
#   playerstab.py           ptab        for add/change/del players
#   tourneystab.py          ttab        for add/change/del tourneys
#   resultstab.py           rsltab
#   reportstab.py           rtab        select/print reports
#   finishtab.py            ftab        wrap up - update db as required
#   helptab.py              htab        help tab
#
################## obsolete tabs ################
#   scoringtab.py           sctab       capture score cards and games
#   validatetab.py          vtab        validate/correct recorded scores
#   tourneyplayerstab.py    tptab       add/change/del/seat tourney players
#   seatingtab.py           stab        capture games & score cards
##################
#   Action modules
#
#   Becausa most actions are associated with Variable() object closely
#   associated with the tkinter widgets, the actions will mostly be
#   contained along with the screen defintion modules.
#
#   Results that need to be shared across modules will be promoted up
#   to the seniorsconfit module.
#
# 
#    
#    
#
#
################################################################################
# block of outstanding changes
# TODO: Set-up screen for location of reports, progs, database, update peggers.py to include report location
# TODO: Allow confirmation to build blank database or copy from incoming populated database
# TODO: Set-up screen to change club paramaters and create clean database
# TODO: Build quarter tourney allocation screen
# TODO: Test for Python minimum install of Python 3.8.1
#       assert sys.version_info >= (3,7) reqs for fromisoformat()
# TODO: Allow removal of results from results page
# TODO: Check for duplicate entry of results
# TODO: Run dbms scrub for conflicts - as this screws up reporting!
# TODO: Check editing of players - throws errors on dates.

# System imports
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

import peggersconfig as cfg
from peggersstartup     import PeggersStartup
from masterscreen       import MasterScreen
from playerstab         import PlayersTab
from tourneystab        import TourneysTab
from resultstab         import ResultsTab
from reportstab         import ReportsTab
from finishtab          import FinishTab
from helptab            import HelpTab

from player import Player


class Peggers (ttk.Frame):
	#************************************************************
	#   high level GUI
	#
	def __init__ (self, parent, title):
		super().__init__(parent)
		self.grid()
		self.parent = parent
		self.parent.grid()
		self.parent.title(title)
		##        self.rowconfigure(0,weight=1)
		##        self.columnconfigure(0,weight=1)
		cfg.screenDict['peggers'] = self  # register this frame
		print ('Start Peggers')
		# build global xref files
		# moved to peggersstartup.py
		# self.createPlayersXref()
		# self.createClubXref()
		# self.openAccessModules()
		self.buildPanels(self)          # pass in this panel
		

	#************************************************************
	#
	#   call all the modules that build panels for the app
	#   Each screen will also register itself in cfg.screenDict
	#
	def buildPanels (self, parent=None):
		# build master inside peggers panel
		# master sets up the notebook panel to be used by all tabs
		MasterScreen(parent)

		# build out the tabs into notebook and self register themselves
		# when done, postion in first tab

		PlayersTab(cfg.screenDict['notebook'])
		TourneysTab(cfg.screenDict['notebook'])
		# TourneyPlayersTab(cfg.screenDict['notebook'])
		# SeatingTab(cfg.screenDict['notebook'])
		# ScoringTab(cfg.screenDict['notebook'])
		# ValidationTab(cfg.screenDict['notebook'])
		ResultsTab(cfg.screenDict['notebook'])
		ReportsTab(cfg.screenDict['notebook'])
		FinishTab(cfg.screenDict['notebook'])
		HelpTab(cfg.screenDict['notebook'])

		self.setEventCapture()

	# def openAccessModules(self):
	# 	# create an instance of each access module in cfg
	# 	cfg.ap = AccessPlayers()
	# 	cfg.at = AccessTourneys()
	# 	cfg.ar = AccessResults()

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
		tabIndex = cfg.screenDict['notebook'].index(cfg.screenDict['notebook'].select())
		print('Tab Index:=',tabIndex)
		if tabIndex == 0:
			# pass
			cfg.screenDict['ptab'].tabChange(event)
		elif tabIndex == 1:
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
	print ('Starting peggers...')
	PeggersStartup.initDbms()
	PeggersStartup.createPlayersXref()
	PeggersStartup.createClubXref()
	PeggersStartup.createTourneyXref()

	# put root frame object into config module dictionary

	if 'root' not in cfg.screenDict:
		root = tk.Tk()
		cfg.screenDict['root'] = root
	print ('In peggers ... screenDict:= ', cfg.screenDict)
	# make resizeable
	cfg.screenDict['root'].rowconfigure(0, weight=1)
	cfg.screenDict['root'].columnconfigure(0, weight=1)


	# cfg.appTitle = 'Peggers Cribbage' # this is provided out of Peggers.cfg file
	app = Peggers(cfg.screenDict['root'],cfg.appTitle)

	print ('Populated screenDict at end of peggers startup...')
	for k in cfg.screenDict:
		print (k)

	app.mainloop()

    

