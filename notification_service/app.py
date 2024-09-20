# notification_service/app.py
from flask import Flask, request, jsonify
import redis
import os
import json

app = Flask(__name__)
redis_client = redis.Redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379'))

@app.route('/notify', methods=['POST'])
def send_notification():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')
    
    if not user_id or not message:
        return jsonify({"status": "error", "message": "Missing user_id or message"}), 400

    # Vulnerability: Storing sensitive data in plain text
    redis_client.lpush(f"notifications:{user_id}", json.dumps({"message": message}))
    
    return jsonify({"status": "success", "message": "Notification sent"})

@app.route('/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    # Vulnerability: No authentication check
    notifications = redis_client.lrange(f"notifications:{user_id}", 0, -1)
    return jsonify({"status": "success", "notifications": [json.loads(n) for n in notifications]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)