import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# -------------------------------
# Symptoms
# -------------------------------
all_symptoms = [
    "Fever","Cough","Headache","Body Pain","Chills","Fatigue","Nausea","Vomiting",
    "Diarrhea","Abdominal Pain","Chest Pain","Shortness of Breath","Dizziness",
    "Weight Loss","Joint Pain","Rash","Itching","Runny Nose","Sneezing","Sore Throat"
]

# -------------------------------
# Diseases + Medicines
# -------------------------------
disease_data = {
    "Flu": {"symptoms": ["Fever","Cough","Body Pain","Fatigue"], "medicine": ["Paracetamol","Rest","Fluids"]},
    "Cold": {"symptoms": ["Sneezing","Runny Nose","Cough"], "medicine": ["Antihistamine","Steam"]},
    "Dengue": {"symptoms": ["Fever","Rash","Joint Pain"], "medicine": ["Paracetamol","Hydration"]},
    "Diabetes": {"symptoms": ["Weight Loss","Fatigue"], "medicine": ["Diet Control","Doctor Visit"]},
    "Hypertension": {"symptoms": ["Headache","Dizziness"], "medicine": ["Low Salt Diet","Exercise"]},
    "Food Poisoning": {"symptoms": ["Vomiting","Diarrhea","Abdominal Pain"], "medicine": ["ORS","Fluids"]},
    "Migraine": {"symptoms": ["Headache","Nausea"], "medicine": ["Pain Reliever","Rest"]}
}

# -------------------------------
# Colors (Dark Theme)
# -------------------------------
BG = "#121212"
FG = "#ffffff"
BTN = "#1f1f1f"
ACCENT = "#00c853"

# -------------------------------
# App Setup
# -------------------------------
root = tk.Tk()
root.title("Disease Prediction System")
root.geometry("750x650")
root.configure(bg=BG)

# -------------------------------
# Title
# -------------------------------
tk.Label(root, text="Disease Prediction System",
         font=("Arial", 18, "bold"),
         bg=BG, fg=ACCENT).pack(pady=10)

# -------------------------------
# Patient Info
# -------------------------------
name_var = tk.StringVar()
age_var = tk.StringVar()

tk.Label(root, text="Patient Name:", bg=BG, fg=FG).pack()
tk.Entry(root, textvariable=name_var, bg=BTN, fg=FG, insertbackground=FG).pack()

tk.Label(root, text="Age:", bg=BG, fg=FG).pack()
tk.Entry(root, textvariable=age_var, bg=BTN, fg=FG, insertbackground=FG).pack(pady=5)

# -------------------------------
# Search Section (NEW)
# -------------------------------
search_var = tk.StringVar()

search_frame = tk.Frame(root, bg=BG)
search_frame.pack(pady=5)

tk.Entry(search_frame, textvariable=search_var, width=30,
         bg=BTN, fg=FG, insertbackground=FG).pack(side=tk.LEFT, padx=5)

def search_symptom():
    query = search_var.get().lower()
    listbox.delete(0, tk.END)
    for s in all_symptoms:
        if query in s.lower():
            listbox.insert(tk.END, s)

def reset_list():
    search_var.set("")
    listbox.delete(0, tk.END)
    for s in all_symptoms:
        listbox.insert(tk.END, s)

tk.Button(search_frame, text="Search", command=search_symptom,
          bg=ACCENT, fg="black").pack(side=tk.LEFT, padx=5)

tk.Button(search_frame, text="Reset", command=reset_list,
          bg=BTN, fg=FG).pack(side=tk.LEFT)

# -------------------------------
# Listbox
# -------------------------------
frame = tk.Frame(root, bg=BG)
frame.pack()

scroll = tk.Scrollbar(frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE,
                     width=50, height=15,
                     bg=BTN, fg=FG,
                     selectbackground=ACCENT,
                     yscrollcommand=scroll.set)

listbox.pack()
scroll.config(command=listbox.yview)

for s in all_symptoms:
    listbox.insert(tk.END, s)

# -------------------------------
# Select / Clear
# -------------------------------
def select_all():
    listbox.select_set(0, tk.END)

def clear_all():
    listbox.select_clear(0, tk.END)

tk.Button(root, text="Select All", command=select_all,
          bg=BTN, fg=FG).pack(pady=3)

tk.Button(root, text="Clear All", command=clear_all,
          bg=BTN, fg=FG).pack(pady=3)

# -------------------------------
# Prediction
# -------------------------------
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
        match = len(set(selected) & set(data["symptoms"]))
        scores[disease] = match
    
    best = max(scores, key=scores.get)
    
    if scores[best] == 0:
        messagebox.showinfo("Result", "No matching disease found")
        return
    
    medicines = disease_data[best]["medicine"]
    
    result = f"Patient: {name}\nAge: {age}\n\nDisease: {best}\n\nRecommended Care:\n"
    result += "\n".join(medicines)
    
    record = f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | {name} | {age} | {best} | {', '.join(medicines)}"
    
    with open("history.txt", "a") as f:
        f.write(record + "\n")
    
    messagebox.showinfo("Prediction Result", result)

# -------------------------------
# History
# -------------------------------
def view_history():
    win = tk.Toplevel(root)
    win.title("Patient History")
    win.geometry("500x400")
    win.configure(bg=BG)
    
    text = tk.Text(win, bg=BTN, fg=FG)
    text.pack(fill="both", expand=True)
    
    try:
        with open("history.txt", "r") as f:
            text.insert(tk.END, f.read())
    except:
        text.insert(tk.END, "No history available")

# -------------------------------
# Buttons
# -------------------------------
tk.Button(root, text="Predict Disease", command=predict,
          bg=ACCENT, fg="black", font=("Arial", 12)).pack(pady=10)

tk.Button(root, text="View History", command=view_history,
          bg=BTN, fg=FG).pack(pady=5)

# Enter key triggers search
root.bind('<Return>', lambda event: search_symptom())

root.mainloop()
