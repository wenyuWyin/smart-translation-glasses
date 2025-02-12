import unittest
from unittest.mock import MagicMock, patch
from app.Task import Task


class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task("test_user", "1", None, None, None, "English", "French")

    @patch("app.Config.db")
    def test_save_translation_result_success(self, mock_db):
        self.task.results = {
            "http://example.com": {
                (1, 2, 3, 4): {"org_text": "test_text", "trn_text": "translated_text"}
            }
        }

        mock_user_ref = MagicMock()

        mock_db.collection.return_value.document.return_value = mock_user_ref

        # Call the method
        result = self.task.save_task_result()

        # Assertions
        self.assertTrue(result)
        mock_db.collection.assert_called_with("users")
        mock_user_ref.set.assert_called_once_with(
            {
                "history": {
                    "http://example.com": {
                        "(1, 2, 3, 4)": {
                            "org_text": "test_text",
                            "trn_text": "translated_text",
                        }
                    }
                }
            },
            merge=True,
        )

    @patch("app.Config.db")
    def test_save_translation_result_failed(self, mock_db):
        self.task.results = {}

        mock_user_ref = MagicMock()

        mock_db.collection.return_value.document.return_value = mock_user_ref

        # Call the method
        result = self.task.save_task_result()

        # Assertions
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
