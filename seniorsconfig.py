#seniorsconfig.py
##########################################################
#
#   This seniorsconfig.py is used to hold globals
#   that are used across all modules and classes
#
#   Common set-up routines as housed here to be shared by all
#
##########################################################
#
# 12/10/2019 update
# Anything to do with seating and games is no longer required
#
##########################################################

# System imports
from sqlobject import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg

import sys
import os

# Personal imports
from club import Club
from tourney import Tourney
from player import Player
from scorecard import ScoreCard
# from game import Game
# game.py no longer being used
##from seniorstartup import CribbageStartup

# these value will be filled in by various modules progress
# a whole set of tabbed class modules will use this for inter-module comm.
#
# these are static globals across all modules
appTitle = ''
clubName = ''
clubId = 0
clubNumber = ''
clubRecord = ''
season = ''
dbmsDirectory = ''
dbmsName = ''
clubCount = ''      # #players in the club
ClubObject = ''     # the club sqlobject for the club being processed

# These dbma access routines are initialized by
# seniorcribbage __init__ function
ap = ''             # AccessPlayers object
at = ''             # AccessTourneys object
ar = ''             # AccessRetults object

#
# these are dynamic globals between factored modules

tourneyDate = ''
tourneyNumber = 0     # Must be an integer
tourneyRecordId = 0
tourneyRecord = ''      # Used to keep a copy of the tourney sqlobject for the tourney

# tab and screen control
# any module/class that creates a tab or screen puts an entry in here
# any moduel that depends on a tab or screen checks here first before building
# the tkinter frame can be lodged here so dependents can retrieve it easiliy

screenDict = {}     # starts out empty - all screen creators self-register
                    # the key is the unique name of the screen
                    # the value is the top Frame for the screen or tab
                    # thus any module wishing to access the screen can
                    # do so using the ojbect saved in screenDict value

#
#   These are the globals that track who is assigned to a tournament
#
playerXref = {}     # player names keyed by player id {id: name}
playerRefx = {}     # player ids keyed by player name {name: id}
player_dict = {}    # dictionary of all players by id

s_p_ids = []        # list of ids assigned to the selected tournament
                    # built by touryneyplayerstab
s_p_names = []      # list of names assigned to the selected tournament
                    # built by tourneyplayerstab
s_p_id_names = {}   # dict of ids vs names for the tourney
                    # built by seatingtab
list_of_zeros =[]
playersInTourney = {}   # selected players for tourney -> key playerId; val names
#
# This is managed using the in-memory ScoreCard sqlobjects.
# They can be sorted - if updated, the dbms is also updat
# dirtyScoreCards = {}    # entered but unvefirifed scorecards -> playerId in tourney
#                         # built by scoringtab
#                         # these must be memscorecards not arrays of games as
#                         # these cannot be copy because they contain tkinter variables
enteredScoreCards = {}  # games entered for a given tourney player - clean or dirty
                        # used for redisplay when user switches back to scoringtab
                        # ditto for dirtyscorecards comment above
tourneyScoreCards = {}  # dict of MemScoreCards objects for tourney -> key playerId
                        # scorecards have been internally verified
                        # built by scoringtab
# nothing to do with games required
# nineGames = {}          # scorecard's worth of games -> key gameNumber
#                         # build by scoringtab
#   remove all seating references
# seatingDict = {}        # seat assignment with array of Variables ->key playerId
#                         # values are (playerName, seatNumberVariable) tuples
#                         # built by seatngtab
# seatingDups = {}        # used to show dup seating errors -> key by playerId
#                         # parallels seatingDict - built by seatingtab
# seatAssignments = {}    # assigned which seat - read from screen -> key playerId
#                         # built by seatingtab
# seatsBySeat = {}        # seat assignments -> k:v seatNo:playsId
                        # built by seatingtab


#************************************************************
#   do __init__ if we are run from a script
#

if __name__ == '__main__':

##    CribbageStartup.initDbms()

    # set up global cfg module for all others to share
    
    clubName = 'Senior Center'
    clubId = 1
    clubNumber = 999
    tourneyDate = ''      # tourney selection will override this
    tourneyId = 0

    # decide if we need to build our own screen
    if 'startup' not in self.tabDict:
        
        root = tk.Tk()                      # base window frame
        self.tabDict['startup'] = root      # register the root frame
        
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        mp = TourneyPlayers(root)
        root.mainloop()

 
 
