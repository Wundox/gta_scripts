import json
import os
import time

import clipboard
import keyboard
import mouse
import numpy as np
import pyautogui
from PIL import ImageGrab

pyautogui.FAILSAFE = False

# zeit wie lange W,A,S,D gedrückt wird
press = 0.9
##########################################


def log_to_file(message):
    with open('logfile.txt', 'a') as file:
        timestamp = time.strftime("%d.%m.%Y / %H:%M", time.localtime())
        log_message = f"{timestamp} - {message}\n"
        file.write(log_message)


def print_hour_and_minute():
    current_time = time.localtime()
    formatted_time = time.strftime("%d.%m.%Y / %H:%M", current_time)
    print(f"Aktuelles Datum, Stunde und Minute: {formatted_time} Uhr.")

# Überprüft ob ein Pixel im angegeben Farbraum ist
# inputPixel = [R,G,B] ; Der pixel der überprüft wird
# minPixelRange = [R,G,B] ; Der pixel darf nicht unterschreiten
# maxPixelRange = [R,G,B] ; Der pixel darf nicht überschreiten
# Return: True wenn in Range, ansonsten False


def inColorRange(inputPixel, minPixelRange, maxPixelRange):
    for pos in range(3):
        # Erster Fall, zu niedrig
        if inputPixel[pos] < minPixelRange[pos]:
            return False
        # Zweiter Fall, zu hoch
        if inputPixel[pos] > maxPixelRange[pos]:
            return False
    return True


class GamesSaveState:
    def __init__(self, password='', path='', resolution='1920x1080', waittime='15', relogtime='', autostart='', bunkerspawn=''):
        self.password = password
        self.path = path
        self.resolution = resolution
        self.waittime = waittime
        self.relogtime = relogtime
        self.autostart = autostart
        self.bunkerspawn = bunkerspawn
        self.create()

    def read_waittime(self):
        return self.waittime

    def read_relogtime(self):
        return self.relogtime

    def read_resolution(self):
        return self.resolution

    def read_password(self):
        return self.password

    def read_path(self):
        return self.path

    def read_autostart(self):
        return self.autostart
    
    def read_bunkerspawn(self):
        return self.bunkerspawn

    def write_waittime(self, waittime):
        self.waittime = waittime

    def write_relogtime(self, relogtime):
        self.relogtime = relogtime

    def write_resolution(self, resolution):
        self.resolution = resolution

    def write_password(self, password):
        self.password = password

    def write_path(self, path):
        self.path = path

    def write_autostart(self, autostart):
        self.autostart = autostart

    def write_bunkerspawn(self, bunkerspawn):
        self.bunkerspawn = bunkerspawn

    def paste_password(self):
        keyboard.wait("ctrl+v")
        new_password = clipboard.paste()
        self.write_password(new_password)
    
    def paste_path(self):
        keyboard.wait("ctrl+v")
        # Entfernt Anführungszeichen, wenn sie vorhanden sind
        new_path = clipboard.paste().strip('"')
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
            "path": self.path,
            "resolution": self.resolution,
            "waittime": self.waittime,
            "relogtime": self.relogtime,
            "autostart": self.autostart,
            "bunkerspawn": self.bunkerspawn,
        }

    def save(self):
        with open(self.config_file(), "+w") as file:
            json.dump(self.write_data(), file)

    def _config_read_checker(self, jsonConfigFile, key: str, alternativValue: any) -> str:
        try:
            return str(jsonConfigFile[key])
        except KeyError:
            # Key nicht in Config vorhanden
            return str(alternativValue)

    def read(self):
        with open(self.config_file(), "r") as file:
            tmp = json.load(file)
            self.password = self._config_read_checker(
                tmp, 'password', self.password)
            self.path = self._config_read_checker(
                tmp, 'path', self.path)
            self.resolution = self._config_read_checker(
                tmp, 'resolution', self.resolution)
            self.waittime = self._config_read_checker(
                tmp, 'waittime', self.waittime)
            self.relogtime = self._config_read_checker(
                tmp, 'relogtime', self.relogtime)
            self.autostart = self._config_read_checker(
                tmp, 'autostart', self.autostart)
            self.bunkerspawn = self._config_read_checker(
                tmp, 'bunkerspawn', self.bunkerspawn)

    def config_path(self):
        return os.path.join(os.getenv('APPDATA'), 'grand_afk_game_start')

    def config_file(self):
        return os.path.join(self.config_path(), 'config.json')


def prepare() -> GamesSaveState:
    speicherZustand = GamesSaveState()
    if speicherZustand.read_autostart() == "JA":
        print("Autostart wird verwenden")
        log_to_file("Autostart wird verwenden")
        return speicherZustand

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

    print('Wartzeit zwischen den ausführungen:')
    print('    Letzte verwendete Zeit ' + str(speicherZustand.read_waittime()))
    print('    Gibt eine Zeit ein zwischen den ausführungen. Am besten für Langsame PCs ca 20sek ')
    print('    0. Standard 15 Sekunden')
    current_wait = input('Zahl eingeben: ')
    speicherZustand.write_waittime(f"{current_wait}")
    match int(current_wait):
        case 0:
            speicherZustand.write_waittime('15')
    print('Verwende Zeit: ' + str(speicherZustand.read_waittime()), 'sekunden.')
    log_to_file("Verwendete Zeit = " + str(speicherZustand.read_waittime()))


    print('Willst du um 15 Uhr und um 20Uhr ein Relog machen?')
    print('    1. Für JA')
    print('    2. Für NEIN')
    current_relog = input('Zahl eingeben: ')
    match int(current_relog):
        case 1:
            speicherZustand.write_relogtime('JA')
        case 2:
            speicherZustand.write_relogtime('NEIN')

    print(speicherZustand.read_relogtime()+' wird gespeicher')
    log_to_file(speicherZustand.read_relogtime()+' wird gespeicher')

    print('Wo Willst du Spawnen?')
    print('    1. Im Bunker')
    print('    2. Im Familienhaus')
    print('    3. Eine Custom Koordinate')
    current_relog = input('Zahl eingeben: ')
    match int(current_relog):
        case 1:
            speicherZustand.write_bunkerspawn('JA')
        case 2:
            speicherZustand.write_bunkerspawn('NEIN')
        case 3:
            speicherZustand.write_bunkerspawn('3')
        
    if speicherZustand.read_bunkerspawn() == "3":
        print("Bitte tippe deine Koordinaten ein bsp: 123, 123 ")
        current_relog = input('Zahl eingeben: ')
        speicherZustand.write_bunkerspawn(f'{current_relog}')
    
    print(speicherZustand.read_bunkerspawn()+' wird gespeicher')
    log_to_file(speicherZustand.read_bunkerspawn()+' wird gespeicher')

    print('Willst Autostart aktivieren?')
    print('    1. Für JA')
    print('    2. Für NEIN')
    current_relog = input('Zahl eingeben: ')
    match int(current_relog):
        case 1:
            speicherZustand.write_autostart('JA')
        case 2:
            speicherZustand.write_autostart('NEIN')

    print(speicherZustand.read_autostart()+' wird gespeicher')
    log_to_file(speicherZustand.read_autostart()+' wird gespeicher')

    if isSpielAn([1870, 50, 1880, 55]):
        speicherZustand.write_resolution('1920x1080')
    elif isSpielAn([1334, 269, 1335, 270]):
        speicherZustand.write_resolution('800x600')
    else:
        print('Verwende Auflösung: ' + str(speicherZustand.read_resolution()))
        print('Kein aktives Spiel erkannt')
        print('Bitte benutze eins von den Verfügbaren Auflösungen:')
        print('    1. 1920x1080')
        print('    2. 800x600 randlos')
        print('    3. Quit')
        current_res = input('Zahl eingeben: ')
        match int(current_res):
            case 1:
                speicherZustand.write_resolution('1920x1080')
            case 2:
                speicherZustand.write_resolution('800x600')

    

    print(speicherZustand.read_resolution()+' Verwende Auflösung')
    log_to_file(speicherZustand.read_resolution()+' Verwende Auflösung')

    speicherZustand.save()
    return speicherZustand


def password():
    print("Password eingabe wurde erkannt.")
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(562, 566, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(851, 550, duration=0.5)
    else:
        print('falsche auflösung')

    warten()
    mouse.click('left')
    print("Password wird eingegeben.")
    warten()
    # keyboard.write('HIER PASSWORD EINGEBEN') # hier password eingeben

    keyboard.write(speicherZustand.read_password())
    warten()
    print("Accoount wird eingeloggt.")
    LoginButton()
    print("Login Fertig.")


def LoginButton():
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(651, 678, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(848, 580, duration=0.5)
    else:
        print('falsche auflösung')

    warten()
    mouse.click('left')


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


def ispasswordabfrage(coord):
    pixel = pixelabfrage(coord)
    minColor = [237, 60, 86]  # Minimun farbe range
    maxColor = [245, 64, 91]  # Maximum farbe range
    if inColorRange(pixel, minColor, maxColor):
        log_to_file(f"Password eingabe erkannt. R:G:B {pixel}")
        return True
    log_to_file(f"keine Password eingabe erkannt. R:G:B {pixel}")
    return False


def isSpielAn(coord):
    pixel = pixelabfrage(coord)
    minColor = [249, 225, 50]
    maxColor = [255, 235, 63]  # Maximum farbe range
    if inColorRange(pixel, minColor, maxColor):
        log_to_file(f"Gelbe 1 erkannt. R:G:B {pixel}")
        return True
    log_to_file(f"Gelbe 1 nicht erkannt. R:G:B {pixel}")
    # print(coord)
    return False


def istgrandcoinssliderda(coord):
    pixel = pixelabfrage(coord)
    minColor = [239, 184, 36]
    maxColor = [245, 188, 40]  # Maximum farbe range
    if inColorRange(pixel, minColor, maxColor):
        log_to_file(f"grand coins slider erkannt. R:G:B {pixel}")
        return True
    log_to_file(f"Grandcoin slider nicht erkannt. R:G:B {pixel}")
    return False


def IsServerFull(coord):
    pixel = pixelabfrage(coord)
    minColor = [237, 60, 86]  # Minimun farbe range
    maxColor = [245, 64, 91]  # Maximum farbe range
    if inColorRange(pixel, minColor, maxColor):
        log_to_file(f"Server Full. R:G:B {pixel}")
        return True
    log_to_file(f"Server nicht Full. R:G:B {pixel}")
    return False


def IstHausda(coord): 
    pixel = pixelabfrage(coord)
    minColor = [150, 135,  28]  # Minimun farbe range
    maxColor = [255, 225, 50]  # Maximum farbe range
    if inColorRange(pixel, minColor, maxColor):
        log_to_file(f"Haus erkannt. R:G:B {pixel}")
        return True
    log_to_file(f"Kein Haus erkannt. R:G:B {pixel}")
    return False


def investfertig(coord):
    pixel = pixelabfrage(coord)
    minColor = [248, 218, 37]  # Minimun farbe range
    maxColor = [255, 230, 47]  # Maximum farbe range
    if inColorRange(pixel, minColor, maxColor):
        log_to_file(f"Invest ist Fertig. R:G:B {pixel}")
        print("Invest ist Fertig")
        return True
    log_to_file(f"Invest ist nicht Fertig. R:G:B {pixel}")
    print("Invest ist nicht Fertig")
    return False

# Überpürft ob charakter gestorben ist
def Istgestorben(coord):
    pixel = pixelabfrage(coord) 
    minColor = [250, 200, 1]  # Minimun farbe range
    maxColor = [255, 210, 6]  # Maximum farbe range
    if inColorRange(pixel, minColor, maxColor):
        log_to_file("Charakter ist Gestorben")
        print("Charakter ist Gestorben")
        return True
    return False

def SpielBeenden():
    print("Alle programme werden beendet.")
    log_to_file("Alle programme werden Beendet")
    print_hour_and_minute()
    os.system("taskkill /f /im GTA5.exe")
    warten()
    os.system("taskkill /f /im Launcher.exe")
    warten()
    os.system("taskkill /f /im LauncherPatcher.exe")
    warten()
    os.system("taskkill /f /im ragemp_v.exe")
    warten()
    os.system("taskkill /f /im PlayGTAV.exe")
    warten()
    os.system("taskkill /f /im updater.exe")
    warten()
    os.system("taskkill /f /im steam.exe")


def startding():
    log_to_file("RageMP wird gestart")
    print("Rage wird gestarted.")
    print_hour_and_minute()
    start_path = speicherZustand.read_path()
    exec_path = "\\".join(start_path.split("\\")[:2])
    start_cmd = "start \"RageMp\" /d {exec_path} {execution_path}".format(
        execution_path=start_path,
        exec_path=exec_path)
    os.system(start_cmd)
    warten()
    # os.system("switch.bat \"RageMp\"")


def RageMPconnenct():
    log_to_file("Ragemp Connect")
    print("Auf Grand connecten.")
    warten()
    print_hour_and_minute()
    pyautogui.moveTo(1357, 217, duration=0.5)
    warten()
    mouse.click('left')
    warten()
    pyautogui.moveTo(864, 557, duration=0.5)
    warten()
    mouse.click('left')
    mouse.click('left')
    mouse.click('left')
    warten()
    keyboard.write("de.gta5grand.com")
    pyautogui.moveTo(1146, 563, duration=0.5)
    warten()
    mouse.click('left')

def Charakterauswahl():
    log_to_file("Charakterauswahl")
    print("Charakterauswahl")
    print_hour_and_minute()
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1700, 982, duration=0.5) 
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1269, 803, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')

def SpawnPunkt():
    warten()
    if speicherZustand.read_bunkerspawn() == 'JA':
        log_to_file("Wird beim Bunker gespawnt")
        print("Wird beim Bunker gespawnt")
        print_hour_and_minute()
        if speicherZustand.read_resolution() == '1920x1080':
            pyautogui.moveTo(798, 935, duration=0.5) 
        elif speicherZustand.read_resolution() == '800x600':
            pyautogui.moveTo(895, 778, duration=0.5)
        else:
            print('falsche auflösung')

    elif speicherZustand.read_bunkerspawn() == 'NEIN':
        log_to_file("Wird bei familie gespawnt")
        print("Wird bei familie gespawnt")
        print_hour_and_minute()
        if speicherZustand.read_resolution() == '1920x1080':
            pyautogui.moveTo(197, 595, duration=0.5)
        elif speicherZustand.read_resolution() == '800x600':
            pyautogui.moveTo(640, 562, duration=0.5)
        else:
            print('falsche auflösung')

    else:
        log_to_file(speicherZustand.read_bunkerspawn()+' Wird als Spawn genutzt')
        print(speicherZustand.read_bunkerspawn()+' Wird als Spawn genutzt')
        # Funktion aufrufen, um den String zu bekommen
        bunkerspawn_str = speicherZustand.read_bunkerspawn() 

        # String in x und y umwandeln
        x_str, y_str = bunkerspawn_str.split(',')
        x, y = int(x_str.strip()), int(y_str.strip())

        # Maus bewegen
        pyautogui.moveTo(x, y, duration=0.5)
        print_hour_and_minute()
        
    

    warten()
    mouse.click('left')


def PressW():
    keyboard.press('w')
    time.sleep(press)
    keyboard.release('w')
    print("W wird gedrückt")


def PressA():
    keyboard.press('a')
    time.sleep(press)
    keyboard.release('a')
    print("A wird gedrückt")


def PressS():
    keyboard.press('s')
    time.sleep(press)
    keyboard.release('s')
    print("D wird gedrückt")


def PressD():
    keyboard.press('d')
    time.sleep(press)
    keyboard.release('d')
    print("D wird gedrückt")


def warten():
    print(f"{speicherZustand.read_waittime()} Sekunden Pause")
    time.sleep(int(speicherZustand.read_waittime()))


def GrandCoinSlider20hours():  # noch nicht fertig
    # investion moven und klicken
    coord = []
    if speicherZustand.read_resolution() == '1920x1080':
        coord = [950, 920, 960, 930]
    elif speicherZustand.read_resolution() == '800x600':
        coord = [950, 920, 960, 930]
    else:
        print('falsche auflösung')
    if istgrandcoinssliderda(coord):
        log_to_file("Grand coin slider erkannt")
        print("Grand Coins erkannt")
        # auf coins slider
        if speicherZustand.read_resolution() == '1920x1080':
            pyautogui.moveTo(950, 804, duration=0.5)
        elif speicherZustand.read_resolution() == '800x600':
            pyautogui.moveTo(950, 804, duration=0.5)
        else:
            print('falsche auflösung')
        warten()
        # coin slider ziehen
        if speicherZustand.read_resolution() == '1920x1080':
            pyautogui.dragTo(956, 329, 1, button='left')
        elif speicherZustand.read_resolution() == '800x600':
            pyautogui.dragTo(956, 329, 1, button='left')
        else:
            print('falsche auflösung')
        warten()
        # auf fertig drücken
        if speicherZustand.read_resolution() == '1920x1080':
            pyautogui.moveTo(950, 804, duration=0.5)
        elif speicherZustand.read_resolution() == '800x600':
            pyautogui.moveTo(950, 804, duration=0.5)
        else:
            print('falsche auflösung')

        warten()
        mouse.click('left')


def escbis20sdtSlider():  # noch nicht fertig
    for x in range(10):
        coord = []
        if speicherZustand.read_resolution() == '1920x1080':
            coord = [950, 920, 960, 930]
        elif speicherZustand.read_resolution() == '800x600':
            coord = [950, 920, 960, 930]
        else:
            print('falsche auflösung')

        if not istgrandcoinssliderda(coord):
            log_to_file("Kein grandcoin slider erkannt")
            print("Esc bis Grandcoinslider")
            print_hour_and_minute()
            keyboard.press_and_release('esc')
            warten()
        else:
            print_hour_and_minute()
            break


def Tagesinvest():
    print("Investion 8 Stunden wird abgeholt")
    log_to_file("8 Stunden invest wird abgeholt")
    # handy rausholen
    warten()
    keyboard.press_and_release('k')
    warten()
    # investion moven und klicken
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1720, 449, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600': 
        pyautogui.moveTo(1277, 581, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()
    # auf tagsüber moven und klicken
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(94, 537, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(598, 535, duration=0.5)
    else:
        print('falsche auflösung')

    warten()
    mouse.click('left')
    warten()
    # scrollbar moven und klicken
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1608, 965, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1230, 697, duration=0.5)
    else:
        print('falsche auflösung')

    warten()
    mouse.click('left')
    warten()
    mouse.click('left')
    warten()

    # Überprüfen ob Gewinn abhol bereit ist /gelb
    coord = []
    if speicherZustand.read_resolution() == '1920x1080':
        coord = [1531, 861, 1532, 862]
    elif speicherZustand.read_resolution() == '800x600':
        coord = [1198, 671, 1199, 672]
    else:
        print('falsche auflösung')

    # 8 stunden invest

    # annhemen
    if not investfertig(coord):
        if speicherZustand.read_resolution() == '1920x1080':
            pyautogui.moveTo(1451, 866, duration=0.5)
        elif speicherZustand.read_resolution() == '800x600':
            pyautogui.moveTo(1159, 674, duration=0.5)
        else:
            print('falsche auflösung')

        warten()
        mouse.click('left')

        if speicherZustand.read_resolution() == '1920x1080':
            pyautogui.moveTo(1047, 701, duration=0.5)
        elif speicherZustand.read_resolution() == '800x600':
            pyautogui.moveTo(995, 612, duration=0.5)
        else:
            print('falsche auflösung')
    else:

        if speicherZustand.read_resolution() == '1920x1080':
            pyautogui.moveTo(1451, 866, duration=0.5)
        elif speicherZustand.read_resolution() == '800x600':
            pyautogui.moveTo(1159, 674, duration=0.5)
        else:
            print('falsche auflösung')

    warten()
    mouse.click('left')
    warten()
    keyboard.press_and_release('esc')
    warten()


def Loginbonus():
    print("Loginbonus wird abgeholt")
    log_to_file("Loginbonus wird abgeholt")

    # M Drücken
    warten()
    keyboard.press_and_release('m')
    warten()

    # Tägliche Aufgabe
    if speicherZustand.read_resolution() == '1920x1080': 
        pyautogui.moveTo(185, 1008, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(600, 818, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()

    # Zu dem Täglichen Belohnungen
    if speicherZustand.read_resolution() == '1920x1080': 
        pyautogui.moveTo(1304, 154, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1098, 377, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()

    escbisspielbeginn()


def FamAufgabe4Stunden():
    print("Familienaufgabe 4 Stunden wird angenommen")
    log_to_file("Familienaufgabe 4 Stunden wird angenommen")

    # Familienaufgabe annhemen
    warten()
    keyboard.press_and_release('m')
    warten()
    # auf familie moven
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1087, 866, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1010, 761, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()
    # familien aufgabe
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(158, 617, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(624, 578, duration=0.5)
    else:
        print('falsche auflösung')

    warten()
    mouse.click('left')
    warten()
    
    # 4 stunden aufgabe annhemen
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1835, 927, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1334, 701, duration=0.5)
    else:
        print('falsche auflösung')

    warten()
    mouse.click('left')


def Geld80std():
    print("80 Stunden werden abgeholt")
    log_to_file("80 Stunden werden abgeholt")
    warten()
    keyboard.press_and_release('m')
    warten()

    # Auf werbeprogramm ziehen und klicken
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1901, 1015, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1355, 819, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()

    # Einsammeln ziehen und drücken
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1419, 914, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1155, 694, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    time.sleep(1)
    mouse.click('left')
    escbisspielbeginn()


def Unternehmenbezhalen():
    print("Unternehmen bezhalen ")
    log_to_file("Unternehmen bezhalen")
    warten()
    bankapp()
    warten()
    # In Bank app auf Unternehmen ziehen und klicken
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1438, 600, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1161, 637, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()
    hauserkennung()
    warten()
    keyboard.press_and_release('esc')
    

def bunkerbezahlen():
    print("Bunker bezahlen")
    log_to_file("Bunker bezahlen")
    warten()
    keyboard.press_and_release('k')
    warten()
    # im handy auf Bunker ziehen und klicken
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1507, 461, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1186, 582, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()
    # Auf Bezahlen für den Bunker ziehen un klicken
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1524, 336, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1201, 451, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()
    hauserkennung()


# ersten mal weiter wo alle häuser sichtbar


def hausauswahlweiter():  # fertig
    if speicherZustand.read_resolution() == '1920x1080':  # fertig
        pyautogui.moveTo(1044, 757, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':  # fertig
        pyautogui.moveTo(997, 627, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()


# weiter klicken wenn haus da ist
def hausweiterklicken():
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1044, 757, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(997, 627, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()

# Überprüfen ob Haus das ist weiter symbol


def hauserkennung():
    coord = []
    if speicherZustand.read_resolution() == '1920x1080':
        coord = [1001, 719, 1002, 720]
    elif speicherZustand.read_resolution() == '800x600':
        coord = [976, 616, 977, 617]
    else:
        print('falsche auflösung')
    warten()
    if IstHausda(coord):
        log_to_file("Haus/Bunker/Unternehmen wurde erkannt")
        print_hour_and_minute()
        print("Haus/Bunker/Unternehmen wurde erkannt")
        # Auf eingabe ziehen und klicken
        if speicherZustand.read_resolution() == '1920x1080':  # fertig
            pyautogui.moveTo(958, 590, duration=0.5)
        elif speicherZustand.read_resolution() == '800x600':  # fertig
            pyautogui.moveTo(963, 560, duration=0.5)
        else:
            print('falsche auflösung')

        warten()
        mouse.click('left')
        warten()
        keyboard.write('1')
        warten()

        # Auf weiter klicken
        hausweiterklicken()

        # Zahlung bestätigen
        if speicherZustand.read_resolution() == '1920x1080':  # fertig
            pyautogui.moveTo(1026, 655, duration=0.5)
        elif speicherZustand.read_resolution() == '800x600':  # fertig
            pyautogui.moveTo(990, 586, duration=0.5)
        else:
            print('falsche auflösung')
        warten()
        mouse.click('left')
        warten()
    else:
        log_to_file("Haus/Bunker/Unternehmen wurde Nicht erkannt")
        print("Haus/Bunker/Unternehmen nicht erkannt")
        print_hour_and_minute()

# In Bank App, Bezahlung Haus Klicken

def bankapphausbezhalen():
    print("Haus bezahlen")
    log_to_file("Haus bezahlen")
    if speicherZustand.read_resolution() == '1920x1080': 
        pyautogui.moveTo(1663, 483, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':
        pyautogui.moveTo(1260, 593, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()


def bankapp():
    print("Bank App öffnen")
    log_to_file("Bank App öffnen")
    warten()
    keyboard.press_and_release('k')
    warten()
    # Auf bank ziehen und klicken
    if speicherZustand.read_resolution() == '1920x1080':
        pyautogui.moveTo(1503, 723, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600': 
        pyautogui.moveTo(1186, 691, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()


def Hausbezahlen():
    print("Haus bezahlen")
    log_to_file("Haus bezahlen")
    bankapp()
    warten()
    Haus1()
    warten()
    Haus2()
    warten()
    Haus3()
    warten()
    Haus4()
    warten()
    keyboard.press_and_release('esc')


def Haus1():
    bankapphausbezhalen()

    # Haus 1 zeiehn klick #fertig
    if speicherZustand.read_resolution() == '1920x1080':  #
        pyautogui.moveTo(944, 380, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':  # fertig
        pyautogui.moveTo(956, 474, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()

    # Aus Weiter ziehen klikc #fertig
    hausauswahlweiter()

    # Überprüfung ob  Haus zu bezahlen ist
    hauserkennung()


def Haus2():
    bankapphausbezhalen()

    # Haus  zeiehn klick #fertig
    if speicherZustand.read_resolution() == '1920x1080': 
        pyautogui.moveTo(959, 472, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':  # fertig
        pyautogui.moveTo(959, 510, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()

    # Aus Weiter ziehen klikc #fertig
    hausauswahlweiter()

    # Überprüfung ob  Haus zu beazheln ist da ist
    hauserkennung()


def Haus3():
    bankapphausbezhalen()

    # Haus 1 zeiehn klick #fertig
    if speicherZustand.read_resolution() == '1920x1080':  # fertig für jeden Hasus machen
        pyautogui.moveTo(954, 561, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':  # fertig
        pyautogui.moveTo(956, 542, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()

    # Aus Weiter ziehen klikc #fertig
    hausauswahlweiter()

    # Überprüfung ob  Haus zu beazheln ist da ist
    hauserkennung()


def Haus4():
    bankapphausbezhalen()
    # # auf scrollbar ziehen
    # if speicherZustand.read_resolution() == '1920x1080':
    #     pyautogui.moveTo(945, 648, duration=0.5)
    # elif speicherZustand.read_resolution() == '800x600':  # fertig
    #     pyautogui.moveTo(1033, 579, duration=0.5)
    # else:
    #     print('falsche auflösung')
    # warten()
    # mouse.click('left')
    # warten()

    # Haus 4 zeiehn klick
    if speicherZustand.read_resolution() == '1920x1080':  # fertig für jeden Hasus machen
        pyautogui.moveTo(945, 648, duration=0.5)
    elif speicherZustand.read_resolution() == '800x600':  # fertig
        pyautogui.moveTo(956, 582, duration=0.5)
    else:
        print('falsche auflösung')
    warten()
    mouse.click('left')
    warten()

    # Aus Weiter ziehen klikc
    hausauswahlweiter()

    # Überprüfung ob  Haus zu beazheln ist da ist
    hauserkennung()


global stop
stop = True


def start_event():
    global stop
    stop = False
    print("Start")
    log_to_file("AFK Bot Programm start mit X taste")


def stop_event():
    global stop
    stop = True
    print("Wird Pausiert")
    log_to_file("AFK Bot Programm stop mit e taste")


keyboard.add_hotkey('x', lambda: start_event())
# keyboard.add_hotkey('e', lambda: stop_event())


def istImZeitraum(start_time=(0, 0), end_time=(0, 0)):
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


def isspielwiklichaus():
    print("Spiel wurde gerade nicht mehr erkannt")
    log_to_file("Spiel wurde gerade nicht mehr erkannt")
    time.sleep(30)
    coord = []  
    if speicherZustand.read_resolution() == '1920x1080':
        coord = [1870, 50, 1880, 55]  # new
    elif speicherZustand.read_resolution() == '800x600':
        coord = [1334, 269, 1335, 270]  # new
    else:
        print('falsche auflösung')
    if isSpielAn(coord):
        warten()
        print("spiel wurde wieder erkannt")
        log_to_file("spiel wurde wieder erkannt")
        solangeSpielAktivIst()
    else:
        print("spiel wird beendet")
        log_to_file("spiel wird beendet")
        SpielBeenden()

# Abfrage ob Charakter gestorben ist 
def Gestorben():
    time.sleep(2)
    coord = []  
    if speicherZustand.read_resolution() == '1920x1080':
        coord = [948, 719, 949, 720]  #fertig
    elif speicherZustand.read_resolution() == '800x600':
        coord = [957, 477, 958, 478]  #fertig
    else:
        print('falsche auflösung')
    time.sleep(2)
    if Istgestorben(coord):
        print("spieler ist gestorben")
        log_to_file("spieler ist gestorben")
        time.sleep(300)
        SpielBeenden()
    else:
        print("spieler ist nicht gestorben")


counter = 0
def solangeSpielAktivIst():
    print_hour_and_minute()
    coord = []
    if speicherZustand.read_resolution() == '1920x1080':
        coord = [1870, 50, 1880, 55]  # new
    elif speicherZustand.read_resolution() == '800x600':
        coord = [1334, 269, 1335, 270]  # new
    else:
        print('falsche auflösung')
    while isSpielAn(coord):
        print_hour_and_minute()
        print("Spiel erkannt")
        time.sleep(3)
        global counter
        counter += 1
        print(counter)
        # Überpüfen ob Charakter Gestorben ist
        Gestorben()

        if counter % 50 == 0:
            print("Charakter wird bewegt!")
            log_to_file("Ist im Spiel")
            PressW()
            time.sleep(1)
            PressS()

            counter = 0

        #Server Neustart
        if istImZeitraum((4, 0), (4, 1)):
            log_to_file("4 Uhr Server Neustart")
            print_hour_and_minute()
            SpielBeenden()
            time.sleep(600)

        # # Tagesinvest
        if istImZeitraum((5, 1), (5, 3)) or istImZeitraum((5, 40), (5, 41)):
            log_to_file("05:01Uhr oder 05:40Uhr Invest und Fam")
            Tagesinvest()
            print_hour_and_minute()
            FamAufgabe4Stunden()
            print_hour_and_minute()
            time.sleep(120)
            escbisspielbeginn()

        if istImZeitraum((10, 26), (10, 27)) or istImZeitraum((12, 40), (12, 41)):
            Hausbezahlen()
            escbisspielbeginn()
            Unternehmenbezhalen()
            escbisspielbeginn()
            bunkerbezahlen()
            escbisspielbeginn()
            time.sleep(120)

        # 15 Uhr Relog
        # 20 Uhr Relog
        if istImZeitraum((15, 1), (15, 2)) or istImZeitraum((20, 1), (20, 2)):
            if speicherZustand.read_relogtime == 'JA':
                log_to_file("15:00Uhr oder 20:01Uhr Relog für Speicherpunkt")
                print("15:00Uhr oder 20:01Uhr Relog für Speicherpunkt")
                SpielBeenden()
                time.sleep(120)
            elif speicherZustand.read_relogtime == 'NEIN':
                time.sleep(120)
            else:
                print('falsche angabe')

        if istImZeitraum((17, 0), (17, 1)) or istImZeitraum((23, 0), (23, 1)):
            Tagesinvest()
            escbisspielbeginn()
            Loginbonus()
            escbisspielbeginn()
            time.sleep(120)

        if istImZeitraum((18, 15), (18, 16)):
            log_to_file("80 Std Abholen ")
            print("80 Std Abholen")
            Geld80std()
            escbisspielbeginn()
            time.sleep(120)

    else:
        isspielwiklichaus()


def escbisspielbeginn():
    for x in range(10):
        coord = []
        if speicherZustand.read_resolution() == '1920x1080':
            coord = [1870, 50, 1880, 55]  # new
        elif speicherZustand.read_resolution() == '800x600':
            coord = [1334, 269, 1335, 270]  # new
        else:
            print('falsche auflösung')

        if not isSpielAn(coord):
            log_to_file("ESC bis im spiel")
            print_hour_and_minute()
            print("ESC bis im zum AFK Botten")
            keyboard.press('esc')
            time.sleep(0.8)  
            keyboard.release('esc')
            warten()
        else:
            print_hour_and_minute()
            break


def IstServerFull():
    for v in range(15):
        coord = []
        if speicherZustand.read_resolution() == '1920x1080':
            coord = [1410, 600, 1416, 610]
        elif speicherZustand.read_resolution() == '800x600':
            coord = [1094, 561, 1095, 562]
        else:
            print('falsche auflösung')
        warten()
        if IsServerFull(coord):
            log_to_file("Server Full erneut login")
            print_hour_and_minute()
            print("Server ist überfüllt. Erneuter Login wird durchgeführt.")
            warten()
            LoginButton()
        else:
            print_hour_and_minute()
            break

        time.sleep(0.5)


def loginfertig():
    for y in range(400):
        print("Warte auf login screen")
        print_hour_and_minute()
        coord = []
        if speicherZustand.read_resolution() == '1920x1080':
            coord = [1410, 600, 1416, 610]
        elif speicherZustand.read_resolution() == '800x600':
            coord = [1094, 561, 1095, 562]
        else:
            print('falsche auflösung')

        if ispasswordabfrage(coord):
            print("Password eingabe erkannt")
            print_hour_and_minute()
            warten()
            password()
            IstServerFull()
            warten()
            Charakterauswahl()
            warten()
            SpawnPunkt()
            # warten()
            # escbis20sdtSlider()
            # warten()
            # GrandCoinSlider20hours()
            warten()
            escbisspielbeginn()
            warten()
            break
        time.sleep(1)


if __name__ == "__main__":
    speicherZustand = prepare()
    if speicherZustand.read_autostart() == "JA":
        stop = False
    while True:
        # warten bis eingabe dann start
        print("Zum Starten X drücken")
        while stop == True:
            time.sleep(1)
            # print("warten")

        while stop == False:
            solangeSpielAktivIst()
            warten()
            SpielBeenden()
            warten()
            startding()
            warten()
            RageMPconnenct()
            time.sleep(40)
            print("Fertig mit warten, login wird abgefragt.")
            loginfertig()
            warten()
