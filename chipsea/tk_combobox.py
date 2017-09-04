import tkinter as tk
from   tkinter import ttk

window = tk.Tk()
window.title = "Combobox"
number = tk.StringVar()
numberChosen=ttk.Combobox(window,width=12,textvariable=number)
numberChosen['values']=(1,2,3,4,5,6,7,8,9)
numberChosen.grid()
numberChosen.current(0)
window.mainloop()
