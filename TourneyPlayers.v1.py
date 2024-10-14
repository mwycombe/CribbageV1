#TourneyPlayers.py
##########################################################
#
# select players and assign seat number
#
# this module will select the players for this tourney
# and assign a seat number.
# these assignments will be recorded in the data base
# and will then be retrieved to record the results
#
##########################################################

# System imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg
from sqlobject import *
import sys
import os

# Personal imports
import SeniorsConfig as cfg
from Club import Club
from Tourney import Tourney
from Player import Player
from MemPlayer import MemPlayer
from MemScoreCard import MemScoreCard
from MemGame import MemGame

class TourneyPlayers (ttk.Frame):
    #
    # This class is itself a ttk Frame
    #

#************************************************************
#
    def __init__(self, parent=None):
        super().__init__( parent)
        self.grid()
        print ('TourneyPlayers starting . . . ')
        
        #####################################################
        #
        # control variables for GUI
        #
        #####################################################

        self.existingTourneyValues = tk.StringVar()
        self.tourneyDate = tk.StringVar()
        self.tourneyRecordId = ''       # id of the tourney record for selected date
        self.clubId = ''                # used when linking things together
        self.playersInTourney = {}      # keyed by playerId
        self.tourneyScorecards = {}     # keyed by playerId- nest dict of games in each scorecard
        self.nineGames          = {}    # one set of nine games for a std club tourney
        self.s_p_ids = []               # ids of players selected for a Tourney
        self.s_p_id_names = {}          # dict of tourney player ids to names
        self.seatAssignments = {}       # dict of player id to seat in Tourney
        self.playerToScore = tk.IntVar() # used to capture which player to enter scores for
        self.gameArray = {}             # array for game score entry

        # listbox variables
        self.s_p_names = []             # start with empty dictionary
        
        #
        # set up club we are going to use - only one at this time
        #
                
        self.clubPanel = ttk.LabelFrame (self,
                                    height='3c',
                                    width = '10c',
                                    borderwidth='5p',
                                    relief = 'sunken',
                                    text = 'Club')
        self.clubPanel.grid(row=0, column = 0,
                            sticky='nsew',columnspan = 2)

        ttk.Label(self.clubPanel,
                   text ='  Using Club Name =  ',
                   relief = 'sunken',
                   borderwidth = '2c'
                  ).grid(row = 0,column = 0,sticky = 'w')
        
        self.clubName = Club.get(1).ClubName
        self.clubNumber = Club.get(1).ClubNumber
        self.clubId = Club.get(1).id
                
        ttk.Label(self.clubPanel,
                  text = self.clubName,
                  relief = 'sunken',
                  borderwidth = '2c',
                  font = ('Helvetica','10','bold'),
                  foreground='blue',
                  ).grid (row = 0,column = 1,sticky = 'e')
        #
        # set up tabbed notebook
        #
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0,
                           sticky='nsew')
        #
        # set notebook virtual event handler
        # and build the notebook tabs
        #
        
        self.notebook.bind("<<NotebookTabChanged>>",self.tabChange)
        
        self.pickTourney = ttk.Frame(self.notebook,
                                     padding = '10p')
        self.notebook.add(self.pickTourney, text='Tourney')

        self.assignPlayers = ttk.Frame(self.notebook,
                                       padding = '10p')
        self.notebook.add(self.assignPlayers, text='Players')

        self.assignSeats = ttk.Frame(self.notebook,
                                     padding = '10p')
        self.notebook.add(self.assignSeats, text = 'Seats')

        self.scoring = ttk.Frame(self.notebook,
                                 padding = '10p')
        self.notebook.add(self.scoring, text = 'Scoring')

        #
        # Build Tourney tab
        #
        self.tourneyPanel = ttk.LabelFrame(self.pickTourney,
                                           relief='sunken',
                                           height='10c',
                                           width = '10c',
                                           padding='10p',
                                           text='Select Tourney'
                                           )
        self.tourneyPanel.grid(row=0, column=0,
                               sticky='nsew')
        # tourney panel row 0
        
        self.doubleClickLabel = ttk.Label(self.tourneyPanel,
                  text='Double Click Date for Tourney')
        self.doubleClickLabel.grid(row=0, column=0)

        #
        # tourney panel row 1
        #
        # show past tourneys - arbitrarily show 12 - no scroll bar for now
        #
        self.existingTourneysLabel = ttk.Label(self.tourneyPanel,
                                          text = 'Existing Tourneys:   ')
        self.existingTourneysLabel.grid(row=4, column=0, sticky = 'n')
        self.existingTourneys = tk.Listbox(self.tourneyPanel,
                                       listvariable=self.existingTourneyValues)
        self.existingTourneys.grid(row=4, column=1)
        self.populateExistingTourneys()

        #
        # have to bind event to listbox as there is no command option
        #
        self.existingTourneys.bind('<Double-Button-1>',self.selectedTourney)
        
        #
        # Build Players tab
        #
        self.playerPanel = ttk.LabelFrame(self.assignPlayers,
                                          relief='sunken',
                                          height='10c',
                                          width = '10c',
                                          padding='10p',
                                          text='Assign Players'
                                          )
        self.playerPanel.grid(row=0, column=0,
                              sticky='nsew')
        # player panel row 0
        
        self.tourneyLabel = ttk.Label(self.playerPanel,
                                      text='Selected Tourney Date is:   ')
        self.tourneyLabel.grid(row=0, column=0)

        self.dateOfTourney = ttk.Label(self.playerPanel
                                       )
        self.dateOfTourney.grid(row=0, column=1)

        #
        # player panel row 1
        #
        ttk.Label(self.playerPanel,
                  text='Check players then press Seating button').grid(row=1, column=0)
        self.populatePlayers()      # retrieve players and build check box selection list
 
        #
        # Build Seats tab
        #
        self.seatsPanel = ttk.LabelFrame(self.assignSeats,
                                         relief='sunken',
                                         height='10c',
                                         width ='10c',
                                         padding='10p',
                                         text='Assign Seats'
                                         )
        self.seatsPanel.grid(row=0, column=0)
        ttk.Label(self.seatsPanel,
                  text='Assign unique seat number and press Assign button').grid(row=0, column=0,
                                                                                 columnspan=2)

        #
        # Build Scoring tab
        #
        self.scoringPanel = ttk.LabelFrame(self.scoring,
                                           relief='sunken',
                                           height='10c',
                                           width = '10c',
                                           padding='10p',
                                           text='Enter Score Cards'
                                           )
        self.scoringPanel.grid(row=0, column=0)
        self.scoringPanelHeader = ttk.Frame(self.scoringPanel,
                                            relief='sunken',
                                            height='10c',
                                            width = '10c',
                                            padding='10p'
                                            )
        self.scoringPanelHeader.grid(row=0, column=0,sticky='nsew')

        #
        # Build scoring panel header frame
        #
        ttk.Label(self.scoringPanelHeader,
                     text='Tourneys'
                     ).grid(row=0, column=0, columnspan=2,
                            sticky='ew')
        ttk.Label(self.scoringPanelHeader,
                     text='Select a Player From List'
                     ).grid(row=1, column=0, sticky='w')
        ttk.Label (self.scoringPanelHeader,
                     text='. . . and Enter Game Scores'
                     ).grid(row=2, column=0, sticky='w')
        clubNameLabel = 'Using Club:  ' + self.clubName
        ttk.Label(self.scoringPanelHeader,
                     text=clubNameLabel
                     ).grid(row=1, column=1, sticky = 'e')
        tourneyDateLabel = 'Tourney Date: ' + self.tourneyDate.get()
        ttk.Label(self.scoringPanelHeader,
                     text=tourneyDateLabel
                     ).grid(row=2, column=1, sticky = 'e')

        #
        # Build scoring entry panel
        #
        self.scoringEntryPanel = ttk.Frame(self.scoringPanel,
                                           relief='sunken',
                                           height='10c',
                                           width = '10c',
                                           padding='10p'
                                           )
        self.scoringEntryPanel.grid(row=1, column=0, sticky='nsew')


#************************************************************
#
    def populateExistingTourneys(self):
        #
        # retrieve up to twelve existing tourneys for display
        # latest first
        # TODO only show empty tourneys' unless we are correcting
        #
##        print (Tourney.select)
        self.dbmsTourneyDates = list(Tourney.select().orderBy('-Date'))
        self.existingTourneyValues.set([self.dbmsTourneyDates[x].Date for x in range(len(self.dbmsTourneyDates))])

#************************************************************
#
    def selectedTourney(self, event):
        # this is activated by DoubleClick-1 : left mouse button
        self.listBoxIndex = self.existingTourneys.curselection()
        print(eval(self.existingTourneyValues.get())[self.listBoxIndex[0]])
        self.tourneyDate.set(eval(self.existingTourneyValues.get())[self.listBoxIndex[0]])
        print ('tourneyDate:=  ' + self.tourneyDate.get())
        self.tourneyRecordId = self.getTourneyId(self.tourneyDate.get())
        self.notebook.select(1)     # go to players tab
        self.dateOfTourney.config(text=self.tourneyDate.get())
#************************************************************
#
    def getTourneyId(self,date):
        print (date)
        t = Tourney.select(Tourney.q.Date == date)
        l = list(t)
##        print (l)
##        print (l[0].id)
        return l[0].id
 
#************************************************************
#
    def populatePlayers (self):
        print('populate players')
        all_players = Player.select().orderBy('FirstName')
        player_name_list = [x.FirstName + ' ' + x.LastName for x in list(all_players)]
        player_id_list = [x.id for x in list(all_players)]
        print (player_name_list)
        print (player_id_list)
        self.list_of_zeros = [0 for x in all_players]
        player_name_tuples = zip(player_name_list,
                                 self.list_of_zeros)
        list_of_player_name_tuples = [list(y) for y in player_name_tuples]
        name_zero_list = zip(player_id_list,
                             list_of_player_name_tuples)
        self.player_dict = {key:value for key, value in name_zero_list}
        print (self.player_dict)
        for player_id in self.player_dict:
            self.player_dict[player_id][1] = tk.Variable()
            cb = ttk.Checkbutton(self.playerPanel,
                                 text=self.player_dict[player_id][0],
                                 variable=self.player_dict[player_id][1])
            cb.grid(sticky='w')
        print ('Setup of checkbuttons done...')
        assign_button = ttk.Button(self.playerPanel,
                                   text='Seating',
                                   command=self.assignPlayerstoTourney
                                   )
        assign_button.grid()
      
#************************************************************
#
    def tabChange(self,event):
        # from here we can find out which tab is currently selected.
        print ('Tab change')
##        print (self.notebook.tabs())
##        print (self.notebook.select())
##        if self.notebook.select() == '.!notebook.!frame2':
##            print ('On tab 2 - Players')
##        print('Tab Players tab index is: ',self.notebook.index('.!notebook.!frame2'))
##                                
#************************************************************
#
    def assignPlayerstoTourney(self):
        # parse slections and build in-memory tourney structure
        print ('Assign players to tourney')
        self.s_p_ids =[]
        self.s_p_names = []
##        print(self.player_dict)
        for player in self.player_dict:
            if self.player_dict[player][1].get() == '1':
                self.s_p_ids.append(player)
                self.s_p_names.append(self.player_dict[player][0])
        print (self.s_p_ids)
        print (self.s_p_names)
        self.getSeatingAssignments()
#************************************************************
#

    def getSeatingAssignments(self):
        # build the structure ready for seat assignments
        self.notebook.select(2)     # go to Seats tab
        ## selected_tuples = zip(self.s_p_names,self.list_of_zeros)
        list_of_selected_tuples = [list(y) for y in zip(self.s_p_names,
                                                        self.list_of_zeros)]
        print (list_of_selected_tuples)
        self.seatingDict = {key: value for key, value in zip(self.s_p_ids,list_of_selected_tuples)}

        for x in self.seatingDict:
            self.seatingDict[x][1] = tk.StringVar()
        print ('seatingDict: ')
        print (self.seatingDict)

        ttk.Label(self.seatsPanel,text='Player Name').grid(row=1,
                                                           column=0,
                                                           sticky='e')
        ttk.Label(self.seatsPanel,text='Seat Number').grid(row=1,
                                                            column=1,
                                                           sticky='w')

        n = 3
        for k in self.seatingDict:
            ttk.Label(self.seatsPanel,text=self.seatingDict[k][0]).grid(row=n,
                                                                        column=0,
                                                                        sticky='e')
            ttk.Entry(self.seatsPanel,
                      textvariable=self.seatingDict[k][1],
                      width=5).grid(row=n,
                                    column=1,
                                    sticky='w')
            n += 1
        
        self.playerSeats = ttk.Button(self.seatsPanel,
                                      text='Assign',
                                      command=self.readSeatAssignments)
        self.playerSeats.grid(row=n, column=1)
        
#************************************************************
#
    def readSeatAssignments(self):
        for k in self.seatingDict:
            self.seatAssignments[k]=self.seatingDict[k][1].get()
        self.validateSeatAssignments()
        print(self.seatAssignments)
        self.buildTourneyInMemory()
        self.buildScoringTab()
        self.notebook.select(3)

#************************************************************
#   Make sure there are no duplicate seat assignments
#
    def validateSeatAssignments (self):
        # go through and makes sure every seat number is unique
        testSeats = {}
        for k in self.seatAssignments:
            if k in testSeats:
                self.showDuplicateSeats(k)
                return
            else:
                testSeats[k] = self.seatAssignments[k]

        # if we drop through then all seats were found to be unique
        #
        # re-key seat assignment by seat
        # only do this after ensuring seat numbers are unique
        #
        self.seatsBySeat = {}
        for k in self.seatAssignments:
            self.seatsBySeat[self.seatAssignments[k]] = k
            
#************************************************************
#   Show duplicate seat error and await correctoin
#
    def showDuplicateSeats(self,seat):
        print('Show duplicate seats')
        
       
#************************************************************
#
    def buildTourneyInMemory(self):
        print('Build Tourney')
        self.s_p_id_names = {key:value for key, value in zip(self.s_p_ids,
                                                       self.s_p_names)}
        for k in self.s_p_id_names:
            self.playersInTourney[k] = MemPlayer(k,
                                            self.s_p_id_names[k])

        for k in self.seatAssignments:
            self.tourneyScorecards[k] = MemScoreCard(self.tourneyRecordId,
                                                k,
                                                self.seatAssignments[k])

#************************************************************
#
    def buildScoringTab(self):

        self.pickPlayer = ttk.Frame(self.scoringEntryPanel,
                                    relief='sunken',
                                    height='10c',
                                    width ='10c',
                                    padding='10p'
                                    )
        self.pickPlayer.grid(row=0, column=0, sticky='n')
        self.enterScores = ttk.Frame(self.scoringEntryPanel,
                                     relief='sunken',
                                     height='10c',
                                     width ='10c',
                                     padding='10p'
                                     )
        self.enterScores.grid(row=0, column=1, sticky='n')

        self.scoringEntryPanel.columnconfigure(0,weight=1)
        self.scoringEntryPanel.columnconfigure(1,weight=4)

        ttk.Label(self.pickPlayer,
                  text='Players in This Tournament'
                  ).grid(row=0, column=0)
        
        r = 1
        for k in self.s_p_id_names:
            ttk.Radiobutton(self.pickPlayer,
                            text=self.s_p_id_names[k],
                            value=k,
                            variable=self.playerToScore,
                            command=self.scoreThisPlayer,
                            ).grid(row=r, column=0, sticky='w')
            r += 1     

#************************************************************
#   Read the players id from the Radiobutton and setup scoring panel

    def scoreThisPlayer(self):
        print('Score player:= ' + str(self.playerToScore.get())
              + ' '
              + self.s_p_id_names[self.playerToScore.get()])
        self.buildGameEntry()



#************************************************************
#   Build out game entry panel for selelcted player

    def buildGameEntry(self):
        
        self.gameEntryHeader = ttk.Frame(self.enterScores,
                                         relief='sunken',
                                         height='10c',
                                         width ='10c',
                                         padding='10p'
                                         )
        self.gameEntryHeader.grid(row=0, column=1, sticky='n')    
        
        ttk.Label(self.gameEntryHeader,
                  text='Player Name'
                  ).grid(row=0, column=1, sticky='ew')
        ttk.Label(self.gameEntryHeader,
                  text='Seat No.'
                  ).grid(row=0, column=2, sticky='ew')
        ttk.Label(self.gameEntryHeader,
                  text=self.s_p_id_names[self.playerToScore.get()],
                  relief='raised',padding='10p'
                  ).grid(row=1, column=1, sticky='ew')
        ttk.Label(self.gameEntryHeader,
                  text=self.seatAssignments[self.playerToScore.get()],
                  relief='raised',padding='10p'
                  ).grid(row=1, column=2, sticky='ew')
        ttk.Label(self.gameEntryHeader,
                  text='(Note: Players can play each other more than once at Seniors)'
                  ).grid(row=2, column=1, columnspan=2)

        self.gameEntryDetail = ttk.Frame(self.enterScores,
                                         relief='sunken',
                                         height='10c',
                                         width ='10c',
                                         padding='10p'
                                         )
        self.gameEntryDetail.grid(row=1, column=1, sticky='ew')

        
        ttk.Label(self.gameEntryDetail,text='Cut Card').grid(row=0, column=0)
        ttk.Label(self.gameEntryDetail,text='Game').grid(row=0, column=1)
        ttk.Label(self.gameEntryDetail,text='Points').grid(row=0, column=2)
        ttk.Label(self.gameEntryDetail,text='Plus').grid(row=0, column=3)
        ttk.Label(self.gameEntryDetail,text='Minus').grid(row=0, column=4)
        ttk.Label(self.gameEntryDetail,text='Opp Seat').grid(row=0, column=5)
        self.gameErrorHeader = ttk.Label(self.gameEntryDetail,text=' Errors')
        self.gameErrorHeader.grid(row=0, column=6)

        self.buildGameArray()
        ttk.Button(self.enterScores,
                   text='Read Scores',
                   command=self.readScores
                   ).grid(row=2, column=1)
        
#************************************************************
#
    def buildGameArray(self):
        self.gameArray = {}

        for r in range (1,10):
            varList = []
            varList.append(tk.StringVar())
            varList.append(tk.IntVar())
            varList.append(tk.IntVar())
            varList.append(tk.IntVar())
            varList.append(tk.IntVar())
            varList.append(tk.StringVar())
            self.gameArray[r] = varList
            ttk.Entry(self.gameEntryDetail,
                      textvariable=self.gameArray[r][0],
                      width=3).grid(row=r+1, column=0)
            ttk.Label(self.gameEntryDetail,
                      text=str(r),
                      width=3).grid(row=r+1, column=1)
            ttk.Entry(self.gameEntryDetail,
                      textvariable=self.gameArray[r][1],
                      width=3).grid(row=r+1, column=2)
            ttk.Entry(self.gameEntryDetail,
                      textvariable=self.gameArray[r][2],
                      width=3).grid(row=r+1, column=3)
            ttk.Entry(self.gameEntryDetail,
                      textvariable=self.gameArray[r][3],
                      width=3).grid(row=r+1, column=4)
            ttk.Entry(self.gameEntryDetail,
                      textvariable=self.gameArray[r][4],
                      width=3).grid(row=r+1, column=5)
            ttk.Label(self.gameEntryDetail,
                      textvariable=self.gameArray[r][5],
                      width=15).grid(row=r+1, column=6)

        # hide error header for now
        self.gameErrorHeader.grid_remove()
        

#************************************************************
#
    def readScores(self):
        print('Scores for:= ' + self.s_p_id_names[self.playerToScore.get()])
        for g in range (1,10):
            print('Cut Card: ' + self.gameArray[g][0].get()
                  + ' Game: ' + str(g)
                  + ' Points: ' + str(self.gameArray[g][1].get())
                  + ' Plus: ' + str(self.gameArray[g][2].get())
                  + ' Minus: ' + str(self.gameArray[g][3].get())
                  + ' Opp Seat: ' + str(self.gameArray[g][4].get())
                  )
        #
        # Validate lines before we build memory structures - no point in building error-filled structures
        #
        gameErrors = self.validateGameScores()
        if gameErrors:
            # somewhere there are errors to show - show the column header
            self.gameErrorHeader.grid()
            for g in self.errorArray:
                if self.errorArray[g]:
                    errorString = self.decodeErrorCode(self.errorArray[g])
                    self.showErrorString(g,errorString)
        else:
            # no errors found so build MemGame and MemScorecard
            # Now we build the in-memory representation for this score card and games for this player
            self.gameErrorHeader.grid_remove()
            self.buildMemScoreCard (self.playerToScore.get(), self.gameArray)

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
        self.gameArray[g][5].set(eString)

#************************************************************
#   build in-memory score card for a given player's validated game lines.

    def buildMemScoreCard(self, playerId, gameArray):
        print('Build memory score card')
        print('cfg.tourneyId: ' + str(cfg.tourneyId))
        self.tourneyScoreCards[playerId] = MemScoreCard(cfg.tourneyId, playerId, self.seatAssignments[playerId])

        # build up to nine games to associate with this scorecards
        
        self.nineGames = {}     # clear out the games dict
        
        for x in range(1,10):
            if gameArray[x][3] > 0 :
                spread = gameArray[x][3]    # this was a win
            else:
                spread = -gameArray[x][4]   # this was a loss
            self.nineGames[x] = MemGame(game = x,
                                        points = gameArray[x][2].get(),
                                        spread = spread,
                                        opponent = gameArray[x][5],
                                        cutCard = gameArrat[x][1]
                                        )
            
        # plug the nine game array into the in-memory score card
        
        self.tourneyScoreCards[playerid].games = self.nineGames
            

#************************************************************
#   check that each line has valid entries that are in range and self-consistent
#   all-zero lines are permitted for Senior Tourney

    def validateGameScores(self):
        anyError = 0
        self.errorArray = {}
        self.pointsDict = {0:0,2:2,3:3}
        self.cardDict = {'A':'A','1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':'J','Q':'Q','K':'K'}
        self.errorDict = {'NoError':0,
                      'Points':1,
                     'PlusMinus':2,
                     'Seat':4,
                     'Cut':8,
                     }
            
        for g in self.gameArray:
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
        return (self.gameArray[g][1].get() == 0 and
                self.gameArray[g][2].get() == 0 and
                self.gameArray[g][3].get() == 0 and
                self.gameArray[g][4].get() == 0
                )

#************************************************************
#   check a game line for point errors

    def validatePoints(self,g):
        # save values we want to test
        points = self.gameArray[g][1].get()
        plus   = self.gameArray[g][2].get()
        minus  = self.gameArray[g][3].get()
        seat   = self.gameArray[g][4].get()
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
        points = self.gameArray[g][1].get()
        plus   = self.gameArray[g][2].get()
        minus  = self.gameArray[g][3].get()
        seat   = self.gameArray[g][4].get()

        if (plus == 0 and minus == 0) or(plus == 0 and minus == 0) or(points == 2 and plus == 0) or (points == 2 and plus > 30) or (points == 3 and plus < 31):
##            print ('+/- error')
            return self.errorDict['PlusMinus']
        else:
            return self.errorDict['NoError']

#************************************************************
# check a game line for seat errors

    def validateSeat (self, g):
        # save value we want to test
        seat   = self.gameArray[g][4].get()
        print (self.seatsBySeat)
        if str(seat) not in self.seatsBySeat:
##            print('Seat:= ' + str(seat))
##            print(self.seatsBySeat)
##            print('Seat error')
            return self.errorDict['Seat']
        else:
            return self.errorDict['NoError']

#************************************************************
# check a game line for cut card error

    def validateCut (self, g):
        cutCard = self.gameArray[g][0].get()
        # missing cutCard is ok
##        print ('CutCard:= ' + cutCard)
        if cutCard == '' or cutCard in self.cardDict:
            return self.errorDict['NoError']
        else:
##            print('Cut error')
            return self.errorDict['Cut']


#************************************************************
#


#************************************************************
#

#************************************************************
#

if __name__ == '__main__':
    # search baseDir for a sqlite3 file - i.e. a dbms
    # make sure we are positioned at the appropriate directory
    #
    appTitle = ''
    dbmsDirectory = ''
    dbmsName = ''
    season = ''
    try:
        cfg = open('Seniors.cfg')      # this is the master config file
    except FileNotFoundError:
        print ('Unable to locate Seniors.cfg\n Terminating')
        sys.exit(-1)
    print ('Config file found')
    for line in cfg:
        print (line)
        eName = line.split(sep='=')[0].strip()
        eValue = line.split(sep='=')[1].strip()
        if eName == 'title':
            appTitle = eValue
        elif eName == 'directory':
            dbmsDirectory = eValue
        elif eName == 'dbms':
            dbmsName = eValue
        elif eName == 'season':
            season = eValue
    # and go to where the data base is located
    os.chdir(dbmsDirectory)

    print ('Current directory: ' + dbmsDirectory)
    print ('appTitle:= ' + appTitle)
    print ('dbmsDirectory:= ' + dbmsDirectory)
    print ('dbmsName:= ' + dbmsName)
    print ('season:= ' + season)

    # see if we can connect to the database
    try:
        print('Connecting to: ' + dbmsDirectory + dbmsName)
        connection_string = 'sqlite:' + dbmsDirectory + dbmsName
        print ('connection_string:= ' + connection_string)
        conn = connectionForURI(connection_string)
        sqlhub.processConnection = conn     # make available to all classses
        # none of these widgets yet exist so promote the
        # action to the higher level
    except:
        print ('Unable to locate data base - terminating')
        os._exit(-1)

    # set up global cfg module for all others to share
    cfg.clubName = 'Senior Center'
    cfg.clubId = 1
    cfg.clubNumber = 999
    cfg.tourneyDate = '2019-05-01'
    cfg.tourneyId = 11
    
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    mp = TourneyPlayers(root)
    root.mainloop()
