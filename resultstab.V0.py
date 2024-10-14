# resultstab.py
# 7/21/2020 updated to cribbageconfig
# cloned from and replaces scoringtab.py
#
#####################################################################
#
#   Creates tab screen for gathering scores
#   Will self-register in notebook found in screenDict of cfg
#
#####################################################################
#   TODO:   Replace in situ entry/edit with pull out line above results
#   TODO:   Replace scrolling canvas with synced listboxes
#   TODO:   Allow new entry, old edit, old delete
#   TODO:   Support odd player count with imbalance of spread points and skunks
#   TODO:   Show cash totals
#   TODO:   Allow test commit/final commit for a tourney - needed for odd player count
#   TODO:   when we finish a results line entry and hit enter at the end of the line
#           have to hit Left to get back to select a player - mouse button doesn't work
#           on list of players.
#           Also, there is no visual clue that the results have been accepted
#   TODO:   When results line is accepted upon enter, Count of players is never updated
#           though player points get shown ok
#   TODO:   When results rolls off the bottom of the srcollable area, need to shift
#           focus to the last new entry so we can key in results
#   TODO:   If any results exist for a tourney then update the entered indicator in tourney row

# System imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg

from sqlobject import *

import sys
import os

# Personal imports
import cribbageconfig as cfg
from masterscreen import MasterScreen

from player import Player
from tourney import Tourney
from scorecard import ScoreCard
from club import Club
from verticalscrolledframe import VerticalScrolledFrame

class ResultsTab(tk.Frame):
    # screen class is always a frame


    #   sets up tab for capturing scores cards and games within

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid()

        # control variables for results tab
        #
        # build out tab and register with notebook
        self.config(padx = '5', pady = '5')
        parent.add(self, text='Results Panel')
        cfg.screenDict['rsltab'] = self
        print('register rsltab')

        # control variables
        self.count = tk.IntVar()
        self.tourneyDate = tk.StringVar()
        self.tourneyNumber = tk.IntVar()
        self.plusSpread = tk.IntVar()
        self.minusSpread = tk.IntVar()
        self.diffSpread = tk.IntVar()
        self.givenSkunks =  tk.IntVar()
        self.takenSkunks = tk.IntVar()
        self.diffSkunks = tk.IntVar()

        # initialize restults tracking variables
        self.plusSpread.set(0)
        self.minusSpread.set(0)
        self.diffSpread.set(0)
        self.givenSkunks.set(0)
        self.takenSkunks.set(0)
        # used to display progress of scoring
        self.playerList = tk.StringVar()
        self.playerPoints = tk.StringVar()

        #####################################################
        #
        #   control variables for GUI
        #
        #####################################################

        #####################################################
        #
        #   set up the panels and areas for selecting players
        #   for this tournament and enterering their results
        #
        #####################################################

        self.results = tk.LabelFrame(self,
                                           relief = 'sunken',
                                           height='10c',
                                           width='5c',
                                           padx = '10', pady ='10',
                                           text='Results Panel'
                                            )
        self.results.grid(row=0, column=0, sticky='nsew')

        # set up player selection
        self.tourneyHeaderPanel = tk.Frame(self.results,
                                            relief='flat',
                                            padx = '5', pady ='5'
                                            )
        self.tourneyHeaderPanel.grid(row=0, column=0, sticky='nsew')

        self.resultsHeaderPanel = tk.Frame(self.results,
                                       relief='flat',
                                       padx = '5', pady ='5')
        self.resultsHeaderPanel.grid(row=0, column=1, sticky='nsew')


        # now set up the scrolled panels - clones from results1.py
        self.playerPanel = tk.LabelFrame(self.results,
                                          relief='sunken',
                                          height='10c',
                                          width='10c',
                                          padx = '5', pady='5',
                                          text='Select Players')
        self.playerPanel.grid(row=1, column=0, sticky='nsew')

        self.resultsPanel = tk.LabelFrame(self.results,
                                           relief='sunken',
                                           height='10c',
                                           width='5c',
                                           padx = '5', pady ='5',
                                           text='Enter Results')
        self.resultsPanel.grid(row=1, column=1, sticky='nsew')

    # ************************************************************
    #   check to see if our tab was selected.
    #
    #   This structure <index(cfg.screenDict['notebook'].select())>
    #   gets the WindowId via parameterless .select() then converts that
    #   into the current tab index (from zero)
    #
    def tabChange(self, event):
        # populate the tab whenever we get selected
        ##        if cfg.screenDict['notebook'].index(cfg.screenDict['notebook'].select()) == 4:
        print('**Resultstab got the notebook changed event***')

        # this has to be deferred until after the tourney date has been selected
        self.buildActivityPanel()
        self.buildScoringPanels()

        #   TODO:   Provide the future ability to sort various ways.

    def buildActivityPanel(self):
        MasterScreen.wipeActivityPanel()
        self.ap = cfg.screenDict['activity']

        self.resultsLabels = tk.Frame(self.ap,
                                       relief='flat',
                                       padx = 5, pady ='5'
                                      )
        self.resultsTotals = tk.Frame(self.ap,
                                     relief='flat',
                                     padx='5', pady='5')
        self.resultsLabels.grid(row=0, column=0, sticky='ew')
        self.resultsTotals.grid(row=0, column=1, stick='nw')

        self.plusLabel = tk.Label(self.resultsTotals,
                                   text='Plus ')
        self.minusLabel = tk.Label(self.resultsTotals,
                                    text='Minus')
        self.diffLabel = tk.Label(self.resultsTotals,
                                   text='Diff')

        self.ph1 = tk.Label(self.resultsTotals,
                             width=5,
                             text=' ')
        self.ph2 = tk.Label(self.resultsTotals,
                             width=5,
                             text=' ')
        self.reCalc = tk.Button(self.resultsTotals,
                                 text='ReCalc',
                                 command=self.reCalc)
        self.plusLabel.grid(row=0, column=1)
        self.minusLabel.grid(row=0, column=2)
        self.diffLabel.grid(row=0, column=3)

        self.ph2.grid(row=0, column=4)
        self.reCalc.grid(row=0, column=5)

        self.spreadLabel = ttk.Label(self.resultsTotals,
                                     text='Spread')
        self.skunksLabel = ttk.Label(self.resultsTotals,
                                     text='Skunks')
        self.spreadLabel.grid(row=1, column=0, sticky='w')
        self.skunksLabel.grid(row=2, column=0, sticky='w')


        self.plusSpreadLabel = tk.Label(self.resultsTotals,
                                        background = 'white',
                                        width = 4,
                                        textvariable = self.plusSpread)
        self.minusSpreadLabel = tk.Label(self.resultsTotals,
                                          background = 'white',
                                          width = 4,
                                          textvariable = self.minusSpread)
        self.diffSpreadLabel = tk.Label(self.resultsTotals,
                                         background = 'white',
                                         width = 3,
                                         textvariable = self.diffSpread)
        self.givenSkunksLabel = tk.Label(self.resultsTotals,
                                          background = 'white',
                                          width = 3,
                                          textvariable = self.givenSkunks)
        self.takenSkunksLabel = tk.Label(self.resultsTotals,
                                          background = 'white',
                                          width = 3,
                                          textvariable = self.takenSkunks)
        self.diffSkunksLabel = ttk.Label(self.resultsTotals,
                                         background = 'white',
                                         width = 3,
                                         textvariable = self.diffSkunks)
        self.plusSpreadLabel.grid(row = 1, column = 1, sticky = 'w')
        self.minusSpreadLabel.grid(row = 1, column = 2, sticky = 'w')
        self.diffSpreadLabel.grid(row = 1, column = 3, sticky = 'w')
        self.givenSkunksLabel.grid(row = 2, column = 1, sticky = 'w')
        self.takenSkunksLabel.grid(row = 2, column = 2, sticky = 'w')
        self.diffSkunksLabel.grid(row = 2, column = 3, sticky = 'w')



    def buildScoringPanels(self):
        # TODO: This is where we will build the verticalscrolledscreen canvases, retrieving everything
        #       from the sqlobject dbms.
        #       Upon reentry, need to ensure that prior display is vanished
        #
        self.tourneyDateLabel = ttk.Label(self.tourneyHeaderPanel,
                                       text='Tourney Date:')
        self.tourneyDateLabel.grid(row=0, column=0, sticky='w')
        self.tourneyNumberLabel = ttk.Label(self.tourneyHeaderPanel,
                                            text='Tourney No.')
        self.tourneyNumberLabel.grid(row=1, column=0, sticky='w')
        self.tourneyDate.set(cfg.tourneyDate)
        self.tourneyDateValue = ttk.Label(self.tourneyHeaderPanel,
                                          background = 'white',
                                          textvariable=self.tourneyDate)
        self.tourneyDateValue.grid(row=0, column=1)
        self.tourneyNumber.set(cfg.tourneyNumber)
        self.tourneyNumberValue = ttk.Label(self.tourneyHeaderPanel,
                                            background = 'white',
                                            textvariable=self.tourneyNumber)
        self.tourneyNumberValue.grid(row=1, column=1, sticky = 'w')
        self.countLabel = ttk.Label(self.tourneyHeaderPanel,
                                    text='Count:   ')
        self.countLabel.grid(row=2, column=0, sticky='w')
        # count of results for selected tourney
        print('cfg.tourneyRecord: ', type(cfg.tourneyRecord))
        print('cfg.tourneyRecord: ',cfg.tourneyRecord )
        print('cfg tourneyRecordId: ', cfg.tourneyRecordId)
        self.count.set(cfg.ar.countTourneyResults(cfg.tourneyRecord))
        self.playerCount = ttk.Label(self.tourneyHeaderPanel,
                                     background = 'white',
                                     textvariable=self.count)
        self.playerCount.grid(row=2, column=1, sticky='w')

        # TODO: Update count after every input of line of results.

        self.createWidgets()


        # def scoreThisPlayer(self):
        # 	print('Score player:= ' + str(self.playerToScore.get())
        # 	      + ' '
        # 	      + cfg.s_p_id_names[self.playerToScore.get()])
        #
        # 	# this is where the radio button comes when a player is selected
    def computeDifferences(self):
        # just compute the running differences
        # this means the ctrl variables are IntVar type
        self.diffPoints.set(self.plusPoints.get() - self.minusPoints.get())
        self.diffSkunks.set(self.givenSkunks.get() - self.takenSkunks.get())

        # def buildPlayerPanel(self):
        #     super().__init__(master)
        #     self.createPlayerXref()
        #     self.create_widgets()
        #     self.grid(row=0, column=0)
        #     self.listOfPlayers = []
        #     self.listOfResults = []
        #     self.populatePframe()
        #     self.populateRframe()
        #     self.createPlayerXref()
    def returnFromResultsPanel(self):
        # self.create_widgets()        # just rebuild everything
        self.populatePframe()
    def createWidgets(self):
        # p prefix is for players
        # r prefix is for results
        ######################################################################
        #####Tricky task of creating players game points with names
        #
        #   cfg.clubRecord should be set to club999 object
        #   cfg.playerXrefById = {p.id : p.LastName + ', ' + p.FirstName
        #       for p in ap.playersByLastName(cfg.clubRecord)
        #
        ##### cfg.tourneyRecord holds record for tourney being scored
        ##### Pull in the latest set of scores from the dbms - always
        ##### refresh this on entry as we may have come from the
        ##### another tab
        #   self.allTourneyResults = ar.allTourneyResults(cfg.tourneyRecord)
        #
        ##### the gathering of GamePoints and PlayerIds from the
        ##### allTourneyResults relies on the accumption that
        ##### the processing of the list of allTourneyResults
        ##### returns the record objects in the same order each time
        ##### and, both lists will be the same length
        #
        #   playerPoints = [x.GamePoints for x in self.allTourneyResults]
        #   playerIdList = [x.Player.id for x in self.allTourneyResults]
        #   pointDict = {k:v for (k,v) in zip(playerIdList, playerPoints)}
        #
        ##### Generate the list of names for playerIds with scores
        #
        #   pointsNameList = [cfg.playersXrefById[x] for x in list(pointDict.keys()]
        #
        ##### and the final merge gives us dictionary keyed by display name
        ##### with value as the gamepoints scored.
        ##### Same method will work for spread, games won, skunksgiven or
        ##### taken and cash.
        #
        #   pointsByName = { k:v for (k,v) in zip(pointsNameList, list(pointDict.values())}
        #
        ##### phewww....
        ######################################################################
        # Start by allocating the two verticalscrolledframes inside the
        # playerPanel and resultsPanel - then populate them
        self.pPanel = ttk.LabelFrame(self.playerPanel)
        self.pPanel.grid(row = 0, column = 0, sticky = 'ew')
        self.pFrame = VerticalScrolledFrame(self.pPanel)
        self.pFrame.pack(side=tk.LEFT)
        self.pFrame.rowconfigure(0,weight=1)
        self.pFrame.columnconfigure(0,weight=1)
        print ('pFrame: ', self.pFrame)
        # self.label = ttk.Label(text="Shrink the window to activate the scrollbar.")
        # self.label.pack()
        self.pFrame.interior.config(height='10c', width='5c')
        # self.pFrame.interior.grid_propagate(0)
        # add our own special tag to the interior frame
        newtags = ('pKeyEvent',) + self.pFrame.interior.bindtags()
        self.pFrame.interior.bindtags(newtags)
        ##############################
        #
        # put results header frame above results frame
        #
        self.rHdrPanel = ttk.LabelFrame(self.resultsPanel)
        self.rHdrPanel.grid(row = 0, column = 0, stick = 'ew')
        self.rDtlPanel = ttk.LabelFrame(self.resultsPanel)
        self.rDtlPanel.grid(row = 1, column = 0)

        self.rFrame = VerticalScrolledFrame(self.rDtlPanel)
        self.rFrame.pack(side=tk.LEFT)
        self.rFrame.rowconfigure(0, weight=1)
        self.rFrame.columnconfigure(1,weight=1)

        #
        # totals section - running totals of points and skunks and spreads
        #
        self.nameHdr = ttk.Label(self.rHdrPanel,
                                  text = 'Names',
                                  font=('Helvetica', '8', 'bold'),
                                  width = 24)
        self.gpHdr = ttk.Label(self.rHdrPanel,
                               text = 'Gp',
                               font=('Helvetica', '8', 'bold'),
                               width = 6)
        self.gwHdr = ttk.Label(self.rHdrPanel,
                               text = 'Gw',
                               font=('Helvetica', '8', 'bold'),
                               width = 5)
        self.sprdHdr = ttk.Label(self.rHdrPanel,
                                 text = 'Sprd',
                                 font=('Helvetica', '8', 'bold'),
                                 width = 6)
        self.cashHdr = ttk.Label(self.rHdrPanel,
                                 text = " $'s",
                                 font=('Helvetica', '8', 'bold'),
                                 width = 6)
        self.tknHdr = ttk.Label(self.rHdrPanel,
                                text = ''
                                       'Tkn',
                                font=('Helvetica', '8', 'bold'),
                                width = 6)
        self.gvnHdr = ttk.Label(self.rHdrPanel,
                                text = ' Gvn',
                                font=('Helvetica', '8', 'bold'),
                                width = 6)
        self.nameHdr.grid(row = 0, column = 0, sticky = 'ew')
        self.gpHdr.grid(row = 0, column = 1, sticky = 'ew')
        self.gwHdr.grid(row = 0, column = 2, sticky = 'ew')
        self.sprdHdr.grid(row = 0, column = 3, sticky = 'ew')
        self.cashHdr.grid(row = 0, column = 4, sticky = 'ew')
        self.tknHdr.grid(row = 0, column = 5, sticky = 'ew')
        self.gvnHdr.grid(row = 0, column = 6, sticky = 'ew')
        #
        # details section
        #
        self.listOfPlayers = []
        self.listOfResults = []

        self.tourneyResultsCount = cfg.ar.countTourneyResults(cfg.tourneyRecord)
        self.tourneyResults = []
        self.gp = []
        self.gw = []
        self.sprd = []
        self.cash = []
        self.taken = []
        self.given = []         # these are computed

        # self.createPlayerXref() # class method in peggersstartup
    #
    # and now populated these scrolled panels
    # (see resultpanel1.py in MyPyFiles for reference to a working version
    #
        self.populatePframe()
        self.populateRframe()
        self.updateTotals()

    def reCalc(self):
        # cheap way - just re-display everything like we had entered
        self.buildScoringPanels()
    def populatePframe(self):
        self.textIndex = 2      # index of name text in pframe child
        self.allPlayerObjects = cfg.ap.playersByLastName(cfg.clubRecord)
        self.listOfPlayerNames = [pn.LastName + ', ' + pn.FirstName for pn in self.allPlayerObjects]
        self.allTourneyResultObjects = cfg.ar.allTourneyResults(cfg.tourneyRecord)
        self.tourneyPointsList = [sc.GamePoints for sc in self.allTourneyResultObjects]
        self.tourneyIdList =[sc.Player.id for sc in self.allTourneyResultObjects]
        self.idPointsDict = {k:v for (k,v) in zip(self.tourneyIdList, self.tourneyPointsList)}
        self.namePointsDict = {}
        for name in self.listOfPlayerNames:
            self.namePointsDict[name] =  self.idPointsDict.get(cfg.playerRefx[name], -1)
        # namePointDict is now a dictionary in name order with points for the
        # current tournament score card or-1. Cannot use 0 as 0 is a valid game
        # points total when a player has a sting of pearls
        self.listOfPoints = []
        if len(self.listOfPlayers) > 0:
            # destroy all prior singlePlayerFrames that were grided
            for spf in self.listOfPlayers:
                spf.destroy()
        print ("List of allPlayerObjects size: ", len(self.allPlayerObjects))
        for p in self.allPlayerObjects:
            singlePlayerFrame = ttk.Frame(self.pFrame.interior)
            spn = p.LastName + ', ' + p.FirstName
            spp = self.namePointsDict[spn]
            if spp < 0:
                playerGamePoints = ttk.Label(singlePlayerFrame,
                                             text = '',
                                             borderwidth = 3,
                                             width = 4)
            else:
                playerGamePoints = ttk.Label(singlePlayerFrame,
                                             text = spp,
                                             borderwidth = 3,
                                             width = 4)
                self.hilite(playerGamePoints)
            spacer = ttk.Label(singlePlayerFrame,
                               text = '  ',
                               width = 2)
            singlePlayerName = ttk.Label(singlePlayerFrame,
                                     text = spn)
            playerGamePoints.grid(row=0, column=0)
            spacer.grid(row=0, column=1)
            singlePlayerName.grid(row=0, column=2)
            self.listOfPlayers.append(singlePlayerFrame)
            # this stacks the last singlePlayerFrame into the next available row by default
            self.listOfPlayers[-1].grid(column=0,sticky='nw')
            # self.listOfPlayers[-1].grid( column=0, sticky='ns')
            # self.listOfPlayers[-1].pack()
        # set the internal verticalscroll bar interior frame indexes
        print ('canvas  height: ', self.pFrame.canvas.winfo_height())
        print ('interior height: ', self.pFrame.interior.winfo_height())
        print ('interior req_height: ', self.pFrame.interior.winfo_reqheight())
        self.pFrame.activeIndex = 0
        self.pFrame.topIndex = 0
        self.pFrame.bottomIndex = len(self.pFrame.interior.winfo_children())-1
        print('Top p index: ', self.pFrame.topIndex)
        print('Bottom p Index: ',self.pFrame.bottomIndex)

        # set up interior to capture key events
        # force keyboard focus onto interior player frame
        self.pFrame.interior.focus_force()

        # show the first name as current
        self.hiLiteActiveName(self.pFrame.activeIndex)
        self.pFrame.canvas.config(scrollregion = self.pFrame.canvas.bbox('all'))

        def _pkeyCapture(keyEvent):
            #################################################
            #   handle the key input events
            #   actions depend on the activeindex that tracks
            #   logically which entry we are in as we are not using
            #   a listbox.
            #   Down:   Advance to next name entry unless already at bottom
            #   Up:     Go up to prior name entry unless already at top
            #   Return: Select the name and go to Results page to create
            #           a new results line at the bottom for this name
            #           Or, check if name is already on results page and
            #           position at that line
            #   Right:  Switch to results frame, position on first entry
            #################################################
            print('Captured key: ', keyEvent.keysym)
            # print('Event x:y:= ', keyEvent.x, ':', keyEvent.y)
            if keyEvent.keysym == 'Down':
                if self.pFrame.activeIndex < self.pFrame.bottomIndex:
                    self.hiLiteNextName(self.pFrame.activeIndex)
                    self.pFrame.activeIndex += 1
                else:
                    self.hiLiteActiveName(self.pFrame.activeIndex)
                # otherwise, we must be at the bottom entry so just stay there
            elif keyEvent.keysym == 'Up':
                if self.pFrame.activeIndex > self.pFrame.topIndex:
                    self.hiLitePriorName(self.pFrame.activeIndex)
                    self.pFrame.activeIndex -= 1
                # else we are at the top slot so just stay there
            elif keyEvent.keysym == 'Return':
                print('Copy current entry to results frame')
                self.goToResultsPanel(self.pFrame.interior.winfo_children()[self.pFrame.activeIndex].winfo_children()[2]['text'])
                # copies the current line or positions at existing entry line
            elif keyEvent.keysym == 'Right':
                print('Switch to results frame')
                # does not copy the current entry
                self.positionInResultsAtTop()  # results, first line, first field

            elif keyEvent.char.isalpha():
                print(keyEvent.char.upper(), ' key pressed')
                print('ActiveIndex: ', self.pFrame.activeIndex)
                if self.pFrame.activeIndex >= self.pFrame.bottomIndex:
                    self.searchFromTop(self.pFrame.interior, keyEvent.char.upper())
                elif self.currentSlotMatches(self.pFrame.activeIndex, keyEvent.char.upper()):
                    if self.nextSlotMatches(self.pFrame.activeIndex, keyEvent.char.upper()):
                        self.hiLiteNextName(self.pFrame.activeIndex)
                        self.pFrame.activeIndex += 1
                    else:
                        self.searchFromTop(self.pFrame.interior, keyEvent.char.upper())
                else:
                    self.searchFromTop(self.pFrame.interior, keyEvent.char.upper())
            else:
                print('non alpha key: ', keyEvent.char)
            return 'break'  # this stops any other bindings from firing.

            # bind_class binds to our local keyevent tag - any key pressed
            # notice we don't use self.cmd as the even handler is inside the create-widgets command
            # and, the event handler is bound after definition of the event handler

        self.pFrame.interior.bind_class('pKeyEvent', '<KeyPress>', _pkeyCapture)
    def populateRframe(self):
        # if len(self.listOfResults) > 0:
        #     for lor in self.listOfResults:
        #         lor.destroy()
        self.resultFrameIndex = 0
        # self.listOfResults = []     # and clear out the list
        if self.tourneyResultsCount > 0:
            self.tourneyResults = cfg.ar.tourneyResultsInEntryOrder(cfg.tourneyRecord)
        for r in self.tourneyResults:
            singleResultFrame = ttk.Frame(self.rFrame.interior)
            self.buildResultLine (singleResultFrame,r,self.resultFrameIndex)
            self.listOfResults.append(singleResultFrame)
            self.listOfResults[-1].grid(column=0, sticky='n')
            self.resultFrameIndex += 1
    def goToResultsPanel(self,playerName):
        # check for existing player line entry - look through tourneyResults for playerid
        # first clear out and repopulate rframe - let populateRframe do thi
        # self.populateRframe()
        existingResultIndex = self.locatePlayerResult(playerName)
        if existingResultIndex < 0:
            self.addNewResultLine(playerName)
        else:
            # if not, add an empty line at the bottom of the results panel
            self.positionAtPlayerNameResult(existingResultIndex)
    def positionAtPlayerNameResult(self, eridx):
        self.positionAt(eridx, 1)       # first entry field in the existing row
    def locatePlayerResult(self,playerName):
        pidx = 0
        for spf in self.rFrame.interior.winfo_children():
            print('spf children: ', spf)
            if playerName == spf.winfo_children()[0]['text']:
                return pidx
            pidx += 1
        return -1
    def addNewResultLine(self,playerName):
        # TODO: If we add a new line, position the focus at this line and set the focus
        # create a new single result frame with an empty entry
        # and push it onto the end of interior frame children
        rframe = ttk.Frame(self.rFrame.interior)
        resultFrameIdx = self.findNextRframeIndexSlot()
        nameLabel = ttk.Label(rframe, width=20, text = playerName)
        nameLabel.grid(row=0, column=0, sticky='n')
        self.gp.append(tk.StringVar())
        self.gw.append(tk.StringVar())
        self.sprd.append(tk.StringVar())
        self.cash.append(tk.StringVar())
        self.taken.append(tk.StringVar())
        self.given.append(tk.StringVar())
        self.gp[-1].set('')
        self.gw[-1].set('0')
        self.sprd[-1].set('0')
        self.cash[-1].set('0')
        self.taken[-1].set('0')
        self.given[-1].set('0')
        gp = tk.Entry(rframe, width=6, textvariable=self.gp[resultFrameIdx])
        gp.grid(row=0, column=1, sticky='n')
        self.setTagsandHandler(gp, resultFrameIdx, 1)
        gw = tk.Entry(rframe, width=6, textvariable=self.gw[resultFrameIdx])
        gw.grid(row=0,column=2, sticky='n')
        self.setTagsandHandler(gw, resultFrameIdx, 2)
        sprd = tk.Entry(rframe, width=6, textvariable=self.sprd[resultFrameIdx])
        sprd.grid(row=0, column=3, sticky='n')
        self.setTagsandHandler(sprd, resultFrameIdx, 3)
        # cash not used for seniors
        cash = tk.Entry(rframe, width=6, textvariable=self.cash[resultFrameIdx])
        cash.grid(row=0, column=4, sticky='n')
        self.setTagsandHandler(cash,resultFrameIdx,4)

        taken = tk.Entry(rframe, width=6, textvariable=self.taken[resultFrameIdx])
        taken.grid(row=0, column=5, sticky='n')
        self.setTagsandHandler(taken, resultFrameIdx, 5)
        # skunks given is computed and should not be an entry field
        given = tk.Label(rframe, width=6, textvariable=self.given[resultFrameIdx])
        given.grid(row=0, column=6, sticky='n')
        # add thes new rframe at the end of the current list of results
        self.listOfResults.append(rframe)
        self.listOfResults[-1].grid(column=0, sticky='n')
        print('Len listOfResults: ', len(self.listOfResults))
        self.ensureNewResultLineVisibility(len(self.listOfResults) - 1)
        self.positionAt(len(self.listOfResults)-1, 1)
    def findNextRframeIndexSlot(self):
        # it's the length of the current lists - before we add anything
        # len-1 is last index for current list. Len will be index for newe additions
        return len(self.gp)      # anyone will do...
    # player navigation area
    #
    def currentSlotMatches(self, idx, initial):
        return self.pFrame.interior.winfo_children()[idx].winfo_children()[self.textIndex]['text'][0] == initial

    def nextSlotMatches(self, idx, initial):
        print('Next slot: ',
              self.pFrame.interior.winfo_children()[idx + 1].winfo_children()[self.textIndex]['text'][0])
        return self.pFrame.interior.winfo_children()[idx + 1].winfo_children()[self.textIndex]['text'][0] == initial

    def searchFromTop(self, iFrame, initial):
        self.pFrame.activeIndex = 0
        self.resetHilites()
        while (iFrame.winfo_children()[self.pFrame.activeIndex].winfo_children()[self.textIndex]['text'][0] != initial):
            print('searchFromTop slot: ',
                  iFrame.winfo_children()[self.pFrame.activeIndex].winfo_children()[self.textIndex]['text'][0],
                  ' initial: ', initial)
            self.pFrame.activeIndex += 1
            if self.pFrame.activeIndex > self.pFrame.bottomIndex:
                self.pFrame.activeIndex = 0  # ran off end - default to top
                self.hiLiteActiveName(self.pFrame.activeIndex)
                break
        # activeIndex will be where we matched
        self.hiLiteActiveName(self.pFrame.activeIndex)
    def ensureNewResultLineVisibility(self, rdx):
        # rdx is the line that we need to have visible
        print ('Results visibility, rdx: ', rdx)
        if rdx < 12:
            return
        t = self.rFrame.interior.winfo_height()
        v = self.rFrame.canvas.winfo_height()
        vf = v / t  # fraction of interior frame covered by canvas
        # new results line is always at the bottom, so always move canvas to bottom of interior
        lf = 1.0
        uf = lf - vf
        self.rFrame.canvas.yview_moveto(t * uf+15)
        self.rFrame.vscrollbar.set(uf, lf)
    def ensureResultLineVisibility(self,rdx):
        if rdx == 0:
            # position at top
            t = self.rFrame.interior.winfo_height()
            v = self.rFrame.canvas.winfo_height()
            vf = v / t  # fraction of interior frame covered by canvas
            uf = 0
            lf = vf + uf    # uf is is zero, so lf is lower edge or canvas
            self.rFrame.canvas.yview_moveto(uf)
            self.rFrame.vscrollbar.set(uf, lf)
    def hiLiteActiveName(self, idx):
        self.hilite(self.pFrame.interior.winfo_children()[idx].winfo_children()[self.textIndex])
        # send appropriate fraction to vscrollbar
        vfraction = idx / len(self.allPlayerObjects)
        # the following two  have to be kept in sync with idx
        self.pFrame.vscrollbar.set(0.5, 1.0)
        self.pFrame.canvas.yview_moveto(0.5)
        # make it visible
        # self.pFrame.interior.winfo_children().see(idx)
        # we have to simulate this is there is no listbox to send .see(idx) to
        # interior conatains a set of rows, each with a singlePlayerFrame
        # we will have to yview_moveto so desired row shows.
        if idx < 13:
            self.pFrame.canvas.yview_moveto(0)
        elif idx > 17:
            self.pFrame.canvas.yview_moveto(602/337)
        else:
            self.pFrame.canvas.yview_moveto(0.25)
        # print ('Interior, Canvas Height:', interiorWindowHeight, ', ', canvasHeight)
        # t = self.pFrame.interior.winfo_height()
        # v = self.pFrame.interior.winfo_height()
        # n = len(self.listOfResults) - 1
        # toplf = 0
        # bottomlf = 1.0
        # vf = v/t
        # perLine = t/n       # pixels per display line, given n lines inside interior
        # nPerv = n * vf      # now many lines inside the canvas
        #                     # same as v / perLine
        # if rdx <= nPerv/2:      # position at top
        #     uf = 0
        #     lf = uf + vf
        #     self.pFrame.canvas.yview_moveto(0)
        #     self.pFrame.vscrollbar.set(uf, lf)
        #     return
        # if rdx >= n - nPerv/2:  # position at bottom
        #     lf = 1.0
        #     uf = lf - vf
        #     self.pFrame.canvas.yview_moveto(uf)
        #     self.pFrame.vscrollbar.set(uf, lf)
        #     return
        # rdxPixel = rdx * perLine    # line pixel value in interior (t)
        # lowerEdge = rdxPixel * v/2         # bottom edge of v with rdx at midpoint
        # lf = lowerEdge / t if lowerEdge < t else 1.0
        # uf = lf - vf
        # self.pFrame.canvs.yview_moveto(uf)
        # self.pFrame.vscrollbar.set(uf, lf)
    def hiLiteNextName(self, idx):
        self.resetHilite(self.pFrame.interior.winfo_children()[idx].winfo_children()[self.textIndex])
        self.hiLiteActiveName(idx + 1)

    def hiLitePriorName(self, idx):
        self.resetHilite(self.pFrame.interior.winfo_children()[idx].winfo_children()[self.textIndex])
        self.hiLiteActiveName((idx - 1))

    def resetHilites(self):
        for w in self.pFrame.interior.winfo_children():
            self.resetHilite(w.winfo_children()[self.textIndex])
    def hiLiteGamePoints(self,w):
        self.hilite(w)
    def hilite(self, w):
        w.config(background='blue', foreground='yellow')
    def resetHilite(self, w):
        w.config(background='whitesmoke', foreground='black')
    def errorHiLite(self, rfidx, offset):
        self.rFrame.interior.winfo_children()[rfidx].winfo_children()[offset]\
            .config(background='red', foreground='white')
    def resetScoringErrorHiLite(self,rfidx, offset):
        self.resetEntryHiLite(self.rFrame.interior.winfo_children()[rfidx].winfo_children()[offset])
    def resetEntryHiLite(self, w):
        w.config(background='white', foreground='black')

    #
    # end player navigation area
    #################################
    # results naviagation area
    #
    def positionInResultsAtTop(self):
        self.ensureResultLineVisibility(0)
        self.positionInResults(0,1)
    def positionInResults(self,rfidx, fldidx):
        # position at line and field, and move keyboard focus
        self.listOfResults[rfidx].winfo_children()[fldidx].focus_force()
    ############################
    # for testing only
    # cfg.tourneyRecord = at.getTourneyRecordById(cfg.tourneyRecordId)
    #
    ###########################

    def buildResultLine(self, rframe, result, resultFrameIdx):
        # build a single result line
        player = cfg.ap.getPlayerForaScoreCardInTourney(result)
        # playerName = player.FirstName + ', ' + player.LastName
        nameLabel = ttk.Label(rframe, width=20,
                              text=player.LastName + ', ' +player.FirstName)
        nameLabel.grid(row=0, column=0, sticky='n')
        self.gp.append(tk.StringVar())
        # instead of resultFrameIdx being passed in could use
        # self.gp[len(self.gp) - 1] to get the last entry
        self.gp[resultFrameIdx].set(str(result.GamePoints))
        self.gw.append(tk.StringVar())
        self.gw[resultFrameIdx].set(str(result.GamesWon))
        self.sprd.append(tk.StringVar())
        self.sprd[resultFrameIdx].set(str(result.Spread))
        self.cash.append(tk.StringVar())
        self.cash[resultFrameIdx].set(str(result.Cash))
        self.taken.append(tk.StringVar())
        self.taken[resultFrameIdx].set(str(result.SkunksTaken))
        self.given.append(tk.StringVar())
        self.given[resultFrameIdx].set(str(result.SkunksGiven))
        gp = tk.Entry(rframe, width=6, textvariable=self.gp[resultFrameIdx])
        gp.grid(row=0, column=1, sticky='n')
        self.setTagsandHandler(gp, resultFrameIdx, 1)
        gw = tk.Entry(rframe, width=6, textvariable=self.gw[resultFrameIdx])
        gw.grid(row=0,column=2, sticky='n')
        self.setTagsandHandler(gw, resultFrameIdx, 2)
        sprd = tk.Entry(rframe, width=6, textvariable=self.sprd[resultFrameIdx])
        sprd.grid(row=0, column=3, sticky='n')
        self.setTagsandHandler(sprd, resultFrameIdx, 3)
        # cash not used for seniors
        cash = tk.Entry(rframe, width = 6, textvariable=self.cash[resultFrameIdx])
        cash.grid(row=0, column=4, sticky='n')
        self.setTagsandHandler(cash, resultFrameIdx, 4)
        taken = tk.Entry(rframe, width=6, textvariable=self.taken[resultFrameIdx])
        taken.grid(row=0, column=5, sticky='n')
        self.setTagsandHandler(taken, resultFrameIdx, 5)
        # skunks given is computed and should not be an entry field
        given = tk.Label(rframe, width=6, textvariable=self.given[resultFrameIdx])
        given.grid(row=0, column=6, sticky='n')
        # self.setTagsandHandler(given, resultFrameIdx, 5)


    def _rEventHandler(self,event,rfi,fldi):
        #########################
        # handle the key input events from entry fields
        print('Entry field event:',event,' Frame and entry index: ', rfi, fldi)
        # key events handled
        # As each field is selected, change field kb focus
        # Return: accept current IntVar entry and move one entry field to the right
        #       if at last IntVar entry field, move to first IntVar entry field of next line
        #       if at last field of last result line, move to first field of top line of results
        # Tab:  move one field to right of IntVars, unless at last entry field
        #       treat tab as if Return was pressed to capture the input when we leave the field
        # Shift-Tab:    move one field to left of IntVars, unless at first entry field
        # Down: Move down one result line to first IntVar if not at last line
        # Up:   Move up one result line to first IntVar if not at first line
        # Left: Move back to Player Select screen
        # Prior: aka PageUp - go to top line, first entry
        # Next:  aka PageDown - to to last line, first entry
        #
        # .... and kb focus follow each movement.
        ###########################
        self.rFrame.maxItem = 5     # gp=1; gw=2; spread=3; cash=4; taken=5;
        self.rFrame.minItem = 1
        self.rFrame.topIndex = 0    # which line of results, starting @ 0
        self.rFrame.bottomIndex = len(self.tourneyResults) - 1

        rfmax = len(self.tourneyResults) - 1    # input to generate rframes
        if event.keysym == 'Return' or event.keysym == 'Tab':
            self.validateEntryField(rfi, fldi)
            # always update the database when we wrap past the end value
            # or when we go up or down and leave current line
            if rfi >= self.rFrame.bottomIndex:
                if fldi >= self.rFrame.maxItem:
                    self.updateDBMS(rfi, fldi)        # last item in the line
                    rfi = self.rFrame.topIndex
                    fldi = self.rFrame.minItem
                    self.positionAt(rfi, fldi)
                    self.returnFromResultsPanel()   # go back to people list, set focus
                else:
                    fldi +=1
                    self.positionAt(rfi, fldi)
            else:
                if fldi >= self.rFrame.maxItem:
                    self.updateDBMS(rfi, fldi)
                    rfi += 1
                    fldi = self.rFrame.minItem
                    self.positionAt(rfi, fldi)
                else:
                    fldi += 1
                    self.positionAt(rfi, fldi)
        # elif event.keysym == 'Tab':
        #     if fldi != self.rFrame.maxItem:
        #         fldi += 1
        # elif event.keysym == 'Shift-Tab':
        #     if fldi != self.rFrame.minItem:
        #         fldi -= 1
        elif event.keysym == 'Down':
            self.updateDBMS(rfi, fldi)
            if rfi >= self.rFrame.bottomIndex:
                rfi = self.rFrame.bottomIndex     # stay on last line
                self.positionAt(rfi, fldi)
            else:               # next line, first entry
                rfi += 1
                fld1 = self.rFrame.minItem
                self.positionAt(rfi, fldi)
        elif event.keysym == 'Up':
            self.updateDBMS(rfi, fldi)
            if rfi <= self.rFrame.topIndex:
                rfi = self.rFrame.topIndex     # stay on first line
                self.positionAt(rfi, fldi)
            else:               # prior line, first entry
                rfi -= 1
                self.positionAt(rfi, fldi)
        elif event.keysym == 'Prior':   # page up == top
            self.updateDBMS(rfi, fldi)
            rfi = self.rFrame.topIndex
            fldi = self.rFrame.minItem
            self.positionAt(rfi, fldi)
        elif event.keysym == 'Next':    # page down == bottom
            self.updateDBMS(rfi, fldi)
            rfi = self.rFrame.bottomIndex
            fldi = self.rFrame.maxItem
            self.positionAt(rfi, fldi)
        elif event.keysym == 'Left':
            print ('Back to player select screen')
            self.returnFromResultsPanel()
        else:
            print ('Unknown key: ', event.keysym)
    def createPlayerXref(self):
        # cross-refs used to build results screens
        cfg.playerXref = {p.id : p.LastName + ', ' + p.FirstName for p in list(Player.select())}
        cfg.playerRefx = { v:k for k, v in cfg.playerXref.items()}
    def crossCheckGpGw(self, rfidx ):
        # all we need is the row index to get both values
        gp = int(self.gp[rfidx].get())
        gw = int(self.gw[rfidx].get())
        if gp >= 2 * gw:
            return True
        else:
            return False
    def computeSkunksGiven(self, rfidx):
        print ('gp: ', self.gp[rfidx].get(), 'gw: ', self.gw[rfidx].get())
        return int(self.gp[rfidx].get()) - 2 * int(self.gw[rfidx].get())
    def gpValidation(self, rfidx):
        # validate permissible range of gp
        # always start by resetting errorlite
        self.resetScoringErrorHiLite(rfidx, 1)
        self.resetScoringErrorHiLite(rfidx, 2)
        gp = self.gp[rfidx].get()       # get the gp for the line
        if not gp.isnumeric():
            self.errorHiLite(rfidx, 1)
            return False
        if int(gp) > 35:
            self.errorHiLite(rfidx, 1)
            print ('GP value ', gp, ' too big')
            return False
        # defer this cross-check until the GW has been input
        # if not self.crossCheckGpGw(rfidx):
        #     self.errorHiLite(self.rFrame.interior.winfo_children()[rfidx].winfo_children()[1])
        #     self.errorHiLite(self.rFrame.interior.winfo_children()[rfidx].winfo_children()[2])
        #     return False
        # cannnot compute skunks given until gw for newly entered lines
        # self.given[rfidx].set(self.computeSkunksGiven(rfidx))
        return True
    def gwValidation(self, rfidx):
        #validate permissible games won
        self.resetScoringErrorHiLite(rfidx, 1)
        self.resetScoringErrorHiLite(rfidx, 2)
        gw = self.gw[rfidx].get()       # get the gw for the line
        if not gw.isnumeric():
            self.errorHiLite(rfidx, 2)
            return False
        if int(gw) > 18:
            print('GW value ', gw, ' not possible')
            self.errorHiLite(rfidx, 2)
            return False
        if not self.crossCheckGpGw(rfidx):
            self.errorHiLite(rfidx, 1)
            self.errorHiLite(rfidx, 2)
            return False
        self.given[rfidx].set(str(self.computeSkunksGiven(rfidx)))
        return True
    def spreadValidation(self, rfidx):
        # validate total spread
        spread = self.sprd[rfidx].get() # get the spread for the line
        self.resetScoringErrorHiLite(rfidx, 3)
        try:
            int(spread)
        except ValueError:
            self.errorHiLite(rfidx, 3)
            return False
        if abs(int(spread)) > 250:
            print ('Check Huge Spread value ', spread)
            self.errorHiLite(rfidx, 3)
            return False
        return True
    def cashValidation(self, rfidx):
        # validate amount of cash
        cash = self.cash[rfidx].get()   # get the cash awarded
        self.resetScoringErrorHiLite(rfidx, 4)
        try:
            int(cash)
        except ValueError:
            self.errorHiLite(rfidx, 4)
            return False
        if int(cash) < 0 or int(cash) > 150:
            self.errorHiLite(rfidx, 4)
            return False
        return True
    def takenValidation(self, rfidx):
        # validate number of taken skunks
        self.resetScoringErrorHiLite(rfidx, 5)
        taken = self.taken[rfidx].get() # get the skunks taken for the line
        if not taken.isnumeric():
            self.errorHiLite(rfidx, 5)
            return False
        if int(taken) > 9:
            print('Taken value ', taken,' not possible')
            self.errorHiLite(rfidx, 5)
            return False
        return True
    def validateEntryField(self,rfidx, fldidx):
        # invoked appropriate validation routine for each field
        # all functions must be defined before the switcher
        switcher = {
            1: self.gpValidation,
            2: self.gwValidation,
            3: self.spreadValidation,
            4: self.cashValidation,
            5: self.takenValidation
        }
        return switcher.get(fldidx)(rfidx)
    # TODO: after we leave a line, and no errors, then update the dmbs entry using SQLObject
    def setTagsandHandler(self, w, rfindex, fldindex):
        self.setTags(w,'rKeyEvent')
        def entryHandler(event, self=self, rfi = rfindex, fldi = fldindex):
            return self._rEventHandler(event, rfi, fldi)
        w.bind('<KeyPress>', entryHandler)
    def setTags(self,w, tag):
        newtags = (tag,) + w.bindtags()
        print ('New Tags', newtags)
        w.bindtags(newtags)
    def positionAt(self, rfi, fldi):
        # print('rFrame children: ',self.rFrame.winfo_children())
        self.rFrame.interior.winfo_children()[rfi].winfo_children()[fldi].focus_force()
    def updateDBMS(self, rfi, fldi):
        # we don't really care about fldi as we are going to update all fields from the control variables
        # only rfi is of interest
        # update tourneyRecord that is held in self.tourneyResults[]
        # TODO: This does not work for a new entry line. Have to build an empty scorecard record which we can
        #       then update.
        print ('Update DBMS**** rfi, fldi: ', rfi, fldi)
        if rfi > (len(self.tourneyResults) - 1):
            # this must be a new scorecard being created for the line @ rfi
            # tourneyRecordId is stored in cfg
            # the player id is pulled from cfg.Refx, keyted by playerid from label text on rfi record
            # the entry order is one more than the number of record currently in tourneyResults
            print('Player Name: ', self.rFrame.interior.winfo_children()[rfi].winfo_children()[0]['text'])
            dbmsScoreCardRecord = ScoreCard(
                                            Tourney = cfg.tourneyRecordId,
                                            Player = cfg.playerRefx[self.rFrame.interior.winfo_children()[rfi]\
                                            .winfo_children()[0]['text']],
                                            GamePoints = 0,
                                            GamesWon = 0,
                                            Spread = 0,
                                            Cash = 0,
                                            SkunksTaken = 0,
                                            SkunksGiven = 0,
                                            EntryOrder = len(self.tourneyResults)+1)
            # this new record will get pushed to the database
            self.tourneyResults.append(dbmsScoreCardRecord)     # and add it to the list of tourneResults
            self.updatePlayerCount()
        else:
            dbmsScoreCardRecord = self.tourneyResults[rfi]
        # and this code should now work as we pushed the new record onto the end of tourneyRestuls
        dbmsScoreCardRecord.set(GamePoints = int(self.gp[rfi].get()),
                              GamesWon = int(self.gw[rfi].get()),
                              Spread = int(self.sprd[rfi].get()),
                              Cash = int(self.cash[rfi].get()),
                              SkunksTaken = int(self.taken[rfi].get()),
                              SkunksGiven = int(self.given[rfi].get())
                              )
        dbmsScoreCardRecord.syncUpdate()
        # after updating the dbms, update the views
        self.populatePframe()
        self.updateTotals()
    def updateTotals(self):
        # step through all results and refresh totals
        # print ('self.tourneyResults ', self.tourneyResults)
        # print ('GP: ',[p.GamePoints for p in self.tourneyResults ])
        # print ('Game Points: ',[p.GamePoints for p in self.tourneyResults if p.GamePoints > 0])
        self.plusSpread.set(sum([p.Spread for p in self.tourneyResults if p.Spread > 0]))
        self.minusSpread.set(sum([m.Spread for m in self.tourneyResults if m.Spread < 0]))
        self.givenSkunks.set(sum([g.SkunksGiven for g in self.tourneyResults]))
        self.takenSkunks.set(sum([t.SkunksTaken for t in self.tourneyResults]))
        self.diffSpread.set(self.plusSpread.get() + self.minusSpread.get())
        self.diffSkunks.set(self.givenSkunks.get() - self.takenSkunks.get())
        self.updatePlayerCount()
    def updatePlayerCount(self):
        # count players for current tourney in database
        self.count.set(cfg.ar.countTourneyResults(cfg.tourneyRecord))
if __name__ == "__main__":
    #############################################
    # hardwire cfg for testing                  #
    cfg.appTitle = 'Results Testing'  #
    cfg.clubNumber = 999  #
    cfg.season = '2019-20'  #
    cfg.clubName = 'Seniors'  #
    cfg.tourneyDate = '2019-05-02'  #
    cfg.tourneyRecordId = 11  #
    cfg.tourneyNumber = 8  #
    # defer getting club record until connection made
    # cfg.clubRecord = Club.get(1)                #
    # cfg.clubId = cfg.clubRecord.id              #
    #                                           #

    # open up the tso to create dbms connection
    cstring = ''
    conn = ''
    dbmsObject = tso.TSO()

    # test ability to access players
    ap = AccessPlayers()
    players = list(Player.select())
    print (players)
    cfg.clubRecord = Club.get(1)
    cfg.clubId = cfg.clubRecord.id
    club999 = list(Club.select(Club.q.clubNumber == 999))[0]

    print('Count of players: ',ap.countPlayers(club999))
    countOfPlayers = ap.countPlayers(club999)
     # get tourney record
    at = AccessTourneys()
    ar = AccessResults()
    cfg.tourneyRecord = at.getTourneyByNumber(cfg.tourneyNumber)[0]
    cfg.tourneyRecordId = cfg.tourneyRecord.id
    cfg.tourneyNumber = cfg.tourneyRecord.TourneyNumber

    root = tk.Tk()
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    # root.columnconfigure(1,weight=1)
    # root.geometry('400x500')
    app = SampleApp(master=root)
    app.rowconfigure(0, weight=1)
    app.columnconfigure(0, weight=1)
    app.columnconfigure(1, weight=1)
    app.master.title('Result Panel 1')
    app.mainloop()
