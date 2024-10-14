# markTourneyDataTest.py
# System imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg

from sqlobject import *

import sys as sys
import os as os

# Personal imports
from accessResults import AccessResults
from accessPlayers import AccessPlayers
from accessTourneys import AccessTourneys
from accessClubs import AccessClubs

import cribbageconfig as cfg

from club import Club
from player import Player
from tourney import Tourney

# for testing
from dbms100tso import *

class MTDT(object):
	def __init__(self):
		print ('mark tourney data test')
		cfg.ar = AccessResults()
		cfg.ap = AccessPlayers()
		cfg.at = AccessTourneys()
		cfg.ac = AccessClubs()
		print ('cfg.ar ', cfg.ar)

		cfg.clubRecord = cfg.ac.clubByNumber(100)
		print ('cfg.clubRecord: ', cfg.clubRecord)

		self.allTourneys = cfg.at.allTourneysForClubBySeason(cfg.clubRecord[0], '2019-20')
		print('allTourneys: ', self.allTourneys)
		self.tourneysWithResults = cfg.at.getTourneyRecordsWithResults("2019-20")
		print ('With Results: ', self.tourneysWithResults)
		for ty in self.allTourneys:
			ty.Entered = ''
			ty.sync()
		# use list of tuples of qualifying tourneys
		for l in self.tourneysWithResults:
			ty = list(Tourney.select(Tourney.q.TourneyNumber == l[1]))[0]
			ty.Entered = '*'
			ty.sync()
if __name__ == '__main__':

	dbmsobject = TSO()
	app = MTDT()