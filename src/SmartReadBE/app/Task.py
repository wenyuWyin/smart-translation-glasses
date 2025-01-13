from SmartReadBE.TextExtractionModule.TextExtractionManager import TextExtractionManager
from SmartReadBE.TranslationModule.TranslationManager import TranslationManager
import cv2


class Task:
    def __init__(
        self,
        task_id: int,
        extraction_manager: TextExtractionManager,
        ocr_handler_id: str,
        seg_handler_id: str,
        image: cv2.Mat,
        language: str,
        translation_manager: TranslationManager,
        trn_handler_id: str,
        target_language: str,
        source_language: str,
    ):
        # Initializes a task
        self.task_id = task_id
        self.task_status = False  # Indicates whether the task is initialized

        self.extraction_manager = extraction_manager  # TextExtractionManager instance
        self.ocr_handler_id = ocr_handler_id
        self.seg_handler_id = seg_handler_id
        self.image = image  # Image for text extraction
        self.language = language  # Language for OCR
        self.translation_manager = translation_manager
        self.trn_handler_id = trn_handler_id
        self.target_language = target_language  # Target language for translation
        self.source_language = source_language  # Source language for translation
        self.results = None

    def get_status(self) -> bool:
        return self.task_status

    def set_status(self, status: bool) -> None:
        self.task_status = status

    def initialize(self) -> bool:
        print(f"Initializing task {self.task_id} of type {self.task_type}")
        self.set_status(True)
        return True

    def execute_task(self) -> bool:
        segmentation_results = self.extraction_manager.segmentation(
            self.seg_handler_id, self.image
        )

        if not segmentation_results:
            print(f"Image Segmentation failed for task {self.task_id}.")
            return False

        print(f"Image Segmentation successfully for task {self.task_id}")

        self.results = {key: {} for key in segmentation_results}

        print(f"Executing TextExtractionTask {self.task_id}")
        for key, value in segmentation_results.items():
            extracted_text = self.extraction_manager.extract(
                self.ocr_handler_id, value, self.language
            )

            if not extracted_text:
                print(f"Text extraction failed for task {self.task_id} segment {key}.")

            self.results[key]["org_text"] = extracted_text if extracted_text else ""
            print(
                f"Text extracted successfully for task {self.task_id} segment {key}: {extracted_text}"
            )

            translated_text = self.translation_manager.doTranslate(
                self.trn_handler_id,
                extracted_text,
                self.target_language,
                self.source_language,
            )

            if translated_text.startswith(
                "Translation failed"
            ) or translated_text.startswith("An error"):
                print(f"Task {self.task_id} for {extracted_text}: {translated_text}")
                translated_text = ""

            self.results[key]["trn_text"] = translated_text
            print(f"Translation completed. Translated text: {translated_text}")

            # TODO
            # sends results to frontend and stores in cloud

        return True

    def terminate_task(self) -> bool:
        if not self.get_status():
            print(f"Task {self.task_id} is not active.")
            return False
        print(f"Terminating task {self.task_id}")
        self.set_status(False)
        return True
