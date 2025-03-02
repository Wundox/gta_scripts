import time

import keyboard
import mouse

global stop
stop = True


def mouseLeftclick():
    mouse.click('left')


def wait():
    time.sleep(wartezeit)


def inventar():
    keyboard.press_and_release('tab')


def esc():
    keyboard.press_and_release('esc')


def panelkaufen():
    mouse.move(792, 450, absolute=True)
    wait()
    mouseLeftclick()
    wait()
    mouse.move(967, 550, absolute=True)
    wait()
    mouseLeftclick()
    wait()
    keyboard.write('33')
    wait()
    mouse.move(1044, 639, absolute=True)
    time.sleep(1)
    mouseLeftclick()
    wait()
    mouseLeftclick()
    mouseLeftclick()
    wait()
    mouseLeftclick()
    mouseLeftclick()
    mouseLeftclick()


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

wartezeit = float(
    input("Gib die Wartezeit zwischen den Eingaben in Sekunden ein: "))

while True:

    # warten bis eingabe dann start
    print("Zum Starten x drücken dund e zum Pausieren")
    while stop == True:
        time.sleep(2)

    while stop == False:
        keyboard.press_and_release('e')
        # produkte kaufen drücken
        wait()
        mouse.move(1230, 878, absolute=True)
        wait()
        mouseLeftclick()
        if stop == True:
            break
        # scrollen
        wait()
        mouse.move(1632, 613, absolute=True)
        wait()
        mouseLeftclick()
        if stop == True:
            break
        # auf panel drücken
        wait()
        panelkaufen()
        wait()
        esc()
        wait()
        if stop == True:
            break
        inventar()
        wait()
        esc()
        wait()
        inventar()
        if stop == True:
            break
        # auf slot 1 ziehen
        wait()
        mouse.move(328, 247, absolute=True)
        wait()
        mouse.press('left')
        wait()
        if stop == True:
            break
        mouse.move(1037, 430, absolute=5)
        wait()
        mouse.release('left')
        wait()
        esc()
        if stop == True:
            break
