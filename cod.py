import threading
import time
import tkinter as tk
from tkinter import ttk

import keyboard
from pynput import mouse

# Flags
spamming_enabled = False
use_mouse_mode = False
left_mouse_pressed = False
interval_ms = 50

# Lock für Thread-Sicherheit
lock = threading.Lock()


def spam_loop():
    while True:
        with lock:
            active = spamming_enabled and (
                not use_mouse_mode or left_mouse_pressed)
            interval = interval_ms / 1000.0
        if active:
            keyboard.press_and_release('p')
            time.sleep(interval)
        else:
            time.sleep(0.01)


def on_click(x, y, button, pressed):
    global left_mouse_pressed
    if button == mouse.Button.left:
        with lock:
            left_mouse_pressed = pressed


def toggle_spam_hotkey(e):
    global spamming_enabled
    with lock:
        spamming_enabled = not spamming_enabled
        status_label.config(
            text=f"Status: {'Aktiviert' if spamming_enabled else 'Deaktiviert'}")


def on_interval_change(*args):
    global interval_ms
    try:
        val = int(interval_entry.get())
        with lock:
            interval_ms = max(1, val)
    except:
        pass


def on_mode_change():
    global use_mouse_mode
    with lock:
        use_mouse_mode = mode_var.get()


# GUI erstellen
root = tk.Tk()
root.title("P-Spammer")

frame = ttk.Frame(root, padding=10)
frame.grid()

status_label = ttk.Label(frame, text="Status: Deaktiviert")
status_label.grid(row=0, column=0, columnspan=2, pady=5)

mode_var = tk.BooleanVar()
mode_checkbox = ttk.Checkbutton(
    frame, text="Maus-Modus (halten zum Spammen)", variable=mode_var, command=on_mode_change)
mode_checkbox.grid(row=1, column=0, columnspan=2, pady=5)

ttk.Label(frame, text="Intervall (ms):").grid(row=2, column=0, sticky='e')
interval_entry = ttk.Entry(frame, width=10)
interval_entry.insert(0, "50")
interval_entry.grid(row=2, column=1, sticky='w')
interval_entry.bind("<KeyRelease>", on_interval_change)

ttk.Label(frame, text="Hotkey: F8").grid(row=3, column=0, columnspan=2, pady=5)
ttk.Label(frame, text="Zum Beenden: Strg+C oder Fenster schließen").grid(row=4,
                                                                         column=0, columnspan=2)

# Listener starten
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()
keyboard.on_press_key("f8", toggle_spam_hotkey)

# Spam-Thread starten
threading.Thread(target=spam_loop, daemon=True).start()

# GUI starten
root.mainloop()
