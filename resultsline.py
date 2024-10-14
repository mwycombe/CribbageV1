# resultsline.py
# 8/10/2020
#
# results line struct for new resultstab
#
# resultstab will create an array of these for showing the tourney results
# when user hits F10 or F11 values will be propagated to the datebase
# of user hits Esc, everything will be dropped with no database updates
class resultsLine(object):
	playerId = ''           # id from database - used to key dictionary of entry line
	tourneyId = ''          # used when we switch back to tab after a non-commit
	playerName = ''         # last, first name
	playerGamePoints = 0    # tourney points
	playerGamesWon = 0      # tourney games won
	playerSpread = 0        # tourney spread (+ or - or zero)
	playerTaken = 0         # tourney skunks received by player
	playerCash = 0          # tourney dollars (excludes poker)
	playerGiven = 0         # tourney skunks given - computed
	playerEntryOrder = 0    # order in which cards were entered - for editing