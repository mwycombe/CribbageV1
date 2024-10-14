# ScoreCard.py
# sqlojbect class
# update 9/10/2019

from sqlobject import *
from sqlobject.sqlite import builder; SQLiteConnection = builder()

class ScoreCard(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
    Tourney = ForeignKey('Tourney')
    Player = ForeignKey('Player')
    
    GamePoints = IntCol()
    GamesWon = IntCol()
    Spread = IntCol()
    Cash = IntCol()
    SkunksTaken = IntCol()
    SkunksGiven = IntCol()
    EntryOrder  = IntCol()
