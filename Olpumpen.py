import sys
import time

import keyboard
import mouse
import numpy as np
from PIL import ImageGrab

# game_coords = [653, 347, 1142, 763]

counter = 0


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
    pixel = pixelabfrage([824, 518, 825, 519])
    minColor = [210, 190, 40]  # Minimun farbe range
    maxColor = [255, 255, 255]  # Maximum farbe rangexe
    if inColorRange(pixel, minColor, maxColor):
        # print(f"R:G:B {pixel}")
        return True
    # print(f"R:G:B {pixel}")
    return False


def notonoil():
    pixel = pixelabfrage([1247, 931, 1248, 932])
    minColor = [210, 190, 240]  # Minimun farbe range
    maxColor = [255, 255, 255]  # Maximum farbe rangexe
    if inColorRange(pixel, minColor, maxColor):
        # print(f"R:G:B {pixel}")
        # print("keine Öle erkannt")
        return True
    # print(f"R:G:B {pixel}")
    # print("in Öle  erkannt")
    return False


def ObCaptchada():
    global counter
    time.sleep(0.5)
    while Captcha():
        print("Captcha erkannt")
        time.sleep(3)
    while not notonoil():
        print("Nicht in Öl quelle")
        time.sleep(3)
        counter = 0
        # ObCaptchada()


print("--------------------------------------------------")
selection = input(
    "Boost? (1), kein Boost (2), AFK-Oil (3), Selbstbestimmung (4):")

if selection == '4':
    print("--------------------------------------------------")
    zahl = input("Wie viele sekunden soll gedrückt halten?:")

if int(selection) not in range(1, 4):
    print("Falsche eingabe")
    quit()


def drücken():
    while stop == True:
        time.sleep(1)
        print("Warte")
    mouse.press('left')
    if selection == '1':
        print("Drücken 2.4 sek")
        time.sleep(2.4)
    if selection == '2':
        time.sleep(3.6)
        print("Drücken 3.6 sek")
    if selection == '3':
        print("Drücken 90 sek")
        time.sleep(90)
    if selection == '4':
        # print(f"{zahl} Drücken")
        time.sleep(int(zahl))
    mouse.release('left')
    print("Taste wird gehalten")


def movemouse():
    global counter
    counter += 1
    if counter == 1:
        mouse.move(300, 600, absolute=True)
    elif counter == 2:
        mouse.move(400, 600, absolute=True)
    elif counter == 3:
        mouse.move(500, 600, absolute=True)
    elif counter == 4:
        mouse.move(600, 600, absolute=True)
        counter = 0
    drücken()


global stop
stop = True


def start_event():
    global stop
    stop = False
    print("Start")


def stop_event():
    global stop
    stop = True
    print("Wird Pausiert")


keyboard.add_hotkey('q', lambda: start_event())
keyboard.add_hotkey('h', lambda: stop_event())

while True:

    # warten bis eingabe dann start
    print("Zum Starten q drücken und e zum Pausieren")
    while stop == True:
        time.sleep(1)

    while stop == False:
        ObCaptchada()
        movemouse()
        while stop == True:
            time.sleep(1)
            print("Warte")
            ObCaptchada()
