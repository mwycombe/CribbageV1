# helptab.py
# 7/21/2020 updated to cribbageconfig
#
#####################################################################
#
#   Info for user
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
import cribbageconfig as cfg

class HelpTab (ttk.Frame):
    # screen class is always a frame

    #************************************************************   
    #   
    #   sets up tab for aassigning seats to players in a Tourney

    def __init__ (self, parent=None):
        ttk.Frame.__init__(self, parent)
        self.grid()

    # build out tab and register with notebook
        self.config(padding = '10p')
        parent.add(self,text='Help')
        cfg.screenDict['htab'] = self

        self.helpPanel = ttk.LabelFrame(self,
                                        text='Help Panel')
        self.helpPanel.grid(row=0, column=0,
                            sticky='nsew')
                                        

        self.helpText = tk.Text(self.helpPanel,height=20, width=85)
        self.vscrollBar= ttk.Scrollbar(self.helpPanel)
        self.helpText.grid(row=0, column=0, sticky='ew')
        self.vscrollBar.grid(row=0,column=1,sticky='ns')
        self.vscrollBar.config(command=self.helpText.yview)
        self.helpText.config(yscrollcommand=self.vscrollBar.set)
        self.hscrollBar= ttk.Scrollbar(self.helpPanel, orient=tk.HORIZONTAL )
        self.hscrollBar.grid(row=1, column=0, sticky='ew')
        self.hscrollBar.config(command=self.helpText.xview)
        self.helpText.config(xscrollcommand=self.hscrollBar.set)
        
        self.help = """Overview Help for SeniorCribbage
When the program starts up, it selects a club and club number from the database.
If there is more than one club, user will be asked to select which club to use.
Tabs and their usage:
Players:
        User can add/change/delete players for the club
        A player delete is a soft delete, marking the player inactive
        but leaving any prior results in place
Tourneys:
        User can add/change/delete tourneys, using their date
Playing:
        Pick which tourney to use, by date, then select which players are in
        this tournament.
        When finished, use Seating button to go assign seats for the selected
        players.
Seating:
        For each players, assign a unique seat number. The only constraint is
        there are no duplicates
Scoring:
        For each player, record the games from the paper scorecard.
Validate:
        Will cross-check the score cards and present any conflicts for
        resolution.
        When all is valid, user will see All Good button which advances to the
        Reports tab.
Reports:
        Presents user with selection of Reports to create and print on the
        default printer.
Finish:
        Cleans up all of the internal structures and ensures the database is
        updated with the results from this tourney.
        """
        self.helpText.insert(tk.END, self.help)

    def tabChange(self, event):
        #
        # do nothing for now
        #
        pass