"""
Unit test file for TextExtractionModule
"""

import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from TextExtractionModule.TextExtractionManager import TextExtractionManager as tem
import cv2


TEXT_ACC_BOUND = 0.95
IOU_BOUND = 0.6


# Helper functions
def capture_outputs(test_name, actual_output):
    with open("test_outputs.txt", "a") as f:
        f.write(f"{test_name}:\n{actual_output}\n\n")


def levenshtein_distance(s1: str, s2: str) -> int:
    # Computes the Levenshtein Distance between two strings.
    s1, s2 = s1.lower(), s2.lower()  # Convert both strings to lowercase
    len_s1, len_s2 = len(s1), len(s2)
    dp = np.zeros((len_s1 + 1, len_s2 + 1), dtype=int)

    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # Deletion
                dp[i][j - 1] + 1,  # Insertion
                dp[i - 1][j - 1] + cost,
            )  # Substitution

    return dp[len_s1][len_s2]


def levenshtein_accuracy(s1: str, s2: str) -> float:
    # Computes the normalized accuracy score based on Levenshtein Distance.
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return round(1 - (distance / max_len), 4) if max_len > 0 else 1.0


def iou(boxA, boxB):
    # Computes Intersection over Union (IoU) between two bounding boxes.
    xA = max(boxA[0], boxB[0])
    xB = max(boxA[1], boxB[1])
    yA = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)

    boxAArea = (boxA[1] - boxA[0]) * (boxA[3] - boxA[2])
    boxBArea = (boxB[1] - boxB[0]) * (boxB[3] - boxB[2])

    unionArea = boxAArea + boxBArea - interArea
    return interArea / unionArea if unionArea > 0 else 0


def mean_iou(ground_truth_boxes, extracted_boxes):
    # Computes the normalized accuracy score.
    ious = [iou(gt, ex) for gt, ex in zip(ground_truth_boxes, extracted_boxes)]
    return sum(ious) / len(ious) if ious else 0


class testSegExt(unittest.TestCase):
    @patch("TextExtractionModule.TextExtractionManager.importlib.import_module")
    def test_initialize_success(self, mock_import_module):
        # UT-01-2: ExtractorsAndSegmentorsInitializationTest
        manager = tem()
        result = manager.initialize()

        self.assertTrue(result)
        self.assertEqual(len(manager.extractors), 1)
        self.assertEqual(len(manager.segmentors), 1)

    @patch("TextExtractionModule.TextExtractionManager.importlib.import_module")
    def test_invalid_extractors_and_segmentors_handlers(self, mock_import_module):
        # UT-02-2: InvalidExtractorsAndSegmentorsHandlersTest
        # Simulate import failure
        mock_import_module.side_effect = ImportError("Module not found")

        manager = tem()
        result = manager.initialize()

        self.assertFalse(result)
        self.assertEqual(len(manager.extractors), 0)
        self.assertEqual(len(manager.segmentors), 0)
        self.assertEqual(manager.avail_extractors, [])
        self.assertEqual(manager.avail_segmentors, [])

    @patch("TextExtractionModule.TextExtractionManager.importlib.import_module")
    def test_no_available_extractors_and_segmentors_handler(self, mock_import_module):
        # UT-03-2: NoAvailableExtractorsAndSegmentorsTest
        manager = tem()
        # Initialize a TranslationManager with no available handlers
        manager.AVAILABLE_OCR_HANDLERS = []
        manager.AVAILABLE_SEGMENTATION_HANDLERS = []
        result = manager.initialize()

        self.assertFalse(result)
        self.assertEqual(len(manager.extractors), 0)
        self.assertEqual(len(manager.segmentors), 0)
        self.assertEqual(manager.avail_extractors, [])
        self.assertEqual(manager.avail_segmentors, [])

    def test_single_region_segmentation(self):
        # UT-05 SingleRegionSegmentationTest
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_05.jpg"  # path

        image = cv2.imread(img_path)
        segmentation_results = list(manager.segmentation(image).keys())
        expected_output = [(43, 609, 28, 62)]
        capture_outputs("UT-05", segmentation_results)  # Store result
        self.assertEqual(len(expected_output), len(segmentation_results))
        accuracy = mean_iou(segmentation_results, expected_output)

        self.assertGreaterEqual(accuracy, IOU_BOUND)

    def test_multiple_region_segmentation(self):
        # UT-06 MultipleRegionSegmentationTest
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_06.jpg"  # path

        image = cv2.imread(img_path)
        segmentation_results = list(manager.segmentation(image).keys())
        expected_output = [(14, 607, 15, 49), (14, 551, 73, 107), (14, 567, 126, 160)]
        capture_outputs("UT-06", segmentation_results)  # Store result
        self.assertEqual(len(expected_output), len(segmentation_results))
        accuracy = mean_iou(segmentation_results, expected_output)

        self.assertGreaterEqual(accuracy, IOU_BOUND)

    def test_no_text_segmentation(self):
        # UT-07 NoTextSegmentationTest
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_07.jpg"  # path

        image = cv2.imread(img_path)
        segmentation_results = list(manager.segmentation(image).keys())
        expected_output = []  # should be empty

        capture_outputs("UT-07", segmentation_results)  # Store result
        self.assertEqual(expected_output, segmentation_results)

    def test_normal_text_extraction(self):
        # UT-08 Normal text extraction test
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_08.jpg"  # path

        image = cv2.imread(img_path)
        extracted_text = manager.extract(image, "en")
        expected_output = "The river flows gently through the valley, reflecting the golden sunset. Birds sing in the trees, while a cool breeze carries the scent of blooming flowers across the peaceful landscape."
        # text
        accuracy = levenshtein_accuracy(extracted_text, expected_output)

        capture_outputs("UT-08", extracted_text)  # Store result
        self.assertGreaterEqual(accuracy, TEXT_ACC_BOUND)

    def test_normal_text_extraction_multiple_region(self):
        # UT-08-2 Normal text extraction test with multiple region text
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_08_2.jpg"  # path

        image = cv2.imread(img_path)
        extracted_text = manager.extract(image, "en")
        expected_output = """The sun dipped below the horizon, painting the sky in hues of orange and purple. Waves whispered against the shore, a serene end to day.
        In the digital age, innovation accelerates, connecting minds across continents. Yet, amidst progress, the quest for balance between advancement and ethics continues.
        She paused, reflecting on journeys taken and paths untraveled. Growth often blooms in quiet moments of introspection, where courage meets vulnerability."""  # text
        accuracy = levenshtein_accuracy(extracted_text, expected_output)

        capture_outputs("UT-08-2", extracted_text)  # Store result
        self.assertGreaterEqual(accuracy, TEXT_ACC_BOUND)

    def test_no_text_extraction(self):
        # UT-09 NoTextExtraction
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_09.jpg"  # path

        image = cv2.imread(img_path)
        extracted_text = manager.extract(image, "en")
        if extracted_text is None:
            extracted_text = ""
        expected_output = ""  # should be empty
        accuracy = levenshtein_accuracy(extracted_text, expected_output)

        capture_outputs("UT-09", extracted_text)  # Store result
        self.assertGreaterEqual(accuracy, TEXT_ACC_BOUND)

    def test_bright_text_extraction(self):
        # UT-10 BrightTextExtractionAccuracy
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_10.jpg"  # path

        image = cv2.imread(img_path)
        extracted_text = manager.extract(image, "en")
        expected_output = "molly hooper mortician//020.7946.0287 LLY@BARTH"  # text
        accuracy = levenshtein_accuracy(extracted_text, expected_output)

        capture_outputs("UT-10", extracted_text)  # Store result
        self.assertGreaterEqual(accuracy, TEXT_ACC_BOUND)

    def test_dark_text_extraction(self):
        # UT-11 DarkTextExtractionAccuracy
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_11.jpg"  # path

        image = cv2.imread(img_path)
        extracted_text = manager.extract(image, "en")
        expected_output = "molly hooper mortician//020.7946.0287 LLY@BARTH"  # text
        accuracy = levenshtein_accuracy(extracted_text, expected_output)

        capture_outputs("UT-11", extracted_text)  # Store result
        self.assertGreaterEqual(accuracy, TEXT_ACC_BOUND)

    def test_normallight_text_extraction(self):
        # UT-12 NormalLightTextExtractionAccuracy
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_12.jpg"  # path

        image = cv2.imread(img_path)
        extracted_text = manager.extract(image, "en")
        expected_output = "molly hooper mortician//020.7946.0287 LLY@BARTH"  # text
        accuracy = levenshtein_accuracy(extracted_text, expected_output)

        capture_outputs("UT-12", extracted_text)  # Store result
        self.assertGreaterEqual(accuracy, TEXT_ACC_BOUND)

    def test_overlighting_text_extraction(self):
        # UT-13 OverLightingTextExtractionAccuracy
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_13.jpg"  # path

        image = cv2.imread(img_path)
        extracted_text = manager.extract(image, "en")
        expected_output = "molly hooper mortician//020.7946.0287 LLY@BARTH"  # text
        accuracy = levenshtein_accuracy(extracted_text, expected_output)

        capture_outputs("UT-13", extracted_text)  # Store result
        self.assertGreaterEqual(accuracy, TEXT_ACC_BOUND)

    def test_underlighting_text_extraction(self):
        # UT-14 UnderLightingTextExtractionAccuracy
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_14.jpg"  # path

        image = cv2.imread(img_path)
        extracted_text = manager.extract(image, "en")
        expected_output = "molly hooper mortician//020.7946.0287 LLY@BARTH"  # text
        accuracy = levenshtein_accuracy(extracted_text, expected_output)

        capture_outputs("UT-14", extracted_text)  # Store result
        self.assertGreaterEqual(accuracy, TEXT_ACC_BOUND)

    def test_arial_segmentation(self):
        # UT-15 ArialSegmentation
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_15.jpg"  # path

        image = cv2.imread(img_path)
        segmentation_results = list(manager.segmentation(image).keys())
        expected_output = [(17, 300, 8, 108)]
        capture_outputs("UT-15", segmentation_results)  # Store result
        self.assertEqual(len(expected_output), len(segmentation_results))
        accuracy = mean_iou(segmentation_results, expected_output)

        self.assertGreaterEqual(accuracy, IOU_BOUND)

    def test_calibri_segmentation(self):
        # UT-16 CalibriSegmentation
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_16.jpg"  # path

        image = cv2.imread(img_path)
        segmentation_results = list(manager.segmentation(image).keys())
        expected_output = [(42, 629, 256, 438), (42, 629, 509, 680), (42, 640, 12, 187)]
        capture_outputs("UT-16", segmentation_results)  # Store result
        self.assertEqual(len(expected_output), len(segmentation_results))
        accuracy = mean_iou(segmentation_results, expected_output)

        self.assertGreaterEqual(accuracy, IOU_BOUND)

    def test_arial_text_extraction(self):
        # UT-17 ArialTextExtractionAccuracy
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_17.jpg"  # path

        image = cv2.imread(img_path)
        extracted_text = manager.extract(image, "en")
        expected_output = "LEG TICKETS .NL"  # text
        accuracy = levenshtein_accuracy(extracted_text, expected_output)

        capture_outputs("UT-17", extracted_text)  # Store result
        self.assertGreaterEqual(accuracy, TEXT_ACC_BOUND)

    def test_calibri_text_extraction(self):
        # UT-18 CalibriTextExtractionAccuracy
        manager = tem()
        manager.initialize()
        img_path = r"imgs\ut_18.jpg"  # path

        image = cv2.imread(img_path)
        extracted_text = manager.extract(image, "en")
        expected_output = "Calibri Calibri Calibri"  # text
        accuracy = levenshtein_accuracy(extracted_text, expected_output)

        capture_outputs("UT-18", extracted_text)  # Store result
        self.assertGreaterEqual(accuracy, TEXT_ACC_BOUND)


if __name__ == "__main__":
    unittest.main()
