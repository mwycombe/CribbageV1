# columnwweights.py
# 7/22/2020
# sets equal weight to the number of columns requests for a widget
#
class ColumnWeights ():
	@classmethod
	def columnWeights(cls, widget, howmany):
		for col in range(0, howmany):
			widget.columnconfigure(col, weight=1)
