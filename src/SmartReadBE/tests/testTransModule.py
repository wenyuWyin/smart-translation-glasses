import unittest
from unittest.mock import patch, MagicMock
from TranslationModule.TranslationManager import TranslationManager


class TestTranslationModule(unittest.TestCase):
    @patch("TranslationModule.TranslationManager.importlib.import_module")
    def test_initialize_success(self, mock_import_module):
        # UT-01: TranslatorInitializationTest
        manager = TranslationManager()
        result = manager.initialize()

        self.assertTrue(result)
        self.assertEqual(len(manager.translators), 1)

    @patch("TranslationModule.TranslationManager.importlib.import_module")
    def test_invalid_translator_handlers(self, mock_import_module):
        # UT-02: InvalidTranslatorHandlersTest
        # Simulate import failure
        mock_import_module.side_effect = ImportError("Module not found")

        manager = TranslationManager()
        result = manager.initialize()

        self.assertFalse(result)
        self.assertEqual(len(manager.translators), 0)
        self.assertEqual(manager.avail_translators, [])

    @patch("TranslationModule.TranslationManager.importlib.import_module")
    def test_no_available_translator_handler(self, mock_import_module):
        # UT-03: NoAvailableTranslatorHandlersTest
        manager = TranslationManager()
        # Initialize a TranslationManager with no available handlers
        manager.AVALIABLETRANSLATOR = []
        result = manager.initialize()

        self.assertFalse(result)
        self.assertEqual(len(manager.translators), 0)
        self.assertEqual(manager.avail_translators, [])

    @patch("TranslationModule.TranslationManager.TranslationManager.initialize")
    def test_translate(self, mock_initialize):
        # UT-04: TranslateTest
        # Mock the translator instance
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


if __name__ == "__main__":
    unittest.main()
