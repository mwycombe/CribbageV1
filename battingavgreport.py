# battingavgreport.py
# 2/24/2020
# 7/22/2020 updated to use cribbageconfig and cribbagereport
# This is the report for national rating
#
# note need to us '{formatspec}.format(values) to 'almost' get things aligned
# need non-proporional font (Courier) for easy alignment
#
# TODO: Handle tied positions in addLineToReport

import cribbageconfig as cfg
import cribbagereport as rpt
from scorecard import ScoreCard
from tourney import Tourney
from player import Player
from accessResults import AccessResults
from accessTourneys import AccessTourneys
from accessPlayers import AccessPlayers
from accessClubs import AccessClubs
from cribbagetso import *

# system imports
import os, sys
from fpdf import FPDF


class BattingAvgReport(object):
	def __init__(self):
		# tourney passed in is the tourney object in rpt for the tourney being reported on
		self.rptData = BuildReportData()
		rpt.reportLineNumber = 0
		os.chdir(cfg.reportDirectory)
		print('Report Dir: ', os.getcwd())
		self.reportName = rpt.reportSeason + '-Week-' + str(rpt.tourneyRecord.TourneyNumber) + '-BattingAvg.pdf'
		self.reportTitle = 'BATTING AVERAGES For'
		self.playedOn = 'Played:'
		self.clubNoLiteral = 'Club No.'
		self.clubNumber = str(cfg.clubNumber)
		self.clubName = cfg.clubName
		self.clubLocation = 'Napa'
		self.clubSeason = cfg.season + ' Season'
		self.clubLiteral = 'Club'
		self.charterLiteral = 'Charter No:'
		self.afterHdr = 'After  ' + str(rpt.tourneyNumber) + '  Tournaments'
		self.nameLiteral = 'Name'
		self.gmsLiteral = 'Gms'
		self.winlossLiteral = 'W/L'
		self.averageLiteral = 'Average Game Points'
		self.gameLiteral = 'Game'
		self.playerLiteral = 'Player'
		self.plydLiteral = 'Plyd'
		self.wonLiteral = 'Won'
		self.averLiteral = 'Aver'
		self.tourLiteral = 'Tour'
		self.ptsLiteral = 'Pts'
		self.noLiteral = 'No.'
		self.playedLiteral = 'Played'
		self.withoutLiteral = 'Players wihout enough tourneys:'
		self.mustLiteral = '(Must play in 1/2 of tourneys since joining club or played in ten or more)'
		self.tbd = 'To be implemented in the future'
		self.title0 = ' '  # a blank cell spacer

		self.pdf = FPDF(format='Letter')  # default mm units
		self.pdf.l_margin = 12
		self.pdf.r_margin = 12
		self.pdf.t_margin = 25
		self.pdf.b_margin = 50

		self.pdf.add_page()  # leave portrait as default
		# compute effective width and height, and text height from font size.
		self.pdf.set_font('Courier', '', 10)
		self.epw = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
		self.eph = self.pdf.h - self.pdf.t_margin - self.pdf.b_margin
		self.texth = self.pdf.font_size
		self.reportNumber = str(rpt.tourneyRecord.TourneyNumber)
		self.playedOnDate = rpt.tourneyDate

		self.setCell(0, self.reportTitle)
		self.setCell(47, self.clubName)
		self.setCell(129, self.clubNoLiteral)
		self.setCell(148, self.clubNumber)
		self.pdf.ln(self.texth)

		self.setCell(0, self.clubLocation)
		self.pdf.ln(2 * self.texth)

		self.setCell(0, self.afterHdr)
		self.setCell(129, self.clubSeason)
		self.pdf.ln(2 * self.texth)

		self.setCell(63, self.gmsLiteral)
		self.setCell(73, self.gmsLiteral)
		self.setCell(87, self.winlossLiteral)
		self.setCell(105, self.averageLiteral)
		self.setCell(157, self.noLiteral)
		self.setCell(167, self.gameLiteral)
		self.pdf.ln(self.texth)

		self.setCell(0, self.playerLiteral)
		self.setCell(63, self.plydLiteral)
		self.setCell(73, self.wonLiteral)
		self.setCell(87, self.averLiteral)
		self.setCell(105, self.playerLiteral)
		self.setCell(157, self.tourLiteral)
		self.setCell(167, self.ptsLiteral)
		self.pdf.ln(self.texth)

		self.pdf.set_line_width(0.25)
		self.setLine(0, 42)
		self.setLine(64, 72)
		self.setLine(74, 80)
		self.setLine(88,95)
		self.setLine(106, 150)
		self.setLine(158, 164)
		self.setLine(168, 174)
		# self.pdf.line(self.pdf.l_margin, self.pdf.get_y(),
		#               self.pdf.l_margin + self.epw, self.pdf.get_y()
		#               )
		self.pdf.ln(2 * self.texth)

		for rline in self.rptData.rptLines:
		    self.addLineToReport(rline)

		#   add trainling information lines
		self.pdf.ln(2 * self.texth)
		self.setCell(0, self.withoutLiteral)
		self.pdf.ln(self.texth)
		self.setCell(0, self.mustLiteral)
		self.pdf.ln(self.texth)
		self.setCell(0, self.tbd)
		self.pdf.ln(self.texth)

		self.printReport()

	def addLineToReport(self, aLine):

		rpt.reportLineNumber += 1
		# print ('aLine ', aLine[0][0], aLine)
		# won = aLine[3][1]
		# played = 9 * aLine[1][1]
		# lost = played - won
		# winLoss = won / played
		# print ('aLine: ', aLine)
		# aLine format ( line# , (pid, gms, won, w/l avge), (pid, touneys, pts avge) )

		# self.setCell(2, '{:2n}'.format(aLine[0]) + '.')
		if aLine[0] > 0:
			self.setCell(2,'{:2n}'.format(aLine[0]) + '.')
		else:
			self.setCell(2, ' ')

		self.setCell(10, cfg.playerXref[aLine[1][0] ])
		self.setCell(63, '{:3n}'.format(aLine[1][1]))
		self.setCell(73, '{:3n}'.format(aLine[1][2]))
		self.setCell(85, '{:.3f}'.format(aLine[1][3]))

		# self.setCell(105, '{:2n}'.format(aLine[2]) + '.')
		if aLine[2] > 0:
			self.setCell(105,'{:2n}'.format(aLine[2]) + '.')
		else:
			self.setCell(105, ' ')

		self.setCell(112, cfg.playerXref[aLine[3][0]])
		self.setCell(156, '{:2n}'.format(aLine[3][1]))
		self.setCell(167, '{:4.1f}'.format(aLine[3][2]))

		self.pdf.ln(self.texth)
		if rpt.reportLineNumber % 5 == 0: self.pdf.ln(self.texth)

	def setLine(self, start, finish):
		# draw a line from start to finish
		self.pdf.line(self.pdf.l_margin + start,
		              self.pdf.get_y(),
		              self.pdf.l_margin + finish,
		              self.pdf.get_y()
		              )
		return
	def setCell(self, o, text):
		# o is offset from l_margin
		# l is literal to display in cell
		self.pdf.set_x(self.pdf.l_margin + o)
		self.pdf.cell(self.pdf.get_string_width(text), 0, text)


	def printReport(self):
		# set up two multi_cell columns of skunk results stored by Given and Taken
		self.pdf.close()
		self.pdf.output(self.reportName)


class BuildReportData(object):
	# creates the lines for the tourney report
	# TODO: need to limit results to tourneys-to-date in the query
	def __init__(self):
		# lineNumber = 0
		#     print (aLine)
		# TODO: Need to drop out those with less than the necessary number of tourneys
		# TODO: Add duplicate processing
		# TODO: Add tourneyNumber <= tno to selection for results records to be processed for each tourney
		#
		# TPQ = "select PlayerID, count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney where season = '2019-20' ) group by PlayerID"
		# TGPQ = "select PlayerID, sum(GamePoints) from ScoreCard where TourneyID in (select TourneyID from Tourney where season = '2019-20' ) group by PlayerID"
		# TGWQ = "select PlayerID, sum(GamesWon) from ScoreCard where TourneyID in (select TourneyID from Tourney where season = '2019-20' ) group by PlayerID"
		# # get the raw data from the database
		# tPlayed = sqlhub.processConnection.queryAll(TPQ)
		# tGamePoints = sqlhub.processConnection.queryAll(TGPQ)
		# tGamesWon = sqlhub.processConnection.queryAll(TGWQ)
		tPlayed = cfg.ar.totalTourneysPlayedForPlayersToDate(str(rpt.tourneyNumber), cfg.season)
		tGamePoints = cfg.ar.totalGamePointsForPlayersToDate(str(rpt.tourneyNumber), cfg.season)
		tGamesWon = cfg.ar.totalGamesWonForPlayersToDate(str(rpt.tourneyNumber), cfg.season)
		# build the won/played average
		# combine tourneys played and games won
		tPlayedWon = list ( zip(tPlayed, tGamesWon))
		tPWAvge = [ (x[0][0], 9 * x[0][1], x[1][1], x[1][1]/ (9 * x[0][1]) ) for x in tPlayedWon]
		sortedtPWAvge = sorted(tPWAvge, key=lambda v: v[3], reverse=True)

		# add line count via range
		plydRptLines = list(zip(range(1, len(sortedtPWAvge) + 1), sortedtPWAvge))

		# print ('tCombo: ', tCombo)
		print ('tPlayed: ', tPlayed)
		print ('tPlayedWon:', tPlayedWon)
		print ('tGamePoints: ',tGamePoints)
		print ('plydRptLines: ', plydRptLines)
		# build the pts avge lines
		tPlayedPoints = list (zip( tPlayed, tGamePoints))
		print ('tPlayedPoints: ', tPlayedPoints)
		tPP = [(x[0][0], x[0][1], x[1][1]) for x in tPlayedPoints]
		# print ('tPP: ', tPP)
		tPPAvge = [(x[0], x[1], x[2] /  x[1]) for x in tPP]
		sortedtPPAvge = sorted(tPPAvge, key=lambda v: v[2], reverse=True)
		avgeRptLines = list(zip(range(1, len(tPPAvge) + 1), sortedtPPAvge))
		# handle ties in plydRptLines & avgeRptLines separately before combining
		# replace plydRptLines & avgeRptLines from tie handlers
		plydRptLines = self.handlePlydRptLineTies(plydRptLines)
		avgeRptLines = self.handleAvgeRptLinesTies(avgeRptLines)
		# finally, combine all into a single set of rptLines
		tempRptLines = list(zip(plydRptLines, avgeRptLines))
		# eliminate duplications
		self.rptLines = [ (x[0][0], x[0][1], x[1][0], x[1][1]) for x in tempRptLines]
		# print ('rptLines \n', self.rptLines)
	def handlePlydRptLineTies(self, lines):
		newPlydLines = []
		savedLine = lines[0]
		newPlydLines.append(savedLine)
		for x in range (1, len(lines)):
			tempLine = list(lines[x])
			# print ('tempLine: ', tempLine)
			if savedLine[1][3] == tempLine[1][3]:
				tempLine[0] = 0
			savedLine = tempLine
			newPlydLines.append(savedLine)
		return newPlydLines
	def handleAvgeRptLinesTies(self, lines):
		newAvgeLines = []
		savedLine = lines[0]
		newAvgeLines.append(savedLine)
		for x in range (1, len(lines)):
			tempLine = list(lines[x])
			if savedLine[1][2] == tempLine[1][2]:
				tempLine[0] = 0
			savedLine = tempLine
			newAvgeLines.append(savedLine)
		return newAvgeLines

if __name__ == '__main__':
	print('Create batting average report')

	#############################################
	# hardwire cfg for testing                  #
	cfg.appTitle = 'Reports Testing'  #
	cfg.clubNumber = 100  #
	cfg.season = '2018-19'  #
	cfg.clubName = 'Peggers'  #
	rpt.tourneyDate = '2018-09-04'  #
	rpt.tourneyRecordId = 25 #
	rpt.tourneyNumber = 1  #

	# defer getting club record until connection made
	# cfg.clubRecord = Club.get(1)                #
	# cfg.clubId = cfg.clubRecord.id              #
	#                                           #

	# open up the tso to create dbms connection
	cstring = ''
	conn = ''
	dbmsObject = TSO()

	# test ability to access players
	cfg.ap = AccessPlayers()
	cfg.at = AccessTourneys()
	cfg.ar = AccessResults()
	cfg.ac = AccessClubs()
	print('cfg.ar: ', cfg.ar)
	players = list(Player.select())
	print(players)
	cfg.playerXref = {p.id: p.LastName + ', ' + p.FirstName for p in list(Player.select())}
	cfg.playerRefx = {v: k for k, v in cfg.playerXref.items()}
	cfg.clubRecord = Club.get(1)
	cfg.clubId = cfg.clubRecord.id
	cfg.clubName = cfg.clubRecord.clubName
	cfg.clubLocation = cfg.clubLocation
	club100 = list(Club.select(Club.q.clubNumber == 100)) [0]
	cfg.reportDirectory = club100.reportDirectory
	club100 = list(Club.select(Club.q.clubNumber == 100))[0]
	rpt.tourneyRecord = cfg.at.getTourneyByNumber(rpt.tourneyNumber)[0]
	print('rpt.tourneyRecord: ', rpt.tourneyRecord)
	# reportData = BuildReportData()
	battingAvgReport = BattingAvgReport()
	# battingAvgReport.printReport()  # moved to end of init

##################################################################
#
#   Used for running GUI tests
#
# print('Count of players: ',ap.countPlayers(club999))
# countOfPlayers = ap.countPlayers(club999)
#  # get tourney record
# at = AccessTourneys()
# ar = AccessResults()
# cfg.tourneyRecord = at.getTourneyByNumber(cfg.tourneyNumber)[0]
# cfg.tourneyRecordId = cfg.tourneyRecord.id
# cfg.tourneyNumber = cfg.tourneyRecord.TourneyNumber
#
# root = tk.Tk()
# root.rowconfigure(0,weight=1)
# root.columnconfigure(0,weight=1)
# # root.columnconfigure(1,weight=1)
# # root.geometry('400x500')
# app = SampleApp(master=root)
# app.rowconfigure(0, weight=1)
# app.columnconfigure(0, weight=1)
# app.columnconfigure(1, weight=1)
# app.master.title('Result Panel 1')
# app.mainloop()
