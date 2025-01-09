"""
Translation by Google Cloud Translate API
"""

from google.cloud import translate_v2 as translate
from ITranslationHandler import ITranslationHandler
import random
import os

class GoogleTranslator(ITranslationHandler):
    def __init__(self):
        # Load API key
        # To be modified   
        # Create a Translate client with the API key
        self.client = translate.Client()
        self.handlerID = f"TG{random.randint(100, 999)}"
        self.transStatus = False
        self.result = ""

    def translate(self, inputTxt: str, targetLanguage: str, sourceLanguage: str = None) -> str:
        # Translates the input text into the target language.
        try:
            if sourceLanguage:
                # Translation with specified source language
                response = self.client.translate(inputTxt, target_language=targetLanguage, source_language=sourceLanguage)
            else:
                # Translation with auto-detected source language
                response = self.client.translate(inputTxt, target_language=targetLanguage)

            self.result = response["translatedText"]
            self.transStatus = True

        except Exception as e:
            self.result = f"Translation failed: {e}"
            self.transStatus = False
        return self.result

    def statusCheck(self) -> bool:
        # Checks if the translation process is complete.
        return self.transStatus

    def getResult(self) -> str:
        # Retrieves the translation result.
        return self.result
    
    def getID(self) -> int:
        # Retrieves unique identifier for this handler
        return self.handlerID

