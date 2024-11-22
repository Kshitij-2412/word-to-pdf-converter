from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess
from werkzeug.utils import secure_filename
import logging
import time
from datetime import datetime
import PyPDF2

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload and output directories
app.config['UPLOAD_FOLDER'] = '/app/uploads'
app.config['OUTPUT_FOLDER'] = '/app/output'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def convert_to_pdf(input_path):
    """
    Convert DOCX to PDF using LibreOffice
    """
    try:
        filename = os.path.basename(input_path)
        output_dir = app.config['OUTPUT_FOLDER']
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.pdf')

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Use LibreOffice for conversion
        cmd = ['soffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, input_path]
        
        logger.info(f"Running conversion command: {' '.join(cmd)}")
        process = subprocess.run(cmd, capture_output=True, text=True)
        
        if process.returncode != 0:
            logger.error(f"Conversion failed: {process.stderr}")
            return None
            
        if not os.path.exists(output_path):
            logger.error(f"Output file not found at {output_path}")
            return None
            
        logger.info(f"Successfully converted {filename} to PDF")
        return output_path
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        return None

def encrypt_pdf(input_path, output_path, password):
    """
    Encrypt a PDF file with a password
    """
    try:
        reader = PyPDF2.PdfReader(input_path)
        writer = PyPDF2.PdfWriter()

        # Copy all pages from reader to writer
        for page in reader.pages:
            writer.add_page(page)

        # Encrypt with the provided password
        writer.encrypt(password)

        # Save the encrypted PDF
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        return True
    except Exception as e:
        logger.error(f"Error encrypting PDF: {str(e)}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "conversion"}), 200

@app.route('/convert', methods=['POST'])
def convert():
    try:
        logger.info("Received conversion request")
        
        if 'file' not in request.files:
            logger.error("No file part in request")
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            logger.error("No selected file")
            return jsonify({'error': 'No selected file'}), 400
            
        if not file.filename.endswith('.docx'):
            logger.error("Invalid file type")
            return jsonify({'error': 'Only .docx files are supported'}), 400

        # Get password if provided
        password = request.form.get('password')
        logger.info(f"Password protection requested: {'yes' if password else 'no'}")

        # Create unique filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_filename = f"{timestamp}_{secure_filename(file.filename)}"
        temp_pdf_filename = f"{os.path.splitext(input_filename)[0]}_temp.pdf"
        output_filename = f"{os.path.splitext(input_filename)[0]}.pdf"
        
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        temp_pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], temp_pdf_filename)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Save the uploaded file
        file.save(input_path)
        logger.info(f"Saved input file to {input_path}")
        
        try:
            # Convert DOCX to PDF
            convert_cmd = [
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', app.config['OUTPUT_FOLDER'],
                input_path
            ]
            
            logger.info(f"Running conversion command: {' '.join(convert_cmd)}")
            process = subprocess.run(convert_cmd, capture_output=True, text=True)
            
            if process.returncode != 0:
                logger.error(f"Conversion failed: {process.stderr}")
                return jsonify({'error': 'Conversion failed'}), 500

            # Move the converted file to temp location
            os.rename(
                os.path.join(app.config['OUTPUT_FOLDER'], f"{os.path.splitext(input_filename)[0]}.pdf"),
                temp_pdf_path
            )

            # If password is provided, encrypt the PDF
            if password:
                logger.info("Encrypting PDF with password")
                if not encrypt_pdf(temp_pdf_path, output_path, password):
                    return jsonify({'error': 'Failed to encrypt PDF'}), 500
            else:
                # If no password, just use the converted file
                os.rename(temp_pdf_path, output_path)
                
            logger.info(f"Conversion successful, output file: {output_path}")
            return jsonify({'filename': output_filename}), 200
            
        except Exception as e:
            logger.error(f"Error during conversion: {str(e)}")
            return jsonify({'error': str(e)}), 500
            
        finally:
            # Clean up temporary files
            try:
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)
                logger.info("Cleaned up temporary files")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary files: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error in conversion endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        logger.info(f"Download request for file: {filename}")
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return jsonify({'error': 'File not found'}), 404
            
        logger.info(f"Sending file: {file_path}")
        return send_file(
            file_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"Error in download: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
