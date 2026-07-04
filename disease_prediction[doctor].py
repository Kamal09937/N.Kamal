import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ---------------- SECURITY ---------------- #
PASSWORD = "doctor123"

# ---------------- DARK THEME ---------------- #
BG = "#0f0f0f"
FG = "#ffffff"
CARD = "#1c1c1c"
ACCENT = "#00e676"
ENTRY_BG = "#2a2a2a"

# ---------------- DISEASE DATA ---------------- #
disease_data = {
    "Flu": {"symptoms": ["Fever","Cough","Body Pain","Fatigue"], "medicine": ["Paracetamol","Rest","Fluids"]},
    "Dengue": {"symptoms": ["Fever","Rash","Joint Pain"], "medicine": ["Paracetamol","Hydration"]},
    "Malaria": {"symptoms": ["Fever","Chills"], "medicine": ["Antimalarial","Doctor Care"]},
    "Cold": {"symptoms": ["Sneezing","Runny Nose","Cough"], "medicine": ["Antihistamine","Steam"]},
    "Diabetes": {"symptoms": ["Weight Loss","Fatigue"], "medicine": ["Diet Control","Exercise"]},
    "Hypertension": {"symptoms": ["High BP","Headache"], "medicine": ["Low Salt Diet","Exercise"]},
    "Asthma": {"symptoms": ["Shortness of Breath","Cough"], "medicine": ["Inhaler","Avoid Dust"]},
    "Covid-19": {"symptoms": ["Fever","Cough","Loss of Taste"], "medicine": ["Isolation","Fluids"]},
    "Migraine": {"symptoms": ["Headache","Nausea"], "medicine": ["Pain Reliever","Rest"]},
    "Anxiety Disorder": {"symptoms": ["Anxiety","Palpitations"], "medicine": ["Relaxation","Therapy"]},
    "Depression": {"symptoms": ["Depression","Insomnia"], "medicine": ["Counselling","Support"]},
    "Food Poisoning": {"symptoms": ["Vomiting","Diarrhea"], "medicine": ["ORS","Fluids"]},
    "Liver Disease": {"symptoms": ["Yellow Skin","Dark Urine"], "medicine": ["Diet Control"]},
    "Arthritis": {"symptoms": ["Joint Pain","Back Pain"], "medicine": ["Pain Relief","Exercise"]}
}

all_symptoms = sorted({s for d in disease_data.values() for s in d["symptoms"]})

history = []

# ---------------- LOGIN ---------------- #
def login_screen():
    def check():
        if entry.get() == PASSWORD:
            login.destroy()
            main_app()
        else:
            messagebox.showerror("Error", "Wrong Password")

    login = tk.Tk()
    login.title("Login")
    login.geometry("320x200")
    login.configure(bg=BG)

    tk.Label(login, text="🔐 Doctor Login",
             font=("Arial", 14, "bold"),
             fg=ACCENT, bg=BG).pack(pady=15)

    entry = tk.Entry(login, show="*", bg=ENTRY_BG, fg=FG, insertbackground=FG)
    entry.pack(pady=5)

    tk.Button(login, text="Login", command=check,
              bg=ACCENT, fg="black", width=10).pack(pady=10)

    login.mainloop()

# ---------------- MAIN APP ---------------- #
def main_app():
    root = tk.Tk()
    root.title("Disease Prediction System")
    root.geometry("850x750")
    root.configure(bg=BG)

    # ---------------- HEADER ---------------- #
    tk.Label(root, text="👨‍⚕️ Welcome Doctor",
             font=("Arial", 18, "bold"),
             fg=ACCENT, bg=BG).pack(pady=10)

    # ---------------- INPUT VARIABLES ---------------- #
    name_var = tk.StringVar()
    age_var = tk.StringVar()
    search_var = tk.StringVar()

    # ---------------- INPUT FRAME ---------------- #
    form = tk.Frame(root, bg=CARD, padx=10, pady=10)
    form.pack(pady=10, fill="x", padx=20)

    tk.Label(form, text="Patient Name", bg=CARD, fg=FG).grid(row=0, column=0, sticky="w")
    tk.Entry(form, textvariable=name_var,
             bg=ENTRY_BG, fg=FG, insertbackground=FG).grid(row=0, column=1, padx=10)

    tk.Label(form, text="Age", bg=CARD, fg=FG).grid(row=0, column=2, sticky="w")
    tk.Entry(form, textvariable=age_var,
             bg=ENTRY_BG, fg=FG, insertbackground=FG, width=10).grid(row=0, column=3, padx=10)

    tk.Label(form, text="Search Symptoms", bg=CARD, fg=FG).grid(row=1, column=0, sticky="w", pady=10)
    tk.Entry(form, textvariable=search_var,
             bg=ENTRY_BG, fg=FG, insertbackground=FG).grid(row=1, column=1, columnspan=3, sticky="we")

    # ---------------- LISTBOX ---------------- #
    frame = tk.Frame(root, bg=BG)
    frame.pack()

    scroll = tk.Scrollbar(frame)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frame,
                         selectmode=tk.MULTIPLE,
                         width=60,
                         height=15,
                         bg=ENTRY_BG,
                         fg=FG,
                         selectbackground=ACCENT,
                         yscrollcommand=scroll.set)

    listbox.pack()
    scroll.config(command=listbox.yview)

    for s in all_symptoms:
        listbox.insert(tk.END, s)

    def update(*args):
        q = search_var.get().lower()
        listbox.delete(0, tk.END)
        for s in all_symptoms:
            if q in s.lower():
                listbox.insert(tk.END, s)

    search_var.trace("w", update)

    # ---------------- HISTORY ---------------- #
    def save_history(record):
        history.append(record)
        with open("history.txt", "a") as f:
            f.write(record + "\n")

    # ---------------- PREDICT ---------------- #
    def predict():
        name = name_var.get().strip()
        age = age_var.get().strip()
        selected = [listbox.get(i) for i in listbox.curselection()]

        if not name or not age:
            messagebox.showwarning("Warning", "Enter name and age")
            return

        if not selected:
            messagebox.showwarning("Warning", "Select symptoms")
            return

        scores = {}
        for disease, data in disease_data.items():
            score = len(set(selected) & set(data["symptoms"]))
            scores[disease] = score

        best = max(scores, key=scores.get)

        if scores[best] == 0:
            messagebox.showinfo("Result", "No matching disease found")
            return

        meds = disease_data[best]["medicine"]

        result = f"""Patient: {name}
Age: {age}

Disease: {best}

Medicines:
{chr(10).join(meds)}"""

        record = f"{datetime.now()} | {name} | {age} | {best}"
        save_history(record)

        messagebox.showinfo("Result", result)

    # ---------------- HISTORY VIEW ---------------- #
    def view_history():
        win = tk.Toplevel(root)
        win.title("History")
        win.geometry("500x400")
        win.configure(bg=BG)

        txt = tk.Text(win, bg=ENTRY_BG, fg=FG, insertbackground=FG)
        txt.pack(fill="both", expand=True)

        try:
            with open("history.txt", "r") as f:
                txt.insert(tk.END, f.read())
        except:
            txt.insert(tk.END, "No history found")

    # ---------------- BUTTONS ---------------- #
    btn_frame = tk.Frame(root, bg=BG)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Predict Disease",
              command=predict,
              bg=ACCENT, fg="black", width=20).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="View History",
              command=view_history,
              bg=CARD, fg=FG, width=20).grid(row=0, column=1, padx=10)

    tk.Button(root, text="Exit",
              command=root.destroy,
              bg="red", fg="white", width=10).pack(pady=10)

    root.mainloop()

# ---------------- START ---------------- #
login_screen()
