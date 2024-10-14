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
		cstring = 'sqlite:c:\Cribbage\Peggers\dbms\PyPeggers.sqlite3'
		print ('Assign cstring: ',cstring)
		print ('ap: ', ap)
		conn = connectionForURI(cstring)
		sqlhub.processConnection = conn


