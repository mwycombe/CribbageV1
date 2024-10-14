#PhoneNumber.py sample code
#
# from https://developer.ibm.com/articles/os-pythonsqlo/
# with specific sample code for various uses of SQLObject
#

import sqlobject
from Connection import conn


class PhoneNumber(sqlobject.SQLObject):
    _connection = conn
    number = sqlobject.StringCol(length=14, unique=True)
# this is how we specify ForeignKey    
    owner = sqlobject.ForeignKey('Person')
    lastCall = sqlobject.DateTimeCol(default=None)


class Person(sqlobject.SQLObject):
    _idName='fooID'
    _connection = conn
    name = sqlobject.StringCol(length=255)
    #The SQLObject‑defined name for the "owner" field of PhoneNumber
    #is "owner_id" since it's a reference to another table's primary
    #key.
    numbers = sqlobject.MultipleJoin('PhoneNumber', joinColumn='owner_id')


Person.createTable(ifNotExists=True)
PhoneNumber.createTable(ifNotExists=True)
