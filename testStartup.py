#testStartUP.py
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
import sys
import os



startingDir = os.getcwd()
print (startingDir)

appTitle = ''
dbmsDirectory = ''
dbmsName = ''
season = ''

try:
    cfg = open('Seniors.cfg')
except FileNotFoundError:
    print ('Unable to locate Seniors.cfg\nTerminating')
    sys.exit(-1)
print ('Found file')
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
        seasons = eValue

print (appTitle + '\n' + dbmsDirectory + '\n' + dbmsName + '\n' + season + '\n')
print (startingDir)
os.chdir(dbmsDirectory)
print ('Now at ' + dbmsDirectory)

##
##  Add code to open the dbms that sh should be there
##  Then mangle the dmbsname to check handling of dbms not found.
##  and make sure we can create on we find the second time through
##

from sqlobject import *

dbmsFile = dbmsDirectory + dbmsName
print (dbmsFile)
connection_string = 'sqlite:' + dbmsFile

conn = connectionForURI(connection_string)
sqlhub.processConnection = conn
print (connection_string + ' now opened')

