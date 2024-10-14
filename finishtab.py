# finishtab.py
# 7/21/2020 updated to cribbageconfig
#
#####################################################################
#
#   Creates tab screen for cleaning up prior to exit
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
import cribbageconfig as cfg

class FinishTab (ttk.Frame):
    # screen class is always a frame

    #************************************************************   
    #   
    #   sets up tab for finish and cleanup

    def __init__ (self, tabTarget, parent=None):
        ttk.Frame.__init__(self, parent)
        self.grid()

        # build out tab and register with notebook
        self.config(padding = '10p')
        tabTarget.add(self, text='Finish')

        cfg.screenDict['ftab'] = self
    def tabChange(self, event):
        #
        # do nothing for now
        #
        pass