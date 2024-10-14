def showLists(l, *lists):
    """
    Present passed equal-length lists in adjacent scrollboxes.
    """
    # This exists mainly for me to start learning about Tkinter.
    # This widget requires at least one list be passed, and as many additional
    # lists as desired.  Each list is displayed in its own listbox, with
    # additional listboxes added to the right as needed to display all lists.
    # The width of each listbox is set to match the max width of its contents.
    # Caveat: Too wide or too many lists, and the widget can be wider than the screen!
    # The listboxes scroll together, using either the scrollbar or mousewheel.

    # :TODO: Refactor as an object with methods.
    # :TODO: Move to a separate file when other widgets are built.

    # Check arguments
    if (l is None) or (len(l) < 1):
        return
    listOfLists = [l]     # Form a list of lists for subsequent processing
    listBoxes = []  # List of listboxes
    if len(lists) > 0:
        for list in lists:
            # All lists must match length of first list
            # :TODO: Add tail filling for short lists, with error for long lists
            if len(list) != len(l):
                return
            listOfLists.append(list)

    import Tkinter

    def onVsb(*args):
        """
        When the scrollbar moves, scroll the listboxes.
        """
        for lb in listBoxes:
            lb.yview(*args)

    def onMouseWheel(event):
        """
        Convert mousewheel motion to scrollbar motion.
        """
        if (event.num == 4):    # Linux encodes wheel as 'buttons' 4 and 5
            delta = -1
        elif (event.num == 5):
            delta = 1
        else:                   # Windows & OSX
            delta = event.delta
        for lb in listBoxes:
            lb.yview("scroll", delta, "units")
        # Return 'break' to prevent the default bindings from
        # firing, which would end up scrolling the widget twice.
        return "break"

    # Create root window and scrollbar
    root = Tkinter.Tk()
    root.title('Samples w/ time step < 0')
    vsb = Tkinter.Scrollbar(root, orient=Tkinter.VERTICAL, command=onVsb)
    vsb.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

    # Create listboxes
    for i in xrange(0,len(listOfLists)):
        lb = Tkinter.Listbox(root, yscrollcommand=vsb.set)
        lb.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
        # Bind wheel events on both Windows/OSX & Linux;
        lb.bind("<MouseWheel>", onMouseWheel)
        lb.bind("<Button-4>", onMouseWheel)
        lb.bind("<Button-5>", onMouseWheel)
        # Fill the listbox
        maxWidth = 0
        for item in listOfLists[i]:
            s = str(item)
            if len(s) > maxWidth:
                maxWidth = len(s)
            lb.insert(Tkinter.END, s)
        lb.config(width=maxWidth+1)
        listBoxes.append(lb)        # Add listbox to list of listboxes

    # Show the widget
    Tkinter.mainloop()
# End of showLists()