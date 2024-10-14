import tkinter as tk
from tkinter import ttk
from tkinter import font
import numpy

class Testapp(ttk.LabelFrame):
	def __init__ (self,parent):
		super().__init__(parent)
		# self.grid(row=0, column=0, sticky = 'nsew')
		self.grid(stick='nsew')
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		# self.text = 'Test Root Master'
		# self.underlineFont = font.Font(underline=1)
		# self.label = ttk.Label(parent,
        #                        text='Hello')
		# self.label.configure(font=self.underlineFont)
		# self.label.pack()
		self.aButton = ttk.Button(self, text='aButton')
		self.aButton.grid(row=1, column=0, sticky = 'nsew')
		# self.aButton.grid(row=1, column=0,)

		s = ttk.Style()
		s.configure('blueframe.TLabelframe', background = 'blue')
		self.labelFrame = ttk.LabelFrame(self, text = 'Blue Frame', borderwidth = '0',
		                                 height = '100', width='200',
		                                 style='blueframe.TLabelframe')
		self.labelFrame.grid(row=0, column=0, sticky = 'nsew')
		self.labelFrame.rowconfigure(0, weight=1)
		self.labelFrame.columnconfigure(0, weight=1)
		# self.labelFrame.grid(row=0, column=0)

		# s = ttk.Style()
		# s.configure ('Blueframe.TLabelframe',
		#                  # highlightbackground = 'blue',
		#                  background = 'blue',
		#                  borderwidth = '5')
		# self.aFrame = ttk.LabelFrame(self, style='Blueframe.TLabelframe',
		#                              text='Blue Frame')
		# # self.aFrame.text = 'Blue Frame'
		# self.aFrame.grid(row=0, column=0)

		# self.aFrame = ttk.Frame(self)
if __name__ == '__main__':
	root = tk.Tk()
	root.resizable(True, True)
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)
	app = Testapp(root)
	app.mainloop()
