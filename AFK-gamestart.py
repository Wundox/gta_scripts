import json
import os
import subprocess
import time
from pathlib import Path

import clipboard
import keyboard
import mouse
import numpy as np
import pyautogui
from PIL import ImageGrab

    # def get_password(self):
    #     if os.path.exists("password.json"):
    #         with open("password.json", "r") as file:
    #             data = json.load(file)
    #             return data.get("password")
    #     else:
    #         new_password = input("Bitte geben Sie ein neues Passwort ein: ")
    #         set_password(new_password)
    #         print("Passwort gespeichert!")

    #     return None

class GamesSaveState:
    def __init__(self,password = '',path = ''):
        self.password = password
        self.path = path
        self.create()

    def read_password(self):
        return self.password
    
    def read_path(self):
        return self.path
    
    def write_password(self, password):
        self.password = password
    
    def write_path(self, path):
        self.path = path

    def paste_password(self):
        keyboard.wait("ctrl+v")
        new_password = clipboard.paste()
        self.write_password(new_password)

    def paste_path(self):
        keyboard.wait("ctrl+v")
        new_path = clipboard.paste().strip('"')  # Entfernt Anführungszeichen, wenn sie vorhanden sind
        self.write_path(new_path)

    def password_empty(self):
        return len(self.password) == 0
    
    def path_empty(self):
        return len(self.path) == 0
    
    def create(self):
        if not os.path.exists(self.config_path()):
            os.makedirs(self.config_path())
        if not os.path.exists(self.config_file()):
            self.save()
        self.read()

    def write_data(self):
        return {
            "password": self.password,
            "path": self.path
        }

    def save(self):
        with open(self.config_file(), "+w") as file:
                json.dump(self.write_data(), file)

    def read(self):
        with open(self.config_file(), "r") as file:
            tmp = json.load(file)
            self.password = str(tmp['password'])
            self.path = str(tmp['path'])
    
    def config_path(self):
        return os.path.join(os.getenv('APPDATA'),'grand_afk_game_start')

    def config_file(self):
        return os.path.join(self.config_path(),'config.json')

def prepare() -> GamesSaveState:
    speicherZustand = GamesSaveState()
    if speicherZustand.password_empty():
        # new_password = input("Bitte geben Sie ein neues Passwort ein: ")
        print("Bitte schreiben Sie ein Password ein oder (mit STRG+V): ")
        # speicherZustand.write_password(new_password)
        speicherZustand.paste_password()

    if speicherZustand.path_empty():
        # new_path = input("Bitte geben Sie den Pfad ein: ")
        # speicherZustand.write_path(new_path)
        print("Bitte schreiben Sie den Pfad zur .exe-Datei ein oder (mit STRG+V): ")
        speicherZustand.paste_path()

    speicherZustand.save()
    return speicherZustand

# def set_password(password):
#     data = {"password": password}
#     with open("password.json", "w") as file:
#         json.dump(data, file)

# def schreibpassword(password):
#     # password = get_password()
#     keyboard.write(password)


def password():
    print("Password eingabe wurde erkannt.")
    pyautogui.moveTo(562,566,duration=0.5)
    time.sleep(4)
    mouse.click('left')
    print("Password wird eingegeben.")
    time.sleep(4)
    # keyboard.write('HIER PASSWORD EINGEBEN') # hier password eingeben
    
    keyboard.write(speicherZustand.read_password())
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
    start_path = speicherZustand.read_path()
    start_cmd = "start \"RageMp\" /d C:\\RAGEMP {execution_path}".format(execution_path=start_path)
    os.system(start_cmd) #Pfad von rage updater mit doppel // ,weil wenn nur 1 / dann wird es als leerrzeichen erkannt.
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


def Investion8Stunden():
    print("Investion 8 Stunden wird angenommen")
    # handy rausholen
    time.sleep(1)
    keyboard.press_and_release('k')
    time.sleep(3)
    # investion moven und klicken
    pyautogui.moveTo(1713, 1009,duration=0.5)
    time.sleep(3)
    mouse.click('left')
    time.sleep(3)
    # auf tagsüber moven und klicken
    pyautogui.moveTo(94, 537,duration=0.5)
    time.sleep(3)
    mouse.click('left')
    time.sleep(3)
    # scrollbar moven und klicken
    pyautogui.moveTo(1608, 965,duration=0.5)
    time.sleep(3)
    mouse.click('left')
    time.sleep(1)
    mouse.click('left')
    time.sleep(3)
    # 8 stunden invest 
    pyautogui.moveTo(1451, 866,duration=0.5)
    time.sleep(3)
    mouse.click('left')
    time.sleep(3)
    # annhemen
    pyautogui.moveTo(877, 725,duration=0.5)
    time.sleep(3)
    mouse.click('left')
    time.sleep(3)
    # rausgeben
    keyboard.press_and_release('esc')

def FamAufgabe4Stunden():
    print("Familienaufgabe 4 Stunden wird angenommen")

    # Familienaufgabe annhemen
    time.sleep(1)
    keyboard.press_and_release('m')
    time.sleep(3)
    # auf familie moven
    pyautogui.moveTo(1087, 866,duration=0.5)
    time.sleep(3)
    mouse.click('left')
    time.sleep(3)
    # familien aufgabe
    pyautogui.moveTo(156, 685,duration=0.5)
    time.sleep(3)
    mouse.click('left')
    time.sleep(3)
    # Scrollbar
    pyautogui.moveTo(1510, 1051,duration=0.5)
    time.sleep(3)
    mouse.click('left')
    time.sleep(3)
    # 4 stunden aufgabe annhemen
    pyautogui.moveTo(617, 994,duration=0.5)
    time.sleep(3)
    mouse.click('left')

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


# def istEs(hour=0,minute=0):
#     systemzeit = time.localtime()
#     # zeit_string = time.strftime("%H:%M:%S", systemzeit)
#     return systemzeit.tm_hour == hour and systemzeit.tm_min == minute


def istImZeitraum(start_time=(0,0),end_time=(0,0)):
    systemzeit = time.localtime()
    st = time.localtime()
    from_start = time.struct_time(
        (st.tm_year,)
        + (st.tm_mon,)
        + (st.tm_mday,)
        + (start_time[0],)
        + (start_time[1],)
        + (0,)
        + (st.tm_wday,)
        + (st.tm_yday,)
        + (st.tm_isdst,)
    )
    to_end = time.struct_time(
        (st.tm_year,)
        + (st.tm_mon,)
        + (st.tm_mday,)
        + (end_time[0],)
        + (end_time[1],)
        + (0,)
        + (st.tm_wday,)
        + (st.tm_yday,)
        + (st.tm_isdst,)
    )
    # print(time.strftime("%H:%M:%S", systemzeit))
    # print(time.strftime("%H:%M:%S", from_start))
    # print(time.strftime("%H:%M:%S", to_end))
    if time.mktime(systemzeit) < time.mktime(from_start):
        # zu früh
        return False
    if time.mktime(systemzeit) > time.mktime(to_end):
        # zu spät
        return False
    return True


def solangeSpielAktivIst():
    print("AFK bot wird gestartet.")
    while isSpielAn([1870, 50, 1890, 60]):
            print("Spiel erkannt")
            PressA()
            warten()
            PressD()
            warten()
            PressW()

            # Tagesinvest
            if istImZeitraum((5,1),(5,3)):
                Investion8Stunden()
                FamAufgabe4Stunden()
                time.sleep(300)

            # 4 Uhr neustart
            if istImZeitraum((4,0),(4,2)):
                SpielBeenden()
                time.sleep(300)



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

speicherZustand = prepare()

while True:    
    # warten bis eingabe dann start
    print("Zum Starten q drücken und e zum Pausieren.")
    while stop == True:
        time.sleep(1)
        # print("warten")

    while stop == False:
        # get_password()
        solangeSpielAktivIst()

        time.sleep(5)
        
                
        SpielBeenden()
       
        time.sleep(5)
       
        startding()
        # time.sleep(20)

        time.sleep(5)
       
        RageMPconnenct()
       
        print("Warten 300 Sekunden.")
        time.sleep(300)
        print("Fertig mit warten, login wird abgefragt.")
        # # 240 Sekunden warten bis er grün erkennt dann spawn def ausführen, wenn nicht neustart.
        loginfertig()

        time.sleep(5)


    
       