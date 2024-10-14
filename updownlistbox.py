# updowlistbox.py
# 7/24/2020
#
import tkinter as tk


class Example(object):
	def __init__(self):
		self.root = tk.Tk()

		self.vsb = tk.Scrollbar(orient='vertical', command=self.OnVsb)
		self.vsb.pack(side='right', fill='y')

		# self.entry = tk.Entry(self.root)
		self.listbox = tk.Listbox(self.root, exportselection=False,
		                          yscrollcommand=self.vsb_set)
		for i in range(30):
			self.listbox.insert("end", "Item #%s" % i)

		# self.entry.pack(side="top", fill="x")
		self.listbox.pack(side="top", fill="both", expand=True)

		# self.listbox.bind("<Down>", self.handle_updown)
		# self.listbox.bind("<Up>", self.handle_updown)
		self.listbox.bind('<<ListboxSelect>>', self.handle_select)

		self.listbox.focus_force()
		self.listbox.selection_set(0)

	def OnVsb(self,*args):
		print ('OnVsb: ', *args)
		self.listbox.yview(*args)
		# need to also move the selection and active one

	def start(self):
		self.root.mainloop()
	# def handle_updown(self, event):
	# 	# per docs, -delta means scroll down; +delat means scroll up
	# 	self.delta = -1 if event.keysym == "Up" else 1
	# 	self.adjustSelection()
	# 	print('Up/down event: ', event)
	# 	return "break"
	# def adjustSelection(self):
	# 	curselection = self.listbox.curselection()
	# 	if len(curselection) == 0:      # zero length means no current selection tuple
	# 		index = 0
	# 	else:
	# 		index = max(int(curselection[0]) + self.delta, 0)
	#
	# 	self.listbox.selection_clear(0, "end")
	# 	self.listbox.selection_set(index)
	# 	self.listbox.activate(index)

	def handle_select(self, event):
		print ('Select event: ', event, event.widget.curselection())
	def vsb_set(self, *args):
		print ('vsb_set args: ', args)
		self.vsb.set(*args)

if __name__ == "__main__":
	Example().start()
