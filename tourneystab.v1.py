#tourneystab.py
#
#####################################################################
#
#   Creates tab screen for add/change/delete tourneys by date
#   Will self-register in notebook found in screenDict of cfg
#   ManageTourneys was Version 1.0
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
from tourney import Tourney

class TourneysTab (ttk.Frame):
    # screen class is always a frame

    #************************************************************   
    #   
    #   sets up tab for add/change/delete tourney dates

    def __init__ (self, parent=None):
        super().__init__(parent)
        self.grid()

        # control variables for tourneys

        self.tourneyDate = tk.StringVar()
        self.existingTourneyDates = tk.StringVar()
        self.existingTourneyValues = tk.StringVar()

        # build out tab and register with notebook

        self.config(padding='10p')
        parent.add(self,text='Tourneys')


        # register this tab

        cfg.screenDict['ttab'] = self

        # tourney tab row 0
        
        self.newTourneyLabel = ttk.Label(self,
                                         text = 'New Tourney Date:  ')
        self.newTourneyLabel.grid(row=0, column=0)
        self.newTourneyDate = ttk.Entry(self,
                                        textvariable = self.tourneyDate)
        self.newTourneyDate.bind('<KeyPress-Escape>', self.forgetIt)
        self.newTourneyDate.grid(row = 0, column = 1)
        
        #
        # tourney tab row 1
        #
        
        self.addTourney = ttk.Button(self,
                                    text = 'Add New Tourney',
                                    command=self.addNewTourney
                                    )
        self.addTourney.grid(row=1, column=0)
        self.updateTourney = ttk.Button(self,
                                     text = 'Update Tourney',
                                     command=self.updateTourney
                                     )
        self.updateTourney.grid(row=1, column=1)
        self.hideWidget(self.updateTourney)

        
 
        # tourney panel row 2 - spacer
        
        ttk.Label(self,
                  text=' ').grid(row=2
                                 ,column=0)
        self.deleteTourney = ttk.Button(self,
                                        text='Delete Tourney',
                                        command=self.deleteTourney
                                        )
        self.deleteTourney.grid(row=2, column=1)
        self.hideWidget(self.deleteTourney)
        self.Cancel = ttk.Label(self,
                                text='Hit Esc to Cancel')
        self.Cancel.grid(row=3, column=0)
        self.Cancel.grid_remove()   # hide for now
        
        # tourney panel row 3
        
        self.doubleClickLabel = ttk.Label(self,
                  text='Double Click a Date to Take Action On')
        self.doubleClickLabel.grid(row=3, column=1)


        # tourney panel row 4
        #
        # show past tourneys - arbitrarily show 12 - no scroll bar for now
        #
        self.existingTourneysLabel = ttk.Label(self,
                                          text = 'Existing Tourneys:   ')
        self.existingTourneysLabel.grid(row=4, column=0, sticky = 'n')
        self.existingTourneys = tk.Listbox(self,
                                       listvariable=self.existingTourneyValues)
        self.existingTourneys.grid(row=4, column=1)
        self.scrollBar = tk.Scrollbar(self)
        self.scrollBar.grid(row=4, column=2, sticky='n')
        self.existingTourneys.config(yscrollcommand=self.scrollBar.set)
        self.scrollBar.config(command=self.existingTourneys.yview)
        self.populateExistingTourneys()

        # have to bind event to listbox as there is no command option
        self.existingTourneys.bind('<Double-Button-1>',self.editSelectedTourney)

        
    #************************************************************
    #
    def populateExistingTourneys(self):
        #
        # retrieve up to twelve existing tourneys for display
        #
##        print (Tourney.select)
            self.dbmsTourneyDates = list(Tourney.select().orderBy('-Date'))
            self.existingTourneyValues.set([self.dbmsTourneyDates[x].Date for x in range(len(self.dbmsTourneyDates))])
                
    #************************************************************
    #
    def addNewTourney (self):
        # build a new Tourney and add it to the data base
        # and reshow
        try:
            Tourney(Date = self.tourneyDate.get(), ClubID = 1)
            self.populateExistingTourneys()
            self.tourneyDate.set('')
        except dberrors.DuplicateEntryError:
            print('Duplicate tourney date')
            self.redText(self.newTourneyDate)
            # leave date there and offer edit or cancel
##            self.hideWidget(self.addTourney)    # hide button
##            self.showWidget(self.editTourney)  # show button

            if mbx.askretrycancel('Change Date?','Edit date or cancel',parent = self.tourneyTab):
                # set focus and let user retry the date
                self.newTourneyDate.focus_set()
            else:
                self.blackText(self.newTourneyDate)
                self.tourneyDate.set('')
            

    #************************************************************
    #
    def forgetIt(self, event):
        # forget Tourney update or delete
        self.tourneyDate.set('')
        self.newTourneyDate.focus_set()
        self.hideWidget(self.Cancel)
        self.hideWidget(self.updateTourney)
        self.hideWidget(self.deleteTourney)
        self.showWidget(self.addTourney)

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
    def editSelectedTourney(self, event):
        # this is activated by DoubleClick-1 : left mouse button
        self.listBoxIndex = self.existingTourneys.curselection()
        print(eval(self.existingTourneyValues.get())[self.listBoxIndex[0]])
        self.tourneyDate.set(eval(self.existingTourneyValues.get())[self.listBoxIndex[0]])
        self.oldTourneyDate = self.tourneyDate.get()
        self.hideWidget(self.doubleClickLabel)
        self.showWidget(self.updateTourney)
        self.showWidget(self.deleteTourney)
        self.showWidget(self.Cancel)
        self.hideWidget(self.addTourney)
        self.newTourneyDate.focus_set()
        
    #************************************************************
    #
    def updateTourney(self):
        # replace current tourney entry with new date
        self.editingRecordId = self.getRecordId(self.oldTourneyDate)
        t = Tourney.get(self.editingRecordId)
        t.set(Date=self.tourneyDate.get())
        self.populateExistingTourneys()
        self.hideWidget(self.updateTourney)
        self.hideWidget(self.deleteTourney)
        self.showWidget(self.addTourney)
        self.tourneyDate.set('')
    
    #************************************************************
    #
    def deleteTourney(self):
        # delete the current tourney
        # TODO: should check we are not deletng a tourney for
        # which there are already results...this would be a
        # serious data integrity error.
        t = Tourney.select(Tourney.q.Date == self.tourneyDate.get())
        l = list(t)
        Tourney.delete(l[0].id)
        # reshow the list after the deletion
        self.populateExistingTourneys()
        
    #************************************************************
    #
    def getRecordId (self, date):
        print (date)
        t = Tourney.select(Tourney.q.Date == date)
        l = list(t)
        print (l)
        print (l[0].id)
        return l[0].id
       
    
