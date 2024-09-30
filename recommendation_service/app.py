from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import logging
from bson.json_util import loads

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

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
    app.logger.info(f"Received recommendation request for user_id: {user_id}")
    
    if not user_id:
        return jsonify({"status": "error", "message": "Missing user_id"}), 400

    user_id = request.args.get('user_id')
    app.logger.info(f"Received recommendation request for user_id: {user_id}")
    
    if not user_id:
        return jsonify({"status": "error", "message": "Missing user_id"}), 400

    try:
        # VULNERABILITY: NoSQL Injection
        # DO NOT USE THIS IN PRODUCTION
        # Convert the user_id string to a MongoDB query object
        query = {"user_id": loads(user_id)}
        app.logger.debug(f"Query: {query}")
        
        # SECURE ALTERNATIVE (commented out):
        # query = {"user_id": str(user_id)}
        
        users = list(db.users.find(query))
        app.logger.debug(f"Matching users: {users}")

        if not users:
            app.logger.info(f"No users found for query: {query}")
            return jsonify({"status": "success", "recommendations": [], "message": "No matching users found"}), 200

        recommendations = []
        for user in users:
            preferences = user.get('preferences', {})
            app.logger.debug(f"User preferences: {preferences}")

            if preferences:
                user_recommendations = list(db.books.find(preferences).limit(5))
                recommendations.extend(user_recommendations)

        # Remove duplicates and limit to 10 recommendations
        unique_recommendations = list({rec['title']: rec for rec in recommendations}.values())[:10]

        # Remove ObjectId from recommendations for JSON serialization
        for rec in unique_recommendations:
            rec['_id'] = str(rec['_id'])

        return jsonify({
            "status": "success", 
            "recommendations": unique_recommendations,
            "affected_users": len(users)
        }), 200
    except Exception as e:
        app.logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({"status": "error", "message": "An error occurred while processing your request"}), 500

@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    # WARNING: This function lacks proper input validation for educational purposes.
    # DO NOT use this code in a production environment under any circumstances.

    app.logger.info(f"Received update preferences request. Data: {request.get_data(as_text=True)}")
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON data received"}), 400
    
    user_id = data.get('user_id')
    preferences = data.get('preferences')
    
    if not user_id or not preferences:
        return jsonify({"status": "error", "message": "Missing user_id or preferences"}), 400

    try:
        # VULNERABILITY: No input validation
        # DO NOT USE THIS IN PRODUCTION
        result = db.users.update_one(
            {"user_id": user_id},
            {"$set": {"preferences": preferences}},
            upsert=True
        )
        
        # SECURE ALTERNATIVE (commented out):
        # if not isinstance(preferences, dict):
        #     return jsonify({"status": "error", "message": "Invalid preferences format"}), 400
        # validated_preferences = {k: v for k, v in preferences.items() if isinstance(k, str) and isinstance(v, str)}
        # result = db.users.update_one(
        #     {"user_id": str(user_id)},
        #     {"$set": {"preferences": validated_preferences}},
        #     upsert=True
        # )
        
        app.logger.info(f"Update result: {result.raw_result}")
        return jsonify({"status": "success", "message": "Preferences updated"}), 200
    except Exception as e:
        app.logger.error(f"Error updating preferences: {str(e)}")
        return jsonify({"status": "error", "message": "An error occurred while processing your request"}), 500


@app.route('/populate_books', methods=['POST'])
def populate_books():
    try:
        sample_books = [
            {"title": "Dune", "author": "Frank Herbert", "category": "books", "genre": "sci-fi"},
            {"title": "Neuromancer", "author": "William Gibson", "category": "books", "genre": "sci-fi"},
            {"title": "1984", "author": "George Orwell", "category": "books", "genre": "dystopian"},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "books", "genre": "fiction"},
            {"title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "books", "genre": "fantasy"},
            {"title": "Pride and Prejudice", "author": "Jane Austen", "category": "books", "genre": "romance"},
            {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "books", "genre": "fiction"},
            {"title": "Brave New World", "author": "Aldous Huxley", "category": "books", "genre": "dystopian"},
            {"title": "The Foundation Trilogy", "author": "Isaac Asimov", "category": "books", "genre": "sci-fi"},
            {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "category": "books", "genre": "fantasy"}
        ]
        
        result = db.books.insert_many(sample_books)
        return jsonify({"status": "success", "message": f"Added {len(result.inserted_ids)} books to the database"}), 200
    except Exception as e:
        app.logger.error(f"Error populating books: {str(e)}")
        return jsonify({"status": "error", "message": "An error occurred while processing your request"}), 500
    
    
@app.route('/debug/books', methods=['GET'])
def debug_books():
    try:
        books = list(db.books.find({}, {'_id': 0}))  # Exclude _id field
        return jsonify({"status": "success", "books": books}), 200
    except Exception as e:
        app.logger.error(f"Error retrieving books: {str(e)}")
        return jsonify({"status": "error", "message": "An error occurred while processing your request"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)