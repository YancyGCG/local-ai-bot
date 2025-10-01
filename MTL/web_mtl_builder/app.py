from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify, send_from_directory
import os
import logging
import socket
import zipfile
import io
from werkzeug.utils import secure_filename
from mtl_pdf_generator import generate_mtl_document

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = os.path.abspath('uploads')
GENERATED_FOLDER = os.path.abspath('generated_mtls')
ALLOWED_EXTENSIONS = {'json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/download/<filename>')
def download_file(filename):
    """Download a specific generated file."""
    return send_from_directory(app.config['GENERATED_FOLDER'], filename, as_attachment=True)

@app.route('/generated')
def generated_files():
    """Show list of all generated files."""
    files = []
    for f in os.listdir(app.config['GENERATED_FOLDER']):
        if os.path.isfile(os.path.join(app.config['GENERATED_FOLDER'], f)):
            files.append(f)
    return render_template('files.html', files=files)

@app.route('/', methods=['GET', 'POST'])
def index():
    logger.debug(f"Request received: {request.method} from {request.remote_addr}")
    if request.method == 'POST':
        mtl_type = request.form.get('mtl_type')
        revision = request.form.get('revision', '1')
        filetype = request.form.get('filetype', 'docx')
        logger.debug(f"Selected MTL type: {mtl_type}, revision: {revision}, filetype: {filetype}")
        
        # Validate inputs
        if not mtl_type:
            return render_template('index.html', error="Please select an MTL type")
        
        # Check if file was uploaded
        if 'json_files' not in request.files:
            logger.debug("No file part in request")
            return render_template('index.html', error="No file selected")
        
        file = request.files['json_files']
        logger.debug(f"File received: {file.filename}")
        
        # Check if file is valid
        if not file or file.filename == '':
            logger.debug("No file selected")
            return render_template('index.html', error="No file selected")
        
        if not allowed_file(file.filename):
            return render_template('index.html', error="Invalid file type. Please upload a JSON file.")
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        logger.debug(f"Saved file: {file_path}")
        
        try:
            # Generate the MTL document
            result = generate_mtl_document(file_path, mtl_type, app.config['GENERATED_FOLDER'], 
                                          revision=revision, filetype=filetype)
            
            # Determine which file to serve based on filetype
            if filetype == 'docx' and 'docx' in result:
                logger.info(f"Serving DOCX file: {result['docx']}")
                return send_file(result['docx'], as_attachment=True)
            elif filetype == 'pdf' and 'pdf' in result:
                logger.info(f"Serving PDF file: {result['pdf']}")
                return send_file(result['pdf'], as_attachment=True)
            else:
                error_msg = f"Failed to generate MTL {filetype.upper()} file. Please check the server logs."
                logger.error(error_msg)
                return render_template('index.html', error=error_msg)
        except Exception as e:
            logger.error(f"Error generating MTL file: {e}", exc_info=True)
            return render_template('index.html', error=f"Error generating MTL file: {str(e)}")
    
    return render_template('index.html')

if __name__ == '__main__':
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        logger.info(f"Server hostname: {hostname}")
        logger.info(f"Server local IP: {local_ip}")
    except Exception as e:
        logger.warning(f"Could not determine local IP: {e}")
        local_ip = "unknown"
    
    logger.info(f"Starting server on http://0.0.0.0:5555")
    logger.info(f"Try accessing: http://{local_ip}:5555 or http://localhost:5555")
    logger.info(f"External access: http://192.168.100.33:8080 or http://100.70.125.100:8080")
    
    # Show available routes
    logger.info("Available routes:")
    for rule in app.url_map.iter_rules():
        logger.info(f"{rule}")
    
    app.run(debug=True, port=5555, host='0.0.0.0')
