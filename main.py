import os.path

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
HOME_PATH = os.path.expanduser('~')
UPLOAD_FOLDER_LOCATION = os.path.join(HOME_PATH, 'AirNode/Uploads')
os.makedirs(UPLOAD_FOLDER_LOCATION, exist_ok=True)

# List files
@app.route('/api/files', methods=['GET'])
def get_files():
    # List files
    uploaded_files = os.listdir(UPLOAD_FOLDER_LOCATION)
    return jsonify(uploaded_files)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file was supplied.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file.save(os.path.join(UPLOAD_FOLDER_LOCATION, file.filename))
        return jsonify({'message': 'File uploaded successfully'}), 200

# API: Download file
@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER_LOCATION, filename)

# API: Delete file
@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    os.remove(os.path.join(UPLOAD_FOLDER_LOCATION, filename))
    return jsonify({'message': 'File deleted successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)