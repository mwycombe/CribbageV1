# simplelistbox.py
# 8/7/2020
# just explore a simple list box.
# this shows that just using the up/down arrows moves the line but does not auto-select
import tkinter as tk

class ListBox(tk.Frame):
	def __init__(self,parent):
		super().__init__(parent)
		self.grid(sticky='nsew')
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

		self.container = tk.Frame(self, relief='flat')
		self.container.grid(sticky='nsew')
		self.container.rowconfigure(0, weight=1)
		self.container.columnconfigure(0, weight=1)

		self.vsb = tk.Scrollbar(self.container)
		self.vsb.grid(row=0, column=1, sticky='nse')

		self.lb1 = tk.Listbox(self.container,
		                      exportselection=0, selectmode=tk.SINGLE,
		                      yscrollcommand=self.vsb.set)
		# self.selection = 0
		self.lb1.grid(row=0, column=0, sticky='nsew')
		self.vsb['comman'] = self.lb1.yview

		for i in range(1,31):
			self.lb1.insert('end', 'lb1 Item#%s' % i)
		self.lb1.selection_set(0)
		self.lb1.activate(0)

		# bind up/down arrows
		self.lb1.bind('<Down>', self.listBoxUpDown)
		self.lb1.bind('<Up>', self.listBoxUpDown)
		self.lb1.focus_force()
	def listBoxUpDown(self, event):
		selection = event.widget.curselection()[0]
		if event.keysym == 'Up':
			selection += -1
		if event.keysym == 'Down':
			selection += 1

		if 0 <= selection < event.widget.size():
			event.widget.selection_clear(0, tk.END)
			event.widget.selection_set(selection)

		# if self.selection < self.lb1.size()-1:
		# 	self.lb1.select_clear(self.selection)
		# 	self.selection += 1
		# 	self.lb1.select_set(self.selection)
	# def listBoxUp(self, event):
	# 	if self.selection > 0:
	# 		self.lb1.select_clear(self.selection)
	# 		self.selection -= 1
	# 		self.lb1.select_set(self.selection)

if __name__ == '__main__':
	root = tk.Tk()
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	app = ListBox(root)
	app.mainloop()
