#peggersconfig.py
##########################################################
#
#   This peggersconfig.py is used to hold globals
#   that are used across all modules and classes
#
#   Common set-up routines as housed here to be shared by all
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

# these value will be filled in by various modules progress
# a whole set of tabbed class modules will use this for inter-module comm.
#
# these are static globals across all modules
appTitle = ''
clubName = ''
clubLocation = ''
clubId = 0
clubNumber = ''
clubCount = ''      # #players in the club
clubRecord = ''     # the Club sqlobject for the club being processed
season = ''
dbmsDirectory = ''
dbmsName = ''

# These dbms access routines are initialized by
# peggers __init__ function
#
ap = ''     # AccessPlayers ojbect
at = ''     # AccessTourneys object
ar = ''     # AccessRsults object
ac = ''     # AccessClubs objct

# these are dynamic globals between factored modules

tourneyDate = ''
tourneyNumber = 0       # must be an integer
tourneyRecordId = 0     # must be an integer
tourneyRecord = ''      # used to keep a copy of the tourney sqlobject record during scoring

# tab and screen control
# any module/class that creates a tab or screen puts an entry in here
# any moduel that depends on a tab or screen checks here first before building
# the tkinter frame can be lodged here so dependents can retrieve it easiliy

screenDict = {}     # starts out empty - all screen creators self-register
                    # the key is the unique name of the screen
                    # the value is the top Frame for the screen or tab
                    # thus any module wishing to access the screen can
                    # do so using the ojbect saved in screenDict value

# playername for peggers = ('lastName' + ', ' + 'firstName')

playerXref = {}     # {id : playername}
playerRefx = {}     # {playernname : id}
clubXref = {}       # {id : clubnumber}
tourneyXref = {}    # {id : tournenumber}




if __name__ == '__main__':

##    CribbageStartup.initDbms()

    # set up global cfg module for all others to share
    
    clubName = 'Century Peggers'
    clubId = 1
    clubNumber = 100
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

 
 
