import tkinter as tk
from tkinter import ttk
from tkinter import font
import numpy

class GuiTestapp(tk.LabelFrame):
	def __init__ (self,parent):
		super().__init__(parent)
		# self.grid(row=0, column=0, sticky = 'nsew')
		self.grid(sticky='nsew')
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		# self.text = 'Test Root Master'
		# self.underlineFont = font.Font(underline=1)
		# self.label = ttk.Label(parent,
        #                        text='Hello')
		# self.label.configure(font=self.underlineFont)
		# self.label.pack()
		s = ttk.Style()

		s.configure('aquabutton.TButton',
		            background = 'aqua',
		            highlightbackground = 'green',
		            highlightcolor = 'red',
		            highlightthickness = '2cm')

		# self.aButton = ttk.Button(self, text='aButton', style = 'aquabutton.TButton')
		# self.aButton.grid(row=1, column=0, sticky = 'nsew')
		# self.aButton.grid(row=1, column=0,)

		# s = ttk.Style()
		# s.configure('blueframe.TLabelframe', background = 'blue',
		#             highlightbackground = 'green',
		#             highlightcolor = 'red',
		#             highlightthickness = '5m')
		# self.labelFrame = ttk.LabelFrame(self, text = 'Blue Frame', borderwidth = '0',
		#                                  height = '100', width='200',
		#                                  style='blueframe.TLabelframe')
		# self.labelFrame.grid(row=0, column=0, sticky = 'nsew')
		# self.labelFrame.rowconfigure(0, weight=1)
		# self.labelFrame.columnconfigure(0, weight=1)
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
		self.outerFrame = tk.Frame(self,
		                           bd = '2',
		                           bg = 'red',
		                           relief = 'raised',
		                           padx = 2,
		                           pady = 2)
		self.outerFrame.grid(row = 0, column = 0, sticky='nsew')
		self.outerFrame.rowconfigure(0, weight = 1)
		self.outerFrame.columnconfigure(0, weight = 1)

		self.innerFrame = tk.Frame(self.outerFrame,
		                           bd = '5',
		                           bg = 'lawn green',
		                           relief = 'raised',
		                           # highlightthickness = '10',
		                           padx = 2,
		                           pady = 2)
		self.innerFrame.grid(row = 0, column = 0, sticky='nsew')
		self.innerFrame.rowconfigure(0, weight = 1)
		self.innerFrame.rowconfigure(1, weight=1)
		self.innerFrame.columnconfigure(0, weight = 1)

		# self.bButton = tk.Button(self.innerFrame,
		#                          activebackground = 'aqua',
		#                          activeforeground = 'green',
		#                          background = 'grey',
		#                          foreground = 'light blue',
		#                          text='bButton',
		#                          bd = '5',
		#                          highlightbackground = 'yellow',
		#                          highlightcolor = 'red',
		#                          highlightthickness = '1m',
		#                          takefocus = 1)
		# self.bButton.grid(row = 1, column = 0, sticky='nsew')
		#
		# self.cButton = tk.Button(self.innerFrame,
		#                          activebackground = 'aqua',
		#                          activeforeground = 'green',
		#                          background = 'grey',
		#                          foreground = 'light blue',
		#                          text='cButton',
		#                          bd = '1',
		#                          highlightbackground = 'yellow',
		#                          highlightcolor = 'red',
		#                          highlightthickness = '1',
		#                          takefocus = 1)
		# self.cButton.grid(row = 0, column = 0, sticky='nsew')
if __name__ == '__main__':
	root = tk.Tk()
	root.resizable(True, True)
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)
	app = GuiTestapp(root)
	app.mainloop()
