from flask import Blueprint, render_template_string

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
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
