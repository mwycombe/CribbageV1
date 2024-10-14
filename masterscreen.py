# masterscreen.py
# 7/20/2020 cloned from masterscreen.v2.ppy
#
#####################################################################
#
#   Creates root for the application and sets up empty notebook
#   ready for tabs to register themselves
#
#####################################################################
#
#   builds base frames in the root
#   header frame carries all cross-tab static fiels some of which
#   get populated from tab actions
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
from club import Club
from player import Player
from columnweights import ColumnWeights

class MasterScreen (tk.LabelFrame):
    # screen class is always a frame

    @classmethod
    def wipeActivityPanel(cls):
        # any tab can call this to grid_remove all children that share the activity panel
        for panel in cfg.screenDict['activity'].winfo_children():
            panel.grid_remove()
    

    def __init__ (self, parent=None):
        super().__init__( parent)
        self['text'] = 'Master'
        self['relief'] = tk.RAISED
        self.grid(row = 0, column = 0, sticky = 'nsew')
        # self.text = 'Master'
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


        print('MasterScreen started . . .')
        
        # register master screen
        cfg.screenDict['master'] = self

        # make the columns stretchable
    # # control variables
    #   These are initialized in peggersstartup.py
    #
    #     cfg.clubName = Club.get(1).clubName
    #     cfg.clubNumber = Club.get(1).clubNumber
    #     cfg.clubId = Club.get(1).id
    #     cfg.clubCount = Player.select().count()

##        self.headerPanel = ttk.Frame (self,
##                                       height='3c',
##                                       width ='10c',
##                                       borderwidth='10',
##                                       relief = 'sunken')
##        self.headerPanel.grid(row=0, column=0, sticky='n')
##
##        # self register
##        print ('Register header')
##        cfg.screenDict['header'] = self.headerPanel
        self.sessionHeader = tk.LabelFrame(self,
                                            # height = '3c',
                                            # width = '10c',
                                            relief = tk.RAISED,
                                            borderwidth = 5,
                                            text = 'Session'
                                            )
        # self.sessionHeader.columnconfigure(0, weight=1)
        # self.sessionHeader.columnconfigure(1, weight=1)
        self.sessionHeader.grid(row = 0, column = 0, sticky='ew')

        # register both header subpanels
        cfg.screenDict['session'] = self.sessionHeader

        self.clubPanel = tk.LabelFrame (self.sessionHeader,
                                         # height='3c',
                                         # width ='10c',
                                         borderwidth = 2,
                                         relief = tk.GROOVE,
                                         text = 'Club')
        # self.clubPanel.columnconfigure(0, weight=1)
        # self.clubPanel.rowconfigure(0,weight=1)
        self.clubPanel.grid(row=0, column=0,
                            sticky = 'nsew')
        # register club panel
        cfg.screenDict['club'] = self.clubPanel

        self.activityPanel = tk.LabelFrame(self.sessionHeader,
                                            # height = '3c',
                                            # width = '10c',
                                            borderwidth = 2,
                                            relief = tk.GROOVE,
                                            text = 'Activity'
                                            )
        # self.activityPanel.columnconfigure(0, weight=1)
        # self.activityPanel.rowconfigure(0, weight=1)
        self.activityPanel.grid(row = 0, column = 1,
                              stick = 'nsew')

        # register action panel
        cfg.screenDict['activity'] = self.activityPanel
        #
        # the action panel is a 'scratch' area that notebook tabs can post
        # specific local information for that tab.

        # weight as many columns as there are children - after children are created
        ColumnWeights.columnWeights(self.sessionHeader,len(self.sessionHeader.winfo_children()))


        self.clubNumber = tk.Label(self.clubPanel,
                                    text='Club No.:    ',
                                    relief='sunken',
                                    borderwidth='2')
        self.clubNumber.grid(row=0, column=0, sticky='w')

        self.clubNumberLabel = tk.Label(self.clubPanel,
                                         text=cfg.clubNumber,
                                         relief='sunken',
                                         borderwidth='2',
                                         font=('Helvetica', '10', 'bold'),
                                         foreground='blue')
        self.clubNumberLabel.grid(row=0, column=1, sticky='w')
        self.clubLabel = ttk.Label (self.clubPanel,
                                    text = '    Name:  ',
                                    relief = 'sunken',
                                    borderwidth = '10p')
        self.clubLabel.grid(row=0, column=2, sticky='w')

        self.clubNameLabel = ttk.Label (self.clubPanel,
                                   text=cfg.clubName,
                                   relief = 'sunken',
                                   borderwidth='2c',
                                   font = ('Helvetica', '10', 'bold'),
                                   foreground='blue')
        self.clubNameLabel.grid(row=0, column=3, sticky='w')

        self.countLabel = ttk.Label(self.clubPanel,
                                    text='Players in Club   ',
                                    relief='sunken',
                                    borderwidth='10p')
        self.countLabel.grid(row=1, column=0, sticky='w')

        self.memberCount = ttk.Label(self.clubPanel,
                                     text=cfg.clubCount,
                                     relief='sunken',
                                     borderwidth='2c',
                                     font=('Helvetica', '10', 'bold'),
                                     foreground='blue')
        self.memberCount.grid(row=1, column=1, sticky='w')

        self.seasonLabel = ttk.Label(self.clubPanel,
                                     text='Season: ',
                                     relief='sunken',
                                     borderwidth='10p')
        self.seasonLabel.grid(row=1, column = 2, sticky='w')

        self.season = ttk.Label(self.clubPanel,
                                text=cfg.season,
                                relief = 'sunken',
                                borderwidth = '2c',
                                font = ('Helvetica', '10', 'bold'),
                                foreground = 'blue')
        self.season.grid(row=1, column = 3, sticky = 'w')




        # build the notebook in the lower frame tabPanel
    

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0,
                           sticky='news')

        # register notebook panel for tab builders to reference
        print('Register notebook')
        cfg.screenDict['notebook'] = self.notebook


        #
        # self.notebook.bind("<<NotebookTabChanged>>",self.tabchange)
        # set this from the module that cares to track tabchanges
        # tabs within this notebook will register themselves
if __name__ == '__main__':

    # fake set up global cfg module for all others to share just for standalone testing
    cfg.clubName = 'Century Peggers'
    cfg.clubId = 1
    cfg.clubNumber = 100
    tourneyDate = ''  # tourney selection will override this
    tourneyId = 0

    if 'root' not in cfg.screenDict:
        root = tk.Tk()
        cfg.screenDict['root'] = root
        print ('Testing masterscreen. . .')
        print ('screenDict ', cfg.screenDict)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.resizable(True, True)


    app = MasterScreen(root)
    app.mainloop()