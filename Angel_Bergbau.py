import time
import keyboard
import mouse
import numpy as np
import pyautogui
from PIL import ImageGrab

# import Captchaerkunng.googlevisiontest as Captchalösen

global stop
stop = True


def inColorRange(inputPixel, minPixelRange, maxPixelRange):
    for pos in range(3):
        # Erster Fall, zu niedrig
        if inputPixel[pos] < minPixelRange[pos]:
            return False
        # Zweiter Fall, zu hoch
        if inputPixel[pos] > maxPixelRange[pos]:
            return False
    return True


def pixelabfrage(game_coords):
    screenshot = ImageGrab.grab(
        bbox=game_coords, include_layered_windows=True, all_screens=True)
    erkennung = np.array(screenshot)
    # print(str(screenshot))
    xlen = len(erkennung)
    ylen = len(erkennung[0])

    # print("x:" + str(xlen) + " y:" + str(ylen))
    midX = xlen // 2
    midY = ylen // 2
    return erkennung[midX, midY]


def Captcha():
    pixel = pixelabfrage([869, 751, 870, 752])
    minColor = [210, 190, 40]  # Minimun farbe range
    maxColor = [255, 225, 50]  # Maximum farbe rangexe
    if inColorRange(pixel, minColor, maxColor):
        print(f"R:G:B {pixel}")
        print("erkannt")
        return True
    print(f"R:G:B {pixel}")
    print("nicht erkannt")
    return False


def Ebereit():
    pixel = pixelabfrage([932, 561, 933, 562])
    minColor = [254, 254, 254]  # Minimun farbe range
    maxColor = [254, 255, 255]  # Maximum farbe rangexe
    if inColorRange(pixel, minColor, maxColor):
        print(f"R:G:B {pixel}")
        print("E erkannt")
        return True
    print(f"R:G:B {pixel}")
    print("E nicht erkannt")
    return False


def ObCaptchada():
    time.sleep(0.5)

    while Captcha():
        print("test")
        time.sleep(1)


def eDrücken():
    print("E wird gehalten")

    pyautogui.keyDown('e')

    if stop == True:
        print("wait")

    time.sleep(6)

    print("Taste wird losgelassen")

    pyautogui.keyUp('e', _pause=False)

    print("Warte bis nächste runde")

    time.sleep(7)


pyautogui.FAILSAFE = False


def start_event():
    global stop
    stop = False
    print("Start")


def stop_event():
    global stop
    stop = True
    print("Wird Pausiert")


keyboard.add_hotkey('x', lambda: start_event())
keyboard.add_hotkey('e', lambda: stop_event())

while True:

    # warten bis eingabe dann start
    print("Zum Starten x drücken d und e zum Pausieren")
    while stop == True:
        time.sleep(2)

    while stop == False:

        if Captcha():
            time.sleep(0.5)
            # Captchalösen.lösencaptcha()

        eDrücken()
