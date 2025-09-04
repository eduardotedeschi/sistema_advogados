import tkinter as tk
from software_adv import db, ui

def main():
    root = tk.Tk()
    db.monta_tabelas()
    app = ui.App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
