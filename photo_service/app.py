# photo_service/app.py
from flask import Flask, request, jsonify, send_file
import mysql.connector
import os
import uuid

app = Flask(__name__)

db = mysql.connector.connect(
    host="photo_db",
    user="root",
    password=os.environ.get('DB_PASSWORD', 'insecure_password'),
    database="photos"
)

UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400
    
    # Vulnerability: Insecure File Upload
    if file:
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        cursor = db.cursor()
        query = "INSERT INTO photos (filename, user_id) VALUES (%s, %s)"
        cursor.execute(query, (filename, request.form['user_id']))
        db.commit()
        
        return jsonify({"status": "success", "message": "File uploaded successfully", "filename": filename})

@app.route('/photo/<filename>')
def get_photo(filename):
    # Vulnerability: Path Traversal
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path)

@app.route('/photos', methods=['GET'])
def get_photos():
    user_id = request.args.get('user_id')
    cursor = db.cursor()
    query = f"SELECT * FROM photos WHERE user_id = {user_id}"  # Vulnerability: SQL Injection
    cursor.execute(query)
    photos = cursor.fetchall()
    return jsonify({"status": "success", "photos": photos})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)