# talphayreport.py
# 10/4/2024 cloned from tourneyreport.p
# 7/22/2020 update to cribbageconfig and cribbagereport and cribbagetso
# 1/21/2020
# This is the report for an individual tournament
#
# note need to us '{formatspec}.format(values) to 'almost' get things aligned
# from tourneyreportline import TourneyReportLine
# TODO: Handle tied positions in addLineToReport
# TODO: Wrong player name against result line

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



class AlphaReport(object):
    def __init__(self):
        # tourney passed in is the tourney object in rpt for the tourney being reported on
        rptData = BuildReportData()
        rpt.reportLineNumber = 0
        os.chdir(cfg.reportDirectory)
        print('Report Dir: ', os.getcwd())
        self.tourneyReportName = rpt.reportSeason + '-Week-' + str(rpt.tourneyRecord.TourneyNumber) + '-AlphaReport.pdf'
        self.reportTitle = 'LOCAL TOURNAMENT ALPHA REPORT No:'
        self.playedOn = 'Played:'
        self.clubNoHdr = 'Club No.'
        self.clubNo = cfg.clubNumber
        self.clubName = cfg.clubName
        self.clubLocation = 'Napa'
        self.clubSeason = cfg.season + ' Season'
        self.clubLiteral = 'Club'
        self.gmsLiteral = 'Gms'
        self.natLiteral = 'Natl'
        self.sknksLiteral = 'Sknks'
        self.plLiteral = 'Pl'
        self.nameLiteral = 'Name'
        self.accnoLiteral = 'ACC No.'
        self.noLiteral = 'No.'
        self.ptsLiteral = 'Pts'
        self.wonLiteral = 'Won'
        self.sprdLiteral = 'Sprd'
        self.natlLiteral = 'Natl'
        self.cashLiteral = "$'s"
        self.takenLiteral = 'Taken'
        self.givenLiteral = 'Given'
        self.title0 = ' '   # a blank cell spacer
        # self.skunksHdrOffset = 17
        # self.colsHdr = 'Given Net   Name'
        # self.colsHdrOffset = 11

        self.pdf = FPDF(format='Letter')    # default mm units
        self.pdf.l_margin = 25
        self.pdf.r_margin = 25
        self.pdf.t_margin = 25
        self.pdf.b_margin = 50

        self.pdf.add_page()  # leave portrait as default
        # compute effective width and height, and text height from font size.
        self.pdf.set_font('Courier', '', 10)
        self.epw = self.pdf.w - self.pdf.l_margin - self.pdf.r_margin
        self.eph = self.pdf.h - self.pdf.t_margin - self.pdf.b_margin
        self.title0w = self.pdf.get_string_width(self.title0)   # cell for width for padding
        self.texth = self.pdf.font_size
        self.reportNumber = str(rpt.tourneyRecord.TourneyNumber)
        self.playedOnDate = rpt.tourneyDate
        self.title3 = self.clubNoHdr

        self.setCell(0, self.reportTitle)
        self.setCell(70, self.reportNumber)
        self.setCell(95, self.playedOn)
        self.setCell(117, self.playedOnDate)
        self.pdf.ln(2 * self.texth)


        self.setCell(0, self.clubLiteral)
        self.setCell(21, str(self.clubNo))
        self.setCell(33, self.clubName)
        self.setCell(78, self.clubLocation)
        self.pdf.ln(2 * self.texth)

        self.setCell(25, self.clubSeason)
        self.setCell(80, self.clubLiteral)
        self.setCell(92, self.gmsLiteral)
        self.setCell(101, self.gmsLiteral)
        self.setCell(119, self.natlLiteral)
        self.setCell(138, self.sknksLiteral)
        self.setCell(152, self.sknksLiteral)
        self.pdf.ln(self.texth)

        self.setCell(1, self.plLiteral)
        self.setCell(11, self.nameLiteral)
        self.setCell(60, self.accnoLiteral)
        self.setCell(82, self.noLiteral)
        self.setCell(92, self.ptsLiteral)
        self.setCell(101, self.wonLiteral)
        self.setCell(110, self.sprdLiteral)
        self.setCell(120, self.ptsLiteral)
        self.setCell(130, self.cashLiteral)
        self.setCell(138, self.takenLiteral)
        self.setCell(152, self.givenLiteral)
        self.pdf.set_line_width(0.25)
        self.pdf.ln(self.texth)
        self.pdf.line(self.pdf.l_margin, self.pdf.get_y(),
                      self.pdf.l_margin + self.epw, self.pdf.get_y()
                      )
        self.pdf.ln(self.texth)
        for rline in rpt.reportData:
            self.addLineToReport(rline)

        self.printReport()
        # self.pdf.set_x(self.pdf.l_margin + 1)
        # self.pdf.cell(4, 0, '----')
        # self.pdf.set_x(self.pdf.l_margin + 11)
        # self.pdf.cell(16, 0, '----------------')
        # self.pdf.set_x(self.pdf.l_margin + 60)
        # self.pdf.cell(8, 0, '--------')
        # self.pdf.set_x(self.pdf.l_margin + 83)
        # self.pdf.cell(0, 0, '--- --- --- ---- --- --- ----- -----')
    def addLineToReport(self, aLine):
        rpt.reportLineNumber += 1
        # print ('aLine ', aLine[0][0], aLine)
        if aLine[0][0] > 0:
            self.setCell(2, '{:=2n}'.format(aLine[0][0]) + '.')
        else:
            self.setCell(2, ' ')
        self.setCell(11, aLine[0][1])
        self.setCell(60, aLine[0][2])   # ACC No
        # self.setCell(82, str(cfg.clubNumber))
        # self.setCell(83, str(aline[0][2]  # get club number from player record
        self.setCell(83, str(cfg.clubXref[aLine[1].PlayerID]))
        self.setCell(92, '{:2n}'.format(aLine[1].GamePoints))
        self.setCell(103, str(aLine[1].GamesWon))
        self.setCell(109, '{:4n}'.format(aLine[1].Spread))
        if aLine[1].GamePoints > 11 : self.setCell(120, str(aLine[1].GamePoints))
        if aLine[1].Cash > 0 : self.setCell(130, '{:=3n}'.format(aLine[1].Cash))
        if aLine[1].SkunksTaken > 0 : self.setCell(145, str(aLine[1].SkunksTaken))
        if aLine[1].SkunksGiven > 0 : self.setCell(155, str(aLine[1].SkunksGiven))
        self.pdf.ln(self.texth)
        if rpt.reportLineNumber % 5 == 0 : self.pdf.ln(self.texth)
    def setCell(self, o, text):
        # o is offset from l_margin
        # l is literal to display in cell
        self.pdf.set_x(self.pdf.l_margin + o)
        self.pdf.cell(self.pdf.get_string_width(text), 0, text)
    def printReport(self):
        # set up two multi_cell columns of skunk results stored by Given and Taken
        self.pdf.close()
        self.pdf.output(self.tourneyReportName)
class BuildReportData(object):
    # creates the lines for the tourney report
    def __init__ (self):
        # lineNumber = 0
        print ('cfg.ar: ', cfg.ar)
        print ('rpt tourney record id ', rpt.tourneyRecordId)
        tourneyScoreCards = cfg.ar.allTourneyResults(rpt.tourneyRecordId)
        print ('tourney score cards', tourneyScoreCards)
        # print ('len: TSCs: ,  ', len(tourneyScoreCards), ' ', tourneyScoreCards,  )
        players = list(Player.select())
        pns = [x.Player.id for x in tourneyScoreCards]
        # print ('pns: ', pns)
        # acclist = [ [x.ACCNumber for x in players if x.id == y] for y in pns]
        # print ('acclist: ', acclist)
        playerAccListofLists = [ [[x.id, cfg.playerXref[x.id], x.ACCNumber] for x in players if x.id == y] for y in pns]
        # flatten the list of list
        playerAccList = [item for sublist in playerAccListofLists for item in sublist]
        # print ('playerAccList: ', playerAccList)

        # flatacclist = [x[0] for x in acclist]
        # print ('flatacctlist: ', flatacclist)
        # now build a dictionary keyed by pid for this tourney's results
        playerAccDict = {sublist[0]: sublist for sublist in playerAccList}
        # print ('playerAccDict: ', playerAccDict)
        # pnx = [cfg.playerXref[x] for x in pns]
        # print ('pnx: ', pnx)
        # pny = list(zip( pns, pnx))
        # print ('pny: ', pny)
        # pnz = list(zip(pny, flatacclist))
        # print ('pnz: ', pnz)
        # pnzz = [(x[0][0], x[0][1], x[1]) for x in pnz]
        # print ('pnzz: ', pnzz)
        tsc1 = sorted(tourneyScoreCards, key=lambda tourneyScoreCards : tourneyScoreCards.Spread, reverse = True)
        tsc2 = sorted(tsc1, key=lambda tsc1 : tsc1.GamesWon, reverse=True)
        tsc3 = sorted(tsc2, key=lambda tsc2 : tsc2.GamePoints, reverse=True)
        # print ('tsc3: ', tsc3)
        # TODO: Cannot zip as pnzz is not in tourney results order
        # Build pnzz using playerAccDict ordered by pids in tsc3
        playerIdList = [sc.PlayerID for sc in tsc3]
        # print ('playerIdList: ', playerIdList)
        playerInScoreCardOrder = [ playerAccDict[key] for key in playerIdList]
        # print ('playerInScoreCardOrder:' ,playerInScoreCardOrder)
        rankList = list(range(1, len(playerInScoreCardOrder) + 1))
        # print ('rankList: ', rankList)
        reducedPlayerList = [ [ sc[1], sc[2] ] for sc in playerInScoreCardOrder]
        zippedPlayerList = list (zip(rankList, reducedPlayerList) )
        pnzz = [ [ z[0], z[1][0], z[1][1] ] for z in zippedPlayerList]
        # prePnzz = [ [sc[1],sc[2]] for sc in playerInScoreCardOrder]
        # print ('prePnzz: ', prePnzz)
        # pnzz = zip(rankList,prePnzz)
        # pnzz = [ [r, l[1], l[2] ] for l in playerInScoreCardOrder for r in range(1, len(playerInScoreCardOrder))]
        # print('pnzz:', pnzz)
        tupleRptLines = list(zip(pnzz, tsc3))
        # convert to lists
        listRptLines = [ [list(x[0]), x[1]] for x in tupleRptLines]
        print ('tuplerptLines: ', tupleRptLines)
        print ('listrptlines: ', listRptLines)
        # no ties to resolve in alpha report
        # rpt.reportData = self.handleTies(listRptLines)
        rpt.reportData = sorted(listRptLines, key=lambda x: x[0][1])
        # for aLine in rpt.reportData:
        #     print (aLine)
    def handleTies(self, lines):
        print ('In handleTies')
        newTourneyLines = []
        sL = lines[0]
        newTourneyLines.append(sL)
        for x in range(1, len(lines)):
            tL = list(lines[x])
            if sL[1].GamePoints == lines[x][1].GamePoints and sL[1].GamesWon == lines[x][1].GamesWon and sL[1].Spread == lines[x][1].Spread:
                tL[0][0] = 0
            sL = tL
            newTourneyLines.append(sL)
        return newTourneyLines

if __name__ == '__main__':
    print ('Create tourney report')

    #############################################
    # hardwire cfg for testing                  #
    cfg.appTitle = 'Reports Testing'  #
    cfg.clubNumber = 100  #
    cfg.season = '2024-25'  #
    cfg.clubName = 'Peggers'  #
    rpt.tourneyDate = '2024-10-01'  #
    rpt.tourneyRecordId = 179 #
    rpt.tourneyNumber = 5 #

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
    cfg.playerRefx = { v : k for k, v in cfg.playerXref.items() }
    cfg.clubRecord = Club.get(1)
    cfg.clubId = cfg.clubRecord.id
    cfg.reportDirectory = cfg.clubRecord.reportDirectory
    print ('cfg.reportDirectory: ', cfg.reportDirectory)

    # clubXrefQuery = "select PlayerID, ClubNumber from Player, Club where Player.ClubID = Club.ClubID "
    # cfg.clubXref = {x[0]: x[1] for x in sqlhub.processConnection.queryAll(clubXrefQuery)}
    cfg.clubXref = {x[0]: x[1] for x in cfg.ac.clubXref()}

    club100 = list(Club.select(Club.q.clubNumber == 100))[0]
    rpt.tourneyRecord = cfg.at.returnOneTourney(cfg.clubRecord,
                                                 cfg.season,
                                                 rpt.tourneyNumber)[0]
    print('rpt.tourneyRecord: ', rpt.tourneyRecord)
    # reportData = BuildReportData()
    alphaReport = AlphaReport()
    # tourneyReport.printReport()

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
