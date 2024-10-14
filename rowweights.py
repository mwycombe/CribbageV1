# columnwweights.py
# 7/22/2020
# sets equal weight to the number of columns requests for a widget
#
class RowWeights ():
	@classmethod
	def rowWeights(cls, widget, howmany):
		for row in range(0, howmany):
			widget.rowconfigure(row, weight=1)
