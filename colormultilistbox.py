# colormultilistbox.py
# 7/24/2020
#
# incorporates vsb to propagate scrolling across lists
#

import tkinter as tk


class Example(tk.Frame):
	def __init__(self,parent):
		super().__init__(parent)
		self.grid(sticky='nsew')
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

		self.listOfListboxes = []
		# self.active_lb = None
		self.container = tk.Frame(self)

		self.container.grid(sticky='nsew')
		self.container.rowconfigure(0, weight=1)
		self.container.columnconfigure(0, weight=1)
		self.container.columnconfigure(1, weight=1)
		self.container.columnconfigure(2, weight=1)
		self.container.columnconfigure(3, weight=1)


		self.vsb = tk.Scrollbar(orient='vertical', command=self.OnVsb)
		# self.vsb.pack(side='right', fill='y') \
		self.vsb.grid(row=0, column=3, sticky='nsw')

		self.lb1 = tk.Listbox(self.container, exportselection=0,
		                      selectmode= tk.SINGLE, yscrollcommand=self.vsb_set)
		self.lb2 = tk.Listbox(self.container, exportselection=0,
		                      selectmode=tk.SINGLE, yscrollcommand=self.vsb_set)
		self.lb3 = tk.Listbox(self.container, exportselection=0,
		                      selectmode=tk.SINGLE, yscrollcommand=self.vsb_set)

		self.listOfListboxes.append(self.lb1)
		self.listOfListboxes.append(self.lb2)
		self.listOfListboxes.append(self.lb3)


		for i in range(30):
			self.lb1.insert("end", "lb1 Item #%s" % i)
			self.lb2.insert("end", "lb2 Item #%s" % i)
			self.lb3.insert("end", "lb3 Item #%s" % i)

		for lb in self.listOfListboxes:
			# print ('lb: ', lb)
			lb.itemconfig(5, background='blue', foreground='yellow')
			for i in range(lb.size()):
				lb.itemconfig(i, selectbackground= 'light green')

		self.lb1Label = tk.Label(self.container, text='ListBox1')
		self.lb2Label = tk.Label(self.container, text='ListBox2')
		self.lb3Label = tk.Label(self.container, text='ListBox3')

		self.lb1Label.grid(row=0, column=0, sticky='w')
		self.lb2Label.grid(row=0, column=1, sticky='w')
		self.lb3Label.grid(row=0, column=2, sticky='w')

		self.lb1.grid(row=1, column=0, sticky='nsew')
		self.lb2.grid(row=1, column=1, sticky='nsew')
		self.lb3.grid(row=1, column=2, sticky='nsew')

		for lb in self.listOfListboxes:
			lb.bind('<<ListboxSelect>>', self.handle_select)
			lb.bind('<Up>', self.upDownHandler)
			lb.bind('<Down>', self.upDownHandler)

		for lb in self.listOfListboxes:
			lb.selection_set(0)
			lb.activate(0)
		self.listOfListboxes[0].focus_force()

	def start(self):
		self.root.title('colormultilistbox')
		self.root.rowconfigure(0, weight=1)
		self.root.columnconfigure(0, weight=1)
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

	def upDownHandler(self, event):
		selection = event.widget.curselection()[0]
		if event.keysym == 'Up':
			selection += -1
		if event.keysym == 'Down':
			selection += 1

		if 0 <= selection < event.widget.size():
			for lb in self.listOfListboxes:
				lb.selection_clear(0, tk.END)
				lb.selection_set(selection)
if __name__ == "__main__":
	root = tk.Tk()
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	app=Example(root)
	app.mainloop()
