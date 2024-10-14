# nationalratingreport.py
# 7/22/2020 updated to cribbageconfig and cribbagereport and cribbagetso
# 2/24/2020
# This is the report for national reating
#
# note need to us '{formatspec}.format(values) to 'almost' get things aligned
#
# TODO: paramaterize extraction of summary by season and date
# TODO: only extract regional and national when tourney data > report date

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
import collections
from fpdf import FPDF


class NatAllReport(object):
	def __init__(self):
		# tourney passed in is the tourney object in rpt for the tourney being reported on
		rptData = BuildReportData()
		rpt.reportLineNumber = 0
		os.chdir(cfg.reportDirectory)
		print('Report Dir: ', os.getcwd())
		self.reportName = rpt.reportSeason + '-Week-' + str(rpt.tourneyRecord.TourneyNumber) + '-NatAll.pdf'
		self.reportTitle = 'NATIONAL RATING POINTS Including Regional/National Tourneys'
		self.playedOn = 'Played:'
		self.clubNoHdr = 'Club No.'
		self.clubNumber = cfg.clubNumber
		self.clubName = cfg.clubName
		self.clubLocation = cfg.clubLocation
		self.clubSeason = cfg.season + ' Season'
		self.clubLiteral = 'Club'
		self.charterLiteral = 'Charter No:'
		self.afterHdr = 'After  ' + str(rpt.tourneyNumber) + '  Tournaments'
		self.totalLiteral = 'Total'
		self.reglLiteral = 'Regl'
		self.natlLiteral = 'Natl'
		self.tourneysLiteral = 'Tourneys'
		self.nameLiteral = 'Name'
		self.ptsLiteral = 'Pts'
		self.noLiteral = 'No.'
		self.playedLiteral = 'Played'
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

		self.setCell(0, self.reportTitle)
		self.setCell(138, self.playedOnDate)
		self.pdf.ln(2 * self.texth)

		self.setCell(0, self.clubName)
		self.setCell(40, self.clubLocation)
		self.setCell(88, self.charterLiteral)
		self.setCell(118, str(self.clubNumber))
		self.pdf.ln(2 * self.texth)

		self.setCell(0, self.afterHdr)
		self.setCell(88, self.clubSeason)
		self.pdf.ln(2 * self.texth)

		self.setCell(123, self.clubLiteral)
		self.pdf.ln(self.texth)

		self.setCell(70, self.totalLiteral)
		self.setCell(85, self.clubLiteral)
		self.setCell(97, self.reglLiteral)
		self.setCell(108, self.natlLiteral)
		self.setCell(120, self.tourneysLiteral)
		self.setCell(138, self.clubLiteral)
		self.pdf.ln(self.texth)

		self.setCell(11, self.nameLiteral)
		self.setCell(72, self.ptsLiteral)
		self.setCell(85, self.ptsLiteral)
		self.setCell(97, self.ptsLiteral)
		self.setCell(108, self.ptsLiteral)
		self.setCell(122, self.playedLiteral)
		self.setCell(140, self.noLiteral)

		self.pdf.set_line_width(0.25)
		self.pdf.ln(self.texth)
		self.pdf.line(self.pdf.l_margin, self.pdf.get_y(),
		              self.pdf.l_margin + self.epw, self.pdf.get_y()
		              )
		self.pdf.ln(self.texth)
		for rline in rptData.rptLines:
		    self.addLineToReport(rline, rptData)

		self.printReport()
	def addLineToReport(self, aLine, rptData):
		print('aline: ', aLine)
		rpt.reportLineNumber += 1
		self.pdf.ln(self.texth)
		if aLine[0] > 0:
			self.setCell(2, '{:2n}'.format(aLine[0]) + '.')
		else:
			self.setCell(2, ' ')
		self.setCell(11, cfg.playerXref[aLine[1][0]])
		reglPts = self.calcReglPts(aLine[1][0], rptData)
		natlPts = self.calcNatlPts(aLine[1][0], rptData)
		totalPts = aLine[1][1]
		# back out and regional or national points to get club points
		clubPts = totalPts - reglPts - natlPts
		print ('totalPts: ', totalPts,' reglPts: ', reglPts,' natlPts: ',natlPts,' clubPts: ',clubPts)
		self.setCell(72, '{:3n}'.format(totalPts))
		self.setCell(86, '{:3n}'.format(clubPts))
		# print regional and national points separately
		if reglPts > 0:
			self.setCell(97, '{:3n}'.format(reglPts))
		if natlPts > 0:
			self.setCell(108, '{:3n}'.format(natlPts))
		# if aLine[1][0] in rptData.rows45Dict:              # any special tourney entry?
		# 	if rptData.rows45Dict[aLine[1][0]][1] == 41:   # is it regional 41 tourney?
		# 		self.setCell(97, '{:3n}'.format(rptData.rows45Dict[aLine[1][0]] [0]))
		# 	elif rptData.rows45Dict[aLine[1][0]][1] == 42: # is it national 42 tourney?
		# 		self.setCell(108, '{:3n}'.format(rptData.rows45Dict[aLine[1][0]] [0]))
		self.setCell(125, '{:2n}'.format(rptData.tourneyCountDict[aLine[1][0]]))
		print ('clubXref', cfg.clubXref)
		self.setCell(139, '{:3n}'.format(cfg.clubXref[aLine[1][0]]))
		if rpt.reportLineNumber % 5 == 0: self.pdf.ln(self.texth)

	def calcReglPts(self,pid,data):
		grReglPts = 0
		# ksvs holds [(pid,(points, tourney#)),(pid,(points,tourney#))...] in no reliable order
		for k in data.ksvs:
			if k[0] == pid and k[1][1] == 41:
				grReglPts = max(grReglPts,k[1][0])
		return grReglPts    # returns zero if no regional found for this pid
		# if line[1][0] in data.rows45Dict:
		# 	if data.rows45Dict[line[1][0]][1] == 41:
		# 		return data.rows45Dict[line[1][0]] [0]
		# return 0
	def calcNatlPts(self,pid,data):
		grNatlPts = 0
		for k in data.ksvs:
			if k[0] == pid and k[1][1] == 42:
				grNatlPts = max(grNatlPts,k[1][0])
		return grNatlPts    # returns zero if no national found for this pid
		# if line[1][0] in data.rows45Dict:
		# 	if data.rows45Dict[line[1][0]][1] == 42:
		# 		return data.rows45Dict[line[1][0]] [0]
		# return 0

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
		# rows36Query = "select PlayerID, sum(GamePoints) from ScoreCard where GamePoints > 11 AND  TourneyID in  "
		# rows36Query += "(select TourneyID from Tourney where season = '" + cfg.season + "' "
		# rows36Query += "AND Tourney.TourneyNumber BETWEEN 1 and 45) group by PlayerID order by Sum(GamePoints) desc"
		# rows36 = sqlhub.processConnection.queryAll(rows36Query)
		self.r36 = cfg.ar.nat36Results(str(rpt.tourneyNumber), cfg.season)
		print ('rows36: ', self.r36)
		# TODO: only get regional and national points for tourneys data >= report date
		# TODO: have to add in regl & natl points, resort, then handle ties for correct report ordering
		# rows45Query = "select PlayerID, GamePoints, TourneyNumber from ScoreCard, Tourney where "
		# rows45Query += "ScoreCard.TourneyID = Tourney.TourneyID and season = '2019-20' and TourneyNumber between 40 and 45"
		# self.rows45Dict = { r[0] : r[1:] for r in sqlhub.processConnection.queryAll(rows45Query) }
		# get results for any 41,42 tournaments. 41 is presumed regional, 42 national
		self.rows45 = cfg.ar.nat45Results(cfg.season)
		print ('self.rows45: ',self.rows45)
		# get [(pid, points, tourney#)] as a list of tuples
		# turn it into [(pid,(points, tourney#),...]
		ks = [k[0] for k in self.rows45]
		vs = [(v[1],v[2]) for v in self.rows45]
		self.ksvs = list(zip(ks, vs))

		print ('ksvs: ', self.ksvs)
		# this produces [(1,(24,42)), (1,(26,41))] - list with each regl/natl touney pts for each plwyerid
		# turn [(pid,points),(pid,points)....] summed by sql into a dictionary with pid key, points value
		self.r36Dict = {k:v for k,v in self.r36}
		self.r45Dict = self.r36Dict
		# if the pid has a regional or national points add them to the club points
		# if the pid has no club points, then regional and/or national points == club points
		for k in self.ksvs:
			if k[0] in self.r45Dict.keys():
				self.r45Dict[k[0]] += k[1][0]
			else:
				self.r45Dict[k[0]] = k[1][0]
		self.r45List = [(k,v) for k,v in self.r45Dict.items()]
		# create a listof tupples by pid for the total points, club + specials and sort it by points
		self.sorted45List = sorted(self.r45List, key=lambda r: r[1], reverse=True)
		print('sorted45List: ',self.sorted45List)

		# self.rows45Dict = {k: [sum(self.oldRows45Dict[k][0])] for k in self.oldRows45Dict.keys()}
		# print ('rows45Dict: ', self.rows45Dict)
		# tourneyCountQuery = "select PlayerID, count(TourneyID) from ScoreCard where TourneyId in (select TourneyID from "
		# tourneyCountQuery += "Tourney where Season = '2019-20') group by PlayerId order by PlayerID"
		# self.tourneyCountDict = { x[0]:x[1] for x in sqlhub.processConnection.queryAll(tourneyCountQuery) }

		self.tourneyCountDict = { x[0]:x[1] for x in cfg.ar.countTourneys(str(rpt.tourneyNumber),cfg.season) }
		print ('tourneyCountDict ',self.tourneyCountDict)
		# self.rptLines = list(zip(range(1, len(self.rows36)+1), self.rows36))
		# print ('rptLines: ', self.rptLines)
		# handle ties using the total points == club + specials
		self.rptLines = self.handleTies(list(zip(range(1, len(self.sorted45List)+1), self.sorted45List)))
		# self.rptLines = list(zip(range(1, len(self.rows36)+1), self.rows36))
		# print (rows36, '\n', self.rows45Dict)
	def handleTies(self, lines):
		self.newRptLines = []
		self.savedLine = lines[0]
		self.newRptLines.append(self.savedLine)
		for x in range(1, len(lines)):
			self.tempLine = list(lines[x])
			if self.savedLine[1][1] == lines[x][1][1]:
				self.tempLine[0] = 0
			self.savedLine = self.tempLine
			self.newRptLines.append(self.savedLine)
		return self.newRptLines
if __name__ == '__main__':
	print('Create tourney report')

	#############################################
	# hardwire cfg for testing                  #
	cfg.appTitle = 'Natl Report Test'  #
	cfg.clubNumber = 100  #
	cfg.season = '2022-23'  #
	cfg.clubName = 'Peggers'  #
	rpt.tourneyDate = '2022-11-29'  #
	rpt.tourneyRecordId = 111 #
	rpt.tourneyNumber = 13  #

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

	# xref building for stand-alone testing
	cfg.playerXref = {p.id: p.LastName + ', ' + p.FirstName for p in list(Player.select())}
	cfg.playerRefx = {v: k for k, v in cfg.playerXref.items()}

	# moved to peggers __init__
	# clubXrefQuery = "select PlayerID, ClubNumber from Player, Club where Player.ClubID = Club.ClubID "
	# cfg.clubXref = { x[0]:x[1] for x in sqlhub.processConnection.queryAll(clubXrefQuery) }
	# cfg.clubXref = { x[0]:x[1] for x in cfg.ac.clubXref() }

	cfg.clubRecord = cfg.ac.clubByNumber(100)[0]
	cfg.clubId = cfg.clubRecord.id
	cfg.clubLocation = cfg.clubRecord.location
	cfg.clubName = cfg.clubRecord.clubName
	club100 = list(Club.select(Club.q.clubNumber == 100))[0]
	cfg.reportDirectory = club100.reportDirectory
	print ('cfg:reportDirectory: ', cfg.reportDirectory)

	cfg.clubXref = {x[0]: x[1] for x in cfg.ac.clubXref()}

	rpt.tourneyRecord = cfg.at.getTourneyByNumber(rpt.tourneyNumber)[0]
	print('rpt.tourneyRecord: ', rpt.tourneyRecord)
	# reportData = BuildReportData()
	natAllReport = NatAllReport()
	# nationalReport.printReport()

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
