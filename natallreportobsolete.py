# natallreport.py
# 1/23/2020
# OBSOLETE: replaced by nationalratingreport.py
#
# National all points report for teh current season
#
import seniorsconfig as cfg
from scorecard import ScoreCard
from tourney import Tourney
from player import Player
from accessResults import AccessResults
from accessTourneys import AccessTourneys
from accessPlayers import AccessPlayers

# system imports
import os, sys
from fpdf import FPDF

class NatAllReport(object):
	def __init__(self, season):
		# season passed in is the season in cfg for the tourney being reported on
		os.chdir(cfg.reportDirectory)
		print('Dir: ', os.getcwd())
		self.natAllReportName = 'NatAllReport.pdf'
		self.reportTitle = 'NATIONAL RAING POINRTS Include Regional/National Tourneys'
		self.clubName = 'Napa Seniors'
		self.charterLiteral = 'Charter No:'
		self.clubNumber = '100'
		self.afterLiteral = 'After'
		self.reportNumber = '14'
		self.tournamentsLiteral = 'Tournaments'
		self.season = '2019-20'
		self.seasonLiteral = 'Season'
		self.nameLiteral = 'Name'
		self.clubLiteral = 'Club'
		self.totalLiteral = 'Total'
		self.reglLiteral = 'Regl'
		self.natlLiteral = 'Natl'
		self.tourneysLiteral = 'Tourneys'
		self.ptsLiteral = 'Pts'
		self.playedLiteral = 'Played'
		self.noLiteral = 'No.'

		self.pdf = FPDF(format='Letter')
		self.pdf.l_margin = 25
		self.pdf.r_margin = 25
		self.pdf.t_margin = 25
		self.pdf.b_margin = 50

		self.pdf.add_page()  # leave portrati as default
		# compute effective width and height, and text height from font size.
		self.pdf.set_font('Times', '', 10)
		self.epw = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
		self.eph = self.pdf.h - self.pdf.t_margin - self.pdf.b_margin
		self.texth = self.pdf.font_size

		self.setCell(0, self.reportTitle)
		self.setCell(138, self.seasonLiteral)
		self.pdf.ln(2 * self.texth)

		self.setCell(0, self.clubName)
		self.setCell(78, self.charterLiteral)
		self.setCell(108, self.clubNumber)
		self.pdf.ln(2 * self.texth)

		self.setCell(0, self.afterLiteral)
		self.setCell(15, self.reportNumber)
		self.setCell(24, self.tournamentsLiteral)
		self.setCell(88, self.season)
		self.setCell(101, self.seasonLiteral)
		self.pdf.ln(2 * self.texth)

		self.setCell(123, self.clubLiteral)
		self.pdf.ln(self.texth)

		self.setCell(69, self.totalLiteral)
		self.setCell(85, self.clubLiteral)
		self.setCell(96, self.reglLiteral)
		self.setCell(108, self.natlLiteral)
		self.setCell(119, self.tourneysLiteral)
		self.setCell(138, self.clubLiteral)
		self.pdf.ln(self.texth)

		self.setCell(7, self.nameLiteral)
		self.setCell(71, self.ptsLiteral)
		self.setCell(87, self.ptsLiteral)
		self.setCell(99, self.ptsLiteral)
		self.setCell(110, self.ptsLiteral)
		self.setCell(121, self.playedLiteral)
		self.setCell(140, self.noLiteral)
		self.pdf.ln(2 * self.texth)

	def setCell(self, o, l):
		# o is offset from left margin
		# l i literal for cell
		self.pdf.set_x(self.pdf.l_margin + o)
		self.pdf.cell(self.pdf.get_string_width(l), 0, l)

	def printReport(self):
		self.pdf.close()
		self.pdf.output(self.natAllReportName)

if __name__ == '__main__':
	print('Create National All report')
	natAllReport = NatAllReport('2019-20')
	natAllReport.printReport()