"""
OCR using PaddleOCR models
"""

import random
import cv2
from paddleocr import PaddleOCR
from ITextExtractionHandler import ITextExtractionHandler


class PaddleOCRHandler(ITextExtractionHandler):
    def __init__(self):
        self.ocr_en = PaddleOCR(use_angle_cls=True, lang="en")
        self.ocr_fr = PaddleOCR(use_angle_cls=True, lang="fr")
        self.ocr_ch = PaddleOCR(use_angle_cls=True, lang="ch")
        self.ocr_ja = PaddleOCR(use_angle_cls=True, lang="japan")
        self.ocr_it = PaddleOCR(use_angle_cls=True, lang="it")

        self.handlerID = f"PO{random.randint(100, 999)}"
        self.extractionStatus = False
        self.result = ""

    # def extractAllText(self, image: cv2.Mat, language: str) -> str:

    def extractText(self, image: cv2.Mat, language: str) -> str:
        try:
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
