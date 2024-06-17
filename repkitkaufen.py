import time

import keyboard
import mouse

global stop
stop = True
counterLoop = 0


def warten():
    time.sleep(wartezeit)


def tankeöffnen():
    warten()
    keyboard.press('e')
    warten()
    keyboard.release('e')


def repkitkaufen():
    for i in range(int(choice_repkit)):
        tankeöffnen()
        warten()
        mouse.move(1016, 602, absolute=True)
        warten()
        counterLoop = 0
        while counterLoop < 10:
            mouse.click('left')
            if stop == True:
                break
            time.sleep(0.53)
            counterLoop += 1
        print("10 stück wurden gekauft")
        warten()
        kaufbestätigen()


def kanisterkaufen():
    tankeöffnen()
    warten()
    for i in range(int(choice_kanister)):
        mouse.move(1016, 725, absolute=True)
        print("klick")
        mouse.click('left')
        if stop == True:
            break
        time.sleep(0.53)
    print(f"{choice_kanister} stück Kanister wurden gekauft")
    warten()
    kaufbestätigen()


def kaufbestätigen():
    mouse.move(1270, 450, absolute=True)
    warten()
    mouse.click('left')
    warten()


def inventar():
    print("inv")
    warten()
    keyboard.press('tab')
    warten()
    keyboard.release('tab')
    warten()
    # inventar 1 slot
    mouse.move(326, 250, absolute=True)
    warten()
    mouse.press('left')
    warten()
    # auto 1 slot
    mouse.move(1039, 430, absolute=1)
    warten()
    mouse.release('left')
    warten()
    keyboard.press('esc')
    warten()
    keyboard.release('esc')


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

print("")
selection = input("Kanister (1) oder Repkit (2):")
print("")

print("---------------------")
print("Empfohlen von 0.30 bis 99 sekunden")
wartezeit = float(
    input("Gib die Wartezeit zwischen den Eingaben in Sekunden ein: "))

print("---------------------")

IS_REPKIT = False

if (len(selection) > 0) and (str(selection).lower() == '1'):
    IS_REPKIT = True
    # print("---------------------")
    # print("Kanister Aktiviert")
    # print("---------------------")


else:
    IS_REPKIT = False
    # print("---------------------")
    # print("Repkit Aktiviert")
    # print("---------------------")


if IS_REPKIT == False:
    print("------------Repkits Ausgewählt------------")
    print(' 1 ausführung = 10 repkits:')
    print(' wähle zwischen 1 - 99 durchgänge ')
    print(" 1st Slot Inventar und Auto")
    print("")
    choice_repkit = input("Deine Auswahl: ")
    print("---------------------")
else:
    print("------------Kanister Ausgewählt------------")
    print(' wie viele Kanister willst du in einem Durchgang kaufen:')
    print(' wähle zwischen 1 - 99 ')
    print(" 1st Slot Inventar und Auto")
    print("")
    choice_kanister = input("Deine Auswahl: ")
    print("---------------------")

while True:

    # warten bis eingabe dann start
    print("Zum Starten x drücken dund e zum Pausieren")
    while stop == True:
        time.sleep(2)

    while stop == False:
        warten()
        if stop == True:
            break

        if IS_REPKIT == False:
            print("Repkits")
            repkitkaufen()
            warten()
            inventar()
        else:
            print("Kanister")
            kanisterkaufen()
            warten()
            inventar()
        if stop == True:
            break
