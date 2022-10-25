import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Checkbutton
import parser


def make_check():
    make_report_button.configure(state="disable")
    file = filedialog.askopenfile(initialdir="/", title="Select image", filetypes=(("CPP files", "*.cpp"), (("HPP files", "*.hpp")), ("All files", "*.*")))
    if file is None:
        return
    else:
        file_path = file.name
    try:
        file = open(file_path, "r")
        text_file = file.read()
        parser.get_string(text_file, 1)
        unused = []
        inc_n = []
        inc_d = []
        brackets = []
        if unused_var.get() == 1:
            unused = parser.find_unused_names()
        if incorrect_n_var.get() == 1:
            inc_n = parser.find_incorrect_names()
        if incorrect_d_var.get() == 1:
            inc_d = parser.find_incorrect_directives()
        if brackets_var.get() == 1:
            brackets = parser.check_brackets_pairing()
        print(unused + inc_n + inc_d + brackets)
        make_report_button.configure(state="normal")
    except AttributeError:
        print("File error")


def make_report():
    print("report")


parser = parser.CodeParser()
window = tk.Tk()
window.title("Code Parser")
width = 260
height = 200
x_pos = int(window.winfo_screenwidth() / 2 - width / 2)
y_pos = int(window.winfo_screenheight() / 2 - height / 2)
window.resizable(0, 0)
window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

unused_var = tk.IntVar()
incorrect_n_var = tk.IntVar()
incorrect_d_var = tk.IntVar()
brackets_var = tk.IntVar()

checkbox_unused_names = Checkbutton(window, text="Неиспользуемые имена", padding=4, variable=unused_var, onvalue=1, offvalue=0)
checkbox_incorrect_names = Checkbutton(window, text="Некорректные имена", padding=4, variable=incorrect_n_var, onvalue=1, offvalue=0)
checkbox_incorrect_directives = Checkbutton(window, text="Некорректные директивы", padding=4, variable=incorrect_d_var, onvalue=1, offvalue=0)
checkbox_brackets_check = Checkbutton(window, text="Парность скобок", padding=4, variable=brackets_var, onvalue=1, offvalue=0)

choose_type_text_label = tk.Label(window, text="Выберите типы проверок", padx=4, pady=4)
choose_file_text_label = tk.Label(window, text="Выберите файл исходного кода", padx=4, pady=4)
make_report_button = tk.Button(window, text="Отчёт", command=make_report, padx=4, pady=4, state="disabled")
browse_button = tk.Button(window, text="Обзор...", command=make_check, padx=4, pady=4)

choose_type_text_label.grid(column=0, row=0, sticky="W")
checkbox_brackets_check.grid(column=0, row=1, sticky="W")
checkbox_unused_names.grid(column=0, row=2, sticky="W")
checkbox_incorrect_names.grid(column=0, row=3, sticky="W")
checkbox_incorrect_directives.grid(column=0, row=4, sticky="W")
choose_file_text_label.grid(column=0, row=5)
browse_button.grid(column=1, row=5)
make_report_button.grid(columnspan=2, row=6)

window.mainloop()
