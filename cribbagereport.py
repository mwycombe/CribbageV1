# cribbagereport.py
# 7/21/2020 cloned from peggersreport.py
# 2/20/2020
# Separate globals for reporting function
# Cannot use peggersconfig in case we flip back to other tabs
# while having gone to the report tab.
# Have to leave cfg config intact for the return

# System imports
from sqlobject import *
import tkinter as tk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdb

import sys
import os

# Personal imports
from club import Club
from tourney import Tourney
from player import Player
from scorecard import ScoreCard

# these are dynamic globals between report modules
reportSeason = ' '      # filled in for the season being reported on; used by reports.
tourneyDate = ''
tourneyNumber = 0       # must be an integer
tourneyRecordId = 0     # must be an integer
tourneyRecord = ''      # used to keep a copy of the tourney sqlobject record during scoring
# reportData = ''         # here's where the report line data gets posted
reportLineNumber = ''   # used to control line spacing
# quarterEntryTotal = ''  # used for both quarterly reports - full and drop
regionalTourneyNumber = 41
nationalTourneyNumber = 42
# report run selections pushed into here
reportStack = {}        # format { 'reportname' : (rptIntVar, rptClassName) }