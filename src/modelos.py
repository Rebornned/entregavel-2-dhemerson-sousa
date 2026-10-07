import sys
import cv2 as cv

COLOR = {0: (0,255,0), 1: (255,0,0)}

class Deteccao():
    # region ########## Attributes ####################
    # ************************************************
    class_id: int
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    # endregion --------------------------------------

    # region ########## Builders #####################
    # ************************************************
    def __init__(self, class_id: int, x_min: int, y_min: int, x_max: int, y_max: int):
        self.class_id = class_id
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
    # endregion --------------------------------------

    # region ########## Methods ######################
    # ************************************************
    def draw(self, img):
        color = COLOR[self.class_id]
        cv.rectangle(img, (self.x_min, self.y_min), (self.x_max, self.y_max), color, 2)

    def toString(self):
        print(f"class_id: {self.class_id} | x min/max: {self.x_min}/{self.x_max} | y min/max: {self.y_min}/{self.y_max}")
    # endregion --------------------------------------

class ImagemAnotada():
    # region ########## Attributes ####################
     # ************************************************
    img_path: str
    detection_list: list
     # endregion --------------------------------------

    # region ########## Builders #####################
    def __init__(self, img_path):
        self.detection_list: list[Deteccao] = []
        self.img_path = img_path

    # endregion --------------------------------------

    # region ########## Methods ######################
    # ************************************************
    def addDetection(self, detection: Deteccao):
        if(detection is None):
            print("ERROR: attempted to add a null detection to an annotated image.")
            sys.exit(-1);

        self.detection_list.append(detection)
        return True

    def imageProcessing(self, original_img):
        copy = original_img.copy()
        for detection in self.detection_list:
            detection.draw(copy)

        return copy

    def toString(self):
        print(f"Image Path: {self.img_path}")
        for detection in self.detection_list:
            detection.toString()
    # endregion --------------------------------------
