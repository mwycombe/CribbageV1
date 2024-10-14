#testDbmsQueries.py
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
from sqlobject import  *
import sys
import os
from tourney import Tourney
import dateparser
import datetime

from tourney import Tourney
from player import Player
from scorecard import ScoreCard

from accessTourneys import AccessTourneys
from accessPlayers import AccessPlayers
from accessResults import AccessResults

at = AccessTourneys()
ap = AccessPlayers()
ar = AccessResults()

startingDir = os.getcwd()
print (startingDir)

appTitle = ''
dbmsDirectory = ''
dbmsName = ''
season = ''

try:
    cfg = open('cribbage.cfg')
except FileNotFoundError:
    print ('Unable to locate cribbage.cfg\nTerminating')
    sys.exit(-1)
print ('Found file')
for line in cfg:
    print (line)
    eName = line.split(sep='=')[0].strip()
    eValue = line.split(sep='=')[1].strip()
    if eName == 'clubNumber':
        clubNumber = eValue
    elif eName == 'dbmsDirectory':
        dbmsDirectory = eValue
    elif eName == 'dbms':
        dbmsName = eValue
    elif eName == 'season':
        season = eValue

print (clubNumber + '\n' + dbmsDirectory + '\n' + dbmsName + '\n' + season + '\n')
print (startingDir)
# os.chdir(dbmsDirectory)
# print ('Now at ' + dbmsDirectory)

##
##  Add code to open the dbms that sh should be there
##  Then mangle the dmbsname to check handling of dbms not found.
##  and make sure we can create on we find the second time through
##



dbmsFile = dbmsDirectory + dbmsName
print (dbmsFile)
connection_string = 'sqlite:' + dbmsFile

conn = connectionForURI(connection_string)
sqlhub.processConnection = conn
print (connection_string + ' now opened')

##r = list(Tourney.select())
##print(r)
##print (len(r))
##s = [r[x].Date for x in range(len(r))]
##print (r)
##print (s)

# print (list(Tourney.select()))
# print (Tourney.get(2))
#
# print ( list( Tourney.select(Tourney.q.Date == '2019-12-08') ))
#

# all = Tourney.select(1)
# print (all)
# t = Tourney.select(Tourney.q.Date == '2019-05-02')
# print(t)
# print (list(t))

# print ( list(Tourney.select(Tourney.q.TourneyNumber == 19)))
# print ( list(Tourney.select(Tourney.q.Date == '2019-09-10')))
# print ( len(list(Tourney.select(AND(Tourney.q.TourneyNumber == 19, Tourney.q.Date == '2019-09-10')))))
# print ( len(list(Tourney.select(AND(Tourney.q.TourneyNumber == 19, Tourney.q.Date == '2020-02-11')))))
# isoDate = datetime.date(2019, 9, 10)
# # now try retrieving using the tourney record using the datetime.date object
# tourneyRecordList = Tourney.select(Tourney.q.Date == isoDate)
# print ( tourneyRecordList[0])
# if tourneyRecordList[0].Entered == '*':
#     print ('Date Entered')
#     print ("Unexpected error: ", sys.exc_info()[0])

# test out accessPlayers
# this works with Player.q.id refence to the foreign key
# scorecardlist = list(Player.select(ScoreCard.q.Player == Player.q.id))
# print (len(scorecardlist))
# print (scorecardlist)

# player = Player.get(3)      # this should be Alan Cadkin
# print (player)
# tourney = Tourney.get(2)
# print (tourney)
#
# scoreCard = list(ScoreCard.select(
#                             AND(ScoreCard.q.Player == player.id,
#                                 ScoreCard.q.Tourney == tourney.id)
#                 ))
# print (scoreCard)
# print (len(scoreCard))
results = sqlhub.processConnection.queryAll ("Select PlayerID, sum(cash) from ScoreCard where scorecard.TourneyID in (select tourney.tourneyID from tourney where season = '2019-20') group by playerid having sum(cash) > 0 order by sum(cash) desc")
# results = sqlhub.processConnection.queryAll ('Select * From player')
print (results)

cashsummary = ar.cashSummaryForPlayers('2019-20')
print (cashsummary)