# Tourney.py
# sqlobject spec

from sqlobject import *
from sqlobject.sqlite import builder; SQLiteConnection = builder()

class Tourney(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
    Date = DateCol()
    TourneyNumber = IntCol()
    Season = StringCol()
    Club = ForeignKey('Club')
