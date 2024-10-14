#playerstab.py
#
#####################################################################
#
#   Creates tab screen for handling players
#   Will self-register in notebook found in screenDict of cfg
#   Version 1.0 name was ManagePlayers.py
#
#####################################################################
# TODO: Implement F2 for player edit and F3 for new player
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
from player import Player

class PlayersTab (ttk.Frame):
    # screen class is always a frame


    #************************************************************   
    #   
    #   sets up tab for managing players & register with notebook frame

    def __init__ (self, parent=None):

        super().__init__(parent)
        self.grid()

        # control variables for new player form
        
        self.fname = tk.StringVar()
        self.lname = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.accno = tk.StringVar()
        self.homeClub = tk.IntVar()
        self.joined =tk.StringVar()

        # control variable for exsiting players
        self.players=tk.StringVar()


        # build out tab and register with notebook

        self.config(padding = '10p')
        parent.add(self,text='Players')
        
        # perform self-registration under notebook

        cfg.screenDict['ptab'] = self

        print('Register ptab')


        self.oldPlayerPanel = ttk.LabelFrame(self,
                                             height='10c',
                                             width = '5c',
                                             borderwidth='15p',
                                             relief = 'sunken',
                                             text='Existing Players'
                                             )
        self.oldPlayerPanel.grid(row=0, column=0, sticky='ew')

        self.noPlayers = ttk.Label(self.oldPlayerPanel,
                                   text='There are no existing players',
                                   relief = 'raised',
                                   borderwidth='1c'
                                   )

        self.selectPlayer = ttk.Label(self.oldPlayerPanel,
                                      text='Double click player to edit',
                                      borderwidth='1c'
                                      )
        self.selectPlayer.grid(row=0,
                               column=0,
                               sticky='ew')


        
        self.newPlayerPanel = ttk.LabelFrame(self,
                                             height='10c',
                                             width = '5c',
                                             borderwidth='5p',
                                             relief = 'sunken',
                                             text = 'New Player'
                                             )
        self.newPlayerPanel.grid(row=0, column=2, sticky='ns')

        self.newPlayerForm(self.newPlayerPanel)

        self.displayExistingPlayers()

    #************************************************************
    #   build a display of existing players on file
    #
    def displayExistingPlayers(self):
        # list out existing players
        if Player.select().count() == 0:

            self.noPlayers.grid(row = 0,
                             column = 0,
                             sticky='ewns')
            self.selectPlayer.grid_remove()
        else:
#            print('Get and print players')
#           remove any No Players message
            self.hideWidget(self.noPlayers)
            self.showWidget(self.selectPlayer)
            
            self.existingPlayers = list(Player.select().orderBy('FirstName'))
##            print (self.existingPlayers)
            self.playersInDbms = []
#            print (self.existingPlayers[0].FirstName)
            for p in self.existingPlayers:
                self.playersInDbms.append(p.FirstName + ' ' +p.LastName)
            # build listbox
            self.players.set(self.playersInDbms)
            self.exp = tk.Listbox(self.oldPlayerPanel,
                                  listvariable=self.players,
                                  )
            self.exp.grid(row = 1, column = 0)
            
            self.scrollbar = ttk.Scrollbar(self.oldPlayerPanel)
            self.scrollbar.grid(row=1, column=1, stick ='ns')
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
                print(str(cfg.clubId))
                      
                self.player = Player(FirstName  =   self.fname.get(),
                                     LastName   =   self.lname.get(),
                                     Phone      =   self.phone.get(),
                                     Email      =   self.email.get(),
                                     ACCNumber  =   self.accno.get(),
                                     Joined     =   self.joined.get(),
                                     Club       =   cfg.clubId
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
    #   build new player form inside newPlayerPanel
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
        self.editPlayerPanel.grid(row = 0, column = 2,sticky='ns'
                                                             ''
                                                             '')
        self.editPlayerForm(self.editPlayerPanel)
   
    #************************************************************
    #
    def editPlayerForm(self, parent):
        print ('Build edit player widgets')
        self.buildPlayerForm(parent)
        
        self.fname.set(self.existingPlayers[self.ListBoxIndex[0]].FirstName)
        self.lname.set(self.existingPlayers[self.ListBoxIndex[0]].LastName)
        self.joined.set(self.existingPlayers[self.ListBoxIndex[0]].Joined)
        
        ttk.Button(parent,text='Edit',command=self.editAPlayer).grid(row=6,column=0)
        ttk.Button(parent,text='Delete',command=self.deleteAPlayer).grid(row=6,column=1)
        ttk.Button(parent,text='Cancel',command=self.cancelPlayerEdit).grid(row=6,column=2)

    #************************************************************
    #
    def cancelPlayerEdit (self):
        # restore new Player panel
        print ('back to players panel')
        self.editPlayerPanel.grid_remove()
        self.newPlayerPanel.grid()
        self.resetForm()
        self.displayExistingPlayers()

    #************************************************************
    #
    def deleteAPlayer(self):
        deletePlayer = Player.select(Player.q.FirstName == (self.existingPlayers[self.ListBoxIndex[0]].FirstName))[0]
        deletePlayer.delete(deletePlayer.id)
        self.cancelPlayerEdit()
                                
    #************************************************************
    #
    def editSelectedPlayer(self,event):
        print ('Edit selected player from listbox')
        #
        # replace NewPlayer panel with EditPlayer panel
        #
        self.ListBoxIndex = self.exp.curselection()
        print ('ListBoxIndex: ', self.ListBoxIndex)
        self.editEntry = self.exp.get(self.ListBoxIndex)
        print (self.editEntry)
        self.setUpEditPlayerPanel()

        
    #************************************************************
    #
    def editAPlayer (self):
        print ('Replace player entry')
        changePlayer = Player.select(Player.q.FirstName == (self.existingPlayers[self.ListBoxIndex[0]].FirstName))[0]
        changePlayer.FirstName = self.fname.get()
        changePlayer.LastName  = self.lname.get()
        changePlayer.Joined    = self.joined.get()
        self.cancelPlayerEdit()
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
        return (retryPlayerEntry)

    #************************************************************
    #
    def duplicateName(self):
        # just leave things alone for now so user can overtype
        # maybe just pop a std dialog asking try again or

        
        retryPlayerEntry = mbx.askretrycancel('Duplicate Name',
                           'Retry Input or Quit?',
                           parent = self.newPlayerPanel)
        return (retryPlayerEntry)

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




    
