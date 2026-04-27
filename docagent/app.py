from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import logging
import time

from docagent.extractors import FileExtractor, WebExtractor
from docagent.agent.graph import run_agent
from docagent.exporters.markdown_exporter import export_to_markdown
from docagent.exporters.pdf_exporter import export_to_pdf
from docagent.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'py', 'js', 'java', 'go', 'ts', 'cpp', 'c', 'rb', 'php', 'md', 'txt', 'pdf'}
ALLOWED_FORMATS = {'markdown', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_file_safely(path):
    """Remove file with retry for Windows file locking issues"""
    for _ in range(3):
        try:
            os.unlink(path)
            return True
        except PermissionError:
            time.sleep(0.1)
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_document():
    try:
        output_format = 'markdown'
        output_filename = 'document'

        # Handle file upload (multipart/form-data)
        if request.content_type and 'multipart/form-data' in request.content_type:
            if 'file' in request.files:
                file = request.files['file']
                if file.filename == '':
                    return jsonify({'error': 'No file selected'}), 400

                if not allowed_file(file.filename):
                    return jsonify({'error': 'File type not allowed'}), 400

                # Get format from form data
                output_format = request.form.get('format', 'markdown')
                if output_format not in ALLOWED_FORMATS:
                    return jsonify({'error': f'Invalid format. Allowed: {ALLOWED_FORMATS}'}), 400

                # Save to temporary file
                tmp_path = None
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=secure_filename(file.filename)) as tmp:
                        file.save(tmp.name)
                        tmp_path = tmp.name

                    extractor = FileExtractor()
                    content = extractor.extract(tmp_path)
                finally:
                    if tmp_path:
                        remove_file_safely(tmp_path)
            else:
                return jsonify({'error': 'No input provided'}), 400

        # Handle JSON request (URL input)
        elif request.content_type and 'application/json' in request.content_type:
            data = request.get_json()
            output_format = data.get('format', 'markdown')
            if output_format not in ALLOWED_FORMATS:
                return jsonify({'error': f'Invalid format. Allowed: {ALLOWED_FORMATS}'}), 400

            output_filename = data.get('filename', 'document')

            # Handle URL input
            if 'url' in data and data['url']:
                extractor = WebExtractor()
                result = extractor.extract(data['url'])
                content = result.get('content', '')
            else:
                return jsonify({'error': 'No input provided'}), 400
        else:
            return jsonify({'error': 'Unsupported content type'}), 415

        # Run agent to generate document
        generated_doc = run_agent(content)

        # Use a fixed directory instead of TemporaryDirectory to avoid cleanup issues
        tmpdir = tempfile.mkdtemp()
        try:
            if output_format == 'pdf':
                output_path = os.path.join(tmpdir, f"{output_filename}.pdf")
                export_to_pdf(generated_doc, output_path)
                return send_file(output_path, mimetype='application/pdf', as_attachment=True, download_name=f"{output_filename}.pdf")
            else:
                output_path = os.path.join(tmpdir, f"{output_filename}.md")
                export_to_markdown(generated_doc, output_path)
                return send_file(output_path, mimetype='text/markdown', as_attachment=True, download_name=f"{output_filename}.md")
        finally:
            # Clean up with retry
            try:
                for file in os.listdir(tmpdir):
                    remove_file_safely(os.path.join(tmpdir, file))
                os.rmdir(tmpdir)
            except Exception:
                pass  # Ignore cleanup errors

    except Exception as e:
        logger.exception("Error generating document")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.FLASK_ENV == 'development')
