import tkinter as tk
from tkcalendar import Calendar

def abrir_date_picker():
    selected = {"data": None}

    def on_select():
        selected["data"] = cal.get_date()
        root.destroy()

    root = tk.Tk()
    root.title("Selecionar Data")

    cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(padx=20, pady=20)

    btn = tk.Button(root, text="Selecionar", command=on_select)
    btn.pack(pady=10)

    root.mainloop()

    return selected["data"]