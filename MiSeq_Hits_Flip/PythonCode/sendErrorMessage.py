# -*- coding: utf-8 -*-

from sys import argv
from tkinter import messagebox, Tk

text = str(argv[-1])

root = Tk()
root.withdraw()
messagebox.showerror("Error!", text)
