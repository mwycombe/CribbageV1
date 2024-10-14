from sqlobject import *
from club import Club
from tourney import Tourney
from player import Player
from accessTourneys import AccessTourneys
from accessResults import AccessResults
from accessPlayers import AccessPlayers
from accessClubs import AccessClubs
import cribbageconfig as cfg

class TSO (object):
	# connection will be initialized when TSO is instantiated
	def __init__(self):
		# set up to use PySeniors database
		global cstring
		global conn
		global at
		global ar
		global ap
		# at = AccessTourneys()
		# ar = AccessResults()
		# ap = AccessPlayers()
		cstring = 'sqlite:c:\Cribbage\dbms\db100.sqlite3'
		print ('Assign cstring: ',cstring)
		conn = connectionForURI(cstring)
		print('conn: ', conn)
		sqlhub.processConnection = conn


