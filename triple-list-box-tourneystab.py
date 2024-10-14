# triple-list-box-tourneystab.py
# 7/21/2020 updated to cribbageconfig
#
#####################################################################
#
#   Creates tab screen for add/change/delete tourneys by date
#   Will self-register in notebook found in screenDict of cfg
#   ManageTourneys was Version 1.0
#
#####################################################################
# TODO: When tourneys are created, renumber all entries
# TODO: When tourneys are deleted, warn if results have been entered.
# TODO: Mush all tourney entries into a concatenated single entry.
#
# TODO: Change screen key handling as follows:
#       For going to results, select with mouse then press -> to go to results.
#       This frees up the Return key for handling autoselect in various places
# TODO: Implement the Esc key as a general way to get out and back to start.
# TODO: When there are results for a tourney this is not being shown on the
#       list of existing tourneys.

# System imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg

from sqlobject import *

import sys
import os
import datetime

# Personal imports
import cribbageconfig as cfg
from tourney import Tourney
from masterscreen import MasterScreen

class TourneysTab (tk.Frame):
    # screen class is always a frame
    #************************************************************   
    #   
    #   sets up tab for add/change/delete tourney dates

    def __init__ (self, parent=None):
        super().__init__(parent)
        self.grid()
        self.parent = parent

        # [control variables] for tourneys
        self.newTourneyDate = tk.StringVar()
        self.newTourneyNumber = tk.StringVar()
        self.tourneyDate = tk.StringVar()
        self.editTourneyNumber = tk.StringVar()
        self.editTourneyDate = tk.StringVar()
        self.existingTrourneyNumber = tk.StringVar()
        self.existingTourneyDate = tk.StringVar()

        self.selectedResultsTourney = ''
        self.beingEdited = ''
        self.editTourneyOriginalDate = ''
        self.editTourneyOriginalNumber = ''

        # build out tab and register with notebook
        self.config(padx = 5, pady = 5)
        parent.add(self,text='Tourneys')
        # register this tab
        cfg.screenDict['ttab'] = self

        # manage tourneys tab row 0
        self.tourneysPanel = tk.LabelFrame(self,
                                           text='Tourneys',
                                           height=10,
                                           width=6,
                                           borderwidth='2',
                                           relief='sunken')
        self.tourneysPanel.grid(row=0,column=0, sticky='nw')
        self.keyF6 = tk.Label(self.tourneysPanel,
                              text = 'F6 - Enter results for selected tourney',
                              fg='green',
                              font=('Helvetica', '9', 'bold'))
        self.keyF6.grid(row=0, column=0, sticky='w')

        self.tourneyMaintenance = tk.LabelFrame(self,
                                                text="Manage Tourneys",
                                                height=10,
                                                width=7,
                                                borderwidth=2,
                                                relief='sunken')
        self.tourneyMaintenance.grid(row=0, column=1, sticky='nw')
        self.editInstructionsPanel = tk.Frame(self.tourneyMaintenance)
        self.editInstructions1 = tk.Label(self.editInstructionsPanel,
                                         text='Change the selected tourney fields')
        self.editInstructions2 = tk.LabelFrame(self.editInstructionsPanel,
                                               text='Then F10 to save or Esc to cancel')
        self.editInstructions1.grid(row=0, column=0, sticky='w')
        self.editInstructions2.grid(row=1, column=0, sticky='w')

        self.newInstructionsPanel = tk.Frame(self.tourneyMaintenance)
        self.newInstructions1 = tk.Label(self.newInstructionsPanel,
                                       text='Enter new fields')
        self.newInstructions2 = tk.Label(self.newInstructionsPanel,
                                         text='Then F10 to save or Esc to cancel')
        self.newInstructions1.grid(row=0, column=0, sticky='w')
        self.newInstructions2.grid(row=1, column=0, sticky='w')

        self.newTourneyPanel = tk.LabelFrame(self,
                                         height=10,
                                         width=10,
                                         borderwidth=2,
                                         relief='sunken',
                                         text='New Tourney')
        self.newTourneyPanel.grid(row=1,column=1,sticky='nw')
        # self.hideWidget(self.newTourneyPanel)
        #
        # edit existing tourney panel
        #
        self.existingTourneyPanel = tk.LabelFrame(self,
                                                  height=10,
                                                  width=10,
                                                  borderwidth=2,
                                                  relief='sunken',
                                                  text='Existing Tourney')
        self.existingTourneyPanel.grid(row=1, column=1, sticky='nw')

        self.existingTourneyNumberLabel =tk.Label(self.existingTourneyPanel,
                                               text = 'Trny Label: '
                                               )
        self.existingTourneyNumberEntry = tk.Entry(self.existingTourneyPanel,
                                               width = 4,
                                              textvariable = self.editTourneyNumber)
        self.existingTourneyDateLabel = tk.Label(self.existingTourneyPanel,
                                              text = 'Trny Date:  ')
        self.existingTourneyDateEntry = tk.Entry(self.existingTourneyPanel,
                                             width = 10,
                                             textvariable = self.editTourneyDate)
        self.existingTourneyNumberLabel.grid(row = 0, column = 0, sticky='w')
        self.existingTourneyNumberEntry.grid(row = 0, column = 1, sticky='w')
        self.existingTourneyDateLabel.grid(row = 1, column = 0, sticky='w')
        self.existingTourneyDateEntry.grid(row = 1, column = 1, sticky='w')

        self.editTourneyPanel = tk.LabelFrame(self,
                                               height = 10,
                                               width = 10,
                                               borderwidth = 2,
                                               relief = 'sunken',
                                               text = 'Edit Tourney'
                                               )
        self.editTourneyPanel.grid(row = 1, column = 2, sticky = 'nw')
        self.editTourneyNumberLabel =tk.Label(self.editTourneyPanel,
                                               text = 'Trny Label: '
                                               )
        self.editTourneyNumberEntry = tk.Entry(self.editTourneyPanel,
                                               width = 4,
                                              textvariable = self.editTourneyNumber)
        self.editTourneyDateLabel = tk.Label(self.editTourneyPanel,
                                              text = 'Trny Date:  ')
        self.editTourneyDateEntry = tk.Entry(self.editTourneyPanel,
                                             width = 10,
                                             textvariable = self.editTourneyDate)
        self.editTourneyEditError = tk.Label(self.editTourneyPanel,
                                             fg='red',
                                             font=('Helvetica', '9', 'bold'),
                                            text = 'Update has errors'
                                            )
        self.editTourneyNumberLabel.grid(row = 0, column = 0, sticky='w')
        self.editTourneyNumberEntry.grid(row = 0, column = 1, sticky='w')
        self.editTourneyDateLabel.grid(row = 1, column = 0, sticky='w')
        self.editTourneyDateEntry.grid(row = 1, column = 1, sticky='w')
        self.editTourneyEditError.grid(row = 2, column = 0, sticky='w')
        self.editTourneyEditError.grid_remove() # hide until we have an error

        self.newTourneyNumberLabel = tk.Label(self.newTourneyPanel,
                                          text = 'New tourney Number: ')
        self.newTourneyNumberLabel.grid(row = 0, column = 0, sticky = 'w')
        self.newTourneyNumberEntry = tk.Entry(self.newTourneyPanel,
                                          width = 3,
                                          textvariable = self.newTourneyNumber)
        self.newTourneyNumberEntry.bind('<KeyPress-Escape>', self.forgetIt)
        self.setNumberEntryHandler(self.newTourneyNumberEntry)
        self.newTourneyNumberEntry.grid(row = 0, column = 1, sticky = 'w')
        self.newTourneyDateLabel = tk.Label(self.newTourneyPanel,
                                         text='New Tourney Date:  ')
        self.newTourneyDateLabel.grid(row=1, column=0,sticky='w')
        self.newTourneyDateEntry = tk.Entry(self.newTourneyPanel,
                                            width = 12,
                                        textvariable = self.newTourneyDate)
        self.newTourneyDateEntry.bind('<KeyPress-Escape>', self.forgetIt)
        self.setDateEntryHandler(self.newTourneyDateEntry)
        self.newTourneyDateEntry.grid(row = 1, column = 1,sticky='w')
        self.tournamentsPanel = tk.LabelFrame(self,
                                          height=10,
                                          width=5,
                                          borderwidth=2,
                                          relief='sunken',
                                          text='Existing Tournaments')
        self.tournamentsPanel.grid(row=1,column=0,sticky='w')


        self.existingTourneysLabel = ttk.Label(self.tournamentsPanel,
                                          text = 'Tourney No.  ')
        self.existingTourneysLabel.grid(row=1, column=0, sticky = 'w')
        self.tourneyDataLabel = ttk.Label(self.tournamentsPanel,
                                          text = ' Data ')
        self.tourneyDataLabel.grid(row=1, column=1)
        self.tourneysDateLabel = ttk.Label(self.tournamentsPanel,
                                          text = '   Tourney Date')
        self.tourneysDateLabel.grid(row=1, column=2)

        # [hide edit widgets]
        self.hideEditTourney()
        self.hideCreateTourney()


        # now set up displays
        self.existingNumbers = tk.Listbox(self.tournamentsPanel,
                                          exportselection=0,
                                          # listvariable = self.existingTourneyNumbers,
                                          width=4,
                                          height=18,
                                          selectmode='single',
                                          yscrollcommand=self.vsb_set)
        self.existingNumbers.grid(row=2, column=0)

        self.existingValues = tk.Listbox(self.tournamentsPanel,
                                         exportselection=0,
                                         # listvariable = self.existingTourneyValues,
                                         width=4,
                                         height=18,
                                         selectmode='single',
                                         yscrollcommand=self.vsb_set)
        self.existingValues.grid(row=2, column=1)

        self.existingDates = tk.Listbox(self.tournamentsPanel,
                                        exportselection=0,
                                        # listvariable=self.existingTourneyDates,
                                        width=12,
                                        height=18,
                                        selectmode='single',
                                        yscrollcommand=self.vsb_set)
        self.existingDates.grid(row=2, column=2)

        self.vsb= tk.Scrollbar(self.tournamentsPanel, command=self.OnVsb)
        self.vsb.grid(row=2, column=3, sticky='ns')

        self.listOfListboxes = []
        self.listOfListboxes.append(self.existingNumbers)
        self.listOfListboxes.append(self.existingValues)
        self.listOfListboxes.append(self.existingDates)

        # [binding section]
        for lb in self.listOfListboxes:
            lb.bind('<F2>', self.editSelectedTourney)
            lb.bind('<F3>', self.createNewTourney)
            lb.bind('<F6>', self.enterResults)
            lb.bind('<F9>', self.deleteTourney)

        for lb in self.listOfListboxes:
            lb.bind('<<ListboxSelect>>', self.handle_select)

        # self.vsb.config(command=self.yview)
        self.populateExistingTourneys()

        for lb in self.listOfListboxes:
            lb.selection_set(0)
            lb.activate(0)

        self.listOfListboxes[0].focus_force()
        self.buildActivityPanel()
    def OnVsb(self, *args):
        for lb in self.listOfListboxes:
            lb.yview(*args)
    def handle_select(self, event):
        # set every list to the same selection
        for lb in self.listOfListboxes:
            if lb != event.widget:
                lb.selection_clear(0, 'end')
                lb.selection_set(event.widget.curselection())
                # lb.activate(event.widget.curselection())
    def vsb_set(self, *args):
        self.vsb.set(*args)
        for lb in self.listOfListboxes:
            lb.yview_moveto(args[0])

    def buildActivityPanel(self):
        # start by wiping any prior entries
        MasterScreen.wipeActivityPanel()
        self.mtp = cfg.screenDict['activity']
        self.keyF2 = tk.Label(self.mtp, text = 'F2   Edit currently selected tourney')
        self.keyF3 = tk.Label(self.mtp, text = 'F3   Create new tourney')
        self.keyF9 = tk.Label(self.mtp, text = 'F9   Delete selected tourney')
        self.keyF10 = tk.Label(self.mtp, text='F10  Save updates')
        self.keyEsc = tk.Label(self.mtp, text = 'Esc  Quit current activity')
        self.keyF2.grid(row=0, column=0, sticky='w')
        self.keyF3.grid(row=1, column=0, sticky='w')
        self.keyF9.grid(row=2, column=0, sticky='w')
        self.keyF10.grid(row=3, column=0, sticky='w')
        self.keyEsc.grid(row=4, column=0, sticky='w')


    def highlightTourney(self,buttonEvent):
        # capture where button was pressed
        self.selectedResultsTourney = self.existingDates.nearest(buttonEvent.y)  # capture the line
        print ('Captured event', buttonEvent)
        print('selectedResultsTourney: ',self.selectedResultsTourney)
        # self.existingDates.selection_anchor(self.selectedResultsTourney)
    def selectForResultsByNumber(self,enterEvent):
        cfg.tourneyNumber = self.existingNumbers.get(self.existingNumbers.curselection())
        cfg.tourneyDate = self.existingDates.get(self.existingNumbers.curselection())
        self.validateTourneySelection()
    def selectForResultsByDate(self,enterEvent):
        # TODO: Check that when enter has been pressed there is a valid
        #       selection of a tournement for results, otherwise the resultstab
        #       does not know what to do.
        #       Show message box and invite retry
        # TODO: After new tourney has been created successfully, reposition
        #       focus back at Tourney Number entry ready for another new tourney or
        #       allow Esc to quit creating new Tourneys ar allow Return to
        #       select the Create Tourney as the default action.
        # select this tourney and advance to results tab
        # print('self.existingTourneyDates: ', self.existingDates.get(self.existingDates.curselection()))

        cfg.tourneyDate = self.existingDates.get(self.existingDates.curselection())
        cfg.tourneyNumber = int(self.existingNumbers.get(self.existingDates.curselection()))
        self.validateTourneySelection()
    def validateTourneySelection(self):
        if not self.ValidTourneyDate(cfg.tourneyDate):
            if self.badTourneyForResults():
                # True means user wishes to retry selection
                # so refresh and await user action
                self.populateExistingTourneys()
                return
            else:
                # Acutally do the same thing, wait for user to select some action
                self.populateExistingTourneys()
                return
        print ('cfg.tourneyDate: ', cfg.tourneyDate)
        print ('iso date: ', self.makeIsoDate(cfg.tourneyDate))
        cfg.tourneyRecordId = cfg.at.getTourneyIdByDate(self.makeIsoDate(cfg.tourneyDate))
        cfg.tourneyRecord = cfg.at.getTourneyRecordByDate(self.makeIsoDate(cfg.tourneyDate))
        print('cfgDate:' ,cfg.tourneyDate)
        print('cfgTourneyNumber: ', cfg.tourneyNumber)
        print('cfgTourneyId: ', cfg.tourneyRecordId)
        print ('Switch to results tab')
        self.parent.select(2)       # this is how we switch to the results panel

    def tabChange(self,event):
        #
        # if not tournements, then must request at least one to be created
        #
        self.buildActivityPanel()
        if cfg.at.countTourneysForSeason(cfg.season) < 1:
            self.showAddButtons()
            self.showWidget((self.newTourneyPanel))

    def populateExistingTourneys(self):
        #
        # retrieve up to twelve existing tourneys for display - well that's not true!
        #
        # print (Tourney.select)
        # always clear out the existing listboxes
        self.clearListBoxes()
        self.unsortedTourneyDates = cfg.at.allTourneysForClubBySeason(cfg.clubRecord, cfg.season)
        for t in self.unsortedTourneyDates:
            print (t.TourneyNumber)
        # show youngest tourneys first - with lowest date & tourney number
        self.dbmsSortedTourneys = sorted(self.unsortedTourneyDates, key = lambda Tourney: Tourney.TourneyNumber)
        # change to use listbox.insert(posn, value) method
        for x in self.dbmsSortedTourneys:
            self.existingNumbers.insert(tk.END, x.TourneyNumber)
            self.existingValues.insert(tk.END, x.Entered)
            self.existingDates.insert(tk.END, self.makeUSDate(x.Date))
    def clearListBoxes(self):
        self.existingNumbers.delete(0, tk.END)
        self.existingValues.delete(0, tk.END)
        self.existingDates.delete(0, tk.END)
    def createNewTourney (self, event):
        # show the new tourney panel and Add/Cancel buttons
        print('Create new tourney')
        self.hideEditTourney()
        self.showWidget(self.newTourneyPanel)
        #switch out manage panel instructions
        # self.hideCreateButtons()
        # self.showAddButtons()
    def editExistingTourney(self, event ):
        print('Edit existing tourney')
        self.hideCreateTourney()
        self.showEditTourney()
    def enterResults(self, event):
        print('Enter results')
    def addTourney (self):
        # build a new Tourney and add it to the data base
        # and reshow
        # validate the inputs
        # either the addTourney button is pressed or is called from keyboard input
        if not self.validateEntryField('number', self.newTourneyNumberEntry.get(), self.newTourneyNumberEntry):
            self.newTourneyNumberEntry.force_focus()
            return
        elif not self.validateEntryField('date', self.newTourneyDateEntry.get(), self.newTourneyDateEntry):
            self.newTourneyDateEntry.force_focus()
            return
        try:
            print ('Try new tourney add')
            Tourney(TourneyNumber = int(self.newTourneyNumber.get()),
                    Date = self.makeIsoDate(self.newTourneyDate.get()),
                    Club = cfg.clubRecord, Season = cfg.season
                    )
            self.populateExistingTourneys()
            self.tourneyDate.set('')
            self.newTourneyDate.set('')
            self.newTourneyNumber.set('')
            self.hideWidget(self.newTourneyPanel)
            self.showWidget(self.manageTourneyPanel)
            self.showCreateButtons()
        except dberrors.DuplicateEntryError:
            print('Duplicate tourney date')
            self.errorHiLite(self.newTourneyDateEntry)
            self.errorHiLite(self.newTourneyNumberEntry)
            # leave date there and offer edit or cancel
##            self.hideWidget(self.addTourney)    # hide button
##            self.showWidget(self.editTourney)  # show button

            if mbx.askretrycancel('Duplicate number or date','Retry/edit or Cancel',parent = self):
                # set focus and let user retry the date
                self.newTourneyNumberEntry.focus_force()
            else:
                # clear out entry fields
                self.resetErrorHiLite(self.newTourneyDateEntry)
                self.resetErrorHiLite((self.newTourneyNumberEntry))
                self.tourneyDate.set('')
    def makeIsoDate(self, USDate):
        # take date in US format and turn into ISO8601 format
        # date format aleadys validate by validateNewTrouneyDate
        mon, day, yr = USDate.split(sep = '/')
        return (yr + '-' + mon + '-' + day)
    def makeUSDate(self, ISODate):
        # presumes the incoming ISODate is valid
        return  ISODate.strftime('%m/%d/%Y')

    def validateNewTourneyNumber(self, value, w):
        print ('Number value: ', value)
        self.resetErrorHiLite(w)
        if not value.isnumeric():
            print ('Not numeric')
            self.errorHiLite(w)
            return False
        if int(value) < 1 or int(value) > 45:
            print ('Out of range')
            self.errorHiLite(w)
            return False
        return True
    def validateNewTourneyDate(self, value,w):
        print ('Date value: ', value)
        self.resetErrorHiLite(w)
        # first check for apparent format
        if value.count('/') != 2:
            self.errorHiLite(w)
            return False
        month, day, year = value.split(sep='/')
        if not month.isnumeric() or not day.isnumeric() or not year.isnumeric():
            self.errorHiLite(w)
            return False
        imonth = int(month)
        iday = int(day)
        iyear = int(year)
        print ('m / d / y: ', month, day, year)
        try:
            newDate = datetime.date(iyear, imonth, iday)
            return True
        except ValueError:
            self.errorHiLite(w)
            return False
        return True
    def ValidTourneyDate(self, value):
        # validates a US format date mm/dd/yyyy
        # return True if the date user has selected is not valid/doesn't exist
        if value.count('/') != 2:
            return False
        month, day,  year = value.split(sep='/')
        if not month.isnumeric()  or not day.isnumeric() or not year.isnumeric():
            return False
        imonth = int(month)
        iday = int(day)
        iyear = int(year)
        try:
            newDate = datetime.date(iyear, imonth, iday)
            return True
        except ValueError:
            return False
        return True
    def badTourneyForResults(self):
        # msg box and retry or cancel for missing tourney selection for results entry
        return mbx.askretrycancel('Invalid Tourney Date Selection',
                                  'Select a Tourney before using Right Arrow',
                                  icon=mbx.Error)
    def validateEntryField(self, field, input, w):
        # invokes appropriate validation field
        switcher = {
            'number': self.validateNewTourneyNumber,
            'date': self.validateNewTourneyDate
        }
        return switcher.get(field)(input, w)

    def setNumberEntryHandler(self, w):
        # pass in extra parameters to event handler
        def entryHandler(event, self = self, ):
            return self.numberInputValidation(event)
        w.bind('<KeyPress>', entryHandler)
    def setDateEntryHandler(self, w):
        # pass in extra parameters to event handler
        def entryHandler(event, self = self):
            return self.dateInputValidation(event)
        w.bind('<KeyPress>', entryHandler)
    def numberInputValidation(self, event):
        if event.keysym == 'Return' or event.keysym == 'Tab':
            # self.validateNewTourneyNumber(self.newTourneyNumberEntry.get())
            # advance to date input
            self.newTourneyDateEntry.focus_force()
    def dateInputValidation(self, event):
        if event.keysym == 'Return' or event.keysym == 'Tab':
            # self.validateNewTourneyDate(self.newTourneyDateEntry.get())
            self.addTourney()
    def cancelUpdate(self):
        # go back to starting status
        self.hideEditButtons()
        self.hideWidget(self.editTourneyPanel)
        self.showCreateButtons()
    def forgetIt(self, event):
        # forget Tourney update or delete
        self.tourneyDate.set('')
        self.newTourneyDate.focus_set()
        self.hideWidget(self.Cancel)
        self.hideWidget(self.updateTourney)
        self.hideWidget(self.deleteTourney)
        self.showWidget(self.addTourney)
    def editByDate(self, event):
        # this is activated by DoubleClick-1 :
        self.beingEdited = self.existingDates.curselection()[0]
        self.editSelectedTourney(self.beingEdited)
    def editByNumber(self, event):
        # this is activated by DoubleClick-1
        self.beingEdited = self.existingNumbers.curselection()[0]
        self.editSelectedTourney(self.beingEdited)
    def editSelectedTourney(self, event):
        # this is activated by F2
        self.listBoxIndex = event.widget.curselection()[0]
        print ('List box index:', self.listBoxIndex)
        # print('Tourney number: ',self.existingNumbers.get(listBoxIndex))
        # print('Tourney date: ', self.existingDates.get(listBoxIndex))
        self.showEditPanels(self.listOfListboxes[0].curselection())
        # capture record being edited.
        self.tourneyUnderEdit = self.dbmsSortedTourneys[self.listBoxIndex]
        print('tourney to edit', self.tourneyUnderEdit)
        # print('Tourney under edit: ', self.tourneyUnderEdit)
        # save original parameters in case user user cancels or forgets the edits
        self.editTourneyOriginalDate = self.tourneyUnderEdit.Date
        self.editTourneyOriginalNumber = self.tourneyUnderEdit.TourneyNumber
        # print(str(eval(self.existingTourneyNumbers.get())[self.listBoxIndex[0]]))
        # print(str(eval(self.existingTourneyValues.get())[self.listBoxIndex[0]]))
        # self.tourneyDate.set(eval(self.existingTourneyDates.get()))self.listBoxIndex[0]))
        self.hideWidget(self.newTourneyPanel)
        self.showEditPanel()
        # self.hideWidget(self.doubleClickToEdit)
        self.showWidget(self.updateTourneyButton)
        self.showWidget(self.deleteTourneyButton)
        self.showWidget(self.cancelUpdateButton)
        self.hideCreateButtons()

        # populate the existing selected tourney params
        self.editTourneyNumber.set(self.existingNumbers.get(listBoxIndex))
        self.editTourneyDate.set(self.existingDates.get(listBoxIndex))
        self.showWidget(self.editTourneyPanel)
    def updateTourney(self):
        # first validate the user's update input
        print ('In updateTourney')
        if not self.validateEntryField('number', self.editTourneyNumberEntry.get(),
                                       self.editTourneyNumberEntry):
            self.editTourneyNumberEntry.focus_force()
            return
        elif not self.validateEntryField('date', self.editTourneyDateEntry.get(),
                                          self.editTourneyDateEntry):
            self.editTourneDateEntry.focus_force()
            return
        # otherwise try to replace current tourney entry with new information

        try:
            print ('Try update')
            self.tourneyUnderEdit.set(TourneyNumber = int(self.editTourneyNumberEntry.get()),
                                      Date = self.makeIsoDate(self.editTourneyDateEntry.get()))
            self.tourneyUnderEdit.syncUpdate()
        except dberrors.DuplicateEntryError:
            self.showWidget(self.editTourneyEditError)
            self.showEditErrors()
            return


        # self.editingRecordId = self.getRecordId(self.editTourneyOriginalDate)
        # t = Tourney.get(self.editingRecordId)
        # t.set(Date=self.tourneyDate.get())
        self.populateExistingTourneys()
        self.hideWidget(self.editTourneyPanel)
        self.showWidget(self.manageTourneyPanel)
        self.showCreateButtons()
    def deleteTourney(self, event):
        # delete the current tourney
        print ('delete selected tourney')
        # TODO: should check we are not deletng a tourney for
        # which there are already results...this would be a
        # serious data integrity error.
        # self.dbmsSorterTourneys corresponds to listbox entries
        # self.beingEdited
        print ('Request to delete a tourney')
        # print ('Request to delete tourney: ', self.dbmsSortedTourneys[self.beingEdited])
        # Tourney.delete(self.dbmsSortedTourneys[self.beingEdited].id)
        # reshow the list after the deletion
        self.populateExistingTourneys()
        self.showCreateTourney()
    def getRecordId (self, date):
        print (date)
        t = Tourney.select(Tourney.q.Date == date)
        l = list(t)
        print (l)
        print (l[0].id)
        return l[0].id
    def showCreateTourney(self):
        # self.hideEditButtons()
        self.hideEditTourney()
        self.showCreatePanels()
    def showCreatePanels(self):
        self.showWidget(self.newTourneyPanel)
        self.showWidget(self.newInstructionsPanel)
    def showEditTourney(self):
        self.hideCreateTourney()
        self.showEditPanels()
    def showEditPanels(self, index):
        print ('lb index to edit', index)
        self.showWidget(self.editInstructionsPanel)
        self.showWidget(self.existingTourneyPanel)
        self.showWidget(self.editTourneyPanel)
    def hideCreateTourney(self):
        self.hideWidget(self.newTourneyPanel)
        self.hideWidget((self.newInstructionsPanel))
    def hideEditTourney(self):
        self.hideWidget(self.editInstructionsPanel)
        self.hideWidget(self.existingTourneyPanel)
        self.hideWidget(self.editTourneyPanel)
    def hideWidget(self, w):
        w.grid_remove()
    def showWidget(self, w):
        w.grid()
    def errorHiLite(self, w):
        # print ('Entry config: ', w.config())
        w.config(background = 'red', foreground = 'white')
    def resetErrorHiLite(selfself, w):
        w.config(background = 'white', foreground = 'black')

    def redText(self, w):
        w.config(foreground='red')

    def blackText(self, w):
        w.config(foreground='black')

