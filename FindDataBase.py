#FindDataBase.py
#############################################################
#                                                           #
# After checking the diretory from the cribbage.cfg this    #
# determine if there is a valid sqlite3 dbms in that        #
# and if not, will ask if you wish to create one.           #
#                                                           #
#############################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg
from sqlobject import *
from Club import Club
from Game import Game
from Player import Player
from ScoreCard import ScoreCard
from Tourney import Tourney
import sys
import os
import sqlite3
from sqlite3 import Error

class FindDataBase (tk.Frame):
    # this frame will be imported into CribbageStartUp
    # it provides the panel for locating the data base
    # in the directory selected by FindCribbageDir

    #############################################
    # these will eventually be pushed to global #
    # as every module and panel will need access#
    # to them once they have been filled in by  #
    # the initial set-up panels.                #
    #############################################

##    Make these instance variables because of
##    reference issues with definnition order
##    
##    appTitle = ''
##    dbmsDirectory = ''
##    dbmsName = ''
##    season = ''



#************************************************************
    def __init__ (self, parent=None):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.grid()
 
        # finding the dbms will initialize all of the instance variables
        # needed to build the panels and widgets
 
        self.dbmsPanel = ttk.LabelFrame(self,relief='raised',
                        text='Locate DBMS',
                        height = '3c', width = '12c',
                        border = '8m')
        self.dbmsPanel.grid_propagate(0)
        self.dbmsLocated = self.locateDBMS()
        # make the widgets
        self.makeDbmsPanelWidgets(self.dbmsPanel)
        if self.dbmsLocated:
            self.w00.grid_remove()
            self.w10.grid_remove()
            self.w11.grid_remove()
        else:
            self.w10.grid_remove()
            self.w20.grid_remove()        
        self.dbmsPanel.grid()

#************************************************************
    def makeDbmsPanelWidgets(self,parent):
        self.w00 = ttk.Label(parent,text='No Data Base found in ' + self.dbmsDirectory)
        self.w00.grid(row=0, column=0)
        self.w10 = ttk.Label(parent,text='Enter Data Base Name')
        self.w10.grid(row=1, column=0)
        self.w11 = ttk.Entry(parent)
        self.w11.grid(row=1, column=1)
        self.w20 = ttk.Label(parent,text='Using Data Base:= ' +
                             self.dbmsDirectory + self.dbmsName)
        self.w20.grid(row=2, column=0)

#************************************************************
    def locateDBMS(self):
        # search baseDir for a sqlite3 file - i.e. a dbms
        # make sure we are positioned at the appropriate directory
        # returns True is dbms is found; else returns False
        try:
            self.cfg = open('Seniors.cfg')      # this is the master config file
        except FileNotFoundError:
            print ('Unable to locate Seniors.cfg\n Terminating')
            sys.exit(-1)
        print ('Config file found')
        for line in self.cfg:
            print (line)
            eName = line.split(sep='=')[0].strip()
            eValue = line.split(sep='=')[1].strip()
            if eName == 'title':
                self.appTitle = eValue
            elif eName == 'directory':
                self.dbmsDirectory = eValue
            elif eName == 'dbms':
                self.dbmsName = eValue
            elif eName == 'season':
                self.season = eValue
        # and go to where the data base is located
        os.chdir(self.dbmsDirectory)

        # see if we can connect to the database
        try:
            print('Connecting to: ' + self.dbmsDirectory + self.dbmsName)
            self.connection_string = 'sqlite:' + self.dbmsDirectory + self.dbmsName
            self.conn = connectionForURI(self.connection_string)
            sqlhub.processConnection = conn     # make available to all classses
            # none of these widgets yet exist so promote the
            # action to the higher level
            
##            self.w00.grid_remove()
##            self.w10.grid_remove()
##            self.w11.grid_remove()
            return True
        except:
            # this has to happen outside this function as
            # widgets have not yet been created.
#            self.w20.grid_remove()
            
            print ('Unable to connect to ' + self.dbmsDirectory + self.dbmsName)
            self.makeNewDBMS = mbx.askyesno(title='DBMS Setup',
                                    message='Create New DBMS?',
                                    parent=self.parent)
            print (self.makeNewDBMS)
            if self.makeNewDBMS:     # No dbms, so create one
                # already positioned at correct 
                return self.createDBMS(self.dbmsName)
            else:
                mbx.showerror ('No Data Base Located','Application will stop',
                               parent = self.parent)
                sys.exit(-1)
            return False

#************************************************************
#   def createDBMS (self):
#        print('Will set up new DBMS')
    def createDBMS(self, dbmsName):
        print ('create new dbms')

        #***********************************************
        ## Uncomment any of these to empty and then
        ## recreate one of the tables should they
        ## become polluted or corrupted
        #***********************************************
        
        #************************************************
        #
        # CREATE THE ACTUAL DATABASE
        #
        # already positioned in the correct director
        try:
            conn = sqlite3.connect(dbmsName)
            print (sqlite3.version)
        except Error as e:
            print (e)
        finally:
            conn.close()

        #************************************************
        # Connect to the virgin database with sqlobject
        # so we can create the tables we need.
        self.conn = connectionForURI('sqlite:' + dbmsName)
        sqlhub.processConnection = self.conn
        

        #************************************************
        #
        # TABLE DROPS

        ##Club.dropTable(True)
        ##Game.dropTable(True)
        ##Player.dropTable(True)
        ##ScoreCard.dropTable(True)
        ##Tourney.dropTable(True)

        #************************************************
        #
        # TABLE CREATES

        Club.createTable(ifNotExists=True)
        Game.createTable(ifNotExists=True)
        Player.createTable(ifNotExists=True)
        ScoreCard.createTable(ifNotExists=True)
        Tourney.createTable(ifNotExists=True)

        #************************************************
        #
        # Set up the club record

        self.club = Club(Director = 'Michael Rogers',
                         Location = 'Moose Lodge, Napa',
                         Contact = '510.504.6905 mlr94549@yahoo.com',
                         ClubNumber = 100,
                         ClubName = 'Century Peggers'
                         )

        return True
                   
if __name__ == '__main__':
  fdb = FindDataBase()

    
