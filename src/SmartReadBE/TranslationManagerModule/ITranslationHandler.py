"""
Interface for Translation Handlers in the TranslationManagerModule.
"""
from abc import ABC, abstractmethod

class ITranslationHandler(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def translate(self, inputTxt: str, targetLanguage: str, sourceLanguage: str = None) -> str:
        """
        Performs the translation.

        :param targetLanguage: The target language code (e.g., 'fr', 'es')
        :return: The translated text as a string
        """
        pass

    @abstractmethod
    def statusCheck(self) -> bool:
        """
        Checks if the translation is complete.

        :return: True if the translation is complete, otherwise False
        """
        pass

    @abstractmethod
    def getResult(self) -> str:
        """
        Retrieves the result of the translation.

        :return: The translated text as a string
        """
        pass

    @abstractmethod
    def getID(self) -> int:
        """
        Retrieves the unique identifier for this handler.

        :return: The handler ID
        """
        pass
