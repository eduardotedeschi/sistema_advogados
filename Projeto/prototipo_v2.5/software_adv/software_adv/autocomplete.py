import tkinter as tk
from tkinter import ttk, END
import re

class AutocompleteEntry(ttk.Entry):
    def __init__(self, autocompleteList, *args, **kwargs):
        self.listboxLength = kwargs.pop('listboxLength', 8)
        self.matchesFunction = kwargs.pop('matchesFunction', self.default_match)
        super().__init__(*args, **kwargs)

        self.autocompleteList = autocompleteList
        self.var = self["textvariable"]
        if not self.var:
            self.var = self["textvariable"] = tk.StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        self.listboxUp = False

    def default_match(self, fieldValue, acListEntry):
        pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
        return re.match(pattern, acListEntry)

    def changed(self, *args):
        if not self.var.get():
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = tk.Listbox(self.master, width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True
                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END, w)
            elif self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(tk.ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(END)

    def moveUp(self, event):
        if self.listboxUp:
            index = self.listbox.curselection()[0] if self.listbox.curselection() else 0
            if index != 0:
                self.listbox.selection_clear(first=index)
                index -= 1
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            index = self.listbox.curselection()[0] if self.listbox.curselection() else 0
            if index != END:
                self.listbox.selection_clear(first=index)
                index += 1
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        return [w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w)]
