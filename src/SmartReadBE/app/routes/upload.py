from flask import Blueprint, request
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files and not request.data:
        return "No file part", 400

    try:
        image_data = request.data
        filename = os.path.join(UPLOAD_FOLDER, "image.jpg")
        with open(filename, 'wb') as f:
            f.write(image_data)
        print(f"Image is saved to {filename}")
        return "Image received", 200
    except Exception as e:
        print(f"Error saving image: {e}")
        return "Failed to save image", 500
