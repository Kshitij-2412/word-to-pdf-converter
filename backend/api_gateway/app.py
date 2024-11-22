from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import requests
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
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "expose_headers": ["Content-Type", "Authorization", "Content-Disposition"],
    "supports_credentials": False,
    "send_wildcard": False
}})

# Service URLs (using Docker service names)
UPLOAD_SERVICE_URL = 'http://upload_service:5001'
CONVERSION_SERVICE_URL = 'http://conversion_service:5002'

@app.route('/api/upload', methods=['POST', 'OPTIONS'])
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
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({'error': 'No selected file'}), 400
            
        files = {'file': (file.filename, file.stream, file.content_type)}
        logger.debug(f"Forwarding file to upload service: {file.filename}")
        
        response = requests.post(f"{UPLOAD_SERVICE_URL}/upload", files=files)
        logger.debug(f"Upload service response: {response.status_code} - {response.text}")
        return response.json(), response.status_code
    except Exception as e:
        logger.error(f"Error in upload: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/convert', methods=['POST'])
def convert_file():
    try:
        logger.debug("Received convert request")
        logger.debug(f"Files in request: {request.files}")
        logger.debug(f"Request headers: {request.headers}")
        
        if 'file' not in request.files:
            logger.error("No file part in request")
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({'error': 'No selected file'}), 400
            
        files = {'file': (file.filename, file.stream, file.content_type)}
        data = {}
        
        # Add password if provided
        if 'password' in request.form:
            data['password'] = request.form['password']
            
        logger.debug(f"Forwarding file to conversion service: {file.filename}")
        
        response = requests.post(
            f"{CONVERSION_SERVICE_URL}/convert",
            files=files,
            data=data
        )
        
        logger.debug(f"Conversion service response: {response.status_code} - {response.text}")
        return response.json(), response.status_code
        
    except Exception as e:
        logger.error(f"Error in conversion: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        logger.debug(f"Download request for file: {filename}")
        
        # Get the file from conversion service
        response = requests.get(f"{CONVERSION_SERVICE_URL}/download/{filename}", stream=True)
        
        if response.status_code != 200:
            logger.error(f"Error getting file from conversion service: {response.text}")
            return jsonify({"error": "File not found"}), 404
            
        # Stream the file to the client
        return Response(
            response.iter_content(chunk_size=8192),
            content_type='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Length': response.headers.get('content-length', '')
            }
        )
        
    except Exception as e:
        logger.error(f"Error in download: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring deployment status"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'wordtopdf-api',
        'version': '1.0.0'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
