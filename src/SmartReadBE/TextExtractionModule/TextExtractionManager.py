"""
TextExtractionManager manages handler instances that perform OCR and image segmentation
"""

import importlib
from typing import Dict
import cv2


class TextExtractionManager:
    AVAILABLE_OCR_HANDLERS = ["TextExtractionModule.PaddleOCRHandler"]
    AVAILABLE_SEGMENTATION_HANDLERS = ["TextExtractionModule.YoloSegmentationHandler"]

    def __init__(self):
        # Initializes the TranslationManager
        self.extractors = dict()
        self.avail_extractors = []
        self.segmentors = dict()
        self.avail_segmentors = []

    def initialize(self) -> bool:
        try:
            # Need to initialize YOLO models before PaddleOCR models to avoid compatibility issue
            for segmentor_class_name in self.AVAILABLE_SEGMENTATION_HANDLERS:
                # Dynamically import the class from the current folder
                class_name = segmentor_class_name.rsplit(".", 1)[1]
                module = importlib.import_module(segmentor_class_name)

                # Get the class from the module
                segmentor_class = getattr(module, class_name)

                if segmentor_class is None:
                    print(f"Error: Class {class_name} not found.")
                    return False

                # Create two instances of the class
                for _ in range(2):
                    instance = segmentor_class()  # Create an instance of the class
                    self.segmentors[instance.getID()] = (
                        instance  # Store the instance in the dictionary
                    )
                    self.avail_segmentors.append(instance.getID())

            for ocr_class_name in self.AVAILABLE_OCR_HANDLERS:
                # Dynamically import the class from the current folder
                class_name = ocr_class_name.rsplit(".", 1)[1]
                module = importlib.import_module(ocr_class_name)

                # Get the class from the module
                ocr_class = getattr(module, class_name)

                if ocr_class is None:
                    print(f"Error: Class {class_name} not found.")
                    return False

                # Create two instances of the class
                for _ in range(2):
                    instance = ocr_class()  # Create an instance of the class
                    self.extractors[instance.getID()] = (
                        instance  # Store the instance in the dictionary
                    )
                    self.avail_extractors.append(instance.getID())

            return True  # Initialization successful
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False

    def extract(self, image: cv2.Mat, language: str) -> str:
        # Performs text extraction using the assigned ExtractionHandler instance
        try:
            handlerID = self.avail_extractors.pop()
            if not handlerID:
                raise Exception("No available handler for text extraction.")

            handler = self.extractors.get(handlerID)
            # Perform text extraction
            extraction_result = handler.extractText(image, language)

            self.avail_extractors.append(handlerID)

            # Check text extraction status
            if handler.statusCheck():
                return extraction_result
            else:
                return None
        except Exception as e:
            print(f"Text extraction error: {e}")
            return None

    def segmentation(self, image: cv2.Mat) -> Dict[tuple, cv2.Mat]:
        # Performs image segmentation using the assigned ImageSegmentationHandler instance
        try:
            handlerID = self.avail_segmentors.pop()
            if not handlerID:
                raise Exception("No available handler for segmentation.")

            handler = self.segmentors.get(handlerID)
            # Perform image segmentation
            segmentation_result = handler.imageSegmentation(image)

            self.avail_segmentors.append(handlerID)
            # Check image segmentation status
            if handler.statusCheck():
                return segmentation_result
            else:
                return None
        except Exception as e:
            print(f"Image segmentation error: {e}")
            return None
