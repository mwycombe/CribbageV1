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
#   TODO:   Make sure top player is selected in listbox after Enter of results
#   TODO:   *** Check that results are saved before exiting results tab
#   TODO:   Replace in situ entry/edit with pull out line above results
#   TODO:   Results edit changed entry order; duplicates entry in dbms on Enter accept
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
#   TODO:   Implement concept of commit or quit or pause tourney entry
#   TODO:   Can implement pause using F11 to force partial commit
#   TODO:   Check that there is a tourney selected when F6 is pressed to enter results - this is in Tourney Tab, not results...
#   TODO:   *** Warn if leaving results page without saving what has been entered so far.
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
from resultsline import resultsLine

from accessPlayers import AccessPlayers
from accessTourneys import AccessTourneys
from accessPlayers import AccessPlayers
from accessResults import AccessResults

# For testing
import dbms100tso as tso

# TODO: Edit results does not replace line
# TODO: Edit results does not update dbms
# TODO: Edit results dows not correctly add up summary

# from verticalscrolledframe import VerticalScrolledFrame

class ResultsTab(tk.Frame):
    # screen class is always a frame


    #   sets up tab for capturing scores cards and games within

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid()

        # control variables for results tab
        #
        # build out tab, add to notebook (parent),  and register with notebook
        self.config(padx = '5', pady = '5')
        parent.add(self, text='Results Panel')
        cfg.screenDict['rsltab'] = self
        print('register rsltab')

        self.reg = parent.register(self.justNumeric)
        self.minusInput = parent.register(self.minusNumeric)
        #####################################################
        #
        #   control variables for GUI
        #
        #####################################################

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

        # initialize results tracking variables
        self.plusSpread.set(0)
        self.minusSpread.set(0)
        self.diffSpread.set(0)
        self.givenSkunks.set(0)
        self.takenSkunks.set(0)
        # used to display progress of scoring
        self.playerList = tk.StringVar()
        self.playerPoints = tk.StringVar()

        # used for the results entry line
        self.resultsNameVar = tk.StringVar()
        self.resultsGpVar = tk.StringVar()
        self.resultsGwVar= tk.StringVar()
        self.resultsSprdVar = tk.StringVar()
        self.resultsCashVar = tk.StringVar()
        self.resultsTknVar = tk.StringVar()
        self.resultsGvnVar = tk.StringVar()
        self.resultsOrderVar = tk.StringVar()

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
                                     padx = '5', pady ='5',
                                     text='Results Panel'
                                      )
        self.results.grid(row=0, column=0, sticky='nsew')

        # set up player selection
        self.tourneyHeaderPanel = tk.Frame(self.results,
                                            relief='raised', bd=2,
                                            padx = '5', pady ='5'
                                            )
        self.tourneyHeaderPanel.grid(row=0, column=0, sticky='w')

        self.resultsSummaryPanel = tk.Frame(self.results,
                                       relief='raised', bd=2,
                                       padx = '5', pady ='5')
        self.resultsSummaryPanel.grid(row=0, column=1, sticky='w')

        self.resultsTourneyTypePanel = tk.Frame(self.results,
                                              relief='raised',bd=2,
                                              padx='5', pady='5')
        self.resultsTourneyTypePanel.grid(row=0, column=2, sticky='w')
        self.resultsNewTourney = tk.Label(self.resultsTourneyTypePanel,
                                          text='Entering new tourney',
                                          padx='5', pady='5')
        self.resultsNewTourney.grid(row=0, column=0, sticky='w')
        self.resultsExistingTourney = tk.Label(self.resultsTourneyTypePanel,
                                               text='Editing existing tourney',
                                               padx='5', pady='5')
        self.resultsExistingTourney.grid(row=0, column=0, sticky='w')
        self.hideWidget(self.resultsTourneyTypePanel)
        self.hideWidget(self.resultsNewTourney)
        self.hideWidget(self.resultsExistingTourney)

        self.resultsEntryInstructionsPanel = tk.Frame(self.results,
                                                      relief='flat',
                                                      padx='5', pady='5')
        self.resultsEntryInstructionsPanel.grid(row=0, column=2, sticky='w')
        self.resultsInstructions1 = tk.Label(self.resultsEntryInstructionsPanel,
                                             text='Tab/Shift-Tab/Click on entry fields to input')
        self.resultsInstructions2 = tk.Label(self.resultsEntryInstructionsPanel,
                                             text='Press Enter when done to submit result line')
        self.resultsInstructions1.grid(row=0, column=0, sticky='w')
        self.resultsInstructions2.grid(row=1, column=0, sticky='w')

        # results line input error messages
        self.errorsPanel = tk.Frame(self.results,
                                    relief='flat',
                                    padx='5', pady='5')
        self.errorsPanel.grid(row=1, column=3, sticky='w')
        self.gpError = tk.Label(self.errorsPanel,
                                padx='5', pady='5',
                                text='Game points not valid integer or out of range')
        self.gwError = tk.Label(self.errorsPanel,
                                padx='5', pady='5',
                                text='Games won not valid integer or out of range')
        self.spreadError = tk.Label(self.errorsPanel,
                                    padx='5', pady='5',
                                    text='Spread not valid integer or out of range')
        self.cashError = tk.Label(self.errorsPanel,
                                  padx='5', pady='5',
                                  text='Cash not valid integer or out of range')
        self.tknError = tk.Label(self.errorsPanel,
                                 padx='5', pady='5',
                                 text='Taken skunks not valid integer or out of range')
        self.gpError.grid(row=0, column=0, sticky='w')
        self.gwError.grid(row=1, column=0, sticky='w')
        self.spreadError.grid(row=2, column=0, sticky='w')
        self.cashError.grid(row=3, column=0, sticky='w')
        self.tknError.grid(row=4, column=0, sticky='w')
        self.hideResultLineErrorMessages()

        self.resultsEntryPanel = tk.Frame(self.results,
                                          relief='flat',
                                          padx = '5', pady = '5')
        self.resultsEntryPanel.grid(row=0, column=4, sticky='w')

        # this edit panel is used to hold a new result or one being edited.
        self.resultsInputPanel = tk.Frame(self.resultsEntryPanel,
                                         relief='flat')
        self.resultsInputPanel.grid(row=0, column=0, sticky='w')

        # label headers
        self.resultsNameLabel = tk.Label(self.resultsInputPanel,
                                        width=15, text='Name')
        self.resultsGpLabel = tk.Label(self.resultsInputPanel,
                                       width=4, text=' Gp ')
        self.resultsGwLabel = tk.Label(self.resultsInputPanel,
                                       width=4, text=' Gw ')
        self.resultsSprdLabel = tk.Label(self.resultsInputPanel,
                                         width=4, text='Sprd')
        self.resultsTknLabel = tk.Label(self.resultsInputPanel,
                                        width=4, text='Tkn ')
        self.resultsCashLabel = tk.Label(self.resultsInputPanel,
                                       width=4, text=" $'s")
        self.resultsGvnLabel = tk.Label(self.resultsInputPanel,
                                        width=4, text='Gvn ')
        self.resultsOrderLabel = tk.Label(self.resultsInputPanel,
                                          width=4, text='Order')
        self.resultsNameLabel.grid(row=0, column=0, sticky='w')
        self.resultsGpLabel.grid(row=0, column=1, sticky='w')
        self.resultsGwLabel.grid(row=0, column=2, sticky='w')
        self.resultsSprdLabel.grid(row=0, column=3, sticky='w')
        self.resultsTknLabel.grid(row=0, column=4, sticky='w')
        self.resultsCashLabel.grid(row=0, column=5, sticky='w')
        self.resultsGvnLabel.grid(row=0, column=6, sticky='w')
        self.resultsOrderLabel.grid(row=0, column=7, sticky='w')

        # entry fields
        # Name is disabled - autofilled; skunks Gvn is computed and autofilled as is order
        self.resultsNameEntry = tk.Entry(self.resultsInputPanel, width=20,
                                         state=tk.DISABLED,
                                         font=('Helvetica','12','bold'),
                                         textvariable=self.resultsNameVar)
        self.resultsGpEntry = tk.Entry(self.resultsInputPanel, width=4,
                                       textvariable=self.resultsGpVar,
                                       validate='key', validatecommand=(self.reg, '%P'))
        self.resultsGwEntry = tk.Entry(self.resultsInputPanel, width=4,
                                       textvariable=self.resultsGwVar,
                                       validate='key', validatecommand=(self.reg, '%P'))
        self.resultsSprdEntry = tk.Entry(self.resultsInputPanel, width=4,
                                         textvariable=self.resultsSprdVar,
                                         validate='focusout', validatecommand=(self.minusNumeric, '%P'))
        self.resultsTknEntry = tk.Entry(self.resultsInputPanel, width=4,
                                        textvariable=self.resultsTknVar,
                                        validate='key', validatecommand=(self.reg, '%P'))
        self.resultsCashEntry = tk.Entry(self.resultsInputPanel, width=4,
                                         textvariable=self.resultsCashVar,
                                         validate='key', validatecommand=(self.reg, '%P'))
        self.resultsGvnEntry = tk.Entry(self.resultsInputPanel, width=4,
                                        state=tk.DISABLED,
                                        textvariable=self.resultsGvnVar)
        self.resultsOrderEntry = tk.Entry(self.resultsInputPanel, width=4,
                                          state=tk.DISABLED,
                                          textvariable=self.resultsOrderVar)
        self.resultsNameEntry.grid(row=1, column=0, sticky='w')
        self.resultsGpEntry.grid(row=1, column=1, sticky='w')
        self.resultsGwEntry.grid(row=1, column=2, sticky='w')
        self.resultsSprdEntry.grid(row=1, column=3, sticky='w')
        self.resultsTknEntry.grid(row=1, column=4, sticky='w')
        self.resultsCashEntry.grid(row=1, column=5, sticky='w')
        self.resultsGvnEntry.grid(row=1, column=6, stick='w')
        self.resultsOrderEntry.grid(row=1, column=7, sticky='w')

        # bind Enter (Return) key to each eligible field.
        # NameEntry field is always prefilled; GvnEntry field is always computed
        self.resultsNameEntry.bind('<Return>', self.handleResultLine)
        self.resultsGpEntry.bind('<Return>', self.handleResultLine)
        self.resultsGwEntry.bind('<Return>', self.handleResultLine)
        self.resultsSprdEntry.bind('<Return>', self.handleResultLine)
        self.resultsCashEntry.bind('<Return>', self.handleResultLine)
        self.resultsTknEntry.bind('<Return>', self.handleResultLine)
        self.resultsGvnEntry.bind('<Return>', self.handleResultLine)
        self.resultsOrderEntry.bind('<Return>', self.handleResultLine)

        # allow user to quit entering a result line
        self.resultsNameEntry.bind('<Escape>', self.quitResultLine)
        self.resultsGpEntry.bind('<Escape>', self.quitResultLine)
        self.resultsGwEntry.bind('<Escape>', self.quitResultLine)
        self.resultsSprdEntry.bind('<Escape>', self.quitResultLine)
        self.resultsCashEntry.bind('<Escape>', self.quitResultLine)
        self.resultsTknEntry.bind('<Escape>', self.quitResultLine)
        self.resultsGvnEntry.bind('<Escape>', self.quitResultLine)
        self.resultsOrderEntry.bind('<Escape>', self.quitResultLine)

        # hide edit panel for now
        self.hideResultsInputPanel()
        self.hideResultsInstructionsPanel()

        # result type switch area as results input area does double duty.
        cfg.newTourney = False      # must be doing an edit then

        # now set up the scrolled panels - clones from results1.py
        self.playerPanel = tk.LabelFrame(self.results,
                                          relief='ridge',
                                          height='10c',
                                          width='10c',
                                          padx = '5', pady='5',
                                          text='Select Players')
        self.playerPanel.grid(row=1, column=0, sticky='nsew')

        self.tourneyResultsPanel = tk.LabelFrame(self.results,
                                           relief='ridge',
                                           height='10c',
                                           width='5c',
                                           padx = '5', pady ='5',
                                           text='Tourney Results')
        self.tourneyResultsPanel.grid(row=1, column=1, columnspan=2, sticky='nsew')

        # start by assuming not an edit
        cfg.tourneyEdit = False

    # ************************************************************
    #   check to see if our tab was selected.
    #
    #   This structure <index(cfg.screenDict['notebook'].select())>
    #   gets the WindowId via parameterless .select() then converts that
    #   into the current tab index (from zero)
    #
    def tabChange(self, event):
        # populate the tab whenever we get selected
        ##  if cfg.screenDict['notebook'].index(cfg.screenDict['notebook'].select()) == 4:
        print('**Resultstab got the notebook changed event***')

        # TODO this has to be deferred until after the tourney date has been selected
        # TODO if entered without a selection, issues message and return to tourneytab for selection
        self.buildActivityPanel()
        self.buildScoringPanels()
        # position in player panel for now
        # TODO: Provide the future ability to sort various ways.
        # TODO: Check for non-empty listOfResultLines i.e. uncommitted
        #       This implies a tab switch out then back - else honor F6 for
        #       current tourney record from dbms
        # TODO: Detect new tourney results vs existing & set flag
        cfg.newTourney = self.newTourney()
        print ('cfg.newTourney: ', cfg.newTourney)
        self.goToTopOfPlayers()
        # if cfg.newTourney:
        #     self.showWidget(self.resultsNewTourney)
        # else:
        #     self.showWidget(self.resultsExistingTourney)
    def buildActivityPanel(self):
        MasterScreen.wipeActivityPanel()
        mtp = cfg.screenDict['activity']
        self.leftActivityPanel = tk.Frame(mtp, relief='flat')
        self.rightActivityPanel = tk.Frame(mtp, relief='flat')
        self.leftActivityPanel.grid(row=0, column=0, sticky='w')
        self.rightActivityPanel.grid(row=0, column=1, sticky='nw')
        lap = self.leftActivityPanel
        rap = self.rightActivityPanel
        self.keyF2 = tk.Label(lap, text = 'F2   Edit results for selected player')
        self.keyF3 = tk.Label(rap, text = 'F3   Create new result for selected player')
        self.keyF4 = tk.Label(lap, text = 'F4   Complete the delete request')
        self.keyF9 = tk.Label(rap, text = 'F9   Remove the selected result from tourney')
        self.keyF10 = tk.Label(lap, text = 'F10  Save the results as entered')
        self.keyF11 = tk.Label(rap, text = 'F11  Force save of partial tourney or with diff')
        self.keyEsc = tk.Label(lap, text = "Esc  Quit what your're doing")
        # self.button = tk.Label(rap, text = 'Click  Sorts tourney results by column order')
        self.keyF2.grid(row=0, column=0, sticky='w')
        self.keyF3.grid(row=0, column=0, sticky='w')
        self.keyF4.grid(row=1, column=0, sticky='w')
        self.keyF9.grid(row=1, column=0, sticky='w')
        self.keyF10.grid(row=2, column=0, sticky='w')
        self.keyF11.grid(row=2, column=0, sticky='w')
        self.keyEsc.grid(row=3, column=0, sticky='w')
        # self.button.grid(row=3, column=0, sticky='w')

        self.populateResultsHeaderPanel()

    def populateResultsHeaderPanel(self):
        self.tsp = self.resultsSummaryPanel

        self.resultsLabels = tk.Frame(self.tsp,
                                       relief='flat'
                                      )
        self.resultsTotals = tk.Frame(self.tsp,
                                     relief='flat')
        self.resultsLabels.grid(row=0, column=0, sticky='w')
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
        # self.reCalc = tk.Button(self.resultsTotals,
        #                          text='ReCalc',
        #                          command=self.reCalc)
        self.plusLabel.grid(row=0, column=1)
        self.minusLabel.grid(row=0, column=2)
        self.diffLabel.grid(row=0, column=3)

        self.ph2.grid(row=0, column=4)
        # self.reCalc.grid(row=0, column=5)

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
                                          width = 3,
                                          textvariable = self.minusSpread)
        self.diffSpreadLabel = tk.Label(self.resultsTotals,
                                         background = 'white',
                                         width = 3,
                                         textvariable = self.diffSpread)
        self.givenSkunksLabel = tk.Label(self.resultsTotals,
                                          background = 'white',
                                          width = 4,
                                          textvariable = self.givenSkunks)
        self.takenSkunksLabel = tk.Label(self.resultsTotals,
                                          background = 'white',
                                          width = 4,
                                          textvariable = self.takenSkunks)
        self.diffSkunksLabel = ttk.Label(self.resultsTotals,
                                         background = 'white',
                                         width = 4,
                                         textvariable = self.diffSkunks)
        self.plusSpreadLabel.grid(row = 1, column = 1, sticky = 'w')
        self.minusSpreadLabel.grid(row = 1, column = 2, sticky = 'w')
        self.diffSpreadLabel.grid(row = 1, column = 3, sticky = 'w')
        self.givenSkunksLabel.grid(row = 2, column = 1, sticky = 'w')
        self.takenSkunksLabel.grid(row = 2, column = 2, sticky = 'w')
        self.diffSkunksLabel.grid(row = 2, column = 3, sticky = 'w')

    def buildScoringPanels(self):
        self.tourneyDateLabel = tk.Label(self.tourneyHeaderPanel,
                                       text='Tourney Date:')
        self.tourneyDateLabel.grid(row=0, column=0, sticky='w')
        self.tourneyNumberLabel = tk.Label(self.tourneyHeaderPanel,
                                            text='Tourney No.')
        self.tourneyNumberLabel.grid(row=1, column=0, sticky='w')
        self.tourneyDate.set(cfg.tourneyDate)
        self.tourneyDateValue = tk.Label(self.tourneyHeaderPanel,
                                          background = 'white',
                                          textvariable=self.tourneyDate)
        self.tourneyDateValue.grid(row=0, column=1)
        self.tourneyNumber.set(cfg.tourneyNumber)
        self.tourneyNumberValue = tk.Label(self.tourneyHeaderPanel,
                                            background = 'white',
                                            textvariable=self.tourneyNumber)
        self.tourneyNumberValue.grid(row=1, column=1, sticky = 'w')
        self.countLabel = tk.Label(self.tourneyHeaderPanel,
                                    text='Count:   ')
        self.countLabel.grid(row=2, column=0, sticky='w')
        # count of results for selected tourney
        print('cfg.tourneyRecord: ', type(cfg.tourneyRecord))
        print('cfg.tourneyRecord: ',cfg.tourneyRecord )
        print('cfg tourneyRecordId: ', cfg.tourneyRecordId)
        self.count.set(cfg.ar.countTourneyResults(cfg.tourneyRecord))
        self.playerCount = tk.Label(self.tourneyHeaderPanel,
                                     background = 'white',
                                     textvariable=self.count)
        self.playerCount.grid(row=2, column=1, sticky='w')

        # TODO: Update count after every input of new line of results.

        self.createWidgets()

    # def computeDifferences(self):
    #     # just compute the running differences
    #     # this means the ctrl variables are IntVar type
    #     self.diffPoints.set(self.plusPoints.get() - self.minusPoints.get())
    #     self.diffSkunks.set(self.givenSkunks.get() - self.takenSkunks.get())
    #
    # # def returnFromtourneyResultsPanel(self):
    # #     # self.create_widgets()        # just rebuild everything
    # #     self.populatePframe()
    def createWidgets(self):
        # TODO: No - use in-memory list if return for same tourney
        # TODO: Add sort feature to the Tourney Results columns
        # TODO: Now depends on the in-memory list of resultLine objects

        # always start with another next list of listboxes

        self.pListOfListboxes = []      # synchronized player names and points list boxes
        self.rListOfListboxes = []      # synchronized results list boxes


        # create synchronized listboxes to hold players and points
        self.playerPointsListBoxLabel = tk.Label(self.playerPanel, text='Points')
        self.playerNameListBoxLabel = tk.Label(self.playerPanel, text='Player Name')
        self.playerPointsListBoxLabel.grid(row=0, column=0, sticky='w')
        self.playerNameListBoxLabel.grid(row=0, column=1, sticky='w')
        # and now the listboxes that hold the information
        self.pvsb = tk.Scrollbar(self.playerPanel,
                                 orient='vertical', command=self.p_OnVsb)
        self.pvsb.grid(row=1, column=2, sticky='nsw')

        self.playerPointsListBox = tk.Listbox(self.playerPanel, exportselection=0,
                                              width = 4, height = 20,
                                              selectmode=tk.SINGLE, yscrollcommand=self.p_vsb_set)
        self.playerNameListBox = tk.Listbox(self.playerPanel, exportselection=0,
                                            width = 20, height = 20,
                                             selectmode=tk.SINGLE, yscrollcommand=self.p_vsb_set)
        self.playerPointsListBox.grid(row=1, column=0, sticky='w')
        self.playerNameListBox.grid(row=1, column=1, sticky='w')

        self.pListOfListboxes.append(self.playerNameListBox)
        self.pListOfListboxes.append(self.playerPointsListBox)

        for lb in self.pListOfListboxes:
            lb.selection_clear(0,tk.END)
            lb.selection_set(0)
            lb.activate(0)
        self.pListOfListboxes[0].focus_force()

        # player list boxes navigation binds and handlers
        for lb in self.pListOfListboxes:
            lb.bind('<<ListboxSelect>>', self.p_handle_select)
            lb.bind('<Up>', self.p_UpDownHandler)
            lb.bind('<Down>', self.p_UpDownHandler)

        # add alpha search to list box of names
        self.pListOfListboxes[0].focus_set()
        self.pListOfListboxes[0].unbind('<key>')
        self.pListOfListboxes[0].bind('<Key>', self.on_key_press)

        # rHdrPanel holds the listbox labels
        self.rHdrPanel = tk.Frame(self.tourneyResultsPanel)
        self.rHdrPanel.grid(row = 0, column = 0, stick = 'ew')
        self.nameHdr = tk.Button(self.rHdrPanel, text = 'Names',
                                 font=('Helvetica', '10', 'bold'),
                                 takefocus=0, bd=0, width=17)
        self.gpHdr = tk.Button(self.rHdrPanel, text = 'Gp',
                               font=('Helvetica', '10', 'bold'),
                               takefocus=0, bd=0, width=4)
        self.gwHdr = tk.Button(self.rHdrPanel, text='Gw',
                               font=('Helvetica', '10', 'bold'),
                               takefocus=0, bd=0, width=4)
        self.sprdHdr = tk.Button(self.rHdrPanel, text='Sprd',
                                 font=('Helvetica', '10', 'bold'),
                                 takefocus=0, bd=0, width=3)
        self.cashHdr = tk.Button(self.rHdrPanel, text=" $'s",
                                 font=('Helvetica', '10', 'bold'),
                                 takefocus=0, bd=0, width=4)
        self.tknHdr = tk.Button(self.rHdrPanel, text='Tkn',
                                font=('Helvetica', '10', 'bold'),
                                takefocus=0, bd=0, width=4)
        self.gvnHdr = tk.Button(self.rHdrPanel, text='Gvn',
                                font=('Helvetica', '10', 'bold'),
                                takefocus=0, bd=0, width=3)
        self.orderHdr = tk.Button(self.rHdrPanel, text='Order',
                                  font=('Helvetica', '10', 'bold'),
                                  takefocus=0, bd=0, width=4)
        self.nameHdr.grid(row = 0, column = 0, sticky = 'w')
        self.gpHdr.grid(row = 0, column = 1, sticky = 'w')
        self.gwHdr.grid(row = 0, column = 2, sticky = 'w')
        self.sprdHdr.grid(row = 0, column = 3, sticky = 'w')
        self.tknHdr.grid(row = 0, column = 4, sticky = 'w')
        self.cashHdr.grid(row = 0, column = 5, sticky = 'w')
        self.gvnHdr.grid(row = 0, column = 6, sticky = 'w')
        self.orderHdr.grid(row=0, column = 7, sticky = 'w')

        self.initializeSortDictionary()
        # rDtlPanel holds the listboxes of names and results
        self.rDtlPanel = tk.Frame(self.tourneyResultsPanel)
        self.rDtlPanel.grid(row = 1, column = 0, sticky='w')

        # rDtlPanel is going to hold the various result listboxes
        #
        # details section
        #

        # allocate the listboxes used to show results on screen
        self.rvsb = tk.Scrollbar(self.rDtlPanel,
                                 orient='vertical', command=self.r_OnVsb)
        self.resultsNamesLB = tk.Listbox(self.rDtlPanel, exportselection=0,
                                         width=17,
                                         height=20,
                                         selectmode=tk.SINGLE,
                                         yscrollcommand=self.r_vsb_set)
        self.resultsGpLB = tk.Listbox(self.rDtlPanel, exportselection=0,
                                      width=4, height=20,
                                      selectmode=tk.SINGLE,
                                      yscrollcommand=self.r_vsb_set)
        self.resultsGwLB = tk.Listbox(self.rDtlPanel, exportselection=0,
                                      width=4, height=20,
                                      selectmode=tk.SINGLE,
                                      yscrollcommand=self.r_vsb_set)
        self.resultsSprdLB = tk.Listbox(self.rDtlPanel, exportselection=0,
                                        width=4, height=20,
                                        selectmode=tk.SINGLE,
                                        yscrollcommand=self.r_vsb_set)
        self.resultsTknLB = tk.Listbox(self.rDtlPanel, exportselection=0,
                                       width=4, height=20,
                                       selectmode=tk.SINGLE,
                                       yscrollcommand=self.r_vsb_set)
        self.resultsCashLB = tk.Listbox(self.rDtlPanel, exportselection=0,
                                        width=4, height=20,
                                        selectmode=tk.SINGLE,
                                        yscrollcommand=self.r_vsb_set)
        self.resultsGvnLB = tk.Listbox(self.rDtlPanel, exportselection=0,
                                       width=4, height=20,
                                       selectmode=tk.SINGLE,
                                       yscrollcommand=self.r_vsb_set)
        self.resultsOrderLB = tk.Listbox(self.rDtlPanel, exportselection=0,
                                         width=4, height=20,
                                         selectmode=tk.SINGLE,
                                         yscrollcommand=self.r_vsb_set)
        self.resultsNamesLB.grid(row=1, column=0, sticky='w')
        self.resultsGpLB.grid(row=1, column=1, sticky='w')
        self.resultsGwLB.grid(row=1, column=2, sticky='w')
        self.resultsSprdLB.grid(row=1, column=3, sticky='w')
        self.resultsTknLB.grid(row=1, column=4, sticky='w')
        self.resultsCashLB.grid(row=1, column=5, sticky='w')
        self.resultsGvnLB.grid(row=1, column=6, sticky='w')
        self.resultsOrderLB.grid(row=1, column=7, sticky='w')
        self.rvsb.grid(row=1, column=8, sticky='ns')

        self.rListOfListboxes.append(self.resultsNamesLB)
        self.rListOfListboxes.append(self.resultsGpLB)
        self.rListOfListboxes.append(self.resultsGwLB)
        self.rListOfListboxes.append(self.resultsSprdLB)
        self.rListOfListboxes.append(self.resultsTknLB)
        self.rListOfListboxes.append(self.resultsCashLB)
        self.rListOfListboxes.append(self.resultsGvnLB)
        self.rListOfListboxes.append(self.resultsOrderLB)


        # self.listOfPlayers = []
        # self.listOfResults = []

        self.tourneyResultsCount = cfg.ar.countTourneyResults(cfg.tourneyRecord)
        self.tourneyResults = []
        self.gp = []
        self.gw = []
        self.sprd = []
        self.taken = []
        self.cash = []
        self.given = []         # these are computed

        # results frame listboxes binds and handler
        for lb in self.rListOfListboxes:
            lb.bind('<<ListboxSelect>>', self.r_handle_select)
            lb.bind('<Up>', self.r_UpDownHandler)
            lb.bind('<Down>', self.r_UpDownHandler)
        self.populatePframe()
        self.populateRframe()

        self.goToTopOfPlayers()

        #****************************************************
        # bind section
        #****************************************************
        # F2 can be activated from Players or Results list box
        # F3 can only be recongnized from Players
        # F7 switches back to list of  Players
        # F9 can only be recongnized from Results and Players
        # F10 can be recognized from Players or Results
        # F11 can be recognized from Players or Results
        # Esc can happen just about anywhere - quit
        # Allow results for a new tourney to be committed from wherever the focus is

        for lb in self.pListOfListboxes:
            lb.bind('<F2>', self.editResultsFromPlayer)
            lb.bind('<F3>', self.newResult)
            lb.bind('<F9>', self.pResultLineDelete)
            lb.bind('<F10>', self.commitResults)
            lb.bind('<F11>', self.forceResultsCommit)
            lb.bind('<Escape>', self.quitResults)

        # for lb in self.rListOfListboxes:
        for lb in self.rListOfListboxes:
            lb.bind('<F2>', self.editResultsFromResults)
            lb.bind('<F9>', self.deleteResultLine)
            lb.bind('<F7>', self.backToPlayers)
            lb.bind('<F10>', self.commitResults)
            lb.bind('<F11>', self.forceResultsCommit)
            lb.bind('<Escape>', self.quitResults)

        # binds for sorting results
        self.nameHdr.bind('<1>', self.rSortHandler)
        self.gpHdr.bind('<1>', self.rSortHandler)
        self.gwHdr.bind('<1>', self.rSortHandler)
        self.sprdHdr.bind('<1>', self.rSortHandler)
        self.tknHdr.bind('<1>', self.rSortHandler)
        self.cashHdr.bind('<1>', self.rSortHandler)
        self.gvnHdr.bind('<1>', self.rSortHandler)
        self.orderHdr.bind('<1>', self.rSortHandler)

        self.updateTotals()

    # multi-listbox handler area for players
    def p_OnVsb(self, *args):
        for lb in self.pListOfListboxes:
            lb.yview(*args)
        # self.playerPointsListBox.yview(*args)
        # self.playerNameListBox.yview(*args)
    def p_vsb_set(self, *args):
        self.pvsb.set(*args)
        for lb in self.pListOfListboxes:
            lb.yview_moveto(args[0])
        # self.playerPointsListBox.yview_moveto(args[0])
        # self.playerNameListBox.yview_moveto(args[0])
    def p_handle_select(self, event):
        for lb in self.pListOfListboxes:
            if lb != event.widget:
                lb.selection_clear(0, 'end')
                lb.selection_set(event.widget.curselection())
                lb.activate(event.widget.curselection())
    def p_UpDownHandler(self, event):
        selection = event.widget.curselection()[0]
        if event.keysym == 'Up':
            selection += -1
        if event.keysym == 'Down':
            selection += 1

        if 0 <= selection < event.widget.size():
            for lb in self.pListOfListboxes:
                lb.selection_clear(0, tk.END)
                lb.selection_set(selection)

    # multil-listbox handler area for results
    def r_OnVsb(self, *args):
        for lb in self.rListOfListboxes:
            lb.yview(*args)
        # self.playerPointsListBox.yview(*args)
        # self.playerNameListBox.yview(*args)
    def r_vsb_set(self, *args):
        self.rvsb.set(*args)
        for lb in self.rListOfListboxes:
            lb.yview_moveto(args[0])
        # self.playerPointsListBox.yview_moveto(args[0])
        # self.playerNameListBox.yview_moveto(args[0])
    def r_handle_select(self, event):
        for lb in self.rListOfListboxes:
            if lb != event.widget:
                lb.selection_clear(0, 'end')
                lb.selection_set(event.widget.curselection())
                lb.activate(event.widget.curselection())
    def r_UpDownHandler(self, event):
        selection = event.widget.curselection()[0]
        if event.keysym == 'Up':
            selection += -1
        if event.keysym == 'Down':
            selection += 1

        if 0 <= selection < event.widget.size():
            for lb in self.rListOfListboxes:
                lb.selection_clear(0, tk.END)
                lb.selection_set(selection)

    #***************************************************
    # alpha name search handler
    def on_key_press(self, event):
        lb = self.pListOfListboxes[0]
        pb = self.pListOfListboxes[1]
        if event.char.isalpha():
            # get the current selection tuple of indexes - empty tuple if nothing
            current_selection = lb.curselection()
            if current_selection:
                current_index = current_selection[0]
            else:
                # search from top - no current selection
                self.searchAlphaFromTop(lb,pb,event.char.lower())
                return
            if lb.get(current_index + 1).lower().startswith(event.char.lower()):
                # next item is another hit
                self.setAlphaPosition(lb,pb,current_index + 1)
            else:
                self.searchAlphaFromTop(lb,pb,event.char.lower())
                return

    def searchAlphaFromTop(self,lb,pb,lowAlpha):
        for ix in range(0,lb.size()):
            item = lb.get(ix)
            if item.lower().startswith(lowAlpha):
                self.setAlphaPosition(lb, pb,ix)
                return
        # if we didn't return then no match found
        self.resetAlphaTop(lb,pb)

    def setAlphaPosition(self,lb,pb,ix):
        lb.selection_clear(0,tk.END)
        lb.selection_set(ix)
        lb.see(ix)
        lb.activate(ix)
        pb.selection_clear(0,tk.END)
        pb.selection_set(ix)
        pb.see(ix)
        pb.activate(ix)

        # ensure we can see it

    def resetAlphaTop(self,lb,pb):
        self.setAlphaPosition(lb,pb,0)

    # def reCalc(self):
    #     # cheap way - just re-display everything like we had entered
    #     self.buildScoringPanels()
    #     to change active status, go back to playerstab
    def populatePframe(self):
        # self.textIndex = 2      # index of name text in pframe child
        self.allPlayerObjects = cfg.ap.allActivePlayers(cfg.clubRecord)
        self.listOfPlayerNames = [pn.LastName + ', ' + pn.FirstName for pn in self.allPlayerObjects]
        # get all results for this one tourney
        self.allTourneyResultObjects = cfg.ar.allTourneyResults(cfg.tourneyRecord)
        self.tourneyPointsList = [sc.GamePoints for sc in self.allTourneyResultObjects]
        self.tourneyIdList =[sc.Player.id for sc in self.allTourneyResultObjects]
        self.idPointsDict = {k:v for (k,v) in zip(self.tourneyIdList, self.tourneyPointsList)}
        self.namePointsDict = {}
        for name in self.listOfPlayerNames:
            self.namePointsDict[name] =  self.idPointsDict.get(cfg.playerRefx[name], -1)
        # namePointDict is now a dictionary in name order with points for the
        # current tournament score card or-1. Cannot use 0 as 0 is a valid game
        # points total when a player has a string of pearls
        self.refreshPframe()
        for lb in self.pListOfListboxes:
            lb.selection_set(0)
            lb.activate(0)
            lb.focus_force()

    def refreshPframe(self):
        # flush both player list boxes
        for lb in self.pListOfListboxes:
            lb.delete(0, tk.END)
        for key in self.namePointsDict:
            print ('Key:Value: ',key, ' ',type(key), ' ',self.namePointsDict[key], ' ',type(self.namePointsDict[key]))
            if int(self.namePointsDict[key]) >=0:
                self.playerPointsListBox.insert('end', self.namePointsDict[key])
            else:
                self.playerPointsListBox.insert('end', ' ')
            self.playerNameListBox.insert('end', key)
        self.goToTopOfPlayers()
       #
    def populateRframe(self):
        # if len(self.listOfResults) > 0:
        #     for lor in self.listOfResults:
        #         lor.destroy()
        # self.resultFrameIndex = 0
        self.listOfResults = []     # and clear out the list
        if self.tourneyResultsCount > 0:
            self.tourneyResults = cfg.ar.tourneyResultsInEntryOrder(cfg.tourneyRecord)
        for p in self.tourneyResults:
            rLine = resultsLine()
            rLine.playerId = p.PlayerID
            rLine.tourneyId = cfg.tourneyRecordId
            rLine.playerName = cfg.playerXref[p.PlayerID]
            rLine.playerGamePoints = p.GamePoints
            rLine.playerGamesWon = p.GamesWon
            rLine.playerSpread = p.Spread
            rLine.playerTaken = p.SkunksTaken
            rLine.playerCash = p.Cash
            rLine.playerGiven = p.SkunksGiven
            rLine.playerEntryOrder = p.EntryOrder
            self.listOfResults.append(rLine)
        self.populateRframeLBs(self.listOfResults)
    def populateRframeLBs (self, rLineList):
        # refactored to allow for refreshing after add or edit line
        # need to empty any existing content
        self.emptyRframeLBs()
        for r in rLineList:
            self.resultsNamesLB.insert(tk.END, cfg.playerXref[r.playerId])  # get name from xref
            self.resultsGpLB.insert(tk.END, r.playerGamePoints)
            self.resultsGwLB.insert(tk.END, r.playerGamesWon)
            self.resultsSprdLB.insert(tk.END, r.playerSpread)
            self.resultsTknLB.insert(tk.END, r.playerTaken)
            self.resultsCashLB.insert(tk.END, r.playerCash)
            self.resultsGvnLB.insert(tk.END, r.playerGiven)
            self.resultsOrderLB.insert(tk.END, r.playerEntryOrder)
    def emptyRframeLBs(self):
        for rlb in self.rListOfListboxes:
            rlb.delete(0, tk.END)
    def emptyPframeLBs(self):
        for plb in self.pListOfListboxes:
            plb.delete(0, tk.END)
    def positionInResultsAtTop(self):
        self.ensureResultLineVisibility(0)
        self.positionInResults(0,1)
    def positionInResults(self,rfidx, fldidx):
        # position at line and field, and move keyboard focus
        self.listOfResults[rfidx].winfo_children()[fldidx].focus_force()

    def initializeSortDictionary(self):
        # set up dictionary to control sort directions
        # would rather associate directly with widget, but no place to hang 'notes'
        self.resultsSortDict = {'nameHdr':None,
                               'gpHdr':None,
                               'gwHdr':None,
                               'sprdHdr':None,
                               'cashHdr':None,
                               'tknHdr':None,
                               'gvnHdr':None,
                               'orderHdr':'Asc'}
    # event handlers
    # handler area for sorting
    def rSortHandler(self, event):
        if event.widget == self.nameHdr:
            self.rSortNames(event)
        elif event.widget == self.gpHdr:
            self.rSortGp(event)
        elif event.widget == self.gwHdr:
            self.rSortGw(event)
        elif event.widget == self.sprdHdr:
            self.rSortSprd(event)
        elif event.widget == self.cashHdr:
            self.rSortCash(event)
        elif event.widget == self.tknHdr:
            self.rSortTkn(event)
        elif event.widget == self.gvnHdr:
            self.rSortGvn(event)
        else:
            self.rSortOrder(event)
    def rSortNames(self,event):
        dir = self.resultsSortDict['nameHdr']
        if dir == None or dir == 'Desc':
            print ('Sort names asc')
            self.resultsSortDict['nameHdr'] = 'Asc'
        else:
            print ('Sort names desc')
            self.resultsSortDict['nameHdr'] = 'Desc'
    def rSortGp(self, event):
        dir = self.resultsSortDict['gpHdr']
        if dir == None or dir == 'Desc':
            print ('Sort gp asc')
            self.resultsSortDict['gpHdr'] = 'Asc'
        else:
            print ('Sort gp desc')
            self.resultsSortDict['gpHdr'] = 'Desc'
    def rSortGw(self, event):
        dir = self.resultsSortDict['gwHdr']
        if dir == None or dir == 'Desc':
            print ('Sort gw asc')
            self.resultsSortDict['gwHdr'] = 'Asc'
        else:
            print ('Sort gw desc')
            self.resultsSortDict['gwHdr'] = 'Desc'
    def rSortSprd(self, event):
        dir = self.resultsSortDict['sprdHdr']
        if dir == None or dir == 'Desc':
            print ('Sort sprd asc')
            self.resultsSortDict['sprdHdr'] = 'Asc'
        else:
            print ('Sort sprd desc')
            self.resultsSortDict['sprdHdr'] = 'Desc'
    def rSortCash(self, event):
        dir = self.resultsSortDict['cashHdr']
        if dir == None or dir == 'Desc':
            print ('Sort cash asc')
            self.resultsSortDict['cashHdr'] = 'Asc'
        else:
            print ('Sort cash desc')
            self.resultsSortDict['cashHdr'] = 'Desc'
    def rSortTkn(self, event):
        dir = self.resultsSortDict['tknHdr']
        if dir == None or dir == 'Desc':
            print ('Sort tkn asc')
            self.resultsSortDict['tknHdr'] = 'Asc'
        else:
            print ('Sort tkn desc')
            self.resultsSortDict['tknHdr'] = 'Desc'
    def rSortGvn(self, event):
        dir = self.resultsSortDict['gvnHdr']
        if dir == None or dir == 'Desc':
            print ('Sort gvn asc')
            self.resultsSortDict['gvnHdr'] = 'Asc'
        else:
            print ('Sort gvn desc')
            self.resultsSortDict['gvnHdr'] = 'Desc'
    def rSortOrder(self, event):
        dir = self.resultsSortDict['orderHdr']
        if dir == None or dir == 'Desc':
            print ('Sort order asc')
            self.resultsSortDict['orderHdr'] = 'Asc'
        else:
            print ('Sort orders desc')
            self.resultsSortDict['orderHdr'] = 'Desc'

    # handle add/edit/delete
    def quitResultLine(self, event):
        # quit and determine where to reposition
        print ('Quit the result line entry with no action.')
        self.clearEditLine()
        self.hideResultsInputPanel()
        self.hideResultsInstructionsPanel()
        self.hideWidget(self.resultsExistingTourney)
        self.hideWidget(self.resultsNewTourney)
        self.playerNameListBox.activate(0)
        self.playerNameListBox.focus_force()
    def editResultsFromPlayer(self, event):
        # user pressed F2 on a player entry
        # check that player has entry in listOfResults
        # if none found then convert to new Result entry
        cfg.tourneyEdit = True
        if self.resultExists(self.playerNameListBox.get(self.playerNameListBox.curselection()[0])):
            self.buildEditLine(self.playerNameListBox.get(self.playerNameListBox.curselection()[0]))
        else:
            self.buildNewLine(self.playerNameListBox.get(self.playerNameListBox.curselection()[0]))
    def editResultsFromResults(self, event):
        # user pressed F2 at a result line
        # set up edit for player on result line
        self.buildEditLine(self.resultsNamesLB.get(self.resultsNamesLB.curselection()[0]))
    def newResult(self, event):
        # user pressed F3 on a player entry - doesn't make sense on a result line
        # get player record for curselection player then create and append resultLine
        # if already result line, then convert to edit
        print ('F3 on player: ',self.playerNameListBox.get(self.playerNameListBox.curselection()[0]))
        if self.resultExists(self.playerNameListBox.get(self.playerNameListBox.curselection()[0])):
            self.buildEditLine(self.playerNameListBox.get(self.playerNameListBox.curselection()[0]))
        else:
            self.buildNewLine(self.playerNameListBox.get(self.playerNameListBox.curselection()[0]))
    def pResultLineDelete(self, event):
        # find result line for name then go to resultLine delete process
        # if player has points in the playerPointsListBox or
        # player has an enty in the listOfResults - there is work to do
        # just look in listOfResults for player name, regardles
        pId = cfg.playerRefx[self.playerNameListBox.get(self.playerNameListBox.curselection()[0])]
        matchingResultLine = self.findResultLineByPid(pId)
        if matchingResultLine >= 0:
            # highliht resultsLine if we found and entry for the player
            self.resultsNamesLB.selection_set(matchingResultLine)
            if mbx.askokcancel('Confirm Delete', 'Do you really want to delete this results?') == True:
                self.deleteResult(pId)
        else:
            mbx.showinfo('No results for this player', 'Try another player')
            # reposition to top of players


    def findResultLineByPid(self, pId):
        # search listof results using playerid for editing
        posn = 0
        for r in self.listOfResults:
            if r.playerId  == pId:
                return posn
            posn += 1
        return -1

    def deleteResultLine(self, event):
        # user pressed F9 on a result line
        # confirm delete with msgbox then remove from listOfResults and from dbms immediately
        pId = cfg.playerRefx[self.resultsNamesLB.get(self.resultsNamesLB.curselection()[0])]
        if mbx.askokcancel('Confirm Delete', 'Do you really want to delete this result?') == True:
            # proceed with the delete
            self.deleteResult(pId)
        else:
            # not yes means leave it alone
            pass
    def deleteResult(self, pId):
        # can be any LB entry on the row of results
        # check if listOfResults line is already in the dbms - so must be deleted from dbms
        # line is always removed from the listOfResults
        # set the single player object by id
        player = cfg.ap.getPlayerById(pId)
        # tourney is in cfg.tourneyRecord
        print ('player selected for result delete', player)
        # get the unique score card for tourney and player
        scoreCard = cfg.ar.getSpecificScoreCard(cfg.tourneyRecord, player)
        if len(scoreCard) > 0:
            ScoreCard.delete(scoreCard[0].id)  # delete score card by id
        # remove score card from listOfResults and compute summary totals
        # we look it up by pId as we may have come here from playerLB rater than resultsLB

        del self.listOfResults[self.findResultLineByPid(pId)]
        playerName = cfg.playerXref[pId]
        self.removePlayerPoints(playerName)
        self.refreshPframe()
        self.updateTotals()
        self.populateRframeLBs(self.listOfResults)
        self.goToTopOfPlayers()
    def goToTopOfResults(self):
        # check that there is anything in results - else revert to players
        if self.resultsNamesLB.size() > 0:
            for rlb in self.rListOfListboxes:
                rlb.selection_set(0)
        else:
            self.goToTopOfPlayers()

    def goToTopOfPlayers(self):
        for plb in self.pListOfListboxes:
            plb.selection_clear(0,tk.END)
            plb.selection_set(0)
            plb.activate(0)
        self.pListOfListboxes[0].see(0)
        self.pListOfListboxes[0].activate(0)
        self.pListOfListboxes[0].focus_force()
        # print (self.pListOfListboxes[0].get(0))

        # self.pListOfListboxes[0].selection_set(0)
        # self.pListOflistboxes[0].focus_force()
    def handleResultLine(self, event):
        # validate entry line then leave in listOfResults in memory if new tourney, else update dbms immediately
        # input could be a correction to an existing line for a new or existing tourney.
        # a new result line could be an addition to new tourney or an addition to an existing tourney
        # TODO: update the points list box for the player list; each location has a ' ' if no points
        #       Update the namePointsDict while still in memory.
        resultPlayerName = ''
        resultPoints = ''
        goodEntry = True
        goodEntry = goodEntry and self.gpValidation()
        goodEntry = goodEntry and self.gwValidation()
        goodEntry = goodEntry and self.spreadValidation()
        goodEntry = goodEntry and self.cashValidation()
        goodEntry = goodEntry and self.takenValidation()
        print('Validations: good gp gw crosscheck spread cash taken ',goodEntry, self.gpValidation(), self.gwValidation(), \
              self.crossCheckGpGw(), self.spreadValidation(), self.cashValidation(), self.takenValidation())
        if not goodEntry:
            # go back to start of entry to retry - or escape
            # must now show this as a line edit rather than line new
            # recycle to user display
            self.resultsGpEntry.focus_force()
            return
        # always recompute the skunks given
        # for a new line added, have to compute Order of Entry
        # always update in-memory results and summary totals
        # if a new tourney - do nothing - will handle at F10/F11 commit
        # if existing tourney - updates are done as they are submitted
        print ('tourneyEdit, newResultLine: ', cfg.tourneyEdit, ' ', cfg.newResultLine)
        if cfg.tourneyEdit == True:
            # editing an existing tourney -
            # can be an exisitng line or a new line being added to the existing tourney
            if cfg.newResultLine == True:
                # create a single new line for the existing tourney
                # add the new line to results line and use updateDBMS
                print ("New result line for tourney edit")
                self.appendNewResultLine()
                self.updateDBMS()
                self.populateRframeLBs(self.listOfResults)
                self.refreshPframe()
            else:
                for r in self.listOfResults:
                    if self.resultsNameVar.get() == r.playerName:
                        r.playerId = cfg.playerRefx[r.playerName]
                        r.playerGamePoints = int(self.resultsGpVar.get())
                        r.playerGamesWon = int(self.resultsGwVar.get())
                        r.playerSpread = int(self.resultsSprdVar.get())
                        r.playerCash = int(self.resultsCashVar.get())
                        r.playerTaken = int(self.resultsTknVar.get())
                        r.playerGiven = self.computeSkunksGiven()
                        resultPlayerName = r.playerName
                        resultPoints = r.playerGamePoints
                        # TODO: now replace the rLine in the listOfResults.
                        self.updateTotals()
                        self.populateRframeLBs(self.listOfResults)
                        # Entry field will never change after initial entry
                        # update dbms with this edited line for Tourney edit else leave for new commit
                        # if not cfg.newTourney:
                        #     self.updateDBMSforEdit(r)
                        # break
            self.removeResultInputLine()
        else:
            # not edit, so must be new so create a new resultLine and append to listOfResults
            # update dmbs with this new line if Tourney edit else leave for new commmit with F10/F11
            self.appendNewResultLine()
            self.removeResultInputLine()
            self.populateRframeLBs(self.listOfResults)
            self.refreshPframe()

        # self.updatePlayerPoints(resultPlayerName, resultPoints)
        self.removeResultInputLine()
        # self.refreshPframe()
        # reset focus to player in playerLB
        self.goToTopOfPlayers()
    def removeResultInputLine(self):
        self.clearEditLine()
        self.hideResultsInputPanel()
        self.hideResultsInstructionsPanel()
    def updatePlayerPoints(self, pName, pPoints):
        # locate player by name then insert the points in place of blank
        # redisplay will use the contents of the namePoints dictionary
        print ('updatePlayer: ', pName, pPoints)
        self.namePointsDict[pName] = pPoints
        print ('namePointsDict: ', self.namePointsDict)
    def removePlayerPoints(self, pName):
        # replace any current point value with a ' '
        self.namePointsDict[pName] = -1
    def resultExists(self, pname):
        print ('Test for existing results for: ', pname, type(pname))
        # nameList = self.resultsNamesLB.get(0,tk.END)
        # print ('namelist:', len(nameList), nameList)
        # change to search listOfResults in memory
        print ('pname: ', pname)
        print ('listOfResults: ', self.listOfResults)
        for rl in self.listOfResults:
            print ('resultLine: ', rl.playerName)
            if pname == rl.playerName:
                return True
        return False
        # return pname in self.resultsNamesLB.get(0, tk.END)
    def maxEntryOrder(self, listOfResultLines):
        # listOfReults may be sorted in a different order so have to loop through
        maxEO = 0
        for r in listOfResultLines:
            maxEO = max(maxEO, r.playerEntryOrder)
        print ('maxEO. ', maxEO)
        return maxEO
    def clearEditLine(self):
        # reset all edit line fields for a new results or editing an existing result
        self.resultsNameVar.set('')
        self.resultsGpVar.set('')
        self.resultsGwVar.set('')
        self.resultsSprdVar.set('')
        self.resultsCashVar.set('')
        self.resultsTknVar.set('')
        self.resultsGvnVar.set('')      # this field is always computed
        self.resultsOrderVar.set('')
        self.resetResultLineHiLites()

    def buildEditLine(self, pname):
        # fill in line with existing entry
        print ('Build edit line for: ', pname)
        # get playerid for using listOfResults of rLines
        cfg.tourneyEdit = True      # needed later by dbms update
        cfg.newResultLine = False   # editing exisitng result line
        self.clearEditLine()
        self.resultsNameVar.set(pname)
        pid = cfg.playerRefx[pname]
        for r in self.listOfResults:
            if r.playerId == pid:
                self.resultsGpVar.set(r.playerGamePoints)
                self.resultsGwVar.set(r.playerGamesWon)
                self.resultsSprdVar.set(r.playerSpread)
                self.resultsCashVar.set(r.playerCash)
                self.resultsTknVar.set(r.playerTaken)
                self.resultsGvnVar.set(r.playerGiven)
                self.resultsOrderVar.set(r.playerEntryOrder)
        self.showResultsInputPanel()
        self.showWidget(self.resultsTourneyTypePanel)
        self.showResultsInstructionsPanel()
        self.resultsGpEntry.focus_force()
    def buildNewLine(self, pname):
        # just fill in the name, leave rest blank
        # if already results for player then this becomes and edit
        print ('Build new line for: ',pname)
        # This is an error. Could just be a new player line for a
        # tourney that is being edited.
        # cfg.tourneyEdit = False
        cfg.newResultLine = True
        print ('buildNewLine: ', cfg.newTourney, ' ', cfg.tourneyEdit, ' ', cfg.newResultLine)
        self.clearEditLine()
        self.resultsNameVar.set(pname)
        self.resultsTknVar.set(0)           # in case the user skips it
        self.resultsCashVar.set(0)           # default winnings!
        self.showResultsInputPanel()
        self.showResultsInstructionsPanel()
        self.resultsNameVar.set(pname)
        self.resultsGpEntry.focus_force()
    def newTourney(self):
        # if cfg.tourney has entered set then cfg.newTourney flag is false, else it's true
        # cfg.tourneyRecord has the SQLObject for the tourney selected in tourneystab
        if cfg.tourneyRecord.Entered == '*':
            cfg.newTourney = False
        else:
            cfg.newTourney = True
        cfg.tourneyEdit = not cfg.newTourney
        print ('self.newTourney, newTourney, tourneyEdit: ', cfg.newTourney, ' ', cfg.tourneyEdit)
        return cfg.newTourney
    def commitResults(self, event):
        # user pressed F10 to commit results to dbms
        if self.outOfBalance():
            mbx.showinfo('Tourney out of balance.', 'Use F11 to force results save.')
            return              # quite without saving out-of-balance tourney
        self.updateDBMS()
        self.clearResultLines()
        cfg.screenDict['notebook'].select(1)       # return to tourneys tab
        # self.clearUpEverything()
        # return to tourneytabs screen
    # def saveNewTourney(self):
    #     print('Save newly entered Tourney in dbms and update results display')
    def forceResultsCommit(self, event):
        # user pressed F11 to commit an unbalanced tourney to dbms or just save for now - leave memory intact
        if mbx.askyesno('Force out-of-balance save', 'Force save of tourney results?')  == True:
            print ('Force updatedmbs')
            self.updateDBMS()
            self.clearResultLines()
            # self.cleanEverything()
        else:
            pass        # don't force save and leave memory intact
    def outOfBalance(self):
        # false if everything balances, else True
        return self.diffSpread.get() != 0 or self.diffSkunks.get() != 0
    def backToPlayers(self):
        # user pressed F7 to return to list of Players
        # just leave the listOfResults as they are
        self.playerNameListBox.selection_set(0)     # back to first player list bax entry
    def quitResults(self, event):
        # user pressed Escape to abandon work in progress
        if mbx.askyesno('Quit Entry', 'Quit and drop any new input?') == 'Yes':
            self.clearResultLines()
            self.backToPlayers()
        else:
            pass    # just do nothing
    # def createPlayerXref(self):
    #     # cross-refs used to build results screens
    #     cfg.playerXref = {p.id : p.LastName + ', ' + p.FirstName for p in list(Player.select())}
    #     cfg.playerRefx = { v:k for k, v in cfg.playerXref.items()}
    def clearResultLines(self):
        # after entering results, clear out all results
        self.listOfResults = []
        self.emptyRframeLBs()
        self.emptyPframeLBs()
    def computeSkunksGiven(self):
        print ('gp: ', self.resultsGpVar.get(), 'gw: ', self.resultsGwVar.get())
        return int(self.resultsGpVar.get()) - 2 * int(self.resultsGwVar.get())
    def justNumeric(self, input):
        if input.isnumeric():
            return True
        elif input == '':
            return True
        else:
            return False
    def minusNumeric(self, input):
        # get the complete input for spread
        try:
            int(input)
            return True
        except:
            return False
    def gpValidation(self):
        # only digits allowed in by validationcommand
        # validate permissible range of gp
        # always start by resetting errorlite
        self.resetScoringErrorHiLite(self.resultsGpEntry)
        gp = self.resultsGpVar.get()       # get the gp for the line
        # if not gp.isnumeric():
        #     self.errorHiLite(self.resultsGpEntry)
        #     return False
        if int(gp) > 35:
            self.errorHiLite(self.resultsGpEntry)
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
    def gwValidation(self):
        # only digits allowed in by validation command
        # validate permissible games won
        self.resetScoringErrorHiLite(self.resultsGwEntry)
        gw = self.resultsGwVar.get()       # get the gw for the line
        # if not gw.isnumeric():
        #     self.errorHiLite(self.resultsGwEntry)
        #     return False
        if int(gw) > 18:
            print('GW value ', gw, ' not possible')
            self.errorHiLite(self.resultsGwEntry()                             )
            return False
        if not self.crossCheckGpGw():
            self.errorHiLite(self.resultsGpEntry)
            self.errorHiLite(self.resultsGwEntry)
            return False
        self.resultsGvnVar.set(str(self.computeSkunksGiven()))
        return True
    def crossCheckGpGw(self ):
        # we are checking the resultsline input area
        gp = int(self.resultsGpEntry.get())
        gw = int(self.resultsGwEntry.get())
        print ('gp: gw: ', gp, ' ',gw)
        if gp >= (2 * gw):
            return True
        else:
            self.errorHiLite(self.resultsGpEntry)
            self.errorHiLite(self.resultsGwEntry)
            return False

    def spreadValidation(self):
        # only digits allowed in by validationcommand
        # validate total spread
        # TODO: allow user to accept a huge spread - over/under 350
        spread = self.resultsSprdVar.get() # get the spread for the line
        self.resetScoringErrorHiLite(self.resultsSprdEntry)
        if abs(int(spread)) > 350:
            print ('Check Huge Spread value ', spread)
            self.errorHiLite(self.resultsSprdEntry)
            return False
        return True
    def cashValidation(self):
        # only digits allowed in by validationcommand
        # validate amount of cash
        cash = self.resultsCashVar.get()   # get the cash awarded
        self.resetScoringErrorHiLite(self.resultsCashEntry)
        # try:
        #     int(cash)
        # except ValueError:
        #     self.errorHiLite(self.resultsCashEntry)
        #     return False
        if int(cash) < 0 or int(cash) > 150:
            self.errorHiLite(self.resultsCashEntry)
            return False
        return True
    def takenValidation(self):
        # only digits allowed in by validationcommand
        # validate number of taken skunks
        self.resetScoringErrorHiLite(self.resultsTknEntry)
        taken = self.resultsTknVar.get() # get the skunks taken for the line
        # if not taken.isnumeric():
        #     self.errorHiLite(self.resultsTknEntry)
        #     return False
        if int(taken) > 9:
            print('Taken value ', taken,' not possible')
            self.errorHiLite(self.resultsTknEntry)
            return False
        return True
    # TODO: after we leave a line, and no errors, then update the dmbs entry using SQLObject
    def updateDBMSforEdit(self, r):
        # just update the single line that was changes
        # r is the resultLine object
        # we first need to retrieve the scorecard record before we update it
        print ('r: ', r)
        print('r.playerId: ', r.playerId)
        playerRecord = Player.get(r.playerId)
        tourneyRecord = cfg.tourneyRecord
        # TODO: Why do we come here when adding another line to a partial tourney?
        if mbx.askokcancel('Ok to Save?', 'Do you want to save the edit?') == True:
            changeScoreCard = cfg.ar.getSpecificScoreCard(tourneyRecord, playerRecord)[0]
            # update all of the fields linearly - slow but works
            changeScoreCard.GamePoints = r.playerGamePoints
            changeScoreCard.GamesWon = r.playerGamesWon
            changeScoreCard.Spread = r.playerSpread
            changeScoreCard.SkunksTaken = r.playerTaken
            changeScoreCard.SkunksGive = r.playerGiven
            # scoreCard = ScoreCard(Tourney=cfg.tourneyRecord,
            #                       Player=playerRecord,
            #                       GamePoints=r.playerGamePoints,
            #                       GamesWon=r.playerGamesWon,
            #                       Spread=r.playerSpread,
            #                       Cash=r.playerCash,
            #                       SkunksTaken=r.playerTaken,
            #                       SkunksGiven=r.playerGiven)
            # skip entry order as it should never change
            #                       EntryOrder=r.playerEntryOrder)
            # just rebuild the results frame from updated dbms
            self.populateRframe()
            self.clearEditLine()
            self.goToTopOfPlayers()
        else:
            # leave everything where is is
            self.resultsGpEntry.focus_force()
    def updateDBMS(self):
        # take all of the resultLine objects in listOfResults and add them to the dbms
        # replace them or add new
        # tourney record is already in cfg.tourneyRecord
        print ('updateDBMS, listOfResults: ', self.listOfResults)
        for r in self.listOfResults:
            playerRecord = Player.get(r.playerId)
            scoreCard = cfg.ar.getSpecificScoreCard(cfg.tourneyRecord, playerRecord)
            if len(scoreCard) < 1:
                print ('Add score card for: ', playerRecord.id, playerRecord.LastName)
                # no such record, so create one
                ScoreCard(Tourney =cfg.tourneyRecord,
                          Player = playerRecord,
                          GamePoints = r.playerGamePoints,
                          GamesWon = r.playerGamesWon,
                          Spread = r.playerSpread,
                          Cash = r.playerCash,
                          SkunksTaken = r.playerTaken,
                          SkunksGiven = r.playerGiven,
                          EntryOrder = r.playerEntryOrder)
            else:
                scoreCard[0].set(GamePoints = r.playerGamePoints,
                                 GamesWon = r.playerGamesWon,
                                 Spread = r.playerSpread,
                                 Cash = r.playerCash,
                                 SkunksTaken = r.playerTaken,
                                 SkunksGiven = r.playerGiven,
                                 EntryOrder = r.playerEntryOrder)
        # finally update the tourney record
        cfg.tourneyRecord.set(Entered = '*')
         # TODO: Will have to track where we need updates vs. creates - really for F10 following an F11
    def appendNewResultLine(self):
        # used by new tourney new line or existing tourney add new line
        r = resultsLine()
        # resultPlayerName = r.playerName
        r.playerName = self.resultsNameVar.get()
        r.playerId = cfg.playerRefx[r.playerName]
        r.playerGamePoints = int(self.resultsGpVar.get())
        r.playerGamesWon = int(self.resultsGwVar.get())
        r.playerSpread = int(self.resultsSprdVar.get())
        r.playerCash = int(self.resultsCashVar.get())
        r.playerTaken = int(self.resultsTknVar.get())
        r.playerGiven = self.computeSkunksGiven()
        # resultPlayerName = r.playerName
        # resultPoints = r.playerGamePoints
        r.playerEntryOrder = self.maxEntryOrder(self.listOfResults) + 1
        self.listOfResults.append(r)  # add new line to display stack
        self.updateTotals()
        # need to make sure points are updated in points/players listboxes
        # needs to use playername as dict key
        # self.namePointsDict[r.playerId] = r.playerGamePoints
        self.namePointsDict[r.playerName] = r.playerGamePoints
        print ('Points dict: ', self.namePointsDict)
        # self.populateRframe()

    def updateTotals(self):
        # step through all results and refresh totals
        # use listOfResults - new Tourney has no dbms entries yet!
        # print ('self.tourneyResults ', self.tourneyResults)
        # print ('GP: ',[p.GamePoints for p in self.tourneyResults ])
        # print ('Game Points: ',[p.GamePoints for p in self.tourneyResults if p.GamePoints > 0])
        self.plusSpread.set(sum([p.playerSpread for p in self.listOfResults if p.playerSpread > 0]))
        self.minusSpread.set(sum([m.playerSpread for m in self.listOfResults if m.playerSpread < 0]))
        self.givenSkunks.set(sum([g.playerGiven for g in self.listOfResults]))
        self.takenSkunks.set(sum([t.playerTaken for t in self.listOfResults]))
        self.diffSpread.set(self.plusSpread.get() + self.minusSpread.get())
        self.diffSkunks.set(self.givenSkunks.get() - self.takenSkunks.get())
        self.count.set(len(self.listOfResults))
    def updatePlayerCount(self):
        # count players for current tourney in database
        # TODO: This won't work before commit for a results edit before commit.
        #       Have to count the number of records in listOfResults.
        self.count.set(cfg.ar.countTourneyResults(cfg.tourneyRecord))
    def resetEditEntry(self):
        # clear out the control variables
        self.resultsNameField = None
        self.resultsGpField = None
        self.resultsGwField = None
        self.resultsSprdField = None
        self.resultsCashField = None
        self.resultsTknField = None
        self.resultsGvnField = None
    def hiLiteNextName(self, idx):
        self.resetHilite(self.pFrame.interior.winfo_children()[idx].winfo_children()[self.textIndex])
        self.hiLiteActiveName(idx + 1)

    # def hiLitePriorName(self, idx):
    #     self.resetHilite(self.pFrame.interior.winfo_children()[idx].winfo_children()[self.textIndex])
    #     self.hiLiteActiveName((idx - 1))

    # def resetHilites(self):
    #     for w in self.pFrame.interior.winfo_children():
    #         self.resetHilite(w.winfo_children()[self.textIndex])
    def resetResultLineHiLites(self):
        self.resetScoringErrorHiLite(self.resultsGpEntry)
        self.resetScoringErrorHiLite(self.resultsGwEntry)
        self.resetScoringErrorHiLite(self.resultsSprdEntry)
        self.resetScoringErrorHiLite(self.resultsTknEntry)
    def hiLiteGamePoints(self,w):
        self.hilite(w)
    def hilite(self, w):
        w.config(background='blue', foreground='yellow')
    def resetHilite(self, w):
        w.config(background='whitesmoke', foreground='black')
    def errorHiLite(self, w):
        w.config(background='red', foreground='white')
    def resetScoringErrorHiLite(self, w):
        self.resetEntryHiLite(w)
    def resetEntryHiLite(self, w):
        w.config(background='white', foreground='black')
    def hideResultLineErrorMessages(self):
        self.hideWidget(self.gpError)
        self.hideWidget(self.gwError)
        self.hideWidget(self.spreadError)
        self.hideWidget(self.cashError)
        self.hideWidget(self.tknError)
    def hideResultsInputPanel(self):
        self.hideWidget(self.resultsInputPanel)
    def hideResultsInstructionsPanel(self):
        self.hideWidget(self.resultsEntryInstructionsPanel)
    def showResultsInputPanel(self):
        self.showWidget(self.resultsInputPanel)
    def showResultsInstructionsPanel(self):
        self.showWidget(self.resultsEntryInstructionsPanel)
    def hideWidget(self, w):
        w.grid_remove()
    def showWidget(self, w):
        w.grid()

if __name__ == "__main__":
    #############################################
    # hardwire cfg for testing                  #
    cfg.appTitle = 'Results Testing'  #
    cfg.clubNumber = 100  #
    cfg.season = '2019-20'  #
    cfg.clubName = 'Peggers}'  #
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
    cfg.clubRecord = Club.get(1)
    print ('Club record: ', cfg.clubRecord)
    cfg.clubId = cfg.clubRecord.id
    club100 = Club.select(Club.q.clubNumber == 100)
    ap = AccessPlayers()
    players = ap.allPlayers(cfg.clubRecord)
    print (players)

    print('Count of players: ',ap.countPlayers(club100))
    countOfPlayers = ap.countPlayers(club100)
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
    app = ResultsTab(root)
    app.rowconfigure(0, weight=1)
    app.columnconfigure(0, weight=1)
    app.columnconfigure(1, weight=1)
    app.master.title('Result Panel 1')
    app.mainloop()
