# photo_service/app.py
import logging
from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
import mysql.connector
import os
import time
from mysql.connector import Error
import uuid

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
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO photos (filename, user_id) VALUES (%s, %s)"
            cursor.execute(query, (filename, request.form['user_id']))
            conn.commit()
            
            return jsonify({"status": "success", "message": "File uploaded successfully", "filename": filename})
        except mysql.connector.Error as err:
            app.logger.error(f"Database error during photo upload: {err}")
            return jsonify({"status": "error", "message": f"Database error: {str(err)}"}), 500
        finally:
            cursor.close()
            conn.close()

@app.route('/photo/<filename>')
def get_photo(filename):
    # Vulnerability: Path Traversal
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path)

@app.route('/photos', methods=['GET'])
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
    create_photos_table()
    app.run(host='0.0.0.0', port=5000)