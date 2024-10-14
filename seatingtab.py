#seatingtab.py
### Obsolete 1/24/2020
# Seating is not relevant for tourney summary results, only for manual checking
#
#####################################################################
#
#   Creates tab screen for assigning players to seats in a tourney
#   Will self-register in notebook found in screenDict of cfg
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
from player import Player
from memplayer import MemPlayer
from memscorecard import MemScoreCard

class SeatingTab (ttk.Frame):
    # screen class is always a frame


    seatingError = False    # used to control recycling of seating assignments

    
    #************************************************************   
    #   
    #   sets up tab for aassigning seats to players in a Tourney

    def __init__ (self, parent=None):
        super().__init__( parent)
        self.grid()

    # build out tab and register with notebook
        self.config(padding = '10p')
        parent.add(self,text='Seating')
        cfg.screenDict['stab'] = self

        print('register stab')

        self.seatLabel = ttk.Label(self,
                  text='Assign unique seat number and press Assign Button')
        self.seatLabel.grid(row=0, column=0, columnspan=4)

        # must call .getSeatingAssignments() after tourneyplayer 
        # players have been selected
        # look for event for this tab receiving focus
        ## self.getSeatingAssignments()

        # do this when first loaded so we can always forget
        # then rebuild every time we enter on a tab change
        self.assignSeats = ttk.Button(self,
                              text='Assign',
                              command=self.readSeatAssignments)
        self.assignSeats.grid(row=0, column=1)

##        cfg.screenDict['notebook'].bind('<<NotebookTabChanged>>',self.tabChange)
##        self.bind('<FocusIn>',self.tabChange)

        
    #************************************************************
    #   check to see if our tab was selected.
    #
    def tabChange(self,event):
        # populate the tab whenever we get selected
        # logic issue: if user leaves screen then comes back, all the
        # entries will be erased - screen has no memory of last use
##        print ('Seating tab event captured')
##        if cfg.screenDict['notebook'].index(cfg.screenDict['notebook'].select()) == 3:
        print('**SeatingTab got the notebook changed event***')          
        self.getSeatingAssignments()
        
    #************************************************************
    #
    #
    def getSeatingAssignments(self):
        
        # build the structure ready for seat assignments
        ## selected_tuples = zip(self.s_p_names,self.list_of_zeros)
        print (cfg.s_p_names)
        list_of_selected_tuples = [list(y) for y in zip(cfg.s_p_names,
                                                        cfg.list_of_zeros)]
        print (list_of_selected_tuples)
        cfg.seatingDict = {key: value for key, value in zip(cfg.s_p_ids,list_of_selected_tuples)}
        print (cfg.seatingDict)
        for x in cfg.seatingDict:
            cfg.seatingDict[x][1] = tk.IntVar()
            cfg.seatingDups[x] = tk.StringVar()
            cfg.seatingDups[x].set(' ')
        print ('seatingDict: ')
        print (cfg.seatingDict)

        ttk.Label(self,text='Player Name|').grid(row=1,
                                                column=0,
                                                sticky='e')
        ttk.Label(self,text='Seat Number').grid(row=1,
                                                column=1,
                                                sticky='w')

        n = 3
        for k in cfg.seatingDict:
            ttk.Label(self,text=cfg.seatingDict[k][0]).grid(row=n, column=0,
                      sticky='e')
            ttk.Entry(self,
                      textvariable=cfg.seatingDict[k][1],
                      width=5).grid(row=n,
                                    column=1,
                                    sticky='w')
            ttk.Label(self,
                      textvariable=cfg.seatingDups[k]
                      ).grid(row=n, column=2, sticky='w')
            n += 1

        self.assignSeats.grid_forget()  # erase any prior version
        self.assignSeats = ttk.Button(self,
                                      text='Assign',
                                      command=self.readSeatAssignments)
        self.assignSeats.grid(row=n, column=1)
        self.seatErrorLabel = ttk.Label(self,
                                        text='There were duplicate seats')
        self.seatErrorLabel.grid(row=3, column=4, sticky = 'nw')
        self.seatErrorInstructions = ttk.Label(self,
                                               text='Asterisks show errors')
        self.seatErrorInstructions.grid(row=4, column=4, stick= 'nw')        
        self.seatErrorCorrections = ttk.Label(self,
                                              text='Make corrects, press Correct Seats')
        self.seatErrorCorrections.grid(row=5, column=4, sticky = 'nw')
        self.seatErrorButton = ttk.Button(self,
                                          text='Correct seats',
                                          command=self.correctSeats)
        self.seatErrorButton.grid(row=6, column=4, sticky='nw')
        self.seatErrorLabel.grid_remove()
        self.seatErrorInstructions.grid_remove()
        self.seatErrorCorrections.grid_remove()
        self.seatErrorButton.grid_remove()
      
    #************************************************************
    #
    #
    def readSeatAssignments(self):
        self.seatingError = False
        for k in cfg.seatingDict:
            cfg.seatAssignments[k]=cfg.seatingDict[k][1].get()
        print ('cfg.seatAssignments')
        print(cfg.seatAssignments)
        
        if self.validateSeatAssignments():
             # tell user to retry
             self.seatErrorLabel.grid()
             self.seatErrorInstructions.grid()
             self.seatErrorCorrections.grid()
             self.seatErrorButton.grid()
             return
        self.buildTourneyInMemory()
        cfg.screenDict['notebook'].select(4)

    #************************************************************
    #   Handle user pressing error button
    #
    def correctSeats (self):
        # just let user key in correct seats, kill error msg, and re-read
        self.seatErrorLabel.grid_remove()
        self.seatErrorInstructions.grid_remove()
        self.seatErrorCorrections.grid_remove()
        self.seatErrorButton.grid_remove()
        # remove the asterisks
        for x in cfg.seatAssignments:
            cfg.seatingDups[x].set(' ')

        self.readSeatAssignments()

        
    #************************************************************
    #   Make sure there are no duplicate seat assignments
    #
    def validateSeatAssignments (self):
        # go through and makes sure every seat number is unique
        print('***\nValidate seats')
##        invertedSeats = {v:k for (k,v) in cfg.seatAssignments.items()}
##        print ('inverted seats')
##        print (invertedSeats)
        testSeats = {}
        for k in cfg.seatAssignments:
            print ('k:= ', k, ' v:= ', cfg.seatAssignments[k])
            if cfg.seatAssignments[k] in testSeats:
                print('Found duplicate seat')
                print ('testSeats: ',testSeats)
                self.seatingError = True
                self.showDuplicateSeats(k)
            else:
                testSeats[cfg.seatAssignments[k]] = k
                cfg.seatingDups[k].set(' ')
        print ('testSeats')
        print (testSeats)

        if not self.seatingError:
            # if we drop through then all seats were found to be unique
            #
            # re-key seat assignment by seat
            # only do this after ensuring seat numbers are unique
            #
            cfg.seatsBySeat = {}
            for k in cfg.seatAssignments:
                cfg.seatsBySeat[cfg.seatAssignments[k]] = k
                
        return self.seatingError
                
    #************************************************************
    #   Show duplicate seat error and await correctoin
    #
    def showDuplicateSeats(self,seat):
        # insert the asterisk
        print('Show duplicate seats')
        self.seatingError = True
        cfg.seatingDups[seat].set('***')
        
    #************************************************************
    #
    def buildTourneyInMemory(self):
        print('Build Tourney')
        cfg.s_p_id_names = {key:value for key, value in zip(cfg.s_p_ids,
                                                       cfg.s_p_names)}
        for k in cfg.s_p_id_names:
            cfg.playersInTourney[k] = MemPlayer(k,
                                            cfg.s_p_id_names[k])

        for k in cfg.seatAssignments:
            cfg.tourneyScoreCards[k] = MemScoreCard(cfg.tourneyRecordId,
                                                k,
                                                cfg.seatAssignments[k])
