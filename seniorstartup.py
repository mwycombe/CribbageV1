#seniorstartup.py
#
#####################################################
#                                                   #
#   Locates/confirms database                       #
#   User can select new location, use existing      #
#   dbms location.                                  #
#                                                   #
#####################################################

# System imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg
import sys as sys
import os as os
from sqlobject import *

# Personal imports
import seniorsconfig as cfg
from player import Player
from club import Club


class CribbageStartup ():
   
    # define class method so initDbms can be called without
    # instatiating an instance
    @classmethod
    def initDbms(cls):
        
        # search baseDir for a sqlite3 file - i.e. a dbms
        # make sure we are positioned at the appropriate directory
        # everyone that needs dmbs initialization calls here
        #
        print('initDbms')
        
        cfg.appTitle = ''
        cfg.dbmsDirectory = ''
        cfg.dbmsName = ''
        cfg.season = ''
        try:
            dbmsCfg = open('Seniors.cfg')      # this is the master config file
        except FileNotFoundError:
            print ('Unable to locate Seniors.cfg\n Terminating')
            sys.exit(-1)
        print ('Config file found')
        for line in dbmsCfg:
            print (line)
            eName = line.split(sep='=')[0].strip()
            eValue = line.split(sep='=')[1].strip()
            if eName == 'title':
                cfg.appTitle = eValue
            elif eName == 'directory':
                cfg.dbmsDirectory = eValue
            elif eName == 'dbms':
                cfg.dbmsName = eValue
            elif eName == 'season':
                cfg.season = eValue
        # and go to where the data base is located
##        os.chdir(cfg.dbmsDirectory)

        print ('Current directory: ' + cfg.dbmsDirectory)
        print ('appTitle:= ' + cfg.appTitle)
        print ('dbmsDirectory:= ' + cfg.dbmsDirectory)
        print ('dbmsName:= ' + cfg.dbmsName)
        print ('season:= ' + cfg.season)

        # conversion to access modules 12/10/2019
        # create the Club SQLObject in the cfg base

        # see if we can connect to the database
        try:
            print('In try block')
            print('Connecting to: ' + cfg.dbmsDirectory + cfg.dbmsName)
            connection_string = 'sqlite:' + cfg.dbmsDirectory + cfg.dbmsName
            print ('connection_string:= ' + connection_string)
            conn = connectionForURI(connection_string)
            sqlhub.processConnection = conn     # make available to all classses
            # get the count of club membership
            # none of these widgets yet exist so promote the
            # action to the higher level
        except:
            print ('Unable to locate data base - terminating')
            os._exit(-1)

        # control variables
        cfg.clubName = Club.get(1).clubName
        cfg.clubNumber = Club.get(1).clubNumber
        cfg.clubId = Club.get(1).id
        cfg.clubCount = Player.select().count()
        # and add a Club SQLobject
        cfg.ClubObject = Club.get(1)
        # this is picked up from the Seniors.cfg file in the seniors startup directory
        # cfg.season = '2019-20'

        #************************************************************
    #   call startup for command line start

    def __init__(parent, title):
        print('In startup .... screenDict:=',cfg.screenDict)
        if 'root' not in cfg.screenDict:
            root = tk.Tk()
            cfg.screenDict['root'] = root
        CribbageStartup.initDbms()
        root.mainloop()
    
        
if __name__ == '__main__':
    CribbageStartup.initDbms()
 
