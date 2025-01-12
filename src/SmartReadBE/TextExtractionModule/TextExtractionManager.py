"""
TextExtractionManager manages handler instances that perform OCR and image segmentation
"""

import importlib
from typing import Dict
import cv2


class TextExtractionManager:
    AVAILABLE_OCR_HANDLERS = ["PaddleOCRHandler"]
    AVAILABLE_SEGMENTATION_HANDLERS = ["YoloSegmentationHandler"]

    def __init__(self):
        # Initializes the TranslationManager
        self.extractors = dict()
        self.segmentors = dict()

    def initialize(self) -> bool:
        try:
            for ocr_class_name in self.AVAILABLE_OCR_HANDLERS:
                # Dynamically import the class from the current folder
                module = importlib.import_module(ocr_class_name)

                # Get the class from the module
                ocr_class = getattr(module, ocr_class_name)

                if ocr_class is None:
                    print(f"Error: Class {ocr_class_name} not found.")
                    return False

                # Create two instances of the class
                for _ in range(2):
                    instance = ocr_class()  # Create an instance of the class
                    self.extractors[instance.getID()] = (
                        instance  # Store the instance in the dictionary
                    )

            for segmentor_class_name in self.AVAILABLE_SEGMENTATION_HANDLERS:
                # Dynamically import the class from the current folder
                module = importlib.import_module(segmentor_class_name)

                # Get the class from the module
                segmentor_class = getattr(module, segmentor_class_name)

                if segmentor_class is None:
                    print(f"Error: Class {segmentor_class_name} not found.")
                    return False

                # Create two instances of the class
                for _ in range(2):
                    instance = segmentor_class()  # Create an instance of the class
                    self.segmentors[instance.getID()] = (
                        instance  # Store the instance in the dictionary
                    )

            return True  # Initialization successful
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False

    def extract(self, handlerID: str, image: cv2.Mat, language: str) -> str:
        # Performs text extraction using the assigned ExtractionHandler instance

        try:
            # Perform text extraction
            extraction_result = self.extractors.get(handlerID).extractText(
                image, language
            )

            # Check text extraction status
            if self.extractors.get(handlerID).statusCheck():
                return extraction_result
            else:
                return None
        except Exception as e:
            print(f"Text extraction error: {e}")
            return None

    def segmentation(self, handlerID: str, image: cv2.Mat) -> Dict[tuple, cv2.Mat]:
        # Performs image segmentation using the assigned ImageSegmentationHandler instance
        try:
            # Perform image segmentation
            segmentation_result = self.segmentors.get(handlerID).imageSegmentation(
                image
            )

            # Check image segmentation status
            if self.segmentors.get(handlerID).statusCheck():
                return segmentation_result
            else:
                return None
        except Exception as e:
            print(f"Image segmentation error: {e}")
            return None
