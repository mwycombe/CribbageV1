# cribbagestartup.py
# 7/21/2020 cloned from peggersstartup.py
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
from tkinter.messagebox import askokcancel

from sqlobject import *

# Personal imports
import cribbageconfig as cfg
from player import Player
from club import Club
from tourney import Tourney
from accessPlayers import AccessPlayers
from accessTourneys import AccessTourneys
from accessResults import AccessResults
from accessClubs import AccessClubs


class CribbageStartup ():
   
    # define class method so initDbms can be called without
    # instantiating an instance
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
        cfg.reportDirectory = ''
        try:
            dbmsCfg = open('Cribbage.cfg')      # this is the master config file
        except FileNotFoundError:
            print ('Unable to locate Cribbage.cfg\n Terminating')
            sys.exit(-1)
        print ('Config file found')
        # iterate through the cfg file and strip out the values for each name in <name> = <value>
        for line in dbmsCfg:
            print (line)
            eName = line.split(sep='=')[0].strip()
            eValue = line.split(sep='=')[1].strip()
            # if eName == 'title':
            #     cfg.appTitle = eValue
            if eName == 'clubNumber':
                cfg.clubNumber = int(eValue)
            elif eName == 'dbmsDirectory':
                cfg.dbmsDirectory = eValue
            elif eName == 'dbms':
                cfg.dbmsName = eValue
            elif eName == 'season':
                cfg.season = eValue
            elif eName == 'reportDirectory':
                cfg.reportDirectory = eValue
        # and go to where the data base is located - ?? why??
##        os.chdir(cfg.dbmsDirectory)
        # close out the config file
        dbmsCfg.close()

        # this is good to continue for debugging for future seasons
        print ('Current directory: ' + cfg.dbmsDirectory)
        # print ('appTitle:= ' + cfg.appTitle)
        print ('dbmsDirectory:= ' + cfg.dbmsDirectory)
        print ('dbmsName:= ' + cfg.dbmsName)
        print ('season:= ' + cfg.season)
        print ('clubNumber:= ' + str(cfg.clubNumber))

        if not mbx.askokcancel('Using Data Base',cfg.dbmsDirectory + cfg.dbmsName):
            sys.exit('Wrong data base in use')
        # see if we can connect to the database
        try:
            # validate where we are trying to connect to the database
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
            sys._exit(-1)


        # global reference variables

        cfg.ap = AccessPlayers()
        cfg.ar = AccessResults()
        cfg.at = AccessTourneys()
        cfg.ac = AccessClubs()

        cfg.clubRecord = cfg.ac.clubByNumber(cfg.clubNumber)[0]      # returns one club record in a list
        print (type(cfg.clubRecord))
        cfg.clubId = cfg.clubRecord.id
        cfg.clubName = cfg.clubRecord.clubName
        cfg.clubLocation = cfg.clubRecord.location
        # this is now set from the reportDirectory = entry in cribbage.cfg
        # cfg.reportDirectory = cfg.clubRecord.reportDirectory
        print(cfg.reportDirectory)

        cfg.clubCount = cfg.ap.countPlayers(cfg.clubRecord)
        # PeggersStartup.createPlayersXref()
        # PeggersStartup.createClubXref()
        # we may need to also count players for 21
    @classmethod
    def createPlayersXref(cls):
        # cross-refs used to build results screens
        cfg.playerXref = {p.id: p.LastName + ', ' + p.FirstName for p in list(Player.select())}
        for p in cfg.playerXref.items():
            print ('playerXref:', p)
        cfg.playerRefx = {v: k for k, v in cfg.playerXref.items()}
    @classmethod
    def createClubXref(cls):
        cfg.clubXref = {x[0]: x[1] for x in cfg.ac.clubXref()}
    @classmethod
    def createTourneyXref(cls):
        #  {tid: tno}
        cfg.tourneyXref = {x.id : x.TourneyNumber for x in cfg.at.allTourneysForClubBySeason(cfg.clubRecord, cfg.season)}
        print ('tourneyXref: ', cfg.tourneyXref)
        # {tno : tid}
        cfg.tourneyRefx = { v:k for k, v in cfg.tourneyXref.items() }
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
 
