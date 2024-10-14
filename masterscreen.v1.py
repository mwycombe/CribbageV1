#masterscreen.py
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
import peggersconfig as cfg
from club import Club

class MasterScreen (ttk.Frame):
    # screen class is always a frame

    # control variables
    
    #************************************************************   
    #   
    #   sets up containers - parent is root

    def __init__ (self, parent=None):
        super().__init__( parent)
        self.grid()
        print('MasterScreen started . . .')
        
        # register master screen
        cfg.screenDict['master'] = self


    # control variables
 
        cfg.clubName = Club.get(1).clubName
        cfg.clubNumber = Club.get(1).clubNumber
        cfg.clubId = Club.get(1).id

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
        
        self.clubPanel = ttk.LabelFrame (self,
                                         height='3c',
                                         width ='10c',
                                         borderwidth='10p',
                                         relief = 'sunken',
                                         text = 'Club')
        self.clubPanel.grid(row=0, column=0,
                            sticky = 'nsew')

        # register club panel
        cfg.screenDict['club'] = self.clubPanel

        self.clubLabel = ttk.Label (self.clubPanel,
                                    text = 'Club Name:= ',
                                    relief = 'sunken',
                                    borderwidth = '10p')
        self.clubLabel.grid(row=0, column=0, sticky='w')

        self.clubNameLabel = ttk.Label (self.clubPanel,
                                   text=cfg.clubName,
                                   relief = 'sunken',
                                   borderwidth='2c',
                                   font = ('Helvetica', '10', 'bold'),
                                   foreground='blue')
        self.clubNameLabel.grid(row=0, column=1, sticky='w')
        self.clubNumber = ttk.Label (self.clubPanel,
                                     text = 'Club Number:= ',
                                     relief = 'sunken',
                                     borderwidth = '10p')
        self.clubNumber.grid(row=0, column = 2, sticky = 'e')

        self.clubNumberLabel = ttk.Label (self.clubPanel,
                                          text=cfg.clubNumber,
                                          relief = 'sunken',
                                          borderwidth='2c',
                                          font = ('Helvetica', '10', 'bold'),
                                          foreground='blue')
        self.clubNumberLabel.grid(row=0, column=3, sticky='e')

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
