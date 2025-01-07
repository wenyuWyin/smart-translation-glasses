from flask import Flask, request, render_template_string
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import timedelta
import os
from dotenv import load_dotenv

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'

try:
    # Firebase Admin SDK setup
    cred = credentials.Certificate("firebaseAuth.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Attempt to fetch a collection (e.g., `test_collection`)
    docs = db.collection('users').get()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    print("Firebase connection successful!")
except Exception as e:
    print(f"Firebase connection failed: {e}")

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
    
@app.route('/lang-pref', methods=['POST'])
def save_language_preference():
    data = request.get_json() 
    source_lang = data.get('sourceLang')
    target_lang = data.get('targetLang')
    
    print(f'{source_lang} - {target_lang}')
    
    return "Language Preference Received", 200

@app.route('/', methods=['GET'])
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sample Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to My Flask Server</h1>
        <p>This is a sample HTML response from a GET request.</p>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)