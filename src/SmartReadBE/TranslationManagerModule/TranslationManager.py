"""
TranslationManager manages translator instances and handles translation tasks.
"""
import importlib

class TranslationManager:
    AVALIABLETRANSLATOR = ["GoogleTranslator"]

    def __init__(self):
        # Initializes the TranslationManager
        self.translators = dict() # An object implementing TranslationHandler

    def Initialize(self) -> bool:
        try:
            for translator_class_name in self.AVALIABLETRANSLATOR:
                # Dynamically import the class from the current folder
                module = importlib.import_module(translator_class_name)

                # Get the class from the module
                translator_class = getattr(module, translator_class_name)
                
                if translator_class is None:
                    print(f"Error: Class {translator_class_name} not found.")
                    return False

                # Create two instances of the class
                for i in range(2):
                    instance = translator_class()  # Create an instance of the class
                    self.translators[instance.getID()] = instance  # Store the instance in the dictionary

            return True  # Initialization successful
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False
 
    def doTranslate(self, handlerID: str, inputTxt: str, targetLanguage: str, sourceLanguage: str = None) -> str:
        # Performs translation using the assigned TranslationHandler instance.
        
        try:
            # Perform translation
            translated_text = self.translators.get(handlerID).translate(inputTxt, targetLanguage, sourceLanguage)
            
            # Check translation status
            if self.translators.get(handlerID).statusCheck():
                return translated_text
            else:
                return "Translation failed or incomplete."
        except Exception as e:
            print(f"Translation error: {e}")
            return "An error occurred during translation."