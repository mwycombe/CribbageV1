# updownmultilistbox.py
# 7/24/2020
#
# incorporates vsb to propagate scrolling across lists
#

import tkinter as tk


class Example(object):
	def __init__(self):
		self.root = tk.Tk()
		self.listOfListboxes = []
		# self.active_lb = None
		self.vsb = tk.Scrollbar(orient='vertical', command=self.OnVsb)
		self.vsb.pack(side='right', fill='y')

		self.lb1 = tk.Listbox(self.root, exportselection=0,
		                      selectmode= tk.SINGLE, yscrollcommand=self.vsb_set)
		self.lb2 = tk.Listbox(self.root, exportselection=0,
		                      selectmode=tk.SINGLE, yscrollcommand=self.vsb_set)
		self.lb3 = tk.Listbox(self.root, exportselection=0,
		                      selectmode=tk.SINGLE, yscrollcommand=self.vsb_set)

		self.listOfListboxes.append(self.lb1)
		self.listOfListboxes.append(self.lb2)
		self.listOfListboxes.append(self.lb3)

		for i in range(30):
			self.lb1.insert("end", "lb1 Item #%s" % i)
			self.lb2.insert("end", "lb2 Item #%s" % i)
			self.lb3.insert("end", "lb3 Item #%s" % i)

		self.lb1.pack(side="left", fill="both", expand=True)
		self.lb2.pack(side="left", fill="both", expand=True)
		self.lb3.pack(side="left", fill="both", expand=True)

		for lb in self.listOfListboxes:
			lb.bind('<<ListboxSelect>>', self.handle_select)

		for lb in self.listOfListboxes:
			lb.selection_set(0)
			lb.activate(0)
		self.listOfListboxes[0].focus_force()

	def start(self):
		self.root.title('updownmultilistbox')
		self.root.mainloop()

	def OnVsb(self, *args):
		for lb in self.listOfListboxes:
			lb.yview(*args)

	def vsb_set(self, *args):
		print ('vsb_set args: ', *args)
		self.vsb.set(*args)
		for lb in self.listOfListboxes:
			lb.yview_moveto(args[0])


	def handle_select(self, event):
		# set evey list to the same selection
		print ('select handler: ', event, event.widget.curselection())
		# self.active_lb = event.widget
		for lb in self.listOfListboxes:
			if lb != event.widget:
				lb.selection_clear(0, 'end')    # have to avoid this for the current widget
				lb.selection_set(event.widget.curselection())
				lb.activate(event.widget.curselection())
if __name__ == "__main__":
	Example().start()
