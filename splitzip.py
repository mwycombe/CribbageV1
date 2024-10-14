# splitzip.py
# 2/6/2020
# split zip from State and put into zip column
#
from sqlobject import *
from player import Player
from club import Club

from tso import *

import os
import sys

cstring = ''
conn = ''
club999 = ''
at = ''
ar = ''
ap = ''

class SplitZip (object):
	def __init__(self):
		# get all players
		print (type(ap))
		self.allPlayers = ap.allPlayers(club999)
		for p in self.allPlayers:
			calzip = p.State
			cal, zip = calzip.split(sep=' ')
			print ('Calzip: ', calzip)
			print ('cal, zip', cal, zip)
			p.set(State=cal, Zip=zip)

if __name__ == '__main__':
	dbms = TSO()
	print ('Pegger dbms now open')
	club999 = Club.get(1)
	ap = AccessPlayers()
	splitzip = SplitZip()

