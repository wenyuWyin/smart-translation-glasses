"""
OCR using PaddleOCR models
"""

import random
import cv2
import os
from paddleocr import PaddleOCR
from .ITextExtractionHandler import ITextExtractionHandler


# Get the current folder's absolute path
current_folder = os.path.dirname(os.path.abspath(__file__))

# Append the model file name to the current folder's path
MODEL_PATH = os.path.join(current_folder, "capstone_yolov8_trained.pt")


class PaddleOCRHandler(ITextExtractionHandler):
    def __init__(self):
        # Define all models for different languages
        self.ocr_en = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
        self.ocr_fr = PaddleOCR(use_angle_cls=True, lang="fr", show_log=False)
        self.ocr_ch = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
        self.ocr_ja = PaddleOCR(use_angle_cls=True, lang="japan", show_log=False)
        self.ocr_it = PaddleOCR(use_angle_cls=True, lang="it", show_log=False)

        self.handlerID = f"PO{random.randint(100, 999)}"
        self.extractionStatus = False
        self.result = ""

    def extractText(self, image: cv2.Mat, language: str) -> str:
        try:
            # Apply different models based on the input language
            if language == "Chinese":
                result = self.ocr_ch.ocr(image, cls=True)
            elif language == "English":
                result = self.ocr_en.ocr(image, cls=True)
            elif language == "French":
                result = self.ocr_fr.ocr(image, cls=True)
            elif language == "Japanese":
                result = self.ocr_eja.ocr(image, cls=True)
            elif language == "Italian":
                result = self.ocr_it.ocr(image, cls=True)
            else:
                result = self.ocr_en.ocr(image, cls=True)

            result = result[0]
            texts = [line[1][0] for line in result]

            self.result = " ".join(texts)
            self.extractionStatus = True
        except Exception:
            self.result = None
            self.extractionStatus = False

        return self.result

    def statusCheck(self) -> bool:
        # Checks if the text extraction process is complete.
        return self.extractionStatus

    def getResult(self) -> str:
        # Retrieves the text extraction result.
        return self.result

    def getID(self) -> int:
        # Retrieves unique identifier for this handler
        return self.handlerID
