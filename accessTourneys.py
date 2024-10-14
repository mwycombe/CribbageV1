# accessTourneys.py
# 12/10/2019
# Caller is responsible to sort the list of returned Tourney sqlobjects
# into required order

from sqlobject import *
from tourney import Tourney
from scorecard import ScoreCard

import os
import sys
import datetime

class AccessTourneys (object):
	def allTourneys(self):
		return list(Tourney.select())
	def allTourneysForClub(self,club):
		# club is a Club sqlobjext
		# returns a list
		return  list(Tourney.select(Tourney.q.Club == club))
	def allTourneysForClubBySeason(self, club, season):
		# club is a Club sqlobject
		# season is a string object
		# returns a list
		return list(Tourney.select(
					AND(Tourney.q.ClubID == club,
					    Tourney.q.Season == season)))
	def returnOneTourney(self,club,season,tourneyNumber):
		# club is a Club sqlobject
		# season is a string object
		# tourneyNumber is an integer tourney number
		# returns a list
		return list(Tourney.select(
					AND(Tourney.q.Club == club,
					    Tourney.q.Season == season,
					    Tourney.q.TourneyNumber == tourneyNumber)))
	def getTourneyIdByDate(self,isoDate):
		# print('at date: ', date)
		# tid = list(Tourney.select(Tourney.q.Date == date))[0].id
		# print('id: ', tid)
		return self.getTourneyRecordByDate(isoDate).id
	def getTourneyRecordByDate(self,isoDate):
		# incoming aDate is a string - Tourney DateCol returns a datetime.date object
		# from dbms DATE column so we have to convert the incoming ISO8601 formatted
		# date string into a datetime.date object to make the comparison
		print ('Requested isoDate: ', type(isoDate), isoDate)
		return list(Tourney.select(Tourney.q.Date == datetime.date.fromisoformat(isoDate)))[0]
	def getTourneyRecordById(self,tid):
		# returns a single Tourney object
		return Tourney.get(tid)
	def getTourneyByNumber(self,tno):
		# returns a list
		return list(Tourney.select(Tourney.q.TourneyNumber == tno))
	def countTourneysForSeason(self, season):
		return Tourney.select(Tourney.q.Season == season).count()
	def getTourneysWithResults(self, season):
		# return a list of tourneyid, tournenumber for ths season
		Q = "select TourneyID, TourneyNumber, Date from Tourney where TourneyID in "
		Q += " (select Distinct TourneyId from ScoreCard) and Season = '" + season + "' and TourneyNumber < 40"
		return list ( sqlhub.processConnection.queryAll(Q))
	def getTourneyRecordsWithResults(self, season):
		# return list of tourney field tuples that qualify
		Q = "select * from Tourney where TourneyID in (select distinct TourneyID from ScoreCard) and "
		Q += "Season = '" + season + "'"
		print ('Q: ', Q)
		return list (sqlhub.processConnection.queryAll(Q))
