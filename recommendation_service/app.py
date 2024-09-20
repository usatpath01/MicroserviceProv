# recommendation_service/app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Get MongoDB connection string from environment variable
mongo_uri = os.environ.get('DB_CONNECTION_STRING')
app.logger.info(f"MongoDB URI: {mongo_uri}")

try:
    client = MongoClient(mongo_uri)
    db = client.get_database()
    app.logger.info("Successfully connected to MongoDB")
except Exception as e:
    app.logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

@app.route('/recommend', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"status": "error", "message": "Missing user_id"}), 400

    try:
        # Vulnerability: NoSQL Injection
        query = {"user_id": user_id}
        recommendations = list(db.recommendations.find(query))
        
        # Vulnerability: Sensitive Data Exposure
        return jsonify({"status": "success", "recommendations": recommendations})
    except Exception as e:
        app.logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    data = request.json
    user_id = data.get('user_id')
    preferences = data.get('preferences')
    
    if not user_id or not preferences:
        return jsonify({"status": "error", "message": "Missing user_id or preferences"}), 400

    try:
        # Vulnerability: No input validation
        db.recommendations.update_one({"user_id": user_id}, {"$set": {"preferences": preferences}}, upsert=True)
        
        return jsonify({"status": "success", "message": "Preferences updated"})
    except Exception as e:
        app.logger.error(f"Error updating preferences: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)