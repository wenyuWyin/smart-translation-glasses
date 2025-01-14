"""
Image segmentation using YOLO-based models
"""

import random
import os
from typing import Dict
import cv2
import numpy as np
from ultralytics import YOLO
from .IImageSegmentationHandler import IImageSegmentationHandler

# Get the current folder's absolute path
current_folder = os.path.dirname(os.path.abspath(__file__))

# Append the model file name to the current folder's path
MODEL_PATH = os.path.join(current_folder, "capstone_yolov8_trained.pt")


class YoloSegmentationHandler(IImageSegmentationHandler):
    def __init__(self):
        self.model = YOLO(MODEL_PATH, verbose=True)
        self.handlerID = f"YS{random.randint(100, 999)}"
        self.segmentationStatus = False
        self.result = ""

        # Warm-up model during initialization to allocate resource to YOLO models in advance
        dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)
        self.model(dummy_image)

    def imageSegmentation(self, image: cv2.Mat) -> Dict[tuple, cv2.Mat]:
        try:
            print("Image segmentation started")
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
        except Exception as e:
            print(f"Image segmentation failed with {e}")
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
