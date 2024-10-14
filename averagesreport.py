# averagesreport.py
# 1/23/2020
# This is the averages for all players for the current season
# superceded by battingavgreport.py - was named averages - recieved longer, fuller name
#
import peggersconfig as cfg
import peggersreport as rpt
from scorecard import ScoreCard
from tourney import Tourney
from player import Player
from accessResults import AccessResults
from accessTourneys import AccessTourneys
from accessPlayers import AccessPlayers

# system imports
import os, sys
from fpdf import FPDF

class AveragesReport(object):
	def __init__(self, season):
		# season passed in is the season in cfg for the tourney being reported on
		os.chdir(cfg.reportDirectory)
		print('Dir: ', os.getcwd())
		self.averagesReportName = 'AveragesReport.pdf'
		self.reportTitle = 'BATTING AVERAGES for'
		self.clubName = 'Napa Seniors'
		self.clubNoLiteral = 'Club No:'
		self.clubNumber = '100'
		self.afterLiteral = 'After'
		self.tournamentsLiteral = 'Tournaments'
		self.seasonLiteral = 'Season'
		self.gmsLiteral = 'Gms'
		self.wlLiteral = 'W/L'
		self.averageLiteral = 'Average'
		self.gameLiteral = 'Game'
		self.pointsLiteral = 'Points'
		self.noLiteral = 'No.'
		self.playerLiteral = 'Player'
		self.plydLiteral = 'Plyd'
		self.wonLiteral = 'Won'
		self.averLiteral = 'Aver'
		self.tourLiteral = 'Tour'
		self.ptsLiteral = 'Pts'
		self.title0 = ' '       # blank cell spacer

		self.pdf = FPDF(format='Letter')    # default to mm units
		self.pdf.l_margin = 12
		self.pdf.r_margin = 12
		self.pdf.t_margin = 20
		self.pdf.b_margin = 20

		self.pdf.add_page()
		# compute effective widtha dn height, and text heigth from font size
		self.pdf.set_font('Times', '', 10)
		self.epw = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
		self.eph = self.pdf.h - self.pdf.t_margin - self.pdf.b_margin
		self.titel0w = self.pdf.get_string_width(self.title0)
		self.texth = self.pdf.font_size
		self.reportNumber = '14'
		self.clubSeason = '2019-20'

		self.setCell(0, self.reportTitle)
		self.setCell(47, self.clubName)
		self.setCell(127, self.clubNoLiteral)
		self.setCell(147, self.clubNumber)
		self.pdf.ln(2 * self.texth)

		self.setCell(0, self.afterLiteral)
		self.setCell(14, self.reportNumber)
		self.setCell(23, self.tournamentsLiteral)
		self.setCell(127, self.clubSeason)
		self.setCell(145, self.seasonLiteral)
		self.pdf.ln(2 * self.texth)

		self.setCell(63, self.gmsLiteral)
		self.setCell(73, self.gmsLiteral)
		self.setCell(87, self.wlLiteral)
		self.setCell(105, self.averageLiteral)
		self.setCell(123, self.gameLiteral)
		self.setCell(134, self.pointsLiteral)
		self.setCell(159, self.noLiteral)
		self.setCell(167, self.gameLiteral)

		self.pdf.ln(self.texth)

		self.setCell(0, self.playerLiteral)
		self.setCell(63, self.plydLiteral)
		self.setCell(73, self.wonLiteral)
		self.setCell(87, self.averLiteral)
		self.setCell(105, self.playerLiteral)
		self.setCell(157, self.tourLiteral)
		self.setCell(168, self.ptsLiteral)


		self.pdf.ln(self.texth)
		self.pdf.set_line_width(0.5)
		self.pdf.line(self.pdf.l_margin, self.pdf.get_y(),
		             self.pdf.l_margin + self.epw, self.pdf.get_y()
		             )

	def setCell(self, o, l):
		# o is offset from left margin
		# l i literal for cell
		self.pdf.set_x(self.pdf.l_margin + o)
		self.pdf.cell(self.pdf.get_string_width(l), 0, l)

	def printReport(self):
		self.pdf.close()
		self.pdf.output(self.averagesReportName)

if __name__ == '__main__':
	print('Create averages report')
	averagesReport = AveragesReport(17)
	averagesReport.printReport()