import time

import cv2 as cv
import numpy as np
from PIL import ImageGrab
from ultralytics import YOLO


class VisualInput(object):
    def __init__(self):
        self.videostream = None  # "./assets/fischen_short.mp4"
        self.screen_area = None  # [0,200,1700,1500]

    def useVideo(self, input_source):
        videostream = cv.VideoCapture(input_source)
        if not videostream.isOpened():
            print("missing video input")
            exit(1)
        self.videostream = videostream

    def useScreenshot(self, screen_area):
        self.screen_area = screen_area

    def next(self):
        if self.videostream:
            ret, frame = self.videostream.read()
            if not ret:
                print("Non frame detected. End of stream")
                return
            # https://stackoverflow.com/a/39744436
            lab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
            clahe = cv.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            enhanced_img = cv.cvtColor(lab, cv.COLOR_LAB2BGR)
            return enhanced_img
        elif self.screen_area:
            screenshot = ImageGrab.grab(
                bbox=self.screen_area,
                include_layered_windows=True,
                all_screens=True)
            screen_array = np.asarray(screenshot.convert(mode="RGB"))
            return screen_array
        else:
            return


class FishSymbol(object):
    def __init__(self, posX=0, posY=0, threshold=7) -> None:
        self.x = int(posX)
        self.y = int(posY)
        self.left = False
        self.right = False
        self.threshold = threshold

    def _changeDir(self, newPos):
        dist = self.x - newPos
        if (abs(dist) < self.threshold):
            return False
        if (dist > 0):
            self.left = True
            self.right = False
        else:
            self.left = False
            self.right = True
        return True

    def newPos(self, posX, posY):
        if self._changeDir(int(posX)):
            self.x = int(posX)
            self.y = int(posY)
        return self

    def detected(self) -> bool:
        return self.x > 0 and self.y > 0

    def isLeft(self) -> bool:
        return self.left

    def isRight(self) -> bool:
        return self.right

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class FishSymbolDetection(object):

    def __init__(self, model_path: str = "./assets/model.pt", showOutput: bool = True, custom_fish_symbol: FishSymbol = None):
        self.model = YOLO(model_path)
        self.model.info(verbose=False)
        self.model.overrides["verbose"] = False
        self.showOutput = showOutput
        self.origin_source_input = VisualInput()
        if custom_fish_symbol:
            self.fishsymbol = custom_fish_symbol
        else:
            self.fishsymbol = FishSymbol()

    def _predict_fish(self, source_input: any) -> None:
        results = self.model.predict(
            source=source_input,
            device=0,
            # show=True,
            conf=0.2,
            iou=0.3,
            max_det=1,
            classes=1)
        detected_fishes = [
            result.to("cpu").numpy().boxes for result in results]
        # print(detected_fishes[0])
        if len(detected_fishes[0]) > 0:
            # print("has detected")
            detected_fishes = [each.xywh[0, :2] for each in detected_fishes]
            detected_fish = detected_fishes[0]
            self.fishsymbol.newPos(
                detected_fish[0],
                detected_fish[1]
            )
        else:
            self.fishsymbol.newPos(0, 0)

    def _nextFrame(self):
        next_frame = self.origin_source_input.next()
        # h, w = next_frame .shape[:2]
        # next_frame = cv.resize(next_frame, (w//1, h//1))
        return next_frame
        # return cv.cvtColor(next_frame, cv.COLOR_RGB2BGR)

    def _drawDetected(self, frame):
        x = max(self.fishsymbol.getX()-12, 0)
        y = max(self.fishsymbol.getY()-12, 0)
        return cv.rectangle(
            frame,
            (x, y),
            (x + 25, y + 25),
            (0, 255,   0),
            4)

    def useVideoInput(self, input_source="./assets/fischen_short.mp4"):
        self.origin_source_input.useVideo(input_source)

    def useScreenshotInput(self, screen_area=[100, 500, 2200, 1900]):
        self.origin_source_input.useScreenshot(screen_area)

    def changeShowResult(self, activate=True):
        if activate:
            if self.showOutput:
                self.stop()
            self.showOutput = False

    def start(self, custom_fish_symbol: FishSymbol = None):
        if not self.origin_source_input.videostream:
            self.useScreenshotInput()
        if custom_fish_symbol:
            self.fishsymbol = custom_fish_symbol
        else:
            self.fishsymbol = FishSymbol()

    def detectFish(self) -> FishSymbol:
        frame = self._nextFrame()
        self._predict_fish(frame)
        if self.fishsymbol.detected():
            if self.showOutput:
                frame = self._drawDetected(frame)
        if self.showOutput:
            h, w = frame.shape[:2]
            frame = cv.resize(frame, (w//2, h//2))
            cv.imshow('fish detection result', frame)
        key_input = cv.waitKey(50) & 0xff
        if key_input == 27:
            self.stop()
        return self.fishsymbol

    def stop(self):
        cv.destroyAllWindows()

# results = model.track(
#     source="./assets/fischen_short.mp4",
#     show=True,
#     stream=True,
#     conf=0.4, iou=0.5, max_det=1, vid_stride=True, classes=1)
