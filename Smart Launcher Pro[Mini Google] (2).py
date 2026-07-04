import tkinter as tk
import webbrowser
import urllib.parse

# ---------------- Chrome Setup ---------------- #
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
browser = webbrowser.get("chrome")

# ---------------- LOGIN ---------------- #
PASSWORD = "(@Pt@!N3m0"
USERNAME = "Kamal"

# ---------------- WEBSITE DATABASE ---------------- #
websites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "youtube music": "https://music.youtube.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "gitlab": "https://gitlab.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "amazon": "https://www.amazon.com",
    "flipkart": "https://www.flipkart.com",
    "netflix": "https://www.netflix.com",
    "chatgpt": "https://chatgpt.com",
    "stackoverflow": "https://stackoverflow.com",
    "reddit": "https://www.reddit.com",
    "twitter": "https://x.com",
    "x": "https://x.com",
    "spotify": "https://open.spotify.com",
    "wikipedia": "https://www.wikipedia.org"
}

# ---------------- HISTORY ---------------- #
history = []

# ---------------- LOGIN SCREEN ---------------- #
def check_login():
    if pass_entry.get() == PASSWORD:
        login.destroy()
        open_app()
    else:
        error.config(text="❌ Wrong Password")

login = tk.Tk()
login.title("Login")
login.geometry("300x200")
login.configure(bg="#1e1e1e")

tk.Label(login, text="🔐 Enter Password", fg="white", bg="#1e1e1e").pack(pady=10)

pass_entry = tk.Entry(login, show="*", font=("Arial", 14))
pass_entry.pack()

tk.Button(login, text="Login", command=check_login).pack(pady=5)

error = tk.Label(login, text="", fg="red", bg="#1e1e1e")
error.pack()

# ---------------- MAIN APP ---------------- #
def open_app():
    root = tk.Tk()
    root.title("🚀 Smart Launcher Pro Max")
    root.geometry("900x650")
    root.configure(bg="#1e1e1e")

    # ---------------- HISTORY FUNCTION ---------------- #
    def add_history(text):
        history.append(text)
        history_list.insert(tk.END, text)

    # ---------------- OPEN URL SAFE ---------------- #
    def open_url(name, url):
        browser.open(url)
        add_history(name)

    # ---------------- GOOGLE SEARCH ---------------- #
    def search_google(query):
        url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
        browser.open(url)
        add_history(f"Search: {query}")

    # ---------------- UI ---------------- #
    tk.Label(
        root,
        text=f"👋 Welcome {USERNAME}",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#1e1e1e"
    ).pack(pady=10)

    # Search box
    entry = tk.Entry(root, font=("Arial", 14), width=50)
    entry.pack(pady=10)

    # Results
    result_box = tk.Listbox(root, width=60, height=8)
    result_box.pack()

    # History label
    tk.Label(
        root,
        text="📜 History",
        fg="white",
        bg="#1e1e1e",
        font=("Arial", 12, "bold")
    ).pack(pady=5)

    history_list = tk.Listbox(root, width=60, height=7)
    history_list.pack()

    # ---------------- SMART SEARCH ---------------- #
    def update_results(event=None):
        text = entry.get().lower().strip()
        result_box.delete(0, tk.END)

        if not text:
            return

        found = False
        for name in websites:
            if text in name:
                result_box.insert(tk.END, name)
                found = True

        if not found:
            result_box.insert(tk.END, f"Search Google: {text}")

    # ---------------- OPEN FROM LIST ---------------- #
    def open_selected(event=None):
        selection = result_box.curselection()

        if not selection:
            return  # prevents crash

        selected = result_box.get(selection[0])

        if selected.startswith("Search Google"):
            query = entry.get().strip()
            search_google(query)
        else:
            url = websites.get(selected)
            if url:
                open_url(selected, url)

    # ---------------- CLEAR HISTORY ---------------- #
    def clear_history():
        history.clear()
        history_list.delete(0, tk.END)

    # ---------------- EVENTS ---------------- #
    entry.bind("<KeyRelease>", update_results)
    result_box.bind("<Double-Button-1>", open_selected)

    # ---------------- QUICK BUTTONS ---------------- #
    btn_google = tk.Button(root, text="🌐 Google",
                           command=lambda: open_url("google", websites["google"]))
    btn_google.pack(pady=2)

    btn_youtube = tk.Button(root, text="🎥 YouTube",
                            command=lambda: open_url("youtube", websites["youtube"]))
    btn_youtube.pack(pady=2)

    # ---------------- GRID BUTTONS ---------------- #
    frame = tk.Frame(root, bg="#1e1e1e")
    frame.pack(pady=10)

    for i, (name, url) in enumerate(websites.items()):
        tk.Button(
            frame,
            text=name.title(),
            width=15,
            bg="#4285F4",
            fg="white",
            command=lambda n=name, u=url: open_url(n, u)
        ).grid(row=i // 4, column=i % 4, padx=5, pady=5)

    # ---------------- CONTROL BUTTONS ---------------- #
    tk.Button(root, text="🧹 Clear History", command=clear_history).pack(pady=5)
    tk.Button(root, text="❌ Exit", bg="red", fg="white", command=root.destroy).pack(pady=5)

    root.mainloop()

login.mainloop()

