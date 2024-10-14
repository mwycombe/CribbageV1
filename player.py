# player.py
# sqlobject class

from sqlobject import *
from sqlobject.sqlite import builder; SQLiteConnection = builder()

class Player(SQLObject):
    class sqlmeta:
        style = MixedCaseStyle(longID=True)
    FirstName = StringCol(length=20,varchar=True)
    LastName = StringCol(length=30,varchar=True)
    Street = StringCol(length=30,varchar=True, default=None)
    City = StringCol(length=20,varchar=True, default=None)
    State = StringCol(length=2, default= 'CA')
    Zip = StringCol(length=10, varchar=True, default='99999')
    Phone = StringCol(length=15,varchar=True, default=None)
    Email = StringCol(length=45,varchar=True, default=None)
    Club = ForeignKey('Club')
    ACCNumber = StringCol(length=10, default=None)
    ACCExpiration = DateCol (default=None)
    Active = IntCol(default=0)
    Joined = DateCol(default=None)

