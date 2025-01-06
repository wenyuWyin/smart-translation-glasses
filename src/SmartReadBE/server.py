from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
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

@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload Server</title>
    </head>
    <body>
        <h1>Welcome to the Image Upload Server</h1>
        <p>Use the POST endpoint <code>/upload</code> to upload an image.</p>
    </body>
    </html>
    """
    return render_template_string(html_content)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)