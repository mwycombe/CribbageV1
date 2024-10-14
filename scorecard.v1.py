# ScoreCard.py
# sqlojbect class

from sqlobject import *
from sqlobject.sqlite import builder; SQLiteConnection = builder()

class ScoreCard(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
    Tourney = ForeignKey('Tourney')
    Player = ForeignKey('Player')
    Cash = FloatCol()
    GamePoints = IntCol()
    GamesWon = IntCol()
    Spread = IntCol()
    Cash = FloatCol()
    SkunksTaken = IntCol()
    SkunksGiven = IntCol()

