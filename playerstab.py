# playerstab.py
# 7/21/2020 update to cribbageconfig
#
#####################################################################
#
#   Creates tab screen for handling players
#   Will self-register in notebook found in screenDict of cfg
#   Version 1.0 name was ManagePlayers.py
#
#####################################################################

# TODO: When a new player is added or change need to rebuild the xref tables in cfg -
#  use CribbageStartUp.createPlayersXref()
# TODO: When a new player is added, refresh the in-memory list of players
# TODO: Add new player confirms that add but does not clear the screen
# TODO: Edit player does not clear screen on F10 - have to use esc to quit edit
# TODO: Cannot escape from edit screen
# TODO: Provide option for hiding inactive players from list of players
# TODO: Allow players to be marked for inclusion in results
# TODO: Allow soft delete of especially deceased players and moved away.
# TODO: Support for selection by alpha string.
# System imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg

from sqlobject import *

import sys as sys
import os as os
import datetime
import dateparser

# Personal imports
import cribbageconfig as cfg
from club import Club
from player import Player
from masterscreen import MasterScreen

class PlayersTab (tk.Frame):
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
        self.street = tk.StringVar()
        self.city = tk.StringVar()
        self.zip = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.accno = tk.StringVar()
        self.expiration = tk.StringVar()
        self.joined = tk.StringVar()
        self.active =tk.IntVar()
        self.showAllPlayers = tk.IntVar()
        self.showAllPlayers.set(1)

        # control variable for existing players
        self.players=tk.StringVar()



        # build out tab and register with notebook

        self.config(padx = '2', pady = '2')
        parent.add(self,text='Players')
        
        # perform self-registration under notebook

        cfg.screenDict['ptab'] = self

        print('Register ptab')

        self.oldPlayerPanel = tk.LabelFrame(self,
                                             height='10c',
                                             width='5c',
                                             borderwidth='1c',
                                             relief='flat',
                                             text='Existing Players'
                                             )
        self.oldPlayerPanel.columnconfigure(3, weight = 1, uniform='a')
        self.oldPlayerPanel.rowconfigure(2,weight=1, uniform='a')
        self.oldPlayerPanel.grid(row=0, column=0)

        self.asteriskLabel = ttk.Label(self.oldPlayerPanel,
                                       text = "* = Active")
        self.asteriskLabel.grid(row=0, column=0, sticky='w')

        # choose what to show
        self.showAll = ttk.Checkbutton(self.oldPlayerPanel,
                                       text = 'Show All',
                                       on = 1,
                                       off = 0,
                                       command = self.displayExistingPlayers,
                                       variable=self.showAllPlayers)
        self.showAll.grid(row=0, column=1)
        # for testing
        self.showAllPlayers.set(1)
    #*****************************************************
    #       list box that shows players
    #
        self.exp = tk.Listbox(self.oldPlayerPanel,
                              listvariable=self.players,
                              height=20
                              )
        self.exp.grid(row=1, column=0, columnspan=2)

        self.scrollbar = tk.Scrollbar(self.oldPlayerPanel)
        self.scrollbar.grid(row=1, column=2, sticky='ns')
        self.exp.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.exp.yview)

        #
        # allow ListBox entry to respond to double click for editing
        #
        # TODO: F2 will edit player, F3 to create new player, F9 to delete player

        # # [binding section]
        # Do this binding everytime we recreate the listbox of players
        self.exp.bind('<F2>', self.editSelectedPlayer)
        self.exp.bind('<F3>', self.createPlayer)
        self.exp.bind('<F9>', self.toggleAPlayer)
        self.noPlayers = tk.Label(self.oldPlayerPanel,
                                   text='There are no existing players',
                                   relief='raised',
                                   borderwidth='4'
                                   )
        self.noPlayers.grid(row=0,
                            column=0,
                            sticky='ewns')
        self.hideWidget(self.noPlayers)

        self.newPlayerPanel = tk.LabelFrame(self,
                                             height='10c',
                                             width='5c',
                                             borderwidth='2',
                                             relief='sunken',
                                             text='New Player'
                                             )
        self.newPlayerPanel.grid(row=0, column=1, sticky = 'ns')
        self.hideWidget(self.newPlayerPanel)

        self.editPlayerPanel = tk.LabelFrame(self,
                                        height='10c',
                                        width = '5c',
                                        borderwidth='2',
                                        relief = 'sunken',
                                        fg = 'red',
                                        text = 'Edit Player'
                                        )
        self.editPlayerPanel.grid(row = 0, column = 1, sticky = 'ns')
        self.hideWidget(self.editPlayerPanel)


        # [error panel area]
        self.dateErrorPanel = tk.LabelFrame(self,
                                            height='10c',
                                            width = '5c',
                                            borderwidth='2',
                                            relief = 'sunken',
                                            fg = 'red',
                                            text = 'Bad Date Format'
                                            )
        self.dateErrorPanel.grid(row = 0, column = 2, sticky = 'ns')
        self.hideWidget(self.dateErrorPanel)
        self.dateErrorLabel1 = tk.Label(self.dateErrorPanel,
                                       text = 'The date must be in mm/dd/yyyy US format,')
        self.dateErrorLabel1.grid(row = 0, column = 0)
        self.dateErrorLabel2 = tk.Label(self.dateErrorPanel,
                                        text = 'Press F5 to correct and try again.')
        self.dateErrorLabel2.grid(row=1, column = 0)
        # put the instructions into the Activity panel

        self.newPlayerForm(self.newPlayerPanel)
        self.buildActivityPanel()
        self.displayExistingPlayers()

    # ************************************************************
    #   build out activity panel entries
    def buildActivityPanel(self):
        MasterScreen.wipeActivityPanel()    # start with a clean slate
        self.ap = cfg.screenDict['activity']    # get activity panel widget
        self.keyF1 = tk.Label(self.ap, text = 'F1    Get help with this activity')
        self.keyF2 = tk.Label(self.ap, text = 'F2    Edit player selected in listbox')
        self.keyF3 = tk.Label(self.ap, text = 'F3    Create a new player')
        self.keyF9 = tk.Label(self.ap, text = 'F9    Toggle active status for player selected in listbox')
        self.keyF10 = tk.Label(self.ap, text = 'F10   Save all current changes')
        self.keyEsc = tk.Label(self.ap, text = 'Esc   Quit current activity')
        self.dClick = tk.Label(self.ap, text = 'Double Click to toggle active')
        self.keyF1.grid(row=1, column=0, sticky='w')
        self.keyF2.grid( column=0, sticky='w')
        self.keyF3.grid( column=0, sticky='w')
        self.keyF9.grid( column=0, sticky='w')
        self.keyF10.grid( column=0, sticky='w')
        self.keyEsc.grid( column=0, sticky='w')
        self.dClick.grid( column=0, sticky='w')

    # ************************************************************
    #   handle tab change by refreshing players
    def tabChange(self,event):
        #
        # always refreshes the list of existing players

        self.buildActivityPanel()
        self.displayExistingPlayers()

    #************************************************************
    #   build a display of existing players on file
    def displayExistingPlayers(self):
        # list out existing players
        self.hideWidget(self.noPlayers)
        if Player.select().count() == 0:
            self.showWidget(self.noPlayers)
            self.hideWidget(self.oldPlayerPanel)
        else:
#           print('Get and print players')
#           remove any No Players message
            self.hideWidget(self.noPlayers)
            self.showWidget(self.oldPlayerPanel)

            if self.showAllPlayers.get() > 0 :
                self.existingPlayers = cfg.ap.playersByLastName(cfg.clubRecord)
            else:
                self.existingPlayers = cfg.ap.allActivePlayers(cfg.clubRecord)

            print ('Show all players retrieved')
            print (self.existingPlayers)
            # self.existingPlayers = list(Player.select().orderBy('FirstName'))
##            print (self.existingPlayers)
            self.playersInDbms = []
#            print (self.existingPlayers[0].FirstName)
            # always leve room for the active asterisk
            for p in self.existingPlayers:
                if p.Active > 0:
                    self.playersInDbms.append(' * ' + p.LastName + ', ' +p.FirstName)
                else:
                    self.playersInDbms.append('   ' + p.LastName + ', ' + p.FirstName)
            # build listbox
            self.players.set(self.playersInDbms)
            # self.exp = tk.Listbox(self.oldPlayerPanel,
            #                       listvariable=self.players,
            #                       height = 20
            #                       )
            # self.exp.grid(row = 1, column = 0, columnspan = 2)
            #
            # self.scrollbar = tk.Scrollbar(self.oldPlayerPanel)
            # self.scrollbar.grid(row=1, column=2, sticky ='ns')
            # self.exp.config(yscrollcommand=self.scrollbar.set)
            # self.scrollbar.config(command=self.exp.yview)
            #
            # #
            # # allow ListBox entry to respond to double click for editing
            # #
            # # TODO: F2 will edit player, F3 to create new player, F9 to delete player
            #
            # # [binding section]
            # Do this binding everytime we recreate the listbox of players
            self.exp.bind('<F2>', self.editSelectedPlayer)
            self.exp.bind('<F3>', self.createPlayer)
            self.exp.bind('<F9>', self.toggleAPlayer)
            self.exp.bind('<Double-1>',self.togglePlayer)
        # set focus and selection for listbox
        self.exp.selection_set(0)
        self.exp.focus_force()

    #***********************************************************
    #   handler for double-click player state toggle
    def togglePlayer(self,event):
        # convert the double-click position into a selection
        self.exp.selection_clear(0,tk.END)     # clear any current selection
        self.lbIndex = self.exp.nearest(event.y)
        self.playerInExpName = self.exp.activate(self.lbIndex)
        # strip any * then trim blanks from name
        self.lbText = self.exp.get(self.lbIndex)
        # print ('Selected ' + self.lbText)
        # print ('Cleaned up <' + self.lbText.replace('*',' ').strip() + '>')
        # print('Player pid:= ' + str(cfg.playerRefx[self.lbText.replace('*',' ').strip()]))
        self.playerToToggle = cfg.ap.getPlayerById(str(cfg.playerRefx[self.lbText.replace('*',' ').strip()]))
        # print(self.playerToToggle.LastName + ' Active:= ' + str(self.playerToToggle.Active))
        # toggle the active status - 0 is inactive; <>0 is active
        if self.playerToToggle.Active == 0:
            self.playerToToggle.Active = 1
        else:
            self.playerToToggle.Active = 0
        # print ('Post Toggle ' + self.playerToToggle.LastName + ' Active:= ' + str(self.playerToToggle.Active))
        # and refresh the list of players
        self.displayExistingPlayers()

    #************************************************************
    #
    def submitNewPlayer(self, event):
        print('Validate and add new player')
        
        #validate the required fields
        print ('len(fname): ' + str(len(self.fname.get())))
        print ('len(lname): ' + str(len(self.lname.get())))

        #
        # at a minimum must have first and last name
        #
        print (self.fname.get())
        print (self.lname.get())

        if len(self.fname.get()) < 1 or len(self.lname.get()) < 1:
            # self.redText(self.fnameLabel)
            self.showNewPlayerError()
            self.errorHiLite(fnameEntry)
            self.errorHiLite(lnameEntry)
            return


        # try adding to the data base and catching any errors

        if self.checkForNameDup (self.fname.get(), self.lname.get()):
            self.redText(self.fnameLabel)
            self.redText(self.lnameLabel)
            self.duplicateName()
        else:
            # validate any date fields for new player

            try:
                print(self.fname.get())
                print(self.lname.get())
                print(self.phone.get())
                print(self.email.get())
                print(self.accno.get())
                print(self.joined.get())
                print(str(cfg.clubId))
                # Create a new player - let date field default for now
                # Handle blank active field
                if not (self.active.get() == 0 or self.active.get() == 1):
                    self.active.set(0)
                self.newPlayer = Player(FirstName  =   self.fname.get(),
                                     LastName   =   self.lname.get(),
                                     Street     =   self.street.get(),
                                     City       =   self.city.get(),
                                     Zip        =   self.zip.get(),
                                     Phone      =   self.phone.get(),
                                     Email      =   self.email.get(),
                                     ACCNumber  =   self.accno.get(),
                                     # Joined     =   self.joined.get(),
                                     # ACCExpiration = self.expiration.get(),
                                     Active     =   self.active.get(),
                                     Club       =   cfg.clubId
                                     )

                mbx.showinfo(('Player added successfully', 'Use F9 to make Active'))
                # must add any new player to the xrefs
                self.reBuildXrefs()
                # TODO: special handling required for date fields and blank active field
                # validate each date entry and update record if appropriate
                if self.expiration.get() != 'None':
                    if not (self.validateADate(self.expiration.get(), self.expirationEntry)):
                        self.showDateErrorPanel()
                        mbx.showinfo('Use F2 Edit to fix', 'Esc to quit New, then edit this date field')
                        self.hideDateErrorPanel()
                        self.hideWidget(self.newPlayerPanel)
                        self.resetForm()
                        self.displayExistingPlayers()
                        return
                if self.joined.get() != 'None':
                    if not (self.validateADate(self.joined.get(), self.joinedEntry)):
                        self.showDateErrorPanel()
                        mbx.showinfo('Use F2 Edit to fix', 'Esc to quit New, then edit this date field')
                        self.hideDateErrorPanel()
                        self.hideWidget(self.newPlayerPanel)
                        self.resetForm()
                        self.displayExistingPlayers()
                        return
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
        self.fnameLabel = tk.Label(parent, text='First Name')
        self.fnameLabel.grid(row=0,column=0)
        self.lnameLabel = tk.Label(parent, text='Last Name')
        self.lnameLabel.grid(row=1,column=0)
        self.streetLabel = tk.Label(parent, text='Street')
        self.streetLabel.grid(row=2,column=0)
        self.cityLabel = tk.Label(parent, text='City')
        self.cityLabel.grid(row=3,column=0)
        self.zipLabel = tk.Label(parent, text='Zip')
        self.zipLabel.grid(row=4,column=0)
        self.phoneLabel = tk.Label(parent, text='Phone')
        self.phoneLabel.grid(row=5,column=0)
        self.emailLabel = tk.Label(parent, text='Email')
        self.emailLabel.grid(row=6,column=0)
        self.accnoLabel = tk.Label(parent, text='ACC Number')
        self.accnoLabel.grid(row=7,column=0)
        self.expirationLabel = tk.Label(parent, text='Expires')
        self.expirationLabel.grid(row=8,column=0)
        self.joinedLabel = tk.Label(parent, text='Joined')
        self.joinedLabel.grid(row=9,column=0)
        self.activeLabel = tk.Label(parent, text='Active')
        self.activeLabel.grid(row=10,column=0)
        self.fnameEntry = tk.Entry(parent, textvariable=self.fname)
        self.fnameEntry.grid(row=0,column=1)
        self.lnameEntry = tk.Entry(parent, textvariable=self.lname)
        self.lnameEntry.grid(row=1, column=1)
        self.streetEntry = tk.Entry(parent, textvariable=self.street)
        self.streetEntry.grid(row=2, column=1)
        self.cityEntry = tk.Entry(parent, textvariable=self.city)
        self.cityEntry.grid(row=3, column=1)
        self.zipEntry = tk.Entry(parent, textvariable=self.zip)
        self.zipEntry.grid(row=4, column=1)
        self.phoneEntry = tk.Entry(parent, textvariable=self.phone)
        self.phoneEntry.grid(row=5, column=1)
        self.emailEntry = tk.Entry(parent, textvariable=self.email)
        self.emailEntry.grid(row=6, column=1)
        self.accnoEntry = tk.Entry(parent,textvariable=self.accno)
        self.accnoEntry.grid(row=7, column=1)
        self.expirationEntry = tk.Entry(parent, textvariable=self.expiration)
        self.expirationEntry.grid(row=8, column=1)
        self.joinedEntry = tk.Entry(parent, textvariable=self.joined)
        self.joinedEntry.grid(row=9, column=1)
        self.activeEntry = tk.Entry(parent, textvariable=self.active)
        self.activeEntry.grid(row=10, column=1)

        # navigation key binding
        self.fnameEntry.bind('<Key-Down>',self.handleDownKey)
        self.lnameEntry.bind('<Key-Down>', self.handleDownKey)
        self.streetEntry.bind('<Key-Down>', self.handleDownKey)
        self.cityEntry.bind('<Key-Down>', self.handleDownKey)
        self.zipEntry.bind('<Key-Down>', self.handleDownKey)
        self.phoneEntry.bind('<Key-Down>', self.handleDownKey)
        self.emailEntry.bind('<Key-Down>', self.handleDownKey)
        self.accnoEntry.bind('<Key-Down>', self.handleDownKey)
        self.expirationEntry.bind('<Key-Down>', self.handleDownKey)
        self.joinedEntry.bind('<Key-Down>', self.handleDownKey)


        self.lnameEntry.bind('<Key-Up>', self.handleUpKey)
        self.streetEntry.bind('<Key-Up>', self.handleUpKey)
        self.cityEntry.bind('<Key-Up>', self.handleUpKey)
        self.zipEntry.bind('<Key-Up>', self.handleUpKey)
        self.phoneEntry.bind('<Key-Up>', self.handleUpKey)
        self.emailEntry.bind('<Key-Up>', self.handleUpKey)
        self.accnoEntry.bind('<Key-Up>', self.handleUpKey)
        self.expirationEntry.bind('<Key-Up>', self.handleUpKey)
        self.joinedEntry.bind('<Key-Up>', self.handleUpKey)
        self.activeEntry.bind('<Key-Up>', self.handleUpKey)

        # always position at first entry field.
        self.fnameEntry.focus_force()
    # ************************************************************
    #
    def createPlayer(self,event):
        self.hideWidget(self.editPlayerPanel)
        self.showWidget(self.newPlayerPanel)
        self.resetAllErrorHiLites()
        self.fnameEntry.focus_force()
        self.fnameEntry.select_range(0, tk.END)
    #************************************************************
    #
    def newPlayerForm(self, parent):
        self.buildPlayerForm(parent)

        # [newplayer form binding section]
        self.fnameEntry.bind('<F10>', self.submitNewPlayer)
        self.lnameEntry.bind('<F10>', self.submitNewPlayer)
        self.streetEntry.bind('<F10>', self.submitNewPlayer)
        self.cityEntry.bind('<F10>', self.submitNewPlayer)
        self.zipEntry.bind('<F10>', self.submitNewPlayer)
        self.phoneEntry.bind('<F10>', self.submitNewPlayer)
        self.emailEntry.bind('<F10>', self.submitNewPlayer)
        self.accnoEntry.bind('<F10>', self.submitNewPlayer)
        self.expirationEntry.bind('<F10>', self.submitNewPlayer)
        self.activeEntry.bind('<F10>', self.submitNewPlayer)
        self.joinedEntry.bind('<F10>', self.submitNewPlayer)
        self.activeEntry.bind('<F10>', self.submitNewPlayer)
        self.fnameEntry.bind('<Escape>', self.cancelNewPlayer)
        self.lnameEntry.bind('<Escape>', self.cancelNewPlayer)
        self.streetEntry.bind('<Escape>', self.cancelNewPlayer)
        self.cityEntry.bind('<Escape>', self.cancelNewPlayer)
        self.zipEntry.bind('<Escape>', self.cancelNewPlayer)
        self.phoneEntry.bind('<Escape>', self.cancelNewPlayer)
        self.emailEntry.bind('<Escape>', self.cancelNewPlayer)
        self.accnoEntry.bind('<Escape>', self.cancelNewPlayer)
        self.expirationEntry.bind('<Escape>', self.cancelNewPlayer)
        self.activeEntry.bind('<Escape>', self.cancelNewPlayer)
        self.joinedEntry.bind('<Escape>', self.cancelNewPlayer)
        self.activeEntry.bind('<Escape>', self.cancelNewPlayer)

    #************************************************************
    #
    def setUpEditPlayerPanel (self):
        self.hideWidget(self.newPlayerPanel)
        self.showWidget(self.editPlayerPanel)
        self.editPlayerForm(self.editPlayerPanel)
        self.setFocus(self.fnameEntry)
        self.showSelected(self.fnameEntry)
   
    #************************************************************
    #
    def editPlayerForm(self, parent):
        print ('Build edit player widgets')
        joinedOn = self.existingPlayers[self.ListBoxIndex].Joined
        ACCExpiresOn = self.existingPlayers[self.ListBoxIndex].ACCExpiration
        print ('joineOn ', joinedOn)
        print ('ACCExpiresOn ', ACCExpiresOn)
        self.buildPlayerForm(parent)
        print ('Player to be edited')
        print (self.existingPlayers[self.ListBoxIndex])
        self.fname.set(self.existingPlayers[self.ListBoxIndex].FirstName)
        self.lname.set(self.existingPlayers[self.ListBoxIndex].LastName)
        self.street.set(self.existingPlayers[self.ListBoxIndex].Street)
        self.city.set(self.existingPlayers[self.ListBoxIndex].City)
        self.zip.set(self.existingPlayers[self.ListBoxIndex].Zip)
        self.phone.set(self.existingPlayers[self.ListBoxIndex].Phone)
        self.email.set(self.existingPlayers[self.ListBoxIndex].Email)
        self.accno.set(self.existingPlayers[self.ListBoxIndex].ACCNumber)
        self.expiration.set(self.testDateIsNone(ACCExpiresOn))
        self.joined.set(self.testDateIsNone(joinedOn))
        self.active.set(self.existingPlayers[self.ListBoxIndex].Active)

        # [edit player form binding section]
        self.fnameEntry.bind('<F10>', self.editAPlayer)
        self.lnameEntry.bind('<F10>', self.editAPlayer)
        self.streetEntry.bind('<F10>', self.editAPlayer)
        self.cityEntry.bind('<F10>', self.editAPlayer)
        self.zipEntry.bind('<F10>', self.editAPlayer)
        self.phoneEntry.bind('<F10>', self.editAPlayer)
        self.emailEntry.bind('<F10>', self.editAPlayer)
        self.accnoEntry.bind('<F10>', self.editAPlayer)
        self.expirationEntry.bind('<F10>', self.editAPlayer)
        self.activeEntry.bind('<F10>', self.editAPlayer)
        self.joinedEntry.bind('<F10>', self.editAPlayer)
        self.fnameEntry.bind('<Escape>', self.cancelPlayerEdit)
        self.lnameEntry.bind('<Escape>', self.cancelPlayerEdit)
        self.streetEntry.bind('<Escape>', self.cancelPlayerEdit)
        self.cityEntry.bind('<Escape>', self.cancelPlayerEdit)
        self.zipEntry.bind('<Escape>', self.cancelPlayerEdit)
        self.phoneEntry.bind('<Escape>', self.cancelPlayerEdit)
        self.emailEntry.bind('<Escape>', self.cancelPlayerEdit)
        self.accnoEntry.bind('<Escape>', self.cancelPlayerEdit)
        self.expirationEntry.bind('<Escape>', self.cancelPlayerEdit)
        self.activeEntry.bind('<Escape>', self.cancelPlayerEdit)
        self.joinedEntry.bind('<Escape>', self.cancelPlayerEdit)

    #************************************************************
    #
    def cancelPlayerEdit (self, event):
        # restore new Player panel
        print ('back to players panel')
        self.hideWidget(self.editPlayerPanel)
        self.hideWidget(self.newPlayerPanel)
        # self.editPlayerPanel.grid_remove()
        self.resetForm()
        self.displayExistingPlayers()

    #************************************************************
    #
    def toggleAPlayer(self,event):
        self.ListBoxIndex = event.widget.curselection()[0]
        self.deleteMsg = """\tPlayer Toggle is a soft delete that marks player inactive.
    \tInactive (aka deleted) players do not appear in any reports.
    \tUndelete returns a player to active status.
    \tAll results for deleted players are retained."""
        mbx.showinfo('Toggle a Player', self.deleteMsg)
        cfg.at.countTourneysForSeason(cfg.season)
        cfg.ap.getPlayerById(1)
        togglePlayer = cfg.ap.singlePlayerByFirstandLastNames(self.existingPlayers[self.ListBoxIndex].FirstName,
                                                      self.existingPlayers[self.ListBoxIndex].LastName)
        playerName = togglePlayer.FirstName + ' ' + togglePlayer.LastName
        if togglePlayer.Active == 0:
            togglePlayer.Active = 1
            mbx.showinfo(playerName , 'is now Active')
        else:
            togglePlayer.Active = 0
            mbx.showinfo(playerName, 'is no longer Active')
    # print (togglePlayer)

    #************************************************************
    #
    def editSelectedPlayer(self,event):
        print ('Edit selected player from listbox')
        #
        # replace NewPlayer panel with EditPlayer panel
        #
        self.ListBoxIndex = event.widget.curselection()[0]
        print ('ListBoxIndex: ', self.ListBoxIndex)
        # self.editEntry = self.exp.get(self.ListBoxIndex)
        # print (self.editEntry)
        self.setUpEditPlayerPanel()

        
    #************************************************************
    #
    def editAPlayer (self, event):
        print ('Replace player entry')
        changePlayer = cfg.ap.singlePlayerByFirstandLastNames(self.existingPlayers[self.ListBoxIndex].FirstName,
                                                      self.existingPlayers[self.ListBoxIndex].LastName)
        # changePlayer = Player.select(Player.q.FirstName == (self.exp[self.ListBoxIndex].FirstName))[0]
        print ('Changeplayer ', changePlayer)
        # First we check out the date fields for any errors which need to be corrected.
        # Turn off any prior errors
        self.resetErrorHiLite(self.joinedEntry)
        self.resetErrorHiLite(self.expirationEntry)
        self.hideWidget(self.dateErrorPanel)
        if self.expiration.get() != 'None':
            if not (self.validateADate(self.expiration.get(), self.expirationEntry)):
                self.showDateErrorPanel()
                self.setFocus(self.expirationEntry)
                return  # leave, let user try again
        if self.joined.get() != 'None':
            if not (self.validateADate(self.joined.get(), self.joinedEntry)):
                self.showDateErrorPanel()
                self.setFocus(self.joinedEntry)
                return      # leave, let user try again

        changePlayer.FirstName  = self.fname.get()
        changePlayer.LastName   = self.lname.get()
        changePlayer.Street     = self.street.get()
        changePlayer.City       = self.city.get()
        changePlayer.Zip        = self.zip.get()
        changePlayer.Phone      = self.phone.get()
        changePlayer.Email      = self.email.get()
        changePlayer.ACCNumber  = self.accno.get()
        if self.expiration.get() != 'None':
            changePlayer.ACCExpiration = self.makeIsoDate(self.expiration.get())
        # changePlayer.ACCExpiration = '' if self.expiration.get() == 'None' else self.makeIsoDate(self.expiration.get())
        changePlayer.Active     = self.active.get()
        if self.joined.get() != 'None':
            changePlayer.Joined = self.makeIsoDate(self.joined.get())
        # changePlayer.Joined     = '' if self.joined.get() == 'None' else self.makeIsoDate(self.joined.get())
    #************************************************************
    #
    def cancelNewPlayer(self, event):
        print('Cancel new player add')
        self.resetForm()
        self.hideWidget(self.newPlayerPanel)
        self.exp.selection_clear(0, self.exp.size()-1)
        self.exp.selection_set(0)
        self.exp.activate(0)
        self.exp.focus_force()
        
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
        self.street.set('')
        self.city.set('')
        self.zip.set('')
        self.phone.set('')
        self.email.set('')
        self.accno.set('')
        self.expiration.set('')
        self.active.set('')
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

    def handleDownKey(self, event):
        print ('Handle down key')
        downDict = {
            self.fnameEntry:    self.lnameEntry,
            self.lnameEntry:    self.streetEntry,
            self.streetEntry:   self.cityEntry,
            self.cityEntry:     self.zipEntry,
            self.zipEntry:      self.phoneEntry,
            self.phoneEntry:    self.emailEntry,
            self.emailEntry:    self.accnoEntry,
            self.accnoEntry:    self.expirationEntry,
            self.expirationEntry: self.joinedEntry,
            self.joinedEntry:   self.activeEntry
            }
        downDict[event.widget].focus_force()
        downDict[event.widget].select_range(0, tk.END)

    def handleUpKey(self, event):
        print ('Handle Up Key')
        upDict = {
            self.lnameEntry:    self.fnameEntry,
            self.streetEntry:   self.lnameEntry,
            self.cityEntry:     self.streetEntry,
            self.zipEntry:      self.cityEntry,
            self.phoneEntry:    self.zipEntry,
            self.emailEntry:    self.phoneEntry,
            self.accnoEntry:    self.emailEntry,
            self.expirationEntry: self.accnoEntry,
            self.joinedEntry:   self.expirationEntry,
            self.activeEntry:   self.joinedEntry
        }
        upDict[event.widget].focus_force()
        upDict[event.widget].select_range(0, tk.END)
    def setFocus(self, target):
        target.focus_force()
    def showSelected(self, w):
        w.select_range(0, tk.END)
    def showDateErrorPanel(self):
        self.showWidget(self.dateErrorPanel)
    def hideDateErrorPanel(self):
        self.hideWidget((self.dateErrorPanel))
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
    def errorHiLite(self, w):
        w.config(background = 'pink', foreground = 'black')
    def resetErrorHiLite(self, w):
        w.config(background = 'white', foreground = 'black')
    def resetAllErrorHiLites(self):
        # cycle through any fields that might have been  highlighted
        self.resetErrorHiLite(self.fnameEntry)
        self.resetErrorHiLite(self.lnameEntry)
        self.resetErrorHiLite(self.zipEntry)
        self.resetErrorHiLite(self.activeEntry)
        self.resetErrorHiLite(self.expirationEntry)
        self.resetErrorHiLite(self.joinedEntry)
    def validateADate(self, value, w):
        # validate value as a good US data; errorlite widget w if wrong
        # use the parser funcion to create a datetime.date object - or None
        # TODO have to allow for an empty date field
        if not dateparser.parse(value):
            #bad date
            self.errorHiLite(w)
            return False
        else:
            self.resetErrorHiLite(w)
            return True
    def makeIsoDate(self, USDate):
        # take date in US format and turn into ISO8601 format for data object
        # print (dateparser.parser(USDate).date().isoformat())
        return dateparser.parse(USDate).date().isoformat()
    def makeUSDate(self, ISODate):
        # presumes incoming date is valid ISODate
        return ISODate.strftime('%m/%e/%Y')
    def testDateIsNone(self, dateValue):
        return dateValue  if dateValue is None else self.makeUSDate(dateValue)
    def reBuildXrefs(self):
        # cfg.playerXref = {p.id: p.LastName + ', ' + p.FirstName for p in list(Player.select())}
        CribbageStartup.createPlayersXRef()