# cribbagetso.py
# 7/22/2020 cloned from peggerstso.py and updated to point to new 100.sqlite3 dbms
#
from sqlobject import *
from club import Club
from tourney import Tourney
from player import Player
from accessTourneys import AccessTourneys
from accessResults import AccessResults
from accessPlayers import AccessPlayers

class TSO (object):
	# connection will be initialized when TSO is instantiated
	def __init__(self):
		# set up to use PySeniors database
		global cstring
		global conn
		global at
		global ar
		global ap
		at = AccessTourneys()
		ar = AccessResults()
		ap = AccessPlayers()
		cstring = 'sqlite:c:\Cribbage\dbms\100.sqlite3'
		print ('Assign cstring: ',cstring)
		print ('ap: ', ap)
		conn = connectionForURI(cstring)
		sqlhub.processConnection = conn


