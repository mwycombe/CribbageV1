# stretchListbox.py
# 8/7/2020

import tkinter as tk
import os, sys

class StretchListbox(tk.Frame):
	def __init__ (self, parent):
		super().__init__(parent)
		# parent.grid(sticky='nsew')  # this is rejected

		self.grid(sticky='nsew')
		self.rowconfigure(0, weight=1)      # this is key to having contents stretch with the parent frame
		self.columnconfigure(0, weight=1)   # this is key to having contents stretch with the parent frame
		self.container = tk.LabelFrame(self,
		                               text='Container')
		self.container.grid(sticky='nsew')
		self.container.rowconfigure(0, weight=1)
		self.container.columnconfigure(0, weight=1)

		self.vsb = tk.Scrollbar(self.container, orient='vertical')

		self.lb1 = tk.Listbox(self.container,
		                      yscrollcommand=self.vsb.set)
		self.vsb.grid(row=0, column=1, stick='ns')
		self.lb1.grid(row=0, column=0, sticky='nsew')
		self.lb1.grid_propagate(True)


		self.vsb['command'] = self.lb1.yview
		for i in range(30):
			self.lb1.insert('end', 'lb1 Item #%s' % i)


if __name__ == '__main__':
	root = tk.Tk()
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	app=StretchListbox(root)
	app.mainloop()