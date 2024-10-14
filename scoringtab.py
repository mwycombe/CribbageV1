#scoringtab.py
### Obsolete 1/24/2020
# replaced by resultstab.py
#
#####################################################################
#
#   Creates tab screen for gathering scores
#   Will self-register in notebook found in screenDict of cfg
#
#####################################################################

# System imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg
import copy

from sqlobject import *

import sys as sys
import os as os

# Personal imports
import peggersconfig as cfg
from memplayer import MemPlayer
from memscorecard import MemScoreCard
from memgame import MemGame

class ScoringTab (ttk.Frame):
    # screen class is always a frame

    #************************************************************   
    #
    #   sets up tab for capturing scores cards and games within

    def __init__ (self, parent=None):
        super().__init__( parent)
        self.grid()

        # build out tab and register with notebook
        self.config(padding = '10p')
        parent.add(self, text='Scoring')  
        cfg.screenDict['sctab'] = self
        print ('register sctab')

        #####################################################
        #
        # control variables for GUI
        #
        #####################################################

        cfg.nineGames          = {}    # one set of nine games for a std club tourney
        self.playerToScore = tk.IntVar() # used to capture which player to enter scores for
        ## TODO: see if we should make this playersInTourney to have cross-tab memory of who is being scored.
        
        cfg.gameArray = {}              # array for game score entry
        cfg.enteredGames = {}           # zero out entered games on initialization
        cfg.dirtyScoreCards = {}        # zero out on initialization

        # listbox variables
        self.s_p_names = []             # start with empty dictionary
        ## TODO: this shadows the cfg.s_p_names - why?


        # entry conditions
        # useless to print these at __iniit__ time - will always be empty
        # print ('cfg.s_p_id_names',cfg.s_p_id_names)

        self.pickPlayer = ttk.Frame(self,
                                    relief='sunken',
                                    height='10c',
                                    width ='10c',
                                    padding='10p'
                                    )
        self.pickPlayer.grid(row=0, column=0, sticky='n')
        self.enterScores = ttk.Frame(self,
                                     relief='sunken',
                                     height='10c',
                                     width ='10c',
                                     padding='10p'
                                     )
        self.enterScores.grid(row=0, column=1, sticky='n')

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=4)
        self.gameEntryDetail = ttk.Frame(self.enterScores,
                                         relief='sunken',
                                         height='10c',
                                         width ='10c',
                                         padding='10p'
                                         )
        self.gameEntryDetail.grid(row=1, column=0, sticky='ew')
        self.gameEntryHeader = ttk.Frame(self.enterScores,
                                         relief='sunken',
                                         height='10c',
                                         width ='10c',
                                         padding='10p'
                                         )
        ttk.Label(self.pickPlayer,
                  text='Players in This Tournament'
                  ).grid(row=0, column=0)

        
    #************************************************************
    #   check to see if our tab was selected.
    #
    #   This structure <index(cfg.screenDict['notebook'].select())>
    #   gets the WindowId via parameterless .select() then converts that
    #   into the current tab index (from zero)
    #
    def tabChange(self,event):
        # populate the tab whenever we get selected
##        if cfg.screenDict['notebook'].index(cfg.screenDict['notebook'].select()) == 4:
        print('**ScoringTab got the notebook changed event***')

        #   is lost.
        #   We need to make sure we save incremental input, and, when this tab is re-selected,
        #   make sure we re-display the information entered to date.
        #
        #   When the user selects a particular player to score, then the prior entered scores
        #   should re-populate the score card.
        
        self.buildScoringPanel()

        
    #************************************************************
    #   Populate scoring panel
    #
    def buildScoringPanel(self):
       
        r = 1
        for k in cfg.s_p_id_names:
            ttk.Radiobutton(self.pickPlayer,
                            text=cfg.s_p_id_names[k],
                            value=k,
                            variable=self.playerToScore,
                            command=self.scoreThisPlayer,
                            ).grid(row=r, column=0, sticky='w')
            r += 1     

        
    #************************************************************
    #   Read the players id from the Radiobutton and setup scoring panel
    #
    def scoreThisPlayer(self):
        print('Score player:= ' + str(self.playerToScore.get())
              + ' '
              + cfg.s_p_id_names[self.playerToScore.get()])
        
        # this is where the radio button comes when a player is selected

        self.buildGameEntry()
        
    #************************************************************
    #   Build out game entry panel for selelcted player

    def buildGameEntry(self):

       
        self.gameEntryHeader.grid(row=0, column=0, sticky='n')
        
        ttk.Label(self.gameEntryHeader,
                  text='Player Name'
                  ).grid(row=0, column=1, sticky='ew')
        ttk.Label(self.gameEntryHeader,
                  text='Seat No.'
                  ).grid(row=0, column=2, sticky='ew')
        ttk.Label(self.gameEntryHeader,
                  text=cfg.s_p_id_names[self.playerToScore.get()],
                  relief='raised',padding='10p'
                  ).grid(row=1, column=1, sticky='ew')
        ttk.Label(self.gameEntryHeader,
                  text=cfg.seatAssignments[self.playerToScore.get()],
                  relief='raised',padding='10p'
                  ).grid(row=1, column=2, sticky='ew')
        ttk.Label(self.gameEntryHeader,
                  text='(Note: Players can play each other more than once at Seniors)'
                  ).grid(row=2, column=1, columnspan=2)


        
        ttk.Label(self.gameEntryDetail,text='Cut Card').grid(row=0, column=0)
        ttk.Label(self.gameEntryDetail,text='Game').grid(row=0, column=1)
        ttk.Label(self.gameEntryDetail,text='Points').grid(row=0, column=2)
        ttk.Label(self.gameEntryDetail,text='Plus').grid(row=0, column=3)
        ttk.Label(self.gameEntryDetail,text='Minus').grid(row=0, column=4)
        ttk.Label(self.gameEntryDetail,text='Opp Seat').grid(row=0, column=5)
        self.gameErrorHeader = ttk.Label(self.gameEntryDetail,text=' Errors')
        self.gameErrorHeader.grid(row=0, column=6)

        if self.playerToScore.get() in cfg.dirtyScoreCards:
            print('Call buildGameArray dirtyScoreCards for player ',self.playerToScore.get())
            self.buildGameArray(cfg.dirtyScoreCards[self.playerToScore.get()])
        elif self.playerToScore.get() in cfg.enteredScoreCards:
            print('Call buildGameArray with enteredScoreCards for player ', self.playerToScore.get())
            self.buildGameArray(cfg.enteredScoreCards[self.playerToScore.get()])
        else:
            print('Call buildGameArray with no source for player ', self.playerToScore.get())
            self.buildGameArray()   # build new gameArray from empty
        ttk.Button(self.enterScores,
                   text='Read Scores',
                   command=self.readScores
                   ).grid(row=2, column=0)
        
    #************************************************************
    #
    def buildGameArray(self, memscs=None):
        cfg.gameArray = {}      # used to track screen fields
        

        for r in range (1,10):
            varList = []
            varList.append(tk.StringVar())
            varList.append(tk.IntVar())
            varList.append(tk.IntVar())
            varList.append(tk.IntVar())
            varList.append(tk.IntVar())
            varList.append(tk.StringVar())

            if memscs == None:
                # build empty list
                print ('Build empty gameArray')
                pass
            else:   # build from source
                if r in memscs.games:
                    varList[0].set(memscs.games[r].cutCard)
                    varList[1].set(memscs.games[r].gamePoints)
                    if memscs.games[r].spreadPoints > 0:
                        varList[2].set(memscs.games[r].spreadPoints)
                        varList[3].set(0)
                    else:
                        varList[2].set(0)
                        varList[3].set(-memscs.games[r].spreadPoints)
                    varList[4].set(memscs.games[r].opponentSeat)

            cfg.gameArray[r] = varList
            # cut card
            ttk.Entry(self.gameEntryDetail,
                      textvariable=cfg.gameArray[r][0],
                      width=3).grid(row=r+1, column=0)
            # game number
            ttk.Label(self.gameEntryDetail,
                      text=str(r),
                      width=3).grid(row=r+1, column=1)
            # game points
            ttk.Entry(self.gameEntryDetail,
                      textvariable=cfg.gameArray[r][1],
                      width=3).grid(row=r+1, column=2)
            # plus spread
            ttk.Entry(self.gameEntryDetail,
                      textvariable=cfg.gameArray[r][2],
                      width=3).grid(row=r+1, column=3)
            # minus spread
            ttk.Entry(self.gameEntryDetail,
                      textvariable=cfg.gameArray[r][3],
                      width=3).grid(row=r+1, column=4)
            # opp seat number
            ttk.Entry(self.gameEntryDetail,
                      textvariable=cfg.gameArray[r][4],
                      width=3).grid(row=r+1, column=5)
            # error type
            ttk.Label(self.gameEntryDetail,
                      textvariable=cfg.gameArray[r][5],
                      width=15).grid(row=r+1, column=6)

        # hide error header for now
        self.gameErrorHeader.grid_remove()
        
    #************************************************************
    #
    def readScores(self):
        print('Scores for:= ' + cfg.s_p_id_names[self.playerToScore.get()])
        for g in range (1,10):
            print('Cut Card: ' + cfg.gameArray[g][0].get()
                  + ' Game: ' + str(g)
                  + ' Points: ' + str(cfg.gameArray[g][1].get())
                  + ' Plus: ' + str(cfg.gameArray[g][2].get())
                  + ' Minus: ' + str(cfg.gameArray[g][3].get())
                  + ' Opp Seat: ' + str(cfg.gameArray[g][4].get())
                  )
        #
        # Validate lines - save games in cfg.dirtyScoreCards = move to touryneyScoreCards when validated
        # save unverified game array in dirtyScoreCards
        # saveverified games  entered in cfg.tourneyScoreCardsfor reshowing/adding/correcting

        if self.playerToScore.get() in cfg.enteredScoreCards:
            # delete the old score card 'cause we're going to replace it
            del cfg.enteredScoreCards[self.playerToScore.get()]

        gameErrors = self.validateGameScores()
        if gameErrors:
            # somewhere there are errors to show - show the column header
            # leave 
            self.gameErrorHeader.grid()
            for g in self.errorArray:
                if self.errorArray[g]:
                    errorString = self.decodeErrorCode(self.errorArray[g])
                    self.showErrorString(g,errorString)
            self.buildMemScoreCard(self.playerToScore.get(), cfg.gameArray, cfg.dirtyScoreCards)
        else:
            # no errors found so build MemGame and MemScorecard
            # Now we build the in-memory representation for this score card and games for this player
            self.gameErrorHeader.grid_remove()
            self.buildMemScoreCard (self.playerToScore.get(), cfg.gameArray, cfg.enteredScoreCards)
            if self.playerToScore.get() in cfg.dirtyScoreCards:
                del cfg.dirtyScoreCards[self.playerToScore.get()]   # clean out saved dirty score cards

    #************************************************************
    #   return string that informs errors

    def decodeErrorCode(self, eCode):
        eString = ''
##        print('eCode ' + str(eCode))
        if (eCode % 2) == 1:
            eString = 'Pts '
            eCode -= 1
##            print('eCode ' + str(eCode))
        if (eCode // 8) == 1:
            eString += 'Cut '
            eCode -= 8
##            print('eCode ' + str(eCode))
        if (eCode // 4) == 1:
            eString += 'Seat '
            eCode -=4
##            print('eCode ' + str(eCode))
        if eCode // 2:
            eString += '+/- '
        print('eString: ' + eString)
        return eString
           
    #************************************************************
    # show the error string for a game line

    def showErrorString(self, g, eString):
        # all that's neededis to put the string to be displayed into the control variable
        cfg.gameArray[g][5].set(eString)

    #************************************************************
    #   build in-memory score card for a given player's validated game lines.

    def buildMemScoreCard(self, playerId, gameArray, target):
        # memory score card is build and deposited whereever the target points
        # which should be cfg.dirtyScoreCards or cfg.tourneyScoreCards
        print('Build memory score card')
        print('cfg.tourneyRecordId: ' + str(cfg.tourneyRecordId))
        cfg.tourneyScoreCards[playerId] = MemScoreCard(cfg.tourneyRecordId, playerId, cfg.seatAssignments[playerId])

        # build up to nine games to associate with this scorecards
        # k:v game number : MemGame instance
        cfg.nineGames = {}     # clear out the games dict
        
        for x in range(1,10):
            print ('gameArray[x][4].get() (Opp seat no) := ', gameArray[x][4].get() )
            if gameArray[x][4].get() > 0: # was there any opponent seat? (only for seniors)
                if gameArray[x][2].get() > 0 :
                    self.spread = gameArray[x][2].get()    # this was a win
                else:
                    self.spread = -gameArray[x][3].get()   # this was a loss
                cfg.nineGames[x] = MemGame(game = x,
                                            points = gameArray[x][1].get(),
                                            spread = self.spread,
                                            opponent = gameArray[x][4].get(),
                                            cutCard = gameArray[x][0].get().upper()
                                            )
            
        # plug the nine game array into the in-memory score card

        self.memScoreCard = MemScoreCard(cfg.tourneyRecordId,
                                         playerId,
                                         seat = cfg.seatAssignments[playerId]
                                         )
        self.memScoreCard.games = copy.deepcopy(cfg.nineGames)
        # remove line below which would be a shallow copy
        # self.memScoreCard.games = cfg.nineGames    # put all nine MemGames into the MemScoreCard
        
        target[playerId] = self.memScoreCard     # save the score card for validation
        print('MemCard ', target[playerId])

    #************************************************************
    #   check that each line has valid entries that are in range and self-consistent
    #   all-zero lines are permitted for Senior Tourney

    def validateGameScores(self):
        anyError = 0
        self.errorArray = {}
        self.pointsDict = {0:0,2:2,3:3}
        self.cardDict = {'A':'A','1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':'J','Q':'Q','K':'K',
                         'a':'A','j':'J','q':'Q','k':'K'}
        self.errorDict = {'NoError':0,
                      'Points':1,
                     'PlusMinus':2,
                     'Seat':4,
                     'Cut':8,
                     }


            
        for g in cfg.gameArray:
            if self.allZeroLine(g):
                # that's ok for Seniors
                self.errorArray[g] = 0
                break
            self.errorArray[g]  = self.validatePoints(g)
            self.errorArray[g] += self.validatePlusMinus(g)
            self.errorArray[g] += self.validateSeat(g)
            self.errorArray[g] += self.validateCut(g)

            anyError = self.errorArray[g]

        return anyError
        
        
    #************************************************************            
    #   for Seniors - allowable

    def allZeroLine (self, g):
        return (cfg.gameArray[g][1].get() == 0 and
                cfg.gameArray[g][2].get() == 0 and
                cfg.gameArray[g][3].get() == 0 and
                cfg.gameArray[g][4].get() == 0
                )

    #************************************************************
    #   check a game line for point errors

    def validatePoints(self,g):
        # save values we want to test
        points = cfg.gameArray[g][1].get()
        plus   = cfg.gameArray[g][2].get()
        minus  = cfg.gameArray[g][3].get()
        seat   = cfg.gameArray[g][4].get()
        print ('Pts ' + str(points) + ' + ' + str(plus) + ' - ' +  str(minus) +' seat ' + str(seat))
        
        if (points not in self.pointsDict) or (points == 2 and plus > 30) or (points == 3 and plus < 31):
##            print('Pts error')
            return self.errorDict['Points']
        else:
            return self.errorDict['NoError']

    #************************************************************
    # check a game line for plus/minus errors

    def validatePlusMinus(self,g):
        # save values we want to test
        points = cfg.gameArray[g][1].get()
        plus   = cfg.gameArray[g][2].get()
        minus  = cfg.gameArray[g][3].get()
        seat   = cfg.gameArray[g][4].get()

        if (plus == 0 and minus == 0) or(plus == 0 and minus == 0) or(points == 2 and plus == 0) or (points == 2 and plus > 30) or (points == 3 and plus < 31):
##            print ('+/- error')
            return self.errorDict['PlusMinus']
        else:
            return self.errorDict['NoError']

    #************************************************************
    # check a game line for seat errors

    def validateSeat (self, g):
        # save value we want to test
        seat   = cfg.gameArray[g][4].get()
        print ('cfg.seatsBySeat:= ',cfg.seatsBySeat)
        if seat not in cfg.seatsBySeat:
##            print('Seat:= ' + str(seat))
##            print(cfg.seatsBySeat)
##            print('Seat error')
            return self.errorDict['Seat']
        elif seat == cfg.seatAssignments[self.playerToScore.get()]:
            # we played ourself!
            return self.errorDict['Seat']
        else:
            return self.errorDict['NoError']

    #************************************************************
    # check a game line for cut card error

    def validateCut (self, g):
        cutCard = cfg.gameArray[g][0].get()
        # missing cutCard is ok
##        print ('CutCard:= ' + cutCard)
        if cutCard == '' or cutCard in self.cardDict:
            return self.errorDict['NoError']
        else:
##            print('Cut error')
            return self.errorDict['Cut']






