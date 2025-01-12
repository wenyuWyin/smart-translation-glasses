"""
Interface for Image Segmentation Handlers in the Image Segmentation Module.
"""

from abc import ABC, abstractmethod
from typing import Dict
import cv2


class IImageSegmentationHandler(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def imageSegmentation(self, image: cv2.Mat) -> Dict[tuple, cv2.Mat]:
        """
        Retrieves the result of the image segmentation.

        :return: The image segmentation as a string
        """
        pass

    @abstractmethod
    def statusCheck(self) -> bool:
        """
        Checks if the image segmentation is complete.

        :return: True if the image segmentation is complete, otherwise False
        """
        pass

    @abstractmethod
    def getResult(self) -> str:
        """
        Retrieves the result of the image segmentation.

        :return: The segmentation result as a list of cv2 images
        """
        pass

    @abstractmethod
    def getID(self) -> int:
        """
        Retrieves the unique identifier for this handler.

        :return: The handler ID
        """
        pass
