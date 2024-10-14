# club.py
# 7/20/2020 cloned from club.v1.py
# sqlobject class

from sqlobject import *
from sqlobject.sqlite import builder; SQLiteConnection = builder()

class Club(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
    director = StringCol(length=40,varchar=True)
    location = StringCol(length=50,varchar=True)
    contact = StringCol(length=40,varchar=True)
    clubNumber = IntCol()
    clubName = StringCol(length=40,varchar=True)
    reportDirectory = StringCol(length=40,varchar=True)
