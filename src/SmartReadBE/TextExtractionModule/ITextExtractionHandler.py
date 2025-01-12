"""
Interface for Text Extraction Handlers in the Text Extraction Module.
"""

from abc import ABC, abstractmethod
import cv2


class ITextExtractionHandler(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def extractText(self, image: cv2.Mat, language: str) -> str:
        """
        Checks if the text extraction is complete.

        :return: True if the text extraction is complete, otherwise False
        """
        pass

    @abstractmethod
    def statusCheck(self) -> bool:
        """
        Checks if the text extraction is complete.

        :return: True if the text extraction is complete, otherwise False
        """
        pass

    @abstractmethod
    def getResult(self) -> str:
        """
        Retrieves the result of the text extraction.

        :return: The extraction result as a dictionary
        """
        pass

    @abstractmethod
    def getID(self) -> int:
        """
        Retrieves the unique identifier for this handler.

        :return: The handler ID
        """
        pass
