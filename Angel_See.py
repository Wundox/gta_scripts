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
    model_path=".\\assets\\model2.pt",
    show_result=False,
    pulling_bar_position=[1867, 1000, 1890, 1010]
)
# model_path=".\\model.pt", show_result=False)
# fishDetection = FishSymbolDetection(model_path="assets\model.pt")xp
# fishDetection.use_screenshot_input([0, 20, 650, 700])
# fishDetection.use_video_input(".\\assets\\fischen_dark.mp4")
fishDetection.use_video_input(0)
while True:
    # warten bis eingabe dann start
    print("Zum Starten x drücken p zum Pausieren")
    while stop == True:
        time.sleep(2)

    if stop == False:
        print("Angel wird ausgeworfen")
        start = None
        now = None
        keyboard.press_and_release('e')
        fishDetection.start()

    while stop == False:
        fishsymbol = fishDetection.detect()
        if fishsymbol.detected():
            # Tire out the fish on the hook
            start = time.time()
            if fishsymbol.is_left():
                print("D wird gehalten")
                keyboard.press('d')
                keyboard.release('a')
            if fishsymbol.is_right():
                print("A wird gehalten")
                keyboard.press('a')
                keyboard.release('d')
        elif fishDetection.hasPullingBar():
            print("Fisch einziehen")
            keyboard.release('a')
            keyboard.release('d')
            mouse.press('left')
        elif fishDetection.finishedPullingBar():
            print("Fisch einziehen beenden")
            time.sleep(0.5)
            mouse.release('left')
            time.sleep(0.5)
            print("Fisch eingezogen")
            break
        else:
            if start and (time.time() - start) > 5:
                print("Zeit überschritten")
                break
        print("Warte auf nächstes Bild")
        time.sleep(1)
    fishDetection.stop()
    print("Alle Tasten werden losgelassen")
    keyboard.release('a')
    keyboard.release('d')
    mouse.release('left')
