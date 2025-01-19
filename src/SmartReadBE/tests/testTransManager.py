import unittest
from unittest.mock import patch, MagicMock
from TranslationModule.TranslationManager import TranslationManager

class TestTranslationManager(unittest.TestCase):
    @patch("TranslationModule.TranslationManager.importlib.import_module")
    def test_initialize_success(self, mock_import_module):
        # Mock the dynamically imported class
        MockTranslatorClass = MagicMock()
        mock_instance = MagicMock()
        mock_instance.getID.side_effect = ["translator_1", "translator_2"]

        # Set the return value for the imported module and class
        mock_import_module.return_value = MagicMock()
        setattr(mock_import_module.return_value, "GoogleTranslator", MockTranslatorClass)
        MockTranslatorClass.side_effect = [mock_instance, mock_instance]

        manager = TranslationManager()
        result = manager.initialize()

        self.assertTrue(result)
        self.assertEqual(len(manager.translators), 2)
        self.assertEqual(manager.avail_translators, ["translator_1", "translator_2"])
        mock_import_module.assert_called_once_with("TranslationModule.GoogleTranslator")

    @patch("TranslationModule.TranslationManager.importlib.import_module")
    def test_initialize_failure(self, mock_import_module):
        # Simulate import failure
        mock_import_module.side_effect = ImportError("Module not found")

        manager = TranslationManager()
        result = manager.initialize()

        self.assertFalse(result)
        self.assertEqual(len(manager.translators), 0)
        self.assertEqual(manager.avail_translators, [])

    @patch("TranslationModule.TranslationManager.TranslationManager.initialize")
    def test_translate_success(self, mock_initialize):
        # Mock the translator instance
        MockTranslator = MagicMock()
        mock_instance = MagicMock()
        mock_instance.translate.return_value = "Translated Text"
        mock_instance.statusCheck.return_value = True
        mock_instance.getID.return_value = "translator_1"

        # Set up TranslationManager with mocked translator
        manager = TranslationManager()
        manager.translators["translator_1"] = mock_instance
        manager.avail_translators = ["translator_1"]

        result = manager.translate("Hello", "en", "zh")

        self.assertEqual(result, "Translated Text")
        mock_instance.translate.assert_called_once_with("Hello", "en", "zh")
        mock_instance.statusCheck.assert_called_once()

    def test_translate_no_available_handler(self):
        # Initialize a TranslationManager with no available handlers
        manager = TranslationManager()
        manager.translators = {}
        manager.avail_translators = []

        result = manager.translate("Hello", "en", "zh")

        self.assertEqual(result, "An error occurred during translation.")

    @patch("TranslationModule.TranslationManager.TranslationManager.initialize")
    def test_translate_failed_status_check(self, mock_initialize):
        # Mock the translator instance
        MockTranslator = MagicMock()
        mock_instance = MagicMock()
        mock_instance.translate.return_value = "Incomplete Translation"
        mock_instance.statusCheck.return_value = False
        mock_instance.getID.return_value = "translator_1"

        # Set up TranslationManager with mocked translator
        manager = TranslationManager()
        manager.translators["translator_1"] = mock_instance
        manager.avail_translators = ["translator_1"]

        result = manager.translate("Hello", "en", "zh")

        self.assertEqual(result, "Translation failed or incomplete.")
        mock_instance.translate.assert_called_once_with("Hello", "en", "zh")
        mock_instance.statusCheck.assert_called_once()

if __name__ == "__main__":
    unittest.main()
