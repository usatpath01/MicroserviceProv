import logging
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import mysql.connector
import os
import time
from mysql.connector import Error


app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)


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

def init_db():
    try:
        connection = mysql.connector.connect(
            host="user_db",
            user="root",
            password="insecure_password",
            database="users"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create users table if it doesn't exist
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
            )
            """)
            
            connection.commit()
            print("Database initialized successfully")
    
    except Error as e:
        print(f"Error initializing database: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
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
    app.logger.info(f"Received {request.method} request for /api/v1/users/register")
    app.logger.info(f"Request headers: {request.headers}")
    app.logger.info(f"Request body: {request.get_data(as_text=True)}")
    
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        app.logger.info(f"Attempting to register user: {username}, email: {email}")
        
        if not username or not password or not email:
            app.logger.warning("Missing required fields in registration attempt")
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        db = mysql.connector.connect(
            host="user_db",
            user="root",
            password="insecure_password",
            database="users"
        )
        cursor = db.cursor()
        try:
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            db.commit()
            
            app.logger.info(f"User {username} registered successfully")
            
            cursor.execute("SELECT id, username, email FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            return jsonify({
                "status": "success",
                "message": "User registered successfully",
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2]
                }
            }), 201
        except mysql.connector.IntegrityError as e:
            app.logger.error(f"IntegrityError during registration: {str(e)}")
            return jsonify({"status": "error", "message": f"Username or email already exists: {str(e)}"}), 409
        except Exception as e:
            app.logger.error(f"Database error during registration: {str(e)}")
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500
        finally:
            cursor.close()
            db.close()
    except Exception as e:
        app.logger.error(f"Server error during registration: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500




@app.route('/api/v1/users/login', methods=['POST'])
def login():
    app.logger.info(f"Received {request.method} request for /api/v1/users/login")
    app.logger.info(f"Request headers: {request.headers}")
    app.logger.info(f"Request body: {request.get_data(as_text=True)}")
    
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        app.logger.info(f"Parsed data: {data}")
        
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"status": "error", "message": "Missing username or password"}), 400
        
        # Your existing login logic here
        # For example:
        cursor = db.cursor()
        query = "SELECT id, username, email FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return jsonify({
                "status": "success",
                "message": "Login successful",
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2]
                }
            }), 200
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    except Exception as e:
        app.logger.error(f"Error in login route: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    app.logger.info("Health check request received")
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.logger.info("Starting User Service...")
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)