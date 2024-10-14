# Game.py
# sqlobject class

from sqlobject import *
from sqlobject.sqlite import builder; SQLiteConnection = builder()

class Game(SQLObject):

    class sqlmeta:
        style = MixedCaseStyle(longID=True)
    ScoreCardID = ForeignKey('ScoreCard')
    GamePoints = IntCol()
    Spread = IntCol()
    OpponentSeat = StringCol(length=4)
    CutCard = StringCol(length=2)
