import os 
import keyboard
import mouse
import time
import pyautogui
from pathlib import Path
import subprocess
from PIL import ImageGrab
import numpy as np

def password():
    print("Password eingabe wurde erkannt.")
    pyautogui.moveTo(562,566,duration=0.5)
    time.sleep(4)
    mouse.click('left')
    print("Password wird eingegeben.")
    time.sleep(4)
    keyboard.write('HIER PASSWORD EINGEBEN') # hier password eingeben 
    time.sleep(4)
    print("Accoount wird eingeloggt.")
    pyautogui.moveTo(651,678,duration=0.5)
    time.sleep(4)
    mouse.click('left')
    print("Login Fertig.")

def ispasswordabfrage(game_coords):
    screenshot = ImageGrab.grab(
        bbox=game_coords, include_layered_windows=True, all_screens=True)
    erkennung = np.array(screenshot)
    # print(str(screenshot))
    xlen = len(erkennung)
    ylen = len(erkennung[0])

    # print("x:" + str(xlen) + " y:" + str(ylen))
    midX = xlen // 2
    midY = ylen // 2

    # print("mitte: x:" + str(midX) + " y:" + str(midY))

    r = erkennung[midX, midY][0]
    g = erkennung[midX, midY][1]
    b = erkennung[midX, midY][2]
    if 240 <= r and 64 >= g and 90 >= b:
        print("r:", r,"g:",g,"b:",b)
        return True
    print("r:", r,"g:",g,"b:",b)
    return False

def isSpielAn(game_coords):
    screenshot = ImageGrab.grab(
        bbox=game_coords, include_layered_windows=True, all_screens=True)
    erkennung = np.array(screenshot)
    # print(str(screenshot))
    xlen = len(erkennung)
    ylen = len(erkennung[0])

    # print("x:" + str(xlen) + " y:" + str(ylen))
    midX = xlen // 2
    midY = ylen // 2

    # print("mitte: x:" + str(midX) + " y:" + str(midY))

    r = erkennung[midX, midY][0]
    g = erkennung[midX, midY][1]
    b = erkennung[midX, midY][2]
    if [254, 233, 53] == [r, g, b]:
        print("r:", r,"g:",g,"b:",b)
        return True
    print("r:", r,"g:",g,"b:",b)
    return False

def werberbannerda(game_coords):
    screenshot = ImageGrab.grab(
        bbox=game_coords, include_layered_windows=True, all_screens=True)
    erkennung = np.array(screenshot)
    xlen = len(erkennung)
    ylen = len(erkennung[0])
    midX = xlen // 2
    midY = ylen // 2

    r = erkennung[midX, midY][0]
    g = erkennung[midX, midY][1]
    b = erkennung[midX, midY][2]

    # wenn nicht geld dann wiederholen

    if [254, 233, 53] == [r, g, b]:
        
        return True
    # print("r:", r,"g:",g,"b:",b)
    return False

def loginscreenfertig(game_coords):
    screenshot = ImageGrab.grab(
        bbox=game_coords, include_layered_windows=True, all_screens=True)
    erkennung = np.array(screenshot)
    # print(str(screenshot))
    xlen = len(erkennung)
    ylen = len(erkennung[0])

    rightX = xlen -1
    rightY = ylen -1

    r = erkennung[rightX, rightY][0]
    g = erkennung[rightX, rightY][1]
    b = erkennung[rightX, rightY][2]
    if 55 <= r and 48 <= g and 61 >= b: 
        print("r:", r,"g:",g,"b:",b)
        return True
    print("r:", r,"g:",g,"b:",b)
    return False

def SpielBeenden():
    print("Alle programme werden beendet.")
    os.system("taskkill /f /im GTA5.exe")
    time.sleep(3)
    os.system("taskkill /f /im Launcher.exe")
    time.sleep(3)
    os.system("taskkill /f /im LauncherPatcher.exe")
    time.sleep(3)
    os.system("taskkill /f /im ragemp_v.exe")
    time.sleep(3)
    os.system("taskkill /f /im PlayGTAV.exe")

def startding():
    print("Rage wird gestarted.")
    os.system("start \"RageMp\" /d C:\\RAGEMP C:\\GrandRPLauncher\\RAGEMP\\updater.exe") #Pfad von rage updater mit doppel // ,weil wenn nur 1 / dann wird es als leerrzeichen erkannt.
    # print("Programm öffnen")

def RageMPconnenct():
    print("Auf Grand connecten.")
    pyautogui.moveTo(1357,217,duration=0.5)
    time.sleep(2)
    mouse.click('left')
    time.sleep(2)
    pyautogui.moveTo(864,557,duration=0.5)
    time.sleep(2)
    mouse.click('left')
    mouse.click('left')
    mouse.click('left')
    time.sleep(2)
    keyboard.write("de.gta5grand.com")
    pyautogui.moveTo(1146,563,duration=0.5)
    time.sleep(2)
    mouse.click('left')

def SpawnPunkt():
    print("Spawnpunkt am Familienhaus wird ausgewählt.")
    pyautogui.moveTo(197,595,duration=0.5)
    time.sleep(10)
    mouse.click('left')
    # time.sleep(3)
    # keyboard.press_and_release('esc')
    # time.sleep(2)
    # keyboard.press_and_release('esc')

def PressA():
    keyboard.press('a')
    time.sleep(0.1)
    keyboard.release('a')
    print("A wird gedrückt")

def PressD():
    keyboard.press('d')
    time.sleep(0.1)
    keyboard.release('d')
    print("D wird gedrückt")

def PressW():
    keyboard.press('w')
    time.sleep(0.1)
    keyboard.release('w')   
    print("W wird gedrückt") 

def warten():
    print("10 Sekunden Pause")
    time.sleep(10)

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
keyboard.add_hotkey('e', lambda: stop_event())


def solangeSpielAktivIst():
    print("AFK bot wird gestartet.")
    while isSpielAn([1870, 50, 1890, 60]):
            print("Spiel erkannt")
            PressA()
            warten()
            PressD()
            warten()
            PressW()

# alle 5 sekunden überpüfren wenn 3 minuten um dann weiter/ weiter wenn loginscreen da ist
def loginfertig():
    for y in range(150): 
        print("Warte auf login screen")
        # if loginscreenfertig([900, 600, 953, 688]):
        #     print("Login erknannt")
        #     time.sleep(15)
        #     SpawnPunkt()
        #     time.sleep(5)
        #     escbisspielbeginn()
        #     break
        if ispasswordabfrage([1410, 600, 1416, 610]):
            # print("Password eingabe erkannt")
            time.sleep(5)
            password()
            time.sleep(5)
            SpawnPunkt()
            time.sleep(5)
            escbisspielbeginn()
            break
        time.sleep(1)


def escbisspielbeginn():
    for x in range(10): 
        if not werberbannerda([1870, 30, 1900, 60]):
            keyboard.press_and_release('esc')
            time.sleep(2)
        else:
            break

while True:

    # warten bis eingabe dann start
    print("Zum Starten q drücken und e zum Pausieren.")
    while stop == True:
        time.sleep(1)
        # print("warten")

    while stop == False:
        solangeSpielAktivIst()

        time.sleep(2)
        
                
        SpielBeenden()
       
        time.sleep(5)
       
        startding()
       
        time.sleep(5)
       
        RageMPconnenct()
       
        print("Warten 120 Sekunden.")
        time.sleep(120)
        print("Fertig mit warten, login wird abgefragt.")
        # 240 Sekunden warten bis er grün erkennt dann spawn def ausführen, wenn nicht neustart.
        loginfertig()

        time.sleep(5)


    
       