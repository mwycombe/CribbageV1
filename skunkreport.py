# skunkreport.py - V1 1/14/2020
# 7/22/2020 updated to use cribbageconfig and cribbagereport and cribbagetso
#
# test version to explro layout options for skunk report
#
# no header or footer used, so no custom RPDF required.
#
# use mm units, expand to 25.4 (1 in) margins)
#
# personal imports
import cribbageconfig as cfg
import cribbagereport as rpt
from scorecard import ScoreCard
from player import Player
from tourney import Tourney
from accessResults import AccessResults
from accessPlayers import AccessPlayers
from accessTourneys import AccessTourneys
from cribbagetso import *

# system imports
from fpdf import FPDF
import os
import sys

class SkunkReport (object):
    def __init__(self):
        # rpoData = BuildReportData()       # puts data directly into rpt.reportData
        rptData = BuildReportData()
        rpt.reportLineNumber = 0
        os.chdir(cfg.reportDirectory)
        print ('Dir: ', os.getcwd())
        self.skunkReportName = rpt.reportSeason + '-Week-' + str(rpt.tourneyNumber) + '-SkunkReport.pdf'
        self.skunkListTitle = 'YE OLDE SKUNK LIST'
        self.skunksHdrLiteral = 'Skunks'
        self.givenColsHdrLiteral = 'Given Net  Name'
        self.takenColsHdrLiteral = 'Taken Net  Name'
        self.seasonHeader = cfg.season + ' Season'
        self.tourneyHeader = 'After ' + str(rpt.tourneyNumber) + ' Tourneys'
        self.pdf = FPDF(format = 'Letter')
        self.pdf.l_margin = 25
        self.pdf.r_margin = 25
        self.pdf.t_margin = 25
        self.pdf.b_margin = 50

        self.pdf.add_page()      # leave portrati as default
        # compute effective width and height, and text height from font size.
        self.pdf.set_font('Courier','', 10)
        self.epw = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
        self.eph = self.pdf.h - self.pdf.t_margin - self.pdf.b_margin
        self.texth = self.pdf.font_size

        self.setCell(4, self.skunkListTitle)
        self.setCell(62, self.seasonHeader)
        self.setCell(106, self.tourneyHeader)
        self.pdf.ln(2 * self.texth)

        self.setCell(18, self.skunksHdrLiteral)
        self.setCell(104, self.skunksHdrLiteral)
        self.pdf.ln(self.texth)

        self.setCell(13, self.givenColsHdrLiteral)
        self.setCell(100, self.takenColsHdrLiteral)
        self.pdf.ln(2 * self.texth)
        # print ('reportData: ', rpt.reportData)
        for rLine in rpt.reportData:
            self.addLineToReport(rLine)

        self.printReport()
    def addLineToReport(self, aLine):
        rpt.reportLineNumber += 1
        # print ('aLine: ', aLine)
        # self.setCell(7 posn)
        if aLine[0][0] > 0:
            self.setCell(7, '{:=2n}'.format(aLine[0][0]) + '.')
        else:
            self.setCell(7, ' ')
        # self.setCell(18, given)
        self.setCell(18, '{:=2n}'.format(aLine[0][1][1]))
        # self.setCell(26, net)
        self.setCell(25, '{:3n}'.format(aLine[0][1][3]))
        # self.setCell(37, name)
        self.setCell(37, cfg.playerXref[aLine[0][1][0]])
        # self.setCell(91, posn)
        if aLine[1][0] > 0:
            self.setCell(91, '{:=2n}'.format(aLine[1][0]) + '.')
        else:
            self.setCell(91, ' ')
        # self.setCell(102, taken)
        self.setCell(102, '{:=2n}'.format(aLine[1][1][2]))
        # self.setCell(113, net)
        self.setCell(112, '{:3n}'.format(aLine[1][1][3]))
        # self.setCell(124, name)
        self.setCell(124, cfg.playerXref[aLine[1][1][0]])
        self.pdf.ln(self.texth)
        if rpt.reportLineNumber % 5 == 0: self.pdf.ln(self.texth)

    def setCell(self, o, text):
        # o is the offset from left margin
        # text is literal for cell
        self.pdf.set_x(self.pdf.l_margin + o)
        self.pdf.cell(self.pdf.get_string_width(text), 0, text)
    def printReport(self):
        # set up two multi_cell columns of skunk results stored by Given and Taken
        self.pdf.close()
        self.pdf.output(self.skunkReportName)
class BuildReportData(object):
    def __init__(self):
        # skunkQuery = "select PlayerID, sum(SkunksGiven), sum(SkunksTaken), sum(SkunksGiven) - sum(SkunksTaken) from ScoreCard where ScoreCard.TourneyID in (select Tourney.TourneyID from Tourney where TourneyNumber <= 14) group by PlayerID"
        skunkRows = cfg.ar.getSkunks(str(rpt.tourneyNumber), cfg.season)
        skunksGiven = sorted(skunkRows, key=lambda skunkline: skunkline[1], reverse=True)
        skunksTaken = sorted(skunkRows, key=lambda skunkline: skunkline[2], reverse=True)
        skunksGivenList = list(skunksGiven)
        skunksTakenList = list(skunksTaken)
        skunksGivenList = list( [list(x) for x in skunksGivenList])
        skunksTakenList = list( [list(x) for x in skunksTakenList])
        skunksGivenList = list(zip(range(1, len(skunksGivenList)+1), skunksGivenList))
        skunksTakenList = list(zip(range(1, len(skunksTakenList)+1), skunksTakenList))
        # check for tied players
        skunksGivenList = self.handleGivenTies(skunksGivenList)
        skunksTakenList = self.handleTakenTies(skunksTakenList)

        # print ('skunksgiven: ', skunksGivenList)
        # print ('skunkstaken: ', skunksTakenList)
        skunksLines = list(zip(skunksGivenList, skunksTakenList))
        # print('skunksLines: ', skunksLines)
        rpt.reportData = skunksLines
        # rpt.reportData = skunksLines
    def handleGivenTies(self,lines):
        newSkunkLines = []
        self.savedLine = lines[0]
        newSkunkLines.append(self.savedLine)
        for x in range(1, len(lines)):
            self.tempLine = list(lines[x])
            # print ('Saved, Temp:', self.savedLine, self.tempLine)
            if self.savedLine[1][1] == lines[x][1][1]:
                self.tempLine[0] = 0
            self.savedLine = self.tempLine
            newSkunkLines.append(self.savedLine)
        return newSkunkLines
    def handleTakenTies(self,lines):
        newSkunkLines = []
        self.savedLine = lines[0]
        newSkunkLines.append(self.savedLine)
        for x in range(1, len(lines)):
            self.tempLine = list(lines[x])
            # print ('Saved, Temp:', self.savedLine, self.tempLine)
            if self.savedLine[1][2] == lines[x][1][2]:
                self.tempLine[0] = 0
            self.savedLine = self.tempLine
            newSkunkLines.append(self.savedLine)
        return newSkunkLines

if __name__ == '__main__':
    print ('Create cash report')
    #############################################
    # hardwire cfg for testing                  #
    cfg.appTitle = 'Reports Testing'  #
    cfg.clubNumber = 100  #
    cfg.season = '2018-19'  #
    cfg.clubName = 'Peggers'  #
    rpt.tourneyDate = '2018-04-09'  #
    rpt.tourneyRecordId = 25  #
    rpt.tourneyNumber = 1 #

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
    players = list(Player.select())
    print(players)
    cfg.playerXref = {p.id: p.LastName + ', ' + p.FirstName for p in list(Player.select())}
    cfg.playerRefx = { v : k for k, v in cfg.playerXref.items() }
    cfg.clubRecord = Club.get(1)
    cfg.clubId = cfg.clubRecord.id
    cfg.reportDirectory = cfg.clubRecord.reportDirectory
    club100 = list(Club.select(Club.q.clubNumber == 100))[0]
    rpt.tourneyRecord = cfg.at.getTourneyByNumber(rpt.tourneyNumber)[0]
    rpt.tourneyRecordId = rpt.tourneyRecord.id

    print('cfg.tourneyRecord: ', cfg.tourneyRecord)
    # reportData = BuildReportData()
    skunkReport = SkunkReport()
    # skunkReport.printReport()

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
