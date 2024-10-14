#ormpractice.py
#####################################################   
#                                                   #
# do some practice with sqlobject on sqlite         #
# for seniors.sqlite3 dbms which has been created   #
# via SQLite Studio                                 #
#                                                   #
#####################################################
#
# Use this to try out various orm constructs to
# see how things work
#
#

from sqlobject import *
from sqlobject.sqlite import builder; SQLiteConnection = builder()
import os
import sys
from Club import Club
from Game import Game
from Player import Player
from ScoreCard import ScoreCard
from Tourney import Tourney


baseDir = 'c:/cribbage/PYGR5/dbms/'
baseDbms = '/PracticeSeniors.sqlite3'
baseDbmsFile = '/'+baseDir + baseDbms
connection_string = 'sqlite:' + baseDbmsFile

print (connection_string)


conn = connectionForURI(connection_string)
sqlhub.processConnection = conn

##class Club(SQLObject):
##    _connection = conn
##    class sqlmeta:
##        style = MixedCaseStyle(longID=True)
##    Director = StringCol(length=40,varchar=True)
##    Location = StringCol(length=50,varchar=True)






##    Contact = StringCol(length=40,varchar=True)
##    ClubNumber = IntCol()
##    ClubName = StringCol(length=40,varchar=True)
##
##class Game(SQLObject):
##    _connection = conn
##    class sqlmeta:
##        style = MixedCaseStyle(longID=True)
##    ScoreCard = ForeignKey('ScoreCard')
##    GamePoints = IntCol()
##    OpponentSeat = StringCol(length=4)
##
##class Player(SQLObject):
##    _connection = conn
##    class sqlmeta:
##        style = MixedCaseStyle(longID=True)
##    PlayerName = StringCol(length=30,varchar=True)
##    Phone = StringCol(length=15,varchar=True)
##    Email = StringCol(length=45,varchar=True)
##    Club = ForeignKey('Club')
##    ACCNumber = StringCol(length=10)
##    Joined = DateCol()
##
##class ScoreCard(SQLObject):
##    _connection = conn
##    class sqlmeta:
##        style = MixedCaseStyle(longID=True)
##    Tourney = ForeignKey('Tourney')
##    Player = ForeignKey('Player')
##    SeatNumber = StringCol(length=4)
##
##class Tourney(SQLObject):
##    _connection = conn
##    class sqlmeta:
##        style = MixedCaseStyle(longID=True)
##    Date = DateCol()
##    Club = ForeignKey('Club')

#***********************************************
## Uncomment any of these to empty and then
## recreate one of the tables should they
## become polluted or corrupted
#***********************************************

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

#****************************************
#
# Everytime this is run, it creates yet
# another player and yet another club.
# Each has the next higher id as there
# is no duplicate checking - yet...
#
#****************************************

club = Club( Director = 'Michael Rogers',
            Location = 'Napa Moose Lodge',
            Contact = 'mlr94549@yahoo.com',
            ClubNumber = 100,
            ClubName = 'Century Peggers')

player = Player(PlayerName = 'Michael Rogers',
                Phone = '510-504-6905',
                Email = 'mlr94549@yahoo.com',
                Club = 1,
                ACCNumber = 'CA6999',
                Joined = '2014-07-24')
