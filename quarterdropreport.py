# quarterdropreport.py
# 1/23/2020
# OBSOLETE: replaced by qtrdrop.py
#
# For each quarter in current season, drop worst week
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

class QuarterDropReport(object):
	def __init__(self, season):
		# season passed in is the season in cfg for the tourney being reported on
		os.chdir('e:/Python/Reporting/')
		print('Dir: ', os.getcwd())
		self.qtrDropReportName = 'QtrDropReport.pdf'
		self.reportTitle = 'QUARTER TREASURE HUNT FOR THE PIECES OF EIGHT'
		self.clubName = 'Napa Seniors'
		self.afterLiteral = 'After'
		self.reportNumber = '14'
		self.tournamentsLiteral = 'Tournaments'
		self.season = '2019-20'
		self.seasonLiteral = 'Season'
		self.subtitleLiteral = 'WORST Week Dropped - Total Entries in Quarter'
		self.totalEntries = '79'
		self.quarter = '2nd'
		self.tourneyCount = '5'
		self.weeksLiteral = 'Weeks'
		self.nameLiteral = 'Name'
		self.pointsLiteral = 'Points'
		self.plydLiteral = 'Plyd'


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

		self.setCell(24, self.quarter)
		self.setCell(33, self.reportTitle)
		self.pdf.ln(2 * self.texth)

		self.setCell(24, self.afterLiteral)
		self.setCell(40, self.tourneyCount)
		self.setCell(44, self.tournamentsLiteral)
		self.setCell(102, self.season)
		self.setCell(119, self.seasonLiteral)
		self.pdf.ln(2 * self.texth)

		self.setCell(24, self.subtitleLiteral)
		self.setCell(102, self.tourneyCount)
		self.pdf.ln(self.texth)

		self.setCell(117, self.weeksLiteral)
		self.pdf.ln(self.texth)

		self.setCell(34, self.nameLiteral)
		self.setCell(93, self.pointsLiteral)
		self.setCell(117, self.plydLiteral)
		self.pdf.ln(2 * self.texth)

	def setCell(self, o, l):
		# o is offset from left margin
		# l i literal for cell
		self.pdf.set_x(self.pdf.l_margin + o)
		self.pdf.cell(self.pdf.get_string_width(l), 0, l)

	def printReport(self):
		self.pdf.close()
		self.pdf.output(self.qtrDropReportName)

if __name__ == '__main__':
	print('Create quarter drop report')
	quarterDropReport = QuarterDropReport('2019-20')
	quarterDropReport.printReport()