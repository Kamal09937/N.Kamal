import tkinter as tk
import webbrowser
import urllib.parse

# ---------------- Chrome Setup ---------------- #
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
browser = webbrowser.get("chrome")

# ---------------- Data ---------------- #
favorites = []
history = []

# ---------------- Website Dictionary ---------------- #
websites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com",
    "maps": "https://maps.google.com",
    "wikipedia": "https://www.wikipedia.org",
    "chatgpt": "https://chatgpt.com",
    "github": "https://github.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://x.com",
    "reddit": "https://www.reddit.com",
    "netflix": "https://www.netflix.com",
    "amazon": "https://www.amazon.com",
    "spotify": "https://open.spotify.com"
}

# ---------------- Functions ---------------- #

def open_url(url):
    browser.open(url)
    history.append(url)
    refresh_history()

def smart_open(text):
    text = text.lower().strip()

    if text in websites:
        open_url(websites[text])
    else:
        url = "https://www.google.com/search?q=" + urllib.parse.quote(text)
        open_url(url)

    entry.delete(0, tk.END)
    suggest_box.delete(0, tk.END)

def google_search():
    q = entry.get()
    if q:
        open_url("https://www.google.com/search?q=" + urllib.parse.quote(q))

def youtube_search():
    q = entry.get()
    if q:
        open_url("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q))

def open_custom():
    site = entry.get()
    if site:
        if not site.startswith("http"):
            site = "https://" + site
        open_url(site)

def add_favorite():
    q = entry.get()
    if q:
        favorites.append(q)
        fav_list.insert(tk.END, q)

def refresh_history():
    hist_list.delete(0, tk.END)
    for h in history[-10:]:
        hist_list.insert(tk.END, h)

# ---------------- AUTOCOMPLETE ---------------- #

def update_suggestions(event):
    text = entry.get().lower()
    suggest_box.delete(0, tk.END)

    if text == "":
        return

    for key in websites:
        if text in key:
            suggest_box.insert(tk.END, key)

def open_suggestion(event):
    if suggest_box.curselection():
        selected = suggest_box.get(suggest_box.curselection())
        smart_open(selected)

# ---------------- UI ---------------- #

root = tk.Tk()
root.title("🚀 Smart Launcher Pro")
root.geometry("900x600")
root.configure(bg="#1e1e1e")

title = tk.Label(
    root,
    text="🌐 SMART LAUNCHER PRO (Google Style)",
    font=("Arial", 18, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title.pack(pady=10)

# ---------------- SEARCH BAR ---------------- #

entry = tk.Entry(root, font=("Arial", 14), width=50)
entry.pack(pady=5)
entry.bind("<KeyRelease>", update_suggestions)
entry.bind("<Return>", lambda e: smart_open(entry.get()))

# ---------------- SUGGESTIONS ---------------- #

suggest_box = tk.Listbox(root, height=5, width=50)
suggest_box.pack(pady=5)
suggest_box.bind("<Double-Button-1>", open_suggestion)

# ---------------- BUTTONS ---------------- #

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="🔍 Google", command=google_search).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="🎥 YouTube", command=youtube_search).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="🌍 Website", command=open_custom).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="⭐ Favorite", command=add_favorite).grid(row=0, column=3, padx=5)

# ---------------- PANELS ---------------- #

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

fav_list = tk.Listbox(frame, width=40)
fav_list.grid(row=0, column=0, padx=10)

hist_list = tk.Listbox(frame, width=40)
hist_list.grid(row=0, column=1, padx=10)

# ---------------- WEBSITE BUTTONS ---------------- #

web_frame = tk.Frame(root, bg="#1e1e1e")
web_frame.pack(pady=10)

for i, (name, url) in enumerate(websites.items()):
    tk.Button(
        web_frame,
        text=name.title(),
        width=15,
        bg="#4285F4",
        fg="white",
        command=lambda u=url: open_url(u)
    ).grid(row=i//4, column=i%4, padx=5, pady=5)

# ---------------- EXIT ---------------- #

tk.Button(
    root,
    text="❌ Exit",
    bg="red",
    fg="white",
    command=root.destroy
).pack(pady=10)

root.mainloop()


