from tkinter import *
from tkinter import ttk

class TipCalculator():

    def __init__(self):
        troys_window = Tk()
        troys_window.geometry("600x200")

        self.meal_cost = StringVar()
        self.tax_percent = DoubleVar()
        self.tip_percent = IntVar()
        self.tip = StringVar()
        self.total_cost = StringVar()

        troys_window.title("Troy's Tip Calculator")

        tip_amounts = Label(text="Tip Percentage")
        tip_amounts.grid(column=1, row=1)
        ten_percent_tip = Radiobutton(text="10%", variable=self.tip_percent, value=10)
        ten_percent_tip.grid(column=1, row=2)
        fifteen_percent_tip = Radiobutton(text="15%", variable=self.tip_percent, value=15)
        fifteen_percent_tip.grid(column=1, row=3)
        eighteen_percent_tip = Radiobutton(text="18%", variable=self.tip_percent, value=18)
        eighteen_percent_tip.grid(column=1, row=4)
        twenty_percent_tip = Radiobutton(text="20%", variable=self.tip_percent, value=20)
        twenty_percent_tip.grid(column=1, row=5)

        bill_amount_label = Label(text="Bill Amount")
        bill_amount_label.grid(column=2, row=1)
        bill_amount_entry = Entry(textvariable=self.meal_cost, width=7, justify=RIGHT)
        bill_amount_entry.grid(column=2, row=2)

        tax_amount_label = Label(text="Local Tax: ")
        tax_amount_label.grid(column=3, row=1)

        tax_amount_rb = Radiobutton(text="9.25%", variable=self.tax_percent, value=9.25)
        tax_amount_rb.grid(column=3, row=2)

        calculate_tax = Button(text="Calculate Total Tax", command=self.calculate_tax)
        calculate_tax.grid(column=6, row=3)

        tax_amount_label = Label(text="Tax = ")
        tax_amount_label.grid(column=6, row=4)
        tax_amount_lb = tk.Listbox(listvariable=self.tax_percent, height=1, width=7, justify=RIGHT)
        tax_amount_lb.grid(column=7, row=4)

        calculate_tip = Button(text="Calculate Tip", command=self.calculate_tip)
        calculate_tip.grid(column=6, row=1)

        tip_amount_label = Label(text="Tip = ")
        tip_amount_label.grid(column=6, row=2)
        tip_amount_lb = tk.Listbox(listvariable=self.tip, height=1, width=7, justify=RIGHT)
        tip_amount_lb.grid(column=7, row=2)

        calc_bill_total = Button(text="Calculate Bill Total: ", command=self.calculate_total_bill)
        calc_bill_total.grid(column=8, row=1)

        bill_total_label = Label(text="Bill Total: ", width=7, justify=RIGHT)
        bill_total_label.grid(column=8, row=2)
        bill_total_lb = tk.Listbox(listvariable=self.total_cost, height=1, width=7, justify=RIGHT)
        bill_total_lb.grid(column=9, row=2)

        troys_window.mainloop()

    def calculate_tax(self):
        try:
            pre_tip = self.meal_cost.get()
        except (ValueError):
            mb = tk.Message(troys_window, text="Bad Input")
            mb.grid(column=5, row=7)

        try:
            taxPercent = self.tax_percent.get()
        except (ValueError):
            mb = tk.Message(troys_window, text="Bad Input")
            mb.grid(column=5, row=7)
        tax_amount = round(pre_tip * taxPercent, 2)
        self.tax.set(tax_amount)

    def calculate_tip(self):
        pre_tip = float(self.meal_cost.get())
        tipPercentage = self.tip_percent.get()/100
        tip_amount = round(pre_tip * tipPercentage, 2)
        self.tip.set(tip_amount)

    def calculate_total_bill(self):
        pre_tip = float(self.meal_cost.get())
        tax = self.tax.get()
        tax_amount = pre_tip * tax
        percentage = self.tip_percent.get() / 100
        tip_amount = round(pre_tip * percentage, 2)
        bill_total = pre_tip * (1 + tax_amount) + tip_amount
        self.total_cost.set(bill_total)


TipCalculator()


