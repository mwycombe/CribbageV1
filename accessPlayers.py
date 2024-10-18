# accessPlayers.py
# 12/09/2019
# Caller is responsible to sort list of returned Players sqlobjects
# into desired order if a different order is needed

from sqlobject import *
from player import Player
from scorecard import ScoreCard

import os
import sys

class AccessPlayers (object):
	def allPlayers(self, club):
		# club is Club sqlobject
		# returns an unsorted list
		players = list(Player.select())
		return players
	def allActivePlayers(self, club):
		# club as Club sqlobject
		# active == 0 indicates inactive player
		# returns an unsorted list
		players = list(Player.select(Player.q.Active > 0))
		result = sorted(players, key = lambda Player: Player.LastName)
		return result
	def singlePlayerByLastName(self, club, lname):
		return list(Player.select(Player.q.LastName == lname))[0]
	def singlePlayerByFirstandLastNames(self,fname,lname):
		# return the first player in the list
		return list(Player.select(
			AND(Player.q.FirstName == fname,Player.q.LastName == lname)))[0]
	def getPlayerById(self, pid):
		# returns single player object
		return Player.get(pid)
	def playersByLastName(self, club):
		# club is Club sqlobject
		# return a list
		players = self.allPlayers(club)
		# sort by lastname
		result = sorted(players, key = lambda Player :Player.LastName)
		return result
	def playersByFirstName(self, club):
		# club is Club sqlobject
		# return a list
		players = self.allPlayers(club)
		# sort by FirstName
		result = sorted(players, key = lambda Player:Player.FirstName)
		return result
	def countPlayers(self,club):
		return len(self.allPlayers(club))
	def listOfScoreCardsByPlayer(self):
		# Confirmed that == Player.q.id works just fine
		# return a list
		return list(Player.select(ScoreCard.q.Player == Player.q.id))
	def getPlayerForaScoreCardInTourney(self, ScoreCard):
		# return the actual Player object instance, as it's just one, not a list
		return list(Player.select( Player.q.id == ScoreCard.Player))[0]
	def deletePlayerByName(self, lname, fname):
		DQ = "delete from Player where LastName = '" + lname + "' AND FirstName = '" + fname + "'"
		return sqlhub.processConnection.queryAll(DQ)
