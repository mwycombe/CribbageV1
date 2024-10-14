#individualstatsreport.py
# 7/22/2020 updated to cribbageconfig and cribbagereport and cribbagetso
# 2/24/2020
# This is the report for individual stats, one per page
#
# note need to us '{formatspec}.format(values) to 'almost' get things aligned
# along with non-proportional Courier font
#
# TODO: Handle tied positions in addLineToReport

import cribbageconfig as cfg
import cribbagereport as rpt
from scorecard import ScoreCard
from tourney import Tourney
from player import Player
from club import Club
from accessResults import AccessResults
from accessTourneys import AccessTourneys
from accessPlayers import AccessPlayers
from accessClubs import AccessClubs
from cribbagetso import *

# system imports
import os, sys
from fpdf import FPDF
from itertools import *

class IndividualStatsReport(object):
	def __init__(self):
		# stats list is list with list for each player's individual stats
		# TODO: first is a single page report for a single player
		self.rptData = BuildReportData()
		# rpt.reportLineNumber = 0
		os.chdir(cfg.reportDirectory)
		print('Report Dir: ', os.getcwd())
		self.reportName = rpt.reportSeason + '-Week-' + str(rpt.tourneyRecord.TourneyNumber) + '-IndivStats.pdf'

		# rpt.rptData will be a list of lists. each interior list will be the stats for the individual
		#  [ [playerId , [No plyrs, Gm Pts, Gm won, spread, Natl Pts, Win/Loss, Game prts cash Taken, Given, Net]  ,
		#  [ [playerId , [No plyrs, Gm Pts, Gm won, spread, Natl Pts, Win/Loss, Game prts cash Taken, Given, Net]  ]
		# or it may be a directory of lists, keyed by Playerid.
		# for statPage in rpt.reportData:
		# 	self.buildAPage(statPage)

		self.pdf = FPDF(format='Letter')  # default mm units
		self.pdf.l_margin = 20
		self.pdf.r_margin = 25
		self.pdf.t_margin = 25
		self.pdf.b_margin = 50

		self.playerNames = []

		for stats in self.rptData.lines_for_pid:
			self.pdf.add_page()  # leave portrait as default
			print('newpage: ', stats)
			rpt.tourneyCount = 0
			self.buildAPage(stats)
		self.printReport()
	def buildAPage(self, stats):
		rpt.reportLineNumber = 0
		self.reportTitle = 'INDIVIDUAL STATISTICS'
		print ('stats[0][0][1]: ', stats[0][0][1])
		self.playerName = stats[0][0][1]
		self.clubName = cfg.clubName
		self.playedOn = 'Played:'
		self.clubNoLiteral = 'Club No:'
		self.clubNumber = str(cfg.clubNumber)
		self.clubName = cfg.clubName
		self.clubLocation = cfg.clubLocation
		self.clubSeason = cfg.season + ' Season'
		self.clubLiteral = 'Club'
		self.charterLiteral = 'Charter No:'
		self.afterHdr = 'After  ' + str(rpt.tourneyNumber) + '  Tournaments'
		self.totalLiteral = 'Total'
		self.averagesLiteral = 'AVERAGES'
		self.tnyLiteral = 'Tny'
		self.reglLiteral = 'Regl'
		self.natlLiteral = 'Natl'
		self.tourneysLiteral = 'Tourneys'
		self.nameLiteral = 'Name'
		self.ptsLiteral = 'Pts'
		self.noLiteral = 'No.'
		self.plyrLiteral = 'Plyr'
		self.gmLiteral = 'Gm'
		self.gmsLiteral = 'Gms'
		self.ptsLiteral = 'Pts'
		self.sprdLiteral = 'Sprd'
		self.winLiteral = 'Win/'
		self.lossLiteral = 'Loss'
		self.wonLiteral = 'Won'
		self.cashLiteral = 'Cash'
		self.skunksLiteral = 'Skunks'
		self.takenLiteral = 'Taken'
		self.givenLiteral = 'Given'
		self.netLiteral = 'Net'
		self.gameLiteral = 'Game'
		self.title0 = ' '  # a blank cell spacer

		# self.pdf = FPDF(format='Letter')  # default mm units
		# self.pdf.l_margin = 20
		# self.pdf.r_margin = 25
		# self.pdf.t_margin = 25
		# self.pdf.b_margin = 50
		#
		# self.pdf.add_page()  # leave portrait as default

		# compute effective width and height, and text height from font size.
		self.pdf.set_font('Courier', '', 10)
		self.epw = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
		self.eph = self.pdf.h - self.pdf.t_margin - self.pdf.b_margin
		self.texth = self.pdf.font_size
		self.reportNumber = str(rpt.tourneyRecord.TourneyNumber)
		self.playedOnDate = rpt.tourneyDate

		self.setCell(0, self.playerName)
		self.setCell(55, self.clubName)
		self.pdf.ln(2 * self.texth)

		self.setCell(0, self.reportTitle)
		self.setCell(51, self.clubSeason)
		self.setCell(86, self.clubNoLiteral)
		self.setCell(110, self.clubNumber)
		self.pdf.ln(2 * self.texth)

		self.setCell(80, self.averagesLiteral)
		self.pdf.ln(2 * self.texth)

		self.setCell(0, self.tnyLiteral)
		self.setCell(11, self.noLiteral)
		self.setCell(25, self.gmLiteral)
		self.setCell(37, self.gmsLiteral)
		self.setCell(60, self.natlLiteral)
		self.setCell(78, self.winLiteral)
		self.setCell(93, self.gameLiteral)
		self.setCell(118, self.skunksLiteral)
		self.setCell(133, self.skunksLiteral)
		self.setCell(150, self.netLiteral)
		self.pdf.ln(self.texth)

		self.setCell(0, self.noLiteral)
		self.setCell(10, self.plyrLiteral)
		self.setCell(24, self.ptsLiteral)
		self.setCell(37, self.wonLiteral)
		self.setCell(48, self.sprdLiteral)
		self.setCell(60, self.ptsLiteral)
		self.setCell(78, self.lossLiteral)
		self.setCell(93, self.ptsLiteral)
		self.setCell(105, self.cashLiteral)
		self.setCell(119, self.takenLiteral)
		self.setCell(133, self.givenLiteral)
		self.setCell(149, self.skunksLiteral)
		self.pdf.ln(self.texth)

		self.pdf.set_line_width(0.25)

		self.setLine(0, 7)
		self.setLine(11, 18)
		self.setLine(25, 31)
		self.setLine(38,44)
		self.setLine(49, 57)
		self.setLine(61, 68)
		self.setLine(79,88)
		self.setLine(95, 101)
		self.setLine(107, 114)
		self.setLine(120, 129)
		self.setLine(135, 144)
		self.setLine(151, 160)
		self.pdf.ln(self.texth)

		for rline in stats:
			self.addLineToReport(rline)

	def setLine(self, start, finish):
		# draw a line from start to finish
		self.pdf.line(self.pdf.l_margin + start,
		              self.pdf.get_y(),
		              self.pdf.l_margin + finish,
		              self.pdf.get_y()
		              )
		return


		# for sline in stat:
		#     self.addStatLineToReport(rline)
	def addLineToReport(self, aline):
		rpt.reportLineNumber += 1
		rline =  (*aline[0],*aline[1:])
		print ('rline: ', rline)
		self.setCell(0, '{:2n}'.format(rline[0]) + '.')
		if not(rline[2] == 0 and  rline[3] == 0 and rline[4] == 0):
			rpt.tourneyCount += 1
			print ('rpt.tourneyCount: ', rpt.tourneyCount)
			self.setCell(12, '{:2n}'.format(rpt.playersTourneyDict[cfg.tourneyRefx[rline[0]]]))
			self.setCell(25, '{:2n}'.format(rline[2]))
			self.setCell(40, '{:1}'.format(rline[3]))
			self.setCell(48, '{:4n}'.format(rline[4]))
			if rline[2] > 11:
				self.setCell(62, '{:2n}'.format(rline[2]))
			# win/tourney calc
			if rpt.tourneyCount > 0:
				self.setCell(76, '{:6.3f}'.format( rline[10] / (9 * rpt.tourneyCount)))
			# points/tourney calc
				self.setCell(94, '{:.1f}'.format ( rline[9]/rpt.tourneyCount ))
			self.setCell(105, '{:3n}'.format(rline[11]))
			self.setCell(124, '{:2n}'.format(rline[6]))
			self.setCell(138, '{:2n}'.format(rline[7]))
			self.setCell(153, '{:3n}'.format(rline[6] - rline[7]))
		self.pdf.ln(self.texth)

		# if rpt.reportLineNumber % 5 == 0: self.pdf.ln(self.texth)


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
	def __init__(self):
		# lineNumber = 0
		#     print (aLine)
		# individualQ = "select * from ScoreCard where PlayerID in (select Distinct PlayerID  from ScoreCard "
		# individualQ += "where TourneyID in (select TourneyID from Tourney where season = '2019-20' "
		# individualQ += "and TourneyNumber between 1 and 36)) order by PlayerID"
		# individualResults = sqlhub.processConnection.queryAll(individualQ)
		individualResults = cfg.ar.getIndividualResults(cfg.season)
		print (' len indiv results: ', len(individualResults))
		# print ('individualResults', individualResults)
		self.lines_for_pid = []
		# playersPerTnyQ = "select TourneyID, count(*) from ScoreCard where TourneyID in (select TourneyID from Tourney "
		# playersPerTnyQ += "where season = '2019-20' and TourneyNumber between 1 and 36) group by TourneyID"
		# playersPerTourney = sqlhub.processConnection.queryAll(playersPerTnyQ)
		playersPerTourney = cfg.ar.getPlayersPerTourney(cfg.season)
		rpt.playersTourneyDict = { k:v for k,v in playersPerTourney }   # keyed by tourneyid
		print ('playerspertny: ', rpt.playersTourneyDict)
		listOfPids = [x[2] for x in individualResults]
		setOfPids = set(listOfPids)
		print ('setOfPids:', setOfPids)
		self.setOfTids = cfg.ar.getSeasonTourneyIDs(cfg.season)
		print('setOfTids: ', self.setOfTids)
		for x in self.setOfTids:
			print ('tid: ', x, x[0])
		print ('tXref:', cfg.tourneyXref)       # this is tournid : tourneynumber
		self.maxTourneyNumber = max( list([cfg.tourneyXref[x[0]] for x in self.setOfTids if cfg.tourneyXref[x[0]] < 40]))
		print ('Max tourney number:', self.maxTourneyNumber)
		self.blankGifLines = list(zip(range(1, self.maxTourneyNumber + 1), [list(repeat(0, 8))] * self.maxTourneyNumber))
		self.blankGifList = list((x[0], *x[1]) for x in self.blankGifLines)
		print ('self.blankGifList: ', self.blankGifList)
		for pid in setOfPids:
			gif = [ x for x in individualResults if x[2] == pid]
			# drop the scorecard id from gif and resolve TourneyNumber and PlayerName
			# gif = [ (cfg.tourneyXref[ x[1]], cfg.playerXref[ x[2]], x[3:]) for x in gif  ]
			listGif = [ (cfg.tourneyXref[ x[1]], cfg.playerXref[ x[2]], *(x[3:])) for x in gif  ]
			sortedGif = sorted(listGif, key=lambda k: k[0])
			# merge in the tourney lines with the blank lines
			print ('len, sortedGif: ', len(sortedGif), sortedGif)

			temp1 = []
			# print ('temp1: ', temp1)
			# y = 0
			# for t in sortedGif:
			# 	print ('gifline: ', t)
			# print ('y: ', y)
			for x in self.blankGifList:
				temp1.append(list(x))
			y = 0
			for z in sortedGif:
				print ('z: ', z)
				while temp1[y][0] < z[0]:
					# always plug in the name for the report writing phase
					temp1[y][1] = z[1]
					y += 1
					continue
				# print ('x: ',x)
				# print ('sortedGif[y]: ', sortedGif[y])
				# print ('x[0]: ', x[0])
				temp1[y] = z
				y += 1



			print ('temp1:', temp1)

			cumGamePts = list(accumulate(x[2] for x in temp1))
			cumGamesWon = list(accumulate(x[3] for x in temp1))
			cumCash = list(accumulate(x[5] for x in temp1))


			temp2 = list(zip( temp1, cumGamePts, cumGamesWon, cumCash))
			for t in temp2:
				print ('temp2 line: ', t)
			# testp = [ (x[0], x[1][0], cfg.tournyXref[ x[1][1]], x[1][2], x[2], x[3], x[4]) for x in tfp1]
			# print ('testp:', testp)
			# temp3 = list( (*x[0], x[1], x[2], x[3]) for x in temp2)
			# for t in tfp2:
			# 	print ('tfp2 line: ', t)
			self.lines_for_pid.append( temp2)
			# print ('lines_4_pid: ', self.lines_for_pid)
			# temp_for_pid = list(zip(range(1, len(gfp1) + 1), gfp1, cpf1, cgf1, ccf1))
			# temp_for_pid = [ (x[0], x[1][0], cfg.tourneyXref[ x[1][1] ] , cfg.playerXref[ x[1][2] ], x[1][3], x[1][4], x[1][5], x[1][6], x[1][7], x[1][8], x[1][9]) for x in temp_for_pid ]
			# print ('temp_4_pid: ', temp_for_pid)
			# self.lines_for_pid.append (list( [(x[0], x[1][1], x[1][2], x[1][3], x[1][4], x[1][5], x[1][6], x[1][7], x[1][8], x[1][8] - x[1][7], x[2], x[3], x[4]) for x in tfp3 ]  ))
		# print ('lines_for_pid: ', self.lines_for_pid)
		for p in self.lines_for_pid:
			print ('pid_line: ', p)
if __name__ == '__main__':
	print('Create tourney report')

	#############################################
	# hardwire cfg for testing                  #
	cfg.appTitle = 'Reports Testing'  #
	cfg.clubNumber = 100  #
	cfg.season = '2019-20'  #
	cfg.clubName = 'Peggers'  #
	rpt.tourneyDate = '2019-11-19'  #
	rpt.tourneyRecordId = 12  #
	rpt.tourneyNumber = 10  #

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

	# clubXrefQuery = "select PlayerID, ClubNumber from Player, Club where Player.ClubID = Club.ClubID "
	# cfg.clubXref = { x[0]:x[1] for x in sqlhub.processConnection.queryAll(clubXrefQuery) }

	cfg.clubXref = {x[0]: x[1] for x in cfg.ac.clubXref()}

	cfg.clubRecord = Club.get(1)
	cfg.clubId = cfg.clubRecord.id

	tourneyXrefQuery = "select tourneyID, TourneyNumber from Tourney where season = '2019-20'"
	tourneyXrefList = sqlhub.processConnection.queryAll(tourneyXrefQuery)
	cfg.tourneyXref = { k:v for k,v in tourneyXrefList }
	cfg.tourneyRefx = { v:k for k, v in cfg.tourneyXref.items() }

	club100 = list(Club.select(Club.q.clubNumber == 100))[0]
	cfg.reportDirectory = club100.reportDirectory
	rpt.tourneyRecord = cfg.at.getTourneyByNumber(rpt.tourneyNumber)[0]

	print('rpt.tourneyRecord: ', rpt.tourneyRecord)
	# reportData = BuildReportData()

	individualstatsReport = IndividualStatsReport()
	individualstatsReport.printReport()

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
