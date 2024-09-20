# user_service/app.py
from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(
    host="user_db",
    user="root",
    password=os.environ.get('DB_PASSWORD', 'insecure_password'),
    database="users"
)

# Create a default user
def create_default_user():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = 'testuser'")
    if cursor.fetchone() is None:
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(query, ('testuser', 'pass1234', 'testuser@example.com'))
        db.commit()
    cursor.close()

create_default_user()

# ... rest of the code remains the same ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)