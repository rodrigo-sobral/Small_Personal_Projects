import tkinter as tk

def add_player_input_field(frame: tk.Frame) -> None:
    # define the placeholder text
    PLACEHOLDER_TEXT = "Nome do Jogador"

    # create the entry field and set its placeholder text
    entry = tk.Entry(frame, fg="gray", insertwidth=1, width=20, font=("Arial", 12))
    entry.insert(0, PLACEHOLDER_TEXT)

    def on_click(event):
        if entry.get() == PLACEHOLDER_TEXT:
            entry.delete(0, tk.END)
            entry.config(fg="black")
    def on_focusout(event):
        if entry.get() == "":
            entry.insert(0, PLACEHOLDER_TEXT)
            entry.config(fg="gray")

    entry.bind("<Button-1>", on_click)
    entry.bind("<FocusOut>", on_focusout)
    entry.pack(pady=10, padx=10)



def clear_int(value: str) -> int:
    return int(value.replace(',', '').replace(',', '').replace('(', '').replace(')', ''))

def clear_float(value: str) -> float:
    return float(value.split(' ')[-1].replace("rotate", "").replace("(", "").replace(")", "").replace("deg", "").replace(";", "").replace(" ", ""))
