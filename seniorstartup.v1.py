#peeggerstartup.py
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


class PeggersStartup ():
   
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

        # see if we can connect to the database
        try:
            print('In try block')
            print('Connecting to: ' + cfg.dbmsDirectory + cfg.dbmsName)
            connection_string = 'sqlite:' + cfg.dbmsDirectory + cfg.dbmsName
            print ('connection_string:= ' + connection_string)
            conn = connectionForURI(connection_string)
            sqlhub.processConnection = conn     # make available to all classses
            # none of these widgets yet exist so promote the
            # action to the higher level
        except:
            print ('Unable to locate data base - terminating')
            os._exit(-1)

    
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
 
