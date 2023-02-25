import time

import keyboard

from fishing import FishSymbolDetection

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


keyboard.add_hotkey('x', lambda: start_event())
keyboard.add_hotkey('p', lambda: stop_event())

fishDetection = FishSymbolDetection(
    model_path=".\\assets\\model.pt", showOutput=True)
# fishDetection = FishSymbolDetection(model_path="assets\model.pt")
# fishDetection.useScreenshotInput([0, 20, 650, 700])
fishDetection.useVideoInput(".\\assets\\fischen_short.mp4")
while True:
    # warten bis eingabe dann start
    print("Zum Starten x drücken d und p zum Pausieren")
    while stop == True:
        time.sleep(2)

    fishDetection.start()
    while stop == False:
        fishsymbol = fishDetection.detectFish()
        if fishsymbol.detected():
            if fishsymbol.isLeft():
                # print("fish directed to left")
                print("A wird gehalten")
                keyboard.release('a')
                keyboard.press('d')
            if fishsymbol.isRight():
                # print("fish directed to right")
                print("D wird gehalten")
                keyboard.release('d')
                keyboard.press('a')
        else:
            print("Taste wird losgelassen")
            keyboard.release('a')
            keyboard.release('d')
        print("Warte bis nächste runde")
        time.sleep(0.2)
    print("Taste wird losgelassen")
    keyboard.release('a')
    keyboard.release('d')
    print("Fischerkennung beendet")
    fishDetection.stop()
