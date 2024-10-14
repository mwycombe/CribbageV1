# ManageTourneys.py
##########################################################
#
# Manage list of touryeys
#
# Add/change/delete tourneys
# 
###########################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg
from sqlobject import *
from Club import Club
from Tourney import Tourney
import sys
import os

class ManageTourneys (ttk.Frame):
    #
    # This class is istelf a ttk Frame
    #

#************************************************************
#
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid()
        print ('ManageTourneys started . . .')
        #####################################################
        #
        # control variables for gui
        #
        self.tourneyDate = tk.StringVar()
        self.existingTourneyValues = tk.StringVar()
        
        #
        # set up club we are going to use - only one at this time
        #
                
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
        # set up tournament panel
        #
        self.tourneyPanel = ttk.LabelFrame(self,
                                           height='10c',
                                           width='10c',
                                           borderwidth='15p',
                                           relief='sunken',
                                           text = 'Tournaments'
                                           )
        self.tourneyPanel.grid(row = 1, column = 0, sticky = 'nsew')

        # tourney panel row 0
        
        self.newTourneyLabel = ttk.Label(self.tourneyPanel,
                                         text = 'New Tourney Date:  ')
        self.newTourneyLabel.grid(row=0, column=0)
        self.newTourneyDate = ttk.Entry(self.tourneyPanel,
                                        textvariable = self.tourneyDate)
        self.newTourneyDate.bind('<KeyPress-Escape>', self.forgetIt)
        self.newTourneyDate.grid(row = 0, column = 1)
        
        #
        # tourney panel row 1
        #
        
        self.addTourney = ttk.Button(self.tourneyPanel,
                                    text = 'Add New Tourney',
                                    command=self.addNewTourney
                                    )
        self.addTourney.grid(row=1, column=0)
        self.updateTourney = ttk.Button(self.tourneyPanel,
                                     text = 'Update Tourney',
                                     command=self.updateTourney
                                     )
        self.updateTourney.grid(row=1, column=1)
        self.hideWidget(self.updateTourney)

        
 
        # tourney panel row 2 - spacer
        
        ttk.Label(self.tourneyPanel,text=' ').grid(row=2,column=0)
        self.deleteTourney = ttk.Button(self.tourneyPanel,
                                        text='Delete Tourney',
                                        command=self.deleteTourney
                                        )
        self.deleteTourney.grid(row=2, column=1)
        self.hideWidget(self.deleteTourney)
        self.Cancel = ttk.Label(self.tourneyPanel,
                                text='Hit Esc to Cancel')
        self.Cancel.grid(row=3, column=0)
        self.Cancel.grid_remove()   # hide for now
        
        # tourney panel row 3
        
        self.doubleClickLabel = ttk.Label(self.tourneyPanel,
                  text='Double Click a Date to Take Action On')
        self.doubleClickLabel.grid(row=3, column=1)


        # tourney panel row 4
        #
        # show past tourneys - arbitrarily show 12 - no scroll bar for now
        #
        self.existingTourneysLabel = ttk.Label(self.tourneyPanel,
                                          text = 'Existing Tourneys:   ')
        self.existingTourneysLabel.grid(row=4, column=0, sticky = 'n')
        self.existingTourneys = tk.Listbox(self.tourneyPanel,
                                       listvariable=self.existingTourneyValues)
        self.existingTourneys.grid(row=4, column=1)
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

            if mbx.askretrycancel('Change Date?','Edit date or cancel',parent = self.tourneyPanel):
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
    mp = ManageTourneys(root)
    root.mainloop()

        
