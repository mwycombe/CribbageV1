# normalizeplayernames.py
# 2/4/2020
# Changes all player names and cities to titled words.
#

from sqlobject import *
from player import Player
from accessPlayers import AccessPlayers
from club import Club

from tso import *

club999 = ''
cstring = ''
conn = ''
ap = ''
at = ''
ar = ''

class NormalizePlayerNames (object):
	def __init__(self):
		club999 = Club.get(1)
		print ('Club999: ', club999)
		ap = AccessPlayers
		print ('ap: ', ap)
		self.allPlayers = ap.allPlayers(club999)
		print ('Player count: ', len(self.allPlayers))
		for p in self.allPlayers:
			print ('FirstName: ', p.FirstName, ' LastName: ', p.LastName, ' City: ', p.City)
			FN = p.FirstName
			LN = p.LastName
			CY = p.City
			p.set(FirstName = FN.title(), LastName = LN.title(), City = CY.title())
			print ('FirstName: ', p.FirstName, ' LastName: ', p.LastName, ' City: ', p.City)

if __name__ == '__main__':
	dbms = TSO()
	names = NormalizePlayerNames()
