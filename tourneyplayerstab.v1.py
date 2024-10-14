#tourneyplayerstab.py
#
#####################################################################
#
#   Creates tab screen for adding players to a tourney
#   Will self-register in notebook found in screenDict of cfg
#   TourneyPlayers was V 1.0 of this tab
#
#####################################################################

# System imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg

from sqlobject import *

import sys as sys
import os as os

# Personal imports
import peggersconfig as cfg
from tourney import Tourney
from player import Player


class TourneyPlayersTab (ttk.Frame):
    # screen class is always a frame

    #************************************************************   
    #   
    #   sets up tab for add/change/delete players in a tourney
    #   and assigning seating in the same tab

    def __init__ (self, tabTarget, parent=None):
        super().__init__( parent)
        #####################################################
        #
        # control variables for GUI
        #
        #####################################################

        self.existingTourneyValues = tk.StringVar()
        self.tourneyDate = tk.StringVar()
        self.clubId = ''                # used when linking things together
        self.playersInTourney = {}      # keyed by playerId
        self.s_p_ids = []               # ids of players selected for a Tourney
        self.s_p_id_names = {}          # dict of tourney player ids to names

        # listbox variables
        self.s_p_names = []             # start with empty dictionary
        

        # build out tab and register with notebook
        self.config(padding = '10p')
        tabTarget.add(self, text='Pick Tourney')
        cfg.screenDict['tptab'] = self
      

        #
        # Tourney Date selection
        #
        # show past tourneys - arbitrarily show 12 - no scroll bar for now
        #

        self.tourneyPanel = ttk.LabelFrame(self,
                                           relief = 'sunken',
                                           height = '10c',
                                           width = '10c',
                                           padding = '10p',
                                           text = 'Select Tourney'
                                           )
        self.tourneyPanel.grid(row=0, column=0,
                               sticky = 'nsew')

        self.doubleClickLabel = ttk.Label(self.tourneyPanel,
                  text='Double Click Date for Tourney')
        self.doubleClickLabel.grid(row=0, column=0)


        self.existingTourneysLabel = ttk.Label(self.tourneyPanel,
                                          text = 'Existing Tourneys:   ')
        self.existingTourneysLabel.grid(row=1, column=0, sticky = 'n')
        self.existingTourneys = tk.Listbox(self.tourneyPanel,
                                       listvariable=self.existingTourneyValues)
        
        self.existingTourneys.grid(row=1, column=1,
                                   sticky='nsew')
        self.populateExistingTourneys()

        #
        # have to bind event to listbox as there is no command option
        #
        self.existingTourneys.bind('<Double-Button-1>',self.selectedTourney)
        
        #
        # Build Players selection
        #
        self.playerPanel = ttk.LabelFrame(self,
                                          relief='sunken',
                                          height='10c',
                                          width = '10c',
                                          padding='10p',
                                          text='Assign Players'
                                          )
        self.playerPanel.grid(row=0, column=0,
                              sticky='nsew')
        # hide players for now until Tourney has been selected
        self.playerPanel.grid_remove()
        

        #
        # player panel row 1
        #
        ttk.Label(self.playerPanel,
                  text='Check players then press Seating button').grid(row=1, column=0)
        self.populatePlayers()      # retrieve players and build check box selection list
        
        self.assign_button = ttk.Button(self.playerPanel,
                                   text='Seating',
                                   command=self.assignPlayerstoTourney
                                   )
        self.assign_button.grid()
        self.cancel_button = ttk.Button(self.playerPanel,
                                   text='Go Back',
                                   command=self.goBack)
        self.cancel_button.grid()
        
    #************************************************************
    #   populate tourneys list from database
    #
    def tabChange(self,event):
        self.populateExistingTourneys()

    #************************************************************
    #   populate tourneys list from database
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
      
        self.tourneyLabel = ttk.Label(cfg.screenDict['club'],
                                      text='Tourney Date: ')
        self.tourneyLabel.grid(row=1, column=0)

        self.dateOfTourney = ttk.Label(cfg.screenDict['club'])
        self.dateOfTourney.grid(row=1, column=1)
        
        cfg.tourneyRecordId = self.getTourneyId(self.tourneyDate.get())
        self.dateOfTourney.config(text=self.tourneyDate.get())

        # now swap panels
        self.tourneyPanel.grid_remove()
        self.playerPanel.grid()
        
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
        cfg.list_of_zeros = [0 for x in all_players]
        player_name_tuples = zip(player_name_list,
                                 cfg.list_of_zeros)
        list_of_player_name_tuples = [list(y) for y in player_name_tuples]
        name_zero_list = zip(player_id_list,
                             list_of_player_name_tuples)
        cfg.player_dict = {key:value for key, value in name_zero_list}
        print (cfg.player_dict)
        for player_id in cfg.player_dict:
            cfg.player_dict[player_id][1] = tk.Variable()
            cb = ttk.Checkbutton(self.playerPanel,
                                 text=cfg.player_dict[player_id][0],
                                 variable=cfg.player_dict[player_id][1])
            cb.grid(sticky='w')
        print ('Setup of checkbuttons done...')
    #************************************************************
    #
    def assignPlayerstoTourney(self):
        # parse slections and build in-memory tourney structure
        print ('Assign players to tourney')
        cfg.s_p_ids =[]
        cfg.s_p_names = []
##        print(self.player_dict)
        for player in cfg.player_dict:
            if cfg.player_dict[player][1].get() == '1':
                cfg.s_p_ids.append(player)
                cfg.s_p_names.append(cfg.player_dict[player][0])
        print (cfg.s_p_ids)
        print (cfg.s_p_names)
        cfg.screenDict['notebook'].select(3)

    #************************************************************
    #
    def goBack(self):
        # null out the check box selections
        for player in cfg.player_dict:
            cfg.player_dict[player][1].set(0)
        self.playerPanel.grid_remove()
        self.tourneyPanel.grid()
                                   
                                   
                                   
