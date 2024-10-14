# verticalscrolledcanvasframe.py
# 2019-12-13
# cloned from verticalscrolledframe in resultspanel2.py
#
#############################################################
#   provide a stand-alone class that accepts input from the
#   outside to drop widgets into the interior frame.
#   Design strategy is to provide a scrolled series of
#   self-contained frames encapsulated by the interior frame
#   with access and navigation methods to search the object
#   within the frames.
#   Widgets inside the interior frame may require methods
#   that permit them to be styled.
#   also, permit styling keywords to be provided if necessarty
#   to condition the interior frame.
#############################################################

import tkinter as tk
from tkinter import ttk

class verticalscrolledcanvasframe(ttk.Frame):
	def __init__(self,parent):
		super().__init__.parent

		# create with a canvas object and a vertical scrollbar
		self.vsb = ttk.Scrollbar(self, orient=tk.VERTICAL)
		self.vsb.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.TRUE)
		self.canvas = tk.CAnvas(self, bd=0, highlightthickness=0)