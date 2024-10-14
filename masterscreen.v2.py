# masterscreen.v2.py
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

class MasterScreen (ttk.LabelFrame):
    # screen class is always a frame

    # control variables
    
    #************************************************************   
    #   
    #   sets up containers - parent is root

    def __init__ (self, parent=None):
        super().__init__( parent)
        self.grid(row = 0, column = 0)
        self.text = 'Master'
        print('MasterScreen started . . .')
        
        # register master screen
        cfg.screenDict['master'] = self


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
##                                       borderwidth='10p',
##                                       relief = 'sunken')
##        self.headerPanel.grid(row=0, column=0, sticky='n')
##
##        # self register
##        print ('Register header')
##        cfg.screenDict['header'] = self.headerPanel
        self.sessionHeader = ttk.LabelFrame(self,
                                            height = '3c',
                                            width = '10c',
                                            borderwidth = '5p',
                                            relief = 'sunken',
                                            text = 'Session'
                                            )
        self.sessionHeader.grid(row = 0, column = 0)

        # register both header subpanels
        cfg.screenDict['session'] = self.sessionHeader

        self.clubPanel = ttk.LabelFrame (self.sessionHeader,
                                         height='3c',
                                         width ='10c',
                                         borderwidth='10p',
                                         relief = 'sunken',
                                         text = 'Club')
        self.clubPanel.grid(row=0, column=0,
                            sticky = 'nsew')
        # register club panel
        cfg.screenDict['club'] = self.clubPanel

        self.actionPanel = ttk.LabelFrame(self.sessionHeader,
                                            height = '3c',
                                            width = '10c',
                                            borderwidth = '5p',
                                            relief = 'sunken',
                                            text = 'Action'
                                            )
        self.actionPanel.grid(row = 0, column = 1,
                              stick = 'nsew')

        # register action panel
        cfg.screenDict['action'] = self.actionPanel
        #
        # the action panel is a 'scratch' area that notebook tabs can post
        # specific local information for that tab.


        self.clubNumber = ttk.Label(self.clubPanel,
                                    text='Club No.:    ',
                                    relief='sunken',
                                    borderwidth='10p')
        self.clubNumber.grid(row=0, column=0, sticky='w')

        self.clubNumberLabel = ttk.Label(self.clubPanel,
                                         text=cfg.clubNumber,
                                         relief='sunken',
                                         borderwidth='2c',
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
