#####################################################
#                                                   #
#   guimixin.py                                     #
#                                                   #
# A mixin class for other frames: common methods    #
# the provide abstracted facade to other tkinter    #
# and ttk wdigets and functions.                    #
# Can also be used to set up common ttk styles      #
#                                                   #
# Also, insulates our programs from any future      #
# to standard dialogs and widgets.                  #
#                                                   #
#####################################################

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg
import sys
import os
class GuiMixin:
	def infobox(self, title, text, *args):
		return mbx.showinfo(title, text)
	def errorbox(self, text):
		mbx.showerror('Error!', text)
	def question(self,title, text, *args):
		return mbx.askyesno(title, text)
	def notdone(self):
		mbx.showerror('Not implemented', 'Option no available')
	def quit(self):
		ans = self.question('Verfiy quit', 'Are you sure you want to quit?')
		if ans == 1:
			tk.Frame.quit(self)    # Note: quit not recursive
	def help(self):
		self.infobox('RTFM', 'See instructions in read.me')
	def selectOpenFile(self, file='', dir = '.'):   # use std dialogs
		return fdg.askopenfilename(initialfile=file, initialdir=dir)
	def selectSaveFile(self, file='', dir='.'):
		return fdb.asksaveasfilename(initialfile=file, initialdir=dir)

if __name__ == '__main__':
	class TestMixin (GuiMixin, tk.Frame):
		def __init__(self, parent=None):
			tk.Frame.__init__(self, parent)
			self.pack()
			ttk.Button(self, text='quit', command=self.quit).pack(fill=tk.X)
			ttk.Button(self, text='help', command=self.help).pack(fill=tk.X)
	TestMixin().mainloop()
