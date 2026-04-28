import tkinter as tk
import math

# ---------- Functions ----------
def press(key):
    entry.insert(tk.END, str(key))

def clear():
    entry.delete(0, tk.END)

def backspace():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current[:-1])

def calculate():
    try:
        expr = entry.get()
        result = eval(expr)
        history.insert(tk.END, f"{expr} = {result}\n")
        entry.delete(0, tk.END)
        entry.insert(0, result)
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# Scientific functions
def sin(): press("math.sin(")
def cos(): press("math.cos(")
def tan(): press("math.tan(")
def log(): press("math.log10(")
def ln(): press("math.log(")
def sqrt(): press("math.sqrt(")
def power(): press("**")

def pi(): press(str(math.pi))
def e(): press(str(math.e))

# ---------- UI ----------
root = tk.Tk()
root.title("Pro Calculator")
root.geometry("420x600")
root.configure(bg="#1e1e1e")

# Entry
entry = tk.Entry(root, font=("Arial", 20), bd=10, relief=tk.FLAT,
                 bg="#2d2d2d", fg="white", justify="right")
entry.pack(fill="both", padx=10, pady=10)

# History
history = tk.Text(root, height=5, bg="#1e1e1e", fg="lightgreen", font=("Arial", 10))
history.pack(fill="both", padx=10)

# Button frame
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack()

# Button creator
def create_btn(text, cmd, r, c):
    tk.Button(frame, text=text, width=6, height=2,
              bg="#333", fg="white", activebackground="#555",
              command=cmd).grid(row=r, column=c, padx=5, pady=5)

# ---------- Buttons ----------
buttons = [
    ('7', lambda: press('7')), ('8', lambda: press('8')), ('9', lambda: press('9')), ('/', lambda: press('/')), ('⌫', backspace),
    ('4', lambda: press('4')), ('5', lambda: press('5')), ('6', lambda: press('6')), ('*', lambda: press('*')), ('%', lambda: press('%')),
    ('1', lambda: press('1')), ('2', lambda: press('2')), ('3', lambda: press('3')), ('-', lambda: press('-')), ('+', lambda: press('+')),
    ('0', lambda: press('0')), ('.', lambda: press('.')), ('(', lambda: press('(')), (')', lambda: press(')')), ('=', calculate),
    ('sin', sin), ('cos', cos), ('tan', tan), ('log', log), ('ln', ln),
    ('√', sqrt), ('x²', lambda: press('**2')), ('xʸ', power), ('π', pi), ('e', e),
    ('C', clear)
]

# Place buttons
row = 0
col = 0
for text, cmd in buttons:
    create_btn(text, cmd, row, col)
    col += 1
    if col > 4:
        col = 0
        row += 1

# ---------- Keyboard Support ----------
def key_input(event):
    key = event.char
    if key in "0123456789+-*/().%":
        press(key)
    elif event.keysym == "Return":
        calculate()
    elif event.keysym == "BackSpace":
        backspace()

root.bind("<Key>", key_input)

# Run app
root.mainloop()
