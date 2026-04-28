import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# -------------------------------
# Symptoms
# -------------------------------
all_symptoms = [
    "Fever","Cough","Headache","Body Pain","Chills","Fatigue","Nausea","Vomiting",
    "Diarrhea","Abdominal Pain","Chest Pain","Shortness of Breath","Dizziness",
    "Weight Loss","Weight Gain","Joint Pain","Rash","Itching","Runny Nose",
    "Sneezing","Sore Throat","Anxiety","Depression","Insomnia","Palpitations",
    "High BP","Low BP","Acidity","Loss of Taste","Loss of Smell","Back Pain",
    "Neck Pain","Tremors","Seizures","Memory Loss","Confusion","Dry Mouth",
    "Yellow Skin","Dark Urine","Pale Skin","Allergy","Infection","Inflammation"
]

# -------------------------------
# Diseases
# -------------------------------
disease_data = {
    "Flu": ["Fever","Cough","Body Pain","Fatigue"],
    "Dengue": ["Fever","Rash","Joint Pain"],
    "Malaria": ["Fever","Chills","Sweating"],
    "Cold": ["Sneezing","Runny Nose","Cough"],
    "Diabetes": ["Weight Loss","Fatigue"],
    "Hypertension": ["High BP","Headache"],
    "Asthma": ["Shortness of Breath","Cough"],
    "Covid-19": ["Fever","Cough","Loss of Taste"],
    "Migraine": ["Headache","Nausea"],
    "Anxiety Disorder": ["Anxiety","Palpitations"],
    "Depression": ["Depression","Insomnia"],
    "Food Poisoning": ["Vomiting","Diarrhea"],
    "Liver Disease": ["Yellow Skin","Dark Urine"],
    "Arthritis": ["Joint Pain","Back Pain"]
}

# -------------------------------
# Dark Theme Colors
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

history = []

# -------------------------------
# Title
# -------------------------------
tk.Label(root, text="Disease Prediction System",
         font=("Arial", 18, "bold"),
         bg=BG, fg=ACCENT).pack(pady=10)

# -------------------------------
# Patient Name
# -------------------------------
name_var = tk.StringVar()
tk.Label(root, text="Patient Name:", bg=BG, fg=FG).pack()
tk.Entry(root, textvariable=name_var, bg=BTN, fg=FG, insertbackground=FG).pack(pady=5)

# -------------------------------
# Search Bar
# -------------------------------
search_var = tk.StringVar()

def update_list(*args):
    search = search_var.get().lower()
    listbox.delete(0, tk.END)
    for s in all_symptoms:
        if search in s.lower():
            listbox.insert(tk.END, s)

search_var.trace("w", update_list)

tk.Entry(root, textvariable=search_var, width=40,
         bg=BTN, fg=FG, insertbackground=FG).pack(pady=5)

# -------------------------------
# Listbox
# -------------------------------
frame = tk.Frame(root, bg=BG)
frame.pack()

scroll = tk.Scrollbar(frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE,
                     width=50, height=18,
                     bg=BTN, fg=FG,
                     selectbackground=ACCENT,
                     yscrollcommand=scroll.set)

listbox.pack()
scroll.config(command=listbox.yview)

for s in all_symptoms:
    listbox.insert(tk.END, s)

# -------------------------------
# Buttons
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
# Prediction + Save History
# -------------------------------
def predict():
    name = name_var.get().strip()
    selected = [listbox.get(i) for i in listbox.curselection()]
    
    if not name:
        messagebox.showwarning("Warning", "Enter patient name")
        return
    
    if not selected:
        messagebox.showwarning("Warning", "Select symptoms")
        return
    
    scores = {}
    for disease, symptoms in disease_data.items():
        score = len(set(selected) & set(symptoms))
        scores[disease] = score
    
    best = max(scores, key=scores.get)
    
    # Save history
    record = f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | {name} | {best}"
    history.append(record)
    
    with open("history.txt", "a") as f:
        f.write(record + "\n")
    
    messagebox.showinfo("Result", f"Most Likely Disease:\n\n{best}")

# -------------------------------
# View History
# -------------------------------
def view_history():
    win = tk.Toplevel(root)
    win.title("Patient History")
    win.geometry("500x400")
    win.configure(bg=BG)
    
    tk.Label(win, text="Patient History", font=("Arial", 14, "bold"),
             bg=BG, fg=ACCENT).pack(pady=10)
    
    text = tk.Text(win, bg=BTN, fg=FG)
    text.pack(fill="both", expand=True)
    
    try:
        with open("history.txt", "r") as f:
            text.insert(tk.END, f.read())
    except:
        text.insert(tk.END, "No history available")

# -------------------------------
# Action Buttons
# -------------------------------
tk.Button(root, text="Predict Disease", command=predict,
          bg=ACCENT, fg="black", font=("Arial", 12)).pack(pady=10)

tk.Button(root, text="View History", command=view_history,
          bg=BTN, fg=FG).pack(pady=5)
age_var = tk.StringVar()

tk.Label(root, text="Age:", bg=BG, fg=FG).pack()
tk.Entry(root, textvariable=age_var,
         bg=BTN, fg=FG, insertbackground=FG).pack(pady=5)
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
def predict():
    name = name_var.get().strip()
    age = age_var.get().strip()
    selected = [listbox.get(i) for i in listbox.curselection()]
    
    if not name or not age:
        messagebox.showwarning("Warning", "Enter patient name and age")
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
    
    medicines = disease_data[best]["medicine"]
    
    result = f"Patient: {name}\nAge: {age}\n\nDisease: {best}\n\nRecommended Medicines:\n"
    result += "\n".join(medicines)
    
    # Save history
    record = f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | {name} | {age} | {best} | {', '.join(medicines)}"
    history.append(record)
    
    with open("history.txt", "a") as f:
        f.write(record + "\n")
    
    messagebox.showinfo("Result", result)

root.mainloop()
