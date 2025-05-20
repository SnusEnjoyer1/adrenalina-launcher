import tkinter as tk
from tkinter import messagebox
import webbrowser
import platform
import threading
import time
import os
import winsound
import datetime
import json
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

# ---------------------- CONFIG ----------------------
SERVER_LINK = "fivem://connect/cfx.re/join/ll6aqo"
SOUND_FILE = "siema.wav"
CONFIG_FILE = "config.json"
LOG_FILE = "log.txt"

# Default Config
config = {
    "nickname": "Byku123",
    "theme": "dark"
}

# ---------------------- FUNCTIONS ----------------------
def load_config():
    global config
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    else:
        save_config()

def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def log_action(action):
    with open(LOG_FILE, 'a') as log:
        log.write(f"[{datetime.datetime.now()}] {action}\n")

def play_sound():
    if platform.system() == "Windows" and os.path.exists(SOUND_FILE):
        winsound.PlaySound(SOUND_FILE, winsound.SND_FILENAME)

def connect():
    nickname = nickname_var.get().strip()
    if not nickname:
        messagebox.showerror("Błąd", "Nick nie może być pusty!")
        return

    config["nickname"] = nickname
    save_config()

    status_label.config(text="🚀 Łączenie z AdrenalinaRP...", fg="yellow")
    threading.Thread(target=play_sound).start()
    time.sleep(1)
    webbrowser.open(SERVER_LINK)
    log_action(f"Połączono jako {nickname}")
    status_label.config(text="✅ Połączono! Zamykam za 3 sekundy...", fg="green")
    app.after(3000, app.quit)

def switch_theme():
    config["theme"] = "dark" if config["theme"] == "light" else "light"
    save_config()
    apply_theme()

def apply_theme():
    theme = config["theme"]
    bg = "#1e1e2f" if theme == "dark" else "#f4f4f4"
    fg = "#ffffff" if theme == "dark" else "#000000"
    btn_bg = "#ff4444" if theme == "dark" else "#cc0000"
    entry_bg = "#333333" if theme == "dark" else "#ffffff"
    entry_fg = fg

    app.configure(bg=bg)
    for widget in [title_label, status_label, nickname_label]:
        widget.configure(bg=bg, fg=fg)
    connect_button.configure(bg=btn_bg, fg="white", activebackground="#cc0000")
    nickname_entry.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
    theme_button.configure(bg="#555555" if theme == "dark" else "#dddddd", fg=fg)

# ---------------------- TRAY ICON ----------------------
def create_image():
    # Prosty obrazek do tray (czerwone tło + białe RP)
    image = Image.new('RGB', (64, 64), color=(255, 85, 85))
    d = ImageDraw.Draw(image)
    d.text((18, 20), 'RP', fill=(255, 255, 255))
    return image

def on_quit(icon, item):
    icon.stop()
    app.quit()

def setup_tray():
    image = create_image()
    menu = pystray.Menu(item('Wyjdz', on_quit))
    icon = pystray.Icon("AdrenalinaRP", image, menu=menu)
    threading.Thread(target=icon.run, daemon=True).start()

# ---------------------- GUI SETUP ----------------------
load_config()
app = tk.Tk()
app.title("🔥 AdrenalinaRP Launcher")
app.geometry("400x300")
app.resizable(False, False)

title_label = tk.Label(app, text="🔥 AdrenalinaRP Launcher", font=("Segoe UI", 16, "bold"))
title_label.pack(pady=(20, 10))

nickname_label = tk.Label(app, text="Twój nick:")
nickname_label.pack()

nickname_var = tk.StringVar(value=config["nickname"])
nickname_entry = tk.Entry(app, textvariable=nickname_var, font=("Segoe UI", 12), justify='center')
nickname_entry.pack(pady=(5, 15))

connect_button = tk.Button(app, text="💀 Połącz z serwerem", command=connect, font=("Segoe UI", 12, "bold"), width=25, height=2)
connect_button.pack(pady=10)

status_label = tk.Label(app, text="", font=("Segoe UI", 10, "italic"))
status_label.pack(pady=(10, 0))

theme_button = tk.Button(app, text="🌓 Zmień motyw", command=switch_theme)
theme_button.pack(pady=5)

apply_theme()
setup_tray()
log_action("Launcher uruchomiony")

app.mainloop()
