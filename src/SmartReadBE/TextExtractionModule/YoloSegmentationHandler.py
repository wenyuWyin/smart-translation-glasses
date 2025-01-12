"""
Image segmentation using YOLO-based models
"""

import random
from typing import Dict
import cv2
from ultralytics import YOLO
from IImageSegmentationHandler import IImageSegmentationHandler

MODEL_PATH = "capstone_yolov8_trained.pt"


class YoloSegmentationHandler(IImageSegmentationHandler):
    def __init__(self):
        self.model = YOLO(MODEL_PATH)

        self.handlerID = f"YS{random.randint(100, 999)}"
        self.segmentationStatus = False
        self.result = ""

    def imageSegmentation(self, image: cv2.Mat) -> Dict[tuple, cv2.Mat]:
        try:
            # Segment the image into sub-images
            results = self.model(image)
            result = results[0]

            self.result = {}
            # Get the bounding box of each image
            for _, box in enumerate(result.boxes.xyxy):
                x1, y1, x2, y2 = map(int, box)
                sub_image = image[y1:y2, x1:x2]
                self.result[(x1, x2, y1, y2)] = sub_image

            self.segmentationStatus = True
        except Exception:
            self.result = []
            self.segmentationStatus = False

        return self.result

    def statusCheck(self) -> bool:
        # Checks if the image segmentation process is complete.
        return self.segmentationStatus

    def getResult(self) -> str:
        # Retrieves the image segmentation result.
        return self.result

    def getID(self) -> int:
        # Retrieves unique identifier for this handler
        return self.handlerID
