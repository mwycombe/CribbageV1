# from tkinter import *
# from tkinter.ttk import *


# this code snippet applies that same rollover behavior to both ttk.Buttons
# also, style is only available as ttk.Style - not present in tk

import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.geometry('500x500')

style = ttk.Style()
style.configure('TButton', font =
			('calibri', 20, 'bold'),
                foreground = 'cyan',
                background = 'grey',
					borderwidth = '4')

# Changes will be reflected
# by the movement of mouse.
style.map('TButton', foreground = [('active', '!disabled', 'green')],
					background = [('active', 'yellow')])

# button 1
btn1 = ttk.Button(root, text = 'Quit !', command = root.destroy)
btn1.grid(row = 0, column = 3, padx = 100)

# button 2
btn2 = ttk.Button(root, text = 'Click me !', command = None)
btn2.grid(row = 1, column = 3, pady = 10, padx = 100)

root.mainloop()
