# cashreport.py
# 7/22/2020 updated to cribbageconfig and cribbgereport and cribbagetso
# 1/23/2020
# This is the cumulative cash prizes for the season
#
# TODO: Handle tied positions in addLineToReport
# TODO: Parameterize season for SQL Select where clause
#
import cribbageconfig as cfg
import cribbagereport as rpt
from scorecard import ScoreCard
from tourney import Tourney
from player import Player
from club import Club
from accessResults import AccessResults
from accessTourneys import AccessTourneys
from accessPlayers import AccessPlayers
from cribbagetso import *

# system imports
import os, sys
from fpdf import FPDF

class CashReport(object):
	def __init__(self):
		# all static data retrieved from cfg. and rpt. variables
		rptData = BuildReportData()     # puts data directly into rpt.reportData
		rpt.reportLineNumber = 0
		print ('cfg.reportDirectory.: ', cfg.reportDirectory)
		os.chdir(cfg.reportDirectory)
		print('Report Dir: ', os.getcwd())
		self.cashReportName = rpt.reportSeason + '-Week-' + str(rpt.tourneyRecord.TourneyNumber) + '-CashReport.pdf'
		self.reportTitle = 'PRIZE WINNINGS'
		self.clubName = 'Century Peggers'
		self.clubNoLiteral = 'Club No:'
		self.clubNumber = cfg.clubNumber
		self.afterLiteral = 'After'
		self.reportNumber = str(rpt.tourneyNumber)
		self.tournamentsLiteral = 'Tournaments'
		self.season = cfg.season + ' Season'
		self.nameLiteral = 'Name'
		self.wonLiteral = 'Won'
		self.tourneysLiteral = 'Tourneys'
		self.playedLiteral = 'Played'

		self.pdf = FPDF(format='Letter')
		self.pdf.l_margin = 25
		self.pdf.r_margin = 25
		self.pdf.t_margin = 25
		self.pdf.b_margin = 50

		self.pdf.add_page()  # leave portrait as default
		# compute effective width and height, and text height from font size.
		self.pdf.set_font('Courier', '', 10)
		self.epw = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
		self.eph = self.pdf.h - self.pdf.t_margin - self.pdf.b_margin
		self.texth = self.pdf.font_size

		self.setCell(45, self.reportTitle)
		self.pdf.ln(2 * self.texth)

		self.setCell(23, self.afterLiteral)
		self.setCell(37, self.reportNumber)
		self.setCell(45, self.tournamentsLiteral)
		self.setCell(94, self.season)
		# self.setCell(112, self.seasonLiteral)
		self.pdf.ln(2 * self.texth)

		self.setCell(108, self.tourneysLiteral)
		self.pdf.ln(self.texth)

		self.setCell(34, self.nameLiteral)
		self.setCell(94, self.wonLiteral)
		self.setCell(110, self.playedLiteral)
		self.pdf.ln(2 * self.texth)

		for rline in rptData.rptLines:
			self.addLineToReport(rline)

		self.printReport()

	def addLineToReport(self, aLine):
		rpt.reportLineNumber += 1
		if aLine[0] > 0:
			self.setCell(26, str(aLine[0]))
		else:
			self.setCell(26, ' ')
		playerName = cfg.playerXref[aLine[1][0]]
		self.setCell(34, playerName)
		self.setCell(94, '{:=3n}'.format(aLine[1][1]))
		self.setCell(115, '{:=2n}'.format(aLine[1][2]))
		self.pdf.ln(self.texth)
		if rpt.reportLineNumber % 5 == 0 : self.pdf.ln(self.texth)

	def setCell(self, o, text):
		# o is offset from left margin
		# text is literal for cell
		self.pdf.set_x(self.pdf.l_margin + o)
		self.pdf.cell(self.pdf.get_string_width(text), 0, text)

	def printReport(self):
		self.pdf.close()
		self.pdf.output(self.cashReportName)

class BuildReportData(object):
	# create the lines for the cash report in rpt.reportData
	def __init__(self):
		# # NOTE: use of slqhub.prcessConnction to run raw queries
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
		# HERE'S THE ERROR. ONLY NEED CASH UP TO THE CURRENT TOURNEY
		cashSummaryRows = cfg.ar.cashSummaryForPlayers(str(rpt.tourneyNumber), rpt.reportSeason)
		playerCountRows = cfg.ar.playerCashCount(str(rpt.tourneyNumber), rpt.reportSeason)
		# print(playerCountRows)
		# product list of lists from returned rows which is tuples
		cashSummaryList = [list(x) for x in cashSummaryRows]
		playerCountDict = { k:v for (k,v) in playerCountRows}
		# append returns none but each x gets appended
		throwAway = [x.append(playerCountDict[x[0]]) for x in cashSummaryList]
		cashAndCount = cashSummaryList
		# print(cashAndCount)
		linedCashAndCount = list(zip(range(1, len(cashAndCount) + 1), cashAndCount))
		print ('linedCashandCount: ', linedCashAndCount)
		self.rptLines = self.handleTies(linedCashAndCount)
		# self.rptLines = linedCashAndCount
		# print(rpt.reportData)
	def handleTies(self, lines):
		# first have to convert tuples to lists
		newCashAndCount = []
		self.savedLine = lines[0]
		newCashAndCount.append(self.savedLine)
		for x in range(1,len(lines)):
			tempLine = list(lines[x])
			if self.savedLine[1][1] == lines[x][1][1]:
				tempLine[0] = 0
			self.savedLine = tempLine
			newCashAndCount.append(self.savedLine)
		return newCashAndCount
if __name__ == '__main__':
    print ('Create cash report')
    #############################################
    # hardwire cfg for testing                  #
    cfg.appTitle = 'Reports Testing'  #
    cfg.clubNumber = 100  #
    cfg.season = '2021-22'  #
    cfg.clubName = 'Peggers'  #
    rpt.tourneyDate = '2021-09-07'  #
    rpt.tourneyRecordId = 61 #
    rpt.tourneyNumber = 1 #
    rpt.reportSeason = '2021-22'

    # defer getting club record until connection made
    # cfg.clubRecord = Club.get(1)                #
    # cfg.clubId = cfg.clubRecord.id              #
    #                                           #

    # open up the tso to create dbms connection
    # global cstring
    # global conn
    # cstring = ''
    # conn = ''
    dbmsObject = TSO()

    # test ability to access players
    cfg.ap = AccessPlayers()
    cfg.at = AccessTourneys()
    cfg.ar = AccessResults()
    print('cfg.ar: ', cfg.ar)
    # prove we are connected to dbms
    players = list(Player.select())
    print(players)
    cfg.playerXref = {p.id: p.LastName + ', ' + p.FirstName for p in list(Player.select())}
    cfg.playerRefx = { v : k for k, v in cfg.playerXref.items() }

    clubXrefQuery = "select PlayerID, ClubNumber from Player, Club where Player.ClubID = Club.ClubID "
    cfg.clubXref = {x[0]: x[1] for x in sqlhub.processConnection.queryAll(clubXrefQuery)}

    cfg.clubRecord = Club.get(1)
    cfg.clubId = cfg.clubRecord.id
    club100 = list(Club.select(Club.q.clubNumber == 100))[0]
    cfg.reportDirectory = club100.reportDirectory
    rpt.tourneyRecord = cfg.at.getTourneyRecordById(rpt.tourneyRecordId)
    print('rpt.tourneyRecord: ', rpt.tourneyRecord)
    # reportData = BuildReportData()
    cashReport = CashReport()
    # cashReport.printReport() # added to end of ___init__

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
