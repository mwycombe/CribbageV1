# player.py
# sqlobject class
# update 9/10/2019

from sqlobject import *
from sqlobject.sqlite import builder; SQLiteConnection = builder()

class Player(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
    FirstName = StringCol(length=20,varchar=True)
    LastName = StringCol(length=30,varchar=True)
    Street = StringCol(length=25,varchar=True, default=None)
    City = StringCol(length=20, varchar=True, default=None)
    Zip = IntCol()
    Phone = StringCol(length=15,varchar=True, default=None)
    Email = StringCol(length=45,varchar=True, default=None)
    Club = ForeignKey('Club')
    ACCNumber = StringCol(length=10, default=None)
    Joined = DateCol(default = None)
    Active=bool()
    ScoreCards = MultipleJoin('ScoreCard')
