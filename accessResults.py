# accessResults.py
# 12/09/2019
# Caller is responsible to sort the list of returned Results sqlobjects
# into desired order

import peggersconfig as cfg
from sqlobject import *
from scorecard import ScoreCard
from tourney import Tourney

import os
import sys

class AccessResults (object):
	# def __init__(self):
	# 	print ('In AccessResults')
	def allResults(self):
		# returns a list of ScoreCard objects
		return list(ScoreCard.select())
	def getSpecificScoreCard(self, tourney, player):
		# tourney and player are record sqlobjects
		# if not found returns empty list - no errors
		return list(ScoreCard.select(
									AND(ScoreCard.q.Player == player.id,
									    ScoreCard.q.Tourney == tourney.id)
									))
	def allTourneyResults(self,tourney):
		# tourney is the singular tourney object for which we wish to make the selection
		# results a list of ScoreCard objects
		results = list(ScoreCard.select(ScoreCard.q.Tourney == tourney))
		return results
	def tourneyResultsInEntryOrder(self,tourney):
		# sort results entered for particular tourney by entry order
		# returns a sorted list of ScoreCard objects
		# print ('Entry order results')
		results = self.allTourneyResults(tourney)
		sortedResults = sorted(results, key=lambda ScoreCard : ScoreCard.EntryOrder)
		return sortedResults
	def countTourneyResults(self,tourney):
		# uses tourney object to pick scorecards
		return ScoreCard.select(ScoreCard.q.Tourney == tourney).count()
	def totalGamesPlayedForPlayers(self, season):
		# returns a tuple of values
		TPQ = "select PlayerID, count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		TPQ += "season = '" + season + "' ) group by PlayerID"
		return	sqlhub.processConnection.queryAll(TPQ)
	def totalGamesPlayedForPlayersToDate(self, tno, season):
		# returns a tuple of values
		TPQ = "select PlayerID, count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		TPQ += "season = '" + season + "' and TourneyNumber <= '" + tno + "' ) group by PlayerID"
		return	sqlhub.processConnection.queryAll(TPQ)

	def totalGamePointsForPlayers(self, season):
		# returns a tuple of values
		TGPQ = "select PlayerID, sum(GamePoints) from ScoreCard where TourneyID in (select TourneyID from Tourney "
		TGPQ += " where season = '" + season +"' ) group by PlayerID"
		return sqlhub.processConnection.queryAll(TGPQ)
	def totalGamesWonForPlayers(self, season):
		TGWQ = "select PlayerID, sum(GamesWon) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		TGWQ += "season = '" + season + "' ) group by PlayerID"
		return sqlhub.processConnection.queryAll(TGWQ)


		# TPQ = "select PlayerID, count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney where season = '2019-20' ) group by PlayerID"
		# TGPQ = "select PlayerID, sum(GamePoints) from ScoreCard where TourneyID in (select TourneyID from Tourney where season = '2019-20' ) group by PlayerID"
		# TGWQ = "select PlayerID, sum(GamesWon) from ScoreCard where TourneyID in (select TourneyID from Tourney where season = '2019-20' ) group by PlayerID"
		# # get the raw data from the database
		# tPlayed = sqlhub.processConnection.queryAll(TPQ)
		# tGamePoints = sqlhub.processConnection.queryAll(TGPQ)
		# tGamesWon = sqlhub.processConnection.queryAll(TGWQ)
	def totalTourneysPlayedForPlayersToDate(self, tno, season):
		# returns a tuple of values
		TPQ = "select PlayerID, count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		TPQ += "season = '" + season + "' and TourneyNumber <= '" + tno + "' ) group by PlayerID"
		return	sqlhub.processConnection.queryAll(TPQ)

	def totalGamePointsForPlayersToDate(self, tno, season):
		# returns a tuple of values
		TGPQ = "select PlayerID, sum(GamePoints) from ScoreCard where TourneyID in (select TourneyID from Tourney "
		TGPQ += " where season = '" + season + "' and TourneyNumber <= '" + tno + "' ) group by PlayerID"
		return sqlhub.processConnection.queryAll(TGPQ)

	def totalGamesWonForPlayersToDate(self, tno, season):
		TGWQ = "select PlayerID, sum(GamesWon) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		TGWQ += "season = '" + season + "' and TourneyNumber <= '" + tno + "' ) group by PlayerID"
		return sqlhub.processConnection.queryAll(TGWQ)

	def cashSummaryForPlayers(self, tno, season):
		# returns a tuple of results tno = tourney number with season
		CSQ = "select PlayerID, sum(Cash) from scorecard "
		CSQ += "where cash > 0 and "
		CSQ += "scorecard.TourneyID in (select tourney.TourneyID from tourney where season = "
		CSQ += "'" + season + "' and tourneyNumber <= " + tno + ")"
		CSQ += " GROUP BY PlayerID HAVING SUM(Cash) > 0 ORDER BY SUM(Cash) DESC"
		print ('CSQ: ', CSQ)
		return sqlhub.processConnection.queryAll(CSQ)
	def playerCashCount(self, tno, season):
		# return tuple of results
		PCQ = "SELECT PlayerID, Count(*) FROM ScoreCard "
		PCQ += " where ScoreCard.TourneyID IN (select TourneyID from Tourney where season = '"
		PCQ += season + "' and tourneyNumber <= " + tno + " ) GROUP BY PlayerID ORDER BY PlayerID"
		print ('PCQ: ',PCQ)
		return sqlhub.processConnection.queryAll(PCQ)

		# # NOTE: use of slqhub.processConnction to run raw queries
		# #  select PlayerID, SUM(Cash) from ScoreCard where ScoreCard.TourneyID in (select Tourney.TourneyID from Tourney where season = '2019-20')
		# #  GROUP BY PlayerID HAVING SUM(Cash) > 0 ORDER BY SUM(Cash) DESC
		# cashSummaryQuery = "SELECT PlayerID, SUM(Cash) from ScoreCard "
		# cashSummaryQuery = cashSummaryQuery + "where ScoreCard.TourneyID IN (SELECT Tourney.TourneyID FROM Tourney where Season = "
		# cashSummaryQuery = cashSummaryQuery + "'" + cfg.season + "')"
		# cashSummaryQuery = cashSummaryQuery + " GROUP BY PlayerID HAVING SUM(Cash) > 0 ORDER BY SUM(Cash) DESC"
		# print (cashSummaryQuery)
		# cashSummaryRows = sqlhub.processConnection.queryAll(cashSummaryQuery)
		# print(cashSummaryRows)
		# playerCountQuery = """SELECT PlayerID, Count(*) FROM ScoreCard\
		#  where ScoreCard.TourneyID IN (select Tourney.TourneyID from Tourney where season = '2019-20')\
		#  GROUP BY PlayerID ORDER BY PlayerID"""
		# playerCountRows = sqlhub.processConnection.queryAll(playerCountQuery)
	def qtrDropCount (self, season, qtrNumber, tourneyNumber):
		# return tuple of results
		# TODO: make the quarter computation depend on an incoming parameter
		lower = 1 + (qtrNumber - 1) * 9
		upper = tourneyNumber
		QDQ = "select PlayerID, GamePoints from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		QDQ += "season = '" + season + "' and TourneyNumber between " + str(lower) +" and " + str(upper)
		QDQ += ") order by PlayerID, GamePoints asc"
		return sqlhub.processConnection.queryAll(QDQ)
	def qtrEntryCount (self, season, qtrNumber, tourneyNumber):
		# season is a string like '2019-20' and qtrNumber is an integer
		# return tuple of results
		lower =  1 + (qtrNumber - 1) * 9
		upper = tourneyNumber
		print ('Lower;;Upper::', lower, upper)
		qtrEQ = "select PlayerID, sum(GamePoints) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		qtrEQ += "season = '" + season + "' and TourneyNumber between " + str(lower) + " and " + str(upper)
		qtrEQ += ") group by PlayerID order by sum(GamePoints) desc"
		print ('qtrEQ: ', qtrEQ)
		return sqlhub.processConnection.queryAll(qtrEQ)
		# # total up all entries
		# qtrEQ = "select PlayerID, sum(GamePoints) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		# qtrEQ += "season = '2019-20' and TourneyNumber between (1 + ("
		# qtrEQ += str(qtrNumber) + " - 1)* 9) and (9 + ("
		# qtrEQ += str(qtrNumber) + " -1) * 9))"
		# qtrEQ += " group by PlayerID order by sum(GamePoints) desc"
	def qtrPlayerEntries (self, season, qtrNumber, tourneyNumber):
		# season is a string like '2019-20' and qtrNumber is an integer
		lower =  1 + (qtrNumber - 1) * 9
		upper = tourneyNumber
		print ('Lower: Upper: ', lower, upper)
		PCTQ = "select PlayerID, count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		PCTQ += "season = '" + season + "' and TourneyNumber between " + str(lower) + " and " + str(upper)
		PCTQ += ") group by PlayerID order by sum(GamePoints)"
		print ('PCTQ: ', PCTQ)
		return sqlhub.processConnection.queryAll(PCTQ)

		# # total entries per player
		# playerCTQ = "select PlayerID, count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		# playerCTQ += "season = '2019-20' and TourneyNumber between (1 + ("
		# playerCTQ += str(qtrNumber) + " - 1)* 9) and (9 + ("
		# playerCTQ += str(qtrNumber) + " -1) * 9))"
		# playerCTQ += " group by PlayerID"
	def qtrTotalAllPlayed(self, season, qtrNumber, tourneyNumber):
		# returns tuple of results
		# season is string like '2019-20' and qtrNumber is integer
		lower =  1 + (qtrNumber - 1) * 9
		upper = tourneyNumber

		QCQ = "select count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		QCQ += "season = '" + season + "' and TourneyNumber between "
		QCQ += str(lower) + " and " + str(upper) +")"
		print('QCQ: ', QCQ)
		return sqlhub.processConnection.queryAll(QCQ)

		# total all entries by all players
		# qtrCountQ = "select count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		# qtrCountQ += "season = '2019-20' and TourneyNumber between (1 + ("
		# qtrCountQ += str(qtrNumber) + " - 1)* 9) and (9 + ("
		# qtrCountQ += str(qtrNumber) + " -1) * 9))"
	def nat36Results(self, tno, season):
		# returns tuple of results
		# sum game points so far up to in including tourneyNumber (tno)
		# season is like '2019-20'
		R36Q = "select PlayerID, sum(GamePoints) from ScoreCard where GamePoints > 11 AND  TourneyID in  "
		R36Q += "(select TourneyID from Tourney where season = '" + season + "' "
		R36Q += "AND tourneyNumber <= " + tno + " ) group by PlayerID order by Sum(GamePoints) desc"
		# print ('R26Q: ',R36Q)
		return sqlhub.processConnection.queryAll(R36Q)

		# rows36Query = "select PlayerID, sum(GamePoints) from ScoreCard where GamePoints > 11 AND  TourneyID in  "
		# rows36Query += "(select TourneyID from Tourney where season = '" + cfg.season + "' "
		# rows36Query += "AND Tourney.TourneyNumber BETWEEN 1 and 45) group by PlayerID order by Sum(GamePoints) desc"
	def nat45Results(self, season):
		# returns tuple of results
		# no need for any specific tourney number; no need to sum; only ever two tourneys for 40-45
		# season is like '2019-20'
		R45Q = "select PlayerID, GamePoints, TourneyNumber from ScoreCard, Tourney where "
		R45Q += "ScoreCard.TourneyID = Tourney.TourneyID and season = '" + season + "' and TourneyNumber between 40 and 45"
		R45Q += " order by PlayerID"
		return sqlhub.processConnection.queryAll(R45Q)

		# rows45Query = "select PlayerID, GamePoints, TourneyNumber from ScoreCard, Tourney where "
		# rows45Query += "ScoreCard.TourneyID = Tourney.TourneyID and season = '2019-20' and TourneyNumber between 40 and 45"

	def countTourneys(self, tno, season):
		# return tuple of results
		# season is like '2019-20'
		TCQ = "select PlayerID, count(TourneyID) from ScoreCard where TourneyId in (select TourneyID from "
		TCQ += "Tourney where Season = '" + season +"' and tourneynumber <= " + tno + ") group by PlayerId order by PlayerID"
		return sqlhub.processConnection.queryAll(TCQ)

		# tourneyCountQuery = "select PlayerID, count(TourneyID) from ScoreCard where TourneyId in (select TourneyID from "
		# tourneyCountQuery += "Tourney where Season = '2019-20') group by PlayerId order by PlayerID"
		# self.tourneyCountDict = { x[0]:x[1] for x in sqlhub.processConnection.queryAll(tourneyCountQuery) }
	def getIndividualResults(self,season):
		# return tuple of results
		# season is like '2019-20'
		IQ = "select * from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		IQ += " season = '" + season + "' and TourneyNumber between 1 and 36) order by PlayerID"
		# IQ below returned pid with results in scorecard 41/42
		# IQ = "select * from ScoreCard where PlayerID in (select Distinct PlayerID  from ScoreCard "
		# IQ += "where TourneyID in (select TourneyID from Tourney where season = '" + season + "' "
		# IQ += "and TourneyNumber between 1 and 36)) order by PlayerID"
		return sqlhub.processConnection.queryAll(IQ)

		# individualQ = "select * from ScoreCard where PlayerID in (select Distinct PlayerID  from ScoreCard "
		# individualQ += "where TourneyID in (select TourneyID from Tourney where season = '2019-20' "
		# individualQ += "and TourneyNumber between 1 and 36)) order by PlayerID"
	def getPlayersPerTourney(self, season):
		# return tuple of results
		# season like '2019-20'
		PPTQ = "select TourneyID, count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney "
		PPTQ += "where season = '" + season + "' and TourneyNumber between 1 and 36) group by TourneyID"
		return sqlhub.processConnection.queryAll(PPTQ)

		# playersPerTnyQ = "select TourneyID, count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney "
		# playersPerTnyQ += "where season = '2019-20' and TourneyNumber between 1 and 36) group by TourneyID"
		# playersPerTourney = sqlhub.processConnection.queryAll(playersPerTnyQ)
	def getSkunks(self, tno, season):
		# return tuple of results
		# tno is str(tourneynumber)
		# season like '2019-20'
		# TODO: add season for which to get the skunks
		SKQ = "select PlayerID, sum(SkunksGiven), sum(SkunksTaken), sum(SkunksGiven) - sum(SkunksTaken) from ScoreCard"
		SKQ += " where ScoreCard.TourneyID in (select Tourney.TourneyID from Tourney "
		SKQ += " where season = '" + season + "' and TourneyNumber <= " + tno + " ) group by PlayerID"
		return sqlhub.processConnection.queryAll(SKQ)

	# skunkQuery = "select PlayerID, sum(SkunksGiven), sum(SkunksTaken), sum(SkunksGiven) - sum(SkunksTaken) from ScoreCard where ScoreCard.TourneyID in (select Tourney.TourneyID from Tourney where TourneyNumber <= 14) group by PlayerID"
		# skunkRows = sqlhub.processConnection.queryAll(skunkQuery)
	def getSeasonTourneyIDs(self,season):
		# returns a result tuple
		TIDQ = "select distinct TourneyID from ScoreCard where TourneyID in (select TourneyID from Tourney "
		TIDQ += " where Season = '" + season + "' )"
		return  sqlhub.processConnection.queryAll(TIDQ)

