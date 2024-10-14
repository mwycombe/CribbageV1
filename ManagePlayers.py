# ManagePlayers.py
##########################################################
#
# Manage existing players and add new players.
#
# This module will eventually be under the control of a tab
# For testing it's under a root window frame
###########################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg
from sqlobject import *
from Club import Club
from Player import Player
import sys
import os

class ManagePlayers (ttk.Frame):

    #
    # This class is itself a ttk Frame
    #

#************************************************************
#
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid()
        print ('ManagePlayers started . . .')

        # control variables for new player form
        self.fname = tk.StringVar()
        self.lname = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.accno = tk.StringVar()
        self.joined =tk.StringVar()
        self.players = tk.StringVar()
        
        
        self.clubPanel = ttk.LabelFrame (self,
                                    height='3c',
                                    width = '10c',
                                    borderwidth='5p',
                                    relief = 'sunken',
                                    text = 'Club')
        self.clubPanel.grid(row=0, column = 0,
                            sticky='nsew',columnspan = 2)

        ttk.Label(self.clubPanel,
                   text ='  Using Club Name =  ',
                   relief = 'sunken',
                   borderwidth = '2c'
                  ).grid(row = 0,column = 0,sticky = 'w')
        
        self.clubName = Club.get(1).ClubName
        self.clubNumber = Club.get(1).ClubNumber
                
        ttk.Label(self.clubPanel,
                  text = self.clubName,
                  relief = 'sunken',
                  borderwidth = '2c',
                  font = ('Helvetica','10','bold'),
                  foreground='blue',
                  ).grid (row = 0,column = 1,sticky = 'e')

        
        #
        # set up existing players panel
        #
    
        self.existingPlayerPanel = ttk.LabelFrame(self,
                                             height='10c',
                                             width = '5c',
                                             borderwidth='15p',
                                             relief = 'sunken',
                                             text = 'Existing Players'
                                             )
        self.existingPlayerPanel.grid(row = 1, column = 0)

        self.noPlayers = ttk.Label(self.existingPlayerPanel,
          text='There are no existing players',
          relief = 'raised',
          borderwidth='1c'
          )

        self.displayExistingPlayers()
            
        #
        # set up for submitting a new player
        #
        
       
        #
        # build the new player form inside the new player panel
        #

        self.setUpNewPlayerPanel()        
        self.newPlayerForm(self.newPlayerPanel)

        

        ttk.Button(self.clubPanel,
                   text = 'Add Player?',
                   command = self.addNewPlayer).grid(row=1, column=0)
       
        self.resetForm()
        
#************************************************************
#
    def displayExistingPlayers(self):
        # list out existing players
        if Player.select().count() == 0:

            self.noPlayers.grid(row = 0,
                             column = 0,
                             sticky='ewns')
        else:
#            print('Get and print players')
#           remove any No Players message
            self.noPlayers.grid_remove()
            
            self.existingPlayers = list(Player.select())
#            print (self.existingPlayers)
            self.playersInDbms = []
#            print (self.existingPlayers[0].FirstName)
            for p in self.existingPlayers:
                self.playersInDbms.append(p.FirstName + ' ' +p.LastName)
            # build listbox
            self.players.set(self.playersInDbms)
            self.exp = tk.Listbox(self.existingPlayerPanel,
                                  listvariable=self.players,
                                  )
            self.exp.grid(row = 0, column = 0)
            
            self.scrollbar = ttk.Scrollbar(self.existingPlayerPanel)
            self.scrollbar.grid(row=0, column=1, stick ='ns')
            self.exp.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.exp.yview)

            #
            # allow ListBox entry to respond to double click for editing
            #
            self.exp.bind('<Double-Button-1>',self.editSelectedPlayer)
#************************************************************
#
    def submitNewPlayer(self):
        print('Validate and add new player')
        
        #validate the required fields
        print ('len(fname): ' + str(len(self.fname.get())))
        print ('len(lname): ' + str(len(self.lname.get())))

        #
        # at a minimum must have first and last name
        #
        
        if len(self.fname.get()) < 1:
            self.redText(self.fnameLabel)
            self.showNewPlayerError()
        elif len(self.lname.get()) < 1:
            self.redText(self.lnameLabel)           
            self.showNewPlayerError()
        
        print (self.fname.get())
        print (self.lname.get())
        

        # try adding to the data base and catching any errors

        if self.checkForNameDup (self.fname.get(), self.lname.get()):
            self.redText(self.fnameLabel)
            self.redText(self.lnameLabel)
            self.duplicateName()
        else:
            try:
                print(self.fname.get())
                print(self.lname.get())
                print(self.phone.get())
                print(self.email.get())
                print(self.accno.get())
                print(self.joined.get())
                print(str(self.clubNumber))
                      
                self.player = Player(FirstName  =   self.fname.get(),
                                     LastName   =   self.lname.get(),
                                     Phone      =   self.phone.get(),
                                     Email      =   self.email.get(),
                                     ACCNumber  =   self.accno.get(),
                                     Joined     =   self.joined.get(),
                                     Club       =   self.clubNumber
                                     )
                self.displayExistingPlayers()
                self.resetForm()
            except dberrors.DuplicateEntryError:
               # this will only trigger for duplicate ACC nos in the future
                if self.duplicateACCno(): # true means retry
                    # leave the labels red 
                    self.fnameEntry.focus_set()
                else:
                    self.resetForm()
 
#************************************************************
#
    def setUpNewPlayerPanel (self):
        self.newPlayerPanel = ttk.LabelFrame(self,
                                        height='10c',
                                        width = '5c',
                                        borderwidth='15p',
                                        relief = 'sunken',
                                        text = 'New Player'
                                        )
        self.newPlayerPanel.grid(row = 1, column = 1)

#************************************************************
#
    def buildPlayerForm(self, parent):
        self.fnameLabel = ttk.Label(parent,text = 'First Name')
        self.fnameLabel.grid(row=0,column=0)
        self.lnameLabel = ttk.Label(parent,text = 'Last Name')
        self.lnameLabel.grid(row=1,column=0)
        self.phoneLabel = ttk.Label(parent,text = 'Phone')
        self.phoneLabel.grid(row=2, column=0)
        self.emailLabel = ttk.Label(parent,text = 'Email')
        self.emailLabel.grid(row=3, column=0)
        self.accnoLabel = ttk.Label(parent,text = 'ACC Number')
        self.accnoLabel.grid(row=4,column=0)
        self.joinedLabel = ttk.Label(parent,text = 'Joined')
        self.joinedLabel.grid(row=5,column=0)
        self.fnameEntry = ttk.Entry(parent,textvariable=self.fname)
        self.fnameEntry.grid(row=0,column=1)
        self.lnameEntry = ttk.Entry(parent,textvariable=self.lname)
        self.lnameEntry.grid(row=1,column=1)
        self.phoneEntry = ttk.Entry(parent,textvariable=self.phone)
        self.phoneEntry.grid(row=2,column=1)
        self.emailEntry = ttk.Entry(parent,textvariable=self.email)
        self.emailEntry.grid(row=3,column=1)
        self.accnoEntry = ttk.Entry(parent,textvariable=self.accno)
        self.accnoEntry.grid(row=4,column=1)
        self.joinedEntry = ttk.Entry(parent,textvariable=self.joined)
        self.joinedEntry.grid(row=5,column=1)
        
 
#************************************************************
#
    def newPlayerForm(self, parent):
        self.buildPlayerForm(parent)
        ttk.Button(parent,text='Submit',command=self.submitNewPlayer).grid(row=6,column=0)
        ttk.Button(parent,text='Cancel',command=self.cancelNewPlayer).grid(row=6,column=1)

#************************************************************
#
    def setUpEditPlayerPanel (self):
        self.newPlayerPanel.grid_remove()
        self.editPlayerPanel = ttk.LabelFrame(self,
                                        height='10c',
                                        width = '5c',
                                        borderwidth='15p',
                                        relief = 'sunken',
                                        text = 'Edit Player'
                                        )
        self.editPlayerPanel.grid(row = 1, column = 1)
        self.editPlayerForm(self.editPlayerPanel)

#************************************************************
#
    def editPlayerForm(self, parent):
        print ('Build edit player widgets')
        self.buildPlayerForm(parent)
        ttk.Button(parent,text='Edit',command=self.editAPlayer).grid(row=6,column=0)
        ttk.Button(parent,text='Cancel',command=self.cancelPlayerEdit).grid(row=6,column=1)
                                    
                                  
#************************************************************
#
    def editSelectedPlayer(self,event):
        print ('Edit selected player from listbox')
        #
        # replace NewPlayer panel with EditPlayer panel
        #
        self.ListBoxIndex = self.exp.curselection()
        self.editEntry = self.exp.get(self.ListBoxIndex)
        print (self.editEntry)
        self.setUpEditPlayerPanel()

#************************************************************
#
    def cancelPlayerEdit (self):
        # restore new Player panel
        print ('back to players panel')
        self.editPlayerPanel.grid_remove()
        self.newPlayerPanel.grid()
        
#************************************************************
#
    def editAPlayer (self):
        print ('Replace player entry')
        
#************************************************************
#
    def cancelNewPlayer(self):
        print('Cancel new player add')
        self.resetForm()
        
#************************************************************
#
    def showNewPlayerError (self):
        print ('New Player input error')
        return mbx.askretrycancel('Missing Name Input',
                                              'Retry Input or Quit?',
                                              parent = self.newPlayerPanel)
    
        # check for missing input
        # if self.fname == '':
#************************************************************
#
    def checkForNameDup(self, fname, lname):
        dupPlayerTest = Player.select(
            AND(Player.q.FirstName == fname,
                Player.q.LastName == lname))
        if len(list(dupPlayerTest)) > 0:
            return True
        else:
            return False
            
#************************************************************
#
    def duplicateACCno(self):
        # just leave things alone for now so user can overtype
        # maybe just pop a std dialog asking try again or

        
        retryPlayerEntry = mbx.askretrycancel('Duplicate ACC#',
                           'Retry Input or Quit?',
                           parent = self.newPlayerPanel)
        return retryPlayerEntry

#************************************************************
#
    def duplicateName(self):
        # just leave things alone for now so user can overtype
        # maybe just pop a std dialog asking try again or

        
        retryPlayerEntry = mbx.askretrycancel('Duplicate Name',
                           'Retry Input or Quit?',
                           parent = self.newPlayerPanel)
        return retryPlayerEntry

#************************************************************
#
    def resetForm(self):
        # blank out all form fields via text variables
        self.fname.set('')
        self.lname.set('')
        self.phone.set('')
        self.email.set('')
        self.accno.set('')
        self.joined.set('')
        self.blackText(self.fnameLabel)
        self.blackText(self.lnameLabel)
        self.fnameEntry.focus_set()
        self.blackText(self.fnameLabel)
        self.blackText(self.lnameLabel)
        
#************************************************************
#
    def addNewPlayer(self):
        self.resetForm()
        
        
#************************************************************
#
    def hideWidget(self, w):
        w.grid_remove()
#************************************************************
#
    def showWidget(self,w):
        w.grid()
#************************************************************
#
    def redText(self,w):
        w.config(foreground='red')
#************************************************************
#
    def blackText(self,w):
        w.config(foreground='black')

#************************************************************
#
if __name__ == '__main__':
    # search baseDir for a sqlite3 file - i.e. a dbms
    # make sure we are positioned at the appropriate directory
    #
    appTitle = ''
    dbmsDirectory = ''
    dbmsName = ''
    season = ''
    try:
        cfg = open('Seniors.cfg')      # this is the master config file
    except FileNotFoundError:
        print ('Unable to locate Seniors.cfg\n Terminating')
        sys.exit(-1)
    print ('Config file found')
    for line in cfg:
        print (line)
        eName = line.split(sep='=')[0].strip()
        eValue = line.split(sep='=')[1].strip()
        if eName == 'title':
            appTitle = eValue
        elif eName == 'directory':
            dbmsDirectory = eValue
        elif eName == 'dbms':
            dbmsName = eValue
        elif eName == 'season':
            season = eValue
    # and go to where the data base is located
    os.chdir(dbmsDirectory)

    print ('Current directory: ' + dbmsDirectory)
    print ('appTitle:= ' + appTitle)
    print ('dbmsDirectory:= ' + dbmsDirectory)
    print ('dbmsName:= ' + dbmsName)
    print ('season:= ' + season)

    # see if we can connect to the database
    try:
        print('Connecting to: ' + dbmsDirectory + dbmsName)
        connection_string = 'sqlite:' + dbmsDirectory + dbmsName
        conn = connectionForURI(connection_string)
        sqlhub.processConnection = conn     # make available to all classses
        # none of these widgets yet exist so promote the
        # action to the higher level
    except:
        print ('Unable to locate data base - terminating')
        os._exit(-1)
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    mp = ManagePlayers(root)
    root.mainloop()
