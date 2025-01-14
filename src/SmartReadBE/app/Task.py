from TextExtractionModule.TextExtractionManager import TextExtractionManager
from TranslationModule.TranslationManager import TranslationManager
from TranslationModule.LanguageConvertor import convert_language
import cv2


class Task:
    def __init__(
        self,
        task_id: int,
        extraction_manager: TextExtractionManager,
        image: cv2.Mat,
        translation_manager: TranslationManager,
        target_language: str,
        source_language: str,
    ):
        # Initializes a task
        self.task_id = task_id
        self.task_status = False  # Indicates whether the task is initialized

        self.extraction_manager = extraction_manager  # TextExtractionManager instance
        self.image = image  # Image for text extraction
        self.translation_manager = translation_manager
        self.target_language = target_language  # Target language for translation
        self.source_language = source_language  # Source language for translation
        self.results = None

    def get_status(self) -> bool:
        return self.task_status

    def set_status(self, status: bool) -> None:
        self.task_status = status

    def initialize(self) -> bool:
        self.set_status(True)
        return True

    def execute_task(self) -> bool:
        # Execute a task
        # Divide the image into sub-images -> Extract text on each sub-image -> Translate the extracted text
        segmentation_results = self.extraction_manager.segmentation(self.image)
        print("Segmentation completed")

        if not segmentation_results:
            print(f"Image Segmentation failed for task {self.task_id}.")
            return False

        print(f"Image Segmentation successfully for task {self.task_id}")

        # Initialize the result dictionary
        # Each sub-image corresponds to an original text and translated text
        self.results = {key: {} for key in segmentation_results}

        # Extract text and translate for each sub-image
        print(f"Executing TextExtractionTask {self.task_id}")
        for key, value in segmentation_results.items():
            extracted_text = self.extraction_manager.extract(
                value, self.source_language
            )

            if not extracted_text:
                print(f"Text extraction failed for task {self.task_id} segment {key}.")

            self.results[key]["org_text"] = extracted_text if extracted_text else ""
            print(
                f"Text extracted successfully for task {self.task_id} segment {key}: {extracted_text}"
            )

            # Translate extract text
            translated_text = self.translation_manager.translate(
                extracted_text,
                convert_language(self.target_language),
                convert_language(self.source_language),
            )

            # Assign empty text for translation failure
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
