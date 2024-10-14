# Tourney.py
# sqlobject spec

from sqlobject import *
from sqlobject.sqlite import builder; SQLiteConnection = builder()

class Tourney(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
    TourneyNumber = IntCol(default = None)
    Date = DateCol()
    Club = ForeignKey('Club')
    Season = StringCol()
    Entered = StringCol(default = None)
