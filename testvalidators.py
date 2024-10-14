#testvalidators.py
import formencode
from formencode import validators
validator = validators.Int()

def get_integer():
    while 1:
        try :
            value = input('Enter a number: ')
            return validator.to_python(value)
        except formencode.Invalid as e:
            print (e)

get_integer()
