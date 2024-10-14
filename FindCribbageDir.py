#FindCribbageDir.py
#############################################################
#                                                           #
# Checks for local Cribbage.cfg file and then to see if     #
# it can find the referenced local directory                #
#                                                           #
#############################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg
import sys
import os

class FindCribbageDir (tk.Frame):
    # this frame will be imported into CribbageStartUp
    # it provides the panel for locating the cfg directory
    # it will set the instance variabes for curDir and curFile
    # to the values to be used for running the larger app.


    #############################################
    # these will eventually be pushed to global #
    # as every module and panel will need access#
    # to them once they have been filled in by  #
    # the initial set-up panels.                #
    #############################################
    
    baseDir = ''
    baseFile = ''
    baseDBMS = ''
    
#************************************************************
    def __init__ (self, parent=None):
        tk.Frame.__init__(self,parent)
        self.grid()
        self.filePanel = ttk.LabelFrame(self, relief='raised', text='Locate Directory',
                   height = '3c', width = '12c',
                    border = '8m')
        self.filePanel.grid_propagate(0)
        self.makeFilePanelWidgets(self.filePanel)
        self.filePanel.grid()
        self.readCFG()
#************************************************************
    def makeFilePanelWidgets(self,parent):
        self.w00 = ttk.Label(parent,text='Using Directory')
        self.w00.grid(row=0, column=0)
        self.w01 = ttk.Label(parent,text='<directory>')
        self.w01.grid(row=0,column=1)
        self.w10 = ttk.Label(parent,text='Database Directory')
        self.w10.grid(row=1, column=0)
        self.w20 = ttk.Label(parent,text='Not Found')
        self.w20.grid(row=2, column=0)
        self.w11 = ttk.Label(parent,text='Please Enter a')
        self.w11.grid(row=1, column=1)
        self.w21 = ttk.Label(parent,text='Valid Directory')
        self.w21.grid(row=2, column=1)
        self.w12 = ttk.Entry(parent)
        self.w12.grid(row=1, column=3)
        self.w22 = ttk.Label(parent,text="      E.g. c:/cribbage/senior.data/")
        self.w22.grid(row=2, column=3)    
#************************************************************

    def readCFG(self):          # locate cribbage.cfg file
        try:
            file = open('cribbage.cfg')

        except FileNotFoundError:
            self.w00.grid_remove()
            self.w01.grid_remove()
            self.w10.config(foreground='red')
            self.w20.config(foreground='red')
if __name__ == '__main__':
    root = tk.Tk()
    fcd = FindCribbageDir(root)
# we can also put actions in here - but they will only happen
# during cmd unit test.
    root.mainloop()
# This does't happen until app is close
# print ('afterMainLoop')
# So, everything has to happen inside the GUI code
    

    
