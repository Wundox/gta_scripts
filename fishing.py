import time

import cv2 as cv
import numpy as np
from PIL import ImageGrab
from ultralytics import YOLO


class VisualInput(object):
    def __init__(self, video_input=None, screenshot_input=None):
        self.videostream = None  # "./assets/fischen_short.mp4"
        self.screen_area = None  # [0,200,1700,1500]
        self.current_image = None
        if video_input:
            self.set_video(video_input)
        if screenshot_input:
            self.set_screenshot(screenshot_input)

    def set_video(self, input_source: number | str):
        videostream = cv.VideoCapture(input_source)
        if not videostream.isOpened():
            print("missing video input")
            exit(1)
        self.videostream = videostream

    def set_screenshot(self, screen_area: [number]):
        self.screen_area = screen_area

    def next(self):
        if self.videostream:
            ret, frame = self.videostream.read()
            if not ret:
                Exception("Non frame detected. End of stream")
            # https://stackoverflow.com/a/39744436
            lab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
            clahe = cv.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            enhanced_img = cv.cvtColor(lab, cv.COLOR_LAB2BGR)
            self.current_image = enhanced_img
        elif self.screen_area:
            screenshot = ImageGrab.grab(
                bbox=self.screen_area,
                include_layered_windows=True,
                all_screens=True)
            self.current_image = np.asarray(screenshot.convert(mode="RGB"))
        else:
            Exception("None source input was set")
        return self.current_image

    def has_current(self) -> bool:
        return (self.current_image is not None)

    def current(self):
        if self.has_current():
            return self.current_image
        else:
            return None


class FishSymbol(object):
    def __init__(self, x=0, y=0, threshold=7) -> None:
        self.x = int(x)
        self.y = int(y)
        self.left = False
        self.right = False
        self.threshold = threshold

    def _change_dir(self, new_x_pos: number):
        dist = self.x - new_x_pos
        if (abs(dist) < self.threshold):
            return False
        if (dist > 0):
            self.left = True
            self.right = False
        else:
            self.left = False
            self.right = True
        return True

    def new_x_pos(self, posX, posY):
        if self._change_dir(int(posX)):
            self.x = int(posX)
            self.y = int(posY)
        return self

    def detected(self) -> bool:
        return self.x > 0 and self.y > 0

    def is_left(self) -> bool:
        return self.left

    def is_right(self) -> bool:
        return self.right

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class FishSymbolDetection(object):

    def __init__(self,
                 model_path: str = "./assets/model.pt",
                 show_result: bool = True,
                 custom_fish_symbol: FishSymbol = FishSymbol(),
                 pulling_bar_position: [number] = [1867, 1000, 1890, 1010]):
        self.model = YOLO(model_path)
        self.model.info(verbose=False)
        self.model.overrides["verbose"] = False
        self.show_result = show_result
        self.origin_source_input = VisualInput()
        self.fishsymbol = custom_fish_symbol
        self.pulling_bar_position = pulling_bar_position

    def _predict_fish(self, source_input: any) -> None:
        results = self.model.predict(
            # source='0',
            source=source_input,
            device=0,
            # show=True,
            conf=0.2,
            # iou=0.5,
            # max_det=1,
            # classes=0
        )
        detected_fishes = [
            result.to("cpu").numpy().boxes for result in results]
        # for result in results:
        #     print(result.to("cpu").names)
        # print(detected_fishes[0])
        if len(detected_fishes[0]) > 0:
            # print("has detected")
            detected_fishes = [each.xywh[0, :2] for each in detected_fishes]
            detected_fish = detected_fishes[0]
            self.fishsymbol.new_x_pos(
                detected_fish[0],
                detected_fish[1]
            )
        else:
            self.fishsymbol.new_x_pos(0, 0)

    def _next_frame(self):
        next_frame = self.origin_source_input.next()
        # h, w = next_frame .shape[:2]
        # next_frame = cv.resize(next_frame, (w//1, h//1))
        return next_frame
        # return cv.cvtColor(next_frame, cv.COLOR_RGB2BGR)

    def _draw_detected(self, frame):
        x = max(self.fishsymbol.get_x()-25, 0)
        y = max(self.fishsymbol.get_y()-25, 0)
        return cv.rectangle(
            frame,
            (x, y),
            (x + 50, y + 50),
            (0, 255,   0),
            4)

    def _crop_plane(self):
        frame = self._next_frame()
        array_image = np.array(frame)

        x_start, y_start, x_stop, y_stop = self.pulling_bar_position

        crop_box = array_image[x_start:x_stop, y_start:y_stop]

        print(str(crop_box))
        xlen = len(crop_box)
        ylen = len(crop_box[0])

        print("x:" + str(xlen) + " y:" + str(ylen))
        midX = xlen // 2
        midY = ylen // 2

        print("mitte: x:" + str(midX) + " y:" + str(midY))

        r, g, b = crop_box[midX, midY]
        return [r, g, b]

    def use_video_input(self, input_source="./assets/fischen_short.mp4"):
        self.origin_source_input.set_video(input_source)

    def use_screenshot_input(self, screen_area=[100, 500, 2200, 1900]):
        self.origin_source_input.set_screenshot(screen_area)

    def show_result(self, activate=True):
        if activate:
            if self.show_result:
                self.stop()
            self.show_result = False

    def start(self, custom_fish_symbol: FishSymbol = None):
        if not self.origin_source_input.videostream:
            self.use_screenshot_input()
        if custom_fish_symbol:
            self.fishsymbol = custom_fish_symbol
        else:
            self.fishsymbol = FishSymbol()

    def detect(self) -> FishSymbol:
        frame = self._next_frame()
        self._predict_fish(frame)
        if self.fishsymbol.detected():
            if self.show_result:
                frame = self._draw_detected(frame)
        if self.show_result:
            h, w = frame.shape[:2]
            frame = cv.resize(frame, (w//2, h//2))
            cv.imshow('fish detection result', frame)
        key_input = cv.waitKey(50) & 0xff
        if key_input == 27:
            self.stop()
        return self.fishsymbol

    def hasPullingBar(self) -> bool:
        return [27, 97, 143] == self._crop_plane()

    def finishedPullingBar() -> bool:
        return [79, 184, 255] == self._crop_plane()

    def stop(self):
        cv.destroyAllWindows()

        # results = model.track(
        #     source="./assets/fischen_short.mp4",
        #     show=True,
        #     stream=True,
        #     conf=0.4, iou=0.5, max_det=1, vid_stride=True, classes=1)
