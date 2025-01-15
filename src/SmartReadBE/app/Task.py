import cv2
import uuid
import base64

from TextExtractionModule.TextExtractionManager import TextExtractionManager
from TranslationModule.TranslationManager import TranslationManager
from TranslationModule.LanguageConvertor import convert_language
from .WebSocketHandler import send_image_process_status
from .TaskState import TaskState


class Task:
    def __init__(
        self,
        user_id: int,
        task_id: int,
        extraction_manager: TextExtractionManager,
        image: cv2.Mat,
        translation_manager: TranslationManager,
        target_language: str,
        source_language: str,
    ):
        # Initializes a task
        self.user_id = user_id
        self.task_id = task_id
        self.task_status = False  # Indicates whether the task is initialized

        self.extraction_manager = extraction_manager  # TextExtractionManager instance
        self.image = image  # Image for text extraction
        self.translation_manager = translation_manager
        self.target_language = target_language  # Target language for translation
        self.source_language = source_language  # Source language for translation
        self.results = {}

    def get_status(self) -> bool:
        return self.task_status

    def set_status(self, status: bool) -> None:
        self.task_status = status

    def initialize(self) -> bool:
        self.set_status(True)
        return True

    def execute_task(self) -> bool:
        _, image_buffer = cv2.imencode(".jpg", self.image)
        socket_data = {
            "state": TaskState.IMAGE_RECEIVED.value,
            "image": base64.b64encode(image_buffer).decode("utf-8"),
        }

        send_image_process_status(self.user_id, TaskState.IMAGE_RECEIVED, data=socket_data)
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
        results = {key: {} for key in segmentation_results}

        send_image_process_status(self.user_id, TaskState.TEXT_EXTRACTED)

        # Extract text and translate for each sub-image
        print(f"Executing TextExtractionTask {self.task_id}")
        for key, value in segmentation_results.items():
            extracted_text = self.extraction_manager.extract(
                value, self.source_language
            )

            if not extracted_text:
                print(f"Text extraction failed for task {self.task_id} segment {key}.")

            results[key]["org_text"] = extracted_text if extracted_text else ""
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

            results[key]["trn_text"] = translated_text
            print(f"Translation completed. Translated text: {translated_text}")

        # Save results to Firebase storage and database
        storage_image_url = save_image(self.user_id)
        self.results[storage_image_url] = results
        self.save_task_result()

        print("Task results saved to Firebase")

        socket_data = {
            "state": TaskState.TRANSLATED.value,
            "result": {str(key): value for key, value in results.items()},
        }
        send_image_process_status(self.user_id, TaskState.TRANSLATED, data=socket_data)

        return True

    def terminate_task(self) -> bool:
        if not self.get_status():
            print(f"Task {self.task_id} is not active.")
            return False
        print(f"Terminating task {self.task_id}")
        self.set_status(False)
        return True

    def save_task_result(self) -> bool:
        from .Config import db

        if not self.results:
            return None

        serialized_data = {
            url: {
                str(inner_key): inner_value
                for inner_key, inner_value in nested_dict.items()
            }
            for url, nested_dict in self.results.items()
        }
        try:
            user_ref = db.collection("users").document(self.user_id)
            user_ref.update({"history": serialized_data})
            print(f"Data successfully stored for user: {self.user_id}")

            return True
        except Exception as e:
            print(f"An error occurred: {e}")

            return False


def save_image(user_id: int):
    from firebase_admin import storage

    image_id = uuid.uuid4()
    local_file_path = "TEMP/image.jpg"
    destination_blob_name = f"{user_id}/{image_id}.jpg"

    bucket = storage.bucket()
    blob = bucket.blob(destination_blob_name)

    try:
        # Upload the file
        blob.upload_from_filename(local_file_path)

        # Make the file publicly accessible (optional)
        blob.make_public()

        print(f"File uploaded successfully. Public URL: {blob.public_url}")

        return blob.public_url
    except Exception as e:
        print(f"An error occurred: {e}")

        return None
