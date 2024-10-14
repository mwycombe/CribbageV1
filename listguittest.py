# listguitest.py
#


# System imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbx
from tkinter import filedialog as fdg

import sys as sys
import os as os
import numpy

class ListGuiTestapp(tk.LabelFrame):
	def __init__ (self,parent):
		super().__init__(parent)
		self.otherKey = 'Nothing'
		# self.grid(row=0, column=0, sticky = 'nsew')
		self.grid(sticky='nsew')
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		self.names = ['alpha, a', 'beta, b', 'beta, b', 'delta, d' , 'delta, d', 'gamma, g', 'gamma, g']
		self.existingnames = tk.StringVar()
		self.existingnames.set(self.names)

		self.enames = tk.Listbox(self,
		                         height = 4,
		                         relief = tk.GROOVE,
		                         activestyle = 'underline',
		                         listvariable = self.existingnames)
		self.enames.grid(row=0, column=0)

		self.scrollbar = tk.Scrollbar(self)
		self.scrollbar.grid(row=0, column=1, sticky='ns')
		self.enames.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.enames.yview)
		self.enames.selection_set(0)
		self.enames.focus_set()
		self.enames.activate(0)

		self.F2label = tk.Label(self,
		                        text = 'F2 pressed')
		self.F3label = tk.Label(self,
		                        text = 'F3 pressed')
		self.otherLabel = tk.Label(self,
		                           text = self.otherKey)
		self.F2label.grid(row = 1, column = 0)
		self.F3label.grid(row = 2, column = 0)
		self.otherLabel.grid(row = 3, column = 0)
		self.F2label.grid_remove()
		self.F3label.grid_remove()
		self.otherLabel.grid_remove()

		def F2Handler(event, self=self):
			return self.myF2Handler(event)
		self.enames.bind('<KeyPress-F2>', F2Handler)

		def F3Handler(event, self=self):
			return self.myF3Handler(event)
		self.enames.bind('<KeyPress-F3>', F3Handler)

		def otherKeyHandler(event, self=self):
			return self.myOtherKeyHandler(event)
		self.enames.bind('<Key>', otherKeyHandler)

	def myF2Handler(self, event):
		self.hideAll()
		self.F2label.grid()
	def myF3Handler(self, event):
		self.hideAll()
		self.F3label.grid()

	def myOtherKeyHandler(self, event):
		self.hideAll()
		self.otherKey = event.keysym
		self.otherLabel['text'] = self.otherKey
		print ('otherkey event: ',event, event.widget)
		self.otherLabel.grid()
	def hideAll(self):
		self.F2label.grid_remove()
		self.F3label.grid_remove()
		self.otherLabel.grid_remove()



	# 	s.configure('aquabutton.TButton')
		#             background = 'aqua',
		#             highlightbackground = 'green',
		#             highlightcolor = 'red',
		#             highlightthickness = '2cm')
		#
		# self.outerFrame = tk.Frame(self,
		#                            bd = '2',
		#                            bg = 'red',
		#                            relief = 'raised',
		#                            padx = 2,
		#                            pady = 2)
		# self.outerFrame.grid(row = 0, column = 0, sticky='nsew')
		# self.outerFrame.rowconfigure(0, weight = 1)
		# self.outerFrame.columnconfigure(0, weight = 1)
		#
		# self.innerFrame = tk.Frame(self.outerFrame,
		#                            bd = '5',
		#                            bg = 'lawn green',
		#                            relief = 'raised',
		#                            # highlightthickness = '10',
		#                            padx = 2,
		#                            pady = 2)
		# self.innerFrame.grid(row = 0, column = 0, sticky='nsew')
		# self.innerFrame.rowconfigure(0, weight = 1)
		# self.innerFrame.rowconfigure(1, weight=1)
		# self.innerFrame.columnconfigure(0, weight = 1)

if __name__ == '__main__':
	root = tk.Tk()
	root.resizable(True, True)
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)
	app = ListGuiTestapp(root)
	app.mainloop()
