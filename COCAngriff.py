import os
import time

import cv2
import mouse
import numpy as np
import pyautogui

# Verzeichnis, in dem die Bilder gespeichert sind
image_folder = "images"


def is_colored(image: cv2.typing.MatLike):
    """Überprüft, ob das Bild farbig ist (Sättigung, Farbvarianz & RGB-Unterschiede)."""
    # image = cv2.imread(image_path)

    if image is None:
        print(f"⚠ Fehler: Bild konnte nicht geladen werden!")
        return False

    # **Bild nach HSV umwandeln & Sättigung berechnen**
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation = np.mean(hsv[:, :, 1])  # Mittelwert der Sättigung

    # **Farbvarianz berechnen (wenn zu wenig Farbabweichung → grau)**
    color_variance = np.var(image)

    # **RGB-Farbunterschiede berechnen**
    b, g, r = cv2.split(image)
    mean_diff_rg = np.mean(np.abs(r - g))
    mean_diff_rb = np.mean(np.abs(r - b))
    mean_diff_gb = np.mean(np.abs(g - b))

    # print(
    #     f"🔎 {image_path} | Sättigung: {saturation:.2f} | Varianz: {color_variance:.2f}")
    # print(
    #     f"🎨 Farbabweichungen (RG: {mean_diff_rg:.2f}, RB: {mean_diff_rb:.2f}, GB: {mean_diff_gb:.2f})")

    # **Strenge Kriterien für farbige Bilder:**
    if saturation < 60 or color_variance < 2000 or (mean_diff_rg < 20 and mean_diff_rb < 20 and mean_diff_gb < 20):
        # print(
        #     f"🚫 Bild ist GRAU! (Sat: {saturation:.2f}, Var: {color_variance:.2f})")
        return False

    return True


def find(image_name) -> tuple[int, int] | None:
    """Sucht das Bild auf dem Bildschirm und gibt die Koordinaten zurück, falls gefunden."""
    image_path = os.path.join(image_folder, image_name)

    if not os.path.exists(image_path):
        print(f"⚠ Fehler: Bild '{image_path}' nicht gefunden!")
        return None

    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot_match = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    template = cv2.imread(image_path, 0)
    if template is None:
        print(f"⚠ Fehler: Bild '{image_path}' konnte nicht geladen werden!")
        return None

    found_position: tuple[int, int] | None = None
    top_left = -1
    bottom_right = -1

    for scale in np.linspace(0.8, 1.5, 10):
        resized: cv2.typing.MatLike = cv2.resize(
            template, None, fx=scale, fy=scale)
        w, h = resized.shape[::-1]
        result: cv2.typing.MatLike = cv2.matchTemplate(
            screenshot_match, resized, cv2.TM_CCOEFF_NORMED)

        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.75:
            top_left = max_loc
            bottom_right = (max_loc[0] + w, max_loc[1] + h)
            center_x = max_loc[0] + resized.shape[1] // 2
            center_y = max_loc[1] + resized.shape[0] // 2
            found_position = center_x, center_y
            # print(
            #     f"✅ Bild gefunden bei: X1,Y1={str(top_left)}, X2,Y2={str(bottom_right)}, für Weite={w} und Höhe={h} ,Skalierung={round(scale, 2)}")
            break

    if not found_position:
        print(f"❌ Bild '{image_name}' NICHT gefunden!")
        return None
    # Hier wird im originale Screenshot der gefundene Gobblin ausgeschnitten
    croppedMatchImg = screenshot[top_left[1]
        :bottom_right[1], top_left[0]:bottom_right[0]]
    croppedMatchImg = cv2.cvtColor(croppedMatchImg, cv2.COLOR_BGR2RGB)
    # cv2.imshow("cropped", croppedMatchImg)
    # cv2.waitKey(5)
    # Hier wird geprüft, ob der Gobblin auch farbig ist.
    if not is_colored(croppedMatchImg):
        print(f"❌ Farbiges Bild '{image_name}' NICHT gefunden!")
        # print("Bild hat keine farbe")
        return None  # Falls das Bild zu farblos ist, wird es ignoriert
    print(
        f"✅ Bild '{image_name}' gefunden bei: X={center_x}, Y={center_y}, Skalierung={round(scale, 2)}")
    return found_position


def find_and_click(image_name):
    """Sucht das Bild, bewegt die Maus dorthin und klickt."""
    coords = find(image_name)
    if coords:
        time.sleep(1)
        pyautogui.moveTo(coords[0], coords[1], duration=0.5)
        time.sleep(0.5)
        pyautogui.click()
        return True
    return False


def Xschließen():
    if find_and_click("closeShop.PNG"):
        time.sleep(1)


def BaseSuchen():
    if find_and_click("Angriff.PNG"):
        time.sleep(1)
        if find_and_click("kampf_finden.PNG"):
            print("🔍 Base suchen...")
            time.sleep(5)


def TruppSetzen():

    if find_and_click("Spawn.png"):
        print("Truppe wird platzier")
        for _ in range(2):
            mouse.click('left')
    elif find_and_click("Spawn2.png"):
        print("Truppe wird platzier")
        for _ in range(2):
            mouse.click('left')
    elif find_and_click("Spawn3.png"):
        print("Truppe wird platzier")
        for _ in range(2):
            mouse.click('left')

    # find_and_click("Spawn.png")
    # for unit in ("Spawn.png", "Spawn2.png", "Spawn3.png"):
    #     if find_and_click(unit):
    #         print("Truppe wird platzier")
    #         for _ in range(2):
    #             mouse.click('left')


def Angriff():

    # if find_and_click("Dragons.PNG"):
    #     print("🎯 'Dragons' gefunden! Klicke 8-mal darauf...")
    #     find_and_click("Spawn.png")
    #     for _ in range(7):
    #         mouse.click('left')

    #     print("🖱️ Drache platziert!")

    # if find_and_click("WWEEvent.png"):
    #     TruppSetzen()

    # if find("Goblins.png"):
    #     #     if find("GoblinsGrau.png"):
    #     #         print("goblin sind grau")
    #     print("Farbiger Goblins gefunden")
    # else:
    #     #         find_and_click("Goblins.png")
    #     #         time.sleep(2)
    #     #         TruppSetzen()
    #     # else:
    #     print("Farbiger Goblins Nicht gefunden")
    for unit in ("Barbaren.png", "Goblins.png"):
        if find_and_click(unit):
            print("🎯 'Trupp' gefunden!")
            time.sleep(1)
            actions_position = ["Spawn.png", "Spawn2.png", "Spawn3.png"]
            while len(actions_position) > 0:
                while find(unit) and find_and_click(actions_position[0]):
                    print(f"🖱️ {unit.replace('.png', '')} platziert!")
                    for _ in range(5):
                        time.sleep(0.2)
                        mouse.click('left')
                actions_position = actions_position[1:]  # []

    for unit in ["BarbKing.PNG", "ArcherQueen.PNG", "Warden.PNG",]:
        if find_and_click(unit):
            print(f"🖱️ {unit.replace('.PNG', '')} platziert!")
            TruppSetzen()

    if find_and_click("AttackMainBaseReturnHome.PNG"):
        print("Der Kampf ist vorbei")
        time.sleep(1)


time.sleep(2)
while True:
    Xschließen()
    BaseSuchen()
    Angriff()
    time.sleep(4)
    # find()
