import logging
from flask import Flask, request, jsonify
import mysql.connector
import os
import time

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

def get_db_connection(max_retries=5, delay_seconds=5):
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to database (attempt {attempt + 1})")
            print(f"DB_HOST: {os.environ.get('DB_HOST', 'user_db')}")
            print(f"DB_USER: {os.environ.get('DB_USER', 'root')}")
            print(f"DB_NAME: {os.environ.get('DB_NAME', 'users')}")
            connection = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'user_db'),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', 'insecure_password'),
                database=os.environ.get('DB_NAME', 'users')
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

db = get_db_connection()

@app.route('/api/v1/users/test-db-connection', methods=['GET'])
def test_db_connection():
    app.logger.info("Received request for test-db-connection")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": "Database connection successful"}), 200
    except mysql.connector.Error as err:
        return jsonify({"status": "error", "message": f"Database connection failed: {err}"}), 500


@app.route('/api/v1/users/register', methods=['POST'])
def register():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        
        if not username or not password or not email:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        cursor = db.cursor()
        try:
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            db.commit()
            
            cursor.execute("SELECT id, username, email, is_admin FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            return jsonify({
                "status": "success",
                "message": "User registered successfully",
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "is_admin": user[3]
                }
            }), 201
        except mysql.connector.IntegrityError as e:
            return jsonify({"status": "error", "message": f"Username or email already exists: {str(e)}"}), 409
        except Exception as e:
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500
        finally:
            cursor.close()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

@app.route('/api/v1/users/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        cursor = db.cursor()
        query = f"SELECT id, username, email, is_admin FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return jsonify({
                "status": "success",
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "is_admin": user[3]
                }
            })
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.logger.info("Starting User Service...")
    app.run(host='0.0.0.0', port=5000, debug=True)