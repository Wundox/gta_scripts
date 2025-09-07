import time
import pyautogui
import keyboard

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# ---- KONFIG ----
p1 = (669, 61)
p2 = (691, 919)
p3 = (973, 640)
scroll_amount = -880
step_pause = 0.4
max_loops = 12
# -----------------

running = False

def toggle():
    global running
    running = not running
    print("ON" if running else "OFF")

keyboard.add_hotkey('f2', toggle)

def wait_quick(seconds: float) -> bool:
    end = time.time() + seconds
    while time.time() < end:
        if not running:
            return False
        time.sleep(0.01)
    return True

print("F2 = Start/Stop. Maus oben links = Notaus. Strg+C beendet.")

while True:
    if not running:
        time.sleep(0.05)
        continue

    # 12 Loops
    for i in range(max_loops):
        if not running:
            break

        # Schritt 1: Tab
        pyautogui.press('tab')
        if not wait_quick(step_pause): break

        # Schritt 2: Bewegen + Klick
        pyautogui.moveTo(*p1, duration=0.08)
        pyautogui.click()
        if not wait_quick(step_pause): break

        pyautogui.moveTo(*p2, duration=0.08)

        # Schritt 3: Scrollen
        pyautogui.scroll(scroll_amount)
        if not wait_quick(step_pause): break

        # Schritt 4: Klick
        pyautogui.click()
        if not wait_quick(step_pause): break

        # Schritt 5: Bewegen + Klick
        pyautogui.moveTo(*p3, duration=0.08)
        pyautogui.click()
        if not wait_quick(step_pause): break

    running = False
    print("Fertig mit", max_loops, "Loops.")
