"""
TranslationManager manages translator instances and handles translation tasks.
"""

import importlib


class TranslationManager:
    AVALIABLETRANSLATOR = ["TranslationModule.GoogleTranslator"]

    def __init__(self):
        # Initializes the TranslationManager
        self.translators = dict()  # An object implementing TranslationHandler
        self.avail_translators = []

    def initialize(self) -> bool:
        try:
            for translator_class_name in self.AVALIABLETRANSLATOR:
                # Dynamically import the class from the current folder
                class_name = translator_class_name.rsplit(".", 1)[1]
                module = importlib.import_module(translator_class_name)

                # Get the class from the module
                translator_class = getattr(module, class_name)

                if translator_class is None:
                    print(f"Error: Class {class_name} not found.")
                    return False

                # Create two instances of the class
                for i in range(2):
                    instance = translator_class()  # Create an instance of the class
                    self.translators[instance.getID()] = (
                        instance  # Store the instance in the dictionary
                    )
                    self.avail_translators.append(instance.getID())

            return True  # Initialization successful
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False

    def translate(
        self,
        inputTxt: str,
        targetLanguage: str,
        sourceLanguage: str = None,
    ) -> str:
        # Performs translation using the assigned TranslationHandler instance.
        try:
            handlerID = self.avail_translators.pop()
            if not handlerID:
                raise Exception("No available handler for translation.")

            handler = self.translators.get(handlerID)
            # Perform translation
            translated_text = handler.translate(
                inputTxt, targetLanguage, sourceLanguage
            )
            self.avail_translators.append(handlerID)

            # Check translation status
            if handler.statusCheck():
                return translated_text
            else:
                return "Translation failed or incomplete."
        except Exception as e:
            print(f"Translation error: {e}")
            return "An error occurred during translation."
