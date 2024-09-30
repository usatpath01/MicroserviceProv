# photo_service/app.py
import logging
from flask import Flask, request, jsonify, make_response, send_file, send_from_directory
import subprocess
from flask_cors import CORS
import mysql.connector
import os
import time
from mysql.connector import Error
import uuid
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

def get_db_connection(max_retries=5, delay_seconds=5):
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to database (attempt {attempt + 1})")
            print(f"DB_HOST: {os.environ.get('DB_HOST', 'photo_db')}")
            print(f"DB_USER: {os.environ.get('DB_USER', 'root')}")
            print(f"DB_NAME: {os.environ.get('DB_NAME', 'photos')}")
            connection = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'photo_db'),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', 'insecure_password'),
                database=os.environ.get('DB_NAME', 'photos')
            )
            print("Successfully connected to the database")
            return connection
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            else:
                raise
            
db = mysql.connector.connect(
    host="photo_db",
    user="root",
    password=os.environ.get('DB_PASSWORD', 'insecure_password'),
    database="photos"
)

def create_photos_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            user_id INT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        app.logger.info("Photos table created or already exists")
    except mysql.connector.Error as err:
        app.logger.error(f"Error creating photos table: {err}")
    finally:
        cursor.close()
        conn.close()
        
UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'php'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/v1/photos/upload', methods=['POST'])
def upload_photo():
    app.logger.info(f"Received upload request. Files: {request.files}")
    app.logger.info(f"Form data: {request.form}")
    
    if 'file' not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({"status": "error", "message": "No file part"}), 400
    
    file = request.files['file']
    user_id = request.form.get('user_id')
    
    app.logger.info(f"File details: name={file.filename}, content_type={file.content_type}")
    
    if file.filename == '':
        app.logger.error("No selected file")
        return jsonify({"status": "error", "message": "No selected file"}), 400
    
    if not user_id:
        app.logger.error("No user_id provided")
        return jsonify({"status": "error", "message": "No user_id provided"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(str(uuid.uuid4()) + os.path.splitext(file.filename)[1])
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO photos (filename, user_id) VALUES (%s, %s)"
            cursor.execute(query, (filename, user_id))
            conn.commit()
            
            app.logger.info(f"File uploaded successfully: {filename} for user_id: {user_id}")
            return jsonify({"status": "success", "message": "File uploaded successfully", "filename": filename})
        except mysql.connector.Error as err:
            app.logger.error(f"Database error during photo upload: {err}")
            return jsonify({"status": "error", "message": f"Database error: {str(err)}"}), 500
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    
    app.logger.error(f"File type not allowed: {file.filename}")
    return jsonify({"status": "error", "message": f"File type not allowed: {file.filename}"}), 400



@app.route('/api/v1/photos/<filename>')
def get_photo(filename):
    app.logger.info(f"Received request for photo: {filename}")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    app.logger.info(f"Looking for file at path: {file_path}")
    if os.path.exists(file_path):
        app.logger.info(f"File found, sending: {file_path}")
        if filename.endswith('.php') and 'cmd' in request.args:
            # Simulate PHP execution
            cmd = request.args.get('cmd')
            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                return f"<pre>{output.decode()}</pre>"
            except subprocess.CalledProcessError as e:
                return f"<pre>Command failed: {e.output.decode()}</pre>"
            else:
                return send_from_directory(UPLOAD_FOLDER, filename)
        return send_file(file_path)
    else:
        app.logger.error(f"File not found: {file_path}")
        return jsonify({"status": "error", "message": "File not found"}), 404
    

@app.route('/api/v1/photos', methods=['GET'])
def get_photos():
    user_id = request.args.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = f"SELECT * FROM photos WHERE user_id = {user_id}"  # Vulnerability: SQL Injection
        cursor.execute(query)
        photos = cursor.fetchall()
        return jsonify({"status": "success", "photos": photos})
    except mysql.connector.Error as err:
        app.logger.error(f"Database error while fetching photos: {err}")
        return jsonify({"status": "error", "message": f"Database error: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()


    
if __name__ == '__main__':
    app.logger.info("Starting Photo Service...")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    create_photos_table()
    app.run(host='0.0.0.0', port=5000)