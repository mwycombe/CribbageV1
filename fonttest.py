import tkinter as tk
from tkinter import ttk
from tkinter import font

class Application(tk.Frame):
	def __init__ (self, parent):
		self.underlineFont = font.Font(size=6, underline=1)
		self.label = ttk.Label(parent,
                               text='Hello',
		                       font = self.underlineFont)
#		self.label.configure(font=self.underlineFont)
		self.label.pack()
if __name__ == '__main__':
	root = tk.Tk()
	app = Application(root)
	root.mainloop()
