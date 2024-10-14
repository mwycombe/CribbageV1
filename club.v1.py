# oldclub.v1.py
# obsolete as of 7/20/2020
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
