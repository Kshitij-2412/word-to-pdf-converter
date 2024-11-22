from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from docx import Document
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure CORS
CORS(app, resources={r"/*": {
    "origins": ["http://localhost:3000", "http://localhost:5000", "http://frontend:3000", "http://api_gateway:5000"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "expose_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True,
    "send_wildcard": False
}})

# Configuration
UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'docx'}

# Create necessary directories
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    logger.info(f"Upload directory created/verified at {UPLOAD_FOLDER}")
    # Test write permissions
    test_file = os.path.join(UPLOAD_FOLDER, 'test.txt')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    logger.info("Write permissions verified for upload directory")
except Exception as e:
    logger.error(f"Error setting up upload directory: {str(e)}")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    logger.debug(f"Checking file type for: {filename}")
    if '.' not in filename:
        logger.debug("No file extension found")
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    logger.debug(f"File extension: {ext}")
    return ext in ALLOWED_EXTENSIONS

def format_file_size(size_in_bytes):
    # Convert bytes to human readable format
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"

def format_date(date_obj):
    if not date_obj:
        return ''
    try:
        return date_obj.strftime("%Y-%m-%d %I:%M %p")
    except:
        return ''

def get_document_metadata(doc_path):
    try:
        logger.debug(f"Extracting metadata from: {doc_path}")
        file_size = os.path.getsize(doc_path)
        modified_time = datetime.fromtimestamp(os.path.getmtime(doc_path))
        
        metadata = {
            'filename': os.path.basename(doc_path),
            'size': file_size,  # Send raw size in bytes
            'upload_time': modified_time.isoformat()  # Send ISO format string
        }
        logger.debug(f"Extracted metadata: {metadata}")
        return metadata
    except Exception as e:
        logger.error(f"Error extracting metadata: {str(e)}")
        return {}

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        logger.debug("Received upload request")
        logger.debug(f"Files in request: {request.files}")
        logger.debug(f"Request headers: {request.headers}")
        
        if 'file' not in request.files:
            logger.error("No file part in request")
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        logger.debug(f"Received file: {file.filename}")
        
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type. Only .docx files are allowed'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = os.path.splitext(filename)[0]
        unique_filename = f"{base_filename}_{timestamp}.docx"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        logger.debug(f"Saving file to: {file_path}")
        file.save(file_path)
        
        # Get metadata
        metadata = get_document_metadata(file_path)
        
        response_data = {
            'message': 'File uploaded successfully',
            'filename': unique_filename,
            'metadata': metadata
        }
        logger.debug(f"Upload successful: {response_data}")
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.exception("Upload error")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
