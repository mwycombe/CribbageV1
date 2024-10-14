# qtrdropreport.py
# 7/22/2020 updated to cribbageconfig and cribbagereport and cribbagetso
# 2/24/2020
# This is the report for national reating
#
# note need to use '{formatspec}.format(values) to 'almost' get things aligned
#


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
from tkinter import messagebox as mbx
from itertools import *

# TODO: handle no report possible for 1st tourney of a quarter...
# TODO; change hard-coded quartername

class QtrDropReport(object):
	def __init__(self):
		# tourney passed in is the tourney object in rpt for the tourney being reported on
		# add checke to skip a 1st in quarter tourney
		if rpt.tourneyNumber in (1,10,19,28):
			# cannot be run for first tourney of a quarter
			mbx.showerror('Report cannot be run', 'Cannot run qtrdrop for first tourney of a quarter')
			return
		self.rptData = BuildReportData()
		rpt.reportLineNumber = 0
		os.chdir(cfg.reportDirectory)
		print('Report Dir: ', os.getcwd())
		self.reportName = rpt.reportSeason + '-Week-' + str(rpt.tourneyRecord.TourneyNumber) + '-QtrDrop.pdf'
		self.reportQuarter = self.rptData.qtr
		print ('self.reportQuarter:', self.reportQuarter)
		self.reportTitle = 'QUARTER TREASURE HUNT FOR THE PIECES OF EIGHT'
		self.playedOn = 'Played:'
		self.clubNoHdr = 'Club No.'
		self.clubNumber = cfg.clubNumber
		self.clubName = cfg.clubName
		self.clubLocation = cfg.clubLocation
		self.clubSeason = cfg.season + ' Season'
		self.clubLiteral = 'Club'
		self.charterLiteral = 'Charter No:'
		self.afterHdr = 'After  ' + str(rpt.tourneyNumber) + '  Tournaments'
		self.subTitleLiteral = 'WORST Week Dropped - Total Entries in Quarter'
		self.quarterEntries = str(rpt.quarterEntryTotal)
		self.nameLiteral = 'Name'
		self.pointsLiteral = 'Points'
		self.weeksLiteral = 'Weeks'
		self.plydLiteral = 'Plyd'
		self.title0 = ' '  # a blank cell spacer

		self.pdf = FPDF(format='Letter')  # default mm units
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
		self.reportNumber = str(rpt.tourneyRecord.TourneyNumber)
		self.playedOnDate = rpt.tourneyDate
		self.setCell(24, self.reportQuarter)
		self.setCell(33, self.reportTitle)
		self.pdf.ln(2 * self.texth)

		self.setCell(24, self.clubName)
		self.setCell(85, self.charterLiteral)
		self.setCell(118, str(self.clubNumber))
		self.pdf.ln(self.texth)

		self.setCell(24, self.clubLocation)
		self.pdf.ln(2 * self.texth)

		self.setCell(24, self.afterHdr)
		self.pdf.ln(2 * self.texth)

		self.setCell(24, self.subTitleLiteral)
		self.setCell(127, self.quarterEntries)
		self.pdf.ln(2 * self.texth)

		self.setCell(117, self.weeksLiteral)
		self.pdf.ln(self.texth)

		self.setCell(34, self.nameLiteral)
		self.setCell(93, self.pointsLiteral)
		self.setCell(117, self.plydLiteral)
		self.pdf.ln(self.texth)

		self.pdf.set_line_width(0.25)

		self.pdf.line(self.pdf.l_margin +25, self.pdf.get_y(),
		              self.pdf.l_margin + self.epw - 30, self.pdf.get_y()
		              )
		self.pdf.ln(2 * self.texth)
		# print (' A report line looks like this: ', self.rptData.rptLines[0])
		for rline in self.rptData.rptLines:
			# print('Added line: ',rline)
			self.addLineToReport(rline)
		self.printReport()
		return

	def addLineToReport(self, aLine):
		# return
		rpt.reportLineNumber += 1
		# print ('aLine ', aLine[0][0], aLine)
		if aLine[0] > 0:
			self.setCell(26, '{:2}'.format(aLine[0]) + '.')
		else:
			self.setCell(26, ' ')
		self.setCell(34, cfg.playerXref[aLine[1][0]])
		self.setCell(96, '{:2n}'.format(aLine[1][1]))
		# self.setCell(121, '{:2n}'.format(rptData.))
		# self.setCell(121, '{:2n}'.format(self.rptData.playerCTDict[aLine[1][0]]))
		self.setCell(121, '{:2n}'.format(self.rptData.playerCTDict[aLine[1][0]]))

		if rpt.reportLineNumber % 5 == 0: self.pdf.ln(self.texth)
		self.pdf.ln(self.texth)


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
		# qtrCountQ = "select PlayerID, GamePoints from ScoreCard where TourneyID in (select TourneyID from Tourney where "
		# qtrCountQ += "season = '2019-20' and TourneyNumber between (1 + (1 - 1)* 9) and (9 + (1 -1) * 9)) "
		# qtrCountQ += "order by PlayerID, GamePoints asc"
		# get all pid,games pts for the quarter
		qtrNumber = (rpt.tourneyNumber + 8) // 9
		self.qtr = self.qtrName(qtrNumber)
		self.lowTourney = 1 + (qtrNumber - 1) * 9
		self.highTourney = rpt.tourneyNumber
		self.tourneyCount = self.highTourney - self.lowTourney + 1
		allPlayers = cfg.ar.qtrDropCount(cfg.season, qtrNumber, rpt.tourneyNumber)
		print ('allPlayers', allPlayers)
		# create list of unique player ids; use length for number of players in quarter with points
		uniquePlist = set ( x[0] for x in allPlayers)
		print ('Unique plist: ', uniquePlist)
		# group all pid,pts into individual lists
		groupedQtrPtsByPid = [[x[:] for x in allPlayers if x[0] == list(uniquePlist)[i]] for i in range(len(uniquePlist))]
		print ("groupedQtrPtsByPid: ",groupedQtrPtsByPid)
		# TODO: Make sure we add in weeks where player scored nothing/did not attend
		# drop anyone that has less than one results
		appendedQtrPtsByPid = []
		print ('This quarter, tourney number, count of tourneys: ', qtrNumber, rpt.tourneyNumber, self.tourneyCount)
		for x in groupedQtrPtsByPid:
			print ('Len, List: ', len(x), x)
			y = x
			if len(x) < self.tourneyCount:
				y = [(x[0][0],0)]
				for z in x:
					y.append(z)
			appendedQtrPtsByPid.append(y)
		print('Appended pts list: ', appendedQtrPtsByPid)
		prunedQtrPtsByPid = [x[:] for x in appendedQtrPtsByPid if len(x) > 1]
		print ('prunedQrtPtsByPid:', prunedQtrPtsByPid)
		# clip the first point counts - it's the smallest so is dropped
		clippedPtsList = [x[1:] for x in prunedQtrPtsByPid]
		print('clippedPtsList: ',clippedPtsList)
		# make list of sums for each pid
		unsortedReportLines = [(t[0][0], sum(x[1] for x in t)) for t in clippedPtsList]
		print ('unsortedReportLines:', unsortedReportLines)
		# and finally sort descending on the sums to build report line data
		sortedReportLines = sorted(unsortedReportLines, key=lambda x: x[1], reverse= True)
		playerCT = [(x[0][0], len(x)) for x in groupedQtrPtsByPid]
		self.playerCTDict = {k: v for k, v in playerCT}
		self.linedRptLines = list(zip( range(1, len(sortedReportLines)+1), sortedReportLines))
		print ('linedRptLines: ', self.linedRptLines)
		self.rptLines =self.handleTies(self.linedRptLines)
		print ('rptLines: ', self.rptLines)
		rpt.quarterEntryTotal = sum( len(x) for x in groupedQtrPtsByPid)
		# print ('All data structures:')
		# print ('allPlayers (that have results for the period): ',allPlayers)
		# print ('groupedQtrPtsbyPid: ', groupedQtrPtsByPid)
		# print ('prunedQtrPtsbyPid: ', prunedQtrPtsByPid)
		# print ('clippedPtsList: ', clippedPtsList)
		# print ('unsortedReportLines: ', unsortedReportLines)
		# print ('sortedReportLines: ', sortedReportLines)
		# print ('playerCT:', playerCT)
		# print ('playerCTDict: ', self.playerCTDict)
		# print ('rptLines: ', self.rptLines)
		# print ('quarterEntryTotal: ', rpt.quarterEntryTotal)
	def handleTies(self, lines):
		print ('lines: ', lines)
		newReportLines = []
		savedLine = lines[0]
		newReportLines.append(savedLine)
		for x in range(1, len(lines)):
			tempLine = list(lines[x])
			if savedLine[1][1] == tempLine[1][1]:
				tempLine[0] = 0
			savedLine = tempLine
			newReportLines.append(savedLine)
		return newReportLines
	def qtrName(self,qno):
		qDict = {
			1: '1st',
			2: '2nd',
			3: '3rd',
			4: '4th'
		}
		return qDict[qno]


if __name__ == '__main__':
	print('Create qtrdrop report')

	#############################################
	# hardwire cfg for testing                  #
	cfg.appTitle = 'Reports Testing'  #
	cfg.clubNumber = 100  #
	cfg.season = '2021-22'  #
	cfg.clubName = 'Peggers'  #
	rpt.tourneyDate = '2021-11-30'  #
	rpt.tourneyRecordId = 72  #
	rpt.tourneyNumber = 12  #

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

	clubXrefQuery = "select PlayerID, ClubNumber from Player, Club where Player.ClubID = Club.ClubID "
	cfg.clubXref = { x[0]:x[1] for x in sqlhub.processConnection.queryAll(clubXrefQuery) }

	# cfg.clubRecord = cfg.ac.clubByNumber(100)[0]
	cfg.clubRecord = Club.get(1)
	cfg.clubId = cfg.clubRecord.id
	cfg.clubLocation = cfg.clubRecord.location
	cfg.clubName = cfg.clubRecord.clubName
	club100 = list(Club.select(Club.q.clubNumber == 100))[0]
	cfg.reportDirectory = club100.reportDirectory
	rpt.tourneyRecord = cfg.at.getTourneyByNumber(rpt.tourneyNumber)[0]
	print('rpt.tourneyRecord: ', rpt.tourneyRecord)
	# reportData = BuildReportData()
	qtrDropReport = QtrDropReport()
	# qtrDropReport.printReport()

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
