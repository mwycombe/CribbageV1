# cribbagestyles.py
# 7/20/2020 repositry for all custom styles for cribbage UI
#

from tkinter import ttk

# frame styles
class CribbageStyles():
	def __init__(self):
# this creates all of the styles the UI can use
		s = ttk.Style()
# [frame styles]
		s.configure('blueframe.TFrame',
		            borderwidth = '5',
		            highlightbackground = 'blue'
		            )