import threading
import time
import tkinter as tk
from tkinter import ttk

import keyboard
from pynput import mouse

# Flags und Einstellungen
spamming_enabled = False
use_mouse_mode = False
left_mouse_pressed = False
interval_ms = 150
selected_key = 'p'

# Lock für Thread-Sicherheit
lock = threading.Lock()


def spam_loop():
    while True:
        with lock:
            active = spamming_enabled and (
                not use_mouse_mode or left_mouse_pressed)
            interval = interval_ms / 1000.0
            key = selected_key
        if active:
            keyboard.press_and_release(key)
            time.sleep(interval)
        else:
            time.sleep(0.01)


def on_click(x, y, button, pressed):
    global left_mouse_pressed
    if button == mouse.Button.left:
        with lock:
            left_mouse_pressed = pressed


def update_status():
    status = 'Aktiviert' if spamming_enabled else 'Deaktiviert'
    color = 'green' if spamming_enabled else 'red'
    status_label.config(text=f"Status: {status}", foreground=color)


def toggle_spam_hotkey(e):
    global spamming_enabled
    with lock:
        spamming_enabled = not spamming_enabled
    update_status()


def on_interval_change(*args):
    global interval_ms
    try:
        val = int(interval_entry.get())
        with lock:
            interval_ms = max(1, val)
        interval_entry.config(foreground="black")
    except:
        interval_entry.config(foreground="red")


def on_mode_change():
    global use_mouse_mode
    with lock:
        use_mouse_mode = mode_var.get()


def on_key_select(event):
    global selected_key
    with lock:
        selected_key = key_combo.get()


def on_close():
    mouse_listener.stop()
    root.destroy()


# GUI erstellen
root = tk.Tk()
root.title("Ping-Spammer")

frame = ttk.Frame(root, padding=10)
frame.grid()

status_label = ttk.Label(frame, text="Status: Deaktiviert", foreground="red")
status_label.grid(row=0, column=0, columnspan=2, pady=5)

mode_var = tk.BooleanVar()
mode_checkbox = ttk.Checkbutton(
    frame, text="Maus-Modus (halten zum Spammen)",
    variable=mode_var, command=on_mode_change
)
mode_checkbox.grid(row=1, column=0, columnspan=2, pady=5)

ttk.Label(frame, text="Intervall (ms):").grid(row=2, column=0, sticky='e')
interval_entry = ttk.Entry(frame, width=10)
interval_entry.insert(0, "150")
interval_entry.grid(row=2, column=1, sticky='w')
interval_entry.bind("<KeyRelease>", on_interval_change)

ttk.Label(frame, text="Taste zum Spammen:").grid(row=3, column=0, sticky='e')
key_combo = ttk.Combobox(frame, values=[
    'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u',
    'v', 'w', 'x', 'y', 'z',
    'space', 'enter', 'tab', 'shift', 'ctrl'
], state='readonly')
key_combo.set('p')
key_combo.grid(row=3, column=1, sticky='w')
key_combo.bind("<<ComboboxSelected>>", on_key_select)

ttk.Label(frame, text="Hotkey: F8").grid(row=4, column=0, columnspan=2, pady=5)
ttk.Label(frame, text="Zum Beenden: Strg+C oder Fenster schließen").grid(row=5,
                                                                         column=0, columnspan=2)

root.protocol("WM_DELETE_WINDOW", on_close)

# Listener starten
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()
keyboard.on_press_key("f8", toggle_spam_hotkey)

# Spam-Thread starten
threading.Thread(target=spam_loop, daemon=True).start()

# GUI starten
root.mainloop()
