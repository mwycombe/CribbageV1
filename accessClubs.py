# accessBlub.py
# 2/24/2020
# Caller gets an unsorted list by default

from sqlobject import *
from club import Club
from player import Player

import os
import sys
import datetime

class AccessClubs (object):
	def allClubs(self):
		# returns a list
		return list(Club.select())
	def clubByNumber(self, number):
		# returns a list of one
		return list(Club.select(Club.q.clubNumber == number))
	def clubXref(self):
		# return tuple of results
		CXQ = "select PlayerID, ClubNumber from Player, Club where Player.ClubID = Club.ClubID"
		return sqlhub.processConnection.queryAll(CXQ)

	# clubXrefQuery = "select PlayerID, ClubNumber from Player, Club where Player.ClubID = Club.ClubID "
	# cfg.clubXref = { x[0]:x[1] for x in sqlhub.processConnection.queryAll(clubXrefQuery) }
