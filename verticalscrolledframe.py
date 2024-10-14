# verticalscrolledframe.py
# 12/16/2019
# cloned from resultpanel1.py where we did all of our testing

import tkinter as tk
from tkinter import ttk

# system imports
import os
import sys

class VerticalScrolledFrame (ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent):
        super().__init__(parent)

        # variables for controlling selecting players
        self.activeIndex = 0    # always start at the top of the player list
        self.topIndex = 0       # first frame line index
        self.bottomIndex = 0    # last viable frame index
        self.activeItem = 0     # tracks items in active frame
        self.topItem = 0        # first item in the active frame
        self.bottomItem = 0     # last viable item index
        self.minItem = 0        # minimum index for items within rframe line
        self.maxItem = 0        # maximum index for items with rframe line

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.TRUE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=self.vscrollbar.set)
        self.canvas.pack(side=tk.LEFT,  fill=tk.BOTH, expand=tk.TRUE)
        self.vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(self.canvas,
                                            borderwidth = '15',
                                            # bg = 'yellow',
                                            takefocus=1,
                                            highlightthickness = '1')
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior,
                                                    anchor=tk.NW)
        # let's try adding another overlay frame in a window to capture keystrokes
        # self.capture = tk.Frame(self.canvas,takefocus=1)
        # self.capture_id = self.canvas.create_window(0,0, window=self.capture,
        #                                             anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            print ('Interior event: ', event, event.widget)
            print ('Interior y offset: ', self.interior.winfo_y() )
            # update the scrollbars to match the size of the inner frame
            self.size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % self.size)
            # self.canvas.config(scrollregion = self.canvas.bbox('all'))
            # self.canvas.config(width=self.interior.winfo_reqwidth())
            # self.canvas.config(height=self.interior.winfo_reqheight())
            # if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            #     # update the canvas's width to fit the inner frame
            #     self.canvas.config(width = self.interior.winfo_reqwidth())
            # if self.interior.winfo_reqheight() != self.canvas.winfo_height():
            #     self.canvas.config(height = self.interior.winfo_reqheight())

        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            print ('Canvas event', event, event.widget)
            print ('Canvas y ofset: ', self.canvas.winfo_y())
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
            # if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            #     # update the inner frame's width to fill the canvas
            #     self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

        self.canvas.bind('<Configure>', _configure_canvas)

